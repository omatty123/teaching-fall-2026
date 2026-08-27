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
}

init();
