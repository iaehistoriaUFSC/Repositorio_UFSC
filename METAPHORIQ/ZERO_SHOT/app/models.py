from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from app.paths import models_root, resource_path, user_root


Progress = Callable[[str], None]


@dataclass(frozen=True)
class ModelStatus:
    model_id: str
    installed: bool
    ready: bool
    path: Path
    bytes: int
    detail: str


def load_registry() -> dict:
    return json.loads(resource_path("data", "models.json").read_text(encoding="utf-8"))


def registry_by_id() -> dict[str, dict]:
    return {item["id"]: item for item in load_registry()["models"]}


def model_path(model_id: str) -> Path:
    return models_root() / model_id


def _directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _find_melbert_checkpoint(path: Path) -> Path | None:
    for config in sorted(path.rglob("config.json")):
        candidate = config.parent
        if (candidate / "pytorch_model.bin").is_file():
            return candidate
    return None


def status(model_id: str) -> ModelStatus:
    spec = registry_by_id()[model_id]
    path = model_path(model_id)
    installed = path.is_dir()
    ready = False
    detail = "Not downloaded"
    if installed and spec["kind"] == "huggingface":
        ready = (path / "config.json").is_file() and any(
            (path / name).is_file()
            for name in ("model.safetensors", "pytorch_model.bin")
        )
        detail = "Ready" if ready else "Incomplete Hugging Face snapshot"
    elif installed and spec["kind"] == "melbert_repository":
        ready = (path / "repository" / "main.py").is_file() and bool(
            _find_melbert_checkpoint(path / "checkpoint")
        )
        detail = "Ready" if ready else "Repository or checkpoint is incomplete"
    elif installed and spec["kind"] == "framebert_repository":
        repository = path / "repository"
        ready = (repository / "inference.py").is_file()
        detail = (
            "Experimental repository installed; inference may download extra resources"
            if ready
            else "Repository is incomplete"
        )
    return ModelStatus(
        model_id=model_id,
        installed=installed,
        ready=ready,
        path=path,
        bytes=_directory_size(path) if installed else 0,
        detail=detail,
    )


def all_statuses() -> list[ModelStatus]:
    return [status(item["id"]) for item in load_registry()["models"]]


def _safe_extract(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if os.path.commonpath([str(root), str(target)]) != str(root):
                raise RuntimeError(f"unsafe archive member: {member.filename}")
        archive.extractall(destination)


def _download_file(url: str, destination: Path, progress: Progress) -> None:
    progress(f"Downloading {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "MetaphoriqZeroShot/0.1"})
    with urllib.request.urlopen(request, timeout=120) as response:
        with destination.open("wb") as output:
            shutil.copyfileobj(response, output)


def _install_repository(
    url: str,
    destination: Path,
    progress: Progress,
) -> None:
    repo_url = url.removesuffix(".git")
    archive_url = f"{repo_url}/archive/refs/heads/main.zip"
    with tempfile.TemporaryDirectory(prefix="metaphoriq-repo-") as temp_name:
        temp = Path(temp_name)
        archive = temp / "repository.zip"
        extracted = temp / "extracted"
        _download_file(archive_url, archive, progress)
        _safe_extract(archive, extracted)
        roots = [item for item in extracted.iterdir() if item.is_dir()]
        if len(roots) != 1:
            raise RuntimeError("repository archive did not contain one root directory")
        shutil.copytree(roots[0], destination)


def _write_state(model_id: str, spec: dict) -> None:
    path = user_root() / "state.json"
    state = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    state.setdefault("models", {})[model_id] = {
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "source": spec.get("repository_id") or spec.get("repository"),
        "license": spec["license"],
    }
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def install_model(model_id: str, progress: Progress = lambda _message: None) -> ModelStatus:
    spec = registry_by_id()[model_id]
    final = model_path(model_id)
    if status(model_id).ready:
        return status(model_id)
    staging = models_root() / f".{model_id}.installing"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    try:
        if spec["kind"] == "huggingface":
            progress(f"Downloading {spec['repository_id']} from Hugging Face")
            from huggingface_hub import snapshot_download

            snapshot_download(
                repo_id=spec["repository_id"],
                local_dir=staging,
                allow_patterns=[
                    "*.json",
                    "*.txt",
                    "*.model",
                    "*.safetensors",
                    "*.bin",
                    "tokenizer*",
                    "vocab*",
                    "merges.txt",
                    "sentencepiece*",
                ],
            )
        elif spec["kind"] == "melbert_repository":
            _install_repository(spec["repository"], staging / "repository", progress)
            checkpoint = staging / "checkpoint"
            checkpoint.mkdir()
            archive = staging / "melbert-checkpoint.zip"
            progress("Downloading the official MelBERT VUA-18 checkpoint")
            import gdown

            downloaded = gdown.download(
                id=spec["checkpoint_file_id"],
                output=str(archive),
                quiet=False,
            )
            if not downloaded or not archive.is_file():
                raise RuntimeError("MelBERT checkpoint download failed")
            _safe_extract(archive, checkpoint)
            archive.unlink()
        elif spec["kind"] == "framebert_repository":
            _install_repository(spec["repository"], staging / "repository", progress)
        else:
            raise ValueError(f"unsupported model kind: {spec['kind']}")
        if final.exists():
            shutil.rmtree(final)
        staging.replace(final)
        _write_state(model_id, spec)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    result = status(model_id)
    if not result.ready:
        raise RuntimeError(result.detail)
    progress(f"{spec['label']} installed")
    return result


def remove_model(model_id: str) -> None:
    path = model_path(model_id).resolve()
    root = models_root().resolve()
    if path.parent != root:
        raise RuntimeError(f"unsafe model removal path: {path}")
    if path.exists():
        shutil.rmtree(path)


def reference_fingerprint() -> str:
    digest = hashlib.sha256()
    for name in ("families.jsonl", "taxonomy_nodes.jsonl", "examples.jsonl"):
        path = resource_path("data", "reference", name)
        digest.update(name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()

