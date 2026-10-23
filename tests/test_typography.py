"""Prevent close-packed Sudoku solution labels and overlapping cover typography."""
from pathlib import Path

import pymupdf

from aibooks.pipeline import build_sudoku
from aibooks.layout import solution_layout


def test_large_solution_label_has_actual_grid_separation(tmp_path: Path):
    for index in (0, 1):
        x, y, grid_size, label_y, label_x, label_size, number_size = solution_layout(index, 2)
        assert y + grid_size + 12 <= label_y
        assert number_size >= 12
        assert grid_size >= 260
    top = solution_layout(0, 2)
    bottom = solution_layout(1, 2)
    assert bottom[1] + bottom[2] + 12 < top[1]
    assert bottom[3] + 14 < top[1]


def test_full_cover_title_and_tagline_do_not_overlap(tmp_path: Path):
    out = tmp_path / "layout-review"
    build_sudoku(out, "Sudoku im Großdruck", 20, 20261023, 45, solutions_per_page=2)
    with pymupdf.open(str(out / "cover-WRAP-DRAFT.pdf")) as pdf:
        page = pdf[0]
        blocks = page.get_text("dict")["blocks"]
        spans = [s for b in blocks for l in b.get("lines", []) for s in l.get("spans", [])]
        t = [s for s in spans if s["text"] in ("Sudoku im", "Großdruck")]
        tag = [s for s in spans if s["text"] == "KONZENTRATION. LOGIK. RÄTSELSPASS."]
        assert len(t) == 2 and len(tag) == 1
        assert max(s["bbox"][3] for s in t) + 10 < tag[0]["bbox"][1]


def test_large_solution_puzzle_headings_are_present(tmp_path: Path):
    out = tmp_path / "large-preview"
    build_sudoku(out, "Sudoku im Großdruck", 20, 20261023, 45, solutions_per_page=2)
    with pymupdf.open(str(out / "interior-DRAFT.pdf")) as pdf:
        assert "Rätsel 001" in pdf[23].get_text()
        assert "Rätsel 002" in pdf[23].get_text()
