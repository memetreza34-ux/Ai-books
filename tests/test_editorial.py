"""Editorial checks detect mismatches between the printed book and manifest."""
import json
from pathlib import Path

import pymupdf
from aibooks.editorial import audit_sudoku_text
from aibooks.pipeline import build_sudoku


def test_custom_title_printed_interior_and_cover(tmp_path: Path):
    title = "Sudoku für die Ferien"
    folder = tmp_path / "custom"
    build_sudoku(folder, title, 20, 42, 40, previews=True)
    with pymupdf.open(str(folder / "interior-DRAFT.pdf")) as pdf:
        assert title in pdf[0].get_text("text")
    with pymupdf.open(str(folder / "cover-WRAP-DRAFT.pdf")) as pdf:
        assert title in pdf[0].get_text("text")
    qa = json.loads((folder / "quality-report.json").read_text(encoding="utf-8"))
    assert qa["editorial"]["content_consistency_passed"]
    assert qa["editorial"]["puzzle_headings_checked"] == 20
    assert qa["editorial"]["solution_headings_checked"] == 20
    assert (folder / "previews" / "cover-full-wrap.png").is_file()


def test_mismatched_title_or_quantity_is_rejected(tmp_path: Path):
    folder = tmp_path / "draft"
    build_sudoku(folder, "Sudoku Testband", 20, 42, 40)
    interior = folder / "interior-DRAFT.pdf"
    cover = folder / "cover-WRAP-DRAFT.pdf"
    wrong_title = audit_sudoku_text(interior, cover, "Falscher Titel", 20)
    assert not wrong_title["content_consistency_passed"]
    assert any("Title mismatch" in issue for issue in wrong_title["problems"])
    wrong_quantity = audit_sudoku_text(interior, cover, "Sudoku Testband", 21)
    assert not wrong_quantity["content_consistency_passed"]
    assert any("puzzle-count" in issue for issue in wrong_quantity["problems"])


def test_long_legible_title_is_shrunk(tmp_path: Path):
    title = "Sudoku und logische Zahlenrätsel für Erwachsene"
    folder = tmp_path / "shrink"
    build_sudoku(folder, title, 20, 20, 40)
    report = audit_sudoku_text(folder / "interior-DRAFT.pdf",
                              folder / "cover-WRAP-DRAFT.pdf", title, 20)
    assert report["content_consistency_passed"]
