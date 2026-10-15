(() => {
 const main=document.querySelector('main'),nav=document.querySelector('.sections');
 const topics=[...main.querySelectorAll(':scope > section')];
 const select=document.createElement('select');select.className='topic-select';select.setAttribute('aria-label','Choose a lesson topic');
 topics.forEach(t=>{const o=document.createElement('option');o.value=t.id;o.textContent=({'region':'1 · Rebuilding empire','changan':'2 · Chang’an','tang-culture':'3 · Tang culture','tang-crisis':'4 · Crisis and poetry','silla':'5 · Silla and Balhae','seokguram':'6 · Silla Buddhism','japan':'7 · Japan','shomu':'8 · Shōmu and Tōdai-ji','close':'9 · Comparison','resources':'Readings'})[t.id];select.append(o)});
 nav.before(select);
 const all=document.createElement('button');all.className='all';all.textContent='Read all topics';all.setAttribute('aria-pressed','false');nav.append(all);
 const pager=document.createElement('nav');pager.className='pager';pager.setAttribute('aria-label','Lesson sequence');main.querySelector('footer').before(pager);
 let showAll=false;
 function render(scroll=false){let id=location.hash.slice(1),i=topics.findIndex(t=>t.id===id);if(i<0)i=0;
 topics.forEach((t,j)=>t.hidden=!showAll&&j!==i);select.value=topics[i].id;
 nav.querySelectorAll('a').forEach(a=>{if(a.hash==='#'+topics[i].id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
 pager.replaceChildren();[i-1,i+1].forEach((j,k)=>{if(topics[j]){const a=document.createElement('a');a.href='#'+topics[j].id;a.textContent=(k?'Next: ':'Previous: ')+topics[j].querySelector('h2').textContent;pager.append(a)}});
 all.textContent=showAll?'View one topic':'Read all topics';all.setAttribute('aria-pressed',String(showAll));
 if(scroll){const heading=topics[i].querySelector('h2');heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true});(showAll?topics[i]:main).scrollIntoView({block:'start'});}
 }
 all.onclick=()=>{showAll=!showAll;render()};select.onchange=()=>location.hash=select.value;
 window.addEventListener('hashchange',()=>render(true));document.body.classList.add('viewer');render();
})();
