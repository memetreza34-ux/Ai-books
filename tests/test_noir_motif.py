"""The typographic Noir cover uses a clean grid motif, no tiny illegible digits."""
from pathlib import Path
import pymupdf
from aibooks.sudoku import make_book
from aibooks.cover import full_wrap_cover


def test_noir_uses_9x9_grid_motif_not_tiny_numerals(tmp_path: Path):
    puzzles = make_book(20, 20261023, 45)
    pdf = tmp_path / "noir.pdf"
    full_wrap_cover(pdf, "Sudoku im Großdruck", puzzles, 34, style="noir")
    with pymupdf.open(str(pdf)) as document:
        front = document[0]
        text = front.get_text("text")
        assert "Sudoku im Großdruck" in " ".join(text.split())
        assert "20" in text
        # Only typography/labels, not the example puzzle's 45 one-digit givens.
        assert len([word for word in text.split() if len(word) == 1 and word in "123456789"]) == 0
