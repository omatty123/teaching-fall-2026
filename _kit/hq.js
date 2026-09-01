/* Fall 2026 Field Desk runtime.
 * Generated markup owns the facts; this file only answers "what is next?"
 * and stores optional personal queue checks in this browser.
 */
(function () {
  "use strict";

  const DAY = 24 * 60 * 60 * 1000;
  const stateKey = "fall-2026-teaching-hq-task-state-v2";

  function localIso(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    return `${y}-${m}-${d}`;
  }

  function formatDate(iso, options) {
    const date = new Date(`${iso}T12:00:00`);
    return new Intl.DateTimeFormat("en-US", options || {
      weekday: "short", month: "short", day: "numeric"
    }).format(date);
  }

  function nextIndex(schedule, now, endMinutes) {
    const today = localIso(now);
    const minute = now.getHours() * 60 + now.getMinutes();
    let index = schedule.findIndex((meeting) =>
      meeting.date > today || (meeting.date === today && minute <= Number(endMinutes || 1440))
    );
    if (index < 0) index = schedule.length - 1;
    return Math.max(0, index);
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function taskBoardState() {
    let saved = {};
    try { saved = JSON.parse(localStorage.getItem(stateKey) || "{}"); } catch { saved = {}; }
    const sourceItems = (window.taskBoardConfig && taskBoardConfig.items) || [];
    return sourceItems.map((item) => ({
      ...item,
      done: Object.prototype.hasOwnProperty.call(saved, item.id) ? Boolean(saved[item.id]) : Boolean(item.done)
    }));
  }

  function renderCourse(key, now) {
    const config = courseConfig[key];
    if (!config || !config.schedule || !config.schedule.length) return null;
    const meeting = config.schedule[nextIndex(config.schedule, now, config.endMinutes)];
    const dateNode = document.getElementById(`${key}Date`);
    const topicNode = document.getElementById(`${key}Topic`);
    if (dateNode) dateNode.textContent = formatDate(meeting.date);
    if (topicNode) topicNode.textContent = meeting.topic || "Meeting details in the course home";
    return { key, config, meeting };
  }

  function refreshSituation(now, sessions) {
    const sorted = sessions.filter(Boolean).sort((a, b) => a.meeting.date.localeCompare(b.meeting.date));
    const today = localIso(now);
    const todaySessions = sorted.filter((item) => item.meeting.date === today);
    const next = sorted[0];
    const nowTitle = document.getElementById("nowTitle");
    const nowDetail = document.getElementById("nowDetail");
    const nextTitle = document.getElementById("nextTitle");
    const nextDetail = document.getElementById("nextDetail");

    if (nowTitle && nowDetail) {
      if (todaySessions.length) {
        nowTitle.textContent = `${todaySessions.length} course${todaySessions.length === 1 ? "" : "s"} meeting today`;
        nowDetail.textContent = todaySessions.map((item) => item.config.code).join(" · ");
      } else {
        nowTitle.textContent = "No course meeting today";
        nowDetail.textContent = "Use the priority move to prepare the next teaching day.";
      }
    }

    if (nextTitle && nextDetail && next) {
      nextTitle.textContent = `${next.config.code} · ${formatDate(next.meeting.date)}`;
      nextDetail.textContent = next.meeting.topic || "Open the course home for the current question.";
    }
  }

  function refreshQueueSummary(items) {
    const open = items.filter((item) => !item.done);
    const completed = items.filter((item) => item.done);
    const priority = open.find((item) => item.lane === "matty") || open[0];
    const risk = document.getElementById("riskTitle");
    const priorityNode = document.getElementById("priorityTask");
    const changed = document.getElementById("changedTitle");
    const count = document.getElementById("todoCount");
    if (risk) risk.textContent = priority ? priority.title : "No blocking decision recorded";
    if (priorityNode) priorityNode.textContent = priority ? priority.title : "Opening preparation is clear";
    if (changed && completed.length) changed.textContent = completed[completed.length - 1].title;
    if (count) count.textContent = `${open.length} open · ${completed.length} complete`;
  }

  function initTaskBoard() {
    const list = document.getElementById("todoList");
    const filters = document.getElementById("todoFilters");
    if (!list || !filters || !window.taskBoardConfig) return;

    const labels = Object.fromEntries(((taskBoardConfig.lanes || [])).map((lane) => [lane.id, lane.label]));
    const filterOptions = [
      ["open", "Open"],
      ...Object.keys(labels).map((key) => [key, labels[key]]),
      ["complete", "Completed"]
    ];
    let active = "open";

    function persist(items) {
      const snapshot = {};
      items.forEach((item) => { snapshot[item.id] = item.done; });
      localStorage.setItem(stateKey, JSON.stringify(snapshot));
    }

    function render() {
      const items = taskBoardState();
      filters.innerHTML = filterOptions.map(([key, label]) =>
        `<button type="button" data-filter="${escapeHtml(key)}" aria-pressed="${key === active}">${escapeHtml(label)}</button>`
      ).join("");

      const shown = items.filter((item) => {
        if (active === "open") return !item.done;
        if (active === "complete") return item.done;
        return item.lane === active;
      });

      list.innerHTML = shown.length ? shown.map((item) => `
        <article class="todo-item${item.done ? " is-done" : ""}">
          <div>
            <span class="todo-lane">${escapeHtml(labels[item.lane] || item.lane || "Term")}</span>
            <h3>${escapeHtml(item.title)}</h3>
            <p>${escapeHtml(item.detail || "")}</p>
          </div>
          <button type="button" data-task-id="${escapeHtml(item.id)}">${item.done ? "Reopen" : "Mark complete"}</button>
        </article>`).join("") : `<p class="todo-empty">Nothing in this view.</p>`;

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
      const items = taskBoardState();
      const item = items.find((entry) => entry.id === button.dataset.taskId);
      if (!item) return;
      item.done = !item.done;
      persist(items);
      render();
      const announcement = document.getElementById("todoAnnouncement");
      if (announcement) announcement.textContent = `${item.title} marked ${item.done ? "complete" : "open"}.`;
    });

    render();
  }

  function init() {
    const now = new Date();
    const dateLabel = document.getElementById("dateLabel");
    if (dateLabel) {
      dateLabel.textContent = new Intl.DateTimeFormat("en-US", {
        weekday: "long", month: "long", day: "numeric", year: "numeric"
      }).format(now);
    }
    const sessions = Object.keys(window.courseConfig || {}).map((key) => renderCourse(key, now));
    refreshSituation(now, sessions);
    initTaskBoard();
  }

  init();
}());
