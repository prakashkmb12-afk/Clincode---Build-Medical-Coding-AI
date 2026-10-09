from typing import Dict, Any


def record_stage_provenance() -> Dict[str, Any]:
    """
    Returns pinned version provenance for pipeline stages and model artifacts.
    Enables auditability of every suggested code.
    """
    return {
        "ner_model": "Bio_ClinicalBERT-v1.2-onnx",
        "assertion_model": "Bio_ClinicalBERT-assertion-v1.0",
        "embedding_model": "bge-small-en-v1.5",
        "reranker_model": "cross-encoder-ms-marco-MiniLM-L-6-v2",
        "coding_rules_version": "ICD10CM-FY2026-v1.0",
        "calibration_version": "isotonic-fit-v1.1",
        "justification_prompt_version": "v2.1-grounded",
        "cdi_query_prompt_version": "v1.4-non-leading"
    }
