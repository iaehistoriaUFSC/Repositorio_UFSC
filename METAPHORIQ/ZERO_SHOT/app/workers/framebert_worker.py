from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


WORD_RE = re.compile(r"\w+(?:['’\-]\w+)*|[^\w\s]", flags=re.UNICODE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    repository = Path(payload["repository"]).resolve()
    article_text = "\n".join(item["text"] for item in payload["sentences"])
    with tempfile.TemporaryDirectory(prefix="metaphoriq-framebert-") as temp_name:
        temp = Path(temp_name)
        input_path = temp / "articles.json"
        input_path.write_text(
            json.dumps({"articles": article_text}, ensure_ascii=False),
            encoding="utf-8",
        )
        env = os.environ.copy()
        env["TOKENIZERS_PARALLELISM"] = "false"
        process = subprocess.run(
            [sys.executable, str(repository / "inference.py"), str(input_path)],
            cwd=repository,
            env=env,
            capture_output=True,
            text=True,
            timeout=7200,
            check=False,
        )
        predictions_path = repository / "predictions.tsv"
        if process.returncode != 0 or not predictions_path.is_file():
            raise RuntimeError(
                "FrameBERT official inference failed. "
                f"This experimental adapter may require upstream frame resources. "
                f"{process.stderr[-2000:]}"
            )
        source_tokens = []
        for sentence in payload["sentences"]:
            for word_index, match in enumerate(WORD_RE.finditer(sentence["text"])):
                source_tokens.append(
                    {
                        "sentence_id": sentence["id"],
                        "sentence_text": sentence["text"],
                        "word_index": word_index,
                        "word": match.group(0),
                        "char_start": sentence["char_start"] + match.start(),
                        "char_end": sentence["char_start"] + match.end(),
                    }
                )
        rows = []
        with predictions_path.open(encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source, delimiter="\t")
            for index, row in enumerate(reader):
                aligned = (
                    source_tokens[index]
                    if index < len(source_tokens)
                    else {
                        "sentence_id": "framebert-document",
                        "sentence_text": article_text,
                        "word_index": index,
                        "word": row.get("Tokens") or "",
                        "char_start": None,
                        "char_end": None,
                    }
                )
                real = str(row.get("Real_metaphors") or "0") == "1"
                rows.append(
                    {
                        **aligned,
                        "model_id": "framebert",
                        "score": 1.0 if real else 0.0,
                        "is_metaphor": real,
                        "frame_label": row.get("Frame_label") or None,
                        "score_semantics": "binary_class_decision_no_probability",
                    }
                )
    Path(args.output).write_text(
        json.dumps({"predictions": rows}, ensure_ascii=False), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
