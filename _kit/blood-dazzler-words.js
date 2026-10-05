(() => {
  'use strict';
  const root = document.querySelector('.bd-words');
  const dataElement = document.getElementById('bd-word-data');
  if (!root || !dataElement) return;
  let data;
  try { data = JSON.parse(dataElement.textContent); } catch (_) { return; }
  if (!Array.isArray(data.nodes) || !data.nodes.length) return;
  const nodes = new Map(data.nodes.map(node => [String(node.id), node]));
  const graph = root.querySelector('.bd-word-graph');
  const svg = root.querySelector('.bd-word-edges');
  const detail = root.querySelector('.bd-word-detail');
  if (!graph || !svg || !detail) return;
  const buttons = new Map();
  const links = (data.links || []).filter(link => nodes.has(String(link.source)) && nodes.has(String(link.target)));
  let selectedId = nodes.has('water') ? 'water' : String(data.nodes[0].id);
  const make = (tag, className, text) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text != null) element.textContent = text;
    return element;
  };
  const connectedLinks = id => links.filter(link => String(link.source) === id || String(link.target) === id);
  const otherId = (link, id) => String(link.source) === id ? String(link.target) : String(link.source);
  root.querySelectorAll('.bd-word-node').forEach(anchor => {
    const id = anchor.dataset.wordId;
    if (!nodes.has(id)) return;
    const button = make('button', 'bd-word-node', nodes.get(id).word);
    button.type = 'button';
    button.dataset.wordId = id;
    button.setAttribute('aria-controls', 'bd-word-selected');
    button.setAttribute('aria-pressed', 'false');
    button.addEventListener('click', () => select(id));
    anchor.replaceWith(button);
    buttons.set(id, button);
  });
  detail.id = 'bd-word-selected';
  function drawEdges() {
    const box = graph.getBoundingClientRect();
    if (!box.width || !box.height) return;
    svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
    const fragment = document.createDocumentFragment();
    for (const cluster of data.clusters || []) {
      const group = Array.from(root.querySelectorAll('.bd-word-group')).find(item => item.dataset.cluster === String(cluster.id));
      const heading = group?.querySelector('h3');
      if (!heading) continue;
      const hr = heading.getBoundingClientRect();
      const hx = hr.left + hr.width / 2 - box.left, hy = hr.bottom + 6 - box.top;
      const active = String(nodes.get(selectedId)?.cluster) === String(cluster.id);
      for (const id of cluster.words || []) {
        const button = buttons.get(String(id));
        if (!button) continue;
        const r = button.getBoundingClientRect();
        const x = r.left + r.width / 2 - box.left, y = r.top + r.height / 2 - box.top;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M ${hx} ${hy} Q ${hx} ${(hy + y) / 2} ${x} ${y}`);
        path.setAttribute('class', `bd-word-edge bd-word-spoke ${active ? 'is-active' : ''}`);
        fragment.append(path);
      }
      const hub = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      hub.setAttribute('cx', hx); hub.setAttribute('cy', hy); hub.setAttribute('r', '3.5');
      hub.setAttribute('class', `bd-word-hub ${active ? 'is-active' : ''}`);
      fragment.append(hub);
    }
    for (const link of links) {
      const a = buttons.get(String(link.source));
      const b = buttons.get(String(link.target));
      if (!a || !b) continue;
      const ar = a.getBoundingClientRect(), br = b.getBoundingClientRect();
      const ax = ar.left + ar.width / 2 - box.left, ay = ar.top + ar.height / 2 - box.top;
      const bx = br.left + br.width / 2 - box.left, by = br.top + br.height / 2 - box.top;
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const bend = Math.min(46, Math.abs(bx - ax) * .16 + Math.abs(by - ay) * .07);
      path.setAttribute('d', `M ${ax} ${ay} Q ${(ax + bx) / 2 + bend} ${(ay + by) / 2 - bend} ${bx} ${by}`);
      path.setAttribute('class', `bd-word-edge ${String(link.source) === selectedId || String(link.target) === selectedId ? 'is-active' : 'is-muted'}`);
      fragment.append(path);
    }
    svg.replaceChildren(fragment);
  }
  function select(id) {
    const node = nodes.get(id);
    if (!node) return;
    selectedId = id;
    const relationships = connectedLinks(id);
    const relatedIds = new Set(relationships.map(link => otherId(link, id)));
    for (const sibling of data.nodes) {
      if (String(sibling.cluster) === String(node.cluster) && String(sibling.id) !== id) relatedIds.add(String(sibling.id));
    }
    for (const [buttonId, button] of buttons) {
      button.setAttribute('aria-pressed', String(buttonId === id));
      button.classList.toggle('is-connected', relatedIds.has(buttonId));
      button.classList.toggle('is-muted', buttonId !== id && !relatedIds.has(buttonId));
    }
    const content = document.createDocumentFragment();
    content.append(make('h3', '', node.word));
    content.append(make('p', '', node.summary));
    const examples = make('ol');
    for (const example of node.examples || []) {
      const item = make('li');
      const title = make('span', 'bd-word-example-title', example.poem);
      const pages = String(example.pages);
      item.append(title, document.createTextNode(' '), make('span', 'bd-word-pages', `${pages.includes('–') ? 'pp.' : 'p.'} ${pages}`));
      item.append(make('p', 'bd-word-example-note', example.note));
      examples.append(item);
    }
    content.append(examples);
    if (node.characters && node.characters.length) content.append(make('p', 'bd-word-character-note', `Characters: ${node.characters.join(', ')}`));
    if (relationships.length) {
      content.append(make('p', 'bd-word-related-title', 'Connected words'));
      const related = make('div', 'bd-word-related');
      const notes = make('ul', 'bd-word-link-notes');
      for (const link of relationships) {
        const relatedNode = nodes.get(otherId(link, id));
        const button = make('button', 'bd-word-related-button', relatedNode.word);
        button.type = 'button';
        button.setAttribute('aria-controls', 'bd-word-selected');
        button.addEventListener('click', () => {
          const nextId = String(relatedNode.id);
          select(nextId);
          const replacement = Array.from(detail.querySelectorAll('button')).find(item => item.textContent === node.word);
          if (replacement) replacement.focus({preventScroll: true});
          else buttons.get(nextId)?.focus({preventScroll: true});
        });
        related.append(button);
        if (link.note) {
          const item = make('li');
          item.append(make('strong', '', relatedNode.word), document.createTextNode(`: ${link.note}`));
          notes.append(item);
        }
      }
      content.append(related, notes);
    }
    detail.replaceChildren(content);
    drawEdges();
  }
  root.classList.add('is-ready');
  select(selectedId);
  let frame;
  const scheduleDraw = () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(drawEdges); };
  if ('ResizeObserver' in window) new ResizeObserver(scheduleDraw).observe(graph);
  window.addEventListener('resize', scheduleDraw, {passive: true});
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(scheduleDraw);
})();
