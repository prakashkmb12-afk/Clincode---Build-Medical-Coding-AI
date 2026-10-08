from clincode_pipeline.stages.rank import rank_and_apply_coding_rules


def test_cross_encoder_rank_and_excludes1_validation():
    entities = [
        {"text": "systolic heart failure", "concept_id": "I50.23", "label": "condition"}
    ]

    candidates_by_entity = {
        "systolic heart failure": [
            {
                "code": "I50.23",
                "description": "Acute-on-chronic systolic (congestive) heart failure",
                "billable": True,
                "excludes1": ["I50.1", "I50.9"]
            },
            {
                "code": "I50.9",
                "description": "Heart failure, unspecified",
                "billable": True,
                "excludes1": ["I50.23"]
            }
        ]
    }

    ranked = rank_and_apply_coding_rules(entities, candidates_by_entity)

    assert "systolic heart failure" in ranked
    top_cands = ranked["systolic heart failure"]

    # I50.23 should be top-ranked due to exact concept match and specificity boost
    assert top_cands[0]["code"] == "I50.23"

    # Excludes1 rule: I50.9 is excluded when I50.23 is present
    codes = [c["code"] for c in top_cands]
    assert "I50.9" not in codes
