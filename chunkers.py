"""
Two beginner-level chunking strategies for the endorsement .txt files.

Every chunk this file produces is a plain dict with these keys, which is
exactly the metadata the assignment asks for:
    - text          the chunk text that gets embedded
    - source_file   e.g. "HO-0304.txt"
    - form_number   e.g. "HO-0304 ed. 03-24"
    - policy_line   e.g. "HO3"
    - edition_date  e.g. "2024-03-01"
    - clause        which section the chunk came from (structure-aware only)
    - strategy      "naive" or "structured"

A chunk with a missing source_file/form_number is treated as a failed
ingest, so both chunkers always fill those fields on every chunk.
"""

import re
from pathlib import Path


def parse_header(text: str) -> dict:
    """
    Every endorsement .txt starts with a small header block like:

        FORM_NUMBER: HO-0304 ed. 03-24
        POLICY_LINE: HO3
        EFFECTIVE_DATE: 2024-03-01
        TITLE: Water Damage and Plumbing Systems Endorsement

    This pulls those four fields out with a simple regex per line.
    """
    fields = {"form_number": None, "policy_line": None, "edition_date": None, "title": None}
    patterns = {
        "form_number": r"FORM_NUMBER:\s*(.+)",
        "policy_line": r"POLICY_LINE:\s*(.+)",
        "edition_date": r"EFFECTIVE_DATE:\s*(.+)",
        "title": r"TITLE:\s*(.+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            fields[key] = match.group(1).strip()
    return fields


# ---------------------------------------------------------------------------
# Strategy 1: naive fixed-size chunking
# ---------------------------------------------------------------------------
def naive_chunk(text: str, source_file: str, chunk_size: int = 600, overlap: int = 80) -> list[dict]:
    """
    Splits the whole document into fixed-size character windows with a
    small overlap. This is what most people's "week 3" chunker looks like.
    It has NO idea where a table row starts or ends, so it can (and will)
    slice an exclusion row away from its table header and form number.
    """
    header = parse_header(text)
    chunks = []
    start = 0
    n = len(text)
    idx = 0
    while start < n:
        end = min(start + chunk_size, n)
        piece = text[start:end].strip()
        if piece:
            chunks.append({
                "text": piece,
                "source_file": source_file,
                "form_number": header["form_number"],
                "policy_line": header["policy_line"],
                "edition_date": header["edition_date"],
                "clause": None,  # naive chunker doesn't track clause boundaries
                "strategy": "naive",
                "chunk_id": f"{source_file}:naive:{idx}",
            })
            idx += 1
        start = end - overlap  # step forward, keep a little overlap
        if end == n:
            break
    return chunks


# ---------------------------------------------------------------------------
# Strategy 2: structure-aware chunking
# ---------------------------------------------------------------------------
def structure_chunk(text: str, source_file: str) -> list[dict]:
    """
    Splits on the "## Heading" sections in each document. The Exclusions
    Table section gets special handling: it is split ONE ROW AT A TIME, but
    every row chunk has the table header + form_number + policy_line
    prepended to its text, so a retrieved row is never orphaned from the
    context that says which endorsement it belongs to.
    """
    header = parse_header(text)
    form_number = header["form_number"]
    policy_line = header["policy_line"]
    edition_date = header["edition_date"]

    # Split the body into "## Section Name" blocks.
    sections = re.split(r"(?m)^##\s+", text)[1:]  # [0] is the header block before the first ## heading
    chunks = []
    idx = 0

    for section in sections:
        section = section.strip()
        if not section:
            continue
        # First line of the split piece is the section title.
        lines = section.split("\n")
        clause_name = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        if not body:
            continue

        if "Exclusions Table" in clause_name:
            # Split the markdown table into individual rows.
            table_lines = [ln for ln in body.split("\n") if ln.strip().startswith("|")]
            if len(table_lines) >= 2:
                table_header = table_lines[0]  # column names, e.g. "| Code | Description | ..."
                separator = table_lines[1] if "---" in table_lines[1] else None
                row_lines = table_lines[2:] if separator else table_lines[1:]
                for row in row_lines:
                    prefixed_text = (
                        f"Form {form_number} ({policy_line}) - {clause_name}\n"
                        f"{table_header}\n{row}"
                    )
                    # pull the exclusion code out of the row for a nicer clause label
                    code_match = re.match(r"\|\s*([A-Za-z0-9\-]+)\s*\|", row)
                    row_code = code_match.group(1) if code_match else "row"
                    chunks.append({
                        "text": prefixed_text,
                        "source_file": source_file,
                        "form_number": form_number,
                        "policy_line": policy_line,
                        "edition_date": edition_date,
                        "clause": f"Exclusions Table - {row_code}",
                        "strategy": "structured",
                        "chunk_id": f"{source_file}:structured:{idx}",
                    })
                    idx += 1
                continue  # don't also add the whole table as one blob

        # Non-table section: one chunk per section, form_number always included.
        prefixed_text = f"Form {form_number} ({policy_line}) - {clause_name}\n{body}"
        chunks.append({
            "text": prefixed_text,
            "source_file": source_file,
            "form_number": form_number,
            "policy_line": policy_line,
            "edition_date": edition_date,
            "clause": clause_name,
            "strategy": "structured",
            "chunk_id": f"{source_file}:structured:{idx}",
        })
        idx += 1

    return chunks


def load_and_chunk_all(data_dir: str = "data/endorsements") -> tuple[list[dict], list[dict]]:
    """Reads every .txt file in data_dir and returns (naive_chunks, structured_chunks)."""
    naive_all, structured_all = [], []
    for path in sorted(Path(data_dir).glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        naive_all.extend(naive_chunk(text, source_file=path.name))
        structured_all.extend(structure_chunk(text, source_file=path.name))
    return naive_all, structured_all


if __name__ == "__main__":
    naive, structured = load_and_chunk_all()
    print(f"naive chunks:      {len(naive)}")
    print(f"structured chunks: {len(structured)}")
    print("\nExample naive chunk:\n", naive[0]["text"][:200])
    print("\nExample structured chunk:\n", structured[0]["text"][:200])