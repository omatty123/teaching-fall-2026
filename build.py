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
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
KIT = ROOT / "_kit"
FEATURES = ROOT / "features"

# Week-grid geometry. Matches the hand-built grid these values replaced:
# HIST 10:25 landed at top:18px, FRST 11:10 at 49px, BUEN 12:40 at 112px.
PX_PER_MIN = 0.70
DAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAY_FULL = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
            "Thu": "Thursday", "Fri": "Friday"}


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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}_kit/hq.css">"""


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

def build_hq(term, courses):
    cards = []
    for c in courses:
        links = [f'<a href="courses/{c["slug"]}.html" class="header-link">Course page</a>']
        for link in c.get("links", []):
            cls = "header-link private" if link.get("private") else "header-link"
            lock = '<span aria-hidden="true">\u2022</span> ' if link.get("private") else ""
            if link.get("local"):
                cls += " local"
                title = ' title="Instructor only \u00b7 runs on your machine, start it with roster.command"'
            elif link.get("private"):
                title = ' title="Instructor only"'
            else:
                title = ""
            links.append(f'<a href="{e(link["href"])}" class="{cls}"{title}>'
                         f'{lock}{e(link["label"])}</a>')

        b = c["theme"].get("banner", {})
        if b.get("type") == "image":
            banner = (f'<div class="card-banner" data-banner="image" role="img"'
                      f' style="{banner_style(c)}"'
                      f' aria-label="{e(b.get("alt", ""))}"></div>')
        else:
            banner = f'<div class="card-banner" data-banner="text">{e(b.get("text", ""))}</div>'

        cards.append(f"""<article class="course-card" id="{c['key']}Card" style="{theme_vars(c)}">
  {banner}
  <div class="course-header">
    <div class="course-code">{e(c['displayCode'])}</div>
    <div class="course-name">{e(c['cardName'])}</div>
    <div class="header-links">{"".join(links)}</div>
  </div>
  <div class="session-info">
    <div class="class-date" id="{c['key']}Date"></div>
    <div class="class-topic" id="{c['key']}Topic"></div>
  </div>
  <div class="course-body" id="{c['key']}Body"></div>
</article>""")

    config = {
        c["key"]: {
            "schedule": c["schedule"],
            "endMinutes": c["meeting"]["endMinutes"],
            "tasks": c["prep"]["tasks"],
            "build": c["prep"]["build"],
        } for c in courses
    }

    archive = term.get("archive")
    archive_html = ""
    nav_archive = ""
    if archive:
        archive_html = f"""
<section class="archive-section" aria-label="Previous terms">
  <div class="archive-link-card"><span>{e(archive['note'])}</span>
  <a href="{e(archive['href'])}">{e(archive['label'])} →</a></div>
</section>"""
        nav_archive = f'<a href="{e(archive["href"])}">Archive</a>'

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term,
      title=f"{term['name']} Teaching HQ",
      description="Next-class preparation, weekly schedule, and course links for "
                  f"{term['name']} at {term['institution']}.",
      og_image="images/hist-212-banner.jpg")}
</head>
<body>
<header>
  <div class="date-label" id="dateLabel">Loading…</div>
  <h1 id="headerTitle">{e(term['name'])} Teaching HQ</h1>
  <div class="subtitle" id="headerSubtitle">Next class, prep queue, and the whole week</div>
  <nav class="hq-nav" aria-label="Teaching HQ">
    <a href="#courses">Course prep</a>
    <a href="#week">Week schedule</a>
    {nav_archive}
  </nav>
</header>

<section class="week-section" id="week" aria-labelledby="weekTitle">
  <div class="section-heading">
    <h2 id="weekTitle">Week at a glance</h2>
    <p>Recurring meetings · {e(term['campus'])}</p>
  </div>
  {week_grid(term, courses)}
</section>

<main class="container" id="courses">
{"".join(cards)}
</main>
{archive_html}
<script>
const courseConfig = {json.dumps(config, ensure_ascii=False, indent=2)};
const termName = {json.dumps(term['name'])};
</script>
<script src="_kit/hq.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(doc)
    return len(cards)


# ---------------------------------------------------------------- course page

def workspace_rows(course):
    rows = [
        ("Syllabus", "Course policies, outcomes, and term plan",
         course.get("syllabusUrl"), "Open syllabus" if course.get("syllabusUrl") else "Ready for materials"),
        ("Class sessions", "Daily plans, slides, activities, and preparation", None,
         f"{len(course['schedule'])} meetings scheduled"),
        ("Attendance", "Roster and class-meeting record", None, "Ready for materials"),
        ("Resources", "Readings, handouts, media, and reference material", None,
         f"{len(course['currentWorks']['items'])} current works added"
         if course.get("currentWorks") else "Ready for materials"),
    ]
    out = []
    for label, detail, href, status in rows:
        inner = (f'<div><h3>{e(label)}</h3><p>{e(detail)}</p></div>'
                 f'<span>{e(status)}{" ↗" if href else ""}</span>')
        if href:
            out.append(f'<a class="workspace-row workspace-link" href="{e(href)}">{inner}</a>')
        else:
            out.append(f'<div class="workspace-row">{inner}</div>')
    return "".join(out)


def schedule_table(course):
    rows = []
    for s in course["schedule"]:
        y, mth, d = s["date"].split("-")
        import datetime
        dt = datetime.date(int(y), int(mth), int(d))
        label = dt.strftime("%a %b ") + str(dt.day)
        flags = []
        if s.get("tentative"):
            flags.append('<em>transition to confirm</em>')
        if s.get("detail"):
            flags.append(e(s["detail"]))
        note = f'<span class="sched-note">{" · ".join(flags)}</span>' if flags else ""
        rows.append(f'<tr><th scope="row">{e(label)}</th><td>{e(s["topic"])}{note}</td></tr>')
    return f"""<section class="course-schedule" aria-labelledby="sched-title">
  <div class="section-heading"><h2 id="sched-title">Meeting schedule</h2>
  <p>{len(course['schedule'])} meetings</p></div>
  <div class="sched-scroll"><table class="sched-table"><tbody>{"".join(rows)}</tbody></table></div>
</section>"""


def build_course(term, course):
    slug = course["slug"]
    m = course["meeting"]
    reg = course["registrar"]

    facts = [
        ("Instructor" + ("s" if len(reg["instructors"]) > 1 else ""), " · ".join(reg["instructors"])),
        ("Meets", f"{m['daysLabel']}<br>{m['timeLabel']}<br>{m['location']}"),
        ("Term", f"{term['startsLabel']}–{term['endsLabel']}"),
        ("Credits · CRN", f"{reg['credits']} · {reg['crn']}"),
    ]
    if course.get("crossListed"):
        facts.append(("Cross-listed", course["crossListed"]))
    facts.append(("Class email", f'<a href="mailto:{reg["email"]}">{reg["email"]}</a>'))
    facts.append(("Grades due", term["gradesDue"]))
    facts_html = "".join(f"<div><dt>{e(k)}</dt><dd>{v}</dd></div>" for k, v in facts)

    feature_html = ""
    feature_css = ""
    feature_file = course.get("feature")
    if feature_file:
        path = FEATURES / feature_file
        if path.exists():
            feature_html = f'<div class="course-feature">{path.read_text()}</div>'
        else:
            print(f"  ! {slug}: feature file {feature_file} missing, skipped")
        sheet = KIT / f"{slug}-feature.css"
        if sheet.exists():
            feature_css = f'\n<link rel="stylesheet" href="../_kit/{sheet.name}">'

    og_image = course["theme"].get("banner", {}).get("src", "images/hist-212-banner.jpg")

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term,
      title=f"{course['code']} · {course['title']}",
      description=course["description"],
      og_image=og_image,
      rel="../",
      og_path=f"courses/{slug}.html")}
<link rel="stylesheet" href="../_kit/course.css">{feature_css}
</head>
<body class="course-body-page" style="{theme_vars(course, rel="../")}">
<nav class="breadcrumb"><a href="../index.html">← Back to {e(term['name'])} Teaching HQ</a></nav>

<header class="course-hero">
  <div class="course-hero-art" data-banner="{e(course['theme'].get('banner', {}).get('type', 'text'))}" style="{banner_style(course, '../')}"></div>
  <div class="course-hero-copy">
    <p class="course-code">{e(course['displayCode'])}</p>
    <h1>{e(course['title'])}</h1>
    <p class="course-lede">{e(course['description'])}</p>
    <div class="course-meeting-lockup">
      <span>{e(m['daysLabel'])}</span>
      <strong>{e(m['timeLabel'])}</strong>
      <span>{e(m['location'])}</span>
    </div>
  </div>
</header>

{feature_html}

<main class="course-main">
  <div class="course-primary">
    <section class="course-workspace" aria-labelledby="ws-title">
      <div class="section-heading"><h2 id="ws-title">Course workspace</h2>
      <p>Ready to fill as the term develops</p></div>
      <div class="workspace-list">{workspace_rows(course)}</div>
    </section>

    {schedule_table(course)}

    <section class="final-callout" aria-labelledby="final-title">
      <div><h2 id="final-title">{e(course['final']['label'])}</h2>
      <p>{e(course['final']['day'])}, {e(course['final']['date'])}</p></div>
      <strong>{e(course['final']['time'])}</strong>
    </section>
  </div>

  <aside class="course-facts" aria-labelledby="facts-title">
    <h2 id="facts-title">Course details</h2>
    <dl>{facts_html}</dl>
  </aside>
</main>

<footer class="site-footer">
  <span>{e(course['code'])} · {e(term['name'])} · {e(term['institution'])}</span>
  <a href="../index.html">← {e(term['name'])} Teaching HQ</a>
</footer>
</body>
</html>
"""
    (ROOT / "courses" / f"{slug}.html").write_text(doc)


def build_extra_page(term, course, page):
    """A standalone page that belongs to a course but is not the course page."""
    slug = page["slug"]
    frag_path = FEATURES / page["fragment"]
    if not frag_path.exists():
        print(f"  ! {slug}: fragment {page['fragment']} missing, skipped")
        return False

    sheet = KIT / f"{slug}.css"
    extra_css = f'\n<link rel="stylesheet" href="../_kit/{sheet.name}">' if sheet.exists() else ""

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(term,
      title=page["title"],
      description=page["description"],
      og_image=page.get("ogImage", "images/hist-212-banner.jpg"),
      rel="../",
      og_path=f"courses/{slug}.html")}
<link rel="stylesheet" href="../_kit/course.css">{extra_css}
</head>
<body class="course-body-page" style="{theme_vars(course, rel="../")}">
<nav class="breadcrumb">
  <a href="../index.html">&larr; Back to {e(term['name'])} Teaching HQ</a>
  <span class="crumb-sep" aria-hidden="true">/</span>
  <a href="{course['slug']}.html">{e(course['code'])}</a>
</nav>

<div class="{e(page.get('wrapperClass', 'course-feature'))}">
{frag_path.read_text()}
</div>

<footer class="site-footer">
  <span>{e(course['code'])} &middot; {e(term['name'])} &middot; {e(term['institution'])}</span>
  <a href="{course['slug']}.html">&larr; {e(course['code'])} course page</a>
</footer>
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
    """Deploy checklist, run every build. Warnings only, never blocks."""
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
        for link in c.get("links", []):
            if "chatgpt.site" in link["href"]:
                note = link.get("pendingMigration", "still hosted on chatgpt.site")
                problems.append(f"{c['slug']}: GPT-SITE — {link['label']} — {note}")
            elif link.get("local"):
                problems.append(
                    f"{c['slug']}: LOCAL-ONLY — {link['label']} points at "
                    f"{link['href']}; works only while roster.command is running. "
                    "Swap for the hosted URL once Cloudflare Access is onboarded.")
    return problems


def main():
    term, courses = load()

    (ROOT / "favicon.svg").write_text(FAVICON)
    n = build_hq(term, courses)
    extras = []
    for c in courses:
        build_course(term, c)
        for page in c.get("extraPages", []):
            if build_extra_page(term, c, page):
                extras.append((c, page))

    print(f"built index.html ({n} course cards)")
    for c in courses:
        feat = " + feature" if c.get("feature") else ""
        print(f"built courses/{c['slug']}.html ({len(c['schedule'])} meetings{feat})")
    for c, page in extras:
        print(f"built courses/{page['slug']}.html ({c['code']} · {page['heading']})")

    problems = check(term, courses)
    if problems:
        print("\ncheck:")
        for p in problems:
            print(f"  · {p}")
    else:
        print("\ncheck: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
