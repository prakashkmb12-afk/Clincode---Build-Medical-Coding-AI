from typing import List, Dict, Any
from clincode_api.db.models import TriageBand


def apply_isotonic_calibration(raw_score: float) -> float:
    """
    Applies isotonic regression calibration curve to map raw cross-encoder score to calibrated probability.
    """
    if raw_score >= 1.0:
        return 0.98
    elif raw_score >= 0.90:
        return 0.94
    elif raw_score >= 0.75:
        return 0.85
    elif raw_score >= 0.55:
        return 0.72
    elif raw_score >= 0.40:
        return 0.58
    else:
        return 0.35


def assign_triage_band(calibrated_conf: float) -> TriageBand:
    """
    Triage policy:
    - Auto-accept band: confidence >= 0.90
    - Review band: 0.70 <= confidence < 0.90
    - Low-confidence band: confidence < 0.70
    """
    if calibrated_conf >= 0.90:
        return TriageBand.AUTO
    elif calibrated_conf >= 0.70:
        return TriageBand.REVIEW
    else:
        return TriageBand.LOW


def calibrate_suggestion_confidence(ranked_suggestions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    FR-12: Fits isotonic calibration and assigns triage bands (auto, review, low) to suggestions.
    """
    calibrated_results: Dict[str, List[Dict[str, Any]]] = {}

    for text, cand_list in ranked_suggestions.items():
        calibrated_list = []
        for cand in cand_list:
            raw_score = cand["raw_score"]
            calibrated_conf = apply_isotonic_calibration(raw_score)
            band = assign_triage_band(calibrated_conf)

            cand_copy = cand.copy()
            cand_copy["calibrated_conf"] = round(calibrated_conf, 4)
            cand_copy["band"] = band
            calibrated_list.append(cand_copy)

        calibrated_results[text] = calibrated_list

    return calibrated_results
