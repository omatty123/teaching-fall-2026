#!/usr/bin/env python3
"""Validate the public resource's navigation, provenance and content boundaries."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'frst-110-resources/narratives-of-slavery.html'
ASSETS = PAGE.parent / 'narratives-of-slavery-assets'
QUESTION = ('Why does it matter to make distinctions between different types of slavery, '
            'especially comparing present to the past, and chattel slavery?')

class Document(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.refs = []
        self.text = []
        self.articles = []
        self.headings = []
        self.article = None
        self.heading = None
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'article':
            self.article = {'id': attrs.get('id'), 'external': []}
            self.articles.append(self.article)
        if re.fullmatch(r'h[1-6]', tag):
            self.heading = {'tag': tag, 'text': [], 'attrs': attrs}
            self.headings.append(self.heading)
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append(attrs[key])
                if tag == 'a' and self.article is not None and attrs[key].startswith('https://'):
                    self.article['external'].append(attrs[key])
        assert tag not in ('form', 'input', 'textarea', 'iframe', 'script'), f'Unexpected active/public collection element: {tag}'
        assert not (tag == 'br' and self.heading is not None), 'Forced heading break'
    def handle_endtag(self, tag):
        if tag == 'article': self.article = None
        if re.fullmatch(r'h[1-6]', tag): self.heading = None
    def handle_data(self, text):
        self.text.append(text)
        if self.heading is not None: self.heading['text'].append(text)

html = PAGE.read_text()
doc = Document(html)
visible = ' '.join(' '.join(doc.text).split())
assert visible.count('?') == 1 and QUESTION in visible, 'Only the approved discussion question belongs here'
assert all(x in doc.ids for x in ('starting','discussion','sources','roots','amistad','twelve-years','django'))
assert {a['id'] for a in doc.articles} == {'roots','amistad','twelve-years','django'}, 'Additional examples are for students to find'
assert all(a['external'] for a in doc.articles), 'Every selected work needs adjacent evidence'
assert 'Life before capture' in visible or 'life before capture or enslavement' in visible
assert 'not a complete inventory' in visible and 'not a ranking of whose suffering matters' in visible
assert not re.search(r'/Users/|127\.0\.0\.1|localhost|teaching-notes/|private-data/|file://|\.config/|Bearer\s', html), 'Private/local material leaked into public page'
for ref in doc.refs:
    url = urlsplit(ref)
    if url.scheme:
        assert url.scheme == 'https', f'Non-HTTPS external URL: {ref}'
        continue
    target = (PAGE.parent / unquote(url.path)).resolve() if url.path else PAGE
    assert target.is_relative_to(ROOT), f'Reference escapes repository: {ref}'
    assert target.is_file(), f'Missing local reference: {ref}'
    if url.fragment and target.suffix == '.html':
        target_ids = doc.ids if target == PAGE else set(re.findall(r'\bid=["\']([^"\']+)', target.read_text()))
        assert url.fragment in target_ids, f'Missing fragment: {ref}'
css = (ASSETS / 'page.css').read_text()
for ref in re.findall(r'url\(["\']?([^"\')]+)', css):
    assert (ASSETS / ref).resolve().is_file(), f'Missing CSS asset: {ref}'
assert '@font-face' in css and 'sans-serif' in css
assert not re.search(r'(?<!sans-)\bserif\b|Georgia|Times New Roman', css), 'Unexpected serif typography'
ledger = json.loads((ASSETS / 'sources.json').read_text())
assert ledger['discussion_question'] == QUESTION
assert {w['id'] for w in ledger['works']} == {a['id'] for a in doc.articles}
ledger_urls = {s['url'] for w in ledger['works'] for s in w['sources']}
ledger_urls |= {s['url'] for s in ledger['comparison_sources']}
ledger_urls |= {s['source'] for s in ledger['media']}
for article in doc.articles:
    assert all(url in ledger_urls for url in article['external']), f'Unrecorded source in {article["id"]}'
for media in ledger['media']:
    assert (ASSETS / media['path']).resolve().is_file(), 'Missing cited image'
    assert media['license'] and media['source'].startswith('https://')
print('Narratives of Slavery: 4 class-named works, approved discussion, local links/anchors, fonts and privacy checks passed.')
