(() => {
  const controls = [...document.querySelectorAll('.setting-select')];
  const map = document.querySelector('.map-frame');
  if (!map) return;
  map.setAttribute('tabindex', '0');
  map.setAttribute('aria-label', 'Great Lakes settings map. Scroll horizontally on a narrow screen.');
  controls.forEach(button => button.addEventListener('click', () => {
    const selected = button.dataset.setting;
    controls.forEach(control => control.setAttribute('aria-pressed', String(control === button)));
    document.querySelectorAll('.setting-pin').forEach(pin => pin.classList.toggle('active', pin.dataset.setting === selected));
    const marker = document.querySelector(`.setting-pin[data-setting="${selected}"]`);
    if (marker && map.scrollWidth > map.clientWidth) {
      const x = marker.getBoundingClientRect().left - map.getBoundingClientRect().left + map.scrollLeft;
      map.scrollLeft = Math.max(0, x - map.clientWidth / 2);
      map.scrollIntoView({block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
    }
  }));
})();
