import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from clincode_api.db.session import SessionLocal, get_db
from clincode_api.db.models import InvestigationRun, Document, DocStatus, User
from clincode_api.auth.roles import get_current_user
from clincode_api.schemas import InvestigationRequest, InvestigationResponse, InvestigationReportResponse
from investigator.graph import run_investigation_graph


def trigger_investigation_async(document_id: str, trigger_type: str = "manual") -> str:
    """Executes investigation workflow synchronously or as async worker task."""
    db: Session = SessionLocal()
    try:
        run_id = uuid.uuid4()
        run = InvestigationRun(
            id=run_id,
            document_id=document_id,
            trigger=trigger_type,
            status="running",
            started_at=datetime.utcnow()
        )
        db.add(run)
        db.commit()

        state = run_investigation_graph(document_id, trigger_type, db)

        run.status = "ready"
        run.finished_at = datetime.utcnow()
        run.report = state.model_dump()
        run.verifier_pass = state.verifier_pass
        run.agent_versions = {
            "supervisor": "v1.0-langgraph",
            "evidence_analyst": "v1.0",
            "guideline_analyst": "v1.0-rag",
            "specificity_agent": "v1.0",
            "verifier": "v1.0-adversarial"
        }
        db.commit()
        return str(run.id)
    finally:
        db.close()


app = FastAPI(title="ClinCode Investigator Service", version="0.1.0")


@app.post("/charts/{document_id}/investigate", response_model=InvestigationResponse)
def start_investigation(
    document_id: str,
    req: InvestigationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """FR-21: Triggers LangGraph multi-agent investigation workflow for complex/low-confidence charts."""
    doc = db.query(Document).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    run_id = uuid.uuid4()
    run = InvestigationRun(
        id=run_id,
        document_id=doc.id,
        trigger=req.trigger.value if req.trigger else "manual",
        status="queued",
        started_at=datetime.utcnow()
    )
    db.add(run)
    db.commit()

    background_tasks.add_task(trigger_investigation_async, str(doc.id), run.trigger)

    return InvestigationResponse(
        run_id=str(run.id),
        document_id=str(doc.id),
        trigger=run.trigger,
        status="queued",
        started_at=run.started_at
    )


@app.get("/investigations/{run_id}", response_model=InvestigationReportResponse)
def get_investigation_report(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """FR-25: Returns typed InvestigationReport (recommendations, evidence, citations, verifier status)."""
    run = db.query(InvestigationRun).filter_by(id=run_id).first()
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Investigation run not found")

    return InvestigationReportResponse(
        run_id=str(run.id),
        document_id=str(run.document_id),
        status=run.status,
        trigger=run.trigger,
        report=run.report,
        verifier_pass=run.verifier_pass,
        started_at=run.started_at,
        finished_at=run.finished_at
    )
