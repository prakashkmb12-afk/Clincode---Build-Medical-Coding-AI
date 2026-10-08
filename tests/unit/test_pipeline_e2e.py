import pytest
from clincode_api.db.session import SessionLocal
from clincode_api.db.models import Document, Entity, CodeSuggestion, CdiQuery, DocStatus, TriageBand
from clincode_pipeline.worker import process_document_pipeline


def test_end_to_end_pipeline_execution():
    db = SessionLocal()
    try:
        doc = db.query(Document).filter_by(external_ref="DEMO-CHART-001").first()
        assert doc is not None

        # Execute deterministic pipeline on demo document
        process_document_pipeline(str(doc.id))

        db.refresh(doc)
        assert doc.status == DocStatus.READY

        entities = db.query(Entity).filter_by(document_id=doc.id).all()
        assert len(entities) > 0

        # Verify Assertion Detection Rules (FR-6, FR-8):
        entity_tuples = [(e.text.lower(), e.assertion.value) for e in entities]
        
        # 1. "acute-on-chronic systolic heart failure" is present
        assert ("acute-on-chronic systolic heart failure", "present") in entity_tuples
        
        # 2. "chest pain" is absent (negated)
        assert ("chest pain", "absent") in entity_tuples
        
        # 3. "diabetes mellitus" under family history is family
        assert ("diabetes mellitus", "family") in entity_tuples

        suggestions = db.query(CodeSuggestion).filter_by(document_id=doc.id).all()
        assert len(suggestions) > 0

        # Assert heart failure code I50.23 is present in suggestions with auto band
        hf_suggs = [s for s in suggestions if s.icd10_code == "I50.23"]
        assert len(hf_suggs) > 0
        assert any(s.band == TriageBand.AUTO for s in hf_suggs)
        assert hf_suggs[0].evidence_spans is not None
        assert any(s.justification_md is not None for s in hf_suggs)

        # Assert negated chest pain (R07.9) was NOT suggested/coded
        coded_icd_codes = [s.icd10_code for s in suggestions]
        assert "R07.9" not in coded_icd_codes  # chest pain excluded because negated!

        cdi_queries = db.query(CdiQuery).filter_by(document_id=doc.id).all()
        assert len(cdi_queries) > 0
        assert any(q.gap_type == "missing_acuity_and_organ_dysfunction" for q in cdi_queries)

    finally:
        db.close()
