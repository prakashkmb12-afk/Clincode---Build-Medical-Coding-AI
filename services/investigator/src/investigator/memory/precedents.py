from typing import List, Dict, Any

PRECEDENT_CHARTS_STORE = [
    {
        "precedent_ref": "PRECEDENT-CHART-089",
        "deid_representation": "acute-on-chronic systolic heart failure dyspnea furosemide",
        "approved_codes": ["I50.23", "I10"],
        "rejected_codes": ["I50.9"],
        "outcome_summary": "Approved by senior coder Meena. Acute-on-chronic systolic heart failure sequenced as principal diagnosis I50.23."
    },
    {
        "precedent_ref": "PRECEDENT-CHART-142",
        "deid_representation": "type 2 diabetes mellitus diabetic nephropathy T2DM",
        "approved_codes": ["E11.21", "I10"],
        "rejected_codes": ["E11.9"],
        "outcome_summary": "Approved by senior coder. Specificity agent upgraded E11.9 to E11.21 based on nephropathy documentation."
    }
]


def search_precedent_memory(deid_text_snippet: str) -> List[Dict[str, Any]]:
    """
    FR-23 Precedent Memory Tool:
    Retrieves top-k similar approved past chart codings and rejected suggestions.
    """
    text_lower = deid_text_snippet.lower()
    matches = []

    for item in PRECEDENT_CHARTS_STORE:
        score = 0.85 if any(kw in text_lower for kw in item["deid_representation"].split()) else 0.50
        matches.append({
            "similar_chart_ref": item["precedent_ref"],
            "similarity_score": score,
            "approved_codes": item["approved_codes"],
            "rejected_codes": item["rejected_codes"],
            "outcome_summary": item["outcome_summary"]
        })

    matches.sort(key=lambda x: x["similarity_score"], reverse=True)
    return matches[:2]
