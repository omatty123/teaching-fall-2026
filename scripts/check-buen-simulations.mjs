import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import { relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { SIMULATIONS } from '../buen-594-resources/ethics-assets/simulation-data.mjs';
import {
  createDraft, readyForReveal, revealDraft, respondToNewInformation,
} from '../buen-594-resources/ethics-assets/simulation-state.mjs';

const ROOT = new URL('../', import.meta.url);
const PAGE = new URL('buen-594-resources/ethics-simulations.html', ROOT);

function requiredStrings(record, keys, context) {
  assert.ok(record && typeof record === 'object', `${context}: expected a record`);
  for (const key of keys) {
    assert.equal(typeof record[key], 'string', `${context}.${key}: expected text`);
    assert.ok(record[key].trim(), `${context}.${key}: empty text`);
  }
}

function stringList(list, min, max, context) {
  assert.ok(Array.isArray(list), `${context}: expected an array`);
  assert.ok(list.length >= min && list.length <= max, `${context}: expected ${min}–${max} entries`);
  for (const [index, value] of list.entries()) requiredStrings({ value }, ['value'], `${context}[${index}]`);
}

function uniqueIds(records, context) {
  for (const record of records) requiredStrings(record, ['id'], context);
  assert.equal(new Set(records.map(record => record.id)).size, records.length, `${context}: duplicate IDs`);
}

test('every scenario has complete branches and IDs unique within their scope', () => {
  assert.equal(SIMULATIONS.length, 6);
  uniqueIds(SIMULATIONS, 'scenarios');
  for (const scenario of SIMULATIONS) {
    requiredStrings(scenario, ['id', 'title', 'field', 'role'], scenario.id);
    stringList(scenario.setup, 2, 2, `${scenario.id}.setup`);
    stringList(scenario.facts, 2, 3, `${scenario.id}.facts`);
    stringList(scenario.unknowns, 2, 2, `${scenario.id}.unknowns`);
    stringList(scenario.people, 2, 3, `${scenario.id}.people`);
    assert.equal(scenario.choices.length, 3, `${scenario.id}: expected three initial choices`);
    uniqueIds(scenario.choices, `${scenario.id}.choices`);
    for (const choice of scenario.choices) {
      const context = `${scenario.id}/${choice.id}`;
      requiredStrings(choice, ['id', 'label', 'detail', 'analysis', 'newInformation'], context);
      assert.equal(choice.outcomes.length, 2, `${context}: expected two possible outcomes`);
      for (const outcome of choice.outcomes) requiredStrings(outcome, ['label', 'immediate', 'later'], context);
      assert.notDeepEqual(choice.outcomes[0], choice.outcomes[1], `${context}: outcomes must be distinct`);
      assert.equal(choice.followups.length, 2, `${context}: expected two follow-up choices`);
      uniqueIds(choice.followups, `${context}.followups`);
      for (const followup of choice.followups) requiredStrings(followup, ['id', 'label', 'feedback'], context);
    }
  }
});

test('no draft and incomplete or whitespace-only predictions cannot reveal outcomes', () => {
  assert.equal(readyForReveal(undefined), false);
  assert.equal(readyForReveal(null), false);
  const incomplete = [
    ['', ''],
    ['An immediate effect.', ''],
    ['', 'A later effect.'],
    [' \n\t ', 'A later effect.'],
    ['An immediate effect.', ' \n\t '],
    ['\u00a0', '\u2003'],
  ];
  for (const [likely, alternative] of incomplete) {
    const draft = { ...createDraft(), likely, alternative, check: 'An optional note cannot replace a prediction.' };
    assert.equal(readyForReveal(draft), false, JSON.stringify({ likely, alternative }));
    assert.throws(() => revealDraft(draft), /both predictions/i);
    assert.equal(draft.revealed, false, 'A rejected reveal must not reveal the draft');
  }
});

test('two substantive predictions allow reveal without an optional note or loss of text', () => {
  const draft = createDraft();
  draft.likely = ' \nThe supervisor may request more information.\t ';
  draft.alternative = ' The decision may be delayed. ';
  assert.equal(draft.check, '');
  assert.equal(readyForReveal(draft), true);
  const original = { ...draft };
  revealDraft(draft);
  assert.equal(draft.revealed, true);
  assert.equal(draft.likely, original.likely);
  assert.equal(draft.alternative, original.alternative);
  assert.equal(draft.followup, null);
});

test('follow-up responses require reveal and belong to the selected initial action', () => {
  const choice = SIMULATIONS[0].choices[0];
  const draft = createDraft();
  draft.likely = 'The supervisor may agree.';
  draft.alternative = 'A colleague may object later.';
  assert.throws(() => respondToNewInformation(choice, draft, choice.followups[0].id), /first predict/i);
  assert.equal(draft.followup, null);
  revealDraft(draft);
  const selected = respondToNewInformation(choice, draft, choice.followups[0].id);
  assert.deepEqual(selected, choice.followups[0]);
  assert.equal(draft.followup, choice.followups[0].id);
  assert.throws(() => respondToNewInformation(choice, draft, '__unknown-response__'), /unknown response/i);
  assert.equal(draft.followup, choice.followups[0].id, 'An invalid response must preserve the prior selection');
  const otherActionId = SIMULATIONS[0].choices[1].followups.find(item => !choice.followups.some(own => own.id === item.id))?.id;
  assert.ok(otherActionId, 'The fixture needs a response belonging only to another action');
  assert.throws(() => respondToNewInformation(choice, draft, otherActionId), /unknown response/i);
});

test('every authored follow-up can be selected and revised after reveal', () => {
  for (const scenario of SIMULATIONS) {
    for (const choice of scenario.choices) {
      const draft = { ...createDraft(), likely: 'An immediate possibility.', alternative: 'A different later possibility.' };
      revealDraft(draft);
      for (const followup of choice.followups) {
        assert.deepEqual(respondToNewInformation(choice, draft, followup.id), followup);
        assert.equal(draft.followup, followup.id);
      }
    }
  }
});

test('separate drafts do not share predictions, reveal state, or follow-up selection', () => {
  const first = createDraft();
  const second = createDraft();
  const secondBefore = { ...second };
  first.likely = 'First action prediction.';
  first.alternative = 'First action alternative.';
  first.check = 'Check the first action assumption.';
  revealDraft(first);
  respondToNewInformation(SIMULATIONS[0].choices[0], first, SIMULATIONS[0].choices[0].followups[0].id);
  assert.deepEqual(second, secondBefore);
  const firstBefore = { ...first };
  second.likely = 'A different action prediction.';
  second.alternative = 'A different action alternative.';
  revealDraft(second);
  assert.deepEqual(first, firstBefore);
  assert.equal(second.followup, null);
  assert.notStrictEqual(first, second);
});

// These checks cover the authored static HTML. Browser behavior and rendered layout
// still need the separate desktop/mobile review used before publication.
function tags(html) {
  return [...html.matchAll(/<([a-z][\w-]*)\b([^>]*?)>/gi)].map(([, name, source]) => ({
    name: name.toLowerCase(),
    attrs: Object.fromEntries([...source.matchAll(/\b([a-z][\w:-]*)\s*=\s*(?:"([^"]*)"|'([^']*)')/gi)]
      .map(([, key, double, single]) => [key.toLowerCase(), double ?? single])),
  }));
}

async function existingLocalTarget(reference, source) {
  assert.ok(reference.trim(), `Empty reference in ${source.pathname}`);
  const target = new URL(reference.replaceAll('&amp;', '&'), source);
  if (target.protocol !== 'file:') return null;
  const path = fileURLToPath(target);
  const withinRepo = relative(fileURLToPath(ROOT), path);
  assert.ok(withinRepo && !withinRepo.startsWith('..'), `Reference leaves the repository: ${reference}`);
  assert.ok((await stat(path)).isFile(), `Missing local file: ${reference}`);
  if (target.hash) {
    const ids = new Set(tags(await readFile(path, 'utf8')).map(tag => tag.attrs.id).filter(Boolean));
    assert.ok(ids.has(decodeURIComponent(target.hash.slice(1))), `Missing local anchor: ${reference}`);
  }
  target.hash = '';
  target.search = '';
  return target;
}

test('the page has valid local links, assets, labels, and a complete browser-module graph', async () => {
  const html = await readFile(PAGE, 'utf8');
  const pageTags = tags(html);
  const allIds = pageTags.map(tag => tag.attrs.id).filter(Boolean);
  const ids = new Set(allIds);
  assert.equal(ids.size, allIds.length, 'Duplicate HTML IDs');
  assert.ok(!html.includes('/Users/') && !html.includes('teaching-fall-2026-roster'), 'Private paths or HQ links on the student page');
  const modules = [];
  let stylesheets = 0;
  for (const { name, attrs } of pageTags) {
    for (const key of ['aria-labelledby', 'aria-describedby', 'aria-controls']) {
      for (const id of (attrs[key] || '').split(/\s+/).filter(Boolean)) assert.ok(ids.has(id), `Missing ${key} target: ${id}`);
    }
    if (attrs.for) assert.ok(ids.has(attrs.for), `Missing form-label target: ${attrs.for}`);
    const reference = attrs.src ?? attrs.href;
    if (['a', 'link'].includes(name)) assert.ok(reference, `<${name}> needs a destination`);
    if (reference !== undefined) {
      const target = await existingLocalTarget(reference, PAGE);
      if (name === 'script' && attrs.type === 'module' && target) modules.push(target);
      if (name === 'link' && attrs.rel === 'stylesheet' && target) stylesheets++;
    }
  }
  assert.ok(stylesheets > 0, 'Missing local stylesheet');
  assert.ok(modules.length > 0, 'Missing local browser-module entry point');
  const visited = new Set();
  while (modules.length) {
    const module = modules.pop();
    if (visited.has(module.href)) continue;
    visited.add(module.href);
    const source = await readFile(module, 'utf8');
    for (const [, id] of source.matchAll(/\$\(\s*['"]([^'"]+)['"]\s*\)/g)) {
      assert.ok(ids.has(id), `Browser module references a missing HTML element: ${id}`);
    }
    for (const [, specifier] of source.matchAll(/^\s*import\s+(?:[^'";]+?\s+from\s+)?['"]([^'"]+)['"]/gm)) {
      assert.ok(specifier.startsWith('.'), `Expected a local browser import: ${specifier}`);
      const target = await existingLocalTarget(specifier, module);
      assert.ok(target, `Missing local browser import: ${specifier}`);
      modules.push(target);
    }
  }
  assert.ok(visited.has(new URL('buen-594-resources/ethics-assets/simulation-data.mjs', ROOT).href), 'The page must load its scenario data');
  assert.ok(visited.has(new URL('buen-594-resources/ethics-assets/simulation-state.mjs', ROOT).href), 'The page must use the tested interaction state');
});
