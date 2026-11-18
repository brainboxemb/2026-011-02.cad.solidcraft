#!/usr/bin/env python3
"""Pull the exact CAD toolchain image, waiting only while it is not published yet.

The CAD image is built by a separate workflow. A source change that creates a
new image identity can therefore start the normal CAD workflow before that
immutable image has been pushed. This helper handles only that expected race.

Authentication errors and other Docker failures are not retried because waiting
cannot repair them.
"""

from __future__ import annotations

import argparse
import subprocess
import time


_RETRYABLE = (
    "not found",
    "manifest unknown",
)


def pull(
    reference: str,
    *,
    attempts: int = 30,
    delay_seconds: float = 10.0,
) -> None:
    """Pull one immutable image, retrying only while the registry has no image.

    `attempts` includes the first pull. A successful pull returns immediately.
    """

    if attempts < 1:
        raise ValueError("attempts must be at least one")
    if delay_seconds < 0:
        raise ValueError("delay_seconds cannot be negative")

    for attempt in range(1, attempts + 1):
        completed = subprocess.run(
            ["docker", "pull", reference],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode == 0:
            if completed.stdout:
                print(completed.stdout, end="")
            return

        detail = (completed.stderr or completed.stdout or "").strip()
        retryable = any(marker in detail.lower() for marker in _RETRYABLE)
        if not retryable:
            raise RuntimeError(
                f"docker pull failed for {reference}: {detail or 'unknown error'}"
            )
        if attempt == attempts:
            raise RuntimeError(
                f"image was not published after {attempts} pull attempts: {reference}"
            )

        print(
            f"Image not published yet ({attempt}/{attempts}); retrying: {reference}"
        )
        time.sleep(delay_seconds)


def main() -> int:
    """Parse workflow arguments and pull the requested image."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference")
    parser.add_argument("--attempts", type=int, default=30)
    parser.add_argument("--delay-seconds", type=float, default=10.0)
    args = parser.parse_args()

    pull(
        args.reference,
        attempts=args.attempts,
        delay_seconds=args.delay_seconds,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
