from clincode_pipeline.stages.deidentify import deidentify_text


def test_phi_leak_prevention():
    raw_clinical_note = (
        "PATIENT NAME: Johnathan Doe\n"
        "MRN: 987654321\n"
        "DOB: 1955-04-12\n"
        "PHONE: 555-123-4567\n\n"
        "Patient Johnathan Doe was admitted on 2026-10-01 with acute-on-chronic systolic heart failure."
    )

    deid_text, raw_enc, phi_map_enc, summary = deidentify_text(raw_clinical_note)

    # ZERO unencrypted PHI must leak into deid_text sent to search indexes or LLMs
    assert "Johnathan Doe" not in deid_text
    assert "987654321" not in deid_text
    assert "555-123-4567" not in deid_text
    assert "1955-04-12" not in deid_text

    # Typed placeholders must be present
    assert "[NAME_1]" in deid_text or "[NAME_" in deid_text
    assert "[MRN_1]" in deid_text or "[MRN_" in deid_text
    assert "[PHONE_1]" in deid_text or "[PHONE_" in deid_text
