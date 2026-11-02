'use strict';
const words=JSON.parse(document.querySelector('#word-data').textContent);
const $=s=>document.querySelector(s);
const shuffle=a=>{a=[...a];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
let round=[],index=0,score=0,answered=false;
function node(tag,text){const n=document.createElement(tag);n.textContent=text;return n;}
function show(){
 answered=false;$('#next').hidden=true;$('#feedback').replaceChildren();$('#answers').replaceChildren();
 const w=round[index],o=w.occurrences[0];
 $('#quiz-status').textContent=`Word ${index+1} of ${round.length} · ${score} correct`;
 $('#question').replaceChildren(node('h3',`In Chapter ${o.chapter===5?'V':'VI'}, what does “${w.term}” mean?`),node('p',o.phrase));
 // Other categories avoid treating near-synonymous feelings as competing correct answers.
 const distractors=shuffle(words.filter(x=>x.category!==w.category&&x.term!==w.term));
 const used=new Set([w.category]),chosen=[];
 for(const x of distractors){if(!used.has(x.category)){chosen.push(x);used.add(x.category);}if(chosen.length===3)break;}
 for(const x of shuffle([w,...chosen])){const b=node('button',x.definition);b.type='button';b.addEventListener('click',()=>answer(x,w));$('#answers').append(b);}
 $('#question h3').tabIndex=-1;$('#question h3').focus();
}
function answer(selected,w){
 if(answered)return;answered=true;const correct=selected.id===w.id;if(correct)score++;
 for(const b of $('#answers').children)b.disabled=true;
 $('#feedback').append(node('p',`${correct?'Correct.':'Review this meaning.'} ${w.term}: ${w.definition}`));
 const o=w.occurrences[0],a=node('a',`Read Chapter ${o.chapter===5?'V':'VI'} · transcription p. ${o.original_page}`);a.href=o.url;$('#feedback').append(a);
 $('#quiz-status').textContent=`Word ${index+1} of ${round.length} · ${score} correct`;
 $('#next').hidden=false;$('#next').textContent=index===round.length-1?'See results':'Next word';
}
$('#start').addEventListener('click',()=>{const c=$('#quiz-category').value;round=shuffle(words.filter(x=>c==='all'||x.category===c)).slice(0,20);index=score=0;show();});
$('#next').addEventListener('click',()=>{if(!answered)return;if(++index<round.length)show();else{$('#question').replaceChildren(node('h3',`Round complete: ${score} of ${round.length} correct`));$('#answers').replaceChildren();$('#feedback').replaceChildren(node('p','Start another round or use the full vocabulary to review.'));$('#next').hidden=true;$('#quiz-status').textContent=`Completed · ${score} of ${round.length} correct`;}});
function filter(){const q=$('#search').value.toLowerCase().trim(),c=$('#category').value;let n=0;for(const w of document.querySelectorAll('.word')){w.hidden=!(w.dataset.search.includes(q)&&(c==='all'||w.dataset.category===c));if(!w.hidden)n++;}for(const g of document.querySelectorAll('.word-group'))g.hidden=![...g.querySelectorAll('.word')].some(x=>!x.hidden);$('#count').textContent=`${n} of ${words.length} entries`;}
$('#search').addEventListener('input',filter);$('#category').addEventListener('change',filter);$('#clear').addEventListener('click',()=>{$('#search').value='';$('#category').value='all';filter();});
