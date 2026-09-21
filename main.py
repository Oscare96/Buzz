#!/usr/bin/env python3
"""Buzz application entry point."""

from buzz.cli import run_cli


def main() -> int:
    return run_cli()


if __name__ == "__main__":
    raise SystemExit(main())
