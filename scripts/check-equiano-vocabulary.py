from pathlib import Path
import json,runpy,hashlib
r=Path(__file__).resolve().parents[1];d=json.loads((r/'frst-110-resources/equiano-vocabulary-assets/words.json').read_text())
assert len(d)>=150 and len({x['id'] for x in d})==len(d)
assert len([x for x in d if x['category'].startswith('Feelings')])>=40
assert {o['chapter'] for x in d for o in x['occurrences']}=={5,6}
for x in d:
 assert x['definition'] and x['occurrences']
 for o in x['occurrences']:assert x['term'].lower() in o['phrase'].lower(),x['term']
p=r/'frst-110-resources/equiano-vocabulary-5-6.html';before=p.read_bytes();runpy.run_path(str(r/'scripts/build-equiano-vocabulary.py'));assert before==p.read_bytes(),'Generated page out of sync'
s=before.decode()
for f in ['/Users/','private-data/','Mock-Filled','<iframe']:assert f not in s,f
j=json.loads((r/'data/frst-110.json').read_text());day=next(x for x in j['schedule'] if x['date']=='2026-11-02');assert any('equiano-vocabulary-5-6.html' in x['href'] for x in day['materials'])
print(f'{len(d)} sourced entries, emotional vocabulary, both chapters, reproducible build, public boundaries and dated course link passed.')
