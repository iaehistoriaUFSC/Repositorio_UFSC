from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from app.main import run_smoke


def test_runtime_smoke_report():
    report_path = Path("smoke.json")

    with (
        patch.object(Path, "mkdir"),
        patch.object(Path, "write_text", return_value=0) as write_text,
    ):
        assert run_smoke(report_path) == 0
    report = json.loads(write_text.call_args.args[0])

    assert report == {
        "status": "ok",
        "application_version": "0.1.1",
        "taxonomy_classes": 44,
        "registered_models": 4,
        "matplotlib_axes": 4,
    }
