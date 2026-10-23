"""KDP paperback full-wrap *draft* for 8.5 x 11 inch B&W Sudoku books."""
from dataclasses import dataclass
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from aibooks.layout import fonts, draw_grid, fitted_title_lines

PT = 72.0
TRIM_W, TRIM_H, BLEED = 8.5, 11.0, 0.125
SPINE_MULTIPLIERS = {"white": 0.002252, "cream": 0.0025}


@dataclass(frozen=True)
class CoverGeometry:
    page_count: int
    paper: str
    spine_in: float
    page_width_pt: float
    page_height_pt: float
    back_start_pt: float
    spine_start_pt: float
    front_start_pt: float


def cover_geometry(page_count: int, paper: str = "white") -> CoverGeometry:
    if paper not in SPINE_MULTIPLIERS:
        raise ValueError("Supported B&W paper: white or cream")
    max_pages = 590 if paper == "white" else 550
    if not 24 <= page_count <= max_pages or page_count % 2:
        raise ValueError(f"Even page count 24..{max_pages} required")
    spine = page_count * SPINE_MULTIPLIERS[paper]
    back = BLEED * PT
    spine_start = back + TRIM_W * PT
    front = spine_start + spine * PT
    return CoverGeometry(page_count, paper, spine,
                         (2 * TRIM_W + spine + 2 * BLEED) * PT,
                         (TRIM_H + 2 * BLEED) * PT, back, spine_start, front)


def full_wrap_cover(path: Path, title: str, puzzles: list[dict],
                    page_count: int, paper: str = "white") -> CoverGeometry:
    if not puzzles:
        raise ValueError("At least one puzzle required")
    g = cover_geometry(page_count, paper)
    regular, bold = fonts()
    c = canvas.Canvas(str(path), pagesize=(g.page_width_pt, g.page_height_pt), invariant=1)
    c.setTitle(title + " - full-wrap DRAFT")
    c.setAuthor("Ai-books prototype")
    navy, mid = HexColor("#11223B"), HexColor("#183354")
    pale, blue = HexColor("#F5F8FC"), HexColor("#70C2E6")
    secondary = HexColor("#B4CEE2")
    c.setFillColor(navy)
    c.rect(0, 0, g.page_width_pt, g.page_height_pt, stroke=0, fill=1)
    fx = g.front_start_pt
    c.setFillColor(mid)
    c.rect(fx, 0, g.page_width_pt - fx, g.page_height_pt, stroke=0, fill=1)
    c.setFillColor(blue)
    c.rect(fx + 57, 754, 90, 5, stroke=0, fill=1)

    centre = fx + TRIM_W * PT / 2
    c.setFillColor(secondary)
    c.setFont(bold, 11)
    c.drawCentredString(centre, 733, "RÄTSELBUCH  ·  9 × 9")
    c.setFillColor(pale)
    title_size, title_lines = fitted_title_lines(
        title, bold, max_width=500, max_size=42, min_size=20
    )
    c.setFont(bold, title_size)
    baseline = 627 if len(title_lines) == 1 else 670
    for index, line in enumerate(title_lines):
        c.drawCentredString(centre, baseline - index * (title_size * 1.18), line)
    c.setFillColor(secondary)
    c.setFont(regular, 18)
    c.drawCentredString(centre, 575, "KONZENTRATION. LOGIK. RÄTSELSPASS.")
    c.setFillColor(pale)
    c.roundRect(fx + 96, 211, 420, 347, 16, stroke=0, fill=1)
    draw_grid(c, puzzles[0]["puzzle"], fx + 166, 247, 280, regular, 16)
    c.setFillColor(blue)
    c.setFont(bold, 22)
    c.drawCentredString(centre, 158, f"{len(puzzles)} SUDOKU-RÄTSEL")
    c.setFillColor(secondary)
    c.setFont(regular, 15)
    c.drawCentredString(centre, 130, "MIT GEPRÜFTEN LÖSUNGEN")
    c.setFillColor(HexColor("#F6C67B"))
    c.setFont(bold, 10)
    c.drawCentredString(centre, 54, "ENTWURF  ·  NICHT VERÖFFENTLICHEN")

    bx = g.back_start_pt + 55
    c.setFillColor(pale)
    c.setFont(bold, 28)
    c.drawString(bx, 665, "EIN MOMENT FÜR DICH.")
    c.setFillColor(secondary)
    c.setFont(regular, 15)
    lines = [
        "Nimm dir Zeit für eine neue Denksportaufgabe.",
        f"In diesem Band erwarten dich {len(puzzles)} Sudoku-Rätsel",
        "mit einem klassischen 9 × 9-Raster.",
        "Jedes Rätsel hat genau eine überprüfte Lösung.",
        "Alle Lösungen findest du im hinteren Buchteil.",
    ]
    for i, line in enumerate(lines):
        c.drawString(bx, 605 - i * 33, line)
    c.setStrokeColor(blue)
    c.setLineWidth(3)
    c.line(bx, 389, bx + 225, 389)
    c.setFillColor(pale)
    c.setFont(bold, 14)
    c.drawString(bx, 352, "DIESER BAND ENTHÄLT")
    c.setFillColor(secondary)
    c.setFont(regular, 13)
    for i, line in enumerate(["• Sudoku im klassischen 9 × 9-Format",
                               "• Ein Rätsel pro Seite",
                               "• Nummerierte Lösungsseiten"]):
        c.drawString(bx, 324 - 30 * i, line)
    c.setFillColor(HexColor("#F6C67B"))
    c.setFont(bold, 10)
    c.drawString(bx, 80, "INTERNE MUSTERAUSGABE  ·  KEIN VERKAUFSTITEL")

    # Reserve blank 2 by 1.2 inch zone, lower-right corner of BACK cover.
    bar_x = g.spine_start_pt - (2.0 + 0.375) * PT
    bar_y = (BLEED + 0.375) * PT
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(bar_x, bar_y, 2 * PT, 1.2 * PT, stroke=0, fill=1)
    # No spine text: the 40-page reference is below KDP's 79-page threshold.
    c.save()
    return g
