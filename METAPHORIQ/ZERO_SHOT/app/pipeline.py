from __future__ import annotations

import csv
import gzip
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from app import __version__
from app.chronology import period_for_year
from app.models import (
    model_path,
    reference_fingerprint,
    registry_by_id,
    status,
)
from app.paths import cache_root
from app.taxonomy import (
    LexicalPrototypeClassifier,
    TaxonomyPrediction,
    accepted_examples,
    cosine,
)


Progress = Callable[[str], None]


@dataclass(frozen=True)
class PipelineConfig:
    model_ids: tuple[str, ...]
    ensemble_rule: str = "majority"
    detection_threshold: float = 0.5
    taxonomy_method: str = "lexical"
    taxonomy_top_k: int = 5
    document_year: int | None = None


def segment_sentences(text: str) -> list[dict]:
    sentences = []
    pattern = re.compile(r"[^.!?\n]+(?:[.!?]+|(?=\n|$))")
    for match in pattern.finditer(text):
        chunk = match.group(0)
        stripped = chunk.strip()
        if not stripped:
            continue
        leading = len(chunk) - len(chunk.lstrip())
        start = match.start() + leading
        sentences.append(
            {
                "id": f"sentence-{len(sentences) + 1:05d}",
                "text": stripped,
                "char_start": start,
                "char_end": start + len(stripped),
            }
        )
    if not sentences and text.strip():
        stripped = text.strip()
        start = text.find(stripped)
        sentences.append(
            {
                "id": "sentence-00001",
                "text": stripped,
                "char_start": start,
                "char_end": start + len(stripped),
            }
        )
    return sentences


def _worker_command(worker: str, input_path: Path, output_path: Path) -> list[str]:
    if getattr(sys, "frozen", False):
        return [
            sys.executable,
            "--worker",
            worker,
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ]
    return [
        sys.executable,
        "-m",
        f"app.workers.{worker}_worker",
        "--input",
        str(input_path),
        "--output",
        str(output_path),
    ]


def _run_worker(worker: str, payload: dict, timeout: int = 7200) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"metaphoriq-{worker}-") as temp_name:
        temp = Path(temp_name)
        input_path = temp / "input.json"
        output_path = temp / "output.json"
        input_path.write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )
        env = os.environ.copy()
        env["TOKENIZERS_PARALLELISM"] = "false"
        process = subprocess.run(
            _worker_command(worker, input_path, output_path),
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
            check=False,
            creationflags=(
                subprocess.CREATE_NO_WINDOW
                if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW")
                else 0
            ),
        )
        if process.returncode != 0 or not output_path.is_file():
            raise RuntimeError(
                f"{worker} worker failed ({process.returncode}): "
                f"{process.stderr[-3000:]}"
            )
        return json.loads(output_path.read_text(encoding="utf-8"))


class ModelRuntime:
    def detect(
        self,
        model_id: str,
        sentences: list[dict],
        threshold: float,
    ) -> list[dict]:
        spec = registry_by_id()[model_id]
        current = status(model_id)
        if not current.ready:
            raise RuntimeError(f"{spec['label']} is not ready: {current.detail}")
        if spec["kind"] == "huggingface":
            payload = {
                "action": "detect",
                "model_id": model_id,
                "model_path": str(current.path),
                "positive_label_id": spec["positive_label_id"],
                "threshold": threshold,
                "sentences": sentences,
            }
            return _run_worker("hf", payload)["predictions"]
        if spec["kind"] == "melbert_repository":
            payload = {
                "repository": str(current.path / "repository"),
                "checkpoint": str(current.path / "checkpoint"),
                "sentences": sentences,
            }
            return _run_worker("melbert", payload)["predictions"]
        if spec["kind"] == "framebert_repository":
            payload = {
                "repository": str(current.path / "repository"),
                "sentences": sentences,
            }
            return _run_worker("framebert", payload)["predictions"]
        raise ValueError(f"unsupported model kind: {spec['kind']}")

    def embed(self, model_id: str, texts: list[str]) -> list[list[float]]:
        spec = registry_by_id()[model_id]
        if "taxonomy_encoder" not in spec["role"]:
            raise ValueError(f"{model_id} is not registered as a taxonomy encoder")
        current = status(model_id)
        if not current.ready:
            raise RuntimeError(f"{spec['label']} is not ready: {current.detail}")
        return _run_worker(
            "hf",
            {
                "action": "embed",
                "model_id": model_id,
                "model_path": str(current.path),
                "texts": texts,
                "batch_size": 8,
            },
        )["vectors"]


class TransformerPrototypeClassifier:
    def __init__(
        self,
        model_id: str,
        runtime: ModelRuntime,
        progress: Progress,
    ) -> None:
        self.model_id = model_id
        self.runtime = runtime
        self.progress = progress
        self.lexical = LexicalPrototypeClassifier()
        self.examples = [
            item
            for item in accepted_examples()
            if item.get("class_id") in self.lexical.classes
        ]
        self.centroids = self._load_or_build()

    def _cache_path(self) -> Path:
        key = f"{self.model_id}:{reference_fingerprint()}"
        digest = __import__("hashlib").sha256(key.encode()).hexdigest()[:16]
        return cache_root() / f"taxonomy-prototypes-{digest}.json.gz"

    def _load_or_build(self) -> dict[str, list[float]]:
        path = self._cache_path()
        if path.is_file():
            with gzip.open(path, "rt", encoding="utf-8") as source:
                return json.load(source)["centroids"]
        self.progress(
            f"Building {self.model_id} taxonomy prototypes from "
            f"{len(self.examples)} accepted examples"
        )
        vectors = self.runtime.embed(
            self.model_id, [item["text"] for item in self.examples]
        )
        grouped: dict[str, list[list[float]]] = defaultdict(list)
        for item, vector in zip(self.examples, vectors):
            grouped[item["class_id"]].append(vector)
        centroids = {}
        for class_id, rows in grouped.items():
            dimensions = len(rows[0])
            centroid = [
                sum(row[index] for row in rows) / len(rows)
                for index in range(dimensions)
            ]
            norm = math.sqrt(sum(value * value for value in centroid)) or 1.0
            centroids[class_id] = [value / norm for value in centroid]
        with gzip.open(path, "wt", encoding="utf-8") as output:
            json.dump(
                {
                    "model_id": self.model_id,
                    "dataset_fingerprint": reference_fingerprint(),
                    "centroids": centroids,
                },
                output,
            )
        return centroids

    def classify(self, text: str, top_k: int) -> list[TaxonomyPrediction]:
        query = self.runtime.embed(self.model_id, [text])[0]
        scores = sorted(
            (
                (cosine(query, centroid), class_id)
                for class_id, centroid in self.centroids.items()
            ),
            reverse=True,
        )[: max(1, top_k)]
        second = scores[1][0] if len(scores) > 1 else 0.0
        result = []
        for index, (score, class_id) in enumerate(scores):
            item = self.lexical.classes[class_id]
            family = self.lexical.families[item["family_id"]]
            result.append(
                TaxonomyPrediction(
                    class_id=class_id,
                    class_label=item["label"],
                    family_id=item["family_id"],
                    family_label=family["label"],
                    similarity=round(score, 6),
                    margin=round(score - second, 6) if index == 0 else 0.0,
                    method=f"annotated-sample-{self.model_id}-centroid-v1",
                )
            )
        return result


def _ensemble(
    predictions_by_model: dict[str, list[dict]],
    model_ids: tuple[str, ...],
    rule: str,
    threshold: float,
) -> list[dict]:
    groups: dict[tuple, dict[str, dict]] = defaultdict(dict)
    for model_id, predictions in predictions_by_model.items():
        for prediction in predictions:
            key = (
                prediction.get("sentence_id"),
                prediction.get("char_start"),
                prediction.get("char_end"),
                prediction.get("word"),
            )
            groups[key][model_id] = prediction
    results = []
    for key, available in groups.items():
        model_rows = [available.get(model_id) for model_id in model_ids]
        scores = [
            float(row.get("score", 0.0)) if row else 0.0 for row in model_rows
        ]
        votes = [bool(row and row.get("is_metaphor")) for row in model_rows]
        if rule == "union":
            accepted = any(votes)
        elif rule == "intersection":
            accepted = all(votes)
        elif rule == "average":
            accepted = sum(scores) / len(scores) >= threshold
        else:
            accepted = sum(votes) >= (len(votes) // 2 + 1)
        if not accepted:
            continue
        template = next(row for row in model_rows if row)
        results.append(
            {
                "sentence_id": template["sentence_id"],
                "sentence_text": template["sentence_text"],
                "word_index": template.get("word_index"),
                "word": template.get("word"),
                "char_start": template.get("char_start"),
                "char_end": template.get("char_end"),
                "ensemble_score": round(sum(scores) / len(scores), 6),
                "positive_votes": sum(votes),
                "model_count": len(model_ids),
                "model_outputs": {
                    model_id: (
                        {
                            "score": row.get("score"),
                            "is_metaphor": row.get("is_metaphor"),
                            "score_semantics": row.get("score_semantics"),
                            "frame_label": row.get("frame_label"),
                        }
                        if row
                        else None
                    )
                    for model_id, row in zip(model_ids, model_rows)
                },
            }
        )
    return sorted(
        results,
        key=lambda item: (
            item["char_start"] if item["char_start"] is not None else 10**12,
            item["word_index"] or 0,
        ),
    )


def analyze(
    text: str,
    config: PipelineConfig,
    progress: Progress = lambda _message: None,
    runtime: ModelRuntime | None = None,
) -> dict:
    if not text.strip():
        raise ValueError("Input text is empty")
    if not config.model_ids:
        raise ValueError("Select at least one installed detection model")
    runtime = runtime or ModelRuntime()
    sentences = segment_sentences(text)
    predictions_by_model = {}
    for model_id in config.model_ids:
        progress(f"Running {registry_by_id()[model_id]['label']}")
        predictions_by_model[model_id] = runtime.detect(
            model_id, sentences, config.detection_threshold
        )
    detections = _ensemble(
        predictions_by_model,
        config.model_ids,
        config.ensemble_rule,
        config.detection_threshold,
    )
    progress(f"Classifying {len(detections)} detected spans")
    if config.taxonomy_method == "lexical":
        classifier = LexicalPrototypeClassifier()
    else:
        classifier = TransformerPrototypeClassifier(
            config.taxonomy_method, runtime, progress
        )
    period = period_for_year(config.document_year)
    rows = []
    for index, detection in enumerate(detections, start=1):
        query = f"{detection['word']} :: {detection['sentence_text']}"
        taxonomy = classifier.classify(query, config.taxonomy_top_k)
        primary = taxonomy[0]
        rows.append(
            {
                "id": f"detection-{index:06d}",
                **detection,
                "taxonomy": asdict(primary),
                "taxonomy_candidates": [asdict(item) for item in taxonomy],
                "document_year": config.document_year,
                "period": period,
                "review_status": "unreviewed_machine_prediction",
            }
        )
    manifest = {
        "schema_version": 1,
        "application_version": __version__,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "models": list(config.model_ids),
        "ensemble_rule": config.ensemble_rule,
        "detection_threshold": config.detection_threshold,
        "taxonomy_method": (
            classifier.method
            if isinstance(classifier, LexicalPrototypeClassifier)
            else f"annotated-sample-{config.taxonomy_method}-centroid-v1"
        ),
        "taxonomy_top_k": config.taxonomy_top_k,
        "reference_dataset_sha256": reference_fingerprint(),
        "document_year": config.document_year,
        "period": period,
        "sentence_count": len(sentences),
        "detection_count": len(rows),
        "warnings": [
            "Detector scores are not assumed to be calibrated probabilities.",
            "Taxonomy assignments are provisional nearest-prototype predictions.",
            "Chronology is assigned from document metadata, not inferred from text.",
        ],
    }
    return {
        "manifest": manifest,
        "sentences": sentences,
        "model_predictions": predictions_by_model,
        "detections": rows,
    }


def export_jsonl(result: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps({"type": "manifest", **result["manifest"]}, ensure_ascii=False))
        output.write("\n")
        for row in result["detections"]:
            output.write(json.dumps({"type": "detection", **row}, ensure_ascii=False))
            output.write("\n")


def export_csv(result: dict, path: Path) -> None:
    fields = [
        "id",
        "word",
        "sentence_text",
        "ensemble_score",
        "positive_votes",
        "model_count",
        "document_year",
        "period_id",
        "family_id",
        "family_label",
        "class_id",
        "class_label",
        "taxonomy_similarity",
        "taxonomy_margin",
        "taxonomy_method",
        "review_status",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in result["detections"]:
            taxonomy = row["taxonomy"]
            writer.writerow(
                {
                    "id": row["id"],
                    "word": row["word"],
                    "sentence_text": row["sentence_text"],
                    "ensemble_score": row["ensemble_score"],
                    "positive_votes": row["positive_votes"],
                    "model_count": row["model_count"],
                    "document_year": row["document_year"],
                    "period_id": row["period"]["id"],
                    "family_id": taxonomy["family_id"],
                    "family_label": taxonomy["family_label"],
                    "class_id": taxonomy["class_id"],
                    "class_label": taxonomy["class_label"],
                    "taxonomy_similarity": taxonomy["similarity"],
                    "taxonomy_margin": taxonomy["margin"],
                    "taxonomy_method": taxonomy["method"],
                    "review_status": row["review_status"],
                }
            )
