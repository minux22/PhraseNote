const {chromium}=require('playwright');const fs=require('fs');
const OUT='guide/img/', META=[];
// demo project: A Verse (I vi IV V), B Chorus (IV V iii vi), melody over 8 bars
const mel=[];const ph=[[67,0,480],[69,480,480],[72,960,960],[71,1920,480],[69,2400,480],[67,2880,960],[64,3840,480],[65,4320,480],[67,4800,960],[69,5760,1920],
 [72,7680,480],[74,8160,480],[76,8640,960],[74,9600,480],[72,10080,480],[71,10560,960],[69,11520,960],[71,12480,480],[72,12960,1920]];
ph.forEach(([p,s,l])=>mel.push({s,l,p}));
const sec=(id,role,ch,drum)=>({bars:4,chords:ch,comp:'beat',voic:'close',inv:false,strum:0,bpat:'root',swing:0,swu:'8',color:'off',lay:0,loose:0,drum:true,dpat:drum,id,role});
const A=[0,0,0,0,10,10,10,10,6,6,6,6,8,8,8,8], B=[6,6,6,6,8,8,8,8,4,4,4,4,10,10,10,10];
const PROJ={v:2,key:0,scale:'major',bpm:96,ts:'4/4',unit:2,sev:false,bass:true,mel,melAmt:30,pick:false,name:'My Song',
  secs:[sec('A','Verse',A,'pop16'),sec('B','Chorus',B,'rock8')],form:['A','B'],slot:0};
Object.assign(PROJ,{chords:A,comp:'beat',drum:true,dpat:'pop16'});
const UI={fsAsked:true,drum:true,dpat:'pop16',cmode:'song',zoom:24,tool:'pen',view:'roll',recMode:'loop',recA:1,recB:4,recLat:0.12};
(async()=>{
const b=await chromium.launch({args:['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream','--autoplay-policy=no-user-gesture-required']});
const ctx=await b.newContext({viewport:{width:360,height:780},deviceScaleFactor:2,colorScheme:'dark',permissions:['microphone']});
const pg=await ctx.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.addInitScript(([P,U])=>{if(!sessionStorage.getItem('x')){sessionStorage.setItem('x',1);localStorage.clear();localStorage.setItem('phrasenote-init-1','1');localStorage.setItem('chord-sketch-comp1','1');localStorage.setItem('phrasenote-ui',JSON.stringify(U));localStorage.setItem('chord-sketch-v1',JSON.stringify(P));}},[PROJ,UI]);
await pg.goto('http://localhost:8765/index.html');await pg.waitForTimeout(900);
const box=async sel=>pg.$eval(sel,e=>{const r=e.getBoundingClientRect();return {x:r.left,y:r.top+scrollY,w:r.width,h:r.height};});
// marks: [n, selector, where('tl'|'tr'|'c'|'l'|'r')]
async function chrome(on){await pg.evaluate(on=>{let st=document.getElementById('gsty');if(!st){st=document.createElement('style');st.id='gsty';document.body.appendChild(st);}st.textContent=on?'':'.dock,#toast{display:none!important} body.kbd-open{padding-bottom:0!important}';},on);}
async function shot(name,clipSel,marks,opt={}){
  let clip;
  if(!opt.view){await chrome(!!opt.keepChrome);await pg.evaluate(()=>scrollTo(0,0));await pg.waitForTimeout(150);}else await chrome(true);
  if(clipSel==='view')clip={x:0,y:await pg.evaluate(()=>scrollY),w:360,h:780};
  else if(typeof clipSel==='object'&&!Array.isArray(clipSel))clip=clipSel;
  else{const bs=[];for(const s of [].concat(clipSel))bs.push(await box(s));const x0=Math.min(...bs.map(r=>r.x)),y0=Math.min(...bs.map(r=>r.y)),x1=Math.max(...bs.map(r=>r.x+r.w)),y1=Math.max(...bs.map(r=>r.y+r.h));
    const pad=opt.pad==null?8:opt.pad;clip={x:0,y:Math.max(0,y0-pad),w:360,h:y1-y0+2*pad};}
  if(opt.fixed){ // element is position:fixed: use viewport coordinates
  }
  const m=[];
  for(const [n,sel,wh] of marks){const r=await box(sel);let x=r.x,y=r.y;const w=wh||'tl';
    if(w==='c'){x=r.x+r.w/2;y=r.y+r.h/2;}else if(w==='tr'){x=r.x+r.w;}else if(w==='l'){y=r.y+r.h/2;}else if(w==='r'){x=r.x+r.w;y=r.y+r.h/2;}else if(w==='b'){x=r.x+r.w/2;y=r.y+r.h;}else if(w==='t'){x=r.x+r.w/2;}
    m.push({n,x:x-clip.x,y:y-clip.y});}
  await pg.screenshot({path:OUT+name+'.png',clip:{x:clip.x,y:clip.y,width:clip.w,height:clip.h},fullPage:!opt.view});
  META.push({name,w:clip.w,h:clip.h,marks:m});
  await chrome(true);
}
// 1 main screen
await shot('main','view',[[1,'#playBtn','tl'],[2,'#rewBtn','tl'],[3,'#bpmVal','tl'],[4,'#drumBtn','tl'],[5,'#drumPick','tr'],[6,'#undoBtn','tl'],[7,'#tsSel','tl'],[8,'#tabChord','tl'],[9,'#dockMix','tl'],[10,'#dockFile','tl']],{view:true});
// 2 song structure
await shot('form','#formPanel',[[1,'#formRow .slot >> nth=0','tl'],[2,'#formRow .slot.add','tl'],[3,'#cmodeSw','tl'],[4,'#slotMenuBtn','tl']]);
// 3 chords panel
await pg.evaluate(()=>document.querySelector('#palette').scrollIntoView({block:'start'}));await pg.waitForTimeout(200);
await shot('chords',['#togBass','#hint'],[[1,'#palette .chip >> nth=0','tl'],[2,'#grid','tl'],[3,'#unitSeg','tl'],[4,'#barsSeg','tl'],[5,'#togBass','tl'],[6,'#togSlash','tl'],[7,'#btnRand','tl'],[8,'#xToggle','tl']]);
// 4 accompaniment
await shot('accomp','#compPanel',[[1,'#compChips','tl'],[2,'#voicSeg','tl'],[3,'#strumR','tl'],[4,'#swingR','tl']]);
// 5 drum pattern list + My pattern grid
await pg.evaluate(()=>scrollTo(0,0));await pg.click('#drumPick');await pg.waitForTimeout(300);
await pg.evaluate(()=>{const e=document.querySelector('#patList button[data-p=custom]');e.scrollIntoView({block:'end'});});await pg.waitForTimeout(200);
await shot('drumlist','#patDlg .dlg',[[1,'#patList button[data-p=custom]','l']],{pad:0});
await pg.click('#patList button[data-p=custom]');await pg.waitForTimeout(500);
await shot('drumgrid','#dSlide .dlg',[[2,'#dRes','tl'],[3,'#dTest','tl'],[4,'#dCopy','tl'],[5,'#dGrid','tl']],{pad:0});
await pg.click('#dsClose');await pg.waitForTimeout(200);
// set pattern back to pop16 via list
await pg.click('#drumPick');await pg.waitForTimeout(200);await pg.click('#patList button[data-p=pop16]');await pg.waitForTimeout(200);await pg.keyboard.press('Escape');
await pg.evaluate(()=>{const d=document.getElementById('patDlg');if(!d.hidden)document.getElementById('patClose').click();});
// 6 melody roll
await pg.click('#tabMelody');await pg.waitForTimeout(600);await pg.evaluate(()=>scrollTo(0,0));
await pg.evaluate(()=>{const ns=[...document.querySelectorAll('#rPlane .nt')];const top=Math.min(...ns.map(n=>n.offsetTop)),bot=Math.max(...ns.map(n=>n.offsetTop));const r=document.getElementById('roll');r.scrollTop=Math.max(0,(top+bot)/2-120);});
const rt=await box('#panelMelody .ctl'), rr=await box('#roll');
await shot('roll',{x:0,y:rt.y-8,w:360,h:rr.y-rt.y+300},[[1,'#viewSeg','tl'],[2,'#togPick','tl'],[3,'#melAmt','tl'],[4,'#toolSeg','tl'],[5,'#lenSel','tl'],[6,'#rLaneP','tl']]);
await pg.evaluate(()=>{scrollTo(0,0);document.getElementById('toast').classList.remove('show');const ns=[...document.querySelectorAll('#rPlane .nt')];const top=Math.min(...ns.map(n=>n.offsetTop)),bot=Math.max(...ns.map(n=>n.offsetTop));const r=document.getElementById('roll');r.scrollTop=Math.max(0,(top+bot)/2-200);});await pg.waitForTimeout(300);
await pg.screenshot({path:OUT+'cover_roll.png'});META.push({name:'cover_roll',w:360,h:780,marks:[]});
// 7 staff
await pg.click('#viewSeg button >> nth=1');await pg.waitForTimeout(700);
await shot('staff',['#panelMelody .ctl','#stWrap'],[[1,'#toolSeg2','tl'],[2,'#nvSeg','tl'],[3,'#dotSeg','tl'],[4,'#accSeg','tl']]);
await pg.click('#viewSeg button >> nth=0');await pg.waitForTimeout(500);
// 8 keys
await pg.click('#dockKeys');await pg.waitForTimeout(500);
await pg.evaluate(()=>{const t=document.getElementById('toast');t.classList.remove('show');});
await shot('keys',{x:0,y:await pg.evaluate(()=>scrollY),w:360,h:780},[[1,'#kMode','tl'],[2,'#kRec','tl'],[3,'#kQ','tl'],[4,'#kLat','tl'],[5,'#kOctDn','tl']],{view:true});
await pg.click('#dockKeys');await pg.waitForTimeout(300);
// 9 quantize open
await pg.evaluate(()=>{document.getElementById('qHead').click();});await pg.waitForTimeout(500);
await pg.evaluate(()=>document.querySelector('.qbox').scrollIntoView({block:'center'}));await pg.waitForTimeout(200);
await shot('quant','.qbox',[[1,'#qGridSeg','tl'],[2,'#qStr','tl'],[3,'#btnQuant','tl']]);
await pg.evaluate(()=>{document.getElementById('qHead').click();scrollTo(0,0);});
// 10 suggest chords (palette with melody) + key guess
await pg.click('#tabChord');await pg.waitForTimeout(400);
await pg.evaluate(()=>document.querySelector('#palette').scrollIntoView({block:'start'}));
await shot('suggest',['#togBass','#palette'],[[2,'#btnRand','tl']]);
await pg.evaluate(()=>scrollTo(0,0));await pg.selectOption('#keySel','guess');await pg.waitForTimeout(400);
await shot('keyguess','#formDlg .dlg',[[1,'#formBody .sfbar >> nth=0','tl']],{pad:0});
await pg.evaluate(()=>{const d=document.getElementById('formDlg');d.hidden=true;});
// 11 audio mode: record takes on A loop (2 passes), then on B
await pg.click('#tabMelody');await pg.click('#viewSeg button >> nth=2');await pg.waitForTimeout(1500);
const rec=async ms=>{await pg.click('#recBtn');await pg.waitForTimeout(ms);await pg.click('#recBtn');await pg.waitForTimeout(800);};
await rec(6000*1.0+5000);
await pg.fill('#recA','5');await pg.press('#recA','Tab');await pg.fill('#recB','8');await pg.press('#recB','Tab');
await rec(11500);
// select section A on the timeline, playhead at bar 2
await pg.evaluate(()=>{const c=document.getElementById('recCv'),r=c.getBoundingClientRect();document.getElementById('recIn').dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.left+r.width*(1.5/12),clientY:r.top+90}));});
await pg.fill('#recA','1');await pg.press('#recA','Tab');await pg.fill('#recB','4');await pg.press('#recB','Tab');await pg.waitForTimeout(400);
await pg.evaluate(()=>scrollTo(0,0));
await pg.evaluate(()=>document.querySelectorAll('#recDev option').forEach(o=>o.textContent='Microphone'));
await pg.evaluate(()=>{scrollTo(0,0);document.getElementById('toast').classList.remove('show');});await pg.waitForTimeout(200);
await pg.screenshot({path:OUT+'cover_audio.png'});META.push({name:'cover_audio',w:360,h:780,marks:[]});
await shot('audio',['#panelMelody .ctl','#takeList'],[[1,'#viewSeg','tl'],[2,'#recDev','tl'],[3,'#recCal','tl'],[4,'#recGain','tl'],[5,'#recModeSw','tl'],[6,'#recRng','tl'],[7,'#recBtn','tl'],[8,'#recWrap','tl'],[9,'#takeList .thead','tl']]);
// 12 loop growth (roll with ghost) : project with only A? use current: chord tab loop + slot A followed by B -> no ghost. Make a single-slot copy view: select B (last) and show roll
await pg.click('#viewSeg button >> nth=0');await pg.waitForTimeout(400);
await pg.click('#tabChord');await pg.waitForTimeout(300);await pg.click('#cmodeSw');await pg.waitForTimeout(200);
const nSl=await pg.$$eval('#formRow .slot:not(.add)',x=>x.length);await pg.click('#formRow .slot:not(.add) >> nth='+(nSl-1));await pg.waitForTimeout(300);
await pg.click('#tabMelody');await pg.waitForTimeout(600);
await pg.evaluate(()=>{const r=document.getElementById('roll'),g=document.querySelector('#rLaneP .cb.gcopy');r.scrollLeft=Math.max(0,g.offsetLeft-150);scrollTo(0,0);});await pg.waitForTimeout(400);
const gr=await box('#roll');await shot('ghost',{x:0,y:gr.y-4,w:360,h:230},[[1,'#rLaneP .cb.gcopy','c']]);
// 13 mixer
await pg.click('#playBtn');await pg.click('#dockMix');await pg.waitForTimeout(2500);
const mb=await pg.$eval('#mixer',e=>{const r=e.getBoundingClientRect();return {x:0,y:r.top,w:360,h:r.height};});
const vm=async sel=>pg.$eval(sel,e=>{const r=e.getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height};});
{const m=[];const add=async(n,s,w)=>{const r=await vm(s);m.push({n,x:(w==='c'?r.x+r.w/2:r.x)-mb.x,y:(w==='c'?r.y+r.h/2:r.y)-mb.y});};
 await add(1,'#mxIn .mx[data-k=m] .mn');await add(2,'#mxIn .mx[data-k=c] .fw input','c');await add(3,'#mxIn .mx[data-k=b] .ms button.m');await add(4,'#mxIn .mx[data-k=b] .ms button.s');await add(5,'#mxIn .mx[data-k=rev] .mn');await add(6,'#mxIn .mx[data-k=mst] .mn');await add(7,'#mxLed');
 await pg.screenshot({path:OUT+'mixer.png',clip:{x:0,y:mb.y,width:360,height:mb.h}});META.push({name:'mixer',w:360,h:mb.h,marks:m});}
await pg.click('#playBtn');await pg.click('#dockMix');await pg.waitForTimeout(300);
// 14 setup: project + sound
await pg.click('#dockFile');await pg.waitForTimeout(1200);
const sv=async(name,firstSel,lastSel,marks)=>{
  await pg.$eval(firstSel,e=>e.scrollIntoView({block:'start'}));await pg.waitForTimeout(250);
  const a=await vm(firstSel), z=await vm(lastSel);console.log(name,a,z);const clip={x:0,y:Math.max(0,a.y-4),w:360,h:Math.min(780-Math.max(0,a.y-4),z.y+z.h-a.y+14)};
  const m=[];for(const [n,s] of marks){const r=await vm(s);m.push({n,x:r.x-clip.x,y:r.y-clip.y});}
  await pg.screenshot({path:OUT+name+'.png',clip:{x:0,y:clip.y,width:360,height:clip.h}});META.push({name,w:360,h:clip.h,marks:m});};
await sv('setup_project','#btnNew','#recentBox',[[1,'#btnNew'],[2,'#btnLoad'],[3,'#btnSave'],[4,'#btnSaveAs'],[5,'#recentBox']]);
await pg.click('#modeSf');await pg.waitForTimeout(400);
await sv('setup_sound','#modeBasic','#dEdit',[[1,'#modeBasic'],[2,'#btnSf'],[3,'#dPat']]);
fs.writeFileSync('guide/meta.json',JSON.stringify(META,null,1));
console.log('errors',errs);await b.close();})();
