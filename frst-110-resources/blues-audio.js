/* Self-hosted piano and acoustic-guitar samples. */
(() => {
  'use strict';
  const PLAN = ['I','I','I','I','IV','IV','I','I','V','IV','I','I'];
  const LABEL = {I:'HOME', IV:'AWAY', V:'TENSION'};
  const GUITAR_NOTES = [40,45,47,49,52,54,56,57,59,61,62,63,64,66,67,69];
  const ROOT = {I:0, IV:5, V:7};
  const NOTES = [[39,'Ds2'],[42,'Fs2'],[45,'A2'],[48,'C3'],[51,'Ds3'],[54,'Fs3'],[57,'A3'],[60,'C4'],[63,'Ds4'],[66,'Fs4'],[69,'A4']];
  const btn = document.getElementById('playchords');
  const sound = document.getElementById('pattern-sound');
  let patternSound='piano';
  const tempo = document.getElementById('blues-tempo');
  const loop = document.getElementById('blues-loop');
  const status = document.getElementById('audio-status');
  const cells = [], scaleCells = [];
  const grid = document.getElementById('chordgrid');
  ['A','A','B'].forEach((row,ri) => {
    const label = document.createElement('span'); label.className='lab'; label.textContent=row; grid.append(label);
    for(let i=0;i<4;i++) {
      const cell=document.createElement('span'); const ch=PLAN[ri*4+i];
      cell.className=ch; cell.innerHTML=`${ch}<small>${LABEL[ch]}</small>`; grid.append(cell); cells.push(cell);
    }
  });
  const scale=document.getElementById('scale');
  [['E',1],['F♯',2],['G♯',3],['A',4],['B',5],['C♯',6],['D♯',7],['E',1]].forEach(([note,degree]) => {
    const el=document.createElement('span'), chord={1:'I',4:'IV',5:'V'}[degree];
    if(chord)el.className=chord;
    el.innerHTML=`<b>${degree}</b>${note}${chord?`<em>${chord}</em><small class="home-label">${LABEL[chord]}</small>`:''}`;
    scale.append(el); scaleCells.push(el);
  });
  let ac, master, guitarBus, outputLimiter, pianoPromise, guitarPromise, mode=null, generation=0, interval=null;
  let nextBeat=0, beatIndex=0, cycle=1, finishAt=null;
  let visual=[], sources=new Set();
  const samples=new Map(), guitarSamples=new Map();
  function mark(ch) {
    scaleCells.forEach(el=>el.classList.remove('now'));
    document.querySelectorAll('.hear button').forEach(el=>el.classList.remove('now'));
    if(!ch)return;
    scaleCells[{I:0,IV:3,V:4}[ch]].classList.add('now');
    if(ch==='I')scaleCells[7].classList.add('now');
    document.querySelector(`[data-ch="${ch}"]`).classList.add('now');
  }
  function stop(message='Stopped.') {
    generation++; clearInterval(interval); interval=null;
    mode=null; visual=[]; finishAt=null;
    if(ac && master) {
      const old=master,oldGuitar=guitarBus,oldLimiter=outputLimiter; old.gain.cancelScheduledValues(ac.currentTime);
      old.gain.setTargetAtTime(0,ac.currentTime,0.008);
      sources.forEach(s=>{try{s.stop(ac.currentTime+0.04);}catch(_) {}});
      setTimeout(()=>{old.disconnect();oldGuitar.disconnect();oldLimiter.disconnect();},80);
    }
    sources.clear(); cells.forEach(el=>el.classList.remove('now')); mark(null);
    btn.textContent='Hear the pattern'; status.textContent=message;
  }
  async function start(kind) {
    stop(''); const token=generation;
    mode=kind; btn.textContent='Stop';
    ac=ac||new (window.AudioContext||window.webkitAudioContext)();
    await ac.resume();
    if(token!==generation)return null;
    master=ac.createGain();master.gain.value=0.65;
    const limiter=outputLimiter=ac.createDynamicsCompressor();limiter.threshold.value=-12;limiter.knee.value=12;limiter.ratio.value=4;
    master.connect(limiter).connect(ac.destination);
    guitarBus=ac.createBiquadFilter();guitarBus.type='lowpass';guitarBus.frequency.value=4800;guitarBus.Q.value=0.5;
    guitarBus.connect(master);
    return token;
  }
  function track(source,gain,out,at,end,offset=0) {
    source.connect(gain).connect(out); sources.add(source);
    source.onended=()=>{sources.delete(source);source.disconnect();gain.disconnect();};
    source.start(at,offset);source.stop(end);
  }
  function loadPiano() {
    if(!pianoPromise) pianoPromise=Promise.all(NOTES.map(async ([midi,name])=>{
      const response=await fetch(`../audio/blues-piano/${name}.mp3`);
      if(!response.ok)throw new Error('Piano sample unavailable');
      const buffer=await ac.decodeAudioData(await response.arrayBuffer());samples.set(midi,buffer);
    })).catch(error=>{pianoPromise=null;throw error;});
    return pianoPromise;
  }
  function piano(ch,at) {
    [0,4,7,12].forEach((offset,i)=>{
      const midi=52+ROOT[ch]+offset;
      const nearest=NOTES.reduce((best,n)=>Math.abs(n[0]-midi)<Math.abs(best[0]-midi)?n:best)[0];
      const source=ac.createBufferSource(),gain=ac.createGain();source.buffer=samples.get(nearest);
      source.playbackRate.value=2**((midi-nearest)/12);
      const begin=at+i*0.006,release=begin+1.05;
      gain.gain.setValueAtTime(0,begin);gain.gain.linearRampToValueAtTime(0.48,begin+0.005);
      gain.gain.setValueAtTime(0.48,release);gain.gain.exponentialRampToValueAtTime(0.0001,release+0.42);
      track(source,gain,master,begin,release+0.44);
    });
  }
  function loadGuitar() {
    if(!guitarPromise) guitarPromise=Promise.all(GUITAR_NOTES.map(async midi=>{
      const names=['C','Cs','D','Ds','E','F','Fs','G','Gs','A','As','B'];
      const name=names[midi%12]+(Math.floor(midi/12)-1);
      const response=await fetch(`../audio/blues-guitar/${name}.mp3`);
      if(!response.ok)throw new Error('Guitar sample unavailable');
      guitarSamples.set(midi,await ac.decodeAudioData(await response.arrayBuffer()));
    })).catch(error=>{guitarPromise=null;throw error;});
    return guitarPromise;
  }
  function guitar(midi,at,duration,velocity) {
    const source=ac.createBufferSource(),gain=ac.createGain();
    if(patternSound==='piano') {
      const nearest=NOTES.reduce((best,n)=>Math.abs(n[0]-midi)<Math.abs(best[0]-midi)?n:best)[0];
      source.buffer=samples.get(nearest);source.playbackRate.value=2**((midi-nearest)/12);
      velocity*=0.70;
    } else source.buffer=guitarSamples.get(midi);
    gain.gain.setValueAtTime(0,at);gain.gain.linearRampToValueAtTime(velocity,at+0.003);
    gain.gain.setValueAtTime(velocity,at+duration*0.72);
    gain.gain.exponentialRampToValueAtTime(0.0001,at+duration);
    track(source,gain,patternSound==='piano'?master:guitarBus,at,at+duration+0.02,patternSound==='piano'?0:0.04);
  }
  function scheduleBeat(index,at,beat) {
    const bar=Math.floor(index/4),b=index%4,ch=PLAN[bar],root=40+ROOT[ch];
    // Alternating bass and lightly rolled shuffle chords; keep bar starts exact.
    guitar(root+(b%2?7:0),at,beat*0.94,0.78);
    // Use the sampled fifth/sixth dyad for the short swung reply.
    guitar(root+12,at+beat*2/3,beat*0.30,0.30);
    guitar(root+(b%2?9:7),at+beat*2/3+0.012,beat*0.29,0.38);
    if(b===0 || b===2) {
      [12,16,19,22].forEach((n,i)=>guitar(root+n,at+0.018+i*0.014,beat*0.90,0.23-i*0.025));
    }
    if(b===0)visual.push({at,bar,ch,cycle});
  }

  function pump() {
    if(!mode)return;
    const now=ac.currentTime;
    if(mode==='pattern') {
      while(nextBeat<now+0.12 && finishAt===null) {
        if(beatIndex===48) {
          if(!loop.checked){finishAt=nextBeat+0.1;break;}
          beatIndex=0;cycle++;
        }
        const beat=60/Number(tempo.value);
        scheduleBeat(beatIndex,nextBeat,beat);nextBeat+=beat;beatIndex++;
      }
    }
    while(visual.length && visual[0].at<=now) {
      const item=visual.shift();mark(item.ch);
      if(item.bar!==undefined) {
        cells.forEach((el,i)=>el.classList.toggle('now',i===item.bar));
        status.textContent=`${patternSound==='piano'?'Piano':'Guitar'} · verse ${item.cycle} · bar ${item.bar+1} of 12 · ${item.ch} · ${LABEL[item.ch]}`;
      } else status.textContent=`Piano · ${item.ch} · ${LABEL[item.ch]}`;
    }
    if(finishAt!==null && now>=finishAt)stop('Finished.');
  }
  btn.addEventListener('click',async()=>{
    if(mode){stop();return;}
    let token;
    try {
      token=await start('pattern');if(token===null)return;
      patternSound=sound.value;
      status.textContent=patternSound==='piano'?'Loading piano…':'Loading acoustic guitar…';
      await (patternSound==='piano'?loadPiano():loadGuitar());if(token!==generation)return;
      beatIndex=0;cycle=1;
      nextBeat=ac.currentTime+0.08;pump();interval=setInterval(pump,25);
    }catch(_){if(token===undefined || token===generation)stop('Instrument could not load. Press Hear the pattern to retry.');}
  });
  document.querySelectorAll('.hear button').forEach(button=>button.addEventListener('click',async()=>{
    let token;
    try {
      token=await start('piano');if(token===null)return;
      status.textContent='Loading piano…';await loadPiano();if(token!==generation)return;
      const seq=button.dataset.seq?['I','IV','V','I']:[button.dataset.ch],at=ac.currentTime+0.06;
      seq.forEach((ch,i)=>{piano(ch,at+i*1.6);visual.push({at:at+i*1.6,ch});});
      finishAt=at+seq.length*1.6;pump();interval=setInterval(pump,25);
    }catch(_){if(token===undefined || token===generation)stop('Piano could not load. Press a chord button to retry.');}
  }));
  sound.addEventListener('change',()=>{if(mode==='pattern')stop('Sound changed. Press Hear the pattern.');});
  tempo.addEventListener('input',()=>{document.getElementById('tempo-value').textContent=tempo.value;});
  document.addEventListener('visibilitychange',()=>{if(document.hidden && mode)stop('Stopped while the page was hidden.');});
  window.addEventListener('pagehide',()=>stop());
})();
