"""Single-book production and machine validation; no upload integrations."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json
from pypdf import PdfReader

from aibooks.layout import PAGE_H, PAGE_W, interior_pdf
from aibooks.cover import full_wrap_cover
from aibooks.preflight import audit_pdfs
from aibooks.editorial import audit_sudoku_text
from aibooks.sudoku import is_valid_solution, make_book, solve


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_sudoku(out: Path, title: str, count: int, seed: int,
                 clues: int, previews: bool = False, paper: str = "white",
                 solutions_per_page: int = 4) -> dict:
    if not title.strip() or len(title) > 90 or any(c in title for c in "\r\n"):
        raise ValueError("title must be a nonempty, single-line string <=90 chars")
    if not 20 <= count <= 150:
        raise ValueError("count must be from 20 to 150")
    if not 28 <= clues <= 70:
        raise ValueError("clues must be from 28 to 70")
    if solutions_per_page not in (2, 4):
        raise ValueError("solutions_per_page must be 2 or 4")
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"Output folder must be empty: {out}")
    out.mkdir(parents=True, exist_ok=True)
    puzzles = make_book(count, seed, clues)
    for item in puzzles:
        if not is_valid_solution(item["solution"]):
            raise AssertionError(f"Invalid solution for {item['number']}")
        solutions, actual = solve(item["puzzle"])
        if solutions != 1 or actual != item["solution"]:
            raise AssertionError(f"Not uniquely solvable: {item['number']}")
    if len(set(p["hash"] for p in puzzles)) != count:
        raise AssertionError("Duplicate puzzles")
    interior = out / "interior-DRAFT.pdf"
    cover = out / "cover-WRAP-DRAFT.pdf"
    pages = interior_pdf(interior, title, puzzles, solutions_per_page)
    geometry = full_wrap_cover(cover, title, puzzles, pages, paper)
    preflight = audit_pdfs(interior, cover, paper)
    if not preflight["machine_preflight_passed"]:
        raise AssertionError("Preflight blocked: " + "; ".join(preflight["problems"][:5]))
    editorial = audit_sudoku_text(interior, cover, title, count, solutions_per_page)
    if not editorial["content_consistency_passed"]:
        raise AssertionError("Editorial check blocked: " + "; ".join(editorial["problems"][:5]))
    reader = PdfReader(interior, strict=True)
    if len(reader.pages) != pages or pages < 24 or pages % 2:
        raise AssertionError("Incorrect interior page count")
    for n, page in enumerate(reader.pages, 1):
        mb = page.mediabox
        if abs(float(mb.width) - PAGE_W) > 0.05 or abs(float(mb.height) - PAGE_H) > 0.05:
            raise AssertionError(f"Incorrect trim size on page {n}")
    _ = PdfReader(cover, strict=True)
    payload = [{
        "number": x["number"], "puzzle": x["puzzle"],
        "solution": x["solution"], "hash": x["hash"]
    } for x in puzzles]
    data_file = out / "puzzles-and-solutions.json"
    data_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    qa = {
        "status": "MACHINE_PREFLIGHTED_DRAFT",
        "human_approved": False,
        "kdp_previewer_verified": False,
        "printed_proof_approved": False,
        "cover_full_wrap_generated": True,
        "kdp_template_approved": False,
        "preflight": preflight,
        "editorial": editorial,
        "puzzles": count, "solutions_per_page": solutions_per_page,
        "unique_puzzles": count, "all_solutions_unique": True,
        "all_solutions_verified": True, "interior_pages": pages,
        "trim_inches": [8.5, 11], "bleed": False,
        "used_fonts_embedded": True,
        "paper": paper,
        "spine_inches": round(geometry.spine_in, 6),
        "checks_performed": ["solution uniqueness", "duplicate hashes", "PDF parse",
                             "page count", "page dimensions", "full-wrap size",
                             "used font embedding", "text safety margins",
                             "title and count consistency", "puzzle/solution heading parity"],
        "checks_still_required": preflight["still_required"]
    }
    quality_file = out / "quality-report.json"
    quality_file.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    files = [interior, cover, data_file, quality_file]
    if previews:
        from aibooks.preview import contact_sheets, cover_preview
        files.extend(contact_sheets(interior, out / "previews"))
        files.append(cover_preview(cover, out / "previews" / "cover-full-wrap.png"))
    manifest = {
        "project": "Ai-books", "version": "0.1.0",
        "product_type": "sudoku", "title": title, "language": "de",
        "count": count, "clues_per_puzzle": clues, "seed": seed,
        "solutions_per_page": solutions_per_page,
        "paper": paper, "spine_inches": round(geometry.spine_in, 6),
        "status": "DRAFT", "sale_ready": False,
        "outputs": {
            str(x.relative_to(out)): {"sha256": file_hash(x), "bytes": x.stat().st_size}
            for x in files
        },
        "notes": "Full-wrap DRAFT, not KDP Previewer-approved. No automatic publication."
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"output": str(out), "pages": pages, "puzzles": count,
            "status": qa["status"], "files": sorted(str(p.relative_to(out)) for p in files) + ["manifest.json"]}
