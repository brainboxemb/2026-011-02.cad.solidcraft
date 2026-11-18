#!/usr/bin/env python3
"""Run model-specific native SolidCraft evidence checks."""
from __future__ import annotations

import argparse
from pathlib import Path

from native_checks import VALIDATORS


def validate(root: Path, models=None):
    selected = set(models) if models is not None else None
    for slug, validator in VALIDATORS.items():
        if selected is not None and slug not in selected:
            continue
        validator(root)
        print(f"{slug}: native validation PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("native_root", type=Path)
    parser.add_argument("--models", nargs="*")
    args = parser.parse_args()
    validate(args.native_root, args.models)


if __name__ == "__main__":
    main()
