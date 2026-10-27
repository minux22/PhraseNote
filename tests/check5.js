const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const mel=[{s:-480,l:480,p:67},{s:-240,l:240,p:69},{s:0,l:480,p:72}];
let p=Core.normalize({bars:4,pick:true,mel,melAmt:100});
assert.strictEqual(p.mel.length,3);
// first pass negative steps
assert.strictEqual(Core.melAt(p,-2).length,1); assert.strictEqual(Core.melAt(p,-1).length,1);
// wrapped at loop end: total=7680, -480+7680=7200 -> step 30 ; -240 -> 7440 step 31
assert.strictEqual(Core.melAt(p,30).length,0); assert.strictEqual(Core.melAt(p,31).length,0);
assert.strictEqual(Core.melAt(p,0).length,1);
// vel of pickup note at beat 4 of bar (t=1440) -> vel4[3]
assert.strictEqual(Core.melVel(p,-480),p.vel4[3]);
// pick off hides
p.pick=false; assert.strictEqual(Core.melAt(p,-2).length,0); assert.strictEqual(Core.melAt(p,30).length,0);
// normalize keeps negative, drops < -1920
assert.strictEqual(Core.normalize({mel:[{s:-2000,l:5,p:60},{s:-1920,l:100,p:60}]}).mel.length,1);
// midi shift
p.pick=true; p.chords=Array(16).fill(0);
fs.writeFileSync('t6.mid',Core.buildMidi(p));
p.pick=false; fs.writeFileSync('t7.mid',Core.buildMidi(p));
console.log('ok');
