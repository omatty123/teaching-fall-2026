'use strict';
const {sections,sources}=window.QUIZ_DATA;
const allItems=sections.flatMap(s=>s.items.map(q=>({...q,section:s.id})));
const $=id=>document.getElementById(id);
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function shuffled(items){const a=[...items];for(let i=a.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
let selected=sections.some(s=>s.id===location.hash.slice(1))?location.hash.slice(1):'dynasties',mode='practice',round=[],index=0,answers=[],finished=false,retry=false;
const sessions=new Map();
function pool(){return selected==='all'?allItems:allItems.filter(q=>q.section===selected);}
function begin(items=pool(),isRetry=false){round=shuffled(items).map(q=>({...q,choices:shuffled([q.answer,...q.distractors])}));index=0;answers=[];finished=false;retry=isRetry;}
function saveSession(){sessions.set(selected,{round,index,answers,finished,retry});}
function chooseSection(id){saveSession();selected=id;const prior=sessions.get(id);if(prior)({round,index,answers,finished,retry}=prior);else begin();render();}
function refs(q){return `<div class="references">${q.sources.map(k=>`<a href="${escapeHTML(sources[k][1])}" target="_blank" rel="noopener">${escapeHTML(sources[k][0])} ↗</a>`).join('')}</div>`;}
function renderNav(){
 $('sections').innerHTML=[...sections,{id:'all',title:'Mix all sections',items:allItems}].map(s=>`<button data-section="${s.id}" aria-current="${selected===s.id}"><span>${escapeHTML(s.title)}</span><span class="count">${s.items.length}</span></button>`).join('');
 document.querySelectorAll('[data-section]').forEach(b=>b.addEventListener('click',()=>chooseSection(b.dataset.section)));
}
function render(){
 renderNav();const s=sections.find(s=>s.id===selected);$('section-title').textContent=s?s.title:'All sections';$('section-description').textContent=s?s.subtitle:'Books, thinkers, rulers, dynasties, dates, and cities';
 $('practice').setAttribute('aria-pressed',String(mode==='practice'));$('study').setAttribute('aria-pressed',String(mode==='study'));
 if(mode==='study')renderStudy();else if(finished)renderResults();else renderQuestion();
}
function renderStudy(){
 $('activity').innerHTML=`<p class="study-intro">Review each entry, then switch to Practice. Your current round will wait.</p><dl class="study-list">${pool().map(q=>`<div class="study-entry"><dt>${escapeHTML(q.label)}</dt><dd><p>${escapeHTML(q.detail)}</p>${refs(q)}</dd></div>`).join('')}</dl>`;
}
function renderQuestion(){
 const q=round[index],response=answers[index];const correct=answers.filter(a=>a.correct).length;
 $('activity').innerHTML=`<section class="quiz-box" aria-label="Practice question"><div class="quiz-top"><span>${retry?'Retry · ':''}Question ${index+1} of ${round.length}</span><span>${correct} correct · ${answers.length} answered</span></div><div class="progress" role="progressbar" aria-label="Questions answered" aria-valuenow="${answers.length}" aria-valuemin="0" aria-valuemax="${round.length}"><span style="width:${100*answers.length/round.length}%"></span></div><h2 class="question" tabindex="-1">${escapeHTML(q.question)}</h2><div class="answers">${q.choices.map((option,i)=>{const cls=response?(option===q.answer?'correct':option===response.choice?'incorrect':'muted'):'';return `<button class="answer ${cls}" data-option="${i}" ${response?'disabled':''}><span class="letter" aria-hidden="true">${String.fromCharCode(65+i)}</span><span>${escapeHTML(option)}${response&&option===q.answer?' · Correct answer':''}${response&&option===response.choice&&!response.correct?' · Your answer':''}</span></button>`;}).join('')}</div><div id="feedback" aria-live="polite">${response?`<div class="feedback"><h3>${response.correct?'Correct.':'Review this answer.'}</h3><p>${escapeHTML(q.detail)}</p>${refs(q)}<button class="primary" id="next">${index===round.length-1?'See results':'Next question'}</button></div>`:''}</div><div class="question-footer"><span>Choose one answer. Explanations follow.</span><button class="plain" id="restart">Restart section</button></div></section>`;
 document.querySelectorAll('[data-option]').forEach(b=>b.addEventListener('click',()=>answer(Number(b.dataset.option))));
 $('restart').addEventListener('click',()=>{begin();render();});
 if(response)$('next').addEventListener('click',next);
}
function answer(option){if(answers[index])return;const q=round[index],choice=q.choices[option];answers.push({id:q.id,choice,correct:choice===q.answer});renderQuestion();$('next').focus({preventScroll:true});}
function next(){if(!answers[index])return;if(index===round.length-1){finished=true;renderResults();document.querySelector('.results h2').focus({preventScroll:true});}else{index++;renderQuestion();document.querySelector('.question').focus({preventScroll:true});}}
function renderResults(){
 const missed=round.filter((q,i)=>!answers[i].correct),count=round.length-missed.length;
 $('activity').innerHTML=`<section class="quiz-box results"><h2 tabindex="-1">${missed.length?'Round complete':'All answers correct'}</h2><p class="score">${count} of ${round.length} correct${retry?' in this retry':''}.</p><div class="result-actions">${missed.length?`<button class="primary" id="retry">Retry ${missed.length} missed ${missed.length===1?'question':'questions'}</button>`:''}<button class="${missed.length?'secondary':'primary'}" id="again">Practice section again</button><button class="secondary" id="review-study">Study this section</button></div><p class="result-note">${missed.length?'Review the explanations below, or retry just the questions you missed.':'Try another section from the menu, or mix all six sections.'}</p>${missed.length?`<div class="review"><h3>Questions to revisit</h3>${missed.map(q=>`<article><h3>${escapeHTML(q.question)}</h3><p><strong>Answer:</strong> ${escapeHTML(q.answer)}</p><p>${escapeHTML(q.detail)}</p>${refs(q)}</article>`).join('')}</div>`:''}</section>`;
 if($('retry'))$('retry').addEventListener('click',()=>{begin(missed,true);render();});
 $('again').addEventListener('click',()=>{begin();render();});$('review-study').addEventListener('click',()=>{mode='study';render();});
}
$('practice').addEventListener('click',()=>{mode='practice';render();});$('study').addEventListener('click',()=>{mode='study';render();});
begin();render();
