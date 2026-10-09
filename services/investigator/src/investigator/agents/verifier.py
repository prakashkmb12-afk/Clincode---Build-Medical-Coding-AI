from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from investigator.state import ChartInvestigationState, InvestigationRecommendation
from investigator.tools.rules_tools import coding_rules_check


def run_adversarial_verifier(state: ChartInvestigationState, db: Session, candidate_codes: List[str] = None) -> ChartInvestigationState:
    """
    FR-24 Adversarial Verifier Agent:
    Attacks and claim-checks every recommendation:
    1. Evidence span exists
    2. Guideline citation or hierarchy justification exists
    3. Zero Excludes1 conflict
    4. Code exists in retrieved candidate set (Retrieval-Only rule enforced in executable code!)
    
    Recommendations failing any check are killed before a human sees them.
    """
    state.tool_call_count += 1
    allowed_candidates = candidate_codes or ["I50.23", "I50.21", "I10", "E11.9", "E11.21", "I69.30", "A41.9", "R65.20", "R07.9", "J18.9"]

    verified_recommendations = []
    all_passed = True

    proposed_code_list = [rec.icd10_code for rec in state.recommendations]
    rules_result = coding_rules_check(db, proposed_code_list)

    for rec in state.recommendations:
        failed_reasons = []

        # Check 1: Code must exist in retrieved candidate set (RETRIEVAL-ONLY RULE ENFORCED IN CODE)
        if rec.icd10_code not in allowed_candidates:
            failed_reasons.append(f"Code {rec.icd10_code} was NOT in retrieved candidate set (Retrieval-Only Violation)")

        # Check 2: Evidence span must exist
        if not rec.evidence_span or len(rec.evidence_span.strip()) < 3:
            failed_reasons.append("Evidence span missing or insufficient")

        # Check 3: Guideline citation or hierarchy justification must exist
        if not rec.guideline_citation or len(rec.guideline_citation.strip()) < 3:
            failed_reasons.append("Guideline citation / hierarchy justification missing")

        # Check 4: No Excludes1 conflicts
        for conflict in rules_result["conflicts"]:
            if conflict["code_a"] == rec.icd10_code or conflict["code_b"] == rec.icd10_code:
                failed_reasons.append(f"Excludes1 conflict detected with {conflict['code_b'] if conflict['code_a'] == rec.icd10_code else conflict['code_a']}")

        if failed_reasons:
            all_passed = False
            rec.verifier_passed = False
            dissent = f"VERIFIER KILLED recommendation for {rec.icd10_code}: " + "; ".join(failed_reasons)
            rec.dissent_note = dissent
            state.dissenting_notes.append(dissent)
        else:
            rec.verifier_passed = True
            verified_recommendations.append(rec)

    # Handle revision loop policy (1 revision allowed)
    if not all_passed and state.revision_loop_count < state.max_revision_loops:
        state.revision_loop_count += 1
        print(f"Adversarial Verifier triggered revision loop {state.revision_loop_count}")

    state.recommendations = verified_recommendations
    state.verifier_pass = all_passed
    return state
