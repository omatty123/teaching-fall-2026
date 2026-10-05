/* Progressive scope selection. Without JavaScript, all four clouds remain visible. */
(() => {
  'use strict';
  const nav = document.querySelector('.bd-cloud-nav');
  if (!nav) return;
  const links = Array.from(nav.querySelectorAll('a[data-cloud]'));
  const sections = links.map(link => document.getElementById(link.dataset.cloud));
  if (links.length !== 4 || sections.some(section => !section)) return;
  const sectionForHash = () => {
    let id;
    try {
      id = decodeURIComponent(window.location.hash.slice(1));
    } catch (_) {
      return 'words-whole';
    }
    return sections.some(section => section.id === id) ? id : 'words-whole';
  };
  const show = (id, scroll) => {
    sections.forEach(section => { section.hidden = section.id !== id; });
    links.forEach(link => {
      if (link.dataset.cloud === id) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
    if (scroll) document.getElementById(id).scrollIntoView({block: 'start'});
  };
  links.forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      if (window.location.hash !== link.hash) window.history.pushState(null, '', link.hash);
      show(link.dataset.cloud, true);
    });
  });
  const restore = () => show(sectionForHash(), true);
  window.addEventListener('popstate', restore);
  window.addEventListener('hashchange', restore);
  show(sectionForHash(), false);
  if (window.location.hash) window.requestAnimationFrame(restore);
})();
