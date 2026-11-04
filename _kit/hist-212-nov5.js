(() => {
  const main = document.querySelector('main');
  const nav = document.querySelector('.sections');
  const topics = [...main.querySelectorAll(':scope > section')];
  const select = document.createElement('select');
  select.className = 'topic-select';
  select.setAttribute('aria-label', 'Choose a lesson topic');
  topics.forEach(topic => {
    const option = document.createElement('option');
    option.value = topic.id;
    option.textContent = topic.querySelector('h2').textContent;
    select.append(option);
  });
  nav.before(select);
  const all = document.createElement('button');
  all.className = 'all';
  all.textContent = 'Read all topics';
  all.setAttribute('aria-pressed', 'false');
  nav.append(all);
  const pager = document.createElement('nav');
  pager.className = 'pager';
  pager.setAttribute('aria-label', 'Lesson sequence');
  main.querySelector('footer').before(pager);
  let showAll = false;
  function render(move = false) {
    const id = location.hash.slice(1);
    let index = topics.findIndex(topic => topic.id === id);
    if (index < 0) index = 0;
    topics.forEach((topic, i) => { topic.hidden = !showAll && i !== index; });
    select.value = topics[index].id;
    nav.querySelectorAll('a').forEach(link => {
      if (link.hash === '#' + topics[index].id) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    pager.replaceChildren();
    [index - 1, index + 1].forEach((i, direction) => {
      if (!topics[i]) return;
      const link = document.createElement('a');
      link.href = '#' + topics[i].id;
      link.textContent = (direction ? 'Next: ' : 'Previous: ') + topics[i].querySelector('h2').textContent;
      pager.append(link);
    });
    pager.hidden = showAll;
    all.textContent = showAll ? 'View one topic' : 'Read all topics';
    all.setAttribute('aria-pressed', String(showAll));
    if (move) {
      const heading = topics[index].querySelector('h2');
      heading.setAttribute('tabindex', '-1');
      heading.focus({preventScroll: true});
      (showAll ? topics[index] : main).scrollIntoView({block: 'start'});
    }
  }
  all.addEventListener('click', () => { showAll = !showAll; render(); });
  select.addEventListener('change', () => { location.hash = select.value; });
  window.addEventListener('hashchange', () => render(true));
  document.body.classList.add('viewer');
  render();
})();
