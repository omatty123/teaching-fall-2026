(() => {
 'use strict';
 const {data,stateAt}=window.SmithTiming;
 const grid=document.getElementById('grid'),cells=[],lines=[],verseButtons=[];
 const status=document.getElementById('status');
 let player,ready=false,lastView='';
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
  if(!ready)return;
  player.seekTo(data.verses[index].start,true);player.playVideo();render(data.verses[index].start);
 }
 function render(time){
  const s=stateAt(time),v=data.verses[s.verse];
  // Word timing is independent of the bar clock: Smith anticipates the next group.
  const singing=v.l.findIndex(([start,end])=>time>=start && time<=end);
  const key=[s.verse,s.bar,s.beat,s.phase,singing].join('|');
  if(key===lastView)return;lastView=key;
  lines.forEach((line,i)=>{line.textContent=v.t[i];line.classList.toggle('sing',i===singing);});
  cells.forEach((cell,i)=>{
   cell.classList.toggle('now',i===s.bar);
   cell.setAttribute('aria-label',`Bar ${i+1}${i===s.bar?`, beat ${s.beat+1}`:''}`);
   cell.querySelectorAll('i').forEach((dot,d)=>dot.classList.toggle('on',i===s.bar && d<=s.beat));
  });
  verseButtons.forEach((b,i)=>{b.parentElement.classList.toggle('live',i===s.verse);b.setAttribute('aria-pressed',String(i===s.verse));});
  if(s.phase==='intro')status.textContent='Piano introduction';
  else if(s.phase==='ending')status.textContent='Ending';
  else status.textContent=`Verse ${s.verse+1} of 7 · bar ${s.bar+1} of 12`;

 }
 function tick(){
  if(ready){
   // Read the media clock directly: pause, buffering, seeking and playback rate
   // must never let a separate animation clock advance ahead of the recording.
   render(player.getCurrentTime());
  }
  requestAnimationFrame(tick);
 }
 window.onYouTubeIframeAPIReady=()=>{
  player=new YT.Player('player',{videoId:data.videoId,playerVars:{rel:0,playsinline:1},events:{
   onReady:()=>{
    ready=true;verseButtons.forEach(b=>b.disabled=false);
   },
   onError:()=>{status.textContent='The recording could not load. Reload this page to retry.';}
  }});
 };
 render(0);requestAnimationFrame(tick);
 const script=document.createElement('script');script.src='https://www.youtube.com/iframe_api';document.head.append(script);
})();
