#!/usr/bin/env python3
"""Buzz application entry point."""

from buzz.core.orchestrator import BuzzOrchestrator


def main() -> int:
    buzz = BuzzOrchestrator()
    print(f"Buzz core online. State: {buzz.state.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
