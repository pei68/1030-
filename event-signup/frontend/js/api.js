/**
 * api.js：所有頁面共用的 API 呼叫與小工具。
 * 修改畫面時通常不需要改這個檔案。
 */
const API = {
  async request(path, options = {}) {
    const res = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const data = await res.json().catch(() => null);
    if (!res.ok) throw new Error(formatError(data));
    return data;
  },

  listActivities(openOnly = true) {
    return this.request(`/api/activities?open=${openOnly}`);
  },
  getActivity(id) {
    return this.request(`/api/activities/${id}`);
  },
  createActivity(payload) {
    return this.request("/api/activities", { method: "POST", body: JSON.stringify(payload) });
  },
  register(activityId, payload) {
    return this.request(`/api/activities/${activityId}/registrations`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
  listRegistrations(activityId) {
    return this.request(`/api/activities/${activityId}/registrations`);
  },
};

/** 把後端錯誤（字串或 422 驗證錯誤陣列）轉成可讀訊息 */
function formatError(data) {
  if (!data || !data.detail) return "發生錯誤，請稍後再試";
  if (typeof data.detail === "string") return data.detail;
  return data.detail
    .map((e) => String(e.msg).replace(/^Value error, /, ""))
    .join("；");
}

/** "2026-11-05T14:00:00" → "2026/11/05 14:00" */
function formatTime(iso) {
  const d = new Date(iso);
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}/${pad(d.getMonth() + 1)}/${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

/** 從網址 ?id=3 取得活動 id */
function getQueryId() {
  return new URLSearchParams(location.search).get("id");
}

/** 防止使用者輸入的文字被當成 HTML 執行 */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text ?? "";
  return div.innerHTML;
}

/** 在指定元素顯示訊息，type 為 "success" 或 "error" */
function showMessage(el, text, type = "error") {
  el.textContent = text;
  el.className = `message ${type}`;
  el.hidden = false;
}
