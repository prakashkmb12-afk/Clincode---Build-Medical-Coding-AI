import pytest
from fastapi.testclient import TestClient

from clincode_api.main import app
from clincode_api.db.session import SessionLocal
from clincode_api.db.models import Document, User

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "clincode_api"


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "process_cpu_seconds_total" in response.text or "python_info" in response.text


def test_auth_login_and_me():
    # Login as demo_coder
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "demo_coder", "password": "coder123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "coder"

    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify /me endpoint
    me_response = client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["username"] == "demo_coder"


def test_document_ingestion_and_suggestions_flow():
    # Login
    auth_resp = client.post(
        "/api/v1/auth/login",
        json={"username": "demo_coder", "password": "coder123"}
    )
    headers = {"Authorization": f"Bearer {auth_resp.json()['access_token']}"}

    # Ingest a new document via API
    create_resp = client.post(
        "/api/v1/documents",
        headers=headers,
        json={
            "external_ref": "API-TEST-DOC-100",
            "doc_type": "discharge",
            "text": (
                "CHIEF COMPLAINT:\nShortness of breath.\n\n"
                "HISTORY OF PRESENT ILLNESS:\nPatient with acute systolic heart failure presenting with dyspnea. "
                "Denies chest pain. Family history of diabetes.\n\n"
                "PAST MEDICAL HISTORY:\nEssential hypertension.\n\n"
                "ASSESSMENT AND PLAN:\nAcute systolic heart failure. Rule out possible sepsis."
            )
        }
    )
    assert create_resp.status_code == 201
    doc_data = create_resp.json()
    doc_id = doc_data["document_id"]
    assert doc_data["external_ref"] == "API-TEST-DOC-100"

    # Get document status
    status_resp = client.get(f"/api/v1/documents/{doc_id}", headers=headers)
    assert status_resp.status_code == 200

    # Get suggestions for document
    sugg_resp = client.get(f"/api/v1/documents/{doc_id}/suggestions", headers=headers)
    assert sugg_resp.status_code == 200
    sugg_data = sugg_resp.json()
    assert sugg_data["document_id"] == doc_id
    assert "entities" in sugg_data
    assert "suggestions" in sugg_data

    # If suggestions exist, perform an accept action
    if len(sugg_data["suggestions"]) > 0:
        suggestion_id = sugg_data["suggestions"][0]["id"]
        action_resp = client.post(
            f"/api/v1/suggestions/{suggestion_id}/action",
            headers=headers,
            json={"action": "accept", "reason": "Confirmed against clinical note"}
        )
        assert action_resp.status_code == 200
        assert action_resp.json()["action"] == "accept"

    # Submit final chart coding
    submit_resp = client.post(
        f"/api/v1/documents/{doc_id}/submit",
        headers=headers,
        json={"final_codes": ["I50.21", "I10"]}
    )
    assert submit_resp.status_code == 200
    assert submit_resp.json()["final_codes"] == ["I50.21", "I10"]

    # Export FHIR Claim JSON
    export_resp = client.get(f"/api/v1/documents/{doc_id}/export", headers=headers)
    assert export_resp.status_code == 200
    export_data = export_resp.json()
    assert export_data["resourceType"] == "Claim"
    assert export_data["clincode_metadata"]["document_id"] == doc_id


def test_admin_metrics_and_models():
    # Login as admin
    auth_resp = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    headers = {"Authorization": f"Bearer {auth_resp.json()['access_token']}"}

    metrics_resp = client.get("/api/v1/admin/metrics", headers=headers)
    assert metrics_resp.status_code == 200
    assert "auto_accept_precision" in metrics_resp.json()

    models_resp = client.get("/api/v1/admin/models", headers=headers)
    assert models_resp.status_code == 200
    assert "ner_model_version" in models_resp.json()
