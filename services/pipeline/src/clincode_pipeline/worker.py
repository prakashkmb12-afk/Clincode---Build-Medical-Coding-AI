import sys
import uuid
import traceback
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from clincode_api.db.session import SessionLocal
from clincode_api.db.models import Document, DocStatus, PipelineRun, Entity, CodeSuggestion, CdiQuery, TriageBand, AssertionStatus
from clincode_pipeline.stages.sectionize import sectionize_note
from clincode_pipeline.stages.ner import run_clinical_ner
from clincode_pipeline.stages.assertion import classify_entity_assertions
from clincode_pipeline.stages.normalize import normalize_and_filter_entities
from clincode_pipeline.stages.retrieve import retrieve_icd10_candidates
from clincode_pipeline.stages.rank import rank_and_apply_coding_rules
from clincode_pipeline.stages.calibrate import calibrate_suggestion_confidence
from clincode_pipeline.stages.genai import generate_justifications_and_cdi_queries
from clincode_pipeline.provenance import record_stage_provenance


def record_checkpoint(db: Session, doc_id: str, stage: str, status: str, error: str = None, versions: Dict[str, Any] = None) -> PipelineRun:
    """Creates or updates a stage checkpoint in the database."""
    run = db.query(PipelineRun).filter_by(document_id=doc_id, stage=stage).first()
    if not run:
        run = PipelineRun(
            id=uuid.uuid4(),
            document_id=doc_id,
            stage=stage,
            status=status,
            model_versions=versions or {},
            started_at=datetime.utcnow(),
            finished_at=datetime.utcnow() if status in ["completed", "failed"] else None,
            error=error
        )
        db.add(run)
    else:
        run.status = status
        run.finished_at = datetime.utcnow() if status in ["completed", "failed"] else None
        run.error = error
        if versions:
            run.model_versions = versions

    db.commit()
    return run


def process_document_pipeline(document_id: str):
    """
    End-to-end execution pipeline for a clinical document.
    Sequentially runs stages 1 to 10 with database stage checkpointing and retry logic.
    """
    db: Session = SessionLocal()
    try:
        doc = db.query(Document).filter_by(id=document_id).first()
        if not doc:
            print(f"Document {document_id} not found.")
            return

        # Ensure idempotency: clear existing entities, suggestions, and queries for re-runs
        db.query(CodeSuggestion).filter_by(document_id=doc.id).delete()
        db.query(Entity).filter_by(document_id=doc.id).delete()
        db.query(CdiQuery).filter_by(document_id=doc.id).delete()
        db.commit()

        doc.status = DocStatus.PROCESSING
        db.commit()

        provenance_versions = record_stage_provenance()

        # Stage 3: Sectionize Note (with span preservation)
        record_checkpoint(db, document_id, "sectionize", "running")
        sections = sectionize_note(doc.deid_text)
        record_checkpoint(db, document_id, "sectionize", "completed", versions=provenance_versions)

        # Stage 4: Clinical NER Extraction
        record_checkpoint(db, document_id, "ner", "running")
        extracted_entities = run_clinical_ner(doc.deid_text, sections)
        record_checkpoint(db, document_id, "ner", "completed", versions=provenance_versions)

        # Stage 5: Assertion Classification
        record_checkpoint(db, document_id, "assertion", "running")
        asserted_entities = classify_entity_assertions(doc.deid_text, extracted_entities)
        record_checkpoint(db, document_id, "assertion", "completed", versions=provenance_versions)

        # Save ALL asserted entities to DB (including absent/family for visibility in console)
        db_entities = []
        for ent_dict in asserted_entities:
            ent = Entity(
                id=uuid.uuid4(),
                document_id=doc.id,
                text=ent_dict["text"],
                label=ent_dict["label"],
                start_char=ent_dict["start_char"],
                end_char=ent_dict["end_char"],
                section=ent_dict["section"],
                assertion=ent_dict["assertion"],
                concept_id=ent_dict.get("concept_id"),
                ner_conf=ent_dict.get("ner_conf", 1.0)
            )
            db.add(ent)
            db_entities.append((ent, ent_dict))
        db.commit()

        # Stage 6: Entity Normalization and Assertion Filtering (FR-8)
        record_checkpoint(db, document_id, "normalize", "running")
        eligible_entities = normalize_and_filter_entities(asserted_entities)
        record_checkpoint(db, document_id, "normalize", "completed", versions=provenance_versions)

        # Stage 7: ICD-10 Candidate Retrieval
        record_checkpoint(db, document_id, "retrieve", "running")
        candidates_by_entity = retrieve_icd10_candidates(db, eligible_entities)
        record_checkpoint(db, document_id, "retrieve", "completed", versions=provenance_versions)

        # Stage 8: Cross-Encoder Reranking & Deterministic Coding Rules
        record_checkpoint(db, document_id, "rank", "running")
        ranked_suggestions = rank_and_apply_coding_rules(eligible_entities, candidates_by_entity)
        record_checkpoint(db, document_id, "rank", "completed", versions=provenance_versions)

        # Stage 9: Isotonic Calibration and Triage Banding
        record_checkpoint(db, document_id, "calibrate", "running")
        calibrated_suggestions = calibrate_suggestion_confidence(ranked_suggestions)
        record_checkpoint(db, document_id, "calibrate", "completed", versions=provenance_versions)

        # Stage 10: Grounded GenAI Justifications and CDI Query Generation
        record_checkpoint(db, document_id, "genai", "running")
        final_suggestions, cdi_queries_generated = generate_justifications_and_cdi_queries(
            doc.deid_text, calibrated_suggestions
        )
        record_checkpoint(db, document_id, "genai", "completed", versions=provenance_versions)

        # Save Code Suggestions to database for eligible present entities
        has_low_confidence = False
        entity_map = {ent_dict["text"]: ent_obj for ent_obj, ent_dict in db_entities}

        for ent_dict in eligible_entities:
            text = ent_dict["text"]
            ent_obj = entity_map.get(text)
            if not ent_obj:
                continue

            ent_suggs = final_suggestions.get(text, [])
            for rank, sugg in enumerate(ent_suggs[:5], start=1):
                if sugg["band"] == TriageBand.LOW:
                    has_low_confidence = True

                cs = CodeSuggestion(
                    id=uuid.uuid4(),
                    document_id=doc.id,
                    entity_id=ent_obj.id,
                    icd10_code=sugg["icd10_code"],
                    description=sugg["description"],
                    rank=rank,
                    raw_score=sugg["raw_score"],
                    calibrated_conf=sugg["calibrated_conf"],
                    band=sugg["band"],
                    justification_md=sugg.get("justification_md"),
                    grounded=sugg.get("grounded", True),
                    evidence_spans=sugg.get("evidence_spans", []),
                    provenance=provenance_versions
                )
                db.add(cs)

        # Save CDI queries to database
        for query_dict in cdi_queries_generated:
            cq = CdiQuery(
                id=uuid.uuid4(),
                document_id=doc.id,
                gap_type=query_dict["gap_type"],
                query_md=query_dict["query_md"],
                status="draft"
            )
            db.add(cq)

        doc.status = DocStatus.READY
        db.commit()

        # Check if chart requires Investigation Team auto-routing (low confidence / conflicts)
        if has_low_confidence:
            try:
                from investigator.main import trigger_investigation_async
                trigger_investigation_async(str(doc.id), trigger_type="low_confidence")
            except Exception as inv_err:
                print(f"Investigation trigger warning: {inv_err}")

    except Exception as e:
        db.rollback()
        err_msg = traceback.format_exc()
        print(f"Pipeline failure for document {document_id}:\n{err_msg}")
        record_checkpoint(db, document_id, "pipeline_orchestration", "failed", error=err_msg)
        
        # Quarantine poison documents
        doc = db.query(Document).filter_by(id=document_id).first()
        if doc:
            doc.status = DocStatus.QUARANTINED
            db.commit()
    finally:
        db.close()
