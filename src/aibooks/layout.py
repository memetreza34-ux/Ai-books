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
    c.setFont(bold, 19)
    c.drawString(56, 731, text)
    c.setStrokeColor(HexColor("#DDE5EC"))
    c.line(56, 714, PAGE_W - 56, 714)
    c.setFont(regular, 9)
    c.setFillColor(MUTED)
    c.drawCentredString(PAGE_W / 2, 34, f"{page}  ·  Ai-books Muster / Entwurf")


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


def interior_pdf(path: Path, title: str, items: list[dict], solutions_per_page: int = 4) -> int:
    if solutions_per_page not in (2, 4):
        raise ValueError('Only two or four solutions per page are supported')
    regular, bold = fonts()
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H), invariant=1)
    c.setTitle(title + " - Innen-PDF ENTWURF")
    c.setAuthor("Ai-books Studio Prototype")
    page = 0

    # 1: Title
    c.setFillColor(INK)
    # The printed title must match the manifest and wraparound cover.
    title_size, title_lines = fitted_title_lines(
        title, bold, PAGE_W - 112, max_size=33, min_size=20
    )
    c.setFont(bold, title_size)
    first_y = 510 if len(title_lines) == 1 else 540
    for index, line in enumerate(title_lines):
        c.drawCentredString(PAGE_W / 2, first_y - index * (title_size * 1.35), line)
    c.setFont(regular, 15)
    c.drawCentredString(PAGE_W / 2, 466, "Sudoku-Rätselbuch · interne Testausgabe")
    c.setFont(regular, 11)
    c.setFillColor(MUTED)
    c.drawCentredString(PAGE_W / 2, 415, f"{len(items)} geprüfte Rätsel mit Lösungen")
    c.drawCentredString(PAGE_W / 2, 140, "Studio-Prototyp · Kein kommerzielles Endprodukt")
    page += 1
    page_done(c)

    # 2: Introduction
    page += 1
    heading(c, "Willkommen", page, regular, bold)
    c.setFont(regular, 12)
    for i, line in enumerate([
        "Dieses Heft enthält automatisch erzeugte 9x9-Sudoku-Rätsel.",
        "Jede Aufgabe besitzt nach technischer Prüfung genau eine Lösung.",
        "Trage die Ziffern 1 bis 9 ein. In jeder Zeile, jeder Spalte",
        "und jedem 3x3-Block darf jede Ziffer nur einmal vorkommen.",
        "Die Lösungen findest du am Ende des Buches.",
        "Die vorliegende PDF ist eine Musterausgabe zur Layoutprüfung.",
    ]):
        c.drawString(60, 650 - i * 28, line)
    page_done(c)

    # 3: Legend
    page += 1
    heading(c, "So nutzt du das Buch", page, regular, bold)
    c.setFont(regular, 12)
    for i, line in enumerate([
        "1. Beginne mit einer Zeile, Spalte oder einem Block.",
        "2. Notiere mögliche Ziffern, falls du nicht sicher bist.",
        "3. Nutze nur logische Schlüsse, keine doppelten Ziffern.",
        "4. Prüfe dein Ergebnis mit der passenden Lösungsnummer.",
        "Die Rätsel sind nach Hinweisdichte einheitlich erzeugt.",
        "Eine geprüfte individuelle Schwierigkeitsklassifizierung",
        "wird in einer späteren Version ergänzt.",
    ]):
        c.drawString(60, 650 - i * 28, line)
    page_done(c)

    for item in items:
        page += 1
        heading(c, f"Rätsel {item['number']:03}", page, regular, bold)
        c.setFillColor(MUTED)
        c.setFont(regular, 11)
        c.drawString(56, 688, "9 × 9  ·  Je Zeile, Spalte und Block 1–9")
        draw_grid(c, item["puzzle"], x=90, y=171, size=432,
                  regular=regular, font_size=22)
        page_done(c)

    for start in range(0, len(items), solutions_per_page):
        page += 1
        heading(c, "Lösungen", page, regular, bold)
        for i, item in enumerate(items[start:start + solutions_per_page]):
            if solutions_per_page == 2:
                x, y, grid_size, label_y, label_x, label_size, number_size = (
                    156, 388 - i * 314, 300, 388 - i * 314 + 307, 156, 13, 15
                )
            else:
                col, row = i % 2, i // 2
                x, y, grid_size, label_y, label_x, label_size, number_size = (
                    77 + col * 255, 432 - row * 285, 190,
                    432 - row * 285 + 204, 77 + col * 255, 11, 9.8
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


