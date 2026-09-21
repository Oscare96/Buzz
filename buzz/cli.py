"""Interactive text shell for Buzz."""

from __future__ import annotations

from buzz.app import build_runtime
from buzz.core.request import BuzzRequest


def run_cli() -> int:
    runtime = build_runtime()
    print("Buzz online. Type 'exit' to quit.")
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            continue
        if text.lower() in {"exit", "quit"}:
            return 0
        try:
            response = runtime.handle(BuzzRequest(text=text, source="cli"))
            print(f"Buzz: {response.text}")
            for action in response.metadata.get("actions", []):
                print(f"  [{action['skill']}] {action['message']}")
        except Exception as exc:
            print(f"Buzz error: {exc}")
