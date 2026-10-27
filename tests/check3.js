const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const ci=(c,k=0,s='major')=>Core.chordInfo(c,k,s);
// F/G : IV (deg 3) with bass degree 5  -> code 5*14+3*2
let f=ci(5*14+6); console.log('IV/5 ->',f.label,f.name,'bass midi',Core.bassNote(f,0));
assert.strictEqual(f.name,'F/G'); assert.strictEqual(Core.bassNote(f,0),43);
// C/B : I with bass degree 7
let c=ci(7*14+0); console.log('I/7 ->',c.label,c.name); assert.strictEqual(c.name,'C/B');
// slash equal to root degree is ignored
assert.strictEqual(ci(1*14+0).label,'I'); assert.strictEqual(ci(1*14+0).slash,false);
// G/B and Am/G in C; Dm7/G
console.log(ci(3*14+8).name, ci(7*14+10).name, ci(5*14+3).name, ci(5*14+3).label);
assert.strictEqual(ci(3*14+8).name,'G/E'); // IV? deg4=V with bass degree3 = E
// notes: Bass on -> chord plain, bass note slash ; Bass off -> low note added to chord
const p=Core.normalize({bass:true,chords:[5*14+6]});
let nf=Core.notesFor(p,f); console.log('bass on :',nf.c,nf.b);
p.bass=false; nf=Core.notesFor(p,f); console.log('bass off:',nf.c,nf.b);
assert.strictEqual(nf.b,null); assert.strictEqual(nf.c[0]%12,7); assert(nf.c[0]<nf.c[1]);
// all codes, all keys/scales run through events + midi without error
let n=0;
for(const scale of ['major','minor','harm'])for(let key=0;key<12;key+=5)for(let code=0;code<=111;code++){
  const q=Core.normalize({scale,key,bars:4,bass:code%2===0,comp:['hold','beat','eighth'][code%3],chords:Array(16).fill(code)});
  assert.strictEqual(q.chords[0],code);
  for(let s=0;s<32;s++)Core.eventsAt(q,s);
  const info=Core.chordInfo(code,key,scale); assert(info.label&&info.name); n++;
}
console.log('all codes ok:',n);
// midi with slash chord in bass track: lowest bass notes
const m=Core.normalize({key:0,bars:4,comp:'beat',bass:true,chords:[].concat(Array(4).fill(5*14+6),Array(4).fill(7*14+0),Array(8).fill(null))});
const bytes=Core.buildMidi(m); fs.writeFileSync('t3.mid',bytes); console.log('midi bytes',bytes.length);
