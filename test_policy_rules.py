"""Plain-Python checks for policy_rules.py - no pytest needed:  python test_policy_rules.py"""
from policy_rules import coverage_in_force, edition_in_force, deductible_and_limits

checks = 0
def check(label, condition):
    global checks
    assert condition, "FAILED: " + label
    checks += 1
    print("ok  ", label)

# policy in force on the loss date (inclusive at both ends)
check("POL-HO-1001 in force on 2024-08-11", coverage_in_force("POL-HO-1001", "2024-08-11")["in_force"] is True)
check("POL-HO-1002 ended 2024-06-30, NOT in force 2024-08-11", coverage_in_force("POL-HO-1002", "2024-08-11")["in_force"] is False)
check("POL-HO-1004 in force ON its last day 2025-02-28", coverage_in_force("POL-HO-1004", "2025-02-28")["in_force"] is True)
check("POL-HO-1004 NOT in force the day after, 2025-03-01", coverage_in_force("POL-HO-1004", "2025-03-01")["in_force"] is False)
check("POL-HO-1003 NOT in force the day before it starts", coverage_in_force("POL-HO-1003", "2025-02-28")["in_force"] is False)
check("POL-HO-1003 in force on its first day", coverage_in_force("POL-HO-1003", "2025-03-01")["in_force"] is True)
r = coverage_in_force("POL-XX-9999", "2024-08-11")
check("unknown policy reports found=False with a recoverable message", r["found"] is False and "look like POL-HO-1001" in r["reason"])
try:
    coverage_in_force("POL-HO-1001", "11/08/2024"); bad = False
except ValueError as e:
    bad = "YYYY-MM-DD" in str(e)
check("bad date format raises a recoverable error naming the format", bad)
try:
    coverage_in_force("POL-HO-1001", "2024-02-30"); bad = False
except ValueError:
    bad = True
check("impossible date (30 Feb) is rejected", bad)

# which wording edition applies - the capstone's headline rule
check("HO3 loss 2024-08-11 -> 2023 edition", edition_in_force("HO3", "2024-08-11")["form_number"] == "HO-0123 ed. 01-23")
check("HO3 loss 2025-02-28 (day BEFORE 2025 edition) -> still 2023 edition", edition_in_force("HO3", "2025-02-28")["form_number"] == "HO-0123 ed. 01-23")
check("HO3 loss 2025-03-01 (day it takes effect) -> 2025 edition", edition_in_force("HO3", "2025-03-01")["form_number"] == "HO-0125 ed. 03-25")
check("HO3 loss 2026-01-15 -> 2025 edition", edition_in_force("HO3", "2026-01-15")["form_number"] == "HO-0125 ed. 03-25")
check("HO3 loss 2022-12-31 -> no wording in force yet", edition_in_force("HO3", "2022-12-31") is None)
check("MO1 loss 2024-08-11 -> motor 2023 edition", edition_in_force("MO1", "2024-08-11")["form_number"] == "MO-0223 ed. 01-23")
check("unknown product -> None", edition_in_force("ZZ9", "2024-08-11") is None)

# deductible, sub-limit and policy limit stay three separate numbers
d = deductible_and_limits("HO3")
check("HO3 deductible 500, water-damage sub-limit 15000, policy limit 250000 - three distinct values",
      (d["deductible"], d["sub_limits"]["water_damage"], d["policy_limit"]) == (500, 15000, 250000))
check("unknown product has no limits", deductible_and_limits("ZZ9") is None)
print(f"\nall {checks} checks passed")
