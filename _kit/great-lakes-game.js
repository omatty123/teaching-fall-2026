(() => {
  'use strict';
  const {items,geojson} = window.pageConfig;
  const $=id=>document.getElementById(id);
  const names={area:'Lakes & bays',water:'Connecting waters',cut:'Canals',port:'Cities & ports'};
  const map=L.map('satellite-map',{center:[45.2,-84],zoom:6,zoomControl:false,attributionControl:true,minZoom:4,maxZoom:17,zoomSnap:.25,scrollWheelZoom:true});
  map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
  const imagery=L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:19,maxZoom:19,attribution:'Imagery © Esri, Vantor, Earthstar Geographics, GIS User Community · Features © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
  let loadedTiles=0,failedTiles=0;
  imagery.on('tileload',()=>{loadedTiles++;$('tile-status').hidden=true;});
  imagery.on('tileerror',()=>{failedTiles++;if(!loadedTiles){$('tile-status').hidden=false;$('tile-status').textContent='Satellite imagery is unavailable. Check your connection and reload.';}});
  const cityLayers=new Map();
  L.geoJSON(geojson,{interactive:false,style:feature=>feature.properties.kind==='city'?{color:'#ffd27b',weight:1.7,fillOpacity:.08,fillColor:'#ffc65a'}:{color:feature.properties.kind==='cut'?'#ffd27b':'#87e1f4',weight:1.8,opacity:.9},onEachFeature:(feature,layer)=>{
    if(feature.properties.kind==='city') {cityLayers.set(feature.properties.id,layer);layer.on('add',()=>layer.getElement()?.setAttribute('data-city',feature.properties.id));}
  }}).addTo(map);
  const markers=new Map(),mapPins=new Map();
  for(const item of items){
    const pin=L.marker([item.lat,item.lon],{icon:L.divIcon({className:`gl-pin ${item.kind}`,html:`<button type="button" class="gl-marker ${item.kind}" data-id="${item.id}" aria-label="Location ${item.id}">${item.id}</button>`,iconSize:[28,28],iconAnchor:[14,14]}),keyboard:false,riseOnHover:true}).addTo(map);
    const button=pin.getElement().querySelector('button');L.DomEvent.disableClickPropagation(button);
    button.addEventListener('click',()=>choose(item.id));
    button.addEventListener('focus',()=>{if(!map.getBounds().contains(pin.getLatLng()))map.panTo(pin.getLatLng(),{animate:false});});
    markers.set(item.id,button);mapPins.set(item.id,pin);
  }
  L.control.scale({imperial:false,position:'bottomright',maxWidth:100}).addTo(map);
  for (const [kind,label] of Object.entries(names)) {
    const group=document.createElement('div'); group.className='gl-study-group';
    const heading=document.createElement('h3'); heading.textContent=label; group.appendChild(heading);
    for (const item of items.filter(i=>i.kind===kind)) {
      const button=document.createElement('button'); button.type='button';
      const number=document.createElement('span'); number.textContent=item.id;
      button.append(number,document.createTextNode(item.name));
      button.addEventListener('click',()=>{ studySelect(item.id); panTo(item.id,true); if(matchMedia('(max-width:700px)').matches)toggleList(false); });
      group.appendChild(button);
    }
    $('study-list').appendChild(group);
  }
  function shuffled(ids) {
    const result=[...ids];
    for (let i=result.length-1;i>0;i--) { const j=Math.floor(Math.random()*(i+1)); [result[i],result[j]]=[result[j],result[i]]; }
    return result;
  }
  let mode='play', queue=[], index=0, firstTry=0, missed=new Set(), attempted=false, resolved=false, finished=false, round=0, points=0, streak=0, autoTimer=null, revealed=false;
  let savedFeedback=null;
  let soundOn=true, audioContext=null;
  const current=()=>items.find(item=>item.id===queue[index]);
  function clearMap() { for (const marker of markers.values()) marker.classList.remove('is-correct','is-wrong','is-selected'); for(const layer of cityLayers.values())layer.setStyle({color:'#ffd27b',weight:1.7,fillOpacity:.08}); }
  function highlightCity(id) {cityLayers.get(id)?.setStyle({color:'#bdf468',weight:3,fillOpacity:.2});}
  function cancelAdvance(){ clearTimeout(autoTimer); autoTimer=null; }
  function scheduleAdvance(){ cancelAdvance(); if(mode==='play' && resolved && !revealed && !finished) autoTimer=setTimeout(advance,1150); }
  function sound(type){
    if(!soundOn) return;
    try {
      const Audio=window.AudioContext||window.webkitAudioContext;
      if(!Audio) return;
      audioContext ||= new Audio(); audioContext.resume().catch(()=>{});
      // Each first-try answer lifts the chime a full semitone. Starting
      // at middle C keeps all 24 steps and milestone flourishes comfortable.
      const root=261.63*2**(Math.min(23,Math.max(0,streak-1))/12);
      const milestone=type==='correct'&&streak>0&&streak%5===0;
      const intervals=milestone?(streak%10===0?[1,1.25,1.5,2,1.5,2]:[1,1.25,1.5,2]):[1,1.25,1.5];
      const frequencies=type==='wrong'?[180,125]:type==='finish'?[523.25,659.25,783.99,1046.5]:intervals.map(interval=>root*interval);
      const spacing=milestone?.09:.075;
      frequencies.forEach((frequency,i)=>{
        const oscillator=audioContext.createOscillator(), gain=audioContext.createGain(), at=audioContext.currentTime+i*spacing;
        oscillator.type='sine';oscillator.frequency.value=frequency;
        gain.gain.setValueAtTime(0,at);gain.gain.linearRampToValueAtTime(.09,at+.012);gain.gain.exponentialRampToValueAtTime(.001,at+.22);
        oscillator.connect(gain);gain.connect(audioContext.destination);oscillator.start(at);oscillator.stop(at+.24);
      });
    } catch(_) { /* Play remains available when audio is unavailable. */ }
  }
  function scoreDisplay(){ $('points').textContent=points; $('streak').textContent=streak; }
  function celebrate(){
    const badge=$('map-celebration');badge.classList.remove('show');void badge.offsetWidth;
    badge.textContent=streak>0&&streak%10===0?`${streak} straight — unstoppable!`:streak>0&&streak%5===0?`${streak} in a row — on fire!`:streak>=2?`${streak} in a row!`:'Nice find!';badge.classList.add('show');
  }

  function say(message,tone='neutral') { $('feedback').textContent=message; $('feedback').dataset.tone=tone; }
  let overviewView=null;
  function resetZoom(){
    const shortPhone=innerWidth<=700&&innerHeight<=550;
    if(innerWidth>700){
      // Fit the actual lake region tightly to the current screen.
      map.fitBounds([[41.30,-92.3],[49.05,-75.7]],{paddingTopLeft:[20,25],paddingBottomRight:[20,30],animate:false});
    } else {
      map.fitBounds([[41.45,-92.3],[49.05,-75.7]],{paddingTopLeft:[shortPhone?15:35,shortPhone?125:80],paddingBottomRight:shortPhone?[265,20]:[35,Math.min(220,innerHeight*.28)],animate:false});
    }
    $('detail-view').value='';
    overviewView={center:map.getCenter(),zoom:map.getZoom()};
  }
  function panTo(id,detail=false){
    const item=items.find(i=>i.id===id);
    map.setView([item.lat,item.lon],detail?(item.kind==='port'?10:item.kind==='area'?7:9):map.getZoom(),{animate:!matchMedia('(prefers-reduced-motion:reduce)').matches});
  }
  function updateMapControls(){
    $('zoom-out').disabled=map.getZoom()<=4;$('zoom-in').disabled=map.getZoom()>=17;
    const compact=map.getZoom()<6.5;
    for(const item of items){const el=markers.get(item.id);el.classList.toggle('is-compact',compact&&[11,12,13,15,21,23].includes(item.id));}
  }
  map.on('zoomend',updateMapControls);
  $('zoom-in').addEventListener('click',()=>map.zoomIn());
  $('zoom-out').addEventListener('click',()=>map.zoomOut());
  $('zoom-reset').addEventListener('click',resetZoom);
  $('detail-view').addEventListener('change',e=>{
    const regions={chicago:[41.8,-87.8],detroit:[42.45,-82.85],niagara:[43.07,-79.12]};
    if(regions[e.target.value])map.setView(regions[e.target.value],9,{animate:false});
  });
  function toggleList(show){$('study-index').hidden=!show;$('show-study').hidden=mode!=='study'||show;}
  $('close-study').addEventListener('click',()=>toggleList(false));
  $('show-study').addEventListener('click',()=>toggleList(true));
  window.addEventListener('resize',()=>{
    const atOverview=overviewView&&map.getZoom()===overviewView.zoom&&map.getCenter().equals(overviewView.center,1e-6);
    map.invalidateSize();
    if(atOverview)resetZoom();
  });
  $('sound-toggle').addEventListener('click',()=>{
    soundOn=!soundOn;$('sound-toggle').setAttribute('aria-pressed',soundOn);$('sound-toggle').setAttribute('aria-label',soundOn?'Sound effects on; click to mute':'Sound effects off; click to enable');
    $('sound-toggle').querySelector('span').textContent=soundOn?'Sound on':'Sound off';if(soundOn)sound('correct');
  });
  function focusPrompt() { $('place-name').focus({preventScroll:true}); }
  function updateScore() { $('score').textContent=`${firstTry} of ${index+(resolved?1:0)} found on the first try`; }
  function renderQuestion() {
    clearMap();
    $('map-celebration').classList.remove('show');
    $('round-label').textContent=round===1?'Full map round':`Practice round ${round}`;
    $('progress-text').textContent=`${index+1} / ${queue.length}`;
    $('round-progress').max=queue.length; $('round-progress').value=index;
    $('place-name').textContent=`Find ${current().name}`; $('place-category').textContent=names[current().kind];
    $('number-form').hidden=false; $('reveal').hidden=false; $('next').hidden=true;
    $('retry').hidden=true; $('restart').hidden=true;
    $('map-number').value='';
    say('Tap the number on the map.'); updateScore();
  }
  function start(ids=items.map(i=>i.id),practice=false) {
    cancelAdvance(); round=practice?round+1:1; points=0;streak=0;scoreDisplay();
    queue=shuffled(ids); index=0; firstTry=0; missed=new Set(); attempted=false; resolved=false; finished=false;revealed=false;
    resetZoom();renderQuestion();
  }
  function finish() {
    finished=true; cancelAdvance();clearMap();sound('finish');
    $('round-label').textContent=round===1?'Full map round':`Practice round ${round}`;
    $('round-progress').value=queue.length;
    $('progress-text').textContent=`${queue.length} / ${queue.length}`;
    $('place-name').textContent=missed.size?'You’re finding your way.':'You know this map.';
    $('place-category').textContent=`${firstTry} of ${queue.length} on the first try`;
    say(missed.size?`${missed.size} ${missed.size===1?'place is':'places are'} ready for another look. Practice just those, or try the full map again.`:'Every place found on the first try. Try another shuffled round whenever you’re ready.');
    $('number-form').hidden=true; $('reveal').hidden=true; $('next').hidden=true;
    $('retry').hidden=missed.size===0; $('restart').hidden=false; $('score').textContent='';
  }
  function complete(wasRevealed=false) {
    revealed=wasRevealed;
    resolved=true;
    markers.get(current().id).classList.add('is-correct');highlightCity(current().id);
    $('number-form').hidden=true; $('reveal').hidden=true; $('next').hidden=!revealed;
    $('next').innerHTML=index===queue.length-1?'See results <span aria-hidden="true">→</span>':'Next place <span aria-hidden="true">→</span>';
    $('round-progress').value=index+1;
    say(`${revealed?'Here it is':'Correct'} — ${current().name} is number ${current().id}.${revealed?' You’ll get another chance to practice it.':''}`,revealed?'neutral':'correct');
    updateScore();scheduleAdvance();
  }
  function choose(id) {
    if (mode==='study') { studySelect(id); return; }
    if (resolved||finished) return;
    const item=items.find(i=>i.id===id);
    if (!item) { say('Enter a map number from 1 to 24.','wrong'); return; }
    clearMap();
    if (id===current().id) {
      if (!attempted) firstTry++;
      points+=attempted?50:100;streak=attempted?0:streak+1;scoreDisplay();sound('correct');complete();celebrate();
    } else {
      attempted=true; missed.add(current().id);streak=0;scoreDisplay();sound('wrong');
      markers.get(id).classList.add('is-wrong');
      say(`That’s number ${id}, ${item.name}. Keep looking for ${current().name}.`,'wrong');
    }
  }
  function studySelect(id) {
    const item=items.find(i=>i.id===id); clearMap();
    markers.get(id).classList.add('is-selected');highlightCity(id);
    $('place-name').textContent=item.name; $('place-category').textContent=`Number ${id} · ${names[item.kind]}`;
    say(`Number ${id}: ${item.name}. The number is directly on this feature. Zoom in for a closer look.`);
  }
  function setMode(nextMode) {
    if (mode===nextMode) return;
    cancelAdvance();mode=nextMode;
    $('play-mode').setAttribute('aria-pressed',mode==='play');
    $('study-mode').setAttribute('aria-pressed',mode==='study');
    $('play-mode').textContent=mode==='study'?'Resume play':'Play';
    toggleList(mode==='study');
    for (const item of items) markers.get(item.id).setAttribute('aria-label',mode==='study'?`Location ${item.id}: ${item.name}`:`Location ${item.id}`);
    if (mode==='study') {
      savedFeedback={text:$('feedback').textContent,tone:$('feedback').dataset.tone};
      clearMap(); $('round-label').textContent='Study the map'; $('progress-text').textContent='24 places';
      $('round-progress').hidden=true;
      $('place-name').textContent='Where does the water go?'; $('place-category').textContent='Select any numbered marker';
      say('Click a marker to learn its name. The complete list is below the map.');
      for (const id of ['number-form','reveal','next','retry','restart']) $(id).hidden=true;
      $('score').textContent='Your round is paused.';
    } else {
      $('round-progress').hidden=false;
      if (finished) finish();
      else {
        renderQuestion();
        if (resolved) complete(attempted && savedFeedback.text.startsWith('Here it is'));
        else if (savedFeedback) say(savedFeedback.text,savedFeedback.tone);
      }
    }
  }
  $('number-form').addEventListener('submit',event=>{ event.preventDefault(); choose(Number($('map-number').value)); if(resolved) focusPrompt(); });
  function advance(){
    cancelAdvance();if(mode!=='play'||finished)return;
    $('map-celebration').classList.remove('show');
    index++;attempted=false;resolved=false;revealed=false;
    if(index===queue.length)finish();else{resetZoom();renderQuestion();}
    focusPrompt();
  }
  $('next').addEventListener('click',advance);
  $('reveal').addEventListener('click',()=>{
    if(mode!=='play'||resolved||finished) return;
    attempted=true;streak=0;scoreDisplay(); missed.add(current().id); clearMap(); complete(true); panTo(current().id,true); $('next').focus({preventScroll:true});
  });
  $('retry').addEventListener('click',()=>{start([...missed],true); focusPrompt();});
  $('restart').addEventListener('click',()=>{start(); focusPrompt();});
  $('study-mode').addEventListener('click',()=>setMode('study'));
  $('play-mode').addEventListener('click',()=>setMode('play'));
  $('gl-app').hidden=false;
  $('map-number').max=items.length;
  start();updateMapControls();
})();
