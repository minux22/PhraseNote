const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
let tot=0;
for(const ts of ['2/4','3/4','4/4','5/4','6/8','9/8','12/8'])
for(const [st] of Core.COMPS)for(const voic of ['close','open','spread'])for(const bpat of ['root','r5','oct','kick'])for(const sev of [false,true])for(const color of ['off','add9','sus','69','nine']){
  const base=Core.normalize({bars:4,ts,comp:st,voic,bpat,swing:50,strum:20,inv:true,sev,color,lay:30});
  const M=Core.meter(base);
  const p=Core.normalize(Object.assign({},base,{color,chords:Array.from({length:4*M.bpb},(_,i)=>[0,8,10,6][Math.floor(i/M.bpb)]+(i===1?2:0))}));
  const S=M.bar/240;
  let n=0;
  for(let s=0;s<4*S;s++)for(const e of Core.eventsAt(p,s,'pop16')){
    n++;assert(e.midi>=24&&e.midi<=100,st+' midi '+e.midi);assert(e.dur>0,st+' dur');assert(e.vel>=1&&e.vel<=127);assert(e.off>=0&&e.off<1.2,st+' off '+e.off);
  }
  assert(n>0,st+' no events '+ts);tot+=n;
}
// legacy defaults: swing 0, no off, same as before
const p0=Core.normalize({bars:4});
const ev=Core.eventsAt(p0,0).map(e=>e.k+e.midi+'@'+(e.off||0)).join();
console.log('beat step0',ev);
// style summaries 4/4
for(const [st] of Core.COMPS){
  const p=Core.normalize({bars:4,comp:st,chords:[0,0,0,0,8,8,8,8,10,10,10,10,6,6,6,6]});
  const a=[];for(let s=0;s<8;s++)Core.eventsAt(p,s).filter(e=>e.k==='c').forEach(e=>a.push(s+'+'+e.off.toFixed(2)+':'+e.midi));
  console.log(st.padEnd(8),a.slice(0,14).join(' '));
}
// midi builds
for(const [st] of Core.COMPS){const p=Core.normalize({bars:4,comp:st,swing:60,chords:[0,0,0,0,8,8,8,8,10,10,10,10,6,6,6,6]});assert(Core.buildMidi(p,'rock8').length>100);}
console.log('events',tot,'ok');
// recipes
for(const [id] of Core.COMPS){const p=Core.normalize({bars:4});Core.applyStyle(p,id);const q=Core.normalize(p);assert.deepStrictEqual([q.comp,q.voic,q.color,q.bpat,q.strum,q.lay,q.swing,q.loose,q.inv],[p.comp,p.voic,p.color,p.bpat,p.strum,p.lay,p.swing,p.loose,p.inv],id);}
console.log('recipes ok');
