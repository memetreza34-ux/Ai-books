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


def cover_preview(pdf: Path, destination: Path) -> Path:
    """Rasterize the single-page full-wrap PDF to a reviewable PNG."""
    import pymupdf
    from PIL import Image
    destination.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(str(pdf)) as pages:
        if len(pages) != 1:
            raise ValueError("Cover preview expects exactly one cover page")
        pix = pages[0].get_pixmap(matrix=pymupdf.Matrix(1.0, 1.0), alpha=False)
        Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(destination, optimize=True)
    return destination

def cover_comparison(preview_files: dict[str, Path], output: Path) -> Path:
    """Side-by-side cropped FRONT covers; original full-wrap PDFs stay untouched."""
    from PIL import Image, ImageDraw
    if set(preview_files) != {"editorial", "blueprint", "noir"}:
        raise ValueError("Cover comparison needs all three styles")
    width, height, label_height, pad = 408, 540, 52, 18
    canvas = Image.new("RGB", (3 * width + 4 * pad, height + label_height + 2 * pad), "#E5E6E4")
    brush = ImageDraw.Draw(canvas)
    for index, name in enumerate(("editorial", "blueprint", "noir")):
        with Image.open(preview_files[name]) as im:
            image = im.convert("RGB")
        # full-wrap front occupies slightly less than right half; take rightmost 48%.
        x0 = round(image.width * 0.515)
        front = image.crop((x0, 0, image.width, image.height))
        front.thumbnail((width, height))
        left = pad + index * (width + pad)
        canvas.paste(front, (left, pad + label_height))
        brush.text((left + 12, pad + 15), name.upper(), fill="#27333B")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)
    return output
