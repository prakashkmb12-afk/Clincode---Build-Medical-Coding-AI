from clincode_pipeline.stages.assertion import classify_entity_assertions


def test_assertion_classification_critical_cases():
    # Case 1: Present condition
    text_1 = "Patient presents with acute pneumonia and shortness of breath."
    entities_1 = [{"text": "pneumonia", "start_char": 22, "end_char": 31, "label": "condition"}]
    asserted_1 = classify_entity_assertions(text_1, entities_1)
    assert asserted_1[0]["assertion"] == "present"

    # Case 2: Negated condition (no evidence of pneumonia)
    text_2 = "Patient denies fever; no evidence of pneumonia on chest X-ray."
    entities_2 = [{"text": "pneumonia", "start_char": 37, "end_char": 46, "label": "condition"}]
    asserted_2 = classify_entity_assertions(text_2, entities_2)
    assert asserted_2[0]["assertion"] == "absent"

    # Case 3: Family history (family history of diabetes)
    text_3 = "Patient is healthy. Family history of diabetes mellitus."
    entities_3 = [{"text": "diabetes mellitus", "start_char": 38, "end_char": 55, "label": "condition"}]
    asserted_3 = classify_entity_assertions(text_3, entities_3)
    assert asserted_3[0]["assertion"] == "family"

    # Case 4: Historical condition (history of stroke)
    text_4 = "Patient has a past history of stroke in 2018."
    entities_4 = [{"text": "stroke", "start_char": 30, "end_char": 36, "label": "condition"}]
    asserted_4 = classify_entity_assertions(text_4, entities_4)
    assert asserted_4[0]["assertion"] == "historical"

    # Case 5: Possible / Uncertain condition (possible sepsis)
    text_5 = "Patient is febrile with concern for possible sepsis."
    entities_5 = [{"text": "sepsis", "start_char": 45, "end_char": 51, "label": "condition"}]
    asserted_5 = classify_entity_assertions(text_5, entities_5)
    assert asserted_5[0]["assertion"] == "possible"
