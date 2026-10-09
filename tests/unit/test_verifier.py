from clincode_api.db.session import SessionLocal
from investigator.state import ChartInvestigationState, InvestigationRecommendation
from investigator.agents.verifier import run_adversarial_verifier


def test_adversarial_verifier_kills_unretrieved_code():
    db = SessionLocal()
    try:
        state = ChartInvestigationState(
            document_id="TEST-DOC-VERIFIER",
            trigger="low_confidence",
            recommendations=[
                InvestigationRecommendation(
                    icd10_code="Z99.99", # Unretrieved ungrounded hallucination
                    description="Arbitrary Code",
                    rank=1,
                    confidence=0.99,
                    evidence_span="Some text",
                    guideline_citation="Section I.A",
                    verifier_passed=True
                )
            ]
        )

        allowed_candidates = ["I50.23", "I10"]

        verified_state = run_adversarial_verifier(state, db, candidate_codes=allowed_candidates)

        # Recommendation for Z99.99 must be KILLED because it violates the Retrieval-Only Rule
        assert len(verified_state.recommendations) == 0
        assert len(verified_state.dissenting_notes) > 0
        assert "Retrieval-Only Violation" in verified_state.dissenting_notes[0]
        assert verified_state.verifier_pass is False

    finally:
        db.close()
