"""Independent editorial text consistency checks for a Sudoku PDF draft.

This gate is *not* a visual review nor a KDP compliance certificate.
"""
from __future__ import annotations

from math import ceil
from pathlib import Path
import re

import pymupdf


def _normalise(text: str) -> str:
    return " ".join(text.split()).casefold()


def audit_sudoku_text(interior: Path, cover: Path, title: str, count: int,
                      solutions_per_page: int = 4) -> dict:
    if solutions_per_page not in (2, 4):
        raise ValueError('Invalid solutions_per_page')
    errors: list[str] = []
    with pymupdf.open(str(interior)) as pdf:
        texts = [page.get_text("text", sort=True) for page in pdf]
        cover_text = ""
        with pymupdf.open(str(cover)) as outside:
            if len(outside) != 1:
                errors.append("Cover PDF must have exactly one page")
            elif outside:
                # Read the FRONT half only. Full-wrap page extraction interleaves
                # back-cover text with two-line front titles when sorted by Y.
                page = outside[0]
                front = pymupdf.Rect(page.rect.width / 2, 0,
                                     page.rect.width, page.rect.height)
                cover_text = page.get_text("text", clip=front, sort=True)

        expected_title = _normalise(title)
        if not texts or expected_title not in _normalise(texts[0]):
            errors.append("Title mismatch: interior title page does not display the requested title")
        if expected_title not in _normalise(cover_text):
            errors.append("Title mismatch: front cover does not display the requested title")

        # Textual claims must describe the contents, not the project defaults.
        if not texts or not re.search(rf"\b{count}\s+geprüfte Rätsel\b", texts[0], re.I):
            errors.append("Interior puzzle-count claim does not match the manifest")
        if not re.search(rf"\b{count}\s+SUDOKU-RÄTSEL\b", cover_text, re.I):
            errors.append("Cover puzzle-count claim does not match the manifest")

        expected_min_pages = 3 + count + ceil(count / solutions_per_page) + 1
        if len(texts) < expected_min_pages:
            errors.append("Missing puzzle, solution or notes pages")

        puzzle_numbers = []
        for index in range(3, min(3 + count, len(texts))):
            labels = re.findall(r"Rätsel\s+(\d{3})", texts[index], re.I)
            puzzle_numbers.extend(labels)
            expected_label = f"{index - 2:03d}"
            if labels != [expected_label]:
                errors.append(f"Puzzle page {index + 1}: expected only Rätsel {expected_label}")

        solution_start = 3 + count
        solution_end = solution_start + ceil(count / solutions_per_page)
        solution_numbers = []
        for page_text in texts[solution_start:solution_end]:
            solution_numbers.extend(re.findall(r"Rätsel\s+(\d{3})", page_text, re.I))
        desired = [f"{i:03d}" for i in range(1, count + 1)]
        if puzzle_numbers != desired:
            errors.append("Puzzle headings missing, out of order or repeated")
        if solution_numbers != desired:
            errors.append("Solution headings missing, out of order or repeated")

    return {
        "content_consistency_passed": not errors,
        "requested_title": title,
        "expected_puzzles": count,
        "solutions_per_page": solutions_per_page,
        "puzzle_headings_checked": len(puzzle_numbers),
        "solution_headings_checked": len(solution_numbers),
        "problems": errors,
        "limitations": ["Does not judge visual quality, typography or commercial originality",
                        "Does not validate rights or market demand"]
    }
