#!/usr/bin/env python3
"""Buzz application entry point."""
import argparse
import json
from buzz.cli import run_cli
from buzz.status import status_report

def main() -> int:
    parser=argparse.ArgumentParser(description="Buzz personal AI automation platform")
    parser.add_argument("--status",action="store_true",help="show local configuration and enabled capabilities without starting AI")
    args=parser.parse_args()
    if args.status:
        print(json.dumps(status_report(),indent=2))
        return 0
    return run_cli()

if __name__=="__main__":
    raise SystemExit(main())
