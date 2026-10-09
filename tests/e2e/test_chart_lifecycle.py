from fastapi.testclient import TestClient
from clincode_api.main import app

client = TestClient(app)


def test_full_chart_lifecycle_e2e():
    # 1. Login
    auth_resp = client.post(
        "/api/v1/auth/login",
        json={"username": "demo_coder", "password": "coder123"}
    )
    assert auth_resp.status_code == 200
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Intake Chart Document
    create_resp = client.post(
        "/api/v1/documents",
        headers=headers,
        json={
            "external_ref": "E2E-CHART-999",
            "doc_type": "discharge",
            "text": (
                "CHIEF COMPLAINT:\nShortness of breath.\n\n"
                "HISTORY OF PRESENT ILLNESS:\nPatient with acute-on-chronic systolic heart failure "
                "presenting to ER with severe dyspnea. Denies chest pain.\n\n"
                "PAST MEDICAL HISTORY:\nEssential hypertension, type 2 diabetes mellitus.\n\n"
                "ASSESSMENT AND PLAN:\nAcute-on-chronic systolic heart failure."
            )
        }
    )
    assert create_resp.status_code == 201
    doc_id = create_resp.json()["document_id"]

    # 3. Retrieve Suggestions & Evidence Spans
    sugg_resp = client.get(f"/api/v1/documents/{doc_id}/suggestions", headers=headers)
    assert sugg_resp.status_code == 200
    sugg_data = sugg_resp.json()
    assert sugg_data["document_id"] == doc_id
    assert len(sugg_data["entities"]) > 0

    # 4. Review Action
    if len(sugg_data["suggestions"]) > 0:
        suggestion_id = sugg_data["suggestions"][0]["id"]
        action_resp = client.post(
            f"/api/v1/suggestions/{suggestion_id}/action",
            headers=headers,
            json={"action": "accept", "reason": "Verified against clinical note"}
        )
        assert action_resp.status_code == 200

    # 5. Submit Final Chart Coding
    submit_resp = client.post(
        f"/api/v1/documents/{doc_id}/submit",
        headers=headers,
        json={"final_codes": ["I50.23", "I10", "E11.9"]}
    )
    assert submit_resp.status_code == 200
    assert submit_resp.json()["final_codes"] == ["I50.23", "I10", "E11.9"]

    # 6. Export FHIR Claim JSON
    export_resp = client.get(f"/api/v1/documents/{doc_id}/export", headers=headers)
    assert export_resp.status_code == 200
    claim_json = export_resp.json()
    assert claim_json["resourceType"] == "Claim"
    assert claim_json["status"] == "active"
    assert claim_json["clincode_metadata"]["document_id"] == doc_id
