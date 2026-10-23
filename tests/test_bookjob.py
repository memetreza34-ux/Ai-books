"""A reusable one-book job contract, without pretending to publish."""
import json
from pathlib import Path

import pytest

from aibooks.bookjob import read_book_spec, build_from_spec
from aibooks.market import print_cost_de_bw_large


def _spec():
    repo = Path(__file__).resolve().parent.parent
    return json.loads((repo / "projects/pilot-grossdruck-sudoku-120-de/book-spec.json")
                      .read_text(encoding="utf-8"))


def test_spec_is_formally_valid(tmp_path: Path):
    path = tmp_path / "book.json"
    path.write_text(json.dumps(_spec()), encoding="utf-8")
    assert read_book_spec(path)["puzzles"] == 120
    assert read_book_spec(path)["solutions_per_page"] == 2


def test_book_job_produces_honest_full_package(tmp_path: Path):
    spec = _spec()
    spec["puzzles"] = 20  # fast regression; dedicated GitHub job builds all 120
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    out = tmp_path / "draft"
    result = build_from_spec(spec_path, out, previews=False)
    assert result["pages"] == 34
    assert result["sale_ready"] is False
    qa = json.loads((out / "quality-report.json").read_text())
    manifest = json.loads((out / "manifest.json").read_text())
    plan = json.loads((out / "production-plan-DRAFT.json").read_text())
    meta = json.loads((out / "listing-metadata-DRAFT.json").read_text())
    assert qa["editorial"]["content_consistency_passed"]
    assert qa["preflight"]["machine_preflight_passed"]
    assert qa["market_evidence"] == "HOLD"
    assert manifest["product_spec_id"] == "pilot-grossdruck-sudoku-120-de"
    assert not manifest["sale_ready"]
    assert plan["publishing_status"] == "NOT_APPROVED"
    assert plan["print_profile"]["total_pages"] == 34
    assert meta["author_or_imprint"] is None
    assert len(manifest["outputs"]) >= 7
    assert print_cost_de_bw_large(result["pages"]) > 0


def test_unsafe_claims_or_overwrites_blocked(tmp_path: Path):
    bad = _spec()
    bad["difficulty_label"] = "leicht"
    spec_file = tmp_path / "bad.json"
    spec_file.write_text(json.dumps(bad))
    with pytest.raises(ValueError, match="unverified"):
        build_from_spec(spec_file, tmp_path / "not-created")
    assert not (tmp_path / "not-created").exists()
    good = _spec()
    spec_file.write_text(json.dumps(good))
    out = tmp_path / "existing"
    out.mkdir()
    (out / "important.txt").write_text("do not delete")
    with pytest.raises(FileExistsError):
        build_from_spec(spec_file, out)
    assert (out / "important.txt").read_text() == "do not delete"


@pytest.mark.parametrize("key,value", [
    ("market_status", "GO"),
    ("user_approved_to_publish", True),
    ("paper", "color"),
    ("solutions_per_page", 3),
    ("seed", True),
    ("puzzles", 160)
])
def test_book_contract_blocks_unsupported_or_unapproved(tmp_path: Path, key, value):
    bad = _spec()
    bad[key] = value
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps(bad))
    with pytest.raises(ValueError):
        read_book_spec(spec)
