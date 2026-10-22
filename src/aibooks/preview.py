"""Optional full-book contact-sheet previews.

Requires package extra 'preview'; does not modify the source PDF.
"""
from pathlib import Path


def contact_sheets(source_pdf: Path, target_dir: Path) -> list[Path]:
    try:
        import pymupdf
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError("Install the optional preview extras: pip install -e '.[preview]'") from exc
    target_dir.mkdir(parents=True, exist_ok=True)
    sheets: list[Path] = []
    with pymupdf.open(str(source_pdf)) as document:
        for start in range(0, len(document), 6):
            w, h, pad, title_h = 332, 430, 18, 30
            sheet = Image.new("RGB", (2 * w + 3 * pad, 3 * (h + title_h) + 4 * pad), "white")
            painter = ImageDraw.Draw(sheet)
            for index in range(start, min(start + 6, len(document))):
                r, col = divmod(index - start, 2)
                pix = document[index].get_pixmap(matrix=pymupdf.Matrix(0.50, 0.50), alpha=False)
                thumbnail = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                thumbnail.thumbnail((w, h))
                px = pad + col * (w + pad)
                py = pad + r * (h + title_h + pad)
                sheet.paste(thumbnail, (px, py))
                painter.text((px, py + h + 3), f"Seite {index + 1}", fill="black")
            file = target_dir / f"contact-sheet-{start // 6 + 1:03d}.png"
            sheet.save(file, optimize=True)
            sheets.append(file)
    return sheets
