import { SIMULATIONS } from './simulation-data.mjs';
import { createDraft, readyForReveal, revealDraft, respondToNewInformation } from './simulation-state.mjs';

const $ = id => document.getElementById(id);
const sessions = new Map(SIMULATIONS.map(s => [s.id, { choiceId: null, drafts: new Map() }]));
let current = SIMULATIONS.find(s => s.id === location.hash.slice(1)) || SIMULATIONS[0];
const node = (tag, text, className) => {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
};
const session = () => sessions.get(current.id);
const choice = () => current.choices.find(c => c.id === session().choiceId);
const draft = () => session().drafts.get(session().choiceId);
const fillList = (id, items) => $(id).replaceChildren(...items.map(item => node('li', item)));
const focus = id => { $(id).focus(); $(id).scrollIntoView({ block: 'start' }); };
const announce = message => { if ($('status').textContent !== message) $('status').textContent = message; };

function renderIndex() {
  $('scenario-list').replaceChildren(...SIMULATIONS.map(s => {
    const button = node('button', undefined, 'scenario-button');
    button.type = 'button';
    button.dataset.scenario = s.id;
    button.setAttribute('aria-pressed', String(s.id === current.id));
    button.append(node('strong', s.title), node('span', s.field));
    button.addEventListener('click', () => {
      current = s;
      history.replaceState(null, '', '#' + s.id);
      renderScenario();
      focus('scenario-title');
    });
    return button;
  }));
}

function radioRow(item, group, checked, onChange, detail = null) {
  const label = node('label', undefined, 'choice-row');
  const input = document.createElement('input');
  input.type = 'radio'; input.name = group; input.value = item.id; input.checked = checked;
  input.addEventListener('change', () => onChange(item.id));
  const copy = node('span');
  copy.append(node('strong', item.label));
  if (detail) copy.append(node('span', detail, 'detail'));
  label.append(input, copy);
  return label;
}

function renderReadiness() {
  const d = draft();
  $('reveal').disabled = !readyForReveal(d);
  const step = !choice() ? 'choose' : d.revealed ? 'review' : 'predict';
  for (const name of ['choose', 'predict', 'review']) {
    if (name === step) $('step-' + name).setAttribute('aria-current', 'step');
    else $('step-' + name).removeAttribute('aria-current');
  }
  $('prediction-help').textContent = !choice()
    ? 'Choose an action, then write both predictions. Predictions are kept separately for each action.'
    : 'Write both predictions before comparing the possible outcomes. Short notes are enough.';
}

function renderDebrief() {
  const c = choice(), d = draft();
  const response = c?.followups.find(item => item.id === d?.followup);
  $('debrief').hidden = !response;
  $('feedback').textContent = response?.feedback || '';
}

function renderResults() {
  const c = choice(), d = draft();
  $('chosen-action').textContent = 'Your initial action: ' + c.label;
  $('predicted-likely').textContent = d.likely;
  $('predicted-alternative').textContent = d.alternative;
  $('predicted-check').textContent = d.check ? 'Your check: ' + d.check : '';
  $('predicted-check').hidden = !d.check;
  $('outcomes').replaceChildren(...c.outcomes.map(outcome => {
    const section = node('section', undefined, 'outcome');
    section.append(node('h5', outcome.label));
    for (const [label, value] of [['Soon: ', outcome.immediate], ['Later: ', outcome.later]]) {
      const p = node('p'); p.append(node('strong', label), document.createTextNode(value)); section.append(p);
    }
    return section;
  }));
  $('analysis').textContent = c.analysis;
  $('new-information').textContent = c.newInformation;
  $('followups').replaceChildren(...c.followups.map(item => radioRow(item, 'followup', item.id === d.followup, id => {
    respondToNewInformation(c, d, id);
    renderDebrief();
    announce('Response recorded. Review the reasons and remaining responsibilities.');
    focus('debrief-title');
  })));
  renderDebrief();
}

function renderDraft() {
  const d = draft();
  for (const key of ['likely', 'alternative', 'check']) {
    $(key).value = d?.[key] || '';
    $(key).disabled = !choice();
  }
  $('prediction-form').hidden = Boolean(d?.revealed);
  $('results').hidden = !d?.revealed;
  if (d?.revealed) renderResults();
  renderReadiness();
}

function renderScenario() {
  renderIndex();
  $('scenario-title').textContent = current.title;
  $('scenario-field').textContent = current.field;
  $('scenario-role').textContent = 'Your role: ' + current.role;
  $('scenario-setup').replaceChildren(...current.setup.map(p => node('p', p)));
  fillList('scenario-facts', current.facts);
  fillList('scenario-unknowns', current.unknowns);
  fillList('scenario-people', current.people);
  $('choices').replaceChildren(...current.choices.map(item => radioRow(item, 'initial-action', session().choiceId === item.id, id => {
    session().choiceId = id;
    if (!session().drafts.has(id)) session().drafts.set(id, createDraft());
    renderDraft();
    announce(draft().revealed ? 'Previous predictions and comparison restored for this action.' : 'Action selected. Record your predictions.');
  }, item.detail)));
  renderDraft();
  announce(draft()?.revealed ? 'Your previous comparison is restored.' : 'Situation ready. Choose an initial action.');
}

for (const key of ['likely', 'alternative', 'check']) {
  $(key).addEventListener('input', () => {
    if (!draft()) return;
    draft()[key] = $(key).value;
    renderReadiness();
    if (readyForReveal(draft())) announce('Both predictions are ready to compare.');
  });
}
$('prediction-form').addEventListener('submit', event => {
  event.preventDefault();
  if (!readyForReveal(draft())) return;
  revealDraft(draft());
  renderDraft();
  announce('Possible outcomes revealed. Compare them with your predictions.');
  focus('results-title');
});
$('edit-predictions').addEventListener('click', () => {
  draft().revealed = false;
  renderDraft();
  announce('Predictions reopened for revision. Your notes have been kept.');
  focus('likely');
});
$('another-action').addEventListener('click', () => {
  const alternative = [...document.querySelectorAll('#choices input')].find(input => !input.checked);
  alternative?.focus();
  $('choice-fieldset').scrollIntoView({ block: 'start' });
  announce('Choose another action above. Your previous notes are kept for each action.');
});
$('clear-scenario').addEventListener('click', () => {
  sessions.set(current.id, { choiceId: null, drafts: new Map() });
  renderScenario();
  announce('Notes cleared for this scenario only.');
  focus('scenario-title');
});
window.addEventListener('hashchange', () => {
  const requested = SIMULATIONS.find(s => s.id === location.hash.slice(1));
  if (requested && requested.id !== current.id) { current = requested; renderScenario(); }
});
renderScenario();
$('startup').hidden = true;
$('activity').hidden = false;
