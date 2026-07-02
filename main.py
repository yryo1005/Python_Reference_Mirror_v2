#!/usr/bin/env python3
"""Serve Python official documentation offline from a local archive."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from python_doc_mirror.config import DEFAULT_OUTPUT_DIR
from python_doc_mirror.server import run_server

_REQUIRED_PACKAGES = (
    ("bs4", "beautifulsoup4"),
    ("lxml", "lxml"),
    ("requests", "requests"),
)


def ensure_dependencies() -> None:
    missing = [package for module, package in _REQUIRED_PACKAGES if not _try_import(module)]
    if not missing:
        return

    print("Error: required packages are not installed for this Python:", file=sys.stderr)
    print(f"  Python: {sys.executable}", file=sys.stderr)
    for package in missing:
        print(f"  missing: {package}", file=sys.stderr)
    print(file=sys.stderr)
    print("Install them with:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    print(file=sys.stderr)
    print("If you use a virtual environment, activate it first, then run pip.", file=sys.stderr)
    print("On Windows (PowerShell):", file=sys.stderr)
    print("  .venv\\Scripts\\Activate.ps1", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


def _try_import(module: str) -> bool:
    try:
        __import__(module)
    except ImportError:
        return False
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Browse Python documentation offline from docs.python.org archives.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve = subparsers.add_parser(
        "serve",
        help="Start a local web server for the documentation",
    )
    serve.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Documentation directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    serve.add_argument("--host", default="127.0.0.1", help="Bind address")
    serve.add_argument("--port", type=int, default=8000, help="Port number")
    serve.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open a browser automatically",
    )

    return parser


def cmd_serve(args: argparse.Namespace) -> int:
    ensure_dependencies()
    run_server(
        args.dir,
        host=args.host,
        port=args.port,
        open_browser=not args.no_browser,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "serve":
        return cmd_serve(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
