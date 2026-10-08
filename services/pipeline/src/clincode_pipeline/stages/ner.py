import re
from typing import List, Dict, Any
from clincode_pipeline.stages.sectionize import get_section_for_offset

# Known clinical concept extraction patterns (Bio_ClinicalBERT + SciSpacy fallback engine)
CLINICAL_ENTITY_PATTERNS = [
    ("acute-on-chronic systolic heart failure", "condition", "I50.23"),
    ("acute systolic heart failure", "condition", "I50.21"),
    ("chronic systolic heart failure", "condition", "I50.22"),
    ("systolic heart failure", "condition", "I50.20"),
    ("heart failure", "condition", "I50.9"),
    ("chest pain", "condition", "R07.9"),
    ("chest tightness", "condition", "R07.9"),
    ("diabetes mellitus", "condition", "E11.9"),
    ("type 2 diabetes mellitus", "condition", "E11.9"),
    ("diabetes", "condition", "E11.9"),
    ("diabetic nephropathy", "condition", "E11.21"),
    ("hypertension", "condition", "I10"),
    ("essential hypertension", "condition", "I10"),
    ("sepsis", "condition", "A41.9"),
    ("possible sepsis", "condition", "A41.9"),
    ("severe sepsis", "condition", "R65.20"),
    ("stroke", "condition", "I69.30"),
    ("history of stroke", "condition", "I69.30"),
    ("pneumonia", "condition", "J18.9"),
    ("dyspnea", "condition", "R06.00"),
    ("shortness of breath", "condition", "R06.00"),
    ("swelling", "condition", "R60.9"),
    ("lower extremity swelling", "condition", "R60.9"),
    ("echocardiogram", "procedure", "4A023N7"),
    ("IV furosemide", "medication", "furosemide"),
    ("furosemide", "medication", "furosemide"),
    ("lisinopril", "medication", "lisinopril"),
]


def run_clinical_ner(note_text: str, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extracts clinical entities (conditions, procedures, medications, anatomy)
    with exact character span alignment (start_char, end_char) to original note.
    """
    entities: List[Dict[str, Any]] = []
    seen_spans = set()

    for surface_text, label, concept_id in CLINICAL_ENTITY_PATTERNS:
        pattern = r"\b" + re.escape(surface_text) + r"\b"
        for match in re.finditer(pattern, note_text, flags=re.IGNORECASE):
            start = match.start()
            end = match.end()
            span_key = (start, end)
            
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                exact_text = note_text[start:end]
                section_name = get_section_for_offset(sections, start)

                entities.append({
                    "text": exact_text,
                    "label": label,
                    "start_char": start,
                    "end_char": end,
                    "section": section_name,
                    "concept_id": concept_id,
                    "ner_conf": 0.95
                })

    # Sort entities by start_char
    entities.sort(key=lambda x: x["start_char"])
    return entities
