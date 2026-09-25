'use strict';
const places={
shuruppak:{name:'Shuruppak',coord:[45.5112,31.7772],kind:'Story',text:'Uta-napishti begins his account in this city on the Euphrates. The ancient site is Tell Fara, in southern Iraq.',source:'https://pleiades.stoa.org/places/326150788',offset:[14,-14]},
uruk:{name:'Uruk',coord:[45.6394,31.3234],kind:'Story',text:'Gilgamesh’s city, now the archaeological site of Warka in southern Iraq. Tablet XI ends with his return and attention to the city’s walls.',source:'https://pleiades.stoa.org/places/912986',offset:[14,24]},
nineveh:{name:'Nineveh',coord:[43.1621,36.3583],kind:'Findspot',text:'The tablet was found here, near modern Mosul in northern Iraq, among the remains of Ashurbanipal’s library. This is the manuscript’s findspot, not the city where Uta-napishti begins the flood story.',source:'https://pleiades.stoa.org/places/874621',offset:[14,-14]},
london:{name:'London',coord:[-.1269,51.5194],kind:'Museum',text:'The British Museum holds the Flood Tablet, K.3375. The wider view shows the distance between its Iraqi findspot and its present collection; it does not trace the historical shipping route.',source:'https://www.britishmuseum.org/collection/object/W_K-3375',offset:[14,-14]}
};
let selected='shuruppak',wide=false,countries,rivers;
const svg=document.getElementById('map'),NS='http://www.w3.org/2000/svg';
function elem(tag,attrs={},text){const e=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));if(text)e.textContent=text;return e;}
function merc(lat){return Math.log(Math.tan(Math.PI/4+Math.max(-85,Math.min(85,lat))*Math.PI/360))*180/Math.PI;}
function projection(bounds,w,h,pad=28){let[x0,y0,x1,y1]=bounds;const m0=merc(y0),m1=merc(y1),s=Math.min((w-2*pad)/(x1-x0),(h-2*pad)/(m1-m0));const ox=(w-s*(x1-x0))/2,oy=(h-s*(m1-m0))/2;return c=>[ox+(c[0]-x0)*s,oy+(m1-merc(c[1]))*s];}
function geometryPath(g,p){let lines,close=false;if(g.type==='Polygon'){lines=g.coordinates;close=true;}else if(g.type==='MultiPolygon'){lines=g.coordinates.flat();close=true;}else if(g.type==='LineString')lines=[g.coordinates];else if(g.type==='MultiLineString')lines=g.coordinates;else return '';return lines.map(l=>l.map((c,i)=>{const[x,y]=p(c);return `${i?'L':'M'}${x.toFixed(2)},${y.toFixed(2)}`;}).join(' ')+(close?'Z':'')).join(' ');}
function label(parent,p,c,text,cls){const[x,y]=p(c);parent.append(elem('text',{x,y,class:`map-label ${cls}`,'text-anchor':'middle'},text));}
function renderMap(){if(!countries)return;svg.replaceChildren();const W=Math.max(270,svg.getBoundingClientRect().width),H=W<500?400:520;svg.setAttribute('viewBox',`0 0 ${W} ${H}`);const p=projection(wide?[-12,24,54,57]:[35.3,28.3,51.5,39.3],W,H,24);const land=elem('g');countries.features.forEach(f=>land.append(elem('path',{d:geometryPath(f.geometry,p),fill:f.properties.name==='Iraq'?'#e9dcc3':'#f5f7f2',stroke:'#a8bdb9','stroke-width':1})));svg.append(land);rivers.features.forEach(f=>svg.append(elem('path',{d:geometryPath(f.geometry,p),fill:'none',stroke:'#388a9c','stroke-width':wide?1.6:3})));if(!wide){[[[43.8,33.7],'IRAQ'],[[39,35.2],'SYRIA'],[[40.8,38.8],'TÜRKIYE'],[[49.5,35.5],'IRAN'],[[42.2,29.6],'SAUDI ARABIA']].forEach(([c,t])=>label(svg,p,c,t,'country-label'));label(svg,p,[40.5,33.5],'Euphrates','river-label');label(svg,p,[45.3,35.1],'Tigris','river-label');label(svg,p,[49.2,28.8],'Persian Gulf','river-label');}else{[[[2,47],'FRANCE'],[[31,40],'TÜRKIYE'],[[42,33],'IRAQ'],[[49,34],'IRAN'],[[28,29],'EGYPT']].forEach(([c,t])=>label(svg,p,c,t,'country-label'));}
Object.entries(places).forEach(([id,a])=>{if(!wide&&id==='london')return;const[x,y]=p(a.coord),active=id===selected;const group=elem('g',{class:'map-marker',transform:`translate(${x},${y})`});group.append(elem('circle',{r:active?12:8,fill:a.kind==='Story'?'#a24823':'#075f74',stroke:'#fff','stroke-width':3}));if(active)group.append(elem('circle',{r:18,fill:'none',stroke:'#a24823','stroke-width':2}));let[dx,dy]=a.offset;if(W<500&&id==='shuruppak'){dx=-12;dy=-12;}if(W<500&&id==='uruk'){dx=8;dy=23;}if(wide&&id==='uruk'){dx=12;dy=27;}if(wide&&id==='shuruppak'){dx=-13;dy=8;}group.append(elem('text',{x:dx,y:dy,class:'map-label place-label','text-anchor':(wide||W<500)&&id==='shuruppak'?'end':'start'},a.name));group.addEventListener('click',()=>selectPlace(id));svg.append(group);});
const lat=wide?40:33,km=wide?1000:200,lonSpan=km/(111.32*Math.cos(lat*Math.PI/180)),len=p([lonSpan,lat])[0]-p([0,lat])[0];svg.append(elem('path',{d:`M22,${H-40} v7 h${len} v-7`,fill:'none',stroke:'#344e50','stroke-width':2}));svg.append(elem('text',{x:22,y:H-12,fill:'#344e50','font-size':15},`${km.toLocaleString()} km at ${lat}° N`));svg.setAttribute('aria-label',wide?'Map showing London in Britain and Nineveh, Shuruppak and Uruk in Iraq; no travel route is implied.':'Map of Mesopotamia with modern borders and rivers, Nineveh in the north and Shuruppak and Uruk in the south.');renderLocator();}
function renderLocator(){const loc=document.getElementById('locator');loc.replaceChildren();const p=projection([-20,-15,95,68],180,105,3);countries.features.forEach(f=>loc.append(elem('path',{d:geometryPath(f.geometry,p),fill:'#c4d3d0',stroke:'#eef3f2','stroke-width':.4})));const b=wide?[-12,24,54,57]:[35.3,28.3,51.5,39.3],a=p([b[0],b[3]]),z=p([b[2],b[1]]);loc.append(elem('rect',{x:a[0],y:a[1],width:z[0]-a[0],height:z[1]-a[1],fill:'none',stroke:'#a24823','stroke-width':2}));}
function setExtent(w){wide=w;document.getElementById('region-button').setAttribute('aria-pressed',String(!w));document.getElementById('wide-button').setAttribute('aria-pressed',String(w));renderMap();}
function selectPlace(id){selected=id;const a=places[id];document.querySelectorAll('[data-place]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.place===id)));document.getElementById('place-detail').innerHTML=`<h3>${a.name}</h3><p>${a.text}</p><p class="source"><a href="${a.source}">${id==='london'?'Museum record':'Site record at Pleiades'} ↗</a></p>`;if(id==='london')setExtent(true);else renderMap();}
document.querySelectorAll('[data-place]').forEach(b=>b.addEventListener('click',()=>selectPlace(b.dataset.place)));document.getElementById('region-button').addEventListener('click',()=>{if(selected==='london')selectPlace('nineveh');setExtent(false);});document.getElementById('wide-button').addEventListener('click',()=>setExtent(true));
Promise.resolve(['countries','rivers'].map(n=>JSON.parse(document.getElementById('map-data-'+n).textContent))).then(([c,r])=>{countries=c;rivers=r;selectPlace(selected);}).catch(()=>{svg.replaceChildren(elem('text',{x:30,y:70,fill:'#1b3438','font-size':20},'Map unavailable. Place descriptions and source links remain below.'));});

let resizeFrame;window.addEventListener('resize',()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(renderMap);});

const wordTracks=[...document.querySelectorAll('[data-word]')];
const wordLabels={gods:'ilū · the gods',smelled:'īṣīnū · smelled',fragrance:'irīša · its fragrance'};
function selectWord(key){wordTracks.forEach(t=>{const active=t.dataset.word===key;t.classList.toggle('is-active',active);t.querySelector('button').setAttribute('aria-pressed',String(active));});document.querySelectorAll('[data-photo-word]').forEach(r=>r.classList.toggle('is-active',r.dataset.photoWord===key));document.querySelectorAll('[data-drawing-word]').forEach(r=>r.classList.toggle('is-active',r.dataset.drawingWord===key));document.getElementById('drawing-caption').textContent=`Highlighted signs: ${wordLabels[key]}. Tablet XI 161, K.3375.`;document.getElementById('photo-caption').textContent=`Circled word group: ${wordLabels[key]}. Tablet XI 161, obverse iii 50a.`;}
wordTracks.forEach(t=>{t.querySelector('button').addEventListener('click',()=>selectWord(t.dataset.word));t.querySelector('button').addEventListener('focus',()=>selectWord(t.dataset.word));});
document.querySelectorAll('[data-photo-target]').forEach(r=>r.addEventListener('click',()=>selectWord(r.dataset.photoTarget)));
document.querySelectorAll('[data-drawing-target]').forEach(r=>r.addEventListener('click',()=>selectWord(r.dataset.drawingTarget)));
selectWord('gods');


const wordAudio=document.getElementById('word-audio');
const passageAudio=document.getElementById('akkadian-audio');
const soundButtons=[...document.querySelectorAll('[data-play-word]')];
const audioStatus=document.getElementById('word-audio-status');
const spokenWords={gods:'ilū',smelled:'īṣīnū',fragrance:'irīša'};
let playbackRequest=0;
function clearPlaying(){soundButtons.forEach(b=>{b.classList.remove('is-playing');b.querySelector('.sound-label').textContent='Reading · sound';});}
function finishWord(){clearPlaying();audioStatus.textContent='Press a reading card to hear that word from Karl Hecker’s recording.';}
soundButtons.forEach(button=>button.addEventListener('click',async()=>{
  const request=++playbackRequest,key=button.dataset.playWord;
  passageAudio.pause();wordAudio.pause();clearPlaying();selectWord(key);
  wordAudio.src=`gilgamesh-xi-assets/hecker-${key}.mp3`;
  button.classList.add('is-playing');button.querySelector('.sound-label').textContent='Playing…';
  audioStatus.textContent=`Playing ${spokenWords[key]} — ${wordLabels[key].split(' · ')[1]}.`;
  try{await wordAudio.play();}catch(error){if(request!==playbackRequest)return;clearPlaying();audioStatus.textContent='The word could not play. Try again, or use the recording below.';}
}));
wordAudio.addEventListener('ended',finishWord);
wordAudio.addEventListener('error',()=>{clearPlaying();audioStatus.textContent='The word could not load. Try the recording below.';});
passageAudio.addEventListener('play',()=>{++playbackRequest;wordAudio.pause();finishWord();});

// A single player for the five scholar name excerpts.
(function(){
  const audio=document.getElementById('cast-audio');
  const status=document.getElementById('cast-audio-status');
  const slow=document.getElementById('cast-slow');
  const buttons=[...document.querySelectorAll('.say')];
  let active=null,request=0;
  function reset(){
    buttons.forEach(b=>{b.classList.remove('is-playing');b.setAttribute('aria-pressed','false');b.querySelector('.say-icon').textContent='▶';});
    active=null;
  }
  function stop(){++request;audio.pause();reset();}
  slow.addEventListener('change',()=>{audio.playbackRate=slow.checked?.75:1;});
  buttons.forEach(button=>button.addEventListener('click',async()=>{
    if(active===button){stop();status.textContent='Stopped. Press a name to listen again.';return;}
    stop();const current=++request;
    ++playbackRequest;wordAudio.pause();passageAudio.pause();finishWord();
    active=button;audio.src=button.dataset.audio;audio.playbackRate=slow.checked?.75:1;audio.preservesPitch=true;
    button.classList.add('is-playing');button.setAttribute('aria-pressed','true');button.querySelector('.say-icon').textContent='■';
    status.textContent='Playing '+button.dataset.name+(slow.checked?' at ¾ speed.':'.');
    try{await audio.play();}catch(error){if(current!==request)return;reset();status.textContent='The sample could not play. Try again, or open the recording link beneath the name.';}
  }));
  audio.addEventListener('ended',()=>{const name=active?.dataset.name;reset();status.textContent=(name?name+': ':'')+'press the name again to repeat, or select slow playback.';});
  audio.addEventListener('error',()=>{reset();status.textContent='The sample could not load. Open the recording link beneath the name.';});
  [wordAudio,passageAudio].forEach(other=>other.addEventListener('play',()=>{if(active){stop();status.textContent='Name playback stopped while the tablet reading plays.';}}));
})();
