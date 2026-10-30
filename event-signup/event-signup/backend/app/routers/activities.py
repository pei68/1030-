"""活動相關 API：UC1 新增活動、UC2 列出活動、UC3 取得單一活動。"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Activity
from ..schemas import ActivityCreate, ActivityOut

router = APIRouter(prefix="/api/activities", tags=["活動"])


def get_activity_or_404(activity_id: int, db: Session) -> Activity:
    activity = db.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "找不到這個活動")
    return activity


@router.post("", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(data: ActivityCreate, db: Session = Depends(get_db)):
    """UC1 新增活動"""
    activity = Activity(**data.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.get("", response_model=list[ActivityOut])
def list_activities(open: bool = False, db: Session = Depends(get_db)):
    """UC2 列出活動；open=true 時只列出可報名的活動"""
    activities = db.scalars(select(Activity).order_by(Activity.event_time)).all()
    if open:
        activities = [a for a in activities if a.is_open]
    return activities


@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """UC3 報名表上方顯示的活動資訊"""
    return get_activity_or_404(activity_id, db)
