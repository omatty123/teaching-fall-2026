(() => {
 const main=document.querySelector('main'),nav=document.querySelector('.sections');
 const topics=[...main.querySelectorAll(':scope > section')];
 const select=document.createElement('select');select.className='topic-select';select.setAttribute('aria-label','Choose a lesson topic');
 topics.forEach(t=>{const o=document.createElement('option');o.value=t.id;o.textContent=({'region':'1 · Rebuilding empire','changan':'2 · Chang’an','tang-culture':'3 · Tang culture','tang-crisis':'4 · Du Fu / Bai Juyi','silla':'5 · Silla and Balhae','seokguram':'6 · Silla Buddhism','japan':'7 · Japan','shomu':'8 · Shōmu and Tōdai-ji','close':'9 · Comparison','resources':'Readings'})[t.id];select.append(o)});
 nav.before(select);
 const all=document.createElement('button');all.className='all';all.textContent='Read all topics';all.setAttribute('aria-pressed','false');nav.append(all);
 const pager=document.createElement('nav');pager.className='pager';pager.setAttribute('aria-label','Lesson sequence');main.querySelector('footer').before(pager);
 let showAll=false;
 function render(scroll=false){let id=location.hash.slice(1),i=topics.findIndex(t=>t.id===id);if(i<0)i=0;
 document.body.classList.toggle('poetry-view',!showAll&&topics[i].id==='tang-crisis');
 topics.forEach((t,j)=>t.hidden=!showAll&&j!==i);select.value=topics[i].id;
 nav.querySelectorAll('a').forEach(a=>{if(a.hash==='#'+topics[i].id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
 pager.replaceChildren();[i-1,i+1].forEach((j,k)=>{if(topics[j]){const a=document.createElement('a');a.href='#'+topics[j].id;a.textContent=(k?'Next: ':'Previous: ')+topics[j].querySelector('h2').textContent;pager.append(a)}});
 all.textContent=showAll?'View one topic':'Read all topics';all.setAttribute('aria-pressed',String(showAll));
 if(scroll){const heading=topics[i].querySelector('h2');heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true});(showAll?topics[i]:main).scrollIntoView({block:'start'});}
 }
 all.onclick=()=>{showAll=!showAll;render()};select.onchange=()=>location.hash=select.value;
 window.addEventListener('hashchange',()=>render(true));document.body.classList.add('viewer');render();
})();

// Keep each poet's verse together; preserve both authors without JavaScript.
document.querySelectorAll('.poets').forEach(group=>{
 const tabs=[...group.querySelectorAll('[role=tab]')];
 const panels=[...group.querySelectorAll('.poet-focus')];
 function choose(index,focus=false){
  tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;panels[i].hidden=i!==index;});
  if(focus)tabs[index].focus();
 }
 panels.forEach((p,i)=>{p.setAttribute('role','tabpanel');p.setAttribute('aria-labelledby',tabs[i].id);p.tabIndex=0;});
 tabs.forEach((tab,i)=>{
  tab.addEventListener('click',()=>choose(i));
  tab.addEventListener('keydown',event=>{
   let next=i;
   if(event.key==='ArrowRight')next=(i+1)%tabs.length;
   else if(event.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;
   else if(event.key==='Home')next=0;
   else if(event.key==='End')next=tabs.length-1;
   else return;
   event.preventDefault();choose(next,true);
  });
 });
 group.classList.add('enhanced');group.querySelector('.poet-switch').hidden=false;choose(0);
});
