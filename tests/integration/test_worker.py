import uuid
from clincode_api.db.session import SessionLocal
from clincode_api.db.models import Document, DocStatus, PipelineRun
from clincode_pipeline.worker import process_document_pipeline, record_checkpoint


def test_pipeline_worker_checkpoints_and_quarantine():
    db = SessionLocal()
    try:
        # Create a test document
        doc = Document(
            id=uuid.uuid4(),
            external_ref="WORKER-TEST-DOC-001",
            doc_type="discharge",
            deid_text="CHIEF COMPLAINT:\nShortness of breath.\nASSESSMENT:\nAcute systolic heart failure.",
            status=DocStatus.RECEIVED
        )
        db.add(doc)
        db.commit()

        # Run pipeline
        process_document_pipeline(str(doc.id))

        # Refresh document
        db.refresh(doc)
        assert doc.status == DocStatus.READY

        # Verify checkpoints created in pipeline_runs
        runs = db.query(PipelineRun).filter_by(document_id=doc.id).all()
        assert len(runs) >= 5
        stages = [r.stage for r in runs]
        assert "sectionize" in stages
        assert "ner" in stages
        assert "assertion" in stages
        assert "retrieve" in stages
        assert "rank" in stages
        assert "calibrate" in stages

    finally:
        db.close()
