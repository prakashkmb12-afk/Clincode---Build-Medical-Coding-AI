from clincode_pipeline.stages.retrieve import rrf_fusion


def test_rrf_fusion_scoring():
    dense_hits = [
        {"code": "I50.23", "description": "Acute-on-chronic heart failure", "score": 0.95},
        {"code": "I50.21", "description": "Acute heart failure", "score": 0.85}
    ]
    sparse_hits = [
        {"code": "I50.23", "description": "Acute-on-chronic heart failure", "score": 12.4},
        {"code": "I10", "description": "Essential hypertension", "score": 8.1}
    ]

    fused = rrf_fusion(dense_hits, sparse_hits, k=60, top_n=5)
    assert len(fused) > 0
    # I50.23 appears at rank 1 in both lists, so it must be top ranked
    assert fused[0]["code"] == "I50.23"
    assert "rrf_score" in fused[0]
