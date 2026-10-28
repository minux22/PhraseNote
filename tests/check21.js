/* key guess from the melody, and renaming the key without moving anything */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const mk=(notes,dur=480)=>notes.map((p,i)=>({s:i*dur,l:dur,p}));
const show=g=>g.map(x=>Core.KEY_NAMES[x.key]+' '+x.scale+' '+Math.round(x.r*100)).join(' / ');
// G major tune
let p=Core.normalize({key:0,scale:'major',mel:mk([67,71,74,71,72,71,69,67,66,67,69,71,72,74,71,67])});
let g=Core.guessKey(p);console.log('G tune:',show(g));assert.strictEqual(g[0].key,7);assert.strictEqual(g[0].scale,'major');
// A harmonic minor tune
p=Core.normalize({key:0,mel:mk([69,72,76,72,71,68,69,71,72,74,76,68,69,64,69,69])});
g=Core.guessKey(p);console.log('A minor tune:',show(g));assert.strictEqual(g[0].key,9);assert.strictEqual(g[0].scale,'harm');
// D natural minor tune
p=Core.normalize({key:0,mel:mk([62,65,69,65,67,65,64,62,60,62,64,65,69,67,65,62])});
g=Core.guessKey(p);console.log('D minor tune:',show(g));assert.strictEqual(g[0].key,2);assert.strictEqual(g[0].scale,'minor');
// no melody: nothing
assert.deepStrictEqual(Core.guessKey(Core.normalize({})),[]);
// rekey keeps the sound: C major I V vi IV -> G major IV I ii bVII
const name=(c,k,s)=>Core.chordInfo(c,k,s).name, lab=(c,k,s)=>Core.chordInfo(c,k,s).label;
p=Core.normalize({key:0,scale:'major',bars:4,chords:[0,0,0,0,8,8,8,8,10,10,10,10,6,6,6,6],mel:mk([60,62])});
const before=p.chords.map(c=>name(c,0,'major')).join(' ');
let lost=Core.rekey(p,7,'major');
assert.strictEqual(lost,0);assert.strictEqual(p.key,7);
assert.strictEqual(p.chords.map(c=>name(c,7,'major')).join(' '),before);
assert.deepStrictEqual([0,4,8,12].map(i=>lab(p.chords[i],7,'major')),['IV','I','ii','♭VII']);
assert.deepStrictEqual(p.mel.map(n=>n.p),[60,62],'melody does not move');
// sevenths, slash, minor keys, outside chords round trip
p=Core.normalize({key:0,scale:'major',bars:4,chords:[1,1,1,1,9,9,9,9,Core.xcode(4,0,1),0,0,0,3*14+0,0,0,0]});
const names=p.chords.map(c=>name(c,0,'major'));
Core.rekey(p,9,'minor');assert.deepStrictEqual(p.chords.map(c=>name(c,9,'minor')),names);
Core.rekey(p,0,'major');assert.deepStrictEqual(p.chords.map(c=>name(c,0,'major')),names);
// every section is renamed
p=Core.normalize({key:0,chords:[0,0,0,0],bars:4,secs:[{id:'A',bars:4,chords:Array(16).fill(0)},{id:'B',bars:4,chords:Array(16).fill(8)}],form:['A','B'],slot:0});
Core.rekey(p,7,'major');assert.strictEqual(name(p.secs[1].chords[0],7,'major'),'G');assert.strictEqual(name(p.chords[0],7,'major'),'C');
console.log('key guess ok');
