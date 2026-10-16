const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm'),fs=require('node:fs');
function setup(){
  let clock=0,id=0;const jobs=new Map(),nodes=[];
  function el(dataset={}){const classes=new Set();return {dataset,value:100,checked:false,textContent:'',children:[],events:{},classList:{add:x=>classes.add(x),remove:x=>classes.delete(x),toggle:(x,on)=>on?classes.add(x):classes.delete(x)},append(x){this.children.push(x)},addEventListener(n,fn){this.events[n]=fn}};}
  const ids=Object.fromEntries(['playchords','blues-tempo','blues-loop','audio-status','chordgrid','scale','tempo-value'].map(k=>[k,el()]));
  const buttons=['I','IV','V'].map(ch=>el({ch}));buttons.push(el({seq:'1'}));
  const param=()=>({value:0,setValueAtTime(){},linearRampToValueAtTime(){},exponentialRampToValueAtTime(){},cancelScheduledValues(){},setTargetAtTime(){}});
  function node(){return {gain:param(),frequency:param(),Q:param(),threshold:param(),knee:param(),ratio:param(),playbackRate:param(),connect(){return this},disconnect(){}};}
  class AudioContext{
    constructor(){this.sampleRate=8000;this.destination=node();}
    get currentTime(){return clock;} async resume(){}
    createGain(){return node()} createDynamicsCompressor(){return node()} createBiquadFilter(){return node()}
    createBuffer(_,len){const data=new Float32Array(len);return {getChannelData:()=>data}}
    async decodeAudioData(){return {decoded:true}}
    createBufferSource(){const n=node();n.start=t=>n.startAt=t;n.stop=t=>n.stopAt=t;nodes.push(n);return n;}
  }
  const document={hidden:false,getElementById:id=>ids[id],createElement:()=>el(),querySelectorAll:()=>buttons,querySelector:s=>buttons.find(b=>s.includes(`"${b.dataset.ch}"`)),addEventListener(){}};
  const context={document,window:{AudioContext,addEventListener(){}},fetch:async()=>({ok:true,arrayBuffer:async()=>new ArrayBuffer(8)}),setTimeout:(fn,ms)=>{jobs.set(++id,{fn,at:clock+ms/1000});return id},setInterval:(fn,ms)=>{jobs.set(++id,{fn,at:clock+ms/1000,repeat:ms/1000});return id},clearInterval:i=>jobs.delete(i)};
  vm.runInNewContext(fs.readFileSync('frst-110-resources/blues-audio.js','utf8'),context);
  function advance(seconds){const end=clock+seconds;while(true){const entry=[...jobs].filter(([,v])=>v.at<=end).sort((a,b)=>a[1].at-b[1].at)[0];if(!entry)break;const [k,j]=entry;clock=j.at;if(j.repeat)j.at+=j.repeat;else jobs.delete(k);j.fn();}clock=end;}
  return {ids,buttons,nodes,advance,now:()=>clock,click:async e=>{await e.events.click();}};
}
test('one verse finishes, and Stop cancels scheduled guitar sources',async()=>{
 const h=setup();await h.click(h.ids.playchords);h.advance(29.2);assert.equal(h.ids['audio-status'].textContent,'Finished.');
 await h.click(h.ids.playchords);h.advance(.5);await h.click(h.ids.playchords);assert.equal(h.ids.playchords.textContent,'Hear the pattern');assert(h.nodes.every(n=>n.stopAt<=h.now()+.041));
});
test('loop crosses verse boundary; disabling loop ends at next boundary',async()=>{
 const h=setup();h.ids['blues-loop'].checked=true;await h.click(h.ids.playchords);h.advance(29);assert.match(h.ids['audio-status'].textContent,/verse 2/);
 h.ids['blues-loop'].checked=false;h.advance(29);assert.equal(h.ids['audio-status'].textContent,'Finished.');
});
test('tempo updates the ongoing pattern without restarting it',async()=>{
 const h=setup();await h.click(h.ids.playchords);h.advance(5);h.ids['blues-tempo'].value=140;h.ids['blues-tempo'].events.input();assert.equal(h.ids['tempo-value'].textContent,140);h.advance(20);assert.equal(h.ids['audio-status'].textContent,'Finished.');
});
test('piano replaces guitar and rapid chord clicks cancel previous piano',async()=>{
 const h=setup();await h.click(h.ids.playchords);h.advance(1);const old=h.nodes.slice();await h.click(h.buttons[0]);assert(old.every(n=>n.stopAt<=h.now()+.041));
 h.advance(.1);assert.equal(h.ids['audio-status'].textContent,'Piano · I');const first=h.nodes.slice();await h.click(h.buttons[2]);assert(first.every(n=>n.stopAt<=h.now()+.041));h.advance(.1);assert.equal(h.ids['audio-status'].textContent,'Piano · V');h.advance(2);assert.equal(h.ids['audio-status'].textContent,'Finished.');
});
