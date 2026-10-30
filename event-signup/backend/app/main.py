"""程式進入點：建立資料表、掛載 API 路由與前端靜態頁面。

啟動（在專案根目錄）：uvicorn backend.app.main:app --reload
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import activities, registrations

Base.metadata.create_all(bind=engine)  # 第一次啟動時自動建立 event.db 與資料表

app = FastAPI(title="廢墟版活動報名平台", version="0.1.0")

app.include_router(activities.router)
app.include_router(registrations.router)

# 前端頁面：必須放在 API 路由之後掛載，否則 "/" 會攔截所有請求
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
