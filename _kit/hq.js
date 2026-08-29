/* Teaching HQ — next-session logic.
   Expects `courseConfig` and `termName` to be defined by the page (build.py emits them
   from data/*.json). Nothing here knows the name of any particular course. */

function localIso(now) {
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
}

function formatDate(value) {
  return new Date(value + "T12:00:00").toLocaleDateString("en-US", {
    weekday: "long", month: "long", day: "numeric",
  });
}

function nextIndex(schedule, now, endMinutes) {
  const today = localIso(now);
  const minutes = now.getHours() * 60 + now.getMinutes();
  return schedule.findIndex(
    (item) => item.date > today || (item.date === today && minutes < endMinutes)
  );
}

function taskMarkup(key, session, tasks) {
  return tasks
    .map((task, index) => {
      const storageKey = `${termName}:${key}:${session.date}:${index}`;
      let checked = false;
      try {
        checked = localStorage.getItem(storageKey) === "done";
      } catch (_) {}
      return `<label class="task-item"><input type="checkbox" data-storage-key="${storageKey}" ${
        checked ? "checked" : ""
      }><span>${task}</span></label>`;
    })
    .join("");
}

function renderCourse(key, now) {
  const config = courseConfig[key];
  const index = nextIndex(config.schedule, now, config.endMinutes);
  const session = index >= 0 ? config.schedule[index] : null;
  const upNext =
    index >= 0 && index + 1 < config.schedule.length ? config.schedule[index + 1] : null;
  const dateEl = document.getElementById(`${key}Date`);
  const topicEl = document.getElementById(`${key}Topic`);
  const bodyEl = document.getElementById(`${key}Body`);
  if (!dateEl || !topicEl || !bodyEl) return null;

  if (!session) {
    dateEl.textContent = termName;
    topicEl.textContent = "Regular meetings complete";
    bodyEl.innerHTML = `<div class="no-class">The course page remains available above.</div>`;
    return null;
  }

  dateEl.textContent =
    formatDate(session.date) + (session.tentative ? " · transition to confirm" : "");
  topicEl.textContent = session.topic;

  let html = session.detail ? `<div class="session-detail">${session.detail}</div>` : "";
  html += `<div class="section-title">Before class</div><div class="task-list">${taskMarkup(
    key, session, config.tasks
  )}</div>`;
  html += `<div class="build-note"><strong>Term build:</strong> ${config.build}</div>`;
  if (upNext) {
    html += `<div class="up-next"><div class="up-next-label">Up next</div><div class="up-next-date">${formatDate(
      upNext.date
    )}</div><div class="up-next-topic">${upNext.topic}</div></div>`;
  }
  bodyEl.innerHTML = html;
  return { key, session };
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function taskBoardState(task) {
  const storageKey = `${termName}:term-board:${task.id}`;
  try {
    const saved = localStorage.getItem(storageKey);
    if (saved !== null) return saved === "done";
  } catch (_) {}
  return Boolean(task.done);
}

function initTaskBoard() {
  const list = document.getElementById("todoList");
  const filters = document.getElementById("todoFilters");
  if (!list || !filters || !taskBoardConfig || !Array.isArray(taskBoardConfig.items)) return;

  const lanes = Array.isArray(taskBoardConfig.lanes) ? taskBoardConfig.lanes : [];
  const laneMap = Object.fromEntries(lanes.map((lane) => [lane.id, lane]));
  let activeLane = "all";

  filters.innerHTML = [
    { id: "all", label: "All tasks", tone: "all" },
    ...lanes,
  ].map((lane) => `<button class="todo-filter todo-filter--${escapeHtml(lane.tone || lane.id)}" type="button" data-lane="${escapeHtml(lane.id)}" aria-pressed="${lane.id === "all"}">${escapeHtml(lane.label)}</button>`).join("");

  function render() {
    const visible = taskBoardConfig.items.filter((task) => activeLane === "all" || task.lane === activeLane);
    list.innerHTML = visible.map((task) => {
      const done = taskBoardState(task);
      const lane = laneMap[task.lane] || { label: task.lane, tone: "neutral" };
      return `<article class="todo-item ${done ? "is-done" : ""}" data-tone="${escapeHtml(lane.tone)}">
        <div class="todo-item-copy">
          <div class="todo-meta"><span class="course-chip" data-course="${escapeHtml(task.course)}">${escapeHtml(task.course)}</span><span>${escapeHtml(lane.label)}</span><span>${Number(task.points) || 0} pts</span></div>
          <h3>${escapeHtml(task.title)}</h3>
          <p>${escapeHtml(task.detail)}</p>
        </div>
        <button class="todo-action" type="button" data-task-id="${escapeHtml(task.id)}" aria-label="${done ? "Reopen" : "Complete"} ${escapeHtml(task.title)}">${done ? "Reopen" : `Done +${Number(task.points) || 0}`}</button>
      </article>`;
    }).join("");

    const totalPoints = taskBoardConfig.items.reduce((sum, task) => sum + (Number(task.points) || 0), 0);
    const completed = taskBoardConfig.items.filter(taskBoardState);
    const completedPoints = completed.reduce((sum, task) => sum + (Number(task.points) || 0), 0);
    const percent = totalPoints ? Math.round((completedPoints / totalPoints) * 100) : 0;
    const score = document.getElementById("todoScore");
    const progress = document.getElementById("todoProgress");
    const track = progress && progress.parentElement;
    const count = document.getElementById("todoCount");
    if (score) score.textContent = `${percent}%`;
    if (progress) progress.style.transform = `scaleX(${percent / 100})`;
    if (track) track.setAttribute("aria-valuenow", String(percent));
    if (count) count.textContent = `${completed.length} of ${taskBoardConfig.items.length} tasks · ${completedPoints} points banked`;
  }

  filters.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-lane]");
    if (!button) return;
    activeLane = button.dataset.lane;
    filters.querySelectorAll("button").forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
    render();
  });

  list.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-task-id]");
    if (!button) return;
    const task = taskBoardConfig.items.find((item) => item.id === button.dataset.taskId);
    if (!task) return;
    const nextState = !taskBoardState(task);
    try {
      localStorage.setItem(`${termName}:term-board:${task.id}`, nextState ? "done" : "open");
    } catch (_) {}
    const announcement = document.getElementById("todoAnnouncement");
    if (announcement) announcement.textContent = `${task.title} ${nextState ? "completed" : "reopened"}.`;
    render();
  });

  render();
}

function init() {
  const now = new Date();
  const dateLabel = document.getElementById("dateLabel");
  if (dateLabel) {
    dateLabel.textContent = now.toLocaleDateString("en-US", {
      weekday: "long", month: "long", day: "numeric", year: "numeric",
    });
  }

  const nextSessions = Object.keys(courseConfig)
    .map((key) => renderCourse(key, now))
    .filter(Boolean);
  nextSessions.sort((a, b) => a.session.date.localeCompare(b.session.date));

  const subtitle = document.getElementById("headerSubtitle");
  if (subtitle) {
    if (nextSessions.length) {
      const nextDate = nextSessions[0].session.date;
      const labels = nextSessions
        .filter((item) => item.session.date === nextDate)
        .map((item) => item.key.toUpperCase())
        .join(" + ");
      subtitle.textContent = `Next teaching day · ${formatDate(nextDate)} · ${labels}`;
    } else {
      subtitle.textContent = "Regular meetings complete";
    }
  }

  document.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement) || !target.dataset.storageKey) return;
    try {
      localStorage.setItem(target.dataset.storageKey, target.checked ? "done" : "open");
    } catch (_) {}
  });

  initTaskBoard();
}

init();
