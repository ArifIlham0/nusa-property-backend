from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import UserProfile, Notification, User
from ..schemas import UserProfileSchema, NotificationSchema
from ..utils import format_rupiah
from ..auth import security, decode_access_token

router = APIRouter(prefix="/api", tags=["User & Notifications"])


@router.get("/user/profile", response_model=UserProfileSchema)
def get_user_profile(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    profile = None
    if credentials and credentials.credentials:
        payload = decode_access_token(credentials.credentials)
        if payload and "sub" in payload:
            user = db.query(User).filter(User.id == payload["sub"]).first()
            if user and user.profile:
                profile = user.profile

    if not profile:
        profile = db.query(UserProfile).first()

    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return UserProfileSchema(
        id=profile.id,
        name=profile.name,
        greeting=profile.greeting,
        subtitle=profile.subtitle,
        plafonEstimate=profile.plafon_estimate or 0,
        plafonEstimateFormatted=format_rupiah(profile.plafon_estimate or 0),
        financialScore=profile.financial_score,
        financialScoreGrade=profile.financial_score_grade
    )


@router.get("/notifications", response_model=List[NotificationSchema])
def get_notifications(db: Session = Depends(get_db)):
    notifs = db.query(Notification).order_by(Notification.id.desc()).all()
    return notifs
