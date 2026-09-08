(() => {
  'use strict';
  const {items, lakes, channels} = window.pageConfig;
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
  for (const d of channels) svg('path',{d},$('channel-shapes'));
  const markers = new Map();
  for (const item of items) {
    const {id,kind,x,y,tx,ty} = item;
    if (x !== tx || y !== ty) {
      svg('line',{x1:x,y1:y,x2:tx,y2:ty},$('marker-stems'));
      svg('circle',{cx:x,cy:y,r:2.5},$('marker-stems'));
    }
    const marker = svg('g', {class:`gl-marker ${kind}`,transform:`translate(${tx} ${ty})`,role:'button',tabindex:0,'aria-label':`Location ${id}`,'data-id':id},$('map-markers'));
    svg('circle',{r:27,class:'gl-hit'},marker);
    if (kind === 'water') svg('path',{d:'M0 -21 L21 0 L0 21 L-21 0 Z',class:'gl-token'},marker);
    else if (kind === 'cut') svg('rect',{x:-17,y:-17,width:34,height:34,rx:1,class:'gl-token'},marker);
    else svg('circle',{r:17,class:'gl-token'},marker);
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
      button.addEventListener('click',()=>{ studySelect(item.id); panTo(item.id); });
      group.appendChild(button);
    }
    $('study-list').appendChild(group);
  }
  function shuffled(ids) {
    const result=[...ids];
    for (let i=result.length-1;i>0;i--) { const j=Math.floor(Math.random()*(i+1)); [result[i],result[j]]=[result[j],result[i]]; }
    return result;
  }
  let mode='play', queue=[], index=0, firstTry=0, missed=new Set(), attempted=false, resolved=false, finished=false, round=0;
  let savedFeedback=null;
  const current=()=>items.find(item=>item.id===queue[index]);
  function clearMap() { for (const marker of markers.values()) marker.classList.remove('is-correct','is-wrong','is-selected'); }
  function say(message,tone='neutral') { $('feedback').textContent=message; $('feedback').dataset.tone=tone; syncMobile(); }
  function syncMobile() {
    $('mobile-prompt').textContent=(mode==='study'?'Study: ':'')+$('place-name').textContent;
    $('mobile-feedback').textContent=$('feedback').textContent;
    $('mobile-next').hidden=mode!=='play'||!resolved||finished;
    $('mobile-next').textContent=index===queue.length-1?'Results →':'Next →';
  }
  function panTo(id) {
    const marker=markers.get(id), scroller=document.querySelector('.gl-map-scroll');
    const rect=marker.getBoundingClientRect(), frame=scroller.getBoundingClientRect();
    scroller.scrollLeft+=rect.left+rect.width/2-frame.left-frame.width/2;
  }
  function focusPrompt() { $('place-name').focus({preventScroll:true}); }
  function updateScore() { $('score').textContent=`${firstTry} of ${index+(resolved?1:0)} found on the first try`; }
  function renderQuestion() {
    clearMap();
    $('round-label').textContent=round===1?'Full map round':`Practice round ${round}`;
    $('progress-text').textContent=`${index+1} / ${queue.length}`;
    $('round-progress').max=queue.length; $('round-progress').value=index;
    $('place-name').textContent=`Find ${current().name}`; $('place-category').textContent=names[current().kind];
    $('number-form').hidden=false; $('reveal').hidden=false; $('next').hidden=true;
    $('retry').hidden=true; $('restart').hidden=true;
    $('map-number').value='';
    say('Choose the number that marks this place.'); updateScore();
  }
  function start(ids=items.map(i=>i.id),practice=false) {
    round=practice?round+1:1;
    queue=shuffled(ids); index=0; firstTry=0; missed=new Set(); attempted=false; resolved=false; finished=false;
    renderQuestion();
  }
  function finish() {
    finished=true; clearMap();
    $('round-label').textContent=round===1?'Full map round':`Practice round ${round}`;
    $('round-progress').value=queue.length;
    $('progress-text').textContent=`${queue.length} / ${queue.length}`;
    $('place-name').textContent=missed.size?'You’re finding your way.':'You know this map.';
    $('place-category').textContent=`${firstTry} of ${queue.length} on the first try`;
    say(missed.size?`${missed.size} ${missed.size===1?'place is':'places are'} ready for another look. Practice just those, or try the full map again.`:'Every place found on the first try. Try another shuffled round whenever you’re ready.');
    $('number-form').hidden=true; $('reveal').hidden=true; $('next').hidden=true;
    $('retry').hidden=missed.size===0; $('restart').hidden=false; $('score').textContent='';
  }
  function complete(revealed=false) {
    resolved=true;
    markers.get(current().id).classList.add('is-correct');
    $('number-form').hidden=true; $('reveal').hidden=true; $('next').hidden=false;
    $('next').innerHTML=index===queue.length-1?'See results <span aria-hidden="true">→</span>':'Next place <span aria-hidden="true">→</span>';
    $('round-progress').value=index+1;
    say(`${revealed?'Here it is':'Correct'} — ${current().name} is number ${current().id}.${revealed?' You’ll get another chance to practice it.':''}`,revealed?'neutral':'correct');
    updateScore();
  }
  function choose(id) {
    if (mode==='study') { studySelect(id); return; }
    if (resolved||finished) return;
    const item=items.find(i=>i.id===id);
    if (!item) { say('Enter a map number from 1 to 21.','wrong'); return; }
    clearMap();
    if (id===current().id) {
      if (!attempted) firstTry++;
      complete();
      (matchMedia('(max-width:760px)').matches ? $('mobile-next') : $('next')).focus({preventScroll:true});
    } else {
      attempted=true; missed.add(current().id);
      markers.get(id).classList.add('is-wrong');
      say(`That’s number ${id}, ${item.name}. Keep looking for ${current().name}.`,'wrong');
    }
  }
  function studySelect(id) {
    const item=items.find(i=>i.id===id); clearMap();
    markers.get(id).classList.add('is-selected');
    $('place-name').textContent=item.name; $('place-category').textContent=`Number ${id} · ${names[item.kind]}`;
    say(`Number ${id}: ${item.name}. Follow its line to the location if the marker is offset.`);
  }
  function setMode(nextMode) {
    if (mode===nextMode) return;
    mode=nextMode;
    $('play-mode').setAttribute('aria-pressed',mode==='play');
    $('study-mode').setAttribute('aria-pressed',mode==='study');
    $('play-mode').textContent=mode==='study'?'Resume play':'Play';
    $('study-index').hidden=mode!=='study';
    for (const item of items) markers.get(item.id).setAttribute('aria-label',mode==='study'?`Location ${item.id}: ${item.name}`:`Location ${item.id}`);
    if (mode==='study') {
      savedFeedback={text:$('feedback').textContent,tone:$('feedback').dataset.tone};
      clearMap(); $('round-label').textContent='Study the map'; $('progress-text').textContent='21 places';
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
  $('number-form').addEventListener('submit',event=>{ event.preventDefault(); choose(Number($('map-number').value)); if(resolved) $('next').focus(); });
  $('next').addEventListener('click',()=>{
    index++; attempted=false; resolved=false;
    if(index===queue.length) finish(); else renderQuestion();
    focusPrompt();
  });
  $('reveal').addEventListener('click',()=>{
    if(mode!=='play'||resolved||finished) return;
    attempted=true; missed.add(current().id); clearMap(); complete(true); panTo(current().id); $('next').focus({preventScroll:true});
  });
  $('mobile-next').addEventListener('click',()=>{ $('next').click(); if(!finished) document.querySelector('.gl-mobile-status').scrollIntoView({block:'start'}); });
  $('retry').addEventListener('click',()=>{start([...missed],true); focusPrompt();});
  $('restart').addEventListener('click',()=>{start(); focusPrompt();});
  $('study-mode').addEventListener('click',()=>setMode('study'));
  $('play-mode').addEventListener('click',()=>setMode('play'));
  $('gl-app').hidden=false;
  start();
})();
