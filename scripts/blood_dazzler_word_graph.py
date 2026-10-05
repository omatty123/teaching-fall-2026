"""Public-safe, progressively enhanced thematic word connections."""
import html
import json


def page_label(pages):
    return ('pp. ' if '–' in str(pages) else 'p. ') + str(pages)


def render_graph(data):
    """Return the words section; all reading notes remain available without JS."""
    esc = lambda value: html.escape(str(value), quote=True)
    nodes = {str(node['id']): node for node in data['nodes']}
    groups = []
    fallback = []
    for group in data['clusters']:
        buttons = []
        for node_id in group['words']:
            node = nodes[str(node_id)]
            buttons.append(f'<a class="bd-word-node" data-word-id="{esc(node_id)}" href="#bd-word-{esc(node_id)}">{esc(node["word"])}</a>')
        groups.append(f'<div class="bd-word-group" data-cluster="{esc(group["id"])}"><h3>{esc(group["label"])}</h3><div class="bd-word-group-nodes">{"".join(buttons)}</div></div>')
    for node in data['nodes']:
        examples = ''.join(f'<li><strong>{esc(example["poem"])}</strong> <span class="bd-word-pages">{esc(page_label(example["pages"]))}</span><p>{esc(example["note"])}</p></li>' for example in node.get('examples', []))
        characters = ', '.join(esc(item) for item in node.get('characters', []))
        related = []
        for link in data.get('links', []):
            if node['id'] in (link['source'], link['target']):
                other_id = link['target'] if link['source'] == node['id'] else link['source']
                other = nodes.get(str(other_id))
                if other:
                    related.append(f'<li><strong>{esc(other["word"])}</strong>: {esc(link.get("note", ""))}</li>')
        fallback.append(f'<details id="bd-word-{esc(node["id"])}"><summary>{esc(node["word"])}</summary><div><p>{esc(node["summary"])}</p><ol>{examples}</ol>' + (f'<p><strong>Characters:</strong> {characters}</p>' if characters else '') + (f'<ul>{"".join(related)}</ul>' if related else '') + '</div></details>')
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    return f'''<section id="words" class="bd-words" aria-labelledby="bd-words-title">
<div class="bd-words-heading"><h2 id="bd-words-title">Word connections</h2><p>Choose a word to follow its meaning across the poems.</p></div>
<div class="bd-word-layout"><div class="bd-word-network"><div class="bd-word-graph"><svg class="bd-word-edges" aria-hidden="true" focusable="false"></svg><div class="bd-word-groups">{''.join(groups)}</div></div><p class="bd-word-caption">Groups and lines connect related words and images across the poems.</p><a class="bd-word-read" href="#bd-word-selected">Read selected word ↓</a></div><aside id="bd-word-selected" class="bd-word-detail" aria-label="Selected word" aria-live="polite" aria-atomic="true"></aside></div>
<div class="bd-word-fallback"><h3>Read the word notes</h3>{''.join(fallback)}</div>
<script type="application/json" id="bd-word-data">{payload}</script></section>'''
