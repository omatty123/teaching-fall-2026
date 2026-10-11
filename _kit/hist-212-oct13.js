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
