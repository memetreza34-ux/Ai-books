"""Design-regression tests: covers are different, readable and print-audited."""
import json
from pathlib import Path

import pymupdf
import pytest

from aibooks.bookjob import build_from_spec, read_book_spec
from aibooks.cover import COVER_STYLES
from aibooks.preflight import audit_pdfs


def _spec():
    root = Path(__file__).resolve().parent.parent
    return json.loads((root / "projects/pilot-grossdruck-sudoku-120-de" / "book-spec.json").read_text())


def test_three_cover_variants_and_comparison_are_real_files(tmp_path):
    spec = _spec()
    spec["puzzles"] = 20
    source = tmp_path / "spec.json"
    source.write_text(json.dumps(spec))
    output = tmp_path / "book"
    build_from_spec(source, output, previews=True)
    image = output / "previews" / "cover-comparison.png"
    assert image.exists()
    pdf_hashes = set()
    for style in COVER_STYLES:
        file = output / f"cover-CONCEPT-{style}.pdf"
        assert file.exists()
        pdf_hashes.add(file.read_bytes())
        assert audit_pdfs(output / "interior-DRAFT.pdf", file)["machine_preflight_passed"]
        with pymupdf.open(str(file)) as pages:
            visible = pages[0].get_text()
            assert "Sudoku im Großdruck" in " ".join(visible.split())
            assert "20 SUDOKU" in " ".join(visible.split()) or (
                style == "noir" and "20" in visible)
    assert len(pdf_hashes) == 3
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["cover_study"]["selected"] == "editorial"
    assert len(manifest["cover_study"]["options"]) == 3
    assert manifest["outputs"]["previews/cover-comparison.png"]["sha256"]


@pytest.mark.parametrize("bad", ["AI_magic", "", None, 1])
def test_invalid_cover_styles_rejected_before_output(tmp_path, bad):
    spec = _spec()
    spec["cover_style"] = bad
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec))
    with pytest.raises(ValueError):
        read_book_spec(path)
