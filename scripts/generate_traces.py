"""
Builds up traces.jsonl with a varied batch of questions -- not just your
easy golden-set questions, but the kind of messy mix a real week of usage
would produce: in-scope, out-of-scope, ambiguous, compound, and typo'd.

Run from the project root:
    python scripts/generate_traces.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tracing import run_traced_query  # noqa: E402

QUESTIONS = [
    # --- your original golden-set questions (in-scope, known answers) ---
    "Does this platform ingest raw vehicle CAN-bus or ECU data as part of its normal operation?",
    "Can the system step in to intervene and help a driver avoid a collision while it's happening?",
    "Is the platform able to drive the vehicle itself or take over vehicle control?",
    "Would a participant be able to get unrestricted, unsupervised access to someone else's raw biometric recordings?",
    "Is lane detection or tracking a feature that is actively working right now in the shipped product?",
    "What devices does Neurora Capture integrate with to record eye-tracking and physiological data during a session?",
    "What can trainers and analysts do inside Neurora Insight with a recorded session?",
    "What kind of access does a participant get through Neurora Selfview, and is it a full raw-data analytics view?",
    "In the end-to-end Neurora workflow, what does a trainer do first, before any device is connected?",
    "Which metric does Neurora use to measure how much time a driver's eyes spend off the road during a session?",
    "What access controls and security measures does the platform require for handling biometric data?",
    "According to the Claims Note, what should a trainer be able to trace an automated finding back to?",
    # --- out-of-corpus (should refuse cleanly) ---
    "What is the refund policy if a customer cancels their Neurora subscription?",
    "Does Neurora offer a mobile app for iOS and Android?",
    "What is the pricing for the enterprise tier of the Neurora platform?",
    "Who is the CEO of the company that makes Neurora?",
    "Does the platform support languages other than English?",
    # --- ambiguous / compound (two questions in one) ---
    "Does the platform support both autonomous driving and medical diagnosis features?",
    "Is the biometric data encrypted, and who exactly is allowed to see it unencrypted?",
    "Can a participant both correct their own AOI tags and see other participants' sessions?",
    # --- typo'd / informal phrasing ---
    "wat divices does neurora capture intergrate with for eye tracking",
    "is lane detction curently enabled in teh product",
    "can this thing drive the car by itself lol",
    # --- meta / about-the-document questions ---
    "What form number and version does this PRD document carry?",
    "How many exclusion codes are listed in the Exclusions Table?",
    # --- near-duplicate rephrasing of an already-tricky question, to check consistency ---
    "Is real-time collision intervention something this platform actually does?",
    "If two participants are in the same session, can one see the other's raw biometric feed without permission?",
]


def main():
    print(f"Firing {len(QUESTIONS)} questions through the traced pipeline...\n")
    for i, q in enumerate(QUESTIONS, start=1):
        record = run_traced_query(q, strategy="naive", top_k=5)
        status = "ERROR" if record["error"] else ("REFUSED" if record["refused"] else "ANSWERED")
        print(f"[{i:2}/{len(QUESTIONS)}] {status:8} {q[:70]}")
    print(f"\nDone. Traces appended to traces.jsonl.")


if __name__ == "__main__":
    main()