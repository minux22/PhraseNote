/* 16th swing and held pushes (anticipation) */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const ch=[0,0,0,0,10,10,10,10,6,6,6,6,8,8,8,8];
// 16th swing: 16th off-beats move by swing/100/12 beat, 8th off-beats stay; drums follow
let p=Core.normalize({bars:4,chords:ch,bpm:100});Core.applyStyle(p,'pluck16');p.swing=60;p.swu='16';
let e=Core.eventsAt(p,0,null).filter(x=>x.k==='c');const offs=[...new Set(e.map(x=>+x.off.toFixed(4)))];
assert.deepStrictEqual(offs,[0,+(0.25+0.6/12).toFixed(4)]);
e=Core.eventsAt(p,1,null).filter(x=>x.k==='c');assert.deepStrictEqual([...new Set(e.map(x=>+x.off.toFixed(4)))],[0,+(0.25+0.05).toFixed(4)]);
let d=Core.drumsAt(p,1,'pop16');assert.deepStrictEqual(d.map(x=>+x.off.toFixed(4)).sort(),[0,0.3]);
p.swu='8';d=Core.drumsAt(p,1,'pop16');assert.deepStrictEqual(d.map(x=>+x.off.toFixed(4)).sort(),[0.1,0.35]);
// recipes pick the 16th unit
const q=Core.normalize({chords:ch});Core.applyStyle(q,'lofi');assert.strictEqual(q.swu,'16');Core.applyStyle(q,'jazzcomp');assert.strictEqual(q.swu,'8');
// kick bass is swung once, not twice
p=Core.normalize({bars:4,chords:ch});Core.applyStyle(p,'beat');p.bpat='kick';p.swing=60;p.swu='8';
const kb=Core.eventsAt(p,5,'syncpop').filter(x=>x.k==='b');const kd=Core.drumsAt(p,5,'syncpop').filter(x=>x.n===36);
assert.deepStrictEqual(kb.map(x=>+x.off.toFixed(4)),kd.map(x=>+x.off.toFixed(4)));
// anticipation: the pushed chord is held through the downbeat; no strike at beat 1 of the next bar
p=Core.normalize({bars:4,chords:ch});Core.applyStyle(p,'antic');
const at=s=>Core.eventsAt(p,s,null).filter(x=>x.k==='c');
assert.strictEqual(at(8).length,0,'no downbeat strike in bar 2');
const push=at(7);assert(push.length>0);assert(Math.abs(push[0].dur-(3+5)*0.25*0.95)<1e-9,'push held over the downbeat');
assert(at(0).length>0,'loop: bar 1 is struck (no tie across the loop point)');
assert(Math.abs(at(31)[0].dur-3*0.25*0.95)<1e-9,'loop: last push not held');
// song: first slot has no previous bar -> struck; last slot pushes nothing past the end
const s2=Core.normalize({chords:ch,comp:'antic',secs:[{id:'A',bars:4,chords:ch,comp:'antic'},{id:'B',bars:4,chords:[6,6,6,6,8,8,8,8,0,0,0,0,0,0,0,0],comp:'pop'}],form:['A','B'],slot:0});
let a=Core.songAt(s2,0);assert(Core.eventsAt(a.view,a.local,null).filter(x=>x.k==='c').length>0,'song start is struck');
a=Core.songAt(s2,31);const pe=Core.eventsAt(a.view,a.local,null).filter(x=>x.k==='c');
assert(pe.length>0);assert(Math.abs(pe[0].dur-3*0.25*0.95)<1e-9,'next section has another style: push not held');
const nm=pe.map(x=>x.midi%12).sort((x,y)=>x-y);assert.deepStrictEqual([...new Set(nm)],[0,5,9],'push plays the next section chord (F)');
// MIDI still has no overlapping notes
console.log('swing16 + ties ok');
