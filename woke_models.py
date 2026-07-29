"""Download, extração e carregamento local dos modelos WOKE."""

from __future__ import annotations

import os
import shutil
import zipfile
from pathlib import Path
from typing import Callable

import gdown
from gensim.models import KeyedVectors

from woke_catalog import ModelPackage


APP_HOME = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Woke"
MODEL_HOME = Path(os.environ.get("WOKE_MODEL_HOME", APP_HOME / "modelos"))


def package_dir(package: ModelPackage) -> Path:
    return MODEL_HOME / package.slug


def model_files(package: ModelPackage) -> list[Path]:
    return sorted(package_dir(package).glob("*.wordvectors"), key=lambda path: path.name)


def is_installed(package: ModelPackage) -> bool:
    files = model_files(package)
    # Pacotes grandes salvam os vetores em arquivos .npy auxiliares; os menores
    # (como HST) incorporam os vetores no próprio .wordvectors. Ambos são válidos.
    return len(files) == package.intervals and all(path.stat().st_size > 0 for path in files)


def installed_size(package: ModelPackage) -> int:
    root = package_dir(package)
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file()) if root.exists() else 0


def _safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as zipped:
        for member in zipped.infolist():
            target = (destination / member.filename).resolve()
            if root != target and root not in target.parents:
                raise ValueError(f"Caminho inseguro no ZIP: {member.filename}")
        zipped.extractall(destination)


def install_package(
    package: ModelPackage,
    status: Callable[[str], None] | None = None,
    progress: Callable[[int, int | None], None] | None = None,
) -> Path:
    """Baixa com retomada e extrai um pacote; nunca remove um pacote funcional."""
    report = status or (lambda _message: None)
    destination = package_dir(package)
    if is_installed(package):
        report("O pacote já está instalado.")
        return destination

    MODEL_HOME.mkdir(parents=True, exist_ok=True)
    downloads = MODEL_HOME / ".downloads"
    downloads.mkdir(exist_ok=True)
    archive = downloads / f"{package.slug}.zip"
    report(f"Baixando {package.label}. O download pode ser retomado.")
    result = gdown.download(
        id=package.file_id,
        output=str(archive),
        quiet=True,
        resume=True,
        progress=progress,
    )
    if not result or not archive.exists():
        raise RuntimeError("O Google Drive não concluiu o download.")

    staging = MODEL_HOME / f".{package.slug}.extracting"
    if staging.exists():
        shutil.rmtree(staging)
    report("Download concluído. Descompactando os modelos…")
    _safe_extract(archive, staging)
    found = list(staging.rglob("*.wordvectors"))
    if len(found) != package.intervals:
        raise RuntimeError(
            f"Pacote incompleto: esperados {package.intervals} modelos; encontrados {len(found)}."
        )
    if destination.exists():
        backup = MODEL_HOME / f".{package.slug}.previous"
        if backup.exists():
            shutil.rmtree(backup)
        destination.replace(backup)
    staging.replace(destination)
    archive.unlink(missing_ok=True)
    report("Pacote instalado e verificado.")
    return destination


def load_models(package: ModelPackage) -> list[tuple[str, KeyedVectors]]:
    if not is_installed(package):
        raise FileNotFoundError(f"O pacote {package.label} ainda não foi baixado.")
    return [(path.stem, KeyedVectors.load(str(path), mmap="r")) for path in model_files(package)]


def copy_downloaded_defaults(source: Path) -> None:
    """Importa os dois ZIPs usados durante o desenvolvimento, quando presentes."""
    MODEL_HOME.mkdir(parents=True, exist_ok=True)
    mapping = {
        "UFSC_Incremental_Modelo_1.zip": "UFSC 2003-2006|Incremental|1",
        "UFSC_Temporal_Modelo_1.zip": "UFSC 2003-2006|Temporal|1",
        "HST_Incremental_Modelo_1.zip": "HST-03-10|Incremental|1",
        "HST_Temporal_Modelo_1.zip": "HST-03-10|Temporal|1",
    }
    from woke_catalog import package_by_key

    for filename, key in mapping.items():
        archive = source / filename
        package = package_by_key(key)
        if archive.exists() and not is_installed(package):
            destination = package_dir(package)
            staging = MODEL_HOME / f".{package.slug}.extracting"
            if staging.exists():
                shutil.rmtree(staging)
            _safe_extract(archive, staging)
            staging.replace(destination)
