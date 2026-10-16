(() => {
 'use strict';
 const {data,stateAt}=window.SmithTiming;
 const grid=document.getElementById('grid'),cells=[],lines=[],verseButtons=[];
 const status=document.getElementById('status'),note=document.getElementById('pickup-note');
 const replay=document.getElementById('replay-verse'),repeat=document.getElementById('loop-verse'),speed=document.getElementById('smith-speed');
 let player,ready=false,selected=0,loopSeeking=false,lastView='';
 ['A','A','B'].forEach((row,r)=>{
  const label=document.createElement('div');label.className='lab '+row;label.textContent=row;grid.append(label);
  for(let b=0;b<4;b++){
   const cell=document.createElement('div');cell.className='watch-bar row'+row;
   cell.innerHTML=`<span>Bar ${r*4+b+1}</span><span class="watch-dots" aria-hidden="true"><i></i><i></i><i></i><i></i></span>`;
   grid.append(cell);cells.push(cell);
  }
  const line=document.createElement('div');line.className='line row'+row;grid.append(line);lines.push(line);
 });
 const list=document.getElementById('verses');
 data.verses.forEach((v,i)=>{
  const li=document.createElement('li'),button=document.createElement('button');button.type='button';button.disabled=true;
  const title=document.createElement('span');title.className='v';title.textContent=`Verse ${i+1}`;button.append(title);
  v.t.forEach((text,n)=>{const span=document.createElement('span');span.textContent=text;if(n)span.className='rep';button.append(span);if(n<2)button.append(document.createElement('br'));});
  button.addEventListener('click',()=>playVerse(i));li.append(button);list.append(li);verseButtons.push(button);
 });
 function playVerse(index){
  if(!ready)return;selected=index;loopSeeking=true;
  replay.textContent=`Replay verse ${index+1}`;
  player.seekTo(data.verses[index].start,true);player.playVideo();render(data.verses[index].start);
 }
 replay.addEventListener('click',()=>playVerse(selected));
 repeat.addEventListener('change',()=>{
  if(repeat.checked && ready){selected=stateAt(player.getCurrentTime()).verse;replay.textContent=`Replay verse ${selected+1}`;}
 });
 speed.addEventListener('change',()=>{if(ready)player.setPlaybackRate(Number(speed.value));});
 function render(time){
  const s=stateAt(time),v=data.verses[s.verse];
  // Word timing is independent of the bar clock: Smith anticipates the next group.
  const singing=v.l.findIndex(([start,end])=>time>=start && time<=end);
  const future=data.verses[s.verse+1];
  const pickup=future && time>=future.l[0][0] && time<future.start;
  const key=[s.verse,s.bar,s.beat,s.phase,singing,pickup].join('|');
  if(key===lastView)return;lastView=key;
  lines.forEach((line,i)=>{line.textContent=v.t[i];line.classList.toggle('sing',i===singing);});
  cells.forEach((cell,i)=>{
   cell.classList.toggle('now',i===s.bar);
   cell.setAttribute('aria-label',`Bar ${i+1}${i===s.bar?`, beat ${s.beat+1}`:''}`);
   cell.querySelectorAll('i').forEach((dot,d)=>dot.classList.toggle('on',i===s.bar && d<=s.beat));
  });
  verseButtons.forEach((b,i)=>{b.parentElement.classList.toggle('live',i===s.verse);b.setAttribute('aria-pressed',String(i===s.verse));});
  if(s.phase==='intro')status.textContent='Piano introduction · twelve-bar verse begins at 0:05';
  else if(s.phase==='ending')status.textContent='Ending · seven twelve-bar verses complete';
  else status.textContent=`Verse ${s.verse+1} of 7 · bar ${s.bar+1} of 12 · beat ${s.beat+1} of 4`;
  if(pickup)note.textContent=`Smith begins verse ${s.verse+2} before its first bar: “${future.t[0]}”`;
  else if(singing>=0){
   const anticipated=s.phase==='intro' || s.bar<singing*4;
   note.textContent=`Smith sings line ${['A','A (repeat)','B'][singing]}${anticipated?' before its four-bar group begins.':'.'}`;
  } else note.textContent=s.phase==='ending'?'Piano ending.':'Piano between vocal phrases.';
  if(!repeat.checked){selected=s.verse;replay.textContent=`Replay verse ${selected+1}`;}
 }
 function tick(){
  if(ready){
   // Read the media clock directly: pause, buffering, seeking and playback rate
   // must never let a separate animation clock advance ahead of the recording.
   const time=player.getCurrentTime(),v=data.verses[selected];
   if(loopSeeking && Math.abs(time-v.start)<.35)loopSeeking=false;
   if(repeat.checked && player.getPlayerState()===1 && !loopSeeking && time>=v.end){
    loopSeeking=true;player.seekTo(v.start,true);
   } else render(time);
  }
  requestAnimationFrame(tick);
 }
 window.onYouTubeIframeAPIReady=()=>{
  player=new YT.Player('player',{videoId:data.videoId,playerVars:{rel:0,playsinline:1},events:{
   onReady:()=>{
    ready=true;replay.disabled=false;verseButtons.forEach(b=>b.disabled=false);
    const rates=player.getAvailablePlaybackRates();speed.replaceChildren();
    rates.filter(rate=>rate>=.5 && rate<=1).forEach(rate=>{const option=document.createElement('option');option.value=rate;option.textContent=rate===1?'Normal':`${rate}×`;speed.append(option);});
    speed.value='1';speed.disabled=false;
   },
   onStateChange:event=>{if(event.data===YT.PlayerState.PLAYING || event.data===YT.PlayerState.PAUSED)loopSeeking=false;},
   onPlaybackRateChange:event=>{speed.value=String(event.data);},
   onError:()=>{status.textContent='The recording could not load. Reload this page to retry.';}
  }});
 };
 render(0);replay.textContent='Play verse 1';requestAnimationFrame(tick);
 const script=document.createElement('script');script.src='https://www.youtube.com/iframe_api';document.head.append(script);
})();
