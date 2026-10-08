import pytest
from clincode_api.db.session import SessionLocal
from clincode_api.db.models import Document, InvestigationRun
from clincode_pipeline.worker import process_document_pipeline
from investigator.graph import run_investigation_graph
from investigator.agents.verifier import run_adversarial_verifier
from investigator.state import ChartInvestigationState, InvestigationRecommendation


def test_investigation_graph_execution():
    db = SessionLocal()
    try:
        doc = db.query(Document).filter_by(external_ref="DEMO-CHART-001").first()
        assert doc is not None

        # Populate document entities via pipeline
        process_document_pipeline(str(doc.id))

        # Run Multi-Agent Investigation Graph
        state = run_investigation_graph(str(doc.id), "low_confidence", db)

        assert state.status == "ready"
        assert len(state.evidence_findings) > 0
        assert len(state.guideline_findings) > 0
        assert len(state.hierarchy_findings) > 0
        assert len(state.recommendations) > 0
        assert state.verifier_pass is True

        # Verify recommendation structure
        rec = state.recommendations[0]
        assert rec.icd10_code == "I50.23"
        assert rec.evidence_span is not None
        assert "Section I.C.9.a.1" in rec.guideline_citation

    finally:
        db.close()


def test_adversarial_verifier_kills_hallucinated_code():
    db = SessionLocal()
    try:
        state = ChartInvestigationState(
            document_id="dummy-doc",
            trigger="manual",
            recommendations=[
                # Planted bad recommendation with hallucinated code NOT in candidate set
                InvestigationRecommendation(
                    icd10_code="Z99.99_HALLUCINATED",
                    description="Fake Code",
                    rank=1,
                    confidence=0.99,
                    evidence_span="Some span",
                    guideline_citation="Some citation"
                )
            ]
        )

        # Allowed candidates list
        allowed = ["I50.23", "I10"]

        state = run_adversarial_verifier(state, db, candidate_codes=allowed)

        # Assert adversarial verifier KILLED the unretrieved hallucinated code (100% kill rate)
        assert len(state.recommendations) == 0
        assert len(state.dissenting_notes) == 1
        assert "Retrieval-Only Violation" in state.dissenting_notes[0]

    finally:
        db.close()
