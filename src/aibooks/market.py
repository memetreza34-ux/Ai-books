"""Evidence-controlled bookstore comparison and KDP printing scenarios.

Retailer observations are supplied as dated snapshots. This module never
fetches or certifies retailer pages, infers unit sales, or authorizes publishing.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from statistics import median
from urllib.parse import urlsplit
import json

PRINT_COST_SOURCE = "https://kdp.amazon.com/de_DE/help/topic/G201834340"
ROYALTY_SOURCE = "https://kdp.amazon.com/de_DE/help/topic/G201834330"
ALLOWED_MERCHANTS = {"thalia.de", "hugendubel.de"}
REQUIRED_NICHES = {"sudoku-grossdruck", "mathe-grundschule", "kinder-labyrinthe"}


def _decimal(value: object, field: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"{field} must be a number")
    try:
        d = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be a decimal") from exc
    if not d.is_finite():
        raise ValueError(f"{field} must be finite")
    return d


def _euros(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _merchant(link: str) -> str:
    if not isinstance(link, str):
        raise ValueError("Offer needs a URL")
    parts = urlsplit(link)
    host = (parts.hostname or "").lower().removeprefix("www.")
    if parts.scheme != "https" or host not in ALLOWED_MERCHANTS:
        raise ValueError("Merchant not allowlisted")
    if host == "thalia.de" and not parts.path.startswith("/shop/home/artikeldetails/"):
        raise ValueError("Thalia URL must be a product detail")
    if host == "hugendubel.de" and not parts.path.startswith("/de/"):
        raise ValueError("Hugendubel URL must be a product detail")
    if parts.username or parts.password:
        raise ValueError("Credentials in URL forbidden")
    return host


def print_cost_de_bw_large(pages: int) -> Decimal:
    """Germany Amazon marketplace, large paperback B&W, white or cream.

    Static official rate snapshot checked 2026-10-23. Recheck KDP before use.
    """
    if type(pages) is not int or pages < 24 or pages > 590 or pages % 2:
        raise ValueError("Expected even 24..590 paperback pages")
    if pages <= 110:
        return Decimal("2.48")
    return Decimal("0.75") + Decimal("0.016") * pages


def paperback_royalty_scenario(pages: int, net_list_price_eur: object) -> dict:
    """Direct Amazon marketplace example, before taxes/ad/other costs.

    KDP list price must be entered EXCLUDING applicable customer VAT.
    """
    p = _decimal(net_list_price_eur, "net_list_price_eur")
    if not Decimal("4.96") <= p <= Decimal("250"):
        raise ValueError("Scenario net list price must be between 4.96 and 250 EUR")
    royalty_rate = Decimal("0.60") if p >= Decimal("9.99") else Decimal("0.50")
    cost = print_cost_de_bw_large(pages)
    payout = royalty_rate * p - cost
    if payout < 0:
        raise ValueError("Scenario below estimated KDP print-cost recovery; increase list price")
    return {
        "list_price_before_vat_eur": _euros(p),
        "royalty_rate": _euros(royalty_rate),
        "print_cost_eur": _euros(cost),
        "royalty_before_other_expenses_eur": _euros(payout),
        "is_a_sales_forecast": False,
        "rate_assumptions_checked_on": "2026-10-23",
        "rate_source": PRINT_COST_SOURCE,
        "royalty_source": ROYALTY_SOURCE,
        "limitations": "Illustrative DE large-format B&W, direct Amazon channel, before taxes, ads, operating expenses and refunds; confirm current KDP settings."
    }


def evaluate_market(data: dict, today: date | None = None) -> dict:
    today = today or date.today()
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Expected schema_version = 1")
    niches = data.get("niches")
    if not isinstance(niches, list) or not niches or len(niches) > 10:
        raise ValueError("Need 1..10 niches")
    outputs, ids = [], set()
    for niche in niches:
        if not isinstance(niche, dict):
            raise ValueError("Niche must be an object")
        ident, name = niche.get("id"), niche.get("name")
        if not isinstance(ident, str) or not ident or ident in ids:
            raise ValueError("Every niche needs a unique ID")
        ids.add(ident)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Every niche needs a name")
        readiness = niche.get("engineering_readiness")
        if type(readiness) is not int or not 0 <= readiness <= 10:
            raise ValueError("engineering_readiness must be an integer 0..10")
        offers = niche.get("offers")
        if not isinstance(offers, list) or not 1 <= len(offers) <= 30:
            raise ValueError("At least one retailer product observation required")
        processed, urls, hosts, errors = [], set(), set(), []
        for offer in offers:
            if not isinstance(offer, dict):
                raise ValueError("Offer must be an object")
            uri = offer.get("url")
            host = _merchant(uri)
            if uri in urls:
                raise ValueError("Repeated retailer URL in same niche")
            urls.add(uri)
            hosts.add(host)
            observed = date.fromisoformat(offer["observed_on"])
            age = (today - observed).days
            if age < 0 or age > 90:
                raise ValueError("Retail observations older than 90 days or from the future")
            title = offer.get("title")
            if not isinstance(title, str) or len(title.strip()) < 8:
                raise ValueError("Incomplete retailer title")
            price = _decimal(offer.get("consumer_price_eur"), "consumer_price_eur")
            if not Decimal("0.01") <= price <= Decimal("250"):
                raise ValueError("Retailer price out of plausible range")
            pages = offer.get("pages")
            if type(pages) is not int or pages < 16 or pages > 1200:
                raise ValueError("Pages missing or implausible")
            if offer.get("source_method") != "manually_read_public_product_page":
                raise ValueError("Unverified source method")
            processed.append({
                "title": title.strip(), "consumer_price_eur_including_vat": _euros(price),
                "pages": pages, "retailer": host, "url": uri,
                "observed_on": str(observed),
                "source_method": "manually_read_public_product_page",
                "live_checked_by_this_code": False
            })
        print_plan = niche.get("print_plan")
        if not isinstance(print_plan, dict) or print_plan.get("format") != "large_bw_white":
            raise ValueError("MVP supports only large B&W white paperback print assumptions")
        planned = print_plan.get("pages")
        cost = print_cost_de_bw_large(planned)
        price_levels = print_plan.get("net_list_prices_eur")
        if not isinstance(price_levels, list) or not 1 <= len(price_levels) <= 4:
            raise ValueError("Supply 1..4 illustrative net list prices")
        scenarios = [paperback_royalty_scenario(planned, v) for v in price_levels]
        if len(hosts) < 2:
            errors.append("Only one retailer domain sampled")
        demand = niche.get("demand_evidence", [])
        if not isinstance(demand, list):
            raise ValueError("demand_evidence must be a list")
        for d in demand:
            if d.get("type") != "retailer_rank_proxy" or "url" not in d:
                raise ValueError("Only explicitly weak retailer rank proxies supported")
            _merchant(d["url"])
            rank = d.get("rank")
            if type(rank) is not int or rank < 1:
                raise ValueError("Retailer rank must be positive integer")
            when = date.fromisoformat(d["observed_on"])
            if (today - when).days < 0 or (today - when).days > 90:
                raise ValueError("Demand proxy stale or future dated")
        prices = [float(p["consumer_price_eur_including_vat"]) for p in processed]
        outputs.append({
            "id": ident, "name": name,
            "engineering_readiness": readiness,
            "retailer_observations": processed,
            "retailer_domains_sampled": sorted(hosts),
            "retailer_price_range_gross_eur": [_euros(Decimal(str(min(prices)))), _euros(Decimal(str(max(prices))))],
            "retailer_price_median_gross_eur": _euros(Decimal(str(median(prices)))),
            "demand_proxies": demand,
            "proxies_are_not_sales": True,
            "independently_verified_buyer_demand": False,
            "commercial_decision": "HOLD",
            "engineering_pilot_rank_only": readiness,
            "kdp_print_plan": {"pages": planned, "format": "large_bw_white",
                               "print_cost_eur": _euros(cost), "illustrative_scenarios": scenarios},
            "warnings": errors + ["Retail prices INCLUDE VAT, scenario list prices EXCLUDE VAT; do not compare directly.",
                                  "This software validates entered source fields, not the live retailer webpage.",
                                  "No category-wide sales forecast or proof of profitable demand."]
        })
    outputs.sort(key=lambda row: (-row["engineering_readiness"], row["id"]))
    return {
        "schema_version": 1, "as_of": today.isoformat(),
        "evaluation_type": "manual_retailer_snapshot_and_engineering_priority",
        "sales_estimated": False, "commercial_best_niche_selected": False,
        "all_niches_commercial_status": "HOLD",
        "pilot_priority_is_not_sales_rank": True,
        "kdp_rates_checked_on": "2026-10-23",
        "disclaimer": "Do not claim retailer URLs were fetched automatically; do not infer monthly sales from these prices, ranks or catalog entries.",
        "niches": outputs
    }


def evaluate_market_file(source: Path, destination: Path, today: date | None = None) -> dict:
    if destination.exists():
        raise FileExistsError("Market report already exists, refusing to overwrite")
    raw = json.loads(source.read_text(encoding="utf-8"))
    report = evaluate_market(raw, today=today)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report
