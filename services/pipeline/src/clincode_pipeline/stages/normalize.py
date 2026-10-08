from typing import List, Dict, Any

CLINICAL_ABBREVIATIONS = {
    "htn": "hypertension",
    "t2dm": "type 2 diabetes mellitus",
    "dm": "diabetes mellitus",
    "chf": "congestive heart failure",
    "sob": "shortness of breath",
    "cva": "cerebrovascular accident",
    "cad": "coronary artery disease",
}


def normalize_and_filter_entities(
    entities: List[Dict[str, Any]],
    allow_historical: bool = True
) -> List[Dict[str, Any]]:
    """
    FR-7 & FR-8: Normalizes clinical abbreviations and UMLS concepts.
    FILTERS entities: Only present (and optionally historical) conditions proceed to ICD-10 retrieval.
    Entities with assertion 'absent' (negated) or 'family' are strictly excluded.
    """
    eligible = []

    for ent in entities:
        assertion = ent.get("assertion", "present")

        # FR-8 Critical Rule: Negated (absent) and family history entities MUST NOT be coded
        if assertion == "absent" or assertion == "family" or assertion == "conditional":
            continue
        
        if assertion == "historical" and not allow_historical:
            continue

        text_lower = ent["text"].lower().strip()
        normalized_text = CLINICAL_ABBREVIATIONS.get(text_lower, ent["text"])

        ent_copy = ent.copy()
        ent_copy["normalized_text"] = normalized_text
        eligible.append(ent_copy)

    return eligible
