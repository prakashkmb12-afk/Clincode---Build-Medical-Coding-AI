import re
from typing import List, Dict, Any, Tuple

# Canonical clinical section headers with regex matching variations
CANONICAL_SECTIONS = [
    ("CHIEF COMPLAINT", r"\b(?:CHIEF COMPLAINT|CC):?"),
    ("HISTORY OF PRESENT ILLNESS", r"\b(?:HISTORY OF PRESENT ILLNESS|HPI):?"),
    ("PAST MEDICAL HISTORY", r"\b(?:PAST MEDICAL HISTORY|PMH|PAST HISTORY):?"),
    ("MEDICATIONS", r"\b(?:MEDICATIONS|CURRENT MEDICATIONS|MEDS):?"),
    ("ALLERGIES", r"\b(?:ALLERGIES|ALLERGIC REACTIONS):?"),
    ("PHYSICAL EXAMINATION", r"\b(?:PHYSICAL EXAMINATION|PHYSICAL EXAM|PE):?"),
    ("LABORATORY DATA", r"\b(?:LABORATORY DATA|LABS|LAB RESULTS):?"),
    ("RADIOLOGY", r"\b(?:RADIOLOGY|IMAGING|X-RAY|CT SCAN|MRI):?"),
    ("ASSESSMENT AND PLAN", r"\b(?:ASSESSMENT AND PLAN|ASSESSMENT & PLAN|IMPRESSION|PLAN|A&P):?"),
    ("DISCHARGE DIAGNOSES", r"\b(?:DISCHARGE DIAGNOSES|FINAL DIAGNOSES|DIAGNOSES):?"),
]


def sectionize_note(note_text: str) -> List[Dict[str, Any]]:
    """
    Splits a clinical note into canonical sections with exact character span preservation.
    Returns a list of dicts:
    [
      {
        "section_name": "HISTORY OF PRESENT ILLNESS",
        "start_char": 42,
        "end_char": 285,
        "text": "..."
      }
    ]
    Invariant: note_text[start_char:end_char] == text for every section.
    """
    matches: List[Tuple[int, int, str]] = []

    # Find all header matches across the text
    for canonical_name, pattern in CANONICAL_SECTIONS:
        for m in re.finditer(pattern, note_text, flags=re.IGNORECASE):
            matches.append((m.start(), m.end(), canonical_name))

    # Sort matches by start position in text
    matches.sort(key=lambda x: x[0])

    # If no headers detected, classify entire text as UNKNOWN
    if not matches:
        return [{
            "section_name": "UNKNOWN",
            "start_char": 0,
            "end_char": len(note_text),
            "text": note_text
        }]

    sections: List[Dict[str, Any]] = []

    # Handle preamble before the first header if present
    first_start = matches[0][0]
    if first_start > 0:
        preamble_text = note_text[0:first_start]
        if preamble_text.strip():
            sections.append({
                "section_name": "PREAMBLE",
                "start_char": 0,
                "end_char": first_start,
                "text": preamble_text
            })

    # Slice note into section segments between consecutive header starts
    for idx, (start, end, name) in enumerate(matches):
        next_start = matches[idx + 1][0] if idx + 1 < len(matches) else len(note_text)
        
        # Ensure we don't create zero-length sections
        sec_start = start
        sec_end = max(next_start, sec_start + 1) if idx + 1 < len(matches) else len(note_text)
        sec_text = note_text[sec_start:sec_end]

        sections.append({
            "section_name": name,
            "start_char": sec_start,
            "end_char": sec_end,
            "text": sec_text
        })

    return sections


def get_section_for_offset(sections: List[Dict[str, Any]], char_offset: int) -> str:
    """Returns the section name covering a given character offset in the note."""
    for sec in sections:
        if sec["start_char"] <= char_offset < sec["end_char"]:
            return sec["section_name"]
    return "UNKNOWN"
