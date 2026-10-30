"""建立範例資料，方便前端開發測試。

執行（在專案根目錄）：python -m backend.seed
"""
from datetime import datetime, timedelta

from .app.database import Base, SessionLocal, engine
from .app.models import Activity, Registration

Base.metadata.create_all(bind=engine)
now = datetime.now().replace(second=0, microsecond=0)

with SessionLocal() as db:
    if db.query(Activity).count() > 0:
        print("資料庫已有資料，略過建立範例資料。")
    else:
        hiking = Activity(
            title="大坑步道健行", description="早上集合，走 1 號步道，約 3 小時。",
            location="大坑風景區停車場", event_time=now + timedelta(days=10),
            deadline=now + timedelta(days=7), capacity=20,
        )
        workshop = Activity(
            title="手沖咖啡體驗", description="從磨豆到沖煮，器材現場提供。",
            location="社團辦公室", event_time=now + timedelta(days=5),
            deadline=now + timedelta(days=3), capacity=2,
        )
        old = Activity(
            title="上學期期末聚餐", description="已結束的活動，用來測試截止狀態。",
            location="學餐", event_time=now - timedelta(days=30),
            deadline=now - timedelta(days=35), capacity=None,
        )
        db.add_all([hiking, workshop, old])
        db.flush()
        db.add_all([
            Registration(activity_id=hiking.id, name="王小明", phone="0912345678"),
            Registration(activity_id=workshop.id, name="陳小華", phone="0922333444"),
            Registration(activity_id=workshop.id, name="林小美", phone="0933444555"),
        ])
        db.commit()
        print("已建立 3 筆活動、3 筆報名範例資料（手沖咖啡已額滿、期末聚餐已截止）。")
