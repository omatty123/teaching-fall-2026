const characters = ['快 · kuài · quick / sudden','雪 · xuě · snow','時 · shí · time / at times','晴 · qíng · clear weather'];
const focusBox = document.querySelector('#glyph-focus');
const statusLine = document.querySelector('#glyph-status');
document.querySelectorAll('[data-glyph]').forEach(button => {
  button.addEventListener('click', () => {
    const index = Number(button.dataset.glyph);
    document.querySelectorAll('[data-glyph]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    focusBox.style.top = `${[44.4, 50.9, 57.4, 64.2][index]}%`;
    focusBox.hidden = false;
    statusLine.textContent = `${characters[index]}. Outlined in the right-hand column of the model.`;
  });
});
