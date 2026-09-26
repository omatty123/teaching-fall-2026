'use strict';
const data=JSON.parse(document.getElementById('reader-data').textContent);
const byNote=Object.fromEntries(data.notes.map(n=>[n.id,n]));
const byVerse=Object.fromEntries(data.verses.map(v=>[v.ref,v.text]));
const panel=document.getElementById('note-panel');
const content=document.getElementById('note-content');
const initialContent=content.innerHTML;
let lastTrigger=null;
const mobile=()=>window.matchMedia('(max-width:760px)').matches;
const verseId=ref=>'v-'+ref.replace(':','-');
function el(tag,text,className){const e=document.createElement(tag);if(text)e.textContent=text;if(className)e.className=className;return e;}
function clearSelection(){document.querySelectorAll('.verse.active,.phrase.selected').forEach(e=>e.classList.remove('active','selected'));document.querySelectorAll('[data-note][aria-expanded=true]').forEach(e=>e.setAttribute('aria-expanded','false'));}
function openNote(id,ref,trigger,scroll=false){
 const note=byNote[id];if(!note)return;
 ref=ref||note.refs[0];lastTrigger=trigger||document.querySelector(`#${verseId(ref)} .verse-number`);
 clearSelection();document.getElementById(verseId(ref))?.classList.add('active');
 document.querySelectorAll('[data-note]').forEach(e=>{if(e.dataset.note===id&&e.dataset.ref===ref){e.setAttribute('aria-expanded','true');if(e.classList.contains('phrase'))e.classList.add('selected');}});
 document.getElementById('note-label').textContent=note.kind==='Uncertain'?'Interpretation · uncertain':note.kind+' note';
 content.replaceChildren(el('p','Genesis '+ref,'note-ref'),el('h3',note.title),el('p',note.body));
 if(note.action){const labels={'two-texts':'Compare Genesis and Gilgamesh','clean-animals':'More on clean and unclean animals',questions:'Read the confusing-parts questions',maps:'Explore the terrain maps',timeline:'Follow the flood sequence',family:'See Noah’s family',covenant:'See who the covenant includes',compare:'Compare before and after',birds:'Follow the birds'};const a=el('a',labels[note.action]+' →','note-action');a.href='#'+note.action;a.addEventListener('click',()=>closeNote(false));content.append(a);}
 if(note.source){const p=el('p',null,'note-source'),a=el('a','Source for this explanation ↗');a.href=note.source;p.append(a);content.append(p);}
 const related=data.notes.filter(n=>n.id!==id&&n.refs.includes(ref));
 if(related.length){const wrap=el('div',null,'related');wrap.append(el('strong','Also at this verse'));related.forEach(n=>{const b=el('button',n.title);b.type='button';b.addEventListener('click',()=>openNote(n.id,ref,lastTrigger));wrap.append(b);});content.append(wrap);}
 panel.classList.add('is-open');document.body.classList.add('note-open');panel.scrollTop=0;
 history.replaceState(null,'','#'+verseId(ref));
 if(scroll||mobile()){requestAnimationFrame(()=>document.getElementById(verseId(ref))?.scrollIntoView({block:'start',behavior:'instant'}));}
}
function closeNote(restoreFocus=true){panel.classList.remove('is-open');document.body.classList.remove('note-open');clearSelection();document.getElementById('note-label').textContent='Reading notes';content.innerHTML=initialContent;bindNoteButtons(content);if(restoreFocus)lastTrigger?.focus({preventScroll:true});}
function bindNoteButtons(root){root.querySelectorAll('[data-note]').forEach(b=>b.addEventListener('click',()=>openNote(b.dataset.note,b.dataset.ref,b,b.classList.contains('sample-note'))));}
bindNoteButtons(document);
document.getElementById('close-note').addEventListener('click',()=>closeNote());
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&panel.classList.contains('is-open'))closeNote();});
document.getElementById('show-highlights').addEventListener('change',e=>document.querySelector('.scripture').classList.toggle('no-highlights',!e.target.checked));
document.querySelectorAll('[data-open-note]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();openNote(a.dataset.openNote,a.dataset.ref,a,true);}));
function followHash(){const match=location.hash.match(/^#v-(\d+)-(\d+)$/);if(match){const ref=match[1]+':'+match[2],note=data.notes.find(n=>n.refs.includes(ref));if(note)openNote(note.id,ref,null,true);else closeNote(false);}else if(mobile())closeNote(false);}
window.addEventListener('hashchange',followHash);
if(location.hash.startsWith('#v-'))followHash();

const times=[
 {title:'The rain lasts forty days.',ref:'7:12',label:'The flood begins · 7:11–12',body:'Genesis 7:11 dates the beginning to Noah’s 600th year, second month, seventeenth day. Verse 12 measures the rain. It does not say that forty days later everyone leaves the ark.'},
 {title:'The water has its own duration.',ref:'7:24',label:'Prevailing waters · 7:24; 8:3',body:'The narrative gives 150 days of prevailing waters; 8:3 refers to the end of 150 days as the waters recede. Keep these references together rather than counting them as two separate 150-day periods.'},
 {title:'Resting on mountains is not leaving.',ref:'8:4',label:'Seventh month · day 17',body:'The ark comes to rest. Its occupants stay inside. The account still has drying, observation, birds, and an instruction to leave ahead of it.'},
 {title:'Noah gathers evidence from outside.',ref:'8:5',label:'Tenth month · day 1; then further waiting',body:'The mountaintops appear. Verse 8:6 adds another forty-day interval before Noah opens the window. The raven and the dove then provide information about conditions outside; see their sequence below.'},
 {title:'A view of drying ground.',ref:'8:13',label:'Year 601 · first month · day 1',body:'Noah removes the covering and looks. This observation is distinct from the later statement that the earth is dry and the command to leave.'},
 {title:'The earth is dry. The household leaves.',ref:'8:14',label:'Year 601 · second month · day 27',body:'The narrative has crossed into the next year of Noah’s life. In 8:15–19, God directs the household and the animals out, with instructions for life to multiply again.'}
];
function showTime(index){const t=times[index],out=document.getElementById('timeline-detail');out.replaceChildren(el('p',t.label,'eyebrow'),el('h3',t.title),el('p',t.body),el('blockquote',byVerse[t.ref]));const a=el('a','Read Genesis '+t.ref+' in context →','text-link');a.href='#'+verseId(t.ref);out.append(a);document.querySelectorAll('[data-time]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.time)===index)));}
document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>showTime(Number(b.dataset.time))));showTime(0);
const people={
 noah:{title:'Noah speaks the curse.',label:'Father · 9:24–27',body:'After waking, Noah speaks about Canaan, Shem, and Japheth. Distinguish the speaker here from the divine speech about the covenant earlier in the chapter.',ref:'9:25',note:'curse'},
 shem:{title:'Shem helps cover his father.',label:'Son · 9:23, 26',body:'Shem and Japheth carry a garment backward and cover Noah without looking at his nakedness. Shem then appears in Noah’s blessing.',ref:'9:23',note:'family'},
 ham:{title:'Ham sees and tells.',label:'Son; Canaan’s father · 9:22',body:'The narration says Ham sees his father’s nakedness and tells his brothers. Interpretations of the act differ; the passage’s brief wording leaves questions unresolved. It repeatedly identifies him as Canaan’s father.',ref:'9:22',note:'family'},
 japheth:{title:'Japheth acts with Shem.',label:'Son · 9:23, 27',body:'Japheth helps cover Noah. His name returns in the speech at 9:27. The pamphlet’s footnote identifies wordplay between his name and the Hebrew expression translated “make space for.”',ref:'9:27',note:'curse'},
 canaan:{title:'Canaan is Noah’s grandson.',label:'Ham’s son · 9:18, 25',body:'Noah’s curse names Canaan, although the preceding action is attributed to Ham. The passage does not fully explain that shift. It says nothing about skin color; later racial claims should not be inserted into the wording.',ref:'9:25',note:'curse'}
};
function showPerson(id){const p=people[id],out=document.getElementById('family-detail');out.replaceChildren(el('p',p.label,'eyebrow'),el('h3',p.title),el('p',p.body));const a=el('a','Read '+p.ref+' with its note →','text-link');a.href='#'+verseId(p.ref);a.addEventListener('click',e=>{e.preventDefault();openNote(p.note,p.ref,a,true);});out.append(a);document.querySelectorAll('[data-person]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.person===id)));}
document.querySelectorAll('[data-person]').forEach(b=>b.addEventListener('click',()=>showPerson(b.dataset.person)));showPerson('noah');

let mapsStarted=false,regional,highland;const markers={};
const places={uruk:{name:'Uruk',ll:[31.32337501090747,45.6390521574333],text:'Gilgamesh’s city.',direction:'right'},shuruppak:{name:'Shuruppak',ll:[31.77752465,45.510467950000006],text:'Uta-napishti’s city in the flood account.',direction:'left'},nineveh:{name:'Nineveh',ll:[36.36076152375775,43.159936889690734],text:'Findspot of the famous Tablet XI manuscript.',direction:'right'}};
function initMaps(){
 if(mapsStarted)return;mapsStarted=true;
 if(!window.L){document.querySelectorAll('.map-loading').forEach(e=>e.textContent='The interactive map could not load. Place descriptions and source links remain available below.');return;}
 const attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, SRTM | <a href="https://opentopomap.org">OpenTopoMap</a> (CC-BY-SA)';
 let failures=0;
 function makeMap(id,bounds){document.getElementById(id).replaceChildren();const m=L.map(id,{scrollWheelZoom:false}).fitBounds(bounds,{padding:[10,10]});L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',{attribution,maxZoom:14,subdomains:'abc'}).on('tileerror',()=>{failures++;if(failures>5)document.getElementById('map-status').textContent='Some terrain tiles could not load. The city markers, river overlay, and written place descriptions are still available; try reloading for terrain.';}).addTo(m);L.control.scale({imperial:false}).addTo(m);return m;}
 regional=makeMap('regional-map',[[29,30],[42.5,50.5]]);highland=makeMap('ararat-map',[[37.6,41.5],[40.8,45.9]]);
 L.rectangle([[37.6,41.5],[40.8,45.9]],{color:'#263b46',weight:2,fillOpacity:.02,dashArray:'5 5'}).bindTooltip('Highland detail shown below').addTo(regional);
 Object.entries(places).forEach(([id,p])=>{markers[id]=L.circleMarker(p.ll,{radius:5,color:'#fff',weight:1.5,fillColor:'#174e70',fillOpacity:1}).bindTooltip(p.name,{permanent:true,direction:p.direction,className:'place-label',offset:[p.direction==='left'?-5:5,0]}).bindPopup('<strong>'+p.name+'</strong><br>'+p.text).addTo(regional);});
 fetch('genesis-assets/rivers.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(g=>L.geoJSON(g,{style:{color:'#3784a0',weight:2,opacity:.85},onEachFeature:(f,l)=>{if(f.properties?.name){l.bindTooltip(f.properties.name);if(['Euphrates','Tigris'].includes(f.properties.name)){const points=f.geometry.coordinates.flat(),target=f.properties.name==='Tigris'?34.5:33.8,point=points.reduce((best,p)=>Math.abs(p[1]-target)<Math.abs(best[1]-target)?p:best);L.tooltip({permanent:true,direction:f.properties.name==='Tigris'?'right':'left',className:'river-label'}).setLatLng([point[1],point[0]]).setContent(f.properties.name).addTo(regional);}}}}).addTo(regional)).catch(()=>{});
}
const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){initMaps();observer.disconnect();}},{rootMargin:'300px'});observer.observe(document.getElementById('maps'));
document.getElementById('reset-region').addEventListener('click',()=>{initMaps();if(regional){regional.fitBounds([[29,30],[42.5,50.5]],{padding:[10,10]});regional.closePopup();document.querySelectorAll('[data-place]').forEach(b=>b.classList.remove('active'));}});
document.querySelectorAll('[data-place]').forEach(b=>b.addEventListener('click',()=>{initMaps();if(!regional)return;const id=b.dataset.place;regional.setView(places[id].ll,7);markers[id].openPopup();document.querySelectorAll('[data-place]').forEach(x=>x.classList.toggle('active',x===b));}));
// Printing includes the complete note index, not only the selected explanation.
let openBeforePrint=[];const details=[...document.querySelectorAll('.notes-index details,.confusing-parts details,.footnote-lab details')];
window.addEventListener('beforeprint',()=>{openBeforePrint=details.map(d=>d.open);details.forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>details.forEach((d,i)=>d.open=openBeforePrint[i]));
document.getElementById('print-reader').addEventListener('click',()=>window.print());
