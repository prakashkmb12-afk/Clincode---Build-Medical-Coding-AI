from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from clincode_api.db.session import get_db
from clincode_api.db.models import Document, Entity, CodeSuggestion, User
from clincode_api.schemas import DocumentSuggestionsResponse, EntityResponse, CodeSuggestionResponse, EvidenceSpan
from clincode_api.auth.roles import get_current_user

router = APIRouter(prefix="/documents", tags=["Suggestions"])


@router.get("/{document_id}/suggestions", response_model=DocumentSuggestionsResponse)
def get_document_suggestions(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns de-identified text, extracted entities, suggested ICD-10 codes, confidence scores,
    calibrated triage bands, grounded justifications, and exact sentence evidence spans for a document.
    """
    doc = db.query(Document).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    entities = db.query(Entity).filter_by(document_id=document_id).all()
    suggestions = db.query(CodeSuggestion).filter_by(document_id=document_id).order_by(CodeSuggestion.rank.asc()).all()

    entity_responses = [
        EntityResponse(
            id=str(e.id),
            text=e.text,
            label=e.label,
            start_char=e.start_char,
            end_char=e.end_char,
            section=e.section,
            assertion=e.assertion,
            concept_id=e.concept_id,
            ner_conf=e.ner_conf
        ) for e in entities
    ]

    suggestion_responses = []
    for s in suggestions:
        spans = []
        if s.evidence_spans:
            for item in s.evidence_spans:
                spans.append(EvidenceSpan(
                    sentence=item.get("sentence", ""),
                    start_char=item.get("start_char", 0),
                    end_char=item.get("end_char", 0),
                    section=item.get("section", "UNKNOWN")
                ))

        suggestion_responses.append(CodeSuggestionResponse(
            id=str(s.id),
            entity_id=str(s.entity_id),
            icd10_code=s.icd10_code,
            description=s.description,
            rank=s.rank,
            raw_score=s.raw_score,
            calibrated_conf=s.calibrated_conf,
            band=s.band,
            justification_md=s.justification_md,
            grounded=s.grounded,
            evidence_spans=spans,
            provenance=s.provenance
        ))

    return DocumentSuggestionsResponse(
        document_id=str(doc.id),
        status=doc.status,
        deid_text=doc.deid_text,
        entities=entity_responses,
        suggestions=suggestion_responses
    )
