from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"\w+(?:['’\-]\w+)*|[^\w\s]", flags=re.UNICODE)


def _words(text: str) -> tuple[list[str], list[tuple[int, int]]]:
    matches = list(WORD_RE.finditer(text))
    return [match.group(0) for match in matches], [
        (match.start(), match.end()) for match in matches
    ]


def detect(payload: dict) -> dict:
    import torch
    from transformers import AutoModelForTokenClassification, AutoTokenizer

    model_path = payload["model_path"]
    model_id = payload["model_id"]
    positive_label = int(payload.get("positive_label_id", 1))
    threshold = float(payload.get("threshold", 0.5))
    tokenizer = AutoTokenizer.from_pretrained(
        model_path, local_files_only=True, use_fast=True, add_prefix_space=True
    )
    model = AutoModelForTokenClassification.from_pretrained(
        model_path, local_files_only=True
    )
    model.eval()
    results = []
    for sentence in payload["sentences"]:
        words, offsets = _words(sentence["text"])
        if not words:
            continue
        encoded = tokenizer(
            words,
            is_split_into_words=True,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )
        with torch.inference_mode():
            logits = model(**encoded).logits[0]
            probabilities = torch.softmax(logits, dim=-1)[:, positive_label]
        by_word: dict[int, list[float]] = {}
        for token_index, word_id in enumerate(encoded.word_ids(batch_index=0)):
            if word_id is not None:
                by_word.setdefault(word_id, []).append(
                    float(probabilities[token_index].item())
                )
        for word_index, word in enumerate(words):
            score = max(by_word.get(word_index, [0.0]))
            start, end = offsets[word_index]
            results.append(
                {
                    "model_id": model_id,
                    "sentence_id": sentence["id"],
                    "sentence_text": sentence["text"],
                    "word_index": word_index,
                    "word": word,
                    "char_start": sentence["char_start"] + start,
                    "char_end": sentence["char_start"] + end,
                    "score": round(score, 6),
                    "is_metaphor": score >= threshold,
                    "score_semantics": "model_softmax_not_calibrated",
                }
            )
    return {"predictions": results}


def embed(payload: dict) -> dict:
    import torch
    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        payload["model_path"], local_files_only=True, use_fast=True
    )
    model = AutoModel.from_pretrained(payload["model_path"], local_files_only=True)
    model.eval()
    vectors = []
    batch_size = int(payload.get("batch_size", 8))
    texts = payload["texts"]
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        encoded = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt",
        )
        with torch.inference_mode():
            hidden = model(**encoded).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1)
            pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
            pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
        vectors.extend(pooled.cpu().tolist())
    return {"vectors": vectors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = embed(payload) if payload.get("action") == "embed" else detect(payload)
    Path(args.output).write_text(
        json.dumps(result, ensure_ascii=False), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

