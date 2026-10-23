"""Command-line interface; no remote APIs and no publishing side effects."""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

from aibooks.pipeline import build_sudoku
from aibooks.opportunities import evaluate_file
from aibooks.researcher import research_file
from aibooks.market import evaluate_market_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aibooks", description="Local AI book factory")
    commands = parser.add_subparsers(dest="command", required=True)
    sudoku = commands.add_parser("sudoku", help="Generate a validated Sudoku DRAFT book")
    sudoku.add_argument("--title", default="Sudoku Testband")
    sudoku.add_argument("--count", type=int, default=28)
    sudoku.add_argument("--seed", type=int, default=20261022)
    sudoku.add_argument("--clues", type=int, default=38)
    sudoku.add_argument("--paper", choices=("white", "cream"), default="white")
    sudoku.add_argument("--solutions-per-page", type=int, choices=(2, 4), default=4)
    sudoku.add_argument("--out", type=Path, default=Path("output/sudoku-test"))
    sudoku.add_argument("--previews", action="store_true", help="Generate contact sheets for all pages (optional dependencies)")
    evaluation = commands.add_parser("evaluate", help="Score evidence files without live data or sales promises")
    evaluation.add_argument("--input", required=True, type=Path)
    evaluation.add_argument("--out", type=Path)
    research = commands.add_parser("research", help="Fetch small, live book catalog samples; NOT sales or verified demand")
    research.add_argument("--input", required=True, type=Path)
    research.add_argument("--out", required=True, type=Path)
    research.add_argument("--cache-dir", type=Path, default=Path("output/catalog-cache"))
    market = commands.add_parser("market", help="Compare dated retailer price snapshots and print royalty scenarios; never predict sales")
    market.add_argument("--input", required=True, type=Path)
    market.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "market":
            report = evaluate_market_file(args.input, args.out)
            print(json.dumps({
                "output": str(args.out),
                "evaluated_on": report["as_of"],
                "sales_estimated": report["sales_estimated"],
                "commercial_best_niche_selected": report["commercial_best_niche_selected"],
                "engineering_pilot_order": [
                    {"id": x["id"], "status": x["commercial_decision"],
                     "readiness": x["engineering_readiness"]}
                    for x in report["niches"]
                ]
            }, ensure_ascii=False, indent=2))
            return 0
        if args.command == "research":
            report = research_file(args.input, args.out, args.cache_dir,
                                   contact=os.getenv("AIBOOKS_CONTACT_EMAIL", ""))
            print(json.dumps({
                "output": str(args.out),
                "generated_at": report["generated_at"],
                "ideas": [{"id": item["id"], "status": item["decision"],
                           "sources_ok": item["catalog_sources_ok"],
                           "catalog_examples": item["catalog_examples"]}
                          for item in report["ideas"]],
                "sales_or_demand_claimed": False
            }, ensure_ascii=False, indent=2))
            return 0
        if args.command == "evaluate":
            report = evaluate_file(args.input, args.out)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0
        if args.command == "sudoku":
            report = build_sudoku(args.out, args.title, args.count, args.seed, args.clues,
                                  previews=args.previews, paper=args.paper,
                                  solutions_per_page=args.solutions_per_page)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0
    except (ValueError, KeyError, FileExistsError, AssertionError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 2
