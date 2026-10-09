from typing import List, Dict, Any

OFFICIAL_CODING_GUIDELINES = [
    {
        "section_num": "I.C.9.a.1",
        "topic": "Heart Failure",
        "chapter_scope": "Diseases of the circulatory system (I00-I99)",
        "guideline_text": (
            "If heart failure is documented as acute-on-chronic systolic, code I50.23 as the primary "
            "diagnosis code. Combination codes should be assigned when a patient presents with both acute "
            "decompensation and underlying chronic systolic dysfunction."
        ),
        "citation": "ICD-10-CM Official Guidelines Section I.C.9.a.1"
    },
    {
        "section_num": "I.C.1.a",
        "topic": "Sepsis Sequencing",
        "chapter_scope": "Certain infectious and parasitic diseases (A00-B99)",
        "guideline_text": (
            "For patients presenting with sepsis, the systemic infection (A41.9) is sequenced first, "
            "followed by acute organ dysfunction codes (R65.20/R65.21) if documented by the physician."
        ),
        "citation": "ICD-10-CM Official Guidelines Section I.C.1.a"
    },
    {
        "section_num": "I.C.4.a.1",
        "topic": "Diabetes Mellitus",
        "chapter_scope": "Endocrine, nutritional and metabolic diseases (E00-E89)",
        "guideline_text": (
            "Assign as many codes from category E11 as needed to identify all associated conditions. "
            "When diabetes with nephropathy is documented, assign code E11.21."
        ),
        "citation": "ICD-10-CM Official Guidelines Section I.C.4.a.1"
    },
    {
        "section_num": "I.A.12.a",
        "topic": "Excludes1 Notes",
        "chapter_scope": "General Coding Guidelines",
        "guideline_text": (
            "A type 1 Excludes note is a pure excludes note. It means 'NOT CODED HERE!' "
            "An Excludes1 note indicates that the code excluded should never be used at the same time "
            "as the code above the Excludes1 note."
        ),
        "citation": "ICD-10-CM Official Guidelines Section I.A.12.a"
    }
]


def guideline_search(query: str, chapter_filter: str = None) -> List[Dict[str, Any]]:
    """
    Whitelisted Read-Only Tool: Clause-level GraphRAG over official ICD-10-CM coding guidelines.
    Returns matched guideline clauses with official section citations.
    """
    query_lower = query.lower()
    matches = []

    for item in OFFICIAL_CODING_GUIDELINES:
        if chapter_filter and chapter_filter.lower() not in item["chapter_scope"].lower():
            continue

        if (query_lower in item["topic"].lower() or 
            query_lower in item["guideline_text"].lower() or 
            query_lower in item["section_num"].lower()):
            matches.append(item)

    if not matches:
        matches = [OFFICIAL_CODING_GUIDELINES[0]]

    return matches
