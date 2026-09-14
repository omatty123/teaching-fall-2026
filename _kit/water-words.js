(function () {
  "use strict";

  var cfg = window.pageConfig || {};
  var words = cfg.words || [];
  var svg = document.getElementById("wwWheel");
  var famList = document.getElementById("wwFamilies");
  var credits = document.getElementById("wwCredits");
  if (!svg || !words.length) return;

  var NS = "http://www.w3.org/2000/svg";
  var C = 500;
  var R_BAND = 238, R_DOT = 258, R_TEXT = 274, R_OUT = 498, R_CORE = 214;
  var GAP = 1.2; // empty slots between families

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function html(tag, cls, parent) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (parent) parent.appendChild(n);
    return n;
  }
  function pt(r, deg) {
    var a = (deg - 90) * Math.PI / 180;
    return [C + r * Math.cos(a), C + r * Math.sin(a)];
  }
  function arc(r, a0, a1) {
    var p0 = pt(r, a0), p1 = pt(r, a1);
    return "M" + p0[0].toFixed(2) + " " + p0[1].toFixed(2) +
      " A" + r + " " + r + " 0 " + (a1 - a0 > 180 ? 1 : 0) + " 1 " +
      p1[0].toFixed(2) + " " + p1[1].toFixed(2);
  }
  function wedge(r0, r1, a0, a1) {
    var p0 = pt(r0, a0), p1 = pt(r1, a0), p2 = pt(r1, a1), p3 = pt(r0, a1);
    return "M" + p0 + " L" + p1 + " A" + r1 + " " + r1 + " 0 0 1 " + p2 +
      " L" + p3 + " A" + r0 + " " + r0 + " 0 0 0 " + p0 + " Z";
  }

  // ---- families, in ring order
  var families = [];
  var byFam = {};
  words.forEach(function (w) {
    if (!byFam[w.family]) { byFam[w.family] = { name: w.family, words: [] }; families.push(byFam[w.family]); }
    byFam[w.family].words.push(w);
  });
  families.forEach(function (f, i) {
    var hue = Math.round(205 + i * 137.508) % 360;
    f.color = "hsl(" + hue + " 50% " + (i % 2 ? 37 : 45) + "%)";
  });

  // ---- geometry
  var units = words.length + families.length * GAP;
  var step = 360 / units;
  var cursor = GAP / 2;
  families.forEach(function (f) {
    f.a0 = cursor * step;
    f.words.forEach(function (w) { w.angle = (cursor + 0.5) * step; cursor += 1; });
    f.a1 = cursor * step;
    cursor += GAP;
  });

  // ---- center
  var core = el("g", { class: "ww-center" }, svg);
  el("circle", { class: "ww-core", cx: C, cy: C, r: R_CORE }, core);
  var ripples = [1, 2, 3].map(function (n) {
    return el("circle", { class: "ww-ripple r" + n, cx: C, cy: C, r: R_CORE - 6 }, core);
  });
  var cWord = el("text", { class: "ww-c-word", x: C, y: C - 22 }, core);
  var cRoman = el("text", { class: "ww-c-roman", x: C, y: C + 50 }, core);
  var cLang = el("text", { class: "ww-c-lang", x: C, y: C + 92 }, core);
  var cFam = el("text", { class: "ww-c-fam", x: C, y: C + 120 }, core);
  var cCue = el("g", { class: "ww-c-cue" }, core);
  var cCueIcon = el("path", { d: "" }, cCue);
  var cCueText = el("text", { x: C + 12, y: C - 132 }, cCue);
  core.setAttribute("tabindex", "0");
  core.setAttribute("role", "button");

  function fitCenter() {
    cWord.style.fontSize = "";
    var max = R_CORE * 1.62;
    var len = cWord.getComputedTextLength ? cWord.getComputedTextLength() : 0;
    if (len > max) cWord.style.fontSize = Math.floor(88 * max / len) + "px";
  }
  function setCenter(w) {
    if (!w) {
      cWord.textContent = "water";
      cRoman.textContent = "";
      cLang.textContent = words.length + " languages";
      cFam.textContent = "click a word";
      core.style.removeProperty("--c");
      fitCenter();
      return;
    }
    core.style.setProperty("--c", w.color);
    cWord.textContent = w.word;
    cRoman.textContent = w.roman || "";
    cLang.textContent = w.lang;
    cFam.textContent = w.branch ? w.family + " · " + w.branch : w.family;
    fitCenter();
  }

  // ---- ring
  var bandLayer = el("g", {}, svg);
  var wordLayer = el("g", {}, svg);
  families.forEach(function (f) {
    f.band = el("path", { class: "ww-band", d: arc(R_BAND, f.a0 + step * 0.15, f.a1 - step * 0.15), stroke: f.color }, bandLayer);
    f.words.forEach(function (w) {
      w.color = f.color;
      var g = el("g", {
        class: "ww-word", tabindex: "0", role: "button",
        "aria-label": w.lang + ": " + w.word + (w.roman ? " (" + w.roman + ")" : "")
      }, wordLayer);
      g.style.setProperty("--c", f.color);
      el("path", { class: "ww-hit", d: wedge(R_BAND - 14, R_OUT, w.angle - step / 2, w.angle + step / 2) }, g);
      var d = pt(R_DOT, w.angle);
      el("circle", { class: "ww-dot", cx: d[0].toFixed(2), cy: d[1].toFixed(2), r: 3.5 }, g);

      var left = w.angle > 180;
      var t = el("text", {
        transform: "translate(" + C + " " + C + ") rotate(" + (left ? w.angle + 90 : w.angle - 90).toFixed(3) + ")",
        x: left ? -R_TEXT : R_TEXT, y: 0, "text-anchor": left ? "end" : "start"
      }, g);
      var ws = el("tspan", { class: "ww-w" });
      ws.textContent = w.word;
      var ls = el("tspan", { class: "ww-l" });
      ls.textContent = w.lang;
      if (left) { ls.setAttribute("dx", "0"); t.appendChild(ls); ws.setAttribute("dx", "9"); t.appendChild(ws); }
      else { t.appendChild(ws); ls.setAttribute("dx", "9"); t.appendChild(ls); }

      w.node = g;
      g.addEventListener("click", function () { stopQueue(); play(w); });
      g.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); stopQueue(); play(w); }
      });
    });
  });

  // ---- families list
  families.forEach(function (f) {
    var li = html("li", "ww-fam", famList);
    li.style.setProperty("--c", f.color);
    var name = html("span", "ww-fam-name", li);
    name.textContent = f.name;
    var count = html("small", "", name);
    count.textContent = f.words.length;
    if (f.words.length > 1) {
      var b = html("button", "ww-fam-play", li);
      b.type = "button";
      b.textContent = "Play all";
      b.setAttribute("aria-pressed", "false");
      b.setAttribute("aria-label", "Play all " + f.name + " words");
      b.addEventListener("click", function () {
        if (queueFam === f) { stopQueue(); return; }
        startQueue(f);
      });
      f.button = b;
    } else {
      var one = html("button", "ww-fam-play", li);
      one.type = "button";
      one.textContent = "Play";
      one.setAttribute("aria-label", "Play " + f.words[0].lang + ": " + f.words[0].word);
      one.addEventListener("click", function () { stopQueue(); play(f.words[0]); });
      f.button = one;
    }
    // the whole row is a target; the button carries keyboard access
    li.addEventListener("click", function (ev) {
      if (ev.target.closest("button")) return;
      f.button.click();
    });
    f.row = li;
    var chips = html("div", "ww-chips", li);
    f.words.forEach(function (w) {
      var c = html("button", "ww-chip", chips);
      c.type = "button";
      c.textContent = w.word;
      c.title = w.lang;
      c.setAttribute("aria-label", w.lang + ": " + w.word);
      c.addEventListener("click", function () { stopQueue(); play(w); });
      w.chip = c;
    });
  });

  // ---- credits
  if (credits) {
    words.forEach(function (w) {
      var li = html("li", "", credits);
      var b = html("b", "", li);
      b.textContent = w.lang + " ";
      li.appendChild(document.createTextNode(w.word + " · " + (w.speaker || "unnamed speaker") + " · "));
      var lic = html("a", "", li);
      lic.href = w.licenseUrl || w.source;
      lic.textContent = w.license;
      li.appendChild(document.createTextNode(" · "));
      var src = html("a", "", li);
      src.href = w.source;
      src.textContent = "source";
    });
  }

  // ---- playback
  var audio = new Audio();
  audio.preload = "none";
  var current = null, queue = [], queueFam = null, gapTimer = null;

  function mark(w) {
    words.forEach(function (x) {
      var on = x === w;
      x.node.classList.toggle("is-on", on);
      if (x.chip) x.chip.classList.toggle("is-on", on);
    });
    families.forEach(function (f) {
      var lit = !!w && f.name === w.family;
      f.band.classList.toggle("is-lit", lit);
      f.row.classList.toggle("is-lit", lit);
    });
  }
  function ripple() {
    ripples.forEach(function (r) {
      r.classList.remove("go");
      void r.getBoundingClientRect();
      r.classList.add("go");
    });
  }
  function setCue(touring) {
    cCueText.textContent = touring ? "stop" : (resumeAt ? "continue" : "play all");
    var tw = cCueText.getComputedTextLength ? cCueText.getComputedTextLength() : 80;
    var x0 = C - (13 + 7 + tw) / 2, y = C - 132;
    cCueIcon.setAttribute("d", touring
      ? "M" + x0 + " " + (y - 6.5) + "h13v13h-13z"
      : "M" + x0 + " " + (y - 7.5) + "l13 7.5l-13 7.5z");
    cCueText.setAttribute("x", x0 + 20);
    cCueText.setAttribute("y", y);
    core.setAttribute("aria-label", touring ? "Pause"
      : resumeAt ? "Continue around the circle from " + words[resumeAt].lang
      : "Play all " + words.length + " words around the circle");
    core.classList.toggle("is-touring", touring);
  }
  var TOUR = { name: "circle", words: words };
  var resumeAt = 0, gapPending = false;
  function toggleTour() {
    if (queueFam === TOUR) {
      // pause: pick up with the word that was cut off, or the next one if it had finished
      resumeAt = (words.indexOf(current) + (gapPending ? 1 : 0)) % words.length;
      audio.pause();
      stopQueue();
      return;
    }
    stopQueue();
    queueFam = TOUR;
    setCue(true);
    queue = words.slice(resumeAt);
    play(queue.shift());
  }
  core.addEventListener("click", toggleTour);
  core.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); toggleTour(); }
  });

  function play(w) {
    current = w;
    gapPending = false;
    if (queueFam !== TOUR) { resumeAt = words.indexOf(w); setCue(false); }
    mark(w);
    setCenter(w);
    ripple();
    audio.src = w.audio;
    var p = audio.play();
    if (p && p.catch) p.catch(function () {});
  }
  function startQueue(f) {
    stopQueue();
    queueFam = f;
    f.button.setAttribute("aria-pressed", "true");
    f.button.textContent = "Stop";
    queue = f.words.slice();
    play(queue.shift());
  }
  function stopQueue() {
    clearTimeout(gapTimer);
    gapPending = false;
    queue = [];
    if (queueFam === TOUR) setCue(false);
    if (queueFam && queueFam.button) {
      queueFam.button.setAttribute("aria-pressed", "false");
      queueFam.button.textContent = "Play all";
    }
    queueFam = null;
  }
  audio.addEventListener("ended", function () {
    if (queue.length) {
      gapPending = true;
      gapTimer = setTimeout(function () { play(queue.shift()); }, 350);
    } else if (queueFam) {
      if (queueFam === TOUR) resumeAt = 0;
      stopQueue();
    }
  });

  setCenter(null);
  setCue(false);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { setCenter(current); setCue(queueFam === TOUR); });
})();
