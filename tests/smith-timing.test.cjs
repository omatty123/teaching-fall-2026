const {test}=require('node:test'),assert=require('node:assert/strict');
const {data,stateAt}=require('../frst-110-resources/smith-timing.js');
test('seven complete 48-beat verses have contiguous boundaries',()=>{
 assert.equal(data.verses.length,7);
 data.verses.forEach((v,i)=>{
  assert.equal(v.beats.length,48);assert.equal(v.start,v.beats[0]);
  v.beats.forEach((t,k)=>{if(k)assert(t>v.beats[k-1]);assert(t<v.end)});
  if(i<6)assert.equal(v.end,data.verses[i+1].start);
 });
});
test('every beat maps to the right verse, bar and beat, including backward seeks',()=>{
 for(let v=6;v>=0;v--)for(let b=47;b>=0;b--){
  assert.deepEqual(stateAt(data.verses[v].beats[b]+.001),{verse:v,bar:Math.floor(b/4),beat:b%4,phase:'verse'});
 }
});
test('vocal pickups do not advance the musical bar counter',()=>{
 assert.equal(stateAt(2.94).phase,'intro');
 assert.equal(stateAt(12.58).bar,3); // second A enters before bar five
 assert.equal(stateAt(31.9).verse,0); // next verse lyric during prior verse
 assert.equal(stateAt(33.384).verse,1);
});
test('intro, last beat, ending and replay boundaries are distinct',()=>{
 assert.equal(stateAt(0).bar,-1);assert.equal(stateAt(5.044).bar,0);
 assert.equal(stateAt(196.233).bar,11);assert.equal(stateAt(196.234).phase,'ending');
 assert.equal(stateAt(197.6).phase,'ending');
});
