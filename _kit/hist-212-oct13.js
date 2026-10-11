const characters = ['快 · kuài · sudden','雪 · xuě · snow','時 · shí · time','晴 · qíng · clear'];
const focusBox = document.querySelector('#glyph-focus');
const statusLine = document.querySelector('#glyph-status');
document.querySelectorAll('[data-glyph]').forEach(button => {
  button.addEventListener('click', () => {
    const index = Number(button.dataset.glyph);
    document.querySelectorAll('[data-glyph]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    focusBox.style.top = `${[38, 49, 60, 71][index]}%`;
    focusBox.hidden = false;
    statusLine.textContent = `${characters[index]}. Outlined in the right-hand column of the letter.`;
  });
});
