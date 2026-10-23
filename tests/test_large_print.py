"""Large-print solutions in the production-pilot rendering."""
import json
from pathlib import Path

import pymupdf
import pytest

from aibooks.pipeline import build_sudoku


def test_large_solutions_layout_and_qa(tmp_path: Path):
    out = tmp_path / "large-solutions"
    result = build_sudoku(out, "Sudoku im Großdruck", 20, 20261023, 45,
                          solutions_per_page=2)
    assert result["pages"] == 34  # 3 intro + 20 puzzles + 10 answer + 1 notes
    qa = json.loads((out / "quality-report.json").read_text(encoding="utf-8"))
    assert qa["editorial"]["solutions_per_page"] == 2
    assert qa["editorial"]["solution_headings_checked"] == 20
    assert qa["preflight"]["machine_preflight_passed"]
    with pymupdf.open(str(out / "interior-DRAFT.pdf")) as pdf:
        assert "Rätsel 001" in pdf[23].get_text()
        assert "Rätsel 002" in pdf[23].get_text()
        assert "Rätsel 019" in pdf[32].get_text()


def test_unsupported_solution_layout_fails_safely(tmp_path: Path):
    with pytest.raises(ValueError, match="solutions_per_page"):
        build_sudoku(tmp_path / "bad", "Sudoku im Großdruck", 20, 1, 40,
                     solutions_per_page=3)
    assert not (tmp_path / "bad").exists()
