from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def run_smoke(report_path: Path) -> int:
    from app import __version__
    from app.models import load_registry
    from app.taxonomy import LexicalPrototypeClassifier
    from app.visualization import create_figure

    classifier = LexicalPrototypeClassifier()
    figure = create_figure({})
    report = {
        "status": "ok",
        "application_version": __version__,
        "taxonomy_classes": len(classifier.classes),
        "registered_models": len(load_registry()["models"]),
        "matplotlib_axes": len(figure.axes),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--worker", choices=("hf", "melbert", "framebert"))
    parser.add_argument("--smoke-report", type=Path)
    known, remaining = parser.parse_known_args(argv)
    if known.smoke_report:
        return run_smoke(known.smoke_report)
    if known.worker:
        if known.worker == "hf":
            from app.workers.hf_worker import main as worker_main
        elif known.worker == "melbert":
            from app.workers.melbert_worker import main as worker_main
        else:
            from app.workers.framebert_worker import main as worker_main
        return worker_main(remaining)
    from app.gui import run

    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
