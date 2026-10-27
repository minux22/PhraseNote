/* the melody follows Key, Scale and Time changes */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const m=[{s:0,l:480,p:60},{s:480,l:480,p:64},{s:960,l:480,p:67},{s:1440,l:480,p:71},{s:1920,l:240,p:66}];
// key: nearest direction
assert.deepStrictEqual(Core.shiftMelKey(m,0,2).map(n=>n.p),[62,66,69,73,68]);
assert.deepStrictEqual(Core.shiftMelKey(m,0,10).map(n=>n.p),[58,62,65,69,64]); // C->Bb goes down 2
assert.deepStrictEqual(Core.shiftMelKey(m,0,6).map(n=>n.p),[54,58,61,65,60]);  // tritone: down 6
// scale: C major -> C minor lowers 3,6,7; chromatic F# follows F
assert.deepStrictEqual(Core.mapMelScale(m,0,'major','minor').map(n=>n.p),[60,63,67,70,66]);
assert.deepStrictEqual(Core.mapMelScale(m,0,'major','harm').map(n=>n.p),[60,63,67,71,66]);
assert.deepStrictEqual(Core.mapMelScale(Core.mapMelScale(m,0,'major','minor'),0,'minor','major').map(n=>n.p),[60,64,67,71,66]);
// A minor key (9): A C E G -> A major A C# E G#
const am=[{s:0,l:480,p:69},{s:480,l:480,p:72},{s:960,l:480,p:76},{s:1440,l:480,p:79}];
assert.deepStrictEqual(Core.mapMelScale(am,9,'minor','major').map(n=>n.p),[69,73,76,80]);
// time: 4/4 -> 3/4 keeps beats 1-3 of each bar, drops beat 4
let r=Core.remapMelMeter([{s:0,l:480,p:60},{s:1440,l:480,p:62},{s:1920,l:480,p:64},{s:2400,l:240,p:65}],'4/4','3/4');
assert.strictEqual(r.dropped,1);
assert.deepStrictEqual(r.mel.map(n=>[n.s,n.p]),[[0,60],[1440,64],[1920,65]]);
// 4/4 -> 12/8: beat = dotted quarter, positions stretch by 1.5
r=Core.remapMelMeter([{s:0,l:240,p:60},{s:240,l:240,p:62},{s:1920,l:480,p:64}],'4/4','12/8');
assert.deepStrictEqual(r.mel.map(n=>[n.s,n.l]),[[0,360],[360,360],[2880,720]]);
// and back is lossless
const back=Core.remapMelMeter(r.mel,'12/8','4/4').mel;
assert.deepStrictEqual(back.map(n=>[n.s,n.l]),[[0,240],[240,240],[1920,480]]);
// pickup counted back from bar 1
r=Core.remapMelMeter([{s:-480,l:480,p:67},{s:-1920,l:240,p:60}],'4/4','3/4');
assert.strictEqual(r.dropped,1);assert.deepStrictEqual(r.mel.map(n=>n.s),[-480]);
console.log('melody follows key/scale/time ok');
