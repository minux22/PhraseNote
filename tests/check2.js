const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const core=html.match(/<script id="core">([\s\S]*?)<\/script>/)[1];
const ui=html.match(/<script id="ui">([\s\S]*?)<\/script>/)[1];
new Function(ui);
const Core=new Function(core+';return Core;')();
const assert=require('assert');
// ids referenced by UI exist in markup
const ids=[...ui.matchAll(/\$\('#([A-Za-z]+)'\)/g)].map(m=>m[1]);
const missing=[...new Set(ids)].filter(i=>!html.includes('id="'+i+'"'));
console.log('missing ids:',missing);
// random: every pool item x scale x bars x sev
let n=0;
for(const scale of ['major','minor','harm'])for(const bars of [4,8,16])for(const sev of [false,true])for(let last=-1;last<10;last++){
  const p=Core.normalize({scale,bars,sev,key:3});
  for(const r of [0,0.3,0.99]){
    const out=Core.randomChords(p,()=>r,last);
    assert.strictEqual(out.chords.length,bars*4);
    assert(out.chords.every(c=>Number.isInteger(c)&&((c>=0&&c<=13)||(c>=1000&&c<1200))));
    assert(out.i!==last);
    if(sev)assert(out.chords.every(c=>c&1));
    if(bars>4)assert.strictEqual(out.chords[bars*4-1]&~1,8);
    p.chords=out.chords; for(let s=0;s<bars*8;s++)Core.eventsAt(p,s);
    Core.buildMidi(p); n++;
  }
}
console.log('random combos ok:',n);
const p=Core.normalize({scale:'major',bars:8,key:0}); 
const a=Core.randomChords(p,()=>0.99,-1); console.log('last pool item (major, 8 bars):',a.names, a.chords.join(','));
const q=Core.normalize({scale:'harm',bars:4,key:9,sev:true}); const b=Core.randomChords(q,()=>0.1,-1); console.log('harm minor 7th:',b.names);
const c=Core.randomChords(Core.normalize({scale:'major',bars:4,key:0}),()=>0.9,-1); console.log('canon-ish idx9:',c.i,c.names,c.chords.join(','));
// harmonic minor pool must not contain III or VII triads
for(const prog of Core.POOL_HARM)for(const bar of prog)for(const c of bar)assert(c>=1000||![2,6].includes(c>>1),'harm pool has III/VII');
const labs=Core.POOL_HARM.map((_,i)=>Core.randomChords(Core.normalize({scale:'harm',key:9,sev:false}),()=>i/6+0.01,-1).names);
console.log('harm pool (A):',labs.join(' | '));
console.log('minor pool (A nat):',Core.POOL_MINOR.map((_,i)=>Core.randomChords(Core.normalize({scale:'minor',key:9}),()=>i/Core.POOL_MINOR.length+0.01,-1).names).join(' | '));
console.log('pool ok');
