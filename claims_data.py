"""
Week 7 - a tiny made-up claims desk for the race. ALL DATA HERE IS INVENTED.

CLAIMS      : the "database" the get_claim tool reads
EXCLUSIONS  : the "policy wording" the search_policy tool reads
RACE        : the 10 claims we race on, with the correct answer for each
"""

EXCLUSIONS = [
    {"id": "EXC-01", "title": "Flood",
     "wording": "Loss caused by flood, rising water or an overflowing river or stream is not covered.",
     "keywords": ["flood", "river", "overflow", "rising water", "stream"]},
    {"id": "EXC-02", "title": "Wear and tear",
     "wording": "Loss caused by wear and tear, gradual deterioration or old, worn-out materials is not covered.",
     "keywords": ["wear", "worn", "gradual", "deteriorat", "ageing", "aging"]},
    {"id": "EXC-03", "title": "Intentional damage",
     "wording": "Loss caused deliberately by the policyholder is not covered.",
     "keywords": ["intentional", "deliberate", "arson"]},
    {"id": "EXC-04", "title": "Vacant property",
     "wording": "Loss at a property left vacant or unoccupied for more than 60 days is not covered.",
     "keywords": ["vacant", "vacancy", "unoccupied", "uninhabited"]},
    {"id": "EXC-05", "title": "Business use",
     "wording": "Loss of business stock, or loss arising from business activity at the property, is not covered.",
     "keywords": ["business", "commercial", "shop"]},
]

CLAIMS = {
    "CLM-2026-00001": {"claim_id": "CLM-2026-00001", "status": "OPEN", "date_of_loss": "2026-03-02",
        "loss_amount": 4200.0, "excess": 500.0,
        "notes": "Kitchen pipe burst overnight while the owners slept. Plumber confirmed a failed joint on a two-year-old fitting. Water damaged cabinets and flooring."},
    "CLM-2026-00002": {"claim_id": "CLM-2026-00002", "status": "OPEN", "date_of_loss": "2026-03-09",
        "loss_amount": 3000.0, "excess": 250.0,
        "notes": "Burglary while the family was at work. Rear window forced. Laptop, tablet and jewellery taken. Police report filed and crime reference on file."},
    "CLM-2026-00003": {"claim_id": "CLM-2026-00003", "status": "OPEN", "date_of_loss": "2026-04-14",
        "loss_amount": 12000.0, "excess": 1000.0,
        "notes": "Kitchen fire started by an overheated pan. Fire brigade attended. Smoke damage to kitchen and hallway. Occupants were at home and unhurt."},
    "CLM-2026-00004": {"claim_id": "CLM-2026-00004", "status": "OPEN", "date_of_loss": "2026-05-20",
        "loss_amount": 8500.0, "excess": 500.0,
        "notes": "The river overflowed after three days of rain. The ground floor was flooded to 30 cm. Carpets, sofa and kitchen units are ruined."},
    "CLM-2026-00005": {"claim_id": "CLM-2026-00005", "status": "OPEN", "date_of_loss": "2026-06-01",
        "loss_amount": 2600.0, "excess": 500.0,
        "notes": "Ceiling stains in the back bedroom have been spreading for several years. The roofer reports the tiles are old and worn out and have let water in gradually."},
    "CLM-2026-00006": {"claim_id": "CLM-2026-00006", "status": "OPEN", "date_of_loss": "2026-06-11",
        "loss_amount": 5400.0, "excess": 500.0,
        "notes": "An upstairs bathroom pipe burst and water came through the lounge ceiling. The owner confirms the house has been unoccupied since March while they lived abroad."},
    "CLM-2026-00007": {"claim_id": "CLM-2026-00007", "status": "OPEN", "date_of_loss": "2026-07-03",
        "loss_amount": 1800.0, "excess": 500.0,
        "notes": "Water found in the basement after heavy rain. Cause not yet determined. Drain survey booked for next week."},
    "CLM-2026-00008": {"claim_id": "CLM-2026-00008", "status": "OPEN", "date_of_loss": "2026-07-19",
        "loss_amount": 900.0, "excess": 250.0,
        "notes": ""},
    # CLM-2026-00009 is deliberately NOT here: the claim does not exist in the system.
    "CLM-2026-00010": {"claim_id": "CLM-2026-00010", "status": "OPEN", "date_of_loss": "2026-08-08",
        "loss_amount": 6200.0, "excess": 500.0,
        "notes": "Fire in the spare room. The owner runs an online shop from the property and the business stock stored there was destroyed."},
}

# (claim_id, kind, correct decision, correct exclusion id)
# kind: "clean"              = ordinary claim, same path every time
#       "exclusion-in-notes" = what step 2 (notes) finds decides what step 3 (policy lookup) must do
#       "missing-or-unclear" = no claim, no notes, or cause not known
RACE = [
    ("CLM-2026-00001", "clean",              "COVERED",    None),
    ("CLM-2026-00002", "clean",              "COVERED",    None),
    ("CLM-2026-00003", "clean",              "COVERED",    None),
    ("CLM-2026-00004", "exclusion-in-notes", "EXCLUDED",   "EXC-01"),
    ("CLM-2026-00005", "exclusion-in-notes", "EXCLUDED",   "EXC-02"),
    ("CLM-2026-00006", "exclusion-in-notes", "EXCLUDED",   "EXC-04"),
    ("CLM-2026-00007", "missing-or-unclear", "NEEDS_INFO", None),
    ("CLM-2026-00008", "missing-or-unclear", "NEEDS_INFO", None),
    ("CLM-2026-00009", "missing-or-unclear", "NEEDS_INFO", None),
    ("CLM-2026-00010", "exclusion-in-notes", "EXCLUDED",   "EXC-05"),
]


def expected_payable(claim_id, decision):
    if decision != "COVERED":
        return 0.0
    claim = CLAIMS[claim_id]
    return round(max(0.0, claim["loss_amount"] - claim["excess"]), 2)


def grade(answer, claim_id):
    """True only if decision, exclusion id AND payable amount are all correct."""
    if answer is None:
        return False
    for cid, kind, decision, exclusion in RACE:
        if cid == claim_id:
            return (answer["decision"] == decision
                    and answer["exclusion_id"] == exclusion
                    and abs(answer["payable_amount"] - expected_payable(cid, decision)) < 0.01)
    return False
