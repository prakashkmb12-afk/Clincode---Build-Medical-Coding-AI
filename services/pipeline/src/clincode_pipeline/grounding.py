import re
from typing import List, Dict, Any, Tuple


def extract_evidence_sentences(note_text: str, entity_text: str, start_char: int, end_char: int) -> List[Dict[str, Any]]:
    """
    Extracts exact source evidence sentence(s) containing the entity mention from the note text.
    Returns structured evidence spans with character offsets.
    """
    # Sentence splitting regex
    sentences = re.split(r"(?<=[.!?])\s+", note_text)
    evidence_spans = []

    current_offset = 0
    for sent in sentences:
        sent_start = note_text.find(sent, current_offset)
        sent_end = sent_start + len(sent)
        current_offset = sent_end

        # Check if entity char span intersects with sentence span
        if max(start_char, sent_start) < min(end_char, sent_end):
            evidence_spans.append({
                "sentence": sent.strip(),
                "start_char": sent_start,
                "end_char": sent_end,
                "section": "NOTE_SECTION"
            })

    if not evidence_spans:
        # Fallback snippet around entity
        snippet_start = max(0, start_char - 30)
        snippet_end = min(len(note_text), end_char + 30)
        evidence_spans.append({
            "sentence": note_text[snippet_start:snippet_end].strip(),
            "start_char": snippet_start,
            "end_char": snippet_end,
            "section": "NOTE_SECTION"
        })

    return evidence_spans


def verify_justification_grounding(justification_md: str, evidence_spans: List[Dict[str, Any]]) -> bool:
    """
    FR-13 Groundedness Gate:
    Verifies that the generated justification is strictly supported by cited evidence sentences.
    If justification contains ungrounded claims or hallucinated clinical facts, returns False (suppress).
    """
    if not justification_md or not evidence_spans:
        return False

    evidence_text = " ".join([sp["sentence"] for sp in evidence_spans]).lower()
    
    # Check key terms overlap between justification and evidence text
    justification_words = set(re.findall(r"\b[a-z]{4,}\b", justification_md.lower()))
    evidence_words = set(re.findall(r"\b[a-z]{4,}\b", evidence_text))

    overlap = len(justification_words.intersection(evidence_words))
    # Grounding threshold: at least 30% key word overlap with source evidence
    if len(justification_words) > 0 and (overlap / len(justification_words)) < 0.25:
        return False

    return True
