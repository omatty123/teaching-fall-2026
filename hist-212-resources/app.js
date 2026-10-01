'use strict';
// Practice quiz trimmed from 40 to 24 (2026-09-29). The chart still uses all 40 entries in data.js.
const LEFT_OUT=new Set(['books-2','books-4','books-6','books-8','thinkers-3','thinkers-5','thinkers-7','thinkers-8','dynasties-2','dynasties-3','dynasties-4','dynasties-7','dynasties-8','cities-1','cities-3','cities-6']);
const {sources}=window.QUIZ_DATA;
const sections=window.QUIZ_DATA.sections.map(s=>({...s,items:s.items.filter(q=>!LEFT_OUT.has(q.id))}));
const allItems=sections.flatMap(s=>s.items.map(q=>({...q,section:s.id})));
const $=id=>document.getElementById(id);
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function shuffled(items){const a=[...items];for(let i=a.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
let selected=sections.some(s=>s.id===location.hash.slice(1))?location.hash.slice(1):'all';
let mode='practice',round=[],index=0,answers=[],finished=false,retry=false,timer=null;
const sessions=new Map();
function pool(){return selected==='all'?allItems:allItems.filter(q=>q.section===selected);}
function cancelAdvance(){clearTimeout(timer);timer=null;const hint=$('advance-hint');if(hint)hint.textContent='';}
function begin(items=pool(),isRetry=false){cancelAdvance();round=shuffled(items).map(q=>({...q,choices:shuffled([q.answer,...q.distractors])}));index=0;answers=[];finished=false;retry=isRetry;}
function saveSession(){sessions.set(selected,{round,index,answers,finished,retry});}
function chooseSection(id){cancelAdvance();saveSession();selected=id;const prior=sessions.get(id);if(prior)({round,index,answers,finished,retry}=prior);else begin();render();}
function refs(q){return `<div class="references">${q.sources.map(k=>`<a href="${escapeHTML(sources[k][1])}" target="_blank" rel="noopener">${escapeHTML(sources[k][0])} ↗</a>`).join('')}</div>`;}
function explanation(q){return `<p>${escapeHTML(q.detail)}</p>${refs(q)}`;}
function focusHeading(){document.querySelector('#activity h2').focus({preventScroll:true});}
function render(){
 cancelAdvance();$('sections').value=selected;
 $('study').textContent=mode==='study'?'Back to quiz':'Study';
 $('study').setAttribute('aria-pressed',String(mode==='study'));
 if(mode==='study')renderStudy();else if(finished)renderResults();else renderQuestion();
}
function renderStudy(){
 const s=sections.find(s=>s.id===selected);
 $('activity').innerHTML=`<section><h2 tabindex="-1">${s?escapeHTML(s.title):'All topics'}</h2><p class="study-intro">${s?escapeHTML(s.subtitle):'Books, thinkers, rulers, dynasties, dates, and cities'}. Your quiz progress is saved while you study.</p><dl class="study-list">${pool().map(q=>`<div class="study-entry"><dt>${escapeHTML(q.label)}</dt><dd>${explanation(q)}</dd></div>`).join('')}</dl></section>`;
}
function renderQuestion(){
 const q=round[index],response=answers[index],previous=index>0?round[index-1]:null;
 $('activity').innerHTML=`<section class="quiz-box" aria-label="Practice question">
 <div class="quiz-top"><span>${retry?'Retry · ':''}${index+1} / ${round.length}</span><span>${escapeHTML(sections.find(s=>s.id===q.section).title)}</span></div>
 <h2 class="question" tabindex="-1">${escapeHTML(q.question)}</h2>
 <div class="answers">${q.choices.map((option,i)=>{const cls=response?(option===q.answer?'correct':option===response.choice?'incorrect':'muted'):'';return `<button class="answer ${cls}" data-option="${i}" ${response?'disabled':''}><span class="letter" aria-hidden="true">${String.fromCharCode(65+i)}</span><span>${escapeHTML(option)}${response&&option===q.answer?' · Correct answer':''}${response&&option===response.choice&&!response.correct?' · Your answer':''}</span></button>`;}).join('')}</div>
 <div id="feedback" aria-live="polite"></div>
 ${!response&&previous?`<details class="previous"><summary>Previous answer</summary><p><strong>${escapeHTML(previous.question)}</strong></p><p>${escapeHTML(previous.answer)}</p>${explanation(previous)}</details>`:''}
 </section>`;
 document.querySelectorAll('[data-option]').forEach(b=>b.addEventListener('click',()=>answer(Number(b.dataset.option))));
 if(response)renderFeedback();
}
function renderFeedback(){
 const q=round[index],response=answers[index];
 $('feedback').innerHTML=`<div class="feedback"><div class="feedback-top"><strong>${response.correct?'Correct.':'Not quite.'}</strong><span id="advance-hint"></span></div>
 ${response.correct?`<details id="explanation"><summary>Read explanation</summary>${explanation(q)}</details>`:explanation(q)}
 <button class="primary" id="next">${index===round.length-1?'See results':'Continue'}</button></div>`;
 $('next').addEventListener('click',next);
 if($('explanation'))$('explanation').addEventListener('toggle',()=>{if($('explanation').open)cancelAdvance();});
 // Reading, changing options, or moving away must never race an auto-advance.
 $('feedback').addEventListener('focusin',cancelAdvance);
}
function answer(option){
 if(answers[index]||finished||mode!=='practice')return;
 const q=round[index],choice=q.choices[option];answers.push({id:q.id,choice,correct:choice===q.answer});renderQuestion();
 if(choice===q.answer&&$('auto').checked&&!$('options').open&&!document.hidden){
  $('advance-hint').textContent='Next question automatically…';
  timer=setTimeout(next,1500);
 }else $('next').focus({preventScroll:true});
}
function next(){
 cancelAdvance();if(!answers[index]||finished||mode!=='practice')return;
 if(index===round.length-1){finished=true;renderResults();}else{index++;renderQuestion();}
 focusHeading();
}
function renderResults(){
 const missed=round.filter((q,i)=>!answers[i].correct),count=round.length-missed.length;
 $('activity').innerHTML=`<section class="results"><h2 tabindex="-1">${count} / ${round.length} correct</h2><p>${retry?'Retry complete.':'Round complete.'}</p>
 <div class="result-actions">${missed.length?`<button class="primary" id="retry">Retry ${missed.length} missed</button>`:''}<button class="${missed.length?'plain':'primary'}" id="again">Practice again</button></div>
 ${missed.length?`<div class="review"><h3>Review missed answers</h3>${missed.map(q=>`<article><h3>${escapeHTML(q.question)}</h3><p><strong>${escapeHTML(q.answer)}</strong></p>${explanation(q)}</article>`).join('')}</div>`:''}
 <details class="review"><summary>Review all ${round.length} answers</summary>${round.map(q=>`<article><h3>${escapeHTML(q.question)}</h3><p><strong>${escapeHTML(q.answer)}</strong></p>${explanation(q)}</article>`).join('')}</details></section>`;
 if($('retry'))$('retry').addEventListener('click',()=>{begin(missed,true);render();focusHeading();});
 $('again').addEventListener('click',()=>{begin();render();focusHeading();});
}
$('sections').innerHTML=[{id:'all',title:'All topics',items:allItems},...sections].map(s=>`<option value="${s.id}">${escapeHTML(s.title)} (${s.items.length})</option>`).join('');
$('sections').addEventListener('change',()=>chooseSection($('sections').value));
$('sections').addEventListener('focus',cancelAdvance);
$('study').addEventListener('click',()=>{mode=mode==='study'?'practice':'study';render();focusHeading();});
$('auto').addEventListener('change',cancelAdvance);
$('options').addEventListener('toggle',()=>{if($('options').open)cancelAdvance();});
$('restart').addEventListener('click',()=>{mode='practice';begin();$('options').open=false;render();focusHeading();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelAdvance();});
// Cancel before focus or a pointer action can be displaced by the timer.
 document.addEventListener('keydown',event=>{if(event.key==='Tab'||event.key==='Escape')cancelAdvance();});
 document.addEventListener('pointerdown',()=>{if(timer!==null)cancelAdvance();});
begin();render();
