// guitar styles: six-string shapes, strum directions, style -> patch
const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const core=html.match(/<script id="core">([\s\S]*?)<\/script>/)[1];
const Core=new Function(core+';return Core;')();
const assert=require('assert');
const gv=(code,key)=>Core.gtrVoicing(Core.chordInfo(code,key,'major'),key);
// C (root C3=48 -> A shape, five strings): C3 G3 C4 E4 G4
assert.deepStrictEqual(gv(0,0),[48,55,60,64,67]);
// G (root G2=43 -> E shape, six strings): G2 D3 G3 B3 D4 G4
assert.deepStrictEqual(gv(8,0),[43,50,55,59,62,67]);
// G7: F replaces the octave on the third string
assert.deepStrictEqual(gv(9,0),[43,50,53,59,62,67]);
// Am (A shape): A2 E3 A3 C4 E4
assert.deepStrictEqual(gv(10,0),[45,52,57,60,64]);
// every shape stays on a guitar (E2..about E5)
for(let k=0;k<12;k++)for(let c=0;c<14;c++){const v=gv(c,k);assert(v[0]>=40&&v[v.length-1]<=76,k+' '+c+' '+v);}
// strum16: down strokes go low->high, up strokes high->low on the top four strings
const p=Core.defaults();Core.applyStyle(p,'strum16');p.chords=[0,0,0,0];p.bars=1;p.bass=false;
const ev=[];for(let s=0;s<8;s++)Core.eventsAt(p,s).forEach(e=>ev.push(Object.assign({st:s},e)));
const at=(st,off)=>ev.filter(e=>e.k==='c'&&e.st===st&&Math.abs(e.off-off)<0.06).sort((a,b)=>a.off-b.off).map(e=>e.midi);
assert.deepStrictEqual(at(0,0.05),[48,55,60,64,67]);                 // beat 1: down
assert.deepStrictEqual(at(1,0.30),[67,64,60,55]);                    // the 'a' of 1: up, top four
assert.strictEqual(Core.instOf('strum16'),'guitar');assert.strictEqual(Core.instOf('beat'),'keys');
assert.strictEqual(Core.compPatch('strum16'),25);assert.strictEqual(Core.compPatch('chug'),29);assert.strictEqual(Core.compPatch('beat'),0);
console.log('guitar ok');
// MIDI: Chords on Auto writes each slot's program (piano for Beat, steel guitar for Strum 8th)
const q=Core.defaults();q.chords=[0,0,0,0,0,0,0,0];q.bars=4;Core.applyStyle(q,'beat');
const n=Core.normalize?Core.normalize(q):q;
if(n.secs&&n.secs.length){const B=JSON.parse(JSON.stringify(n.secs[0]));B.id='B';B.comp='strum8';n.secs.push(B);n.form=[n.form[0],'B'];}
const mid=Core.buildMidi(n,null,{cauto:true});const bytes=Array.from(mid instanceof Uint8Array?mid:new Uint8Array(mid));
const pcs=[];for(let i=0;i<bytes.length-1;i++)if(bytes[i]===0xC0)pcs.push(bytes[i+1]);
assert(pcs.indexOf(0)>=0&&pcs.indexOf(25)>=0,'program changes '+pcs);
console.log('midi programs',pcs);
