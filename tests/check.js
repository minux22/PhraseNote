const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const core=html.match(/<script id="core">([\s\S]*?)<\/script>/)[1];
const ui=html.match(/<script id="ui">([\s\S]*?)<\/script>/)[1];
new Function(ui); // syntax only
const Core=new Function(core+';return Core;')();
const assert=require('assert');
const lab=(code,k,s)=>{const i=Core.chordInfo(code,k,s);return i.label+'/'+i.name;};
const cmaj=[0,1,2,3,4,5,6].map(d=>lab(d*2,0,'major'));
console.log('C major  ',cmaj.join(' '));
console.log('A minor  ',[0,1,2,3,4,5,6].map(d=>lab(d*2,9,'minor')).join(' '));
console.log('A harm   ',[0,1,2,3,4,5,6].map(d=>lab(d*2,9,'harm')).join(' '));
console.log('C maj 7th',[0,1,2,3,4,5,6].map(d=>lab(d*2+1,0,'major')).join(' '));
console.log('Cm harm7 ',[0,1,2,3,4,5,6].map(d=>lab(d*2+1,0,'harm')).join(' '));
console.log('Eb major ',[0,3,4].map(d=>lab(d*2,3,'major')).join(' '));
assert.strictEqual(cmaj[0],'I/C'); assert.strictEqual(cmaj[1],'ii/Dm'); assert.strictEqual(cmaj[6],'vii°/Bdim');
assert.strictEqual(lab(8,9,'harm'),'V/E');
// voicing C
console.log('voicing C',Core.voicing(Core.chordInfo(0,0,'major'),0), 'G7',Core.voicing(Core.chordInfo(9,0,'major'),0));
const p=Core.defaults();
for(const comp of ['hold','beat','eighth']){
  p.comp=comp; let n=0,c=0,b=0;
  for(let s=0;s<p.bars*8;s++){const e=Core.eventsAt(p,s);n+=e.length;c+=e.filter(x=>x.k==='c').length;b+=e.filter(x=>x.k==='b').length;}
  console.log(comp,'events',n,'chord',c,'bass',b);
}
p.comp='beat';
const e0=Core.eventsAt(p,0), e2=Core.eventsAt(p,2), e4=Core.eventsAt(p,4);
console.log('vel beat1/2/3', e0[0].vel, e2[0].vel, e4[0].vel);
const mid=Core.buildMidi(p); fs.writeFileSync('t.mid',mid);
const z=Core.zip('sketch-C-90bpm.mid',mid); fs.writeFileSync('t.zip',z);
console.log('midi bytes',mid.length,'zip bytes',z.length,'crc',Core.crc32(mid).toString(16));
// harmonic minor key with 7th midi too
const q=Core.normalize({key:9,scale:'harm',bars:8,bpm:100,comp:'hold',sev:true,chords:[8,8,8,8,10,10,10,10,2,2,2,2,18,18,18,18]});
fs.writeFileSync('t2.mid',Core.buildMidi(q));
console.log('ok');
