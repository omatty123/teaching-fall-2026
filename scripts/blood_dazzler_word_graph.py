"""Render a simple, public-safe cluster of mechanically counted words."""
import html
import json


def render_graph(data):
    """Keep the builder interface; render readable words and counts without JS."""
    esc = lambda value: html.escape(str(value), quote=True)
    words = data.get('words', [])
    highest = max((int(item['count']) for item in words), default=1)
    lowest = min((int(item['count']) for item in words), default=1)
    frequency_range = highest - lowest
    items = []
    for item in words:
        count = int(item['count'])
        weight = (count - lowest) / frequency_range if frequency_range else 0.5
        size = 1.12 + 2.18 * weight
        items.append(f'<li class="bd-frequency-word" data-word="{esc(item["word"])}" data-count="{count}" style="--frequency-size:{size:.3f}rem"><span class="bd-frequency-text">{esc(item["word"])}</span><small class="bd-frequency-count"><span class="bd-frequency-sr"> count: </span>{count}</small></li>')
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    return f'''<section id="words" class="bd-words bd-frequency" aria-labelledby="bd-words-title">
<h2 id="bd-words-title">Word frequency</h2>
<p class="bd-frequency-instruction">Larger words occur more often. Numbers show counts.</p>
<ul class="bd-frequency-cluster" aria-label="Frequently used words and their counts">{''.join(items)}</ul>
<p class="bd-frequency-scope">{esc(data.get('scope', 'pp. vii–24'))} · {len(words)} most frequent words, excluding common words such as the, a, and an.</p>
<details class="bd-frequency-method"><summary>Counting method</summary><div><p>{esc(data.get('method', ''))}</p></div></details>
<script type="application/json" id="bd-word-data">{payload}</script></section>'''
