export function createDraft() {
  return { likely: '', alternative: '', check: '', revealed: false, followup: null };
}
export function readyForReveal(draft) {
  return Boolean(draft && draft.likely.trim() && draft.alternative.trim());
}
export function revealDraft(draft) {
  if (!readyForReveal(draft)) throw new Error('Write both predictions before revealing outcomes.');
  draft.revealed = true;
}
export function respondToNewInformation(choice, draft, id) {
  if (!draft.revealed) throw new Error('First predict and compare possible outcomes.');
  const response = choice.followups.find(item => item.id === id);
  if (!response) throw new Error('Unknown response for this action.');
  draft.followup = id;
  return response;
}
