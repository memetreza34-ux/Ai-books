"""One-book spec -> deterministic PDF draft -> reviewable metadata and manifest.

No external AI API, payments, uploads, or autonomous publishing.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

from aibooks.pipeline import build_sudoku, file_hash
from aibooks.market import paperback_royalty_scenario

REQUIRED = {"schema_version", "project_id", "product_type", "title",
            "language", "audience", "seed", "puzzles", "clues",
            "paper", "solutions_per_page", "market_status", "rights_status"}
ALLOWED_STATUS = {"HOLD", "CANDIDATE_FOR_HUMAN_REVIEW"}


def _json_file(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_book_spec(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Book spec must be a JSON object")
    if data.get("schema_version") != 1 or not REQUIRED.issubset(data):
        raise ValueError("Book spec v1 missing required fields")
    if data["product_type"] != "sudoku" or data["language"] != "de":
        raise ValueError("First supported book spec: sudoku / de")
    project_id = data["project_id"]
    if (not isinstance(project_id, str) or not 1 <= len(project_id) <= 60
        or not all(c.isalnum() or c == "-" for c in project_id)):
        raise ValueError("project_id must be safe alphanumeric/hyphen")
    title = data["title"]
    if (not isinstance(title, str) or not 3 <= len(title) <= 90
        or any(ord(c) < 32 for c in title)):
        raise ValueError("Invalid title")
    if not isinstance(data["audience"], str) or not 5 <= len(data["audience"]) <= 240:
        raise ValueError("Audience must be a clear description")
    if type(data["seed"]) is not int or not 0 <= data["seed"] <= 2**32 - 1:
        raise ValueError("Invalid deterministic seed")
    if type(data["puzzles"]) is not int or not 20 <= data["puzzles"] <= 150:
        raise ValueError("Pilot supports 20..150 puzzles")
    if type(data["clues"]) is not int or not 28 <= data["clues"] <= 70:
        raise ValueError("Clues must be 28..70")
    if data["solutions_per_page"] not in (2, 4):
        raise ValueError("solutions_per_page must be 2 or 4")
    if data["paper"] not in ("white", "cream"):
        raise ValueError("Invalid paper")
    if data["market_status"] not in ALLOWED_STATUS:
        raise ValueError("No commercial GO without separately approved workflow")
    if data["rights_status"] != "review_required":
        raise ValueError("This pilot may only have rights_status review_required")
    if data.get("difficulty_label") not in (None, ""):
        raise ValueError("Do not claim an unverified Sudoku difficulty")
    if data.get("user_approved_to_publish") is True:
        raise ValueError("Approval cannot be claimed in a source book spec")
    if "proposed_net_list_price_eur" in data:
        value = data["proposed_net_list_price_eur"]
        if not isinstance(value, (str, int, float)) or isinstance(value, bool):
            raise ValueError("Invalid illustrative net price")
    return data


def build_from_spec(spec_path: Path, out: Path, previews: bool = False) -> dict:
    book = read_book_spec(spec_path)  # validate everything before modifying output
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"Cannot overwrite existing output: {out}")
    product = build_sudoku(
        out=out, title=book["title"], count=book["puzzles"],
        seed=book["seed"], clues=book["clues"],
        previews=previews, paper=book["paper"],
        solutions_per_page=book["solutions_per_page"]
    )
    generated = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    count = book["puzzles"]
    description = (
        f"{count} nummerierte Sudoku-Rätsel im großzügigen 9×9-Raster "
        "mit einem Rätsel pro Seite. "
        "Die Lösungsseiten zeigen jeweils "
        f"{book['solutions_per_page']} vollständige Sudokus pro Seite. "
        "Jedes Rätsel wurde auf genau eine gültige Lösung geprüft."
    )
    metadata = {
        "status": "DRAFT_METADATA_FOR_HUMAN_EDIT",
        "title": book["title"], "subtitle": "",
        "author_or_imprint": None,
        "language": "de",
        "description_plain_text": description,
        "keyword_research_status": "NOT_VERIFIED",
        "keyword_candidates": ["Sudoku Großdruck", "Sudoku für Erwachsene",
                               "Sudoku Rätselbuch", "Sudoku große Felder"],
        "age_or_difficulty_claims": [],
        "publisher_categories_selected": False,
        "no_automatic_kdp_upload": True,
        "editorial_note": "Cover subtitle and KDP upload metadata must match; owner must approve claims."
    }
    cost = paperback_royalty_scenario(product["pages"],
                                    book.get("proposed_net_list_price_eur", "12.99"))
    plan = {
        "schema_version": 1,
        "project_id": book["project_id"],
        "generation_status": product["status"],
        "commercial_status": book["market_status"],
        "publishing_status": "NOT_APPROVED",
        "product_hypothesis": {
            "audience": book["audience"], "positioning": book.get("positioning", ""),
            "evidence_level": "LIMITED_COMPETITOR_LISTINGS",
            "distinguishing_features": ["one 9x9 grid per page",
                                         f"{book['solutions_per_page']} larger solution grids per page",
                                         "all unique Sudoku solutions checked by solver"]
        },
        "print_profile": {
            "trim_in": [8.5, 11], "paper": book["paper"],
            "ink": "black", "interior_bleed": False,
            "total_pages": product["pages"]
        },
        "illustrative_kdp_royalty_not_sales": cost,
        "required_before_release": [
            "independent content and complete visual review",
            "verify true market differentiation and demand",
            "verify current KDP print rates and official full-wrap cover template",
            "clear authorship, pen name, licensing, AI disclosure and EU requirements",
            "complete actual KDP Previewer and physical proof",
            "owner explicitly approves price and publication"
        ]
    }
    spec_copy = out / "book-spec.json"
    meta = out / "listing-metadata-DRAFT.json"
    checklist = out / "production-plan-DRAFT.json"
    _json_file(spec_copy, book)
    _json_file(meta, metadata)
    _json_file(checklist, plan)
    qa_file = out / "quality-report.json"
    qa = json.loads(qa_file.read_text(encoding="utf-8"))
    qa["market_evidence"] = "HOLD"
    qa["publication_approval"] = False
    qa["readability_review"] = "REQUIRED"
    qa["product_spec_id"] = book["project_id"]
    _json_file(qa_file, qa)
    generated["product_spec_id"] = book["project_id"]
    generated["product_spec_sha256"] = sha256(spec_path.read_bytes()).hexdigest()
    generated["market_status"] = book["market_status"]
    generated["rights_status"] = "review_required"
    generated["status"] = "DRAFT"
    generated["sale_ready"] = False
    # Update hashes after updating the quality file and adding new outputs.
    for f in [qa_file, spec_copy, meta, checklist]:
        generated["outputs"][f.name] = {"sha256": file_hash(f), "bytes": f.stat().st_size}
    _json_file(out / "manifest.json", generated)
    return {
        "project_id": book["project_id"], "pages": product["pages"],
        "puzzles": count, "solutions_per_page": book["solutions_per_page"],
        "quality": product["status"], "market": book["market_status"],
        "sale_ready": False, "output": str(out)
    }
