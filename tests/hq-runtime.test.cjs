const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, '_kit/hq.js'), 'utf8');
const term = JSON.parse(fs.readFileSync(path.join(root, 'data/term.json')));
const minute = value => value.split(':').reduce((h, m) => Number(h) * 60 + Number(m));
const config = Object.fromEntries(term.courseOrder.map(slug => {
  const c = JSON.parse(fs.readFileSync(path.join(root, `data/${slug}.json`)));
  return [c.key, { code: c.code, schedule: c.schedule, startMinutes: minute(c.meeting.start), endMinutes: minute(c.meeting.end), href: `https://example.test/courses/${slug}.html` }];
}));
function harness(date, failStorage = false, initialStorage = {}) {
  const listeners = {}, nodes = {}, stored = { ...initialStorage };
  let focused;
  class Node {
    constructor() { this.textContent = ''; this.hidden = true; this.dataset = {}; this.handlers = {}; this.buttons = []; }
    set innerHTML(value) {
      this.html = value;
      this.buttons = [...value.matchAll(/<button[^>]*data-(filter|task-id)="([^"]+)"/g)].map((m) => {
        const n = new Node(); n.dataset[m[1] === 'filter' ? 'filter' : 'taskId'] = m[2]; return n;
      });
    }
    get innerHTML() { return this.html; }
    querySelectorAll() { return this.buttons; }
    querySelector(selector) { return this.buttons.find(b => selector.includes(b.dataset.filter)); }
    setAttribute(key, value) { this[key] = value; }
    addEventListener(key, fn) { this.handlers[key] = fn; }
    closest() { return this; }
    focus() { focused = this; }
  }
  for (const id of ['todoList', 'todoFilters', 'priorityTask', 'priorityDetail', 'priorityLink', 'todoCount', 'todoStorageError', 'todoAnnouncement', 'dateLabel', 'nowTitle', 'nowDetail', 'nextTitle', 'nextDetail']) nodes[id] = new Node();
  for (const key of Object.keys(config)) for (const suffix of ['Date', 'Topic', 'MeetingLabel']) nodes[key + suffix] = new Node();
  const document = { hidden: false, getElementById: id => nodes[id], querySelectorAll: () => [], querySelector: () => null, addEventListener: (key, fn) => listeners[key] = fn };
  let current = date;
  class Clock extends Date { constructor(...args) { super(...(args.length ? args : [current])); } }
  const window = { courseConfig: config, taskBoardConfig: term.taskBoard, location: { hash: '' }, setInterval: fn => listeners.interval = fn, addEventListener: (key, fn) => listeners[key] = fn };
  vm.runInNewContext(source, { window, document, Date: Clock, Intl, localStorage: { getItem: key => stored[key] || null, setItem: (key, value) => { if (failStorage) throw new Error('QuotaExceededError'); stored[key] = value; } } });
  return { nodes, listeners, focused: () => focused, setDate: value => current = value,
    complete: id => { const button = nodes.todoList.buttons.find(b => b.dataset.taskId === id); assert.ok(button); nodes.todoList.handlers.click({ target: button }); } };
}
test('opening dates are campus dates even when the host timezone differs', () => {
  const h = harness('2026-09-04T20:00:00Z');
  assert.match(h.nodes.frstDate.textContent, /Sep 11/);
  assert.match(h.nodes.histDate.textContent, /Sep 15/);
  assert.match(h.nodes.buenDate.textContent, /Sep 15/);
});
test('Tuesday switches to BUEN when HIST ends, using Chicago time', () => {
  const h = harness('2026-09-15T17:10:00Z');
  assert.match(h.nodes.nextTitle.textContent, /BUEN/);
  assert.match(h.nodes.histDate.textContent, /Sep 17/);
});
test('returning to an old tab refreshes the calendar; end of term is explicit', () => {
  const h = harness('2026-09-15T15:00:00Z');
  h.setDate('2026-12-01T18:00:00Z'); h.listeners.visibilitychange();
  assert.equal(h.nodes.nextTitle.textContent, 'Term complete');
  assert.equal(h.nodes.buenDate.textContent, 'Term complete');
});
test('completing priority changes title, description, destination and keeps focus', () => {
  const h = harness('2026-09-04T20:00:00Z');
  h.complete('frst-delta-listening');
  assert.equal(h.nodes.priorityTask.textContent, 'Test the first three course-pack readings');
  assert.equal(h.nodes.priorityDetail.textContent, 'Open each reading in student context and confirm that access works.');
  assert.match(h.nodes.priorityLink.href, /hist-212/);
  assert.ok(h.focused());
});
test('blocked storage retains check for this tab and explains unsaved state', () => {
  const h = harness('2026-09-04T20:00:00Z', true);
  assert.doesNotThrow(() => h.complete('frst-delta-listening'));
  assert.equal(h.nodes.todoStorageError.hidden, false);
  assert.match(h.nodes.todoStorageError.textContent, /could not be saved/);
  assert.equal(h.nodes.priorityTask.textContent, 'Test the first three course-pack readings');
});
test('all completed tasks clear the previous priority instructions', () => {
  const saved = Object.fromEntries(term.taskBoard.items.map(item => [item.id, true]));
  const h = harness('2026-09-04T20:00:00Z', false, { 'fall-2026-teaching-hq-task-state-v2': JSON.stringify(saved) });
  assert.equal(h.nodes.priorityTask.textContent, 'No open term decisions');
  assert.match(h.nodes.priorityDetail.textContent, /All decisions/);
});
