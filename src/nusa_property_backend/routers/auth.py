import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, UserProfile
from ..auth import hash_password, verify_password, create_access_token, get_current_user
from ..schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    AuthResponseSchema,
    UserDataSchema,
    UserProfileSchema,
    UserUpdateProfileRequest,
)
from ..utils import format_rupiah

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def _build_user_data(user: User) -> UserDataSchema:
    profile_schema = None
    if user.profile:
        p = user.profile
        profile_schema = UserProfileSchema(
            id=p.id,
            name=p.name,
            greeting=p.greeting,
            subtitle=p.subtitle,
            plafonEstimate=p.plafon_estimate or 0,
            plafonEstimateFormatted=format_rupiah(p.plafon_estimate or 0),
            financialScore=p.financial_score,
            financialScoreGrade=p.financial_score_grade
        )

    return UserDataSchema(
        id=user.id,
        email=user.email,
        fullName=user.full_name,
        phone=user.phone,
        profile=profile_schema
    )


@router.post("/register", response_model=AuthResponseSchema, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar. Silakan gunakan email lain atau login."
        )

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    new_user = User(
        id=user_id,
        email=payload.email.strip().lower(),
        hashed_password=hash_password(payload.password),
        full_name=payload.fullName.strip(),
        phone=payload.phone.strip() if payload.phone else None
    )
    db.add(new_user)

    # Automatically create default KPR user profile
    profile_id = f"prof_{uuid.uuid4().hex[:12]}"
    new_profile = UserProfile(
        id=profile_id,
        user_id=user_id,
        name=payload.fullName.strip(),
        greeting="Halo",
        subtitle="Selamat datang di Nusa Property!",
        plafon_estimate=500_000_000,
        financial_score="Baik (A)",
        financial_score_grade="A"
    )
    db.add(new_profile)

    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.id, "email": new_user.email})
    return AuthResponseSchema(
        accessToken=token,
        tokenType="bearer",
        user=_build_user_data(new_user)
    )


@router.post("/login", response_model=AuthResponseSchema)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau kata sandi tidak sesuai."
        )

    token = create_access_token({"sub": user.id, "email": user.email})
    return AuthResponseSchema(
        accessToken=token,
        tokenType="bearer",
        user=_build_user_data(user)
    )


@router.get("/me", response_model=UserDataSchema)
def get_me(current_user: User = Depends(get_current_user)):
    return _build_user_data(current_user)


@router.put("/profile", response_model=UserDataSchema)
def update_profile(
    payload: UserUpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if payload.fullName is not None:
        current_user.full_name = payload.fullName.strip()
        if current_user.profile:
            current_user.profile.name = payload.fullName.strip()
    if payload.phone is not None:
        current_user.phone = payload.phone.strip()

    db.commit()
    db.refresh(current_user)
    return _build_user_data(current_user)
