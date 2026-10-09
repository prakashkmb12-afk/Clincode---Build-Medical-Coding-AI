from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from clincode_api.db.session import get_db
from clincode_api.db.models import User
from clincode_api.schemas import LoginRequest, TokenResponse, UserResponse
from clincode_api.auth.jwt import verify_password, create_access_token
from clincode_api.auth.roles import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticates user credentials and returns JWT token."""
    user = db.query(User).filter_by(username=req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    token = create_access_token(data={"sub": str(user.id), "username": user.username, "role": user.role.value})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=str(user.id),
        username=user.username,
        role=user.role
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns details of currently authenticated user."""
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at
    )
