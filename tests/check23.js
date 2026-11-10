// bass techniques: every one plays in 4/4 and 3/4, stays in range, and walking leads into the next root
const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const core=html.match(/<script id="core">([\s\S]*?)<\/script>/)[1];
const Core=new Function(core+';return Core;')();
const assert=require('assert');
function bassOf(bpat,ts,chords){
  const p=Core.defaults();Core.applyStyle(p,'beat');p.ts=ts||'4/4';p.bass=true;p.bpat=bpat;
  const M=Core.meter(p);p.chords=chords||[0,0,0,0,10,10,10,10];p.bars=p.chords.length/M.bpb;
  const ev=[];for(let s=0;s<p.chords.length*M.sps;s++)Core.eventsAt(p,s,'rock8').forEach(e=>{if(e.k==='b')ev.push(Object.assign({t:s*0.5+(e.off||0)},e));});
  return ev;
}
Core.BASSES.forEach(function(b){
  ['4/4','3/4'].forEach(function(ts){
    const ev=bassOf(b[0],ts,ts==='3/4'?[0,0,0,10,10,10]:undefined);
    assert(ev.length>0,b[0]+' '+ts+' silent');
    ev.forEach(e=>{assert(e.midi>=28&&e.midi<=60,b[0]+' range '+e.midi);assert(e.dur>0,b[0]+' dur');});
  });
});
// walking in C -> Am: only chord tones; beat 4 of bar 1 is the C-chord tone closest to A (G)
const w=bassOf('walk');const b4=w.filter(e=>Math.abs(e.t-3)<0.01)[0];
assert(b4&&b4.midi%12===7,'approach '+(b4&&b4.midi));
assert.strictEqual(w.filter(e=>e.t===4)[0].midi%12,9);
// a longer line (C Am Dm G7 C/E): every note is a tone of its chord, no leap over a sixth
{const ch=[0,0,0,0,10,10,10,10,2,2,2,2,9,9,9,9,42,42,42,42,1,1,1,1];const ev=bassOf('walk','4/4',ch);
 const p=Core.defaults();ev.forEach(function(e,i){const inf=Core.chordInfo(ch[Math.round(e.t)],0,'major');
   const pcs=inf.tones.slice(0,inf.sev?4:3).map(x=>((x%12)+12)%12).concat([((inf.bassTone%12)+12)%12]);
   assert(pcs.indexOf(e.midi%12)>=0,'non-chord tone '+e.midi+' at '+e.t);
   if(i)assert(Math.abs(e.midi-ev[i-1].midi)<=9,'leap '+ev[i-1].midi+'->'+e.midi);});
 console.log('walk line',ev.map(e=>e.midi).join(' '));}
assert.strictEqual(Core.bassKind('slap'),'electric');assert.strictEqual(Core.bassPatch('walk'),32);assert.strictEqual(Core.bassPatch('sub'),39);
console.log('bass ok',w.map(e=>e.midi).join(' '));
// MIDI: Bass on Auto writes each slot's program
const q=Core.defaults();q.chords=[0,0,0,0,0,0,0,0];q.bars=4;q.bpat='walk';
const n=Core.normalize?Core.normalize(q):q;
if(n.secs&&n.secs.length){const B=JSON.parse(JSON.stringify(n.secs[0]));B.id='B';B.bpat='slap';B.bkind='electric';n.secs.push(B);n.form=[n.form[0],'B'];}
const mid=Array.from(Core.buildMidi(n,null,{bauto:true}));const pcs=[];for(let i=0;i<mid.length-1;i++)if(mid[i]===0xC1)pcs.push(mid[i+1]);
assert(pcs.indexOf(32)>=0&&pcs.indexOf(36)>=0,'bass programs '+pcs);console.log('bass midi',pcs);
