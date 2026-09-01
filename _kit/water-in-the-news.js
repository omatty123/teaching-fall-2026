(() => {
  const config = window.pageConfig || {};
  const stream = document.querySelector("#newsStream");
  const filters = document.querySelector("#newsFilters");
  const filterSelect = document.querySelector("#newsFilterSelect");
  const status = document.querySelector("#newsStatus");
  const submitLinks = [document.querySelector("#newsSubmit")];
  const fallback = Array.isArray(config.stories) ? config.stories : [];
  let stories = fallback;
  let active = "All";

  submitLinks.forEach(link => {
    if (link && config.formUrl) {
      link.href = config.formUrl;
      link.target = "_blank";
      link.rel = "noopener";
    }
  });

  function parseCsv(text) {
    const rows = [];
    let row = [], value = "", quoted = false;
    for (let i = 0; i < text.length; i += 1) {
      const char = text[i];
      if (char === '"' && quoted && text[i + 1] === '"') { value += '"'; i += 1; }
      else if (char === '"') quoted = !quoted;
      else if (char === "," && !quoted) { row.push(value); value = ""; }
      else if ((char === "\n" || char === "\r") && !quoted) {
        if (char === "\r" && text[i + 1] === "\n") i += 1;
        row.push(value); value = "";
        if (row.some(cell => cell.trim())) rows.push(row);
        row = [];
      } else value += char;
    }
    row.push(value);
    if (row.some(cell => cell.trim())) rows.push(row);
    if (rows.length < 2) return [];
    const headers = rows[0].map(cell => cell.trim().toLowerCase());
    return rows.slice(1).map(cells => Object.fromEntries(headers.map((header, i) => [header, (cells[i] || "").trim()])));
  }

  function safeUrl(value) {
    try {
      const url = new URL(value);
      return ["http:", "https:"].includes(url.protocol) ? url.href : "";
    } catch { return ""; }
  }

  function sourceName(value) {
    try { return new URL(value).hostname.replace(/^www\./, ""); }
    catch { return "Source"; }
  }

  function dateLabel(value) {
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? "Recently added" : new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", year: "numeric" }).format(date);
  }

  function render() {
    const visible = active === "All" ? stories : stories.filter(story => story.category === active);
    stream.replaceChildren();
    stream.setAttribute("aria-busy", "false");
    if (!visible.length) {
      const p = document.createElement("p"); p.className = "news-empty"; p.textContent = "No approved stories in this subject yet."; stream.append(p); return;
    }
    visible.forEach(story => {
      const href = safeUrl(story.url);
      if (!href) return;
      const article = document.createElement("article"); article.className = "news-story";
      const meta = document.createElement("div"); meta.className = "news-story-meta";
      const category = document.createElement("span"); category.className = "news-category"; category.textContent = story.category || "Other";
      const place = document.createElement("span"); place.className = "news-place"; place.textContent = story.place || "Place not specified";
      const date = document.createElement("time"); date.className = "news-date"; date.textContent = dateLabel(story.date); if (story.date) date.dateTime = story.date;
      meta.append(category, place, date);
      const title = document.createElement("div");
      const h3 = document.createElement("h3"); const a = document.createElement("a"); a.href = href; a.target = "_blank"; a.rel = "noopener"; a.textContent = story.headline || "Untitled story"; h3.append(a);
      const source = document.createElement("span"); source.className = "news-source"; source.textContent = sourceName(href); title.append(h3, source);
      const note = document.createElement("p"); note.className = "news-note"; note.textContent = story.note || "";
      article.append(meta, title, note); stream.append(article);
    });
  }

  function renderFilters() {
    const configured = Array.isArray(config.categories) ? config.categories : [];
    const categories = ["All", ...new Set([...configured, ...stories.map(story => story.category || "Other")])];
    filters.replaceChildren();
    if (filterSelect) filterSelect.replaceChildren();
    categories.forEach(label => {
      const button = document.createElement("button");
      button.type = "button"; button.className = "news-filter"; button.textContent = label;
      button.setAttribute("aria-pressed", String(label === active));
      button.addEventListener("click", () => { active = label; renderFilters(); render(); });
      filters.append(button);
      if (filterSelect) {
        const option = document.createElement("option");
        option.value = label; option.textContent = label; option.selected = label === active;
        filterSelect.append(option);
      }
    });
  }

  if (filterSelect) {
    filterSelect.addEventListener("change", () => {
      active = filterSelect.value; renderFilters(); render();
    });
  }

  async function load() {
    if (config.feedUrl) {
      try {
        const response = await fetch(config.feedUrl, { cache: "no-store" });
        if (!response.ok) throw new Error("feed unavailable");
        const fresh = parseCsv(await response.text()).filter(story => safeUrl(story.url));
        if (fresh.length) {
          stories = fresh;
          if (status) { status.textContent = `Live feed · ${fresh.length} approved ${fresh.length === 1 ? "story" : "stories"}`; status.dataset.state = "live"; }
        } else if (status) {
          status.textContent = "Cached approved stories · the live feed is currently empty";
          status.dataset.state = "cached";
        }
      } catch {
        stream.setAttribute("aria-label", "Live feed unavailable; showing the last approved stories.");
        if (status) { status.textContent = "Cached approved stories · live feed unavailable"; status.dataset.state = "cached"; }
      }
    } else if (status) {
      status.textContent = "Cached approved stories";
      status.dataset.state = "cached";
    }
    stories.sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));
    renderFilters(); render();
  }

  load();
})();
