"""Command-line interface; no remote APIs and no publishing side effects."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from aibooks.pipeline import build_sudoku


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aibooks", description="Local AI book factory")
    commands = parser.add_subparsers(dest="command", required=True)
    sudoku = commands.add_parser("sudoku", help="Generate a validated Sudoku DRAFT book")
    sudoku.add_argument("--title", default="Sudoku Testband")
    sudoku.add_argument("--count", type=int, default=28)
    sudoku.add_argument("--seed", type=int, default=20261022)
    sudoku.add_argument("--clues", type=int, default=38)
    sudoku.add_argument("--paper", choices=("white", "cream"), default="white")
    sudoku.add_argument("--out", type=Path, default=Path("output/sudoku-test"))
    sudoku.add_argument("--previews", action="store_true", help="Generate contact sheets for all pages (optional dependencies)")
    args = parser.parse_args(argv)
    try:
        if args.command == "sudoku":
            report = build_sudoku(args.out, args.title, args.count, args.seed, args.clues,
                                  previews=args.previews, paper=args.paper)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0
    except (ValueError, FileExistsError, AssertionError, RuntimeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 2
