/* Fall 2026 teaching clock and browser-local decision queue. */
(function () {
  "use strict";
  const stateKey = "fall-2026-teaching-hq-task-state-v2";
  const timeZone = "America/Chicago";
  let pendingChecks = {};

  function campusClock(date) {
    const parts = Object.fromEntries(new Intl.DateTimeFormat("en-CA", {
      timeZone, year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", hourCycle: "h23"
    }).formatToParts(date).map(({ type, value }) => [type, value]));
    return { date: `${parts.year}-${parts.month}-${parts.day}`, minute: Number(parts.hour) * 60 + Number(parts.minute) };
  }
  function formatDate(iso) {
    return new Intl.DateTimeFormat("en-US", {
      timeZone: "UTC", weekday: "short", month: "short", day: "numeric"
    }).format(new Date(`${iso}T12:00:00Z`));
  }
  function escapeHtml(value) {
    return String(value == null ? "" : value).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }
  function taskBoardState() {
    let saved = {};
    try {
      const parsed = JSON.parse(localStorage.getItem(stateKey) || "{}");
      if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) saved = parsed;
    } catch { /* Source defaults and unsaved checks remain usable. */ }
    const checks = { ...saved, ...pendingChecks };
    return ((window.taskBoardConfig && window.taskBoardConfig.items) || []).map((item) => ({
      ...item, done: Object.prototype.hasOwnProperty.call(checks, item.id) ? Boolean(checks[item.id]) : Boolean(item.done)
    }));
  }
  function renderCourse(key, clock) {
    const config = window.courseConfig[key];
    const schedule = config.schedule || [];
    const meeting = schedule.find((entry) => entry.date > clock.date ||
      (entry.date === clock.date && clock.minute < Number(config.endMinutes ?? 1440)));
    const date = document.getElementById(`${key}Date`);
    const topic = document.getElementById(`${key}Topic`);
    const label = document.getElementById(`${key}MeetingLabel`);
    if (label) label.textContent = meeting ? "Next meeting" : "Schedule status";
    if (date) date.textContent = meeting ? formatDate(meeting.date) : schedule.length ? "Term complete" : "Schedule unavailable";
    if (topic) topic.textContent = meeting ? meeting.topic || "Meeting details in the course home" :
      schedule.length ? "No further class meetings scheduled." : "Open the course page for the latest information.";
    return meeting ? { key, config, meeting } : null;
  }
  function refreshSchedule() {
    const now = new Date();
    const clock = campusClock(now);
    const config = window.courseConfig || {};
    const sessions = Object.keys(config).map((key) => renderCourse(key, clock)).filter(Boolean)
      .sort((a, b) => a.meeting.date.localeCompare(b.meeting.date) || Number(a.config.startMinutes || 0) - Number(b.config.startMinutes || 0));
    const today = sessions.filter((item) => item.meeting.date === clock.date);
    const next = sessions[0];
    const complete = Object.keys(config).length > 0 && Object.values(config).every((course) => (course.schedule || []).length) && !next;
    const setText = (id, value) => { const node = document.getElementById(id); if (node) node.textContent = value; };
    setText("dateLabel", new Intl.DateTimeFormat("en-US", {
      timeZone, weekday: "long", month: "long", day: "numeric", year: "numeric"
    }).format(now));
    setText("nowTitle", today.length ? `${today.length} course${today.length === 1 ? "" : "s"} still to meet today` : "No more course meetings today");
    setText("nowDetail", today.length ? today.map(({ config: c }) => `${c.code} · ${c.timeLabel} · ${c.location}`).join(" / ") :
      complete ? "All scheduled class meetings have finished." : "Check the next meeting and your term decisions below.");
    setText("nextTitle", next ? `${next.config.code} · ${formatDate(next.meeting.date)}` : complete ? "Term complete" : "No upcoming meeting listed");
    setText("nextDetail", next ? next.meeting.topic || "Open the course page for details." : "Course pages and resources remain available.");
    const agenda = document.getElementById("railAgenda");
    if (agenda) agenda.innerHTML = sessions.slice(0, 3).map(({ config: c, meeting }) =>
      `<a class="rail-agenda-item" href="${escapeHtml(c.href)}"><strong>${escapeHtml(c.code)} · ${escapeHtml(formatDate(meeting.date))}</strong><span>${escapeHtml(c.timeLabel)} · ${escapeHtml(c.location)}</span><small>${escapeHtml(meeting.topic)}</small></a>`
    ).join("");
  }
  function taskCourse(item) {
    return Object.values(window.courseConfig || {}).find((course) => course.code.split(" ")[0] === item.course);
  }
  function taskDestination(item) {
    const course = taskCourse(item);
    return item.href ? { href: item.href, label: item.linkLabel || "Open working document" } :
      course ? { href: course.href, label: `Open ${course.code}` } : { href: "#decisions", label: "Open decision queue" };
  }
  function refreshQueueSummary(items) {
    const open = items.filter((item) => !item.done);
    const priority = open.find((item) => item.lane === "matty") || open[0];
    const setText = (id, value) => { const node = document.getElementById(id); if (node) node.textContent = value; };
    setText("priorityTask", priority ? priority.title : "No open term decisions");
    setText("priorityDetail", priority ? priority.detail || "Open the decision queue for context." : "All decisions in this queue are marked complete.");
    setText("todoCount", `${open.length} open · ${items.length - open.length} complete`);
    const link = document.getElementById("priorityLink");
    if (link) {
      const destination = priority ? taskDestination(priority) : { href: "#decisions", label: "Review completed decisions" };
      link.href = destination.href;
      link.textContent = destination.label;
    }
  }
  function initTaskBoard() {
    const list = document.getElementById("todoList");
    const filters = document.getElementById("todoFilters");
    if (!list || !filters || !window.taskBoardConfig) return;
    const labels = Object.fromEntries((window.taskBoardConfig.lanes || []).map((lane) => [lane.id, lane.label]));
    const options = [["open", "All open"], ...Object.entries(labels), ["complete", "Completed"]];
    let active = "open";
    filters.innerHTML = options.map(([key, label]) => `<button type="button" data-filter="${escapeHtml(key)}" aria-pressed="${key === active}">${escapeHtml(label)}</button>`).join("");
    function render() {
      const items = taskBoardState();
      filters.querySelectorAll("button").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.filter === active)));
      const shown = items.filter((item) => active === "complete" ? item.done : !item.done && (active === "open" || item.lane === active));
      list.innerHTML = shown.length ? shown.map((item) => {
        const course = taskCourse(item);
        const destination = taskDestination(item);
        return `<article class="todo-item${item.done ? " is-done" : ""}"><div>
          <span class="todo-course">${escapeHtml(course ? course.code : "Across courses")}</span> · <span class="todo-lane">${escapeHtml(labels[item.lane] || "Term")}</span>
          <h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.detail || "")}</p>
          ${destination.href !== "#decisions" ? `<a class="todo-destination" href="${escapeHtml(destination.href)}">${escapeHtml(destination.label)}</a>` : ""}
          </div><button type="button" data-task-id="${escapeHtml(item.id)}">${item.done ? "Reopen" : "Mark complete"}</button></article>`;
      }).join("") : `<p class="todo-empty">${active === "complete" ? "No completed decisions yet." : "No open decisions in this view."}</p>`;
      refreshQueueSummary(items);
    }
    filters.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-filter]");
      if (!button) return;
      active = button.dataset.filter;
      render();
    });
    list.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-task-id]");
      if (!button) return;
      const buttons = Array.from(list.querySelectorAll("button[data-task-id]"));
      const index = buttons.indexOf(button);
      const items = taskBoardState();
      const item = items.find((entry) => entry.id === button.dataset.taskId);
      if (!item) return;
      item.done = !item.done;
      pendingChecks[item.id] = item.done;
      let saved = true;
      try {
        localStorage.setItem(stateKey, JSON.stringify(Object.fromEntries(items.map((entry) => [entry.id, entry.done]))));
        pendingChecks = {};
      } catch { saved = false; }
      const error = document.getElementById("todoStorageError");
      if (error) {
        error.hidden = saved;
        error.textContent = saved ? "" : "This check is kept in this tab but could not be saved. Allow browser storage before closing or reloading the page.";
      }
      render();
      const remaining = list.querySelectorAll("button[data-task-id]");
      (remaining[Math.min(index, remaining.length - 1)] || filters.querySelector(`[data-filter="${active}"]`))?.focus();
      const announcement = document.getElementById("todoAnnouncement");
      if (announcement) announcement.textContent = `${item.title} marked ${item.done ? "complete" : "open"}.${saved ? "" : " Not saved to browser storage."}`;
    });
    window.addEventListener("storage", (event) => { if (event.key === stateKey || event.key === null) render(); });
    render();
  }
  function renderNextUp() {
    const title = document.getElementById("nextUpTitle");
    if (!title) return;
    const parts = Object.fromEntries(new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Chicago", year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", hourCycle: "h23"
    }).formatToParts(new Date()).map(part => [part.type, part.value]));
    const today = `${parts.year}-${parts.month}-${parts.day}`;
    const minute = Number(parts.hour) * 60 + Number(parts.minute);
    const meetings = Object.values(window.courseConfig || {}).flatMap(config =>
      (config.schedule || []).map(meeting => ({config, meeting}))
    ).filter(({config, meeting}) => meeting.date > today ||
      (meeting.date === today && minute < config.endMinutes)
    ).sort((a, b) => a.meeting.date.localeCompare(b.meeting.date) ||
      a.config.startMinutes - b.config.startMinutes);
    const next = meetings[0];
    const meta = document.getElementById("nextUpMeta");
    const topic = document.getElementById("nextUpTopic");
    const link = document.getElementById("nextUpLink");
    if (!next) {
      title.textContent = "No upcoming classes";
      meta.textContent = "The scheduled meetings for this term are complete.";
      topic.textContent = "";
      link.textContent = "View schedule";
      link.href = "#week";
      return;
    }
    const {config, meeting} = next;
    const inProgress = meeting.date === today && minute >= config.startMinutes;
    title.textContent = `${config.code} · ${formatDate(meeting.date)}${inProgress ? " · In progress" : ""}`;
    meta.textContent = `${config.timeLabel} · ${config.location} · Central time`;
    topic.textContent = meeting.topic || "Meeting details in the course home";
    link.textContent = "Open course";
    link.href = config.href;
  }

  function openDecisions() {
    const disclosure = document.querySelector("#decisions details");
    if (disclosure) disclosure.open = true;
  }
  document.querySelectorAll('a[href="#decisions"]').forEach((link) => link.addEventListener("click", () => {
    if (link.getAttribute("href") === "#decisions") openDecisions();
  }));
  window.addEventListener("hashchange", () => { if (window.location.hash === "#decisions") openDecisions(); });
  if (window.location.hash === "#decisions") openDecisions();
  refreshSchedule();
  renderNextUp();
  if (document.getElementById("nextUpTitle")) window.setInterval(renderNextUp, 60000);
  initTaskBoard();
  document.addEventListener("visibilitychange", () => { if (!document.hidden) refreshSchedule(); });
  window.addEventListener("focus", refreshSchedule);
  window.setInterval(() => { if (!document.hidden) refreshSchedule(); }, 60000);
}());
