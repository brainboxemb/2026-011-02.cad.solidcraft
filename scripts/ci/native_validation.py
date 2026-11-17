#!/usr/bin/env python3
"""Run model-specific native SolidCraft evidence checks."""
from __future__ import annotations

import argparse
from pathlib import Path

from native_checks import VALIDATORS


def validate(root: Path):
    for slug, validator in VALIDATORS.items():
        validator(root)
        print(f"{slug}: native validation PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("native_root", type=Path)
    args = parser.parse_args()
    validate(args.native_root)


if __name__ == "__main__":
    main()
