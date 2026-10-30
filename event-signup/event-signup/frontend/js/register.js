/** 報名表頁：UC3 */
const id = getQueryId();
const infoEl = document.getElementById("activity-info");
const form = document.getElementById("register-form");
const messageEl = document.getElementById("message");

async function loadActivity() {
  try {
    const a = await API.getActivity(id);
    infoEl.innerHTML = `
      <h2>${escapeHtml(a.title)}</h2>
      <p>${formatTime(a.event_time)}｜${escapeHtml(a.location) || "地點未提供"}</p>
      <p>報名截止：${formatTime(a.deadline)}</p>`;
    if (!a.is_open) {
      form.hidden = true;
      showMessage(messageEl, "這個活動已截止或額滿，無法報名。");
    }
  } catch (err) {
    form.hidden = true;
    showMessage(messageEl, err.message);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const button = form.querySelector("button[type=submit]");
  button.disabled = true;
  try {
    await API.register(id, { name: fd.get("name"), phone: fd.get("phone") });
    form.hidden = true;
    showMessage(messageEl, "報名完成！", "success");
  } catch (err) {
    showMessage(messageEl, err.message);
    button.disabled = false;
  }
});

loadActivity();
