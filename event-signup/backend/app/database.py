"""資料庫連線設定：使用 SQLite，資料檔 event.db 放在專案根目錄。"""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "event.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},  # SQLite 搭配 FastAPI 多執行緒需要
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI 依賴注入：每個請求取得一個 Session，結束後關閉。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
