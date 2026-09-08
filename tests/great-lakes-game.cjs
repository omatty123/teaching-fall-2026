const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 require('node:fs').mkdirSync('.impeccable/review/great-lakes',{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`${process.env.GAME_BASE_URL||'http://127.0.0.1:8781'}/courses/great-lakes-game.html`);
 await page.screenshot({path:'.impeccable/review/great-lakes/desktop.png',fullPage:true});
 assert.equal(await page.locator('.gl-marker').count(),21);
 const items=await page.evaluate(()=>window.pageConfig.items);
 let name=await page.locator('#place-name').textContent(); let first=items.find(i=>`Find ${i.name}`===name).id;
 const wrong=items.find(i=>i.id!==first).id;
 await page.locator(`[data-id="${wrong}"]`).dispatchEvent('click');
 assert.match(await page.locator('#feedback').textContent(),/Keep looking/);
 await page.locator('#study-mode').click();
 await page.locator('[data-id="13"]').dispatchEvent('click');
 assert.equal(await page.locator('#place-name').textContent(),'St. Lawrence Seaway');
 await page.locator('#play-mode').click();
 assert.equal(await page.locator('#place-name').textContent(),name);
 await page.locator('#map-number').fill(String(first)); await page.locator('#number-form button').click();
 assert.match(await page.locator('#score').textContent(),/^0 of 1/);
 await page.locator('#next').click();
 let secondName=await page.locator('#place-name').textContent();
 await page.locator('#reveal').click();
 assert.match(await page.locator('#feedback').textContent(),/Here it is/);
 await page.locator('#next').click();
 for(let n=2;n<21;n++){
   name=await page.locator('#place-name').textContent(); const id=items.find(i=>`Find ${i.name}`===name).id;
   // Exercise actual keyboard event handlers, not a exposed state API.
   const target=page.locator(`[data-id="${id}"]`); await target.focus(); await target.press(n%2?'Enter':'Space');
   assert.match(await page.locator('#feedback').textContent(),/Correct/);
   await page.locator('#next').click();
 }
 assert.equal(await page.locator('#place-category').textContent(),'19 of 21 on the first try');
 await page.screenshot({path:'.impeccable/review/great-lakes/results.png',fullPage:true});
 await page.locator('#retry').click();
 assert.equal(await page.locator('#progress-text').textContent(),'1 / 2');
 for(let n=0;n<2;n++){
   name=await page.locator('#place-name').textContent(); const id=items.find(i=>`Find ${i.name}`===name).id;
   assert.ok([first,items.find(i=>`Find ${i.name}`===secondName).id].includes(id));
   await page.locator('#map-number').fill(String(id)); await page.locator('#number-form button').click(); await page.locator('#next').click();
 }
 assert.equal(await page.locator('#retry').isVisible(),false);
 assert.equal(await page.locator('#place-category').textContent(),'2 of 2 on the first try');
 await page.locator('#restart').click(); assert.equal(await page.locator('#progress-text').textContent(),'1 / 21');
 await page.locator('#study-mode').click(); await page.screenshot({path:'.impeccable/review/great-lakes/study.png',fullPage:true});
 // Every visible map target must be distinct, in bounds, and reachable at its center.
 const hitChecks=await page.evaluate(()=>[...document.querySelectorAll('.gl-marker')].map(el=>{
   const r=el.getBoundingClientRect(); const s=document.querySelector('.gl-map-scroll');s.scrollLeft+=r.x+r.width/2-s.getBoundingClientRect().x-s.clientWidth/2;
   const b=el.getBoundingClientRect(); return {id:el.dataset.id,width:b.width,hit:document.elementFromPoint(b.x+b.width/2,b.y+b.height/2)?.closest('.gl-marker')?.dataset.id};
 }));
 console.log('Marker targets',hitChecks);assert.ok(hitChecks.every(i=>i.id===i.hit));
 const mobile=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});
 mobile.on('pageerror',e=>errors.push(e.message)); await mobile.goto(`${process.env.GAME_BASE_URL||'http://127.0.0.1:8781'}/courses/great-lakes-game.html`);
 await mobile.screenshot({path:'.impeccable/review/great-lakes/mobile.png',fullPage:true});
 assert.ok(await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await mobile.locator('#study-mode').click();
 await mobile.locator('#study-list button').filter({hasText:'Toronto'}).click();
 assert.equal(await mobile.locator('#place-name').textContent(),'Toronto');
 const pan=await mobile.locator('.gl-map-scroll').evaluate(el=>el.scrollLeft); assert.ok(pan>400);
 await mobile.evaluate(()=>scrollTo(0,0));
 await mobile.screenshot({path:'.impeccable/review/great-lakes/mobile-study.png',fullPage:true});
 assert.deepEqual(errors,[]);
 console.log('PASS: 21 markers; wrong answer; study pause/resume; reveal; keyboard; 19/21 completion; missed-only retry; perfect retry; reset; phone pan; no page overflow or JS errors.');
 await browser.close();
})();
