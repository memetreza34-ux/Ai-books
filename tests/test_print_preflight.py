from pathlib import Path
from reportlab.pdfgen import canvas
from aibooks.cover import cover_geometry
from aibooks.preflight import audit_pdfs
from aibooks.pipeline import build_sudoku


def test_40_page_cover_dimensions():
    g = cover_geometry(40, "white")
    assert abs(g.spine_in - 0.09008) < 1e-8
    assert abs(g.page_width_pt / 72 - 17.34008) < 1e-8
    assert abs(g.page_height_pt / 72 - 11.25) < 1e-8


def test_paper_changes_spine_and_wrong_profile_blocks(tmp_path: Path):
    out = tmp_path / "book"
    build_sudoku(out, "Sudoku Testband", 20, 29, 40)
    assert audit_pdfs(out / "interior-DRAFT.pdf",
                      out / "cover-WRAP-DRAFT.pdf", "white")["machine_preflight_passed"]
    bad = audit_pdfs(out / "interior-DRAFT.pdf",
                     out / "cover-WRAP-DRAFT.pdf", "cream")
    assert not bad["machine_preflight_passed"]
    assert any("dimensions" in x for x in bad["problems"])


def test_unembedded_used_helvetica_is_blocked(tmp_path: Path):
    out = tmp_path / "book"
    build_sudoku(out, "Test", 20, 21, 40)
    pdf = tmp_path / "unembedded.pdf"
    c = canvas.Canvas(str(pdf), pagesize=(612, 792))
    for i in range(32):
        c.setFont("Helvetica", 12)
        c.drawString(60, 690, "Text using an unembedded font")
        c.showPage()
    c.save()
    problems = audit_pdfs(pdf, out / "cover-WRAP-DRAFT.pdf")["problems"]
    assert any("not embedded" in x for x in problems)


def test_cream_paper_mode(tmp_path: Path):
    out = tmp_path / "cream"
    build_sudoku(out, "Test", 20, 7, 40, paper="cream")
    check = audit_pdfs(out / "interior-DRAFT.pdf",
                       out / "cover-WRAP-DRAFT.pdf", paper="cream")
    assert check["machine_preflight_passed"]
