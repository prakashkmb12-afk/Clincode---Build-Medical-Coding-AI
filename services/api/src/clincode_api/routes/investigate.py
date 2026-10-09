from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from clincode_api.db.session import get_db
from clincode_api.db.models import Document, InvestigationRun, User
from clincode_api.schemas import InvestigationRequest, InvestigationResponse, InvestigationReportResponse
from clincode_api.auth.roles import get_current_user
from investigator.main import trigger_investigation_async

router = APIRouter(prefix="", tags=["Investigation Team"])


@router.post("/documents/{document_id}/investigate", response_model=InvestigationResponse)
def start_investigation(
    document_id: str,
    req: InvestigationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    FR-21 & FR-25: Auto / manual trigger for Multi-Agent Investigation Team.
    Runs supervisor + 5 specialist agents with precedent memory and adversarial verifier.
    """
    doc = db.query(Document).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    trigger_val = req.trigger.value if req.trigger else "manual"
    run_id = trigger_investigation_async(str(doc.id), trigger_val)

    run = db.query(InvestigationRun).filter_by(id=run_id).first()
    return InvestigationResponse(
        run_id=str(run.id),
        document_id=str(doc.id),
        trigger=run.trigger,
        status=run.status,
        started_at=run.started_at
    )


@router.get("/investigations/{run_id}", response_model=InvestigationReportResponse)
def get_investigation(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns InvestigationReport rendered in coder console next to standard suggestions."""
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
