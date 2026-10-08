import pytest
from clincode_pipeline.stages.deidentify import deidentify_text, reidentify_text


def test_deidentify_scrubs_phi_and_encrypts():
    raw_note = (
        "Patient: John Doe, SSN: 123-45-6789, MRN: 98765432. "
        "Dr. Smith evaluated patient on 05/12/2026. Contact at 555-123-4567 or jdoe@example.com."
    )

    deid_text, raw_enc, phi_map_enc, summary = deidentify_text(raw_note)

    # Assert raw PHI strings are NOT present in deid_text
    assert "John Doe" not in deid_text
    assert "123-45-6789" not in deid_text
    assert "98765432" not in deid_text
    assert "555-123-4567" not in deid_text
    assert "jdoe@example.com" not in deid_text

    # Assert placeholders ARE present
    assert "[SSN_1]" in deid_text or "[SSN_1]" in summary["placeholders"]
    assert len(summary["placeholders"]) > 0

    # Assert re-identification restores original text
    restored_note = reidentify_text(deid_text, phi_map_enc)
    assert "123-45-6789" in restored_note
    assert "98765432" in restored_note
    assert "jdoe@example.com" in restored_note
