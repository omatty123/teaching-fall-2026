(() => {
  'use strict';
  const tools = document.getElementById('thought-tools');
  if (!tools) return;
  const rows = [...document.querySelectorAll('.thought-row')];
  const buttons = [...tools.querySelectorAll('[data-thinker]')];
  const search = document.getElementById('thought-search');
  const count = document.getElementById('thought-count');
  const table = document.getElementById('thought-chart');
  const empty = document.getElementById('thought-empty');
  const names = Object.fromEntries(buttons.map(b => [b.dataset.thinker,b.textContent.trim()]));
  let thinker = 'all';
  function readURL() {
    const params = new URLSearchParams(location.search);
    thinker = Object.hasOwn(names, params.get('thinker')) ? params.get('thinker') : 'all';
    search.value = params.get('q') || '';
  }
  readURL();
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[’‘']/g, '').toLowerCase();
  const texts = new Map(rows.map(row => [row, normalize(`${row.textContent} ${row.dataset.search || ''}`)]));
  function apply(updateURL = true) {
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const row of rows) {
      row.hidden = !((thinker === 'all' || row.dataset.thinker === thinker) && terms.every(term => texts.get(row).includes(term)));
      if (!row.hidden) shown++;
    }
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.thinker === thinker));
    count.textContent = `${shown} of ${rows.length} examples · ${names[thinker]}${search.value.trim() ? ` · “${search.value.trim()}”` : ''}`;
    table.hidden = shown === 0;
    empty.hidden = shown !== 0;
    if (updateURL) {
      const url = new URL(location.href);
      thinker === 'all' ? url.searchParams.delete('thinker') : url.searchParams.set('thinker', thinker);
      search.value.trim() ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
      history.replaceState(null, '', url);
    }
  }
  for (const button of buttons) button.addEventListener('click', () => { thinker = button.dataset.thinker; apply(); });
  search.addEventListener('input', () => apply());
  document.getElementById('thought-clear').addEventListener('click', () => { thinker = 'all'; search.value = ''; apply(); search.focus(); });
  document.getElementById('thought-print').addEventListener('click', () => window.print());
  function revealAnchor() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = rows.find(row => row.id === id);
    if (target?.hidden) { thinker = 'all'; search.value = ''; apply(); target.scrollIntoView(); }
  }
  tools.hidden = false;
  apply(false);
  revealAnchor();
  window.addEventListener('hashchange', revealAnchor);
  window.addEventListener('popstate', () => { readURL(); apply(false); revealAnchor(); });
})();
