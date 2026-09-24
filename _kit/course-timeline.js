// Timeline course home: recompute "next class", "due next", the open unit and
// past/next markers from the Chicago date on every visit, so the page never goes
// stale between builds. The static HTML already holds the build-time answer.
(function () {
  var el = document.getElementById("ft-data");
  if (!el) return;
  var data = JSON.parse(el.textContent);

  // "Now" in Chicago as sortable strings: "2026-09-25" and "2026-09-25T11:30"
  var parts = {};
  new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Chicago", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", hour12: false
  }).formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
  var today = parts.year + "-" + parts.month + "-" + parts.day;
  var now = today + "T" + (parts.hour === "24" ? "00" : parts.hour) + ":" + parts.minute;

  // a class stays "next" until it ends on its own day
  var next = data.schedule.filter(function (s) {
    return s.date > today || (s.date === today && now.slice(11) < data.classEnd);
  })[0] || data.schedule[data.schedule.length - 1];
  var due = data.assignments.filter(function (a) { return a.due > now; })[0]
    || data.assignments[data.assignments.length - 1];

  function longDate(iso) {
    var d = new Date(iso + "T12:00:00");
    return d.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
  }
  function dueDate(stamp) {
    var d = new Date(stamp);
    var day = d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" }).replace(",", "");
    var t = d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }).replace(":00", "").toLowerCase();
    return day + " · " + t;
  }
  function esc(s) { var t = document.createElement("span"); t.textContent = s; return t.innerHTML; }

  document.getElementById("ft-next-date").textContent = longDate(next.date);
  document.getElementById("ft-next-topic").textContent = next.topic;
  document.getElementById("ft-next-detail").textContent = next.detail || "";
  document.getElementById("ft-next-mats").innerHTML = (next.materials || []).map(function (m) {
    return '<a class="ft-chip ft-chip-' + esc(m.kind || "page") + '" href="' + esc(m.href) + '">' + esc(m.label) + "</a>";
  }).join("");
  document.getElementById("ft-due-link").href = due.href;
  document.getElementById("ft-due-label").textContent = due.label;
  document.getElementById("ft-due-when").textContent = dueDate(due.due);

  [].forEach.call(document.querySelectorAll(".ft-day"), function (li) {
    li.classList.toggle("is-past", li.dataset.date < next.date);
    li.classList.toggle("is-next", li.dataset.date === next.date);
  });
  [].forEach.call(document.querySelectorAll(".ft-unit"), function (u) {
    var current = u.dataset.start <= next.date && next.date <= u.dataset.end;
    u.classList.toggle("is-current", current);
    u.classList.toggle("is-done", u.dataset.end < next.date);
    if (current) u.open = true;
  });
  [].forEach.call(document.querySelectorAll(".ft-assign"), function (li) {
    li.classList.toggle("is-past", li.dataset.due <= now);
    li.classList.toggle("is-due", li.dataset.due === due.due);
  });
})();
