const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
// tidy
let t=Core.tidy([{s:0,l:480,p:60},{s:240,l:480,p:60},{s:240,l:100,p:60},{s:0,l:100,p:62}]);
console.log(JSON.stringify(t));
assert.strictEqual(t.filter(n=>n.p===60).length,2); assert.strictEqual(t[0].l,240);
// quantize
let q=Core.quantize([{s:130,l:100,p:60},{s:470,l:230,p:62}],120,1,true,1920);
console.log(JSON.stringify(q)); assert.deepStrictEqual(q.map(n=>n.s),[120,480]);
let q0=Core.quantize([{s:130,l:100,p:60}],120,0,true,1920); assert.strictEqual(q0[0].s,130);
let q5=Core.quantize([{s:130,l:100,p:60}],120,0.5,false,1920); console.log(JSON.stringify(q5)); assert.strictEqual(q5[0].s,125);
// vel + melAt
const p=Core.normalize({mel:[{s:0,l:480,p:72},{s:240,l:240,p:74},{s:360,l:120,p:76},{s:99999999,l:1,p:60}],bars:4,melAmt:100});
assert.strictEqual(p.mel.length,3);
console.log(Core.melAt(p,0),Core.melAt(p,1),Core.melAt(p,1).length);
assert.strictEqual(Core.melVel(p,0),100); assert.strictEqual(Core.melVel(p,480),60); assert.strictEqual(Core.melVel(p,240),p.vel8[1]);
p.melAmt=0; assert.strictEqual(Core.melVel(p,0),90); p.melAmt=50; assert.strictEqual(Core.melVel(p,0),Math.round(90+(Core.posVel(p,0)-90)/2)); p.melAmt=100; assert.strictEqual(Core.melVel(p,0),Core.posVel(p,0)); assert.strictEqual(Core.normalize({}).melAmt,30); assert.strictEqual(Core.normalize({melPat:false}).melAmt,0); assert.strictEqual(Core.fresh(()=>0.3).melAmt,30);
// shrink bars
assert.strictEqual(Core.fitMel([{s:5000,l:100,p:60},{s:1800,l:500,p:60}],1920).length,1);
assert.strictEqual(Core.fitMel([{s:1800,l:500,p:60}],1920)[0].l,120);
fs.writeFileSync('t4.mid',Core.buildMidi(p));
fs.writeFileSync('t5.mid',Core.buildMidi(Core.normalize({})));
