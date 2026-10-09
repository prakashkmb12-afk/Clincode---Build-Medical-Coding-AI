import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from clincode_api.db.session import get_db
from clincode_api.db.models import Document, DocStatus, DocType, PipelineRun, User
from clincode_api.schemas import DocumentCreate, DocumentResponse, DocumentStatusResponse
from clincode_api.auth.roles import get_current_user
from clincode_api.audit import log_audit_event
from clincode_pipeline.stages.deidentify import deidentify_text
from clincode_pipeline.stages.ocr_intake import perform_ocr_intake
from clincode_pipeline.worker import process_document_pipeline

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    doc_in: DocumentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    FR-1 & FR-1b: Ingests clinical notes (raw text, scanned PDF/image).
    Applies OCR if scanned, de-identification pass, encrypts PHI map, and enqueues background processing.
    """
    raw_text = doc_in.text
    ocr_applied = False
    ocr_low_conf_count = 0

    if doc_in.is_scanned_pdf and doc_in.image_bytes_base64:
        raw_text, line_data, ocr_low_conf_count = perform_ocr_intake(doc_in.image_bytes_base64)
        ocr_applied = True

    # Perform PHI de-identification pass
    deid_text, raw_enc, phi_map_enc, phi_summary = deidentify_text(raw_text)

    doc_id = uuid.uuid4()
    doc = Document(
        id=doc_id,
        external_ref=doc_in.external_ref,
        doc_type=doc_in.doc_type,
        raw_text_encrypted=raw_enc,
        deid_text=deid_text,
        phi_map_encrypted=phi_map_enc,
        status=DocStatus.RECEIVED,
        version=1,
        ocr_applied=ocr_applied,
        ocr_low_confidence_count=ocr_low_conf_count,
        created_at=datetime.utcnow()
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Log audit event
    log_audit_event(
        db,
        actor=current_user.username,
        action="DOCUMENT_INGESTED",
        resource_type="document",
        resource_id=str(doc.id),
        detail={"external_ref": doc.external_ref, "ocr_applied": ocr_applied, "phi_scrubbed": phi_summary["total_phi_scrubbed"]}
    )

    # Schedule async background processing task
    background_tasks.add_task(process_document_pipeline, str(doc.id))

    return DocumentResponse(
        document_id=str(doc.id),
        external_ref=doc.external_ref,
        doc_type=doc.doc_type,
        status=doc.status,
        version=doc.version,
        ocr_applied=doc.ocr_applied,
        ocr_low_confidence_count=doc.ocr_low_confidence_count,
        deid_text=doc.deid_text,
        created_at=doc.created_at
    )


@router.get("", response_model=List[DocumentResponse])
def list_documents(
    status_filter: Optional[DocStatus] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns list of ingested documents for coder worklist."""
    query = db.query(Document)
    if status_filter:
        query = query.filter(Document.status == status_filter)
    docs = query.order_by(Document.created_at.desc()).limit(limit).all()

    return [
        DocumentResponse(
            document_id=str(d.id),
            external_ref=d.external_ref,
            doc_type=d.doc_type,
            status=d.status,
            version=d.version,
            ocr_applied=d.ocr_applied,
            ocr_low_confidence_count=d.ocr_low_confidence_count,
            deid_text=d.deid_text,
            created_at=d.created_at
        ) for d in docs
    ]


@router.get("/{document_id}", response_model=DocumentStatusResponse)
def get_document_status(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns document status and detailed stage checkpoint progress."""
    doc = db.query(Document).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    pipeline_runs = db.query(PipelineRun).filter_by(document_id=document_id).all()
    stage_progress = [
        {
            "stage": run.stage,
            "status": run.status,
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "finished_at": run.finished_at.isoformat() if run.finished_at else None,
            "error": run.error
        }
        for run in pipeline_runs
    ]

    return DocumentStatusResponse(
        document_id=str(doc.id),
        status=doc.status,
        stage_progress=stage_progress,
        created_at=doc.created_at
    )
