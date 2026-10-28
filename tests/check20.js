/* chord suggestions from a melody */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const p=Core.normalize({key:0,scale:'major',bars:4,unit:4});
const name=c=>c==null?'-':Core.chordInfo(c,0,'major').name;
// C major melody: bar1 C-E-G-E, bar2 A-C-E-C, bar3 F-A-C-A, bar4 G-B-D-B
const bars=[[60,64,67,64],[69,72,76,72],[65,69,72,69],[67,71,74,71]];
const mel=[];bars.forEach((b,i)=>b.forEach((n,j)=>mel.push({s:i*1920+j*480,l:480,p:n})));
let r=Core.suggestChords(p,Array(16).fill(null),mel,4,5);
console.log('best:',[0,4,8,12].map(i=>name(r[0][i])).join(' '),'| alts:',r.slice(1).map(x=>[0,4,8,12].map(i=>name(x[i])).join(' ')).join(' / '));
assert.deepStrictEqual([0,4,8,12].map(i=>name(r[0][i])),['C','Am','F','G']);
assert(r.length>=3,'alternatives');
assert.strictEqual(new Set(r.map(x=>x.join())).size,r.length,'all different');
// filled cells are kept
const fixed=Array(16).fill(null);for(let i=4;i<8;i++)fixed[i]=Core.xcode(4,0,1);
r=Core.suggestChords(p,fixed,mel,4,3);assert.strictEqual(name(r[0][4]),'E7');assert(r.every(x=>x[4]===fixed[4]));
// 2-beat cells
r=Core.suggestChords(p,Array(16).fill(null),mel,2,1);assert.strictEqual(r[0].length,16);
// a G# in the melody calls for E7 (secondary dominant) over Em
const m2=[{s:0,l:1920,p:60},{s:1920,l:960,p:68},{s:2880,l:960,p:71},{s:3840,l:1920,p:69},{s:5760,l:1920,p:65}];
r=Core.suggestChords(p,Array(16).fill(null),m2,4,1);
console.log('with G#:',[0,4,8,12].map(i=>name(r[0][i])).join(' '));
assert.strictEqual(name(r[0][4]),'E7');
console.log('suggest ok');
