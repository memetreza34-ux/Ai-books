"""The typographic Noir cover uses a clean grid motif, no tiny illegible digits."""
from pathlib import Path
import pymupdf
from aibooks.sudoku import make_book
from aibooks.cover import full_wrap_cover, cover_geometry, TRIM_W


def test_noir_uses_9x9_grid_motif_not_tiny_numerals(tmp_path: Path):
    puzzles = make_book(20, 20261023, 45)
    pdf = tmp_path / "noir.pdf"
    full_wrap_cover(pdf, "Sudoku im Großdruck", puzzles, 34, style="noir")
    with pymupdf.open(str(pdf)) as document:
        front = document[0]
        text = front.get_text("text")
        assert "Sudoku im Großdruck" in " ".join(text.split())
        assert "20" in text
        # Check the motif region, not the two digits in the "9 × 9" footer.
        g = cover_geometry(34)
        cx = g.front_start_pt + TRIM_W * 72 / 2
        motif = pymupdf.Rect(cx - 76, g.page_height_pt - 323,
                             cx + 76, g.page_height_pt - 171)
        spans = [span for block in front.get_text("dict")["blocks"]
                 for line in block.get("lines", [])
                 for span in line.get("spans", [])]
        motif_digits = [span for span in spans
                        if span["text"].strip() in set("123456789")
                        and motif.intersects(pymupdf.Rect(span["bbox"]))]
        assert motif_digits == []
