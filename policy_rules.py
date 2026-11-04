"""
Week 12 - the deterministic policy rules. No model, no network, no embeddings: plain Python
that the agent's tools call and that the eval suite can assert against directly.

  coverage_in_force(policy_number, loss_date)  -> was the POLICY in force on the loss date?
  edition_in_force(product, loss_date)         -> which WORDING EDITION applied on the loss date?
  deductible_and_limits(product)               -> deductible, sub-limits, policy limit (three separate numbers)

Dates are inclusive at both ends: a policy ending 2025-02-28 is in force ON 2025-02-28.
An edition effective 2025-03-01 applies FROM 2025-03-01; the day before, the old edition applies.
Wording in this file never says "covered": it reports facts, an adjuster decides.
"""
import json
import re
from datetime import date
from functools import lru_cache
from pathlib import Path

from chunkers import parse_header

ROOT = Path(__file__).resolve().parent
TABLE_PATH = ROOT / "policy_table.json"
WORDING_DIR = ROOT / "data" / "policy_wordings"


def parse_date(value) -> date:
    text = str(value).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise ValueError(f"loss date '{value}' is not valid: use YYYY-MM-DD, for example 2024-08-11")
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise ValueError(f"loss date '{value}' is not a real calendar date: use YYYY-MM-DD, for example 2024-08-11")


@lru_cache(maxsize=1)
def _table() -> dict:
    return json.loads(TABLE_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _editions() -> list[dict]:
    editions = []
    for path in sorted(WORDING_DIR.glob("*.txt")):
        h = parse_header(path.read_text(encoding="utf-8"))
        editions.append({"product": h["policy_line"], "form_number": h["form_number"],
                         "edition_date": h["edition_date"], "source_file": path.name,
                         "edition_int": int(h["edition_date"].replace("-", ""))})
    return editions


def coverage_in_force(policy_number: str, loss_date: str) -> dict:
    d = parse_date(loss_date)
    number = str(policy_number).strip()
    policy = _table()["policies"].get(number)
    if policy is None:
        return {"policy_number": number, "found": False, "in_force": False,
                "reason": f"policy {number} not found: policy numbers look like POL-HO-1001"}
    start, end = date.fromisoformat(policy["in_force_from"]), date.fromisoformat(policy["in_force_to"])
    if d < start:
        reason = f"loss date {loss_date} is before the policy started on {start}"
    elif d > end:
        reason = f"loss date {loss_date} is after the policy ended on {end}"
    else:
        reason = "policy was in force on the loss date"
    return {"policy_number": number, "found": True, "product": policy["product"],
            "loss_date": loss_date, "in_force_from": str(start), "in_force_to": str(end),
            "in_force": start <= d <= end, "reason": reason}


def edition_in_force(product: str, loss_date: str):
    """The wording edition with the latest effective date that is on or before the loss date, or None."""
    d = parse_date(loss_date)
    candidates = [e for e in _editions() if e["product"] == product and date.fromisoformat(e["edition_date"]) <= d]
    return max(candidates, key=lambda e: e["edition_int"]) if candidates else None


def deductible_and_limits(product: str):
    p = _table()["products"].get(product)
    if p is None:
        return None
    return {"product": product, "deductible": p["deductible"],
            "sub_limits": dict(p["sub_limits"]), "policy_limit": p["policy_limit"]}
