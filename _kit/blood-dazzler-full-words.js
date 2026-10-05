/* Counts only: the source poems are not included in this page. */
(() => {
  'use strict';
  const source = document.getElementById('bd-whole-book-data');
  const form = document.getElementById('bd-word-search');
  const input = document.getElementById('bd-lookup-word');
  const title = document.getElementById('bd-result-title');
  const note = document.getElementById('bd-result-note');
  const rows = document.getElementById('bd-result-rows');
  const table = document.getElementById('bd-result-table-wrap');
  const caption = document.querySelector('.bd-result-table caption');
  const error = document.getElementById('bd-search-error');
  if (!source || !form || !input || !title || !note || !rows || !table || !caption || !error) return;
  let book;
  try {
    book = JSON.parse(source.textContent);
    if (!book.counts || !Array.isArray(book.poems)) return;
  } catch (_) {
    return;
  }
  const normalize = value => value.trim().toLowerCase().replace(/[\u2018\u2019]/g, "'");
  const exactWord = /^[\p{L}\p{N}]+(?:['-][\p{L}\p{N}]+)*$/u;
  const countOf = (counts, word) => Object.prototype.hasOwnProperty.call(counts, word) ? Number(counts[word]) : 0;
  const showWord = word => {
    const matches = book.poems.filter(poem => countOf(poem.counts, word) > 0);
    const total = countOf(book.counts, word);
    const fragment = document.createDocumentFragment();
    matches.forEach(poem => {
      const row = document.createElement('tr');
      const heading = document.createElement('th');
      heading.scope = 'row';
      heading.textContent = poem.title;
      const pages = document.createElement('td');
      pages.textContent = poem.pages;
      const count = document.createElement('td');
      count.textContent = String(poem.counts[word]);
      row.append(heading, pages, count);
      fragment.append(row);
    });
    rows.replaceChildren(fragment);
    title.textContent = `${word}: ${total} ${total === 1 ? 'use' : 'uses'} in ${matches.length} ${matches.length === 1 ? 'poem' : 'poems'}`;
    note.textContent = matches.length
      ? 'Counts below refer to poem bodies. Pages are printed book pages.'
      : 'No exact matches in the poem bodies. Word forms are counted separately.';
    caption.textContent = `Poems containing ${word}`;
    table.hidden = matches.length === 0;
  };
  form.hidden = false;
  form.addEventListener('submit', event => {
    event.preventDefault();
    const word = normalize(input.value);
    if (!exactWord.test(word)) {
      error.textContent = 'Enter one word. Contractions and hyphenated words are accepted.';
      input.setAttribute('aria-invalid', 'true');
      input.focus();
      return;
    }
    error.textContent = '';
    input.removeAttribute('aria-invalid');
    input.value = word;
    showWord(word);
  });
})();
