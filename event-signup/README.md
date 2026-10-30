# 廢墟版活動報名平台（基本款）

FastAPI + SQLite + HTML/CSS/JS 的活動報名系統。

## 功能（Use Case）

| 編號 | 角色 | 功能 | 頁面 |
|---|---|---|---|
| UC1 | 主辦者 | 新增活動 | `create.html` |
| UC2 | 參加者 | 瀏覽可報名活動清單 | `index.html` |
| UC3 | 參加者 | 填寫報名表（姓名、連絡電話）並送出 | `register.html?id=活動編號` |
| UC4 | 主辦者 | 查看活動的報名清單 | `registrations.html?id=活動編號` |

「可報名」的定義：尚未超過報名截止時間，且報名人數未達名額上限（名額空白表示不限）。

## 環境需求

Python 3.10 以上

## 安裝與啟動

```bash
# 1. 建立並啟用虛擬環境
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 2. 安裝套件
pip install -r requirements.txt

# 3.（選用）建立範例資料
python -m backend.seed

# 4. 啟動伺服器（在專案根目錄執行）
uvicorn backend.app.main:app --reload
```

啟動後開啟：

- 網站：http://127.0.0.1:8000
- API 文件（可直接測試 API）：http://127.0.0.1:8000/docs

想清空資料，關閉伺服器後刪除根目錄的 `event.db`，重新啟動即可。

## 專案結構

```
event-signup/
├── backend/
│   ├── seed.py              # 範例資料
│   └── app/
│       ├── main.py          # 進入點：掛載 API 與前端頁面
│       ├── database.py      # SQLite 連線
│       ├── models.py        # 資料表（activities、registrations）
│       ├── schemas.py       # 輸入驗證與輸出格式
│       └── routers/
│           ├── activities.py
│           └── registrations.py
├── frontend/
│   ├── index.html / create.html / register.html / registrations.html
│   ├── css/style.css        # 樣式
│   └── js/
│       ├── api.js           # 共用 API 呼叫與工具函式
│       └── index.js / create.js / register.js / registrations.js
├── docs/
└── requirements.txt
```

## 資料庫

**activities**：id、title、description、location、event_time、deadline、capacity（可空）、created_at

**registrations**：id、activity_id（FK）、name、phone、created_at；UNIQUE(activity_id, phone)

## API

| 方法 | 路徑 | 說明 | 錯誤 |
|---|---|---|---|
| POST | `/api/activities` | 新增活動 | 422 欄位錯誤 |
| GET | `/api/activities?open=true` | 活動清單（open=true 只列可報名） | |
| GET | `/api/activities/{id}` | 單一活動 | 404 |
| POST | `/api/activities/{id}/registrations` | 送出報名 | 404、400 已截止或額滿、409 重複報名、422 |
| GET | `/api/activities/{id}/registrations` | 報名清單 | 404 |

## 修改畫面注意事項（給前端組員）

`.html` 與 `css/style.css` 可以自由改版面與樣式，但 JS 是透過下列 **id** 找到元素，改版時請保留這些 id（可以換位置、換標籤外觀）：

| 頁面 | 必須保留的 id | 用途 |
|---|---|---|
| 全部頁面 | `message` | 顯示成功／錯誤訊息（需帶 `hidden` 屬性） |
| index.html | `activity-list`、`open-only` | 活動清單容器、「只顯示可報名」勾選框 |
| create.html | `create-form` | 表單，內含 name 為 title、description、location、event_time、deadline、capacity 的欄位 |
| register.html | `activity-info`、`register-form` | 活動資訊區、表單（內含 name 為 name、phone 的欄位） |
| registrations.html | `activity-title`、`registration-count`、`registration-rows` | 活動名稱、人數、表格的 tbody |

活動卡片與表格列的 HTML 是由 `js/index.js` 的 `renderActivity()` 與 `js/registrations.js` 產生，要改卡片結構請改這兩個地方。
