from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import datetime

router = APIRouter(prefix="/contact", tags=["Contact"])


class ContactSubmission(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class ContactResponse(BaseModel):
    status: str
    message: str
    timestamp: str


@router.post("", response_model=ContactResponse)
def submit_contact_form(req: ContactSubmission):
    """Processes contact form submission securely without exposing credentials."""
    if len(req.name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    if len(req.message.strip()) < 10:
        raise HTTPException(status_code=400, detail="Message must be at least 10 characters")

    # In production, this can send to SendGrid / AWS SES or log securely
    return ContactResponse(
        status="success",
        message="Thank you for contacting ClinCode. Your message has been received by our engineering team.",
        timestamp=datetime.utcnow().isoformat()
    )
