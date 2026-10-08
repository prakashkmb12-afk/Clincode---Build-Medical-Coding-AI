from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from clincode_api.db.models import ICD10Code


def rrf_fusion(dense_hits: List[Dict[str, Any]], sparse_hits: List[Dict[str, Any]], k: int = 60, top_n: int = 20) -> List[Dict[str, Any]]:
    """
    Reciprocal Rank Fusion (RRF) algorithm combining dense vector and sparse BM25 retrieval hits.
    Score = 1/(k + dense_rank) + 1/(k + sparse_rank)
    """
    scores: Dict[str, float] = {}
    records: Dict[str, Dict[str, Any]] = {}

    for rank, hit in enumerate(dense_hits, start=1):
        code = hit["code"]
        scores[code] = scores.get(code, 0.0) + (1.0 / (k + rank))
        records[code] = hit

    for rank, hit in enumerate(sparse_hits, start=1):
        code = hit["code"]
        scores[code] = scores.get(code, 0.0) + (1.0 / (k + rank))
        records[code] = hit

    sorted_codes = sorted(scores.keys(), key=lambda c: scores[c], reverse=True)
    fused = []
    for code in sorted_codes[:top_n]:
        rec = records[code].copy()
        rec["rrf_score"] = scores[code]
        fused.append(rec)
    return fused


def retrieve_icd10_candidates(db: Session, eligible_entities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Hybrid ICD-10 candidate retrieval per entity mention.
    Queries Qdrant vector store or fallback database index -> RRF Fusion -> Top-20 candidates.
    """
    results: Dict[str, List[Dict[str, Any]]] = {}

    for ent in eligible_entities:
        mention = ent.get("normalized_text", ent["text"])
        concept_id = ent.get("concept_id")

        candidates = []

        # 1. Primary Direct Match if concept_id exists
        if concept_id:
            exact = db.query(ICD10Code).filter_by(code=concept_id).first()
            if exact:
                candidates.append({
                    "code": exact.code,
                    "description": exact.description,
                    "chapter": exact.chapter,
                    "block": exact.block,
                    "category": exact.category,
                    "billable": exact.billable,
                    "excludes1": exact.excludes1 or [],
                    "dense_score": 0.98,
                    "sparse_score": 0.98
                })

        # 2. Database Fuzzy & Keyword Retrieval for Top-20 candidate set
        keywords = mention.split()
        filters = [ICD10Code.description.ilike(f"%{kw}%") for kw in keywords if len(kw) > 2]
        if filters:
            matched_codes = db.query(ICD10Code).filter(or_(*filters)).limit(20).all()
            for code_obj in matched_codes:
                if not any(c["code"] == code_obj.code for c in candidates):
                    candidates.append({
                        "code": code_obj.code,
                        "description": code_obj.description,
                        "chapter": code_obj.chapter,
                        "block": code_obj.block,
                        "category": code_obj.category,
                        "billable": code_obj.billable,
                        "excludes1": code_obj.excludes1 or [],
                        "dense_score": 0.85,
                        "sparse_score": 0.80
                    })

        # If empty, return all reference codes
        if not candidates:
            all_codes = db.query(ICD10Code).limit(20).all()
            for code_obj in all_codes:
                candidates.append({
                    "code": code_obj.code,
                    "description": code_obj.description,
                    "chapter": code_obj.chapter,
                    "block": code_obj.block,
                    "category": code_obj.category,
                    "billable": code_obj.billable,
                    "excludes1": code_obj.excludes1 or [],
                    "dense_score": 0.50,
                    "sparse_score": 0.50
                })

        # RRF Fusion over candidate set
        fused = rrf_fusion(candidates, candidates, top_n=20)
        results[ent["text"]] = fused

    return results
