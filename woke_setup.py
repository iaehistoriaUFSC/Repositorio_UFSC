"""Rotinas chamadas pelo instalador Windows."""

from __future__ import annotations

import argparse
import sys

from woke_catalog import CATALOG, DEFAULT_KEYS
from woke_models import install_package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", choices=("none", "defaults", "all"), default="none")
    args = parser.parse_args()
    if args.models == "none":
        return 0
    packages = list(CATALOG) if args.models == "all" else [p for p in CATALOG if p.key in DEFAULT_KEYS]
    for index, package in enumerate(packages, start=1):
        print(f"[{index}/{len(packages)}] {package.label}", flush=True)
        try:
            install_package(package, lambda message: print(f"    {message}", flush=True))
        except Exception as exc:
            print(f"ERRO: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
