import re
from typing import List, Dict, Any, Tuple
from clincode_pipeline.grounding import extract_evidence_sentences, verify_justification_grounding


def generate_justifications_and_cdi_queries(
    note_text: str,
    calibrated_suggestions: Dict[str, List[Dict[str, Any]]]
) -> Tuple[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]:
    """
    FR-13, FR-14, FR-15:
    1. Generates 2-3 sentence grounded justifications for retrieved candidate codes.
    2. Enforces groundedness gate (suppresses justification if ungrounded).
    3. Detects clinical documentation gaps and generates non-leading CDI physician queries.
    """
    final_suggestions: Dict[str, List[Dict[str, Any]]] = {}
    cdi_queries: List[Dict[str, Any]] = []

    for text, cand_list in calibrated_suggestions.items():
        processed_cands = []
        for cand in cand_list:
            code = cand["code"]
            desc = cand["description"]

            # 1. Extract exact sentence-level evidence span
            start_pos = note_text.lower().find(text.lower())
            start_char = start_pos if start_pos != -1 else 0
            end_char = start_char + len(text)
            
            evidence_spans = extract_evidence_sentences(note_text, text, start_char, end_char)
            evidence_text = evidence_spans[0]["sentence"] if evidence_spans else text

            # 2. Draft grounded justification citing exact evidence
            draft_justification = (
                f"Code {code} ({desc}) is supported by documented clinical findings in the note: "
                f'"{evidence_text}". The documentation confirms the diagnosis.'
            )

            # 3. Groundedness Gate Check
            is_grounded = verify_justification_grounding(draft_justification, evidence_spans)
            
            cand_copy = cand.copy()
            cand_copy["evidence_spans"] = evidence_spans
            if is_grounded:
                cand_copy["justification_md"] = draft_justification
                cand_copy["grounded"] = True
            else:
                # Suppress ungrounded justification
                cand_copy["justification_md"] = None
                cand_copy["grounded"] = False

            processed_cands.append(cand_copy)

        final_suggestions[text] = processed_cands

    # FR-14: CDI Documentation-Gap Detection (e.g. unspecified laterality, missing acuity, possible sepsis)
    note_lower = note_text.lower()

    if "possible sepsis" in note_lower or "rule out sepsis" in note_lower:
        cdi_queries.append({
            "gap_type": "missing_acuity_and_organ_dysfunction",
            "query_md": (
                "**Clinical Documentation Query — CDI**\n\n"
                "**Condition Under Inquiry:** Sepsis / Severe Sepsis\n"
                "**Documented Finding:** Note states 'Possible sepsis'.\n"
                "**Physician Clarification Requested:** Please clarify if the patient meets clinical criteria for acute organ dysfunction or severe sepsis (R65.20/A41.9), or if sepsis has been ruled out."
            )
        })

    if "fracture" in note_lower and not any(side in note_lower for side in ["left", "right", "bilateral"]):
        cdi_queries.append({
            "gap_type": "unspecified_laterality",
            "query_md": (
                "**Clinical Documentation Query — CDI**\n\n"
                "**Condition Under Inquiry:** Fracture Laterality\n"
                "**Documented Finding:** Documented fracture without specified side.\n"
                "**Physician Clarification Requested:** Please document whether the fracture affects the left, right, or bilateral sides."
            )
        })

    return final_suggestions, cdi_queries
