/* chords outside the scale: codes survive save/load, play in every style and voicing, export to MIDI */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const pcs=(key,i)=>i.tones.map(t=>(key+t)%12);
// spot checks (C major)
const E7=Core.chordInfo(Core.xcode(4,0,1),0,'major');assert.strictEqual(E7.label,'III7');assert.strictEqual(E7.name,'E7');assert.deepStrictEqual(pcs(0,E7),[4,8,11,2]);
const Ab=Core.chordInfo(Core.xcode(8,3,0),0,'major');assert.strictEqual(Ab.name,'A♭');assert.strictEqual(Ab.label,'♭VI');
const Fm7=Core.chordInfo(Core.xcode(5,1,1),0,'major');assert.strictEqual(Fm7.label,'iv7');assert.deepStrictEqual(pcs(0,Fm7),[5,8,0,3]);
const Dh=Core.chordInfo(Core.xcode(2,2,1),0,'major');assert.strictEqual(Dh.label,'iiø7');assert.strictEqual(Dh.name,'Dm7♭5');
const Gs=Core.chordInfo(Core.xcode(11,4,1),9,'minor');assert.strictEqual(Gs.label,'vii°7');assert.strictEqual(Gs.name,'G♯dim7');assert.deepStrictEqual(pcs(9,Gs),[8,11,2,5]);
// slash: E7 over G# is III7/... (bass degree 3 = E is the root: no slash); A♭ over C (degree 1)
const AbC=Core.chordInfo(Core.xcode(8,3,0,1),0,'major');assert.strictEqual(AbC.name,'A♭/C');assert.strictEqual(AbC.label,'♭VI/1');
// xWith: fixed sevenths stay 7th, others follow the switch
assert.strictEqual(Core.chordInfo(Core.xWith(Core.xcode(4,0,1),false,0),0,'major').label,'III7');
assert.strictEqual(Core.chordInfo(Core.xWith(Core.xcode(8,3,0),true,0),0,'major').label,'♭VImaj7');
// normalize keeps them, rejects junk
const codes=[];Core.extraPalette('major').concat(Core.extraPalette('minor')).forEach(([g,l])=>l.forEach(([r,q,f])=>{for(const sev of [0,1])for(const bd of [0,1,3])codes.push(Core.xWith(Core.xcode(r,q,f),sev,bd));}));
const ch=[];for(let i=0;i<16*4;i++)ch.push(codes[i%codes.length]);
let p=Core.normalize({bars:16,chords:ch.concat([]).map((c,i)=>i===5?2600:i===6?1125:c)});
assert.strictEqual(p.chords[5],null);assert.strictEqual(p.chords[6],null);
p.chords=ch.slice();p=Core.normalize(JSON.parse(JSON.stringify(p)));assert.deepStrictEqual(p.chords,ch);
// every style / voicing / color plays sane notes
let n=0;
for(const [st] of Core.COMPS)for(const voic of ['close','open','spread'])for(const color of ['off','add9','sus','69','nine'])for(const scale of ['major','minor','harm']){
  const q=Core.normalize({bars:16,ts:st==='waltz'?'3/4':'4/4',chords:ch,voic,color,inv:true,scale,key:5,bpat:'r5'});
  if(st==='waltz')q.chords=ch.slice(0,48);
  Core.applyStyle(q,st);q.voic=voic;q.color=color;
  for(let s=0;s<16;s++)for(const e of Core.eventsAt(q,s,'rock8')){assert(e.midi>=20&&e.midi<=100,st+' '+e.midi);n++;}
}
const m=Core.buildMidi(Core.normalize({bars:16,chords:ch}),'pop16');assert(m.length>1000);
console.log('outside chords ok, events',n);
