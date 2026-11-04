"""Plain-Python checks for triage_tools.py - no models, no network:  python test_triage_tools.py"""
from triage_tools import TriageSession, decision_language, LOCAL_TOOL_SPECS

checks = 0
def check(label, condition):
    global checks
    assert condition, "FAILED: " + label
    checks += 1
    print("ok  ", label)

def chunk(cid, form, edition, line="HO3", clause="Exclusions Table - EXC-01"):
    return {"chunk_id": cid, "form_number": form, "edition_date": edition, "policy_line": line,
            "clause": clause, "text": f"{form} flood clause text"}

OLD = chunk("HO3-2023.txt:structured:2", "HO-0123 ed. 01-23", "2023-01-01")
NEW = chunk("HO3-2025.txt:structured:2", "HO-0125 ed. 03-25", "2025-03-01")
GOOD = dict(policy_number="POL-HO-1001", loss_date="2024-08-11", cited_chunk_ids=[OLD["chunk_id"]],
            facts_summary="Surface water entered the ground floor after heavy rain on 2024-08-11.",
            referral_reason="Flood clause wording needs adjuster interpretation.", sub_limit_key="water_damage")

def fresh(check_first=True, retrieved=(OLD, NEW)):
    s = TriageSession()
    s.record_wording_results(list(retrieved))
    if check_first:
        s.call("check_coverage_in_force", {"policy_number": "POL-HO-1001", "loss_date": "2024-08-11"})
    return s

# decision-language detector
for phrase in ["this claim is covered", "Not covered under the policy", "claim approved", "we will pay", "request denied", "the loss is excluded"]:
    check(f"detects decision language: '{phrase}'", len(decision_language(phrase)) > 0)
for phrase in ["Coverage-in-force check ran for the policy", "The flood clause lists surface water run-off", "EXC-01 may be relevant"]:
    check(f"allows factual text: '{phrase}'", decision_language(phrase) == [])

# lookup and in-force tools return errors, never raise
check("lookup finds a policy", fresh().call("lookup_policy", {"policy_number": "POL-HO-1001"})["product"] == "HO3")
check("lookup of an unknown policy is a recoverable error", "look like POL-HO-1001" in fresh().call("lookup_policy", {"policy_number": "X"})["error"])
check("in-force check with a bad date is a recoverable error", "YYYY-MM-DD" in fresh().call("check_coverage_in_force", {"policy_number": "POL-HO-1001", "loss_date": "11/08/2024"})["error"])
check("unknown tool is an error, not a crash", "unknown tool" in fresh().call("delete_everything", {})["error"])
check("wrong argument names are an error, not a crash", "bad arguments" in fresh().call("lookup_policy", {"policy": "x"})["error"])

# refer_to_adjuster: the happy path
r = fresh().call("refer_to_adjuster", GOOD)
check("referral succeeds with a correct-edition citation", r.get("action") == "REFER_TO_ADJUSTER")
check("citation names the endorsement version and clause", r["citations"][0]["form_number"] == "HO-0123 ed. 01-23" and "EXC-01" in r["citations"][0]["clause"])
check("referral records the loss date it was resolved against", r["loss_date"] == "2024-08-11" and r["wording_resolved_against"]["edition_date"] == "2023-01-01")
check("deductible, sub-limit and policy limit are three separate attached numbers",
      (r["deductible"], r["sub_limit"]["amount"], r["policy_limit"]) == (500, 15000, 250000) and r["sub_limit"]["name"] == "water_damage")
check("the record says the policy was in force", r["policy_in_force"] is True)

# refer_to_adjuster: every rule enforced in code
check("refusal: in-force check not run first", "before referring" in fresh(check_first=False).call("refer_to_adjuster", GOOD)["error"])
bad = dict(GOOD, cited_chunk_ids=[NEW["chunk_id"]])
e = fresh().call("refer_to_adjuster", bad)["error"]
check("refusal: citing the 2025 wording for a 2024 loss, naming both editions", "HO-0125" in e and "HO-0123" in e)
check("refusal: citing a chunk id that was never retrieved", "never retrieved" in fresh().call("refer_to_adjuster", dict(GOOD, cited_chunk_ids=["made-up-id"]))["error"])
e = fresh().call("refer_to_adjuster", dict(GOOD, facts_summary="The water damage is covered."))["error"]
check("refusal: the word 'covered' in the summary", "must not state a coverage decision" in e)
check("refusal: decision language in the referral reason", "coverage decision" in fresh().call("refer_to_adjuster", dict(GOOD, referral_reason="Claim approved for payout"))["error"])
check("refusal: invalid sub-limit key lists the valid ones", "jewellery" in fresh().call("refer_to_adjuster", dict(GOOD, sub_limit_key="swimming_pool"))["error"])
check("referral works with no sub-limit", fresh().call("refer_to_adjuster", {k: v for k, v in GOOD.items() if k != "sub_limit_key"})["sub_limit"] is None)

# a 2025 loss must cite the 2025 wording, and the 2023 wording is now the wrong one
s = TriageSession(); s.record_wording_results([OLD, NEW])
s.call("check_coverage_in_force", {"policy_number": "POL-HO-1003", "loss_date": "2025-06-01"})
ok = s.call("refer_to_adjuster", dict(GOOD, policy_number="POL-HO-1003", loss_date="2025-06-01", cited_chunk_ids=[NEW["chunk_id"]]))
check("2025 loss citing the 2025 wording succeeds", ok.get("action") == "REFER_TO_ADJUSTER")
bad = s.call("refer_to_adjuster", dict(GOOD, policy_number="POL-HO-1003", loss_date="2025-06-01", cited_chunk_ids=[OLD["chunk_id"]]))
check("2025 loss citing the superseded 2023 wording is refused", "HO-0123" in bad["error"])

# a policy that was NOT in force still produces a referral, flagged, never a decision
s = TriageSession(); s.record_wording_results([OLD])
s.call("check_coverage_in_force", {"policy_number": "POL-HO-1002", "loss_date": "2024-08-11"})
lapsed = s.call("refer_to_adjuster", dict(GOOD, policy_number="POL-HO-1002", cited_chunk_ids=[], sub_limit_key=None,
                                          facts_summary="Loss date is after the policy period ended.", referral_reason="Policy not in force on the loss date; adjuster to confirm."))
check("lapsed policy: referral flags policy_in_force False", lapsed["policy_in_force"] is False)

# tool declarations
names = [t["name"] for t in LOCAL_TOOL_SPECS]
check("three local tools declared", names == ["lookup_policy", "check_coverage_in_force", "refer_to_adjuster"])
print(f"\nall {checks} checks passed")
