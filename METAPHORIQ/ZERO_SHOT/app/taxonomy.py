from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from app.paths import resource_path


def _read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "").casefold()
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", re.sub(r"[^\w]+", " ", value)).strip()


def _features(value: str) -> list[str]:
    normalized = _normalize(value)
    words = [word for word in normalized.split() if len(word) > 1]
    features = [f"w:{word}" for word in words]
    features += [f"b:{a}_{b}" for a, b in zip(words, words[1:])]
    compact = normalized.replace(" ", "_")
    features += [
        f"c:{compact[index:index + 4]}"
        for index in range(max(0, len(compact) - 3))
    ]
    return features


@dataclass(frozen=True)
class TaxonomyPrediction:
    class_id: str
    class_label: str
    family_id: str
    family_label: str
    similarity: float
    margin: float
    method: str


class LexicalPrototypeClassifier:
    method = "annotated-sample-word-char-tfidf-v1"

    def __init__(self) -> None:
        root = resource_path("data", "reference")
        self.families = {
            item["family_id"]: item for item in _read_jsonl(root / "families.jsonl")
        }
        classes = _read_jsonl(root / "taxonomy_nodes.jsonl")
        self.classes = {
            item["class_id"]: item for item in classes if item.get("assignable")
        }
        examples = [
            item
            for item in _read_jsonl(root / "examples.jsonl")
            if not item.get("needs_review") and item.get("class_id") in self.classes
        ]
        documents: dict[str, list[str]] = defaultdict(list)
        for item in examples:
            documents[item["class_id"]].append(item.get("text") or "")
        for class_id, item in self.classes.items():
            documents[class_id].append(
                " ".join(
                    [
                        item.get("label") or "",
                        item.get("description") or "",
                        " ".join(item.get("terms") or []),
                    ]
                )
            )
        raw_counts = {
            class_id: Counter(
                feature
                for document in class_documents
                for feature in _features(document)
            )
            for class_id, class_documents in documents.items()
        }
        document_frequency: Counter[str] = Counter()
        for counts in raw_counts.values():
            document_frequency.update(counts.keys())
        total = len(raw_counts)
        self.idf = {
            feature: math.log((1 + total) / (1 + frequency)) + 1
            for feature, frequency in document_frequency.items()
        }
        self.vectors = {
            class_id: self._normalize_vector(
                {
                    feature: (1 + math.log(count)) * self.idf[feature]
                    for feature, count in counts.items()
                }
            )
            for class_id, counts in raw_counts.items()
        }

    @staticmethod
    def _normalize_vector(vector: dict[str, float]) -> dict[str, float]:
        norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
        return {key: value / norm for key, value in vector.items()}

    def _query_vector(self, text: str) -> dict[str, float]:
        counts = Counter(_features(text))
        return self._normalize_vector(
            {
                feature: (1 + math.log(count)) * self.idf.get(feature, 1.0)
                for feature, count in counts.items()
            }
        )

    def classify(self, text: str, top_k: int = 5) -> list[TaxonomyPrediction]:
        query = self._query_vector(text)
        scores = []
        for class_id, vector in self.vectors.items():
            score = sum(
                value * vector.get(feature, 0.0)
                for feature, value in query.items()
            )
            scores.append((score, class_id))
        scores.sort(reverse=True)
        top = scores[: max(1, top_k)]
        second = top[1][0] if len(top) > 1 else 0.0
        predictions = []
        for index, (score, class_id) in enumerate(top):
            item = self.classes[class_id]
            family = self.families[item["family_id"]]
            predictions.append(
                TaxonomyPrediction(
                    class_id=class_id,
                    class_label=item["label"],
                    family_id=item["family_id"],
                    family_label=family["label"],
                    similarity=round(score, 6),
                    margin=round(score - second, 6) if index == 0 else 0.0,
                    method=self.method,
                )
            )
        return predictions

    def fingerprint(self) -> str:
        digest = hashlib.sha256()
        for class_id in sorted(self.vectors):
            digest.update(class_id.encode())
            for key, value in sorted(self.vectors[class_id].items()):
                digest.update(f"{key}:{value:.8f}".encode())
        return digest.hexdigest()


def accepted_examples() -> list[dict]:
    return [
        item
        for item in _read_jsonl(
            resource_path("data", "reference", "examples.jsonl")
        )
        if not item.get("needs_review")
    ]


def cosine(left: Iterable[float], right: Iterable[float]) -> float:
    left_values = list(left)
    right_values = list(right)
    dot = sum(a * b for a, b in zip(left_values, right_values))
    left_norm = math.sqrt(sum(value * value for value in left_values))
    right_norm = math.sqrt(sum(value * value for value in right_values))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0

