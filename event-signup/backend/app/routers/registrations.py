"""報名相關 API：UC3 送出報名、UC4 查看報名清單。"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Registration
from ..schemas import RegistrationCreate, RegistrationOut
from .activities import get_activity_or_404

router = APIRouter(prefix="/api/activities/{activity_id}/registrations", tags=["報名"])


@router.post("", response_model=RegistrationOut, status_code=status.HTTP_201_CREATED)
def create_registration(
    activity_id: int, data: RegistrationCreate, db: Session = Depends(get_db)
):
    """UC3 送出報名"""
    activity = get_activity_or_404(activity_id, db)

    if activity.is_expired:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "報名已截止")
    if activity.is_full:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "名額已滿")

    registration = Registration(activity_id=activity_id, **data.model_dump())
    db.add(registration)
    try:
        db.commit()
    except IntegrityError:  # 觸發 UNIQUE(activity_id, phone)
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "這支電話已經報名過此活動")
    db.refresh(registration)
    return registration


@router.get("", response_model=list[RegistrationOut])
def list_registrations(activity_id: int, db: Session = Depends(get_db)):
    """UC4 查看某活動的報名清單"""
    get_activity_or_404(activity_id, db)
    return db.scalars(
        select(Registration)
        .where(Registration.activity_id == activity_id)
        .order_by(Registration.created_at)
    ).all()
