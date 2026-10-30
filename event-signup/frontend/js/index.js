/** 首頁：UC2 列出可報名的活動清單 */
const listEl = document.getElementById("activity-list");
const openOnlyEl = document.getElementById("open-only");
const messageEl = document.getElementById("message");

function quotaText(a) {
  return a.capacity === null
    ? `已報名 ${a.registered_count} 人（不限名額）`
    : `已報名 ${a.registered_count} / ${a.capacity} 人`;
}

function renderActivity(a) {
  return `
    <article class="activity">
      <div class="activity-head">
        <h2>${escapeHtml(a.title)}</h2>
        <span class="status ${a.is_open ? "open" : "closed"}">${a.is_open ? "可報名" : "已截止或額滿"}</span>
      </div>
      <p class="desc">${escapeHtml(a.description)}</p>
      <dl>
        <dt>活動時間</dt><dd>${formatTime(a.event_time)}</dd>
        <dt>地點</dt><dd>${escapeHtml(a.location) || "未提供"}</dd>
        <dt>報名截止</dt><dd>${formatTime(a.deadline)}</dd>
        <dt>人數</dt><dd>${quotaText(a)}</dd>
      </dl>
      <div class="actions">
        ${a.is_open ? `<a class="button" href="register.html?id=${a.id}">報名</a>` : ""}
        <a class="button secondary" href="registrations.html?id=${a.id}">查看報名清單</a>
      </div>
    </article>`;
}

async function loadActivities() {
  messageEl.hidden = true;
  try {
    const activities = await API.listActivities(openOnlyEl.checked);
    listEl.innerHTML = activities.length
      ? activities.map(renderActivity).join("")
      : `<p class="empty">目前沒有活動。<a href="create.html">新增一個活動</a></p>`;
  } catch (err) {
    showMessage(messageEl, err.message);
  }
}

openOnlyEl.addEventListener("change", loadActivities);
loadActivities();
