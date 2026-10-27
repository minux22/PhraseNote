const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
let p=Core.normalize({bars:2});
for(const [pat] of Core.DPATS){
  if(pat==='custom')continue;
  const dp=Core.dpFromPreset(p,pat,16);const q=Core.normalize({bars:2,dp});
  // round trip: custom reproduces preset events (note+offset per step)
  for(let s=0;s<8;s++){
    const a=Core.drumsAt(q,s,'custom').map(e=>e.n+'@'+e.off).sort().join();
    const b=Core.drumsAt(p,s,pat).map(e=>e.n+'@'+e.off).filter(x=>true).sort().join();
    // preset notes not mapped (e.g. 51->42) are folded; compare kick/snare only
    const f=x=>x.replace(/37@/g,'38@').split(',').filter(y=>/^(36|38)@/.test(y)).join();
    assert.strictEqual(f(a),f(b),pat+' step '+s);
  }
}
const dp=Core.dpFromPreset(p,'rock8',8);const q=Core.normalize({bars:2,dp});
const mid=Core.buildMidi(q,'custom');const nodrum=Core.buildMidi(q,null);
console.log('midi with drums',mid.length,'without',nodrum.length, 'track count',mid[11],nodrum[11]);
assert(mid[11]===nodrum[11]+1);
console.log('ok');
