/** 新增活動頁：UC1 */
const form = document.getElementById("create-form");
const messageEl = document.getElementById("message");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const payload = {
    title: fd.get("title"),
    description: fd.get("description"),
    location: fd.get("location"),
    event_time: fd.get("event_time"),
    deadline: fd.get("deadline"),
    capacity: fd.get("capacity") ? Number(fd.get("capacity")) : null,
  };

  const button = form.querySelector("button[type=submit]");
  button.disabled = true;
  try {
    await API.createActivity(payload);
    location.href = "index.html";
  } catch (err) {
    showMessage(messageEl, err.message);
    button.disabled = false;
  }
});
