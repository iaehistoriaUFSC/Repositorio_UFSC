from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import tempfile
from pathlib import Path


# The official VUA loader indexes whitespace-separated corpus tokens. Using a
# punctuation-splitting tokenizer here shifts target indices and corrupts input.
WORD_RE = re.compile(r"\S+", flags=re.UNICODE)


def _pos(word: str) -> str:
    lowered = word.casefold()
    if lowered.endswith("ly"):
        return "ADV"
    if lowered.endswith(("ing", "ed", "en")):
        return "VERB"
    if lowered.endswith(("ous", "ive", "al", "ful", "less", "ic", "able", "ible")):
        return "ADJ"
    return "NOUN"


def _find_checkpoint(path: Path) -> Path:
    for config in sorted(path.rglob("config.json")):
        if (config.parent / "pytorch_model.bin").is_file():
            return config.parent
    raise FileNotFoundError("MelBERT checkpoint files were not found")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args_ns = parser.parse_args(argv)
    payload = json.loads(Path(args_ns.input).read_text(encoding="utf-8"))
    repository = Path(payload["repository"]).resolve()
    checkpoint = _find_checkpoint(Path(payload["checkpoint"]).resolve())
    sys.path.insert(0, str(repository))
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    import numpy as np
    import nltk  # noqa: F401 - required by the dynamically loaded upstream code
    import scipy  # noqa: F401 - required by the dynamically loaded upstream code
    import sklearn  # noqa: F401 - required by the dynamically loaded upstream code
    import torch
    import transformers
    from transformers import AutoTokenizer

    # MelBERT imports the legacy Transformers optimizer even during inference.
    if not hasattr(transformers, "AdamW"):
        transformers.AdamW = torch.optim.AdamW

    torch.cuda.is_available = lambda: False
    torch.cuda.device_count = lambda: 0
    torch.cuda.manual_seed_all = lambda _seed: None

    from data_loader import load_test_data
    from main import WEIGHTS_NAME, load_pretrained_model, run_eval
    from run_classifier_dataset_utils import output_modes, processors
    from utils import Config

    rows = []
    for sentence in payload["sentences"]:
        matches = list(WORD_RE.finditer(sentence["text"]))
        words = [match.group(0) for match in matches]
        for word_index, (word, match) in enumerate(zip(words, matches)):
            rows.append(
                {
                    "target_id": f"{sentence['id']}#w{word_index}",
                    "sentence_id": sentence["id"],
                    "sentence_text": sentence["text"],
                    "word_index": word_index,
                    "word": word,
                    "char_start": sentence["char_start"] + match.start(),
                    "char_end": sentence["char_start"] + match.end(),
                    "pos": _pos(word),
                }
            )

    with tempfile.TemporaryDirectory(prefix="metaphoriq-melbert-") as temp_name:
        temp = Path(temp_name)
        data_dir = temp / "data"
        data_dir.mkdir()
        with (data_dir / "test.tsv").open(
            "w", encoding="utf-8", newline=""
        ) as output:
            writer = csv.writer(output, delimiter="\t")
            writer.writerow(["index", "label", "sentence", "POS", "w_index"])
            for row in rows:
                writer.writerow(
                    [
                        row["target_id"],
                        "0",
                        " ".join(row["sentence_text"].split()),
                        row["pos"],
                        row["word_index"],
                    ]
                )
        try:
            config = Config(main_conf_path=str(checkpoint))
        except Exception:
            config = Config(main_conf_path=str(repository))
        config.bert_model = str(checkpoint)
        config.log_dir = str(checkpoint)
        config.data_dir = str(data_dir)
        config.task_name = "vua"
        config.model_type = "MELBERT"
        config.do_train = False
        config.do_eval = False
        config.do_test = True
        config.do_lower_case = getattr(config, "do_lower_case", False)
        config.eval_batch_size = int(getattr(config, "eval_batch_size", 8) or 8)
        config.max_seq_length = int(getattr(config, "max_seq_length", 150) or 150)
        config.no_cuda = True
        config.seed = int(getattr(config, "seed", 42) or 42)
        config.device = torch.device("cpu")
        config.n_gpu = 0
        random.seed(config.seed)
        np.random.seed(config.seed)
        torch.manual_seed(config.seed)
        processor = processors["vua"]()
        label_list = processor.get_labels()
        config.num_labels = len(label_list)
        tokenizer = AutoTokenizer.from_pretrained(
            config.bert_model,
            do_lower_case=config.do_lower_case,
            local_files_only=True,
        )
        model = load_pretrained_model(config)
        state = torch.load(
            str(checkpoint / WEIGHTS_NAME),
            map_location=config.device,
            weights_only=False,
        )
        target_model = model.module if hasattr(model, "module") else model
        incompatible = target_model.load_state_dict(state, strict=False)
        unexpected = [
            name
            for name in incompatible.unexpected_keys
            if not name.endswith("embeddings.position_ids")
        ]
        if incompatible.missing_keys or unexpected:
            raise RuntimeError(
                "MelBERT checkpoint is incompatible with this runtime: "
                f"missing={incompatible.missing_keys}, unexpected={unexpected}"
            )
        model.to(config.device)

        class Logger:
            def info(self, message):
                print(str(message), file=sys.stderr)

        all_guids, loader = load_test_data(
            config,
            Logger(),
            processor,
            "vua",
            label_list,
            tokenizer,
            output_modes["vua"],
        )
        predictions = run_eval(
            config,
            Logger(),
            model,
            loader,
            all_guids,
            "vua",
            return_preds=True,
        )
    output_rows = []
    for row, prediction in zip(rows, predictions):
        is_metaphor = int(prediction) == 1
        output_rows.append(
            {
                **row,
                "model_id": "melbert",
                "score": 1.0 if is_metaphor else 0.0,
                "is_metaphor": is_metaphor,
                "score_semantics": "binary_class_decision_no_probability",
            }
        )
    Path(args_ns.output).write_text(
        json.dumps({"predictions": output_rows}, ensure_ascii=False),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
