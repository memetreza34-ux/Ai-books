"""Machine checks for fixed 8.5 x 11 inch B&W no-bleed paperback.

Checks are not equivalent to KDP previewer, physical proof or legal approval.
"""
from pathlib import Path

from pypdf import PdfReader
from aibooks.cover import cover_geometry, TRIM_H, TRIM_W


def _sizes(reader, width, height, label):
    return [f"{label} page {i}: incorrect dimensions"
            for i, page in enumerate(reader.pages, 1)
            if abs(float(page.mediabox.width) - width) > 0.1
            or abs(float(page.mediabox.height) - height) > 0.1]


def _used_fonts_embedded(path: Path, label: str):
    import pymupdf
    issues = []
    with pymupdf.open(str(path)) as pdf:
        for i, page in enumerate(pdf, 1):
            known = page.get_fonts(full=True)
            used = {span["font"]
                    for block in page.get_text("dict").get("blocks", [])
                    for line in block.get("lines", [])
                    for span in line.get("spans", [])
                    if span["text"].strip()}
            for font in sorted(used):
                matches = [f for f in known if f[3].split("+")[-1] == font]
                if not matches or not any(f[0] > 0 and len(pdf.extract_font(f[0])[3]) > 0
                                          for f in matches):
                    issues.append(f"{label} page {i}: used font {font} not embedded")
    return issues


def _text_safety(path: Path, geo, cover: bool):
    import pymupdf
    problems = []
    with pymupdf.open(str(path)) as pdf:
        for index, page in enumerate(pdf, 1):
            for block in page.get_text("dict").get("blocks", []):
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if not span["text"].strip():
                            continue
                        x0, y0, x1, y1 = span["bbox"]
                        if cover:
                            safe = 0.25 * 72
                            back_left = geo.back_start_pt + safe
                            back_right = geo.spine_start_pt - safe
                            front_left = geo.front_start_pt + safe
                            front_right = geo.front_start_pt + TRIM_W * 72 - safe
                            okay_x = ((x0 >= back_left and x1 <= back_right) or
                                      (x0 >= front_left and x1 <= front_right))
                            okay_y = (y0 >= 0.125 * 72 + safe and
                                      y1 <= geo.page_height_pt - 0.125 * 72 - safe)
                        else:
                            # Right-hand odd pages bind at left; even pages at right.
                            left = (0.375 if index % 2 else 0.25) * 72
                            right = (TRIM_W - (0.25 if index % 2 else 0.375)) * 72
                            okay_x = x0 >= left - 0.5 and x1 <= right + 0.5
                            okay_y = y0 >= 0.25 * 72 - 0.5 and y1 <= TRIM_H * 72 - 0.25 * 72 + 0.5
                        if not (okay_x and okay_y):
                            problems.append(f"{'Cover' if cover else 'Interior'} page {index}: unsafe text {span['text']!r}")
    return problems


def audit_pdfs(interior: Path, cover: Path, paper: str = "white"):
    inside = PdfReader(str(interior), strict=True)
    wrap = PdfReader(str(cover), strict=True)
    pages = len(inside.pages)
    errors = []
    if len(wrap.pages) != 1:
        errors.append("Cover must have exactly one page")
    try:
        geo = cover_geometry(pages, paper)
    except ValueError as exc:
        errors.append(str(exc))
        geo = None
    if geo:
        errors += _sizes(inside, TRIM_W * 72, TRIM_H * 72, "Interior")
        errors += _sizes(wrap, geo.page_width_pt, geo.page_height_pt, "Cover")
        errors += _text_safety(interior, geo, cover=False)
        errors += _text_safety(cover, geo, cover=True)
    errors += _used_fonts_embedded(interior, "Interior")
    errors += _used_fonts_embedded(cover, "Cover")
    return {
        "machine_preflight_passed": not errors,
        "page_count": pages, "paper": paper,
        "cover_dimensions_inches": [round(geo.page_width_pt / 72, 6),
                                    round(geo.page_height_pt / 72, 6)] if geo else None,
        "spine_inches": round(geo.spine_in, 6) if geo else None,
        "fonts": "verified for rendered text spans",
        "raster_images": "not used by the vector Sudoku prototype",
        "problems": errors,
        "still_required": ["full visual review", "official KDP Cover Calculator",
                           "KDP Previewer", "physical proof", "rights and buyer-demand review",
                           "human publication approval"]
    }
