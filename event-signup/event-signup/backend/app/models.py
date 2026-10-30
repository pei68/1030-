"""資料表定義：activities（活動）與 registrations（報名），一對多。"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, default="")
    location: Mapped[str] = mapped_column(String(100), default="")
    event_time: Mapped[datetime] = mapped_column(DateTime)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)  # None = 不限名額
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="activity", cascade="all, delete-orphan"
    )

    @property
    def registered_count(self) -> int:
        return len(self.registrations)

    @property
    def is_full(self) -> bool:
        return self.capacity is not None and self.registered_count >= self.capacity

    @property
    def is_expired(self) -> bool:
        return datetime.now() >= self.deadline

    @property
    def is_open(self) -> bool:
        """可報名 = 尚未截止 且 尚未額滿。"""
        return not self.is_expired and not self.is_full


class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = (
        # 同一活動不可用同一支電話重複報名
        UniqueConstraint("activity_id", "phone", name="uq_activity_phone"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"))
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    activity: Mapped[Activity] = relationship(back_populates="registrations")
