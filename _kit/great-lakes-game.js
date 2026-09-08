(() => {
  'use strict';
  const {items, lakes, channels, cities} = window.pageConfig;
  const $ = id => document.getElementById(id);
  const names = {area:'Lakes & bays', water:'Connecting waters', cut:'Canals', port:'Cities & ports'};
  const svgNS = 'http://www.w3.org/2000/svg';
  function svg(tag, attributes, parent) {
    const node = document.createElementNS(svgNS,tag);
    for (const [key,value] of Object.entries(attributes)) node.setAttribute(key,value);
    parent.appendChild(node);
    return node;
  }
  for (const d of lakes) svg('path',{d},$('lake-shapes'));
  for (const city of cities) for(const d of city.paths) svg('path',{d,'data-city':city.id},$('city-shapes'));
  for (const channel of channels) for(const d of channel.paths) svg('path',{d,class:channel.kind},$('channel-shapes'));
  const markers = new Map();
  for (const item of items) {
    const {id,kind,x,y} = item;
    const marker = svg('g', {class:`gl-marker ${kind}`,transform:`translate(${x} ${y})`,role:'button',tabindex:0,'aria-label':`Location ${id}`,'data-id':id},$('map-markers'));
    svg('circle',{r:12,class:'gl-hit'},marker);
    svg('text',{x:0,y:0,'aria-hidden':'true'},marker).textContent=id;
    marker.addEventListener('click',()=>choose(id));
    marker.addEventListener('keydown',event=>{
      if (event.key==='Enter'||event.key===' ') { event.preventDefault(); choose(id); }
    });
    markers.set(id,marker);
  }
  for (const [kind,label] of Object.entries(names)) {
    const group=document.createElement('div'); group.className='gl-study-group';
    const heading=document.createElement('h3'); heading.textContent=label; group.appendChild(heading);
    for (const item of items.filter(i=>i.kind===kind)) {
      const button=document.createElement('button'); button.type='button';
      const number=document.createElement('span'); number.textContent=item.id;
      button.append(number,document.createTextNode(item.name));
      button.addEventListener('click',()=>{ studySelect(item.id); panTo(item.id,true); });
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
  function clearMap() { for (const marker of markers.values()) marker.classList.remove('is-correct','is-wrong','is-selected'); document.querySelectorAll('[data-city]').forEach(p=>p.classList.remove('is-selected')); }
  function highlightCity(id) { document.querySelectorAll(`[data-city="${id}"]`).forEach(p=>p.classList.add('is-selected')); }
  function cancelAdvance(){ clearTimeout(autoTimer); autoTimer=null; }
  function scheduleAdvance(){ cancelAdvance(); if(mode==='play' && resolved && !revealed && !finished) autoTimer=setTimeout(advance,1150); }
  function sound(type){
    if(!soundOn) return;
    try {
      const Audio=window.AudioContext||window.webkitAudioContext;
      if(!Audio) return;
      audioContext ||= new Audio(); audioContext.resume().catch(()=>{});
      const frequencies=type==='wrong'?[180,125]:type==='finish'?[523.25,659.25,783.99,1046.5]:[523.25,659.25,783.99];
      frequencies.forEach((frequency,i)=>{
        const oscillator=audioContext.createOscillator(), gain=audioContext.createGain(), at=audioContext.currentTime+i*.075;
        oscillator.type='sine';oscillator.frequency.value=frequency;
        gain.gain.setValueAtTime(0,at);gain.gain.linearRampToValueAtTime(.09,at+.012);gain.gain.exponentialRampToValueAtTime(.001,at+.22);
        oscillator.connect(gain);gain.connect(audioContext.destination);oscillator.start(at);oscillator.stop(at+.24);
      });
    } catch(_) { /* Play remains available when audio is unavailable. */ }
  }
  function scoreDisplay(){ $('points').textContent=points; $('streak').textContent=streak; }
  function celebrate(){
    const badge=$('map-celebration');badge.classList.remove('show');void badge.offsetWidth;
    badge.textContent=streak>=3?`${streak} in a row!`:'Nice find!';badge.classList.add('show');
  }

  function say(message,tone='neutral') { $('feedback').textContent=message; $('feedback').dataset.tone=tone; syncMobile(); }
  function syncMobile() {
    $('mobile-prompt').textContent=(mode==='study'?'Study: ':'')+$('place-name').textContent;
    $('mobile-feedback').textContent=$('feedback').textContent;
    $('mobile-next').hidden=mode!=='play'||(!finished&&(!resolved||!revealed));
    $('mobile-next').textContent=finished?'Results →':'Next →';
  }
  const scroller=document.querySelector('.gl-map-scroll');
  let zoom=1;
  const baseWidth=()=>Math.max(900,scroller.clientWidth);
  function applyZoom(next,center=null){
    const oldScale=baseWidth()*zoom/1000;
    const target=center||[(scroller.scrollLeft+scroller.clientWidth/2)/oldScale,(scroller.scrollTop+scroller.clientHeight/2)/oldScale];
    zoom=Math.max(1,Math.min(10,next));
    $('lakes-map').style.width=`${baseWidth()*zoom}px`;
    for(const item of items) {
      const marker=markers.get(item.id);marker.setAttribute('transform',`translate(${item.x} ${item.y}) scale(${1/zoom})`);
      marker.querySelector('text').style.fontSize=zoom<1.6&&[11,12,13,15,21,23].includes(item.id)?'12px':'17px';
      marker.querySelector('.gl-hit').setAttribute('r',zoom<1.6?11:24);
    }
    const scale=baseWidth()*zoom/1000;
    scroller.scrollLeft=target[0]*scale-scroller.clientWidth/2;scroller.scrollTop=target[1]*scale-scroller.clientHeight/2;
    $('zoom-level').textContent=`${zoom.toFixed(zoom%1?1:0)}×`;
    $('zoom-out').disabled=zoom<=1;$('zoom-in').disabled=zoom>=10;
    const km=zoom>=6?20:zoom>=3?50:100;
    $('scale-rule').style.width=`${km*72/111.195*scale}px`;$('scale-label').textContent=`≈ ${km} km`;
  }
  function resetZoom(){applyZoom(1,[500,330]);}
  function panTo(id,detail=false) {
    const item=items.find(i=>i.id===id);
    applyZoom(detail?(item.kind==='port'?6:item.kind==='area'?2:4):zoom,[item.x,item.y]);
  }
  $('zoom-in').addEventListener('click',()=>applyZoom(zoom*1.6));
  $('zoom-out').addEventListener('click',()=>applyZoom(zoom/1.6));
  $('zoom-reset').addEventListener('click',resetZoom);
  document.querySelectorAll('[data-detail]').forEach(button=>button.addEventListener('click',()=>{
    const regions={chicago:[325,552],detroit:[580,510],niagara:[760,471]};applyZoom(6,regions[button.dataset.detail]);
  }));
  window.addEventListener('resize',()=>applyZoom(zoom));
  let drag=null,suppressClick=false;
  scroller.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button===0){drag={x:e.clientX,y:e.clientY,left:scroller.scrollLeft,top:scroller.scrollTop};suppressClick=false;}});
  window.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>4){suppressClick=true;scroller.classList.add('is-dragging');scroller.scrollLeft=drag.left-dx;scroller.scrollTop=drag.top-dy;}});
  window.addEventListener('pointerup',()=>{drag=null;scroller.classList.remove('is-dragging');});
  scroller.addEventListener('click',e=>{if(suppressClick){e.stopPropagation();e.preventDefault();suppressClick=false;}},true);
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
    $('study-index').hidden=mode!=='study';
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
  $('mobile-next').addEventListener('click',()=>{ if(finished){document.querySelector('.gl-panel').scrollIntoView({block:'start'});return;} $('next').click(); if(!finished) document.querySelector('.gl-mobile-status').scrollIntoView({block:'start'}); });
  $('retry').addEventListener('click',()=>{start([...missed],true); focusPrompt();});
  $('restart').addEventListener('click',()=>{start(); focusPrompt();});
  $('study-mode').addEventListener('click',()=>setMode('study'));
  $('play-mode').addEventListener('click',()=>setMode('play'));
  $('gl-app').hidden=false;
  $('map-number').max=items.length;
  start();
})();
