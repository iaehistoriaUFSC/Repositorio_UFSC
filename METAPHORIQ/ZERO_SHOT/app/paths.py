from __future__ import annotations

import os
import sys
from pathlib import Path


APP_ID = "MetaphoriqZeroShot"


def resource_root() -> Path:
    frozen = getattr(sys, "_MEIPASS", None)
    return Path(frozen) if frozen else Path(__file__).resolve().parents[1]


def resource_path(*parts: str) -> Path:
    return resource_root().joinpath(*parts)


def user_root() -> Path:
    base = Path(os.getenv("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    root = base / APP_ID
    root.mkdir(parents=True, exist_ok=True)
    return root


def models_root() -> Path:
    path = user_root() / "models"
    path.mkdir(parents=True, exist_ok=True)
    return path


def cache_root() -> Path:
    path = user_root() / "cache"
    path.mkdir(parents=True, exist_ok=True)
    return path


def output_root() -> Path:
    path = Path.home() / "Documents" / "METAPHORIQ Zero-Shot"
    path.mkdir(parents=True, exist_ok=True)
    return path

