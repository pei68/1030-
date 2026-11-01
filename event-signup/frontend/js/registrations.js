/** 報名清單頁：UC4 */
const id = getQueryId();
const titleEl = document.getElementById("activity-title");
const countEl = document.getElementById("registration-count");
const pinEl = document.getElementById("activity-pin");
const tbody = document.getElementById("registration-rows");
const messageEl = document.getElementById("message");

async function load() {
  try {
    const [activity, rows] = await Promise.all([API.getActivity(id), API.listRegistrations(id)]);
    titleEl.textContent = activity.title;
    pinEl.checked = activity.is_pinned;
    pinEl.disabled = false;
    countEl.textContent = activity.capacity === null
      ? `共 ${rows.length} 人報名`
      : `共 ${rows.length} / ${activity.capacity} 人報名`;
    tbody.innerHTML = rows.length
      ? rows.map((r, i) => `
          <tr>
            <td>${i + 1}</td>
            <td>${escapeHtml(r.name)}</td>
            <td>${escapeHtml(r.phone)}</td>
            <td>${formatTime(r.created_at)}</td>
          </tr>`).join("")
      : `<tr><td colspan="4" class="empty">還沒有人報名</td></tr>`;
  } catch (err) {
    showMessage(messageEl, err.message);
  }
}

pinEl.addEventListener("change", async () => {
  pinEl.disabled = true;
  messageEl.hidden = true;
  try {
    await API.setActivityPin(id, pinEl.checked);
  } catch (err) {
    pinEl.checked = !pinEl.checked;
    showMessage(messageEl, err.message);
  } finally {
    pinEl.disabled = false;
  }
});

load();
