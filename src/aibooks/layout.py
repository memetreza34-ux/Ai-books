"""Vector-based Sudoku interior draft layout with embedded font support."""
from __future__ import annotations

from pathlib import Path
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

PAGE_W, PAGE_H = 612, 792  # 8.5 x 11 inch; intentional NO BLEED
INK = HexColor("#13243A")
MUTED = HexColor("#5C6670")
ACCENT = HexColor("#2B5E81")


def fonts() -> tuple[str, str]:
    root = Path(reportlab.__file__).resolve().parent / "fonts"
    regular, bold = root / "Vera.ttf", root / "VeraBd.ttf"
    if not regular.is_file() or not bold.is_file():
        raise FileNotFoundError("Bundled Vera TTF fonts missing; cannot embed font")
    if "AiVera" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("AiVera", str(regular)))
        pdfmetrics.registerFont(TTFont("AiVeraBold", str(bold)))
    return "AiVera", "AiVeraBold"



def fitted_title_lines(title: str, font: str, max_width: float,
                       max_size: int, min_size: int = 20) -> tuple[int, list[str]]:
    """Fit a title into at most two centred lines, without breaking words."""
    words = title.split()
    if not words:
        raise ValueError("Title cannot be blank")
    for size in range(max_size, min_size - 1, -1):
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if pdfmetrics.stringWidth(candidate, font, size) <= max_width:
                current = candidate
            else:
                if not current:
                    break
                lines.append(current)
                current = word
        else:
            if current:
                lines.append(current)
            if len(lines) <= 2 and all(
                pdfmetrics.stringWidth(line, font, size) <= max_width for line in lines
            ):
                return size, lines
    raise ValueError("Title too long for a readable two-line cover or title page")

def heading(c: canvas.Canvas, text: str, page: int, regular: str, bold: str) -> None:
    c.setFillColor(INK)
    c.setFillColor(ACCENT)
    c.rect(56, 729, 5, 23, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont(bold, 18)
    c.drawString(72, 732, text)
    c.setStrokeColor(HexColor("#CBD4D4"))
    c.setLineWidth(0.7)
    c.line(56, 714, PAGE_W - 56, 714)
    c.setFont(regular, 8)
    c.setFillColor(MUTED)
    c.drawString(56, 39, "RÄTSEL  /  EDITION")
    c.drawRightString(PAGE_W - 56, 39, f"{page:03}  ·  ENTWURF")


def draw_grid(c: canvas.Canvas, grid: tuple, x: float, y: float,
              size: float, regular: str, font_size: float) -> None:
    cell = size / 9
    c.setFillColor(INK)
    for r in range(9):
        for col in range(9):
            value = grid[r][col]
            if value:
                c.setFont(regular, font_size)
                c.drawCentredString(x + (col + 0.5) * cell,
                                    y + size - (r + 0.72) * cell, str(value))
    for n in range(10):
        c.setStrokeColor(INK if n % 3 == 0 else HexColor("#8795A5"))
        c.setLineWidth(1.8 if n % 3 == 0 else 0.85)
        c.line(x + n * cell, y, x + n * cell, y + size)
        c.line(x, y + n * cell, x + size, y + n * cell)


def page_done(c: canvas.Canvas) -> None:
    c.showPage()


def solution_layout(index: int, solutions_per_page: int) -> tuple:
    """Layout contract in PDF points; gives labels sufficient visual breathing room."""
    if solutions_per_page == 2:
        if index not in (0, 1):
            raise ValueError("Two-solution pages accept index 0 or 1")
        x, y, side = 172, 385 - index * 313, 268
        return x, y, side, y + side + 15, x, 13, 13
    if solutions_per_page == 4:
        if index not in (0, 1, 2, 3):
            raise ValueError("Four-solution pages accept index 0..3")
        col, row = index % 2, index // 2
        x, y, side = 77 + col * 255, 432 - row * 285, 190
        return x, y, side, y + side + 14, x, 11, 9.8
    raise ValueError("Only 2 or 4 solutions per page supported")


def interior_pdf(path: Path, title: str, items: list[dict], solutions_per_page: int = 4) -> int:
    if solutions_per_page not in (2, 4):
        raise ValueError('Only two or four solutions per page are supported')
    regular, bold = fonts()
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H), invariant=1)
    c.setTitle(title + " - Innen-PDF ENTWURF")
    c.setAuthor("Ai-books Studio Prototype")
    page = 0

    # 1: Editorial title leaf. Keep content rights and final imprint unresolved.
    c.setFillColor(ACCENT)
    c.rect(64, 706, 80, 5, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(bold, 11)
    c.drawString(64, 735, "SUDOKU  /  RÄTSEL-EDITION")
    c.setFillColor(INK)
    title_size, title_lines = fitted_title_lines(
        title, bold, PAGE_W - 128, max_size=34, min_size=20
    )
    c.setFont(bold, title_size)
    first_y = 573 if len(title_lines) == 1 else 605
    for index, line in enumerate(title_lines):
        c.drawString(64, first_y - index * (title_size * 1.38), line)
    c.setFillColor(MUTED)
    c.setFont(regular, 13)
    c.drawString(64, 490, "Ein großzügiges Raster. Ein Rätsel pro Seite.")
    c.setStrokeColor(HexColor("#CFD9D8"))
    c.setLineWidth(1)
    c.line(64, 455, PAGE_W - 64, 455)
    c.setFillColor(ACCENT)
    c.setFont(bold, 61)
    c.drawString(61, 341, str(len(items)))
    c.setFillColor(INK)
    c.setFont(regular, 13)
    c.drawString(65, 307, "NUMMERIERTE SUDOKU MIT GEPRÜFTEN LÖSUNGEN")
    c.setFillColor(MUTED)
    c.setFont(regular, 9)
    c.drawString(64, 123, "Interne Designstudie · Nicht zum Verkauf")
    page += 1
    page_done(c)

    # 2: Introduction
    page += 1
    heading(c, "Willkommen", page, regular, bold)
    c.setFont(regular, 12)
    for i, line in enumerate([
        "Nimm dir einen Moment für dein nächstes Zahlenrätsel.",
        f"Auf den folgenden Seiten warten {len(items)} klassische 9×9-Sudoku.",
        "Jede Aufgabe steht auf einer eigenen, großzügigen Seite.",
        "Die dazugehörigen Lösungen findest du gesammelt im zweiten Teil.",
        "",
        "Alle Rätsel wurden technisch auf genau eine Lösung geprüft.",
        "Das Buch enthält keine geprüfte Schwierigkeits-Einstufung.",
    ]):
        c.drawString(62, 650 - i * 32, line)
    page_done(c)

    # 3: Legend
    page += 1
    heading(c, "So nutzt du das Buch", page, regular, bold)
    c.setFont(regular, 12)
    for i, line in enumerate([
        "01  Jede Zeile enthält die Ziffern 1 bis 9 genau einmal.",
        "02  Jede Spalte enthält die Ziffern 1 bis 9 genau einmal.",
        "03  Jeder umrandete 3×3-Block enthält 1 bis 9 genau einmal.",
        "04  Die vorgegebenen Zahlen dürfen nicht verändert werden.",
        "05  Nutze die Lösungen erst, wenn du dein Rätsel geprüft hast.",
        "",
        "Tipp: Suche zunächst nach Zeilen mit wenigen freien Feldern.",
    ]):
        c.drawString(62, 650 - i * 34, line)
    page_done(c)

    for item in items:
        page += 1
        heading(c, f"Rätsel {item['number']:03}", page, regular, bold)
        c.setFillColor(MUTED)
        c.setFont(regular, 11)
        c.drawString(56, 688, "9 × 9   /   EIN RÄTSEL PRO SEITE")
        draw_grid(c, item["puzzle"], x=90, y=171, size=432,
                  regular=regular, font_size=22)
        page_done(c)

    for start in range(0, len(items), solutions_per_page):
        page += 1
        heading(c, "Lösungen", page, regular, bold)
        for i, item in enumerate(items[start:start + solutions_per_page]):
            x, y, grid_size, label_y, label_x, label_size, number_size = (
                solution_layout(i, solutions_per_page)
            )
            c.setFont(bold, label_size)
            c.setFillColor(ACCENT)
            c.drawString(label_x, label_y, f"Rätsel {item['number']:03}")
            draw_grid(c, item["solution"], x=x, y=y, size=grid_size,
                      regular=regular, font_size=number_size)
        page_done(c)

    page += 1
    heading(c, "Notizen", page, regular, bold)
    c.setStrokeColor(HexColor("#CAD5DF"))
    for y in range(665, 95, -28):
        c.line(65, y, PAGE_W - 65, y)
    page_done(c)

    if page % 2:
        page += 1
        heading(c, "Weitere Notizen", page, regular, bold)
        c.setStrokeColor(HexColor("#CAD5DF"))
        for y in range(665, 95, -28):
            c.line(65, y, PAGE_W - 65, y)
        page_done(c)
    c.save()
    return page


