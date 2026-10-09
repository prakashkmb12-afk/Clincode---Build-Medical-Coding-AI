from clincode_pipeline.stages.calibrate import apply_isotonic_calibration, assign_triage_band, calibrate_suggestion_confidence
from clincode_api.db.models import TriageBand


def test_isotonic_calibration_and_triage_bands():
    # 1. Test calibration curve
    assert apply_isotonic_calibration(1.0) == 0.98
    assert apply_isotonic_calibration(0.85) == 0.85
    assert apply_isotonic_calibration(0.50) == 0.58

    # 2. Test triage band mapping
    assert assign_triage_band(0.95) == TriageBand.AUTO
    assert assign_triage_band(0.80) == TriageBand.REVIEW
    assert assign_triage_band(0.55) == TriageBand.LOW

    # 3. Test full suggestion dictionary calibration
    ranked_suggestions = {
        "heart failure": [
            {"code": "I50.23", "description": "Acute-on-chronic heart failure", "raw_score": 0.95},
            {"code": "I50.9", "description": "Heart failure, unspecified", "raw_score": 0.45}
        ]
    }

    calibrated = calibrate_suggestion_confidence(ranked_suggestions)
    suggs = calibrated["heart failure"]

    assert suggs[0]["band"] == TriageBand.AUTO
    assert suggs[0]["calibrated_conf"] >= 0.90

    assert suggs[1]["band"] == TriageBand.LOW
    assert suggs[1]["calibrated_conf"] < 0.70
