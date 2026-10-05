"""Render deterministic packed circles with area proportional to word count."""
import html
import json
import math


def _pack(words):
    """Greedily fill the nearest available tangent positions around the center."""
    placed = []
    gap = 3.0
    # Keep the smallest displayed circle readable at either reading scope.
    # Areas remain proportional to exact counts within each chart.
    radius_scale = 36.0 / math.sqrt(min((int(item['count']) for item in words), default=4))
    for item in words:
        radius = radius_scale * math.sqrt(int(item['count']))
        if not placed:
            placed.append((0.0, 0.0, radius))
            continue
        candidates = []
        # Cardinal tangencies guarantee candidates even with one existing circle.
        for x, y, r in placed:
            distance = r + radius + gap
            for angle in range(0, 360, 15):
                theta = math.radians(angle)
                candidates.append((x + distance * math.cos(theta), y + distance * math.sin(theta)))
        # Intersections of inflated boundaries give compact, exact tangencies.
        for i, (ax, ay, ar) in enumerate(placed):
            a_radius = ar + radius + gap
            for bx, by, br in placed[i + 1:]:
                b_radius = br + radius + gap
                dx, dy = bx - ax, by - ay
                distance = math.hypot(dx, dy)
                if distance < 1e-9 or distance > a_radius + b_radius or distance < abs(a_radius - b_radius):
                    continue
                along = (a_radius * a_radius - b_radius * b_radius + distance * distance) / (2 * distance)
                high = math.sqrt(max(0.0, a_radius * a_radius - along * along))
                cx, cy = ax + along * dx / distance, ay + along * dy / distance
                candidates.extend(((cx - high * dy / distance, cy + high * dx / distance), (cx + high * dy / distance, cy - high * dx / distance)))
        valid = [(x, y) for x, y in candidates if all(math.hypot(x - px, y - py) >= radius + pr + gap - 1e-7 for px, py, pr in placed)]
        if not valid:
            edge = max(math.hypot(x, y) + r for x, y, r in placed)
            valid = [(edge + radius + gap, 0.0)]
        sum_x, sum_y = sum(p[0] for p in placed), sum(p[1] for p in placed)
        x, y = min(valid, key=lambda p: (round(math.hypot(*p) + radius, 7), (sum_x + p[0]) ** 2 + (sum_y + p[1]) ** 2, math.atan2(p[1], p[0])))
        placed.append((x, y, radius))
    return placed


def _label_layout(word, radius):
    """Keep large labels; use normal word divisions for the two long labels."""
    lines = {'something': ('some', 'thing'), 'weather': ('weath', 'er')}.get(word, (word,))
    baselines = (-8.0, 10.0) if len(lines) == 2 else (-2.0,)
    # Conservative advance estimates for Source Sans 3's bold lowercase forms.
    advances = {'a': .53, 'b': .55, 'c': .47, 'd': .55, 'e': .50,
                'f': .35, 'g': .52, 'h': .56, 'i': .28, 'j': .28,
                'k': .52, 'l': .28, 'm': .87, 'n': .55, 'o': .56,
                'p': .55, 'q': .55, 'r': .39, 's': .43, 't': .37,
                'u': .55, 'v': .50, 'w': .82, 'x': .50, 'y': .48, 'z': .47}
    size = 22.0
    while size > 12.0:
        fits = True
        for line, baseline in zip(lines, baselines):
            half_width = sum(advances.get(char, .62) for char in line.lower()) * size * .525
            vertical = max(abs(baseline - size * .75), abs(baseline + size * .25))
            if math.hypot(half_width, vertical) > radius - 1.0:
                fits = False
                break
        if fits:
            break
        size -= .1
    # Leave room for the rendered bold font's full glyph bounds.
    # Browser verification keeps every word at least 18 screen pixels.
    return lines, baselines, size * .91


def render_graph(data, minimum_word_pixels=None, id_prefix=None, title=None):
    """Keep the builder interface; all chart content is native, static SVG."""
    esc = lambda value: html.escape(str(value), quote=True)
    section_id = f'words-{id_prefix}' if id_prefix else 'words'
    id_stem = f'bd-{id_prefix}-' if id_prefix else 'bd-'
    heading = title if title is not None else 'Word cloud'
    words = data.get('words', [])
    positions = _pack(words)
    extent = max((math.hypot(x, y) + r for x, y, r in positions), default=50.0) + 8.0
    diameter = 2 * extent
    chart_width = 850
    if minimum_word_pixels and words:
        smallest_label = min(_label_layout(str(item['word']), radius)[2]
                             for item, (_, _, radius) in zip(words, positions))
        chart_width = max(chart_width, math.ceil(minimum_word_pixels * diameter / smallest_label))
    items = []
    readable = []
    for item, (x, y, radius) in zip(words, positions):
        count = int(item['count'])
        word = esc(item['word'])
        lines, baselines, label_size = _label_layout(str(item['word']), radius)
        cx, cy = x + extent, y + extent
        label = f'{word}: {count} uses'
        spans = ''.join(f'<tspan x="{cx:.6f}" y="{cy + baseline:.6f}">{esc(line)}</tspan>' for line, baseline in zip(lines, baselines))
        count_baseline = 29 if len(lines) == 2 else 22
        # Critical SVG styling travels with the figure: an old or unavailable
        # stylesheet must not produce black circles or start-aligned labels.
        word_style = f"font-family:'Source Sans 3',sans-serif;font-size:{label_size:.3f}px;font-weight:800;text-anchor:middle;fill:#202f35"
        count_style = "font-family:'Source Sans 3',sans-serif;font-size:18px;font-weight:700;text-anchor:middle;fill:#4a5c64"
        items.append(f'<g class="bd-frequency-word" data-word="{word}" data-count="{count}" role="img" aria-label="{label}"><title>{label}</title><circle cx="{cx:.6f}" cy="{cy:.6f}" r="{radius:.6f}" fill="#dbe9f1" stroke="#7393a4" stroke-width="1" vector-effect="non-scaling-stroke"/><text class="bd-frequency-text" x="{cx:.6f}" y="{cy - 2:.6f}" font-size="{label_size:.3f}" style="{word_style}">{spans}</text><text class="bd-frequency-count" x="{cx:.6f}" y="{cy + count_baseline:.6f}" style="{count_style}">{count}</text></g>')
        readable.append(f'<li><span>{word}</span><strong>{count}</strong></li>')
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    return f'''<section id="{esc(section_id)}" class="bd-words bd-frequency" aria-labelledby="{esc(id_stem)}words-title">
<h2 id="{esc(id_stem)}words-title">{esc(heading)}</h2>
<p class="bd-frequency-instruction">Circle area shows frequency. Numbers show counts.</p>
<div class="bd-frequency-chart" style="max-width:{chart_width}px;margin:0 auto;overflow-x:auto;overscroll-behavior-inline:contain" role="region" aria-label="Packed word frequency circles; scroll horizontally on a small screen" tabindex="0"><svg class="bd-frequency-cluster" xmlns="http://www.w3.org/2000/svg" width="{chart_width}" height="{chart_width}" style="display:block;width:100%;min-width:{chart_width}px;max-width:none;height:auto;margin:0;padding:0" viewBox="0 0 {diameter:.6f} {diameter:.6f}" role="img" aria-labelledby="{esc(id_stem)}frequency-chart-title {esc(id_stem)}frequency-chart-desc"><title id="{esc(id_stem)}frequency-chart-title">Word cloud, {esc(data.get('scope', 'pp. vii–24'))}</title><desc id="{esc(id_stem)}frequency-chart-desc">{len(words)} packed circles, one for each counted word. Circle area is proportional to the exact count printed below the word. Common function words are excluded. A readable list of all counts follows.</desc>{''.join(items)}</svg></div>
<p class="bd-frequency-mobile-note">Scroll sideways to read every circle.</p>
<p class="bd-frequency-scope">{esc(data.get('scope', 'pp. vii–24'))} · {len(words)} most frequent words, excluding common words such as the, a, and an.</p>
<details class="bd-frequency-count-list"><summary>Read all word counts</summary><ul>{''.join(readable)}</ul></details>
<details class="bd-frequency-method"><summary>Counting method</summary><div><p>{esc(data.get('method', ''))}</p></div></details>
<script type="application/json" id="{esc(id_stem)}word-data">{payload}</script></section>'''
