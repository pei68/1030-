"""Pydantic 資料格式：負責驗證前端送來的資料，以及定義 API 回傳格式。"""
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

PHONE_PATTERN = re.compile(r"^0\d{8,9}$")  # 手機 09xxxxxxxx 或市話 0x-xxxxxxx(x)


# ---------- 活動 ----------
class ActivityCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    location: str = Field(default="", max_length=100)
    event_time: datetime
    deadline: datetime
    capacity: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def check_deadline(self):
        if self.deadline > self.event_time:
            raise ValueError("報名截止時間不能晚於活動時間")
        return self


class ActivityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    location: str
    event_time: datetime
    deadline: datetime
    capacity: int | None
    created_at: datetime
    registered_count: int
    is_open: bool


# ---------- 報名 ----------
class RegistrationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    phone: str

    @field_validator("phone")
    @classmethod
    def check_phone(cls, v: str) -> str:
        v = v.replace("-", "").replace(" ", "")
        if not PHONE_PATTERN.match(v):
            raise ValueError("電話格式不正確，請輸入 0 開頭的 9～10 碼數字")
        return v


class RegistrationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity_id: int
    name: str
    phone: str
    created_at: datetime
