from pathlib import Path

from aibooks.pipeline import build_sudoku


def test_contact_sheets_for_every_page(tmp_path: Path):
    result = build_sudoku(tmp_path / "book", "Test", 20, 15, 40, previews=True)
    import fitz
    import json
    out = tmp_path / "book"
    assert list((out / "previews").glob("contact-sheet-*.png"))
    with fitz.open(str(out / "interior-DRAFT.pdf")) as document:
        assert len(document) == result["pages"]
    manifest = json.loads((out / "manifest.json").read_text())
    assert any(name.startswith("previews/") for name in manifest["outputs"])
