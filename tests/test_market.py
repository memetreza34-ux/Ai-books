"""Retail data quality, arithmetic and conservative market decision."""
from datetime import date
from copy import deepcopy
import json
import pytest

from aibooks.market import (
    evaluate_market, evaluate_market_file, print_cost_de_bw_large,
    paperback_royalty_scenario,
)


def fixture():
    from pathlib import Path
    return json.loads((Path(__file__).resolve().parent.parent /
                       "examples" / "retailer-observations-de.json").read_text(encoding="utf-8"))


def test_real_snapshot_is_not_claimed_as_sales():
    result = evaluate_market(fixture(), date(2026, 10, 23))
    assert [n["id"] for n in result["niches"]] == [
        "sudoku-grossdruck", "mathe-grundschule", "kinder-labyrinthe"]
    assert result["all_niches_commercial_status"] == "HOLD"
    assert result["sales_estimated"] is False
    assert not result["commercial_best_niche_selected"]
    assert all(n["commercial_decision"] == "HOLD" for n in result["niches"])
    assert result["niches"][0]["retailer_price_range_gross_eur"] == ["3.99", "19.99"]
    assert result["niches"][0]["kdp_print_plan"]["print_cost_eur"] == "3.05"
    assert all(not o["live_checked_by_this_code"]
               for n in result["niches"] for o in n["retailer_observations"])


def test_official_de_printing_rate_boundaries():
    assert print_cost_de_bw_large(40) == 2.48
    assert print_cost_de_bw_large(110) == 2.48
    assert print_cost_de_bw_large(112) == 2.542
    with pytest.raises(ValueError):
        print_cost_de_bw_large(23)


def test_kdp_scenarios_not_sales_projections():
    first = paperback_royalty_scenario(144, "9.98")
    second = paperback_royalty_scenario(144, "9.99")
    assert first["royalty_rate"] == "0.50"
    assert second["royalty_rate"] == "0.60"
    assert first["is_a_sales_forecast"] is False
    assert second["royalty_before_other_expenses_eur"] == "2.94"


@pytest.mark.parametrize("bad", [
    "http://www.thalia.de/shop/home/artikeldetails/A123",
    "https://thalia.de.evil.com/shop/home/artikeldetails/A123",
    "https://example.com/anything",
    "https://www.hugendubel.de.evil.com/de/taschenbuch/anything",
])
def test_untrusted_merchant_domains_fail(bad):
    sample = fixture()
    sample["niches"][0]["offers"][0]["url"] = bad
    with pytest.raises(ValueError):
        evaluate_market(sample, date(2026, 10, 23))


def test_old_stale_offer_rejected():
    sample = fixture()
    sample["niches"][0]["offers"][0]["observed_on"] = "2023-01-01"
    with pytest.raises(ValueError):
        evaluate_market(sample, date(2026, 10, 23))


def test_no_overwrite(tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps(fixture()))
    target = tmp_path / "report.json"
    answer = evaluate_market_file(p, target, date(2026, 10, 23))
    assert answer["niches"]
    with pytest.raises(FileExistsError):
        evaluate_market_file(p, target, date(2026, 10, 23))


def test_bad_source_claim_blocked():
    sample = fixture()
    sample["niches"][1]["offers"][0]["source_method"] = "fabricated_live_scrape"
    with pytest.raises(ValueError):
        evaluate_market(sample, date(2026, 10, 23))


def test_sample_price_not_a_kdp_price():
    result = evaluate_market(fixture(), date(2026, 10, 23))
    offer = result["niches"][0]["retailer_observations"][0]
    scenario = result["niches"][0]["kdp_print_plan"]["illustrative_scenarios"][0]
    assert "including_vat" in offer
    assert "before_vat" in scenario
