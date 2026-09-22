#!/usr/bin/env python3
"""Buzz application entry point."""
import argparse
import json
from buzz.cli import run_cli
from buzz.status import status_report

def main() -> int:
    parser=argparse.ArgumentParser(description="Buzz personal AI automation platform")
    parser.add_argument("--status",action="store_true",help="show local configuration and enabled capabilities without starting AI")
    parser.add_argument("--api",action="store_true",help="start the local Buzz API on 127.0.0.1")
    args=parser.parse_args()
    if args.status:
        print(json.dumps(status_report(),indent=2))
        return 0
    if args.api:
        try:
            import uvicorn
        except ImportError as exc:
            raise SystemExit("Install requirements-api.txt before using --api.") from exc
        uvicorn.run("buzz.api:app",host="127.0.0.1",port=8765,reload=False)
        return 0
    return run_cli()

if __name__=="__main__":
    raise SystemExit(main())
