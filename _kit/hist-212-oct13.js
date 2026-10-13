const statusLine = document.querySelector('#glyph-status');
const characters = ['快 · kuài · sudden', '雪 · xuě · snow', '時 · shí · time', '晴 · qíng · clear'];
document.querySelectorAll('[data-glyph]').forEach(button => {
  button.addEventListener('click', () => {
    const index = Number(button.dataset.glyph);
    document.querySelectorAll('[data-glyph]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    document.querySelectorAll('[data-mark]').forEach(mark => mark.classList.toggle('is-selected', Number(mark.dataset.mark) === index));
    statusLine.textContent = `${index + 1}. ${characters[index]}. Matching brush form in the right-hand column; read downward.`;
  });
});

// Progressive enhancement: the complete lesson remains readable without JavaScript.
(() => {
  const main = document.querySelector('main');
  const header = main.querySelector('header');
  const parts = [...main.querySelectorAll('.lesson-part')];
  if (!parts.length) return;
  const overview = document.createElement('section');
  overview.id = 'overview';
  overview.innerHTML = '<h2>Buddhism in East Asia</h2>';
  header.querySelectorAll('.lesson-argument,.principal-figures,.dunhuang-jump').forEach(el => overview.append(el));
  const photograph = document.querySelector('#dunhuang figure');
  if (photograph) {
    const copy = photograph.cloneNode(true);
    copy.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
    copy.classList.add('overview-photograph');
    overview.insertBefore(copy, overview.children[1]);
  }
  header.after(overview);
  const labels = {'overview':'Today’s lesson','course-story':'From Qin and Han','spread':'Graphic timeline','calligraphy':'Wang Xizhi · calligraphy','dunhuang':'Dunhuang','cave-sites':'Cave sites · Yungang','teachings':'Jewels, truths & path','images':'Buddha & bodhisattva','art':'Pensive Bodhisattva','mouzi':'Mouzi','foreign-affairs':'Foreign practices · PRO / CON','huiyuan':'Huiyuan','silla':'Buddhism in Silla','petition':'Wŏn’gwang’s petition','war-killing':'War and killing','seasonal-killing':'Seasonal killing rules','vegetarianism':'Vegetarianism','dunhuang-tang':'Looking ahead · Tang','close':'What changed','resources':'Readings & sources'};
  const topics = [overview, ...parts.flatMap(p => [...p.querySelectorAll(':scope > section')]), main.querySelector('#resources')].filter(Boolean);
  const aside = document.createElement('nav');
  aside.className = 'lesson-contents';
  aside.setAttribute('aria-label','Class topics');
  const title = document.createElement('strong'); title.textContent = 'October 13 · HIST 212'; aside.append(title);
  const selectLabel = document.createElement('label'); selectLabel.className = 'topic-picker'; selectLabel.textContent = 'Topic';
  const select = document.createElement('select'); select.setAttribute('aria-label','Choose a class topic'); selectLabel.append(select); aside.append(selectLabel);
  const list = document.createElement('div'); list.className = 'topic-links'; aside.append(list);
  topics.forEach(topic => {
    if (topic.parentElement.classList.contains('lesson-part') && topic === topic.parentElement.querySelector('section')) {
      const group = document.createElement('span'); group.className = 'topic-group';
      group.textContent = topic.parentElement.querySelector('h2').textContent.replace(/^\d+\.\s*/, ''); list.append(group);
    }
    const link = document.createElement('a'); link.href = '#' + topic.id; link.textContent = labels[topic.id]; list.append(link);
    const option = document.createElement('option'); option.value = topic.id; option.textContent = labels[topic.id]; select.append(option);
  });
  const toggle = document.createElement('button'); toggle.type = 'button'; toggle.textContent = 'Read all topics'; toggle.setAttribute('aria-pressed','false'); aside.append(toggle);
  main.before(aside);
  const pager = document.createElement('nav'); pager.className = 'topic-pager'; pager.setAttribute('aria-label','Lesson sequence');
  const previous = document.createElement('a'), next = document.createElement('a'); pager.append(previous,next); main.querySelector('footer').before(pager);
  let current = overview, readAll = false;
  function render(scroll = false) {
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    current = topics.find(t => t === target || t.contains(target)) || (target?.classList.contains('lesson-part') ? target.querySelector('section') : overview);
    topics.forEach(t => { t.hidden = !readAll && t !== current; });
    parts.forEach(p => { p.hidden = !readAll && !p.contains(current); });
    document.body.classList.toggle('read-all',readAll);
    document.body.classList.toggle('overview-active',current === overview);
    aside.querySelectorAll('.topic-links a').forEach(a => {
      if(a.hash === '#' + current.id) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });
    select.value = current.id;
    const i = topics.indexOf(current);
    [previous,next].forEach((a,n) => { const t = topics[i+(n ? 1 : -1)]; a.hidden = !t; if(t) {a.href='#'+t.id; a.textContent=(n?'Next: ':'Previous: ')+labels[t.id];} });
    toggle.textContent = readAll ? 'View one topic' : 'Read all topics'; toggle.setAttribute('aria-pressed',String(readAll));
    if(scroll) { (readAll ? current : main).scrollIntoView({block:'start'}); current.tabIndex=-1; current.focus({preventScroll:true}); }
  }
  select.addEventListener('change',() => { location.hash = select.value; });
  toggle.addEventListener('click',() => { readAll = !readAll; render(); });
  window.addEventListener('hashchange',() => render(true));
  document.body.classList.add('lesson-viewer');
  render();
})();
