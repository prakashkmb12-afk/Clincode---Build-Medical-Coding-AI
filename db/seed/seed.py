import os
import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from clincode_api.db.session import engine, Base, SessionLocal
from clincode_api.db.models import User, UserRole, ICD10Code, Document, DocType, DocStatus
from clincode_api.auth.jwt import get_password_hash
from clincode_pipeline.stages.deidentify import deidentify_text

DEMO_CHART_TEXT = (
    "CHIEF COMPLAINT:\n"
    "Shortness of breath and worsening lower extremity swelling.\n\n"
    "HISTORY OF PRESENT ILLNESS:\n"
    "Patient is a 68-year-old male with a history of acute-on-chronic systolic heart failure "
    "presenting to the emergency department with severe dyspnea on exertion. "
    "Patient denies chest pain. Family history of diabetes mellitus.\n\n"
    "PAST MEDICAL HISTORY:\n"
    "Essential hypertension, type 2 diabetes mellitus, history of stroke.\n\n"
    "ASSESSMENT AND PLAN:\n"
    "1. Acute-on-chronic systolic heart failure: Initiate IV furosemide, monitor daily weights and electrolyte panel.\n"
    "2. Hypertension: Continue home oral lisinopril.\n"
    "3. Possible sepsis: Patient is febrile with elevated WBC count. Order blood cultures and start empiric broad-spectrum coverage."
)


def seed_database():
    """Populates the database with initial users, ICD-10 reference codes, and demo chart."""
    print("Creating database tables if not exist...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1. Seed Users
        users_data = [
            ("admin", "admin@clincode.org", "admin123", UserRole.ADMIN),
            ("demo_coder", "coder@clincode.org", "coder123", UserRole.CODER),
            ("demo_cdi", "cdi@clincode.org", "cdi123", UserRole.CDI_SPECIALIST),
            ("demo_manager", "manager@clincode.org", "manager123", UserRole.MANAGER),
        ]

        for username, email, password, role in users_data:
            existing = db.query(User).filter_by(username=username).first()
            if not existing:
                user = User(
                    username=username,
                    email=email,
                    password_hash=get_password_hash(password),
                    role=role
                )
                db.add(user)
        db.commit()
        print("Users seeded successfully.")

        # 2. Seed ICD-10 Codes
        icd10_path = os.path.join("data", "icd10cm", "icd10cm_codes.json")
        if os.path.exists(icd10_path):
            with open(icd10_path, "r", encoding="utf-8") as f:
                codes_list = json.load(f)
            for item in codes_list:
                existing_code = db.query(ICD10Code).filter_by(code=item["code"]).first()
                if not existing_code:
                    icd_rec = ICD10Code(
                        code=item["code"],
                        description=item["description"],
                        chapter=item.get("chapter"),
                        block=item.get("block"),
                        category=item.get("category"),
                        billable=item.get("billable", True),
                        excludes1=item.get("excludes1", []),
                        synonyms=item.get("synonyms", [])
                    )
                    db.add(icd_rec)
            db.commit()
            print(f"Seeded {len(codes_list)} ICD-10 reference codes.")

        # 3. Seed Demo Chart Document
        existing_doc = db.query(Document).filter_by(external_ref="DEMO-CHART-001").first()
        if not existing_doc:
            deid_text, raw_enc, phi_map_enc, summary = deidentify_text(DEMO_CHART_TEXT)
            demo_doc = Document(
                id=uuid.uuid4(),
                external_ref="DEMO-CHART-001",
                doc_type=DocType.DISCHARGE,
                raw_text_encrypted=raw_enc,
                deid_text=deid_text,
                phi_map_encrypted=phi_map_enc,
                status=DocStatus.RECEIVED,
                version=1,
                ocr_applied=False,
                ocr_low_confidence_count=0,
                created_at=datetime.utcnow()
            )
            db.add(demo_doc)
            db.commit()
            print(f"Seeded Demo Chart Document with ID: {demo_doc.id}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
