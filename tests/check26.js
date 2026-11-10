// v0.30: styles leave the bass alone, recipe differences, keys styles on guitar, bass kind separate from technique
const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(html.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const assert=require('assert');
const p=Core.normalize(Core.defaults());
p.bpat='walk';Core.applyStyle(p,'citypop');assert.strictEqual(p.bpat,'walk','style changed the bass');
assert.strictEqual(p.color,'nine');
// style only keeps the options
p.color='off';Core.applyStyle(p,'neosoul',true);assert.strictEqual(p.comp,'neosoul');assert.strictEqual(p.color,'off');
const d=Core.recipeDiff(p,'neosoul').map(x=>x[0]);assert(d.indexOf('color')>=0&&d.indexOf('bpat')<0,'diff '+d);
Core.applyStyle(p,'neosoul');assert.strictEqual(Core.recipeDiff(p,'neosoul').length,0);
// instrument: shared style keeps the choice, guitar style forces guitar, keys-only forces keys
p.inst='guitar';Core.applyStyle(p,'bossa');assert.strictEqual(Core.instP(p),'guitar');assert.strictEqual(Core.compPatch('bossa','guitar'),24);
Core.applyStyle(p,'neosoul');assert.strictEqual(Core.instP(p),'keys');
Core.applyStyle(p,'travis');assert.strictEqual(Core.instP(p),'guitar');
assert(Core.compsFor('guitar').some(c=>c[0]==='bossa')&&Core.compsFor('guitar').some(c=>c[0]==='travis')&&!Core.compsFor('guitar').some(c=>c[0]==='neosoul'));
assert(!Core.compsFor('keys').some(c=>c[0]==='travis'));
// a guitar playing Block uses the six-string shape (E-shape C: 48 55 60 64 67 72 is A-shape; at least 5 notes, lowest >= 40)
{const q=Core.normalize(Core.defaults());q.bass=false;q.chords=[0,0,0,0];q.bars=1;q.comp='hold';q.inst='guitar';
 const ev=Core.eventsAt(q,0).filter(e=>e.k==='c');assert(ev.length>=5,'guitar notes '+ev.length);assert(Math.min.apply(null,ev.map(e=>e.midi))>=40);
 assert(ev.some(e=>e.off>0),'raked');
 q.inst='keys';const ek=Core.eventsAt(q,0).filter(e=>e.k==='c');assert(ek.every(e=>!e.off),'keys not raked');}
// bass kind sets the sound; techniques shared between kinds
assert.strictEqual(Core.bassPatch('r5','acoustic'),32);assert.strictEqual(Core.bassPatch('r5','electric'),33);assert.strictEqual(Core.bassPatch('walk','electric'),33);
assert.strictEqual(Core.bassPatch('r8','electric'),34);assert.strictEqual(Core.bassPatch('sub','synth'),39);assert.strictEqual(Core.bassPatch('root','synth'),38);
assert(Core.BASS_BY_KIND.acoustic.indexOf('r5')>=0);
{const o=Core.defaults();o.bpat='r5';o.bkind='acoustic';const n=Core.normalize(o);assert.strictEqual(n.bkind,'acoustic');
 const o2=Core.defaults();o2.bpat='slap';const n2=Core.normalize(o2);assert.strictEqual(n2.bkind,'electric');
 const o3=Core.defaults();o3.bpat='slap';o3.bkind='acoustic';assert.strictEqual(Core.normalize(o3).bkind,'electric','slap is not on acoustic');}
console.log('v0.30 ok');
