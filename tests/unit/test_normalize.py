from clincode_pipeline.stages.normalize import normalize_and_filter_entities


def test_entity_normalization_and_filtering():
    entities = [
        {"text": "pneumonia", "assertion": "present", "label": "condition"},
        {"text": "pneumonia", "assertion": "absent", "label": "condition"},       # Negated -> Must be filtered
        {"text": "diabetes", "assertion": "family", "label": "condition"},        # Family -> Must be filtered
        {"text": "stroke", "assertion": "historical", "label": "condition"},      # Historical -> Allowed
        {"text": "HTN", "assertion": "present", "label": "condition"},             # Abbreviation -> Expanded
    ]

    filtered = normalize_and_filter_entities(entities, allow_historical=True)

    # Negated and family history must be excluded
    assert len(filtered) == 3
    texts = [e["text"] for e in filtered]
    assert "pneumonia" in texts
    assert "stroke" in texts
    assert "HTN" in texts

    # Verify abbreviation normalization
    htn_ent = next(e for e in filtered if e["text"] == "HTN")
    assert htn_ent["normalized_text"] == "hypertension"
