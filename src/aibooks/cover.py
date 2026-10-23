"""Three reproducible editorial cover systems for a KDP full-wrap DRAFT.

All typography is vector/embedded. Layouts are intentionally low-ink on backs
and remain subject to KDP template validation and human art direction.
"""
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from aibooks.layout import fonts, draw_grid, fitted_title_lines

PT = 72.0
TRIM_W, TRIM_H, BLEED = 8.5, 11.0, 0.125
SPINE_MULTIPLIERS = {"white": 0.002252, "cream": 0.0025}
COVER_STYLES = ("editorial", "blueprint", "noir")

STYLES = {
    "editorial": {
        "label": "Editorial · Papier / Terrakotta",
        "base": "#F5F0E8", "back": "#F5F0E8", "ink": "#24312F",
        "muted": "#62716B", "accent": "#B45F41", "paper": "#FFFFFF",
        "shape": "column"
    },
    "blueprint": {
        "label": "Blueprint · Tinte / Himmelblau",
        "base": "#183C54", "back": "#112F43", "ink": "#FFFFFF",
        "muted": "#B9DCE5", "accent": "#F5BB71", "paper": "#F5F8F7",
        "shape": "band"
    },
    "noir": {
        "label": "Noir · Graphit / Kupfer",
        "base": "#252829", "back": "#252829", "ink": "#F7F3ED",
        "muted": "#C8C7BD", "accent": "#D3A57D", "paper": "#F7F3ED",
        "shape": "frame"
    }
}


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


def _draw_grid_card(c, x, y, side, puzzle, regular, style):
    background = HexColor(STYLES[style]["paper"])
    c.setFillColor(background)
    c.roundRect(x - 22, y - 22, side + 44, side + 44, 5,
                stroke=0, fill=1)
    draw_grid(c, puzzle, x, y, side, regular, 15.5)


def _front_noir(c, g, puzzle, regular, bold, title, count):
    """Type-led alternative, intentionally without the dominant Sudoku card."""
    x = g.front_start_pt
    cx = x + TRIM_W * PT / 2
    ink = HexColor(STYLES["noir"]["ink"])
    muted = HexColor(STYLES["noir"]["muted"])
    accent = HexColor(STYLES["noir"]["accent"])
    c.setStrokeColor(accent)
    c.setLineWidth(1.5)
    c.rect(x + 49, 143, 514, 586, fill=0, stroke=1)
    c.setFillColor(muted)
    c.setFont(bold, 11)
    c.drawString(x + 68, 735, "DIE RÄTSEL-EDITION  /  01")
    c.setFillColor(accent)
    c.setFont(bold, 145)
    c.drawCentredString(cx, 542, str(count))
    c.setFillColor(ink)
    size, lines = fitted_title_lines(title, bold, 485, 35, 21)
    c.setFont(bold, size)
    baseline = 450 if len(lines) == 1 else 473
    for idx, line in enumerate(lines):
        c.drawCentredString(cx, baseline - idx * size * 1.32, line)
    c.setFont(regular, 12)
    c.setFillColor(muted)
    c.drawCentredString(cx, 369, "EIN RÄTSEL PRO SEITE  ·  GEPRÜFTE LÖSUNGEN")
    # Smaller preview acknowledges Sudoku as a product, but typography is hero.
    _draw_grid_card(c, cx - 76, 171, 152, puzzle, regular, "noir")
    c.setFillColor(muted)
    c.setFont(regular, 10)
    c.drawCentredString(cx, 110, "9 × 9  /  GROSSZÜGIGES FORMAT")
    c.setFont(bold, 7.5)
    c.drawCentredString(cx, 55, "ENTWURF · NICHT ZUM VERKAUF")


def _front_art(c, g, style, puzzle, regular, bold, title, count):
    s = STYLES[style]
    x = g.front_start_pt
    cx = x + TRIM_W * PT / 2
    ink, accent, muted = map(HexColor, [s["ink"], s["accent"], s["muted"]])
    c.setFillColor(ink)
    c.setFont(bold, 11)
    c.drawString(x + 64, 730, "SUDOKU  /  DIE GROSSE EDITION")
    c.setFillColor(accent)
    if style == "editorial":
        c.rect(x + 64, 706, 50, 4, fill=1, stroke=0)
        c.rect(x + 64, 153, 482, 2, fill=1, stroke=0)
        card_y, card_side = 244, 242
        title_top = 649
    elif style == "blueprint":
        c.rect(x + 58, 703, 496, 4, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#416782"))
        c.setLineWidth(0.55)
        for k in range(8):
            c.line(x + 62 + k * 65, 203, x + 62 + k * 65, 518)
        card_y, card_side = 248, 235
        title_top = 652
    else:
        c.setLineWidth(2)
        c.setStrokeColor(accent)
        c.rect(x + 49, 161, 514, 558, fill=0, stroke=1)
        c.rect(x + 64, 704, 55, 4, fill=1, stroke=0)
        card_y, card_side = 244, 235
        title_top = 641

    # A smaller max title size keeps a deliberate visual hierarchy on all styles.
    title_size, lines = fitted_title_lines(title, bold, 485, 39, 22)
    c.setFillColor(ink)
    c.setFont(bold, title_size)
    top_baseline = title_top + (title_size * .45 if len(lines) > 1 else 0)
    for i, line in enumerate(lines):
        c.drawCentredString(cx, top_baseline - i * (title_size * 1.28), line)
    c.setFillColor(muted)
    c.setFont(regular, 13)
    c.drawCentredString(cx, 551, "EIN RÄTSEL PRO SEITE  ·  GEPRÜFTE LÖSUNGEN")
    _draw_grid_card(c, cx - card_side / 2, card_y, card_side, puzzle, regular, style)
    c.setFillColor(accent)
    c.setFont(bold, 27)
    c.drawCentredString(cx, 197, f"{count} SUDOKU")
    c.setFillColor(muted)
    c.setFont(regular, 12)
    c.drawCentredString(cx, 126, "9 × 9  /  GROSSZÜGIGES FORMAT")
    # DRAFT mark small and outside the central front artwork.
    c.setFont(bold, 7.5)
    c.drawCentredString(cx, 55, "ENTWURF · NICHT ZUM VERKAUF")


def _back_art(c, g, style, count, regular, bold):
    s = STYLES[style]
    x = g.back_start_pt + 53
    ink, muted, accent = map(HexColor, [s["ink"], s["muted"], s["accent"]])
    c.setFillColor(accent)
    c.rect(x, 693, 57, 4, stroke=0, fill=1)
    c.setFillColor(ink)
    c.setFont(bold, 24)
    c.drawString(x, 647, "ZEIT FÜR EIN RÄTSEL.")
    c.setFont(regular, 13.5)
    c.setFillColor(muted)
    for i, line in enumerate([
        "Ein klares Raster. Ein ruhiger Moment.",
        f"{count} nummerierte Sudoku mit je neun Zeilen",
        "und neun Spalten, eins pro Seite.",
        "Jedes Raster besitzt genau eine geprüfte Lösung.",
        "Zwei größere Lösungsraster pro Seite",
        "helfen beim anschließenden Vergleichen."
    ]):
        c.drawString(x, 579 - i * 30, line)
    c.setStrokeColor(accent)
    c.setLineWidth(2)
    c.line(x, 360, x + 220, 360)
    c.setFillColor(ink)
    c.setFont(bold, 13)
    c.drawString(x, 325, "IM BUCH")
    c.setFont(regular, 12.5)
    c.setFillColor(muted)
    for i, line in enumerate([
        "• Ein großes Sudoku pro Seite",
        "• Durchgängig nummerierte Lösungen",
        "• Ruhiger Satz, viel Platz zum Eintragen"
    ]):
        c.drawString(x, 290 - i * 29, line)
    # Keep all back-cover text away from the barcode rectangle.
    c.setFont(regular, 8)
    c.drawString(x, 67, "INTERNE DESIGNSTUDIE · KDP-FREIGABE AUSSTEHEND")


def full_wrap_cover(path: Path, title: str, puzzles: list[dict],
                    page_count: int, paper: str = "white",
                    style: str = "editorial") -> CoverGeometry:
    if style not in COVER_STYLES:
        raise ValueError("Unknown cover style: " + str(style))
    if not puzzles:
        raise ValueError("At least one puzzle required")
    g = cover_geometry(page_count, paper)
    regular, bold = fonts()
    s = STYLES[style]
    c = canvas.Canvas(str(path), pagesize=(g.page_width_pt, g.page_height_pt),
                      invariant=1)
    c.setTitle(title + " – " + style + " – Cover-DRAFT")
    c.setAuthor("Ai-books editorial design experiment")
    c.setFillColor(HexColor(s["back"]))
    c.rect(0, 0, g.page_width_pt, g.page_height_pt, stroke=0, fill=1)
    c.setFillColor(HexColor(s["base"]))
    c.rect(g.front_start_pt, 0, g.page_width_pt - g.front_start_pt,
           g.page_height_pt, stroke=0, fill=1)

    _back_art(c, g, style, len(puzzles), regular, bold)
    if style == "noir":
        _front_noir(c, g, puzzles[0]["puzzle"], regular, bold, title, len(puzzles))
    else:
        _front_art(c, g, style, puzzles[0]["puzzle"], regular, bold, title, len(puzzles))

    # KDP auto-barcode: reserve white 2 x 1.2 inch box, lower-right back cover.
    bx = g.spine_start_pt - (2 + .375) * PT
    by = (BLEED + .375) * PT
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(bx, by, 2 * PT, 1.2 * PT, fill=1, stroke=0)
    # Spine text intentionally absent, even above KDP's 79-page threshold.
    c.save()
    return g
