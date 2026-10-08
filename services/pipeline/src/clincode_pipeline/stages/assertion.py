import re
from typing import List, Dict, Any

NEGATION_PATTERNS = [
    r"\bdenies\b", r"\bdenied\b", r"\bno\b", r"\bnot\b", r"\bnegative for\b",
    r"\bno evidence of\b", r"\bwithout\b", r"\brules out\b", r"\bruled out\b"
]

FAMILY_PATTERNS = [
    r"\bfamily history of\b", r"\bfather had\b", r"\bmother had\b", r"\bbrother\b", r"\bsister\b", r"\bfh:\b"
]

POSSIBLE_PATTERNS = [
    r"\bpossible\b", r"\brule out\b", r"\br/o\b", r"\bsuspected\b", r"\bprobable\b", r"\bconcern for\b"
]

HISTORICAL_PATTERNS = [
    r"\bhistory of\b", r"\bpast history of\b", r"\bstatus post\b", r"\bs/p\b", r"\bprior\b", r"\bprevious\b"
]

CONDITIONAL_PATTERNS = [
    r"\bif\b", r"\bin the event of\b", r"\bas needed\b", r"\bprn\b"
]


def extract_sentence_context(note_text: str, start_char: int, end_char: int) -> str:
    """Extracts the sentence containing the entity span to prevent cross-sentence leakage."""
    # Find sentence boundaries preceding start_char
    left = max(0, start_char - 80)
    snippet_left = note_text[left:start_char]
    sentence_start_idx = left
    for sent_delim in [".", "\n", ";"]:
        last_delim = snippet_left.rfind(sent_delim)
        if last_delim != -1:
            sentence_start_idx = left + last_delim + 1
            break

    # Find sentence boundaries after end_char
    right = min(len(note_text), end_char + 40)
    snippet_right = note_text[end_char:right]
    sentence_end_idx = right
    for sent_delim in [".", "\n", ";"]:
        first_delim = snippet_right.find(sent_delim)
        if first_delim != -1:
            sentence_end_idx = end_char + first_delim
            break

    return note_text[sentence_start_idx:sentence_end_idx].lower()


def classify_entity_assertions(note_text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Classifies each extracted entity into one of 6 assertion states:
    present, absent (negated), possible, conditional, historical, family.
    Sentence-bounded context extraction prevents cross-sentence assertion leakage.
    """
    asserted_entities = []

    for ent in entities:
        start = ent["start_char"]
        end = ent["end_char"]
        ent_text = ent["text"].lower()

        # Sentence-bounded context window
        context_window = extract_sentence_context(note_text, start, end)

        assertion = "present"

        # 1. Check Family History (family history of)
        for pat in FAMILY_PATTERNS:
            if re.search(pat, context_window):
                assertion = "family"
                break

        # 2. Check Negation
        if assertion == "present":
            for pat in NEGATION_PATTERNS:
                if re.search(pat, context_window):
                    assertion = "absent"
                    break

        # 3. Check Possible / Uncertain
        if assertion == "present":
            for pat in POSSIBLE_PATTERNS:
                if re.search(pat, context_window):
                    assertion = "possible"
                    break

        # 4. Check Historical (only if NOT family and NOT acute)
        if assertion == "present" and "acute" not in ent_text:
            for pat in HISTORICAL_PATTERNS:
                if re.search(pat, context_window):
                    assertion = "historical"
                    break

        # 5. Check Conditional
        if assertion == "present":
            for pat in CONDITIONAL_PATTERNS:
                if re.search(pat, context_window):
                    assertion = "conditional"
                    break

        ent_copy = ent.copy()
        ent_copy["assertion"] = assertion
        asserted_entities.append(ent_copy)

    return asserted_entities
