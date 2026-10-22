import json
from pathlib import Path
from pypdf import PdfReader
import pytest
from aibooks.pipeline import build_sudoku
from aibooks.cli import main


def test_first_book_produces_checked_draft(tmp_path: Path):
    result = build_sudoku(tmp_path / "book", "Sudoku Testband", 20, 9, 40)
    assert result["pages"] >= 24
    assert result["pages"] % 2 == 0
    folder = tmp_path / "book"
    assert len(PdfReader(folder / "interior-DRAFT.pdf").pages) == result["pages"]
    manifest = json.loads((folder / "manifest.json").read_text())
    qa = json.loads((folder / "quality-report.json").read_text())
    assert manifest["sale_ready"] is False
    assert qa["status"] == "MACHINE_PREFLIGHTED_DRAFT"
    assert qa["all_solutions_verified"] is True
    assert qa["cover_full_wrap_generated"] is True
    assert qa["kdp_template_approved"] is False
    assert qa["preflight"]["machine_preflight_passed"] is True
    assert (folder / "cover-WRAP-DRAFT.pdf").exists()


def test_existing_nonempty_output_is_not_overwritten(tmp_path: Path):
    out = tmp_path / "book"
    out.mkdir()
    (out / "important.txt").write_text("do not erase")
    with pytest.raises(FileExistsError):
        build_sudoku(out, "Test", 20, 10, 40)
    assert (out / "important.txt").read_text() == "do not erase"


def test_cli_rejects_invalid_count(tmp_path: Path):
    assert main(["sudoku", "--count", "10", "--out", str(tmp_path / "x")]) == 1
