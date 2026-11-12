for (const chapter of document.querySelectorAll('.chapter')) {
  const timeline = chapter.querySelector('.chron');
  const events = [...timeline.querySelectorAll('.event')];
  const controls = document.createElement('div');
  controls.className = 'timeline-controls';
  controls.setAttribute('role', 'tablist');
  controls.setAttribute('aria-label', timeline.querySelector('h3').textContent);
  const rings = [...chapter.querySelectorAll('.overlay circle')];
  const buttons = events.map((event, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'time-button';
    button.id = event.id + '-tab';
    button.textContent = event.dataset.year;
    button.setAttribute('role', 'tab');
    button.setAttribute('aria-controls', event.id);
    button.setAttribute('aria-label', event.dataset.year + ', ' + event.querySelector('h4').textContent);
    event.setAttribute('role', 'tabpanel');
    event.setAttribute('aria-labelledby', button.id);
    button.addEventListener('click', () => select(index));
    button.addEventListener('keydown', e => {
      let next;
      switch (e.key) {
        case 'ArrowRight': next = (index + 1) % events.length; break;
        case 'ArrowLeft': next = (index + events.length - 1) % events.length; break;
        case 'Home': next = 0; break;
        case 'End': next = events.length - 1; break;
        default: return;
      }
      e.preventDefault();
      select(next);
      buttons[next].focus();
    });
    controls.append(button);
    return button;
  });
  function select(index) {
    const where = events[index].dataset.places.split(' ');
    for (const [i, event] of events.entries()) {
      event.hidden = i !== index;
      buttons[i].setAttribute('aria-selected', String(i === index));
      buttons[i].tabIndex = i === index ? 0 : -1;
    }
    for (const circle of rings) circle.classList.toggle('active', where.includes(circle.dataset.place));
  }
  timeline.querySelector('.events').before(controls);
  timeline.classList.add('timeline-ready');
  select(Number(timeline.dataset.initial));
}
