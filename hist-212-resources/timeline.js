'use strict';
const detail=document.getElementById('detail');
const bank=new Map(window.QUIZ_DATA.sections.flatMap(s=>s.items.map(q=>[q.id,{...q,section:s.id}])));
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const overrides={
 'books-1':{label:'Yijing · Changes 易經',detail:'The Classic of Changes is associated with divination. Its early material and later commentaries formed over time; the position on the chart is not a precise publication date.',sources:['classics']},
 'books-2':{label:'Shijing · Songs 詩經',detail:'The Classic of Poetry, also translated Book of Songs or Book of Odes, collects early Chinese poems and songs. These English names refer to the same work.',sources:['classics']},
 'books-3':{label:'Shujing · Documents 書經',detail:'The Classic of Documents, also known as the Shangshu, preserves speeches and documents attributed to early rulers and ministers. The dates of narrated events and the dates of textual composition are not the same.',sources:['classics']},
 'books-4':{label:'Zuozhuan · Zuo Commentary 左傳',detail:'The Zuo Commentary, also called the Zuo Tradition, presents extended historical narratives traditionally associated with the Spring and Autumn Annals. Its formation and authorship are debated.',sources:['classics']},
 'books-5':{label:'Chunqiu · Spring and Autumn Annals 春秋',detail:'The Spring and Autumn Annals is the chronicle of the state of Lu. Its accounts cover 722–481 BCE. This is a range of narrated events, not a single composition date.',sources:['classics']},
 'books-6':{label:'Shiji · Records of the Grand Historian 史記',detail:'The Shiji is the Han-period history associated with Sima Qian, compiled around 100 BCE. It recounts much earlier history and is distinct from both the Shijing and the Shujing.',sources:['shiji']}
};
function primaryLinks(id){
 const catalog=window.PRIMARY_SOURCES,keys=catalog?.items[id]||[];
 if(!keys.length)return '';
 return `<section class="detail-primary"><h3>Primary sources</h3>${keys.map(k=>{const s=catalog.texts[k];return `<p><a href="${escapeHTML(s.url)}" target="_blank" rel="noopener">${escapeHTML(s.title)} ↗</a><small>${escapeHTML(s.language)}</small></p>`}).join('')}<small>Read later historical accounts as evidence of the traditions they preserve.</small></section>`;
}
let active=null;
detail.querySelector('.close').addEventListener('click',()=>detail.close());
document.querySelectorAll('[data-item]').forEach(button=>button.addEventListener('click',()=>{
 const original=bank.get(button.dataset.item);if(!original)return;const q={...original,...overrides[original.id]};const img=button.querySelector('img');
 document.getElementById('detail-content').innerHTML=`${img?`<img src="${escapeHTML(img.getAttribute('src'))}" alt="${escapeHTML(img.alt)}">`:''}<div><h2 id="detail-title">${escapeHTML(q.label)}</h2><p>${escapeHTML(q.detail)}</p>${img?'<p class="detail-portrait-caption">Original image from the class spreadsheet; a later representation.</p>':''}${primaryLinks(q.id)}<div class="detail-sources"><h3>Background references</h3>${q.sources.map(k=>`<a href="${escapeHTML(window.QUIZ_DATA.sources[k][1])}" target="_blank" rel="noopener">${escapeHTML(window.QUIZ_DATA.sources[k][0])} ↗</a>`).join('')}</div><a class="detail-quiz" href="quiz.html#${escapeHTML(q.section)}">Practice this section →</a></div>`;
 active=button;button.classList.add('active-entry');detail.showModal();
}));
detail.addEventListener('close',()=>{if(active)active.classList.remove('active-entry');});
detail.addEventListener('click',e=>{if(e.target===detail){const r=detail.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)detail.close();}});
const chart=document.getElementById('chart'),scroll=document.getElementById('chart-scroll');let zoom=1;
function resize(){const base=Math.max(1160,scroll.clientWidth);chart.style.width=`${base}px`;chart.style.zoom=zoom;document.getElementById('zoom-value').textContent=`${Math.round(zoom*100)}%`;document.getElementById('zoom-out').disabled=zoom===1;document.getElementById('zoom-in').disabled=zoom>=1.6;}
document.getElementById('zoom-in').addEventListener('click',()=>{zoom=Math.min(1.6,Math.round((zoom+.2)*10)/10);resize();});document.getElementById('zoom-out').addEventListener('click',()=>{zoom=Math.max(1,Math.round((zoom-.2)*10)/10);resize();});document.getElementById('fit').addEventListener('click',()=>{zoom=1;resize();scroll.scrollLeft=0;});window.addEventListener('resize',resize);resize();
