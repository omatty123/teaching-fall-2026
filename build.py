#!/usr/bin/env python3
"""
Build the Fall 2026 teaching site from data/.

    python3 build.py

Reads  : data/term.json + data/<slug>.json + features/<slug>.html + _kit/hq.css
Writes : index.html, courses/<slug>.html, favicon.svg

Nothing in this repo is hand-edited except data/, features/, and _kit/.
If a fact about a course is wrong on the site, it is wrong in data/.
"""

import html
import hashlib
import json
import pathlib
import re
import sys
import datetime

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
KIT = ROOT / "_kit"
FEATURES = ROOT / "features"
PRIVATE_OUT = ROOT / ".private-build"

# Week-grid geometry. Matches the hand-built grid these values replaced:
# HIST 10:25 landed at top:18px, FRST 11:10 at 49px, BUEN 12:40 at 112px.
PX_PER_MIN = 0.70
DAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAY_FULL = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
            "Thu": "Thursday", "Fri": "Friday"}

# Every course card renders this same set, in this same order, with these same
# labels. A course that does not have a destination yet simply omits that
# button — it never gets a different one, and never a dead link.
LINK_SLOTS = [
    ("syllabus", "Syllabus",        False),
    ("canvas",   "Canvas",          False),
    ("waterNews", "Water in the News", False),
    ("artwork",  "Artwork of the day", False),
    ("roster",   "Student roster", True),   # protected by Cloudflare Access
    ("people",   "Meet the class",  False),
]

DIRECTION_CONTRACT = """<!--
THESIS: The term site is an editorial threshold into seminar work: image, question, and next action arrive before administration.
OWN-WORLD: Charcoal utility rails, deep slate title fields, warm paper, compact Inter typography, Outfit controls, ochre signals, and documentary images with quiet white captions.
STORY: Recognize the course, meet its live question, enter the material, then consult the schedule and record.
FIRST VIEWPORT: A thin black course rail opens into a dark editorial title field; on the student index, three image-led course portraits begin immediately below it.
FORM: Seminar screen and course portrait system, adapted directly from the pinned Modern Korea dashboard and student-directory reference.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
-->"""

HQ_DIRECTION_CONTRACT = DIRECTION_CONTRACT.replace(
    "FIRST VIEWPORT: A slim masthead sits above four equal situation columns and one prioritized move; course dispatches begin before the fold ends.\n"
    "FORM: Field Desk situation ledger, grounded direction 7, seed e7d8328d.",
    "FIRST VIEWPORT: A compact term masthead gives way immediately to three course launch panels, with private name drills treated as primary teaching tools.\n"
    "FORM: Course-first teaching launchpad, adapted from the Spring 2026 Teaching Today reference within the Fall Field Desk system."
)


# ---------------------------------------------------------------- helpers

def e(value):
    """Escape a value for HTML text/attribute context."""
    return html.escape(str(value), quote=True)


def minutes(hhmm):
    """'10:25' -> 625"""
    hour, minute = hhmm.split(":")
    return int(hour) * 60 + int(minute)


def clock(mins):
    """600 -> '10:00', 780 -> '1:00' (12-hour, no meridiem)"""
    hour, minute = divmod(mins, 60)
    hour = hour - 12 if hour > 12 else hour
    return f"{hour}:{minute:02d}"


def format_course_date(iso):
    """Public course-page date label without a machine-like ISO string."""
    year, month, day = (int(part) for part in iso.split("-"))
    value = datetime.date(year, month, day)
    return value.strftime("%A, %B ") + str(value.day)


def load():
    term = json.loads((DATA / "term.json").read_text())
    courses = []
    for slug in term["courseOrder"]:
        course = json.loads((DATA / f"{slug}.json").read_text())
        m = course["meeting"]
        m["startMinutes"] = minutes(m["start"])
        m["endMinutes"] = minutes(m["end"])
        m["durationMinutes"] = m["endMinutes"] - m["startMinutes"]
        courses.append(course)
    return term, courses


def banner_style(course, rel=""):
    """background-image written straight onto the element.

    It must NOT go through a custom property: Chrome resolves a url() inside a
    custom property against the stylesheet that substitutes it, not the
    document, which silently breaks the relative path."""
    b = course["theme"].get("banner", {})
    if b.get("type") != "image":
        return ""
    return (f"background-image:url('{rel}{b['src']}');"
            f"background-position:{b.get('position', 'center')}")


def theme_vars(course, rel=""):
    """Inline custom properties that drive every themed rule in hq.css."""
    t = course["theme"]
    out = [f"--course-color:{t['color']}", f"--course-gradient:{t['gradient']}"]
    b = t.get("banner", {})
    if b.get("type") == "text":
        out.append(f"--banner-background:{b['background']}")
    return ";".join(out)


def head(term, *, title, description, og_image, rel="", og_path=""):
    """One head for every page. This is the deploy checklist, enforced in code."""
    base = term["baseUrl"].rstrip("/")
    css_version = hashlib.sha256((KIT / "hq.css").read_bytes()).hexdigest()[:10]
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<link rel="icon" type="image/svg+xml" href="{rel}favicon.svg">
<link rel="apple-touch-icon" href="{rel}images/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Teaching HQ">
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{base}/{og_path}">
<meta property="og:image" content="{base}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{base}/{og_image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}_kit/hq.css?v={css_version}">"""


# ---------------------------------------------------------------- week grid

def week_grid(term, courses):
    win_start = term["scheduleWindow"]["startMinutes"]
    win_end = term["scheduleWindow"]["endMinutes"]

    labels = []
    mark = win_start
    while mark <= win_end - 30:
        top = round((mark - win_start) * PX_PER_MIN)
        style = "top:0" if top == 0 else f"top:{top}px"
        labels.append(f'<span class="time-label" style="{style}">{clock(mark)}</span>')
        mark += 60

    desktop, mobile = [], []
    for day in DAY_ORDER:
        blocks, mobile_blocks = [], []
        for c in courses:
            if day not in c["meeting"]["days"]:
                continue
            m = c["meeting"]
            top = round((m["startMinutes"] - win_start) * PX_PER_MIN)
            height = round(m["durationMinutes"] * PX_PER_MIN)
            href = f"courses/{c['slug']}.html"
            style = f"--top:{top}px;--height:{height}px;--course-color:{c['theme']['color']}"
            blocks.append(
                f'<a class="class-block" style="{style}" href="{href}"'
                f' aria-label="{e(c["code"])}, {e(DAY_FULL[day])}, {e(m["timeLabel"])}, {e(m["location"])}">'
                f'<strong>{e(c["code"])}</strong>'
                f'<span>{clock(m["startMinutes"])}–{clock(m["endMinutes"])} · {e(m["shortLocation"])}</span></a>')
            mobile_blocks.append(
                f'<a class="mobile-block" style="--course-color:{c["theme"]["color"]}" href="{href}">'
                f'<b>{e(c["code"])}</b><span>{clock(m["startMinutes"])}–{clock(m["endMinutes"])}</span></a>')

        desktop.append(
            f'<div class="day-column"><div class="day-name">{day}</div>'
            f'<div class="day-track">{"".join(blocks)}</div></div>')
        inner = "".join(mobile_blocks) or '<span class="no-class">No meetings</span>'
        mobile.append(
            f'<div class="mobile-day"><strong>{DAY_FULL[day]}</strong><div>{inner}</div></div>')

    strip = "".join(
        f'<div class="term-date"><strong>{e(d["stripLabel"])}</strong>{e(d["stripNote"])}</div>'
        for d in term["dates"] if d.get("strip"))

    return f"""<div class="week-card">
  <div class="week-desktop" aria-label="{e(term['name'])} weekly block schedule">
    <div class="time-column">
      <div class="day-name" aria-hidden="true"></div>
      <div class="day-track" aria-hidden="true">{"".join(labels)}</div>
    </div>
    {"".join(desktop)}
  </div>
  <div class="week-mobile">{"".join(mobile)}</div>
  <div class="term-strip" aria-label="Key {e(term['name'].lower())} dates">{strip}</div>
</div>"""


# ---------------------------------------------------------------- HQ page

def public_links(course, *, rel="", instructor=False):
    links = [f'<a href="{rel}courses/{course["slug"]}.html">Course home</a>']
    slots = course.get("links", {})
    for key, label, private in LINK_SLOTS:
        href = slots.get(key)
        if not href or (private and not instructor):
            continue
        suffix = ' <span class="access-tag">Authenticated</span>' if private else ""
        links.append(f'<a href="{e(href)}">{e(label)}{suffix}</a>')
    return "".join(links)


def banner_figure(course, *, rel="", class_name="dispatch-image"):
    b = course["theme"].get("banner", {})
    if b.get("type") != "image":
        return f'<div class="{class_name} dispatch-image--text">{e(b.get("text", course["code"]))}</div>'
    credit = ""
    if b.get("credit"):
        if b.get("creditUrl"):
            credit = f'<figcaption><a href="{e(b["creditUrl"])}">{e(b["credit"])}</a></figcaption>'
        else:
            credit = f'<figcaption>{e(b["credit"])}</figcaption>'
    position = b.get("position", "center")
    return (f'<figure class="{class_name}"><img src="{e(rel + b["src"])}" '
            f'alt="{e(b.get("alt", ""))}" style="object-position:{e(position)}">{credit}</figure>')


def course_dispatch(course, *, rel="", instructor=False):
    m = course["meeting"]
    return f"""<article class="course-dispatch" id="{course['key']}Dispatch" style="{theme_vars(course)}">
  {banner_figure(course, rel=rel)}
  <div class="dispatch-identity">
    <h3>{e(course['title'])}</h3>
    <p class="course-code">{e(course['displayCode'])}</p>
    <p>{e(m['daysLabel'])} · {e(m['timeLabel'])}</p>
  </div>
  <div class="dispatch-session">
    <span>Next meeting</span>
    <strong id="{course['key']}Date">Loading schedule…</strong>
    <p id="{course['key']}Topic"></p>
  </div>
  <nav class="dispatch-links" aria-label="{e(course['code'])} destinations">{public_links(course, rel=rel, instructor=instructor)}</nav>
</article>"""


def course_launch_links(course):
    """First-viewport course actions for the private instructor HQ."""
    links = course.get("links", {})
    out = [
        f'<a class="launch-action" href="courses/{e(course["slug"])}.html">'
        '<span>Course page</span></a>'
    ]
    for key, label in (("syllabus", "Syllabus"), ("canvas", "Canvas"),
                       ("roster", "Learn the names"), ("waterNews", "Water in the News"),
                       ("artwork", "Artwork of the day")):
        if links.get(key):
            roster_class = " launch-action--roster" if key == "roster" else ""
            out.append(f'<a class="launch-action{roster_class}" href="{e(links[key])}"><span>{e(label)}</span></a>')
    return "".join(out)


def course_launch_panel(course):
    m = course["meeting"]
    return f"""<article class="course-launch" id="{course['key']}Dispatch" style="{theme_vars(course)}">
  {banner_figure(course, class_name="launch-image")}
  <div class="launch-body">
    <header class="launch-identity">
      <p class="course-code">{e(course['displayCode'])}</p>
      <h2>{e(course['title'])}</h2>
      <p>{e(m['daysLabel'])} · {e(m['timeLabel'])}<br>{e(m['location'])}</p>
    </header>
    <div class="launch-next">
      <span>Next meeting</span>
      <strong id="{course['key']}Date">Loading schedule…</strong>
      <p id="{course['key']}Topic"></p>
    </div>
  </div>
  <nav class="launch-actions" aria-label="{e(course['code'])} destinations">{course_launch_links(course)}</nav>
</article>"""


def build_hq(term, courses):
    launches = [course_launch_panel(c) for c in courses]
    config = {
        c["key"]: {
            "code": c["code"],
            "schedule": c["schedule"],
            "endMinutes": c["meeting"]["endMinutes"],
            "timeLabel": c["meeting"]["timeLabel"],
            "location": c["meeting"]["shortLocation"],
            "tasks": c["prep"]["tasks"],
            "build": c["prep"]["build"],
            "href": f"courses/{c['slug']}.html",
        } for c in courses
    }

    archive = term.get("archive")
    task_board = term.get("taskBoard", {})
    archive_html = ""
    nav_archive = ""
    if archive:
        archive_html = f"""
<section class="archive-section" aria-label="Previous terms">
  <div class="archive-link-card"><span>{e(archive['note'])}</span>
  <a href="{e(archive['href'])}">{e(archive['label'])}</a></div>
</section>"""
        nav_archive = f'<a href="{e(archive["href"])}">Previous term</a>'

    open_items = [item for item in task_board.get("items", []) if not item.get("done")]
    priority = next((item for item in open_items if item.get("lane") == "matty"), open_items[0] if open_items else None)
    completed = [item for item in task_board.get("items", []) if item.get("done")]
    priority_title = priority["title"] if priority else "Opening preparation is clear"
    priority_detail = priority["detail"] if priority else "No unresolved term decision is currently published here."
    changed = completed[-1]["title"] if completed else f"Public projection reviewed {task_board.get('updated', '')}"
    risk = priority_title if priority else "No blocking decision recorded"

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term,
      title=f"{term['name']} Teaching HQ",
      description="Next-class preparation, weekly schedule, and course links for "
                  f"{term['name']} at {term['institution']}.",
      og_image="images/hist-212-banner.jpg")}
</head>
<body class="hq-page">
{HQ_DIRECTION_CONTRACT}
<a class="skip-link" href="#courses">Skip to courses</a>
<header class="hq-launch-masthead">
  <div>
    <p id="dateLabel">Loading date…</p>
    <h1>Today’s Prep</h1>
    <p>Next class, prep queue, and the whole week</p>
  </div>
  <nav aria-label="Teaching HQ destinations">
    <a href="students.html">Student course index</a>
    <a href="#week">Weekly pattern</a>
    <a href="#decisions">Decision queue</a>
    {nav_archive}
  </nav>
</header>

<main class="hq-launch-main" id="main">
  <section class="course-launch-section" id="courses" aria-labelledby="coursesTitle">
    <div class="launch-heading">
      <div><p>Fall teaching desk</p><h2 id="coursesTitle">Your courses</h2></div>
      <p>Open a course—or practice the student names—without hunting.</p>
    </div>
    <div class="course-launch-grid">{"".join(launches)}</div>
  </section>

  <section class="teaching-brief" aria-labelledby="teachingBriefTitle">
    <h2 class="sr-only" id="teachingBriefTitle">Teaching brief</h2>
    <div><span>Today</span><strong id="nowTitle">Orienting…</strong><p id="nowDetail">Checking today’s teaching schedule.</p></div>
    <div><span>Next</span><strong id="nextTitle">Finding the next meeting…</strong><p id="nextDetail"></p></div>
    <div class="teaching-brief-priority"><span>Before the next class</span><strong id="priorityTask">{e(priority_title)}</strong><p>{e(priority_detail)}</p><a href="#decisions">Open decision queue</a></div>
  </section>

  <section class="week-section" id="week" aria-labelledby="weekTitle">
    <div class="section-heading"><h2 id="weekTitle">Recurring week</h2><p>{e(term['campus'])}</p></div>
    {week_grid(term, courses)}
  </section>

  <section class="decision-section" id="decisions" aria-labelledby="todoTitle">
    <details class="decision-disclosure">
      <summary><span><strong id="todoTitle">All term decisions</strong><small>{e(task_board.get('intro', ''))}</small></span><span id="todoCount">Loading queue…</span></summary>
      <div class="decision-body">
        <div class="todo-filters" id="todoFilters" role="group" aria-label="Filter the decision queue"></div>
        <div class="todo-list" id="todoList"></div>
        <p class="todo-storage-note">Personal checks stay in this browser. Course status files remain authoritative.</p>
        <div class="sr-only" id="todoAnnouncement" aria-live="polite"></div>
      </div>
    </details>
  </section>
</main>
<footer class="hq-launch-footer">
{archive_html}
  <span>{e(term['name'])} · {e(term['institution'])}</span>
</footer>
<script>
window.courseConfig = {json.dumps(config, ensure_ascii=False, indent=2)};
window.termName = {json.dumps(term['name'])};
window.taskBoardConfig = {json.dumps(task_board, ensure_ascii=False, indent=2)};
</script>
<script src="_kit/hq.js"></script>
</body>
</html>
"""
    PRIVATE_OUT.mkdir(exist_ok=True)
    (PRIVATE_OUT / "index.html").write_text(doc)
    return len(launches)


def build_student_index(term, courses):
    # Roster destinations are safe to expose as navigation because the roster
    # site itself is owner-only behind Cloudflare Access. No roster data is
    # embedded in this public page.
    dispatches = [course_dispatch(c, instructor=True) for c in courses]
    config = {c["key"]: {"code": c["code"], "schedule": c["schedule"],
              "endMinutes": c["meeting"]["endMinutes"], "tasks": [], "build": "",
              "href": f"courses/{c['slug']}.html"} for c in courses}
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term, title=f"{term['name']} Student Courses",
      description=f"Student course homes, schedules, syllabi, and Canvas links for {term['name']}.",
      og_image="images/frst-110-banner.jpg")}
</head>
<body class="student-index-page">
{DIRECTION_CONTRACT}
<a class="skip-link" href="#courses">Skip to courses</a>
<header class="student-masthead">
  <p>LAWRENCE UNIVERSITY · {e(term['name'])}</p>
  <h1>{e(term['name'])} Courses</h1>
  <span>Course pages, Canvas, syllabi, and the next meeting</span>
</header>
<main id="courses" class="student-index-main">
  <div class="dispatch-list student-dispatches">{"".join(dispatches)}</div>
</main>
<footer class="site-footer"><span>{e(term['name'])} · {e(term['institution'])}</span></footer>
<script>window.courseConfig = {json.dumps(config, ensure_ascii=False)}; window.termName = {json.dumps(term['name'])}; window.taskBoardConfig = {{"items": []}};</script>
<script src="_kit/hq.js"></script>
</body>
</html>"""
    (ROOT / "index.html").write_text(doc)
    (ROOT / "students.html").write_text(doc)


# ---------------------------------------------------------------- course page

def workspace_items(course):
    links = course.get("links", {})
    rows = [
        ("Canvas", "Assignments, announcements, and current course activity", links.get("canvas"), "Open Canvas"),
        ("Syllabus", "Policies, outcomes, assignments, and the term plan", links.get("syllabus") or course.get("syllabusUrl"), "Open syllabus"),
    ]
    if course.get("waterNewsPage"):
        rows.append((
            "Water in the News",
            "Share and browse current stories about water",
            course["waterNewsPage"],
            "Open the class current",
        ))
    if course.get("feature"):
        rows.append((
            "Water Makes Worlds",
            "Explore the course atlas, shared works, maps, and questions",
            f"{course['slug']}-atlas.html",
            "Open the course atlas",
        ))
    return [row for row in rows if row[2]]


def workspace_rows(course):
    out = []
    for label, detail, href, status in workspace_items(course):
        inner = (f'<div><h3>{e(label)}</h3><p>{e(detail)}</p></div>'
                 f'<span>{e(status)}</span>')
        out.append(f'<a class="workspace-row workspace-link" href="{e(href)}">{inner}</a>')
    return "".join(out)


def schedule_rows(items):
    rows = []
    for s in items:
        y, mth, d = s["date"].split("-")
        dt = datetime.date(int(y), int(mth), int(d))
        label = dt.strftime("%a %b ") + str(dt.day)
        flags = []
        if s.get("tentative"):
            flags.append('<em>transition to confirm</em>')
        if s.get("detail"):
            flags.append(e(s["detail"]))
        note = f'<span class="sched-note">{" · ".join(flags)}</span>' if flags else ""
        rows.append(f'<tr><th scope="row">{e(label)}</th><td>{e(s["topic"])}{note}</td></tr>')
    return "".join(rows)


def upcoming(course, limit=3):
    today = datetime.date.today().isoformat()
    future = [item for item in course["schedule"] if item["date"] >= today]
    return (future or course["schedule"][-limit:])[:limit]


def schedule_table(course):
    next_rows = upcoming(course, 3)
    return f"""<section class="course-schedule" aria-labelledby="sched-title">
  <div class="section-heading"><h2 id="sched-title">Coming meetings</h2><p>{len(course['schedule'])} total</p></div>
  <div class="sched-scroll"><table class="sched-table"><tbody>{schedule_rows(next_rows)}</tbody></table></div>
  <details class="full-schedule"><summary>View all {len(course['schedule'])} meetings</summary>
    <div class="sched-scroll"><table class="sched-table"><tbody>{schedule_rows(course['schedule'])}</tbody></table></div>
  </details>
</section>"""


def course_pattern(course):
    first = upcoming(course, 1)[0]
    if course["key"] == "hist":
        return ("Question and evidence", first["topic"],
                "Each meeting begins with a historical problem and tests it against sources, maps, and counterevidence.")
    if course["key"] == "buen":
        return ("Practice cycle", "Try → Reflect → Adjust",
                "Each Tuesday moves from a question to preparation, practice, an artifact, and a brief reflection.")
    return ("Current inquiry", first["topic"],
            "Close reading, shared works, seminar preparation, and writing move through the term’s water questions.")


def build_course(term, course):
    slug = course["slug"]
    m = course["meeting"]
    reg = course["registrar"]
    credits_label = reg.get("creditsLabel", f"{reg['credits']} credits")

    facts = [
        ("Instructor" + ("s" if len(reg["instructors"]) > 1 else ""), " · ".join(reg["instructors"])),
        ("Meets", f"{m['daysLabel']}<br>{m['timeLabel']}<br>{m['location']}"),
        ("Term", f"{term['startsLabel']}–{term['endsLabel']}"),
        ("Registrar record", f"{credits_label} · CRN {reg['crn']}"),
    ]
    if course.get("crossListed"):
        facts.append(("Cross-listed", course["crossListed"]))
    facts.append(("Class email", f'<a href="mailto:{reg["email"]}">{reg["email"]}</a>'))
    facts.append(("Grades due", term["gradesDue"]))
    facts_html = "".join(f"<div><dt>{e(k)}</dt><dd>{v}</dd></div>" for k, v in facts)

    og_image = course["theme"].get("banner", {}).get("src", "images/hist-212-banner.jpg")
    focus_label, focus_title, focus_copy = course_pattern(course)
    current = upcoming(course, 1)[0]
    current_label = format_course_date(current["date"])
    console_tools = "".join(
        f'<a href="{e(href)}">{e(label)}</a>'
        for label, _detail, href, _status in workspace_items(course)
    )
    notice = ""
    if course.get("unverified"):
        notice = """<aside class="course-notice" aria-label="Course information notice"><strong>Details are still being reconciled.</strong><p>Use the linked syllabus and Canvas course for current student instructions.</p></aside>"""

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term,
      title=f"{course['code']} · {course['title']}",
      description=course["description"],
      og_image=og_image,
      rel="../",
      og_path=f"courses/{slug}.html")}
<link rel="stylesheet" href="../_kit/course.css?v={hashlib.sha256((KIT / 'course.css').read_bytes()).hexdigest()[:10]}">
</head>
<body class="course-body-page" style="{theme_vars(course, rel="../")}">
{DIRECTION_CONTRACT}
<a class="skip-link" href="#course-main">Skip to course materials</a>
<header class="course-console">
  <nav class="breadcrumb"><a class="course-console-brand" href="../students.html"><span>{e(course['displayCode'])}</span><strong>{e(course['title'])}</strong></a></nav>
  <div class="course-console-meeting"><span>Next meeting</span><strong>{e(current_label)}</strong><a href="#schedule">All meetings</a></div>
  <nav class="course-console-tools" aria-label="Course tools">{console_tools}</nav>
</header>

<main class="course-dashboard" id="course-main">
  <section class="session-card" aria-labelledby="current-title">
    <header class="session-header">
      <div><h1 id="current-title">{e(current['topic'])}</h1><p>{e(current_label)}</p></div>
      <div class="session-meets"><span>{e(m['daysLabel'])}</span><strong>{e(m['timeLabel'])}</strong><span>{e(m['location'])}</span></div>
    </header>
    <div class="session-body">
      <div class="session-primary">
        {banner_figure(course, rel='../', class_name='session-art')}
        <div class="session-brief">
          <p class="course-lede">{e(course['description'])}</p>
          <p class="session-detail">{e(current.get('detail', 'Come ready to test the day’s question with evidence and conversation.'))}</p>
          <div class="course-pattern"><h2>{e(focus_title)}</h2><p class="pattern-context">{e(focus_label)}</p><p>{e(focus_copy)}</p></div>
        </div>
      </div>
      <aside class="session-next" aria-label="Coming meetings">
        <div class="section-heading"><h2>Coming next</h2><p>{len(course['schedule'])} meetings</p></div>
        <div class="sched-scroll"><table class="sched-table"><tbody>{schedule_rows(upcoming(course, 3))}</tbody></table></div>
      </aside>
    </div>
  </section>

  <section class="course-workspace" aria-labelledby="ws-title">
    <div class="section-heading"><h2 id="ws-title">Course tools</h2><p>Student destinations</p></div>
    <div class="workspace-list">{workspace_rows(course)}</div>
  </section>

  <div class="course-lower">
    <div class="course-primary">
      <div id="schedule">{schedule_table(course)}</div>
      <section class="final-callout" aria-labelledby="final-title">
        <div><h2 id="final-title">{e(course['final']['label'])}</h2>
        <p>{e(course['final']['day'])}, {e(course['final']['date'])}</p></div>
        <strong>{e(course['final']['time'])}</strong>
      </section>
    </div>
    <aside class="course-facts" aria-labelledby="facts-title">
      <h2 id="facts-title">Course record</h2>
      <dl>{facts_html}</dl>
{notice}
    </aside>
  </div>
</main>

<footer class="site-footer">
  <span>{e(course['code'])} · {e(term['name'])} · {e(term['institution'])}</span>
  <a href="../students.html">All student courses</a>
</footer>
</body>
</html>
"""
    (ROOT / "courses" / f"{slug}.html").write_text(doc)


def build_feature_page(term, course):
    feature_file = course.get("feature")
    if not feature_file:
        return False
    feature_path = FEATURES / feature_file
    if not feature_path.exists():
        print(f"  ! {course['slug']}: feature file {feature_file} missing, skipped")
        return False
    sheet = KIT / f"{course['slug']}-feature.css"
    feature_css = f'<link rel="stylesheet" href="../_kit/{sheet.name}">' if sheet.exists() else ""
    og_image = course["theme"].get("banner", {}).get("src", "images/frst-110-banner.jpg")
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term, title=f"Water Makes Worlds · {course['code']}", description=course['description'],
      og_image=og_image, rel="../", og_path=f"courses/{course['slug']}-atlas.html")}
<link rel="stylesheet" href="../_kit/course.css?v={hashlib.sha256((KIT / 'course.css').read_bytes()).hexdigest()[:10]}">{feature_css}
</head>
<body class="course-body-page course-atlas-page" style="{theme_vars(course, rel='../')}">
{DIRECTION_CONTRACT}
<nav class="breadcrumb"><a href="../students.html">Student courses</a><span class="crumb-sep">/</span><a href="{course['slug']}.html">{e(course['code'])}</a><span class="crumb-sep">/</span><span>Course atlas</span></nav>
<div class="course-feature">{feature_path.read_text()}</div>
<footer class="site-footer"><span>{e(course['code'])} course atlas · {e(term['name'])}</span><a href="{course['slug']}.html">{e(course['code'])} course home</a></footer>
</body>
</html>"""
    (ROOT / "courses" / f"{course['slug']}-atlas.html").write_text(doc)
    return True


def build_extra_page(term, course, page):
    """A standalone page that belongs to a course but is not the course page."""
    slug = page["slug"]
    frag_path = FEATURES / page["fragment"]
    if not frag_path.exists():
        print(f"  ! {slug}: fragment {page['fragment']} missing, skipped")
        return False

    sheet = KIT / f"{slug}.css"
    extra_css = ""
    if sheet.exists():
        version = hashlib.sha256(sheet.read_bytes()).hexdigest()[:10]
        extra_css = f'\n<link rel="stylesheet" href="../_kit/{sheet.name}?v={version}">'
    script = KIT / f"{slug}.js"
    extra_script = ""
    if script.exists():
        config = page.get("config", {})
        version = hashlib.sha256(script.read_bytes()).hexdigest()[:10]
        extra_script = (f'\n<script>window.pageConfig = '
                        f'{json.dumps(config, ensure_ascii=False)};</script>'
                        f'\n<script src="../_kit/{script.name}?v={version}"></script>')

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term,
      title=page["title"],
      description=page["description"],
      og_image=page.get("ogImage", "images/hist-212-banner.jpg"),
      rel="../",
      og_path=f"courses/{slug}.html")}
<link rel="stylesheet" href="../_kit/course.css?v={hashlib.sha256((KIT / 'course.css').read_bytes()).hexdigest()[:10]}">{extra_css}
</head>
<body class="course-body-page" style="{theme_vars(course, rel="../")}">
{DIRECTION_CONTRACT}
<nav class="breadcrumb">
  <a href="../students.html">{e(term['name'])} student courses</a>
  <span class="crumb-sep" aria-hidden="true">/</span>
  <a href="{course['slug']}.html">{e(course['code'])}</a>
</nav>

<div class="{e(page.get('wrapperClass', 'course-feature'))}">
{frag_path.read_text()}
</div>

<footer class="site-footer">
  <span>{e(course['code'])} &middot; {e(term['name'])} &middot; {e(term['institution'])}</span>
  <a href="{course['slug']}.html">{e(course['code'])} course page</a>
</footer>
{extra_script}
</body>
</html>
"""
    (ROOT / "courses" / f"{slug}.html").write_text(doc)
    return True


# ---------------------------------------------------------------- favicon

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="13" fill="#1d1d1f"/>
  <path d="M8 44c7 0 7-6 14-6s7 6 14 6 7-6 14-6 6 3 6 3" fill="none"
        stroke="#c59a37" stroke-width="3.4" stroke-linecap="round"/>
  <text x="32" y="31" font-family="-apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
        font-size="27" font-weight="600" fill="#ffffff" text-anchor="middle">마</text>
</svg>
"""


# ---------------------------------------------------------------- checks

def check(term, courses):
    """Return publication problems. Normal builds report; --strict blocks."""
    problems = []
    for c in courses:
        m = c["meeting"]
        if m["durationMinutes"] <= 0:
            problems.append(f"{c['slug']}: end time is not after start time")
        win = term["scheduleWindow"]
        if m["startMinutes"] < win["startMinutes"] or m["endMinutes"] > win["endMinutes"]:
            problems.append(f"{c['slug']}: {m['timeLabel']} falls outside the week-grid window")
        for d in m["days"]:
            if d not in DAY_ORDER:
                problems.append(f"{c['slug']}: unknown meeting day {d!r}")
        dates = [s["date"] for s in c["schedule"]]
        if dates != sorted(dates):
            problems.append(f"{c['slug']}: schedule dates are out of order")
        if len(dates) != len(set(dates)):
            problems.append(f"{c['slug']}: duplicate dates in schedule")
        for page in c.get("extraPages", []):
            if not (FEATURES / page["fragment"]).exists():
                problems.append(f"{c['slug']}: extra page {page['slug']} has no fragment")
        banner = c["theme"].get("banner", {})
        if banner.get("type") == "image" and not (ROOT / banner["src"]).exists():
            problems.append(f"{c['slug']}: banner image {banner['src']} not found")
        for note in c.get("unverified", []):
            problems.append(f"{c['slug']}: UNVERIFIED — {note}")
        for key, href in (c.get("links") or {}).items():
            if "chatgpt.site" in href:
                problems.append(f"{c['slug']}: GPT-SITE — {key} still points at {href}")
            elif "localhost" in href:
                problems.append(f"{c['slug']}: LOCAL-ONLY — {key} points at {href}")
        missing = [lbl for k, lbl, _ in LINK_SLOTS
                   if k in ("syllabus", "canvas") and not (c.get("links") or {}).get(k)]
        if missing:
            problems.append(f"{c['slug']}: no button for {', '.join(missing)} — add to links{{}} when ready")
    return problems


def main():
    term, courses = load()

    (ROOT / "favicon.svg").write_text(FAVICON)
    n = build_hq(term, courses)
    build_student_index(term, courses)
    extras = []
    atlases = []
    for c in courses:
        build_course(term, c)
        if build_feature_page(term, c):
            atlases.append(c)
        for page in c.get("extraPages", []):
            if build_extra_page(term, c, page):
                extras.append((c, page))

    print(f"built .private-build/index.html ({n} instructor course dispatches)")
    print(f"built index.html + students.html ({n} student course dispatches)")
    for c in courses:
        feat = " + feature" if c.get("feature") else ""
        print(f"built courses/{c['slug']}.html ({len(c['schedule'])} meetings{feat})")
    for c, page in extras:
        print(f"built courses/{page['slug']}.html ({c['code']} · {page['heading']})")
    for c in atlases:
        print(f"built courses/{c['slug']}-atlas.html ({c['code']} course atlas)")

    problems = check(term, courses)
    if problems:
        print("\ncheck:")
        for p in problems:
            print(f"  · {p}")
    else:
        print("\ncheck: clean")
    strict = "--strict" in sys.argv
    if strict and problems:
        print("\nstrict publication check failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
