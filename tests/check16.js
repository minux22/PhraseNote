/* MIDI: program numbers follow the chosen sounds; the song title is written as UTF-8 */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const p=Core.normalize({bars:4,chords:[0,0,0,0,8,8,8,8,10,10,10,10,6,6,6,6],mel:[{s:0,l:480,p:60}],name:'봄날 스케치'});
function progs(u8){const out=[];for(let i=0;i<u8.length-2;i++){if(u8[i]===0&&(u8[i+1]&0xF0)===0xC0)out.push((u8[i+1]&15)+':'+u8[i+2]);}return out.join(' ');}
assert.strictEqual(progs(Core.buildMidi(p,null)),'0:4 1:33 2:80');
assert.strictEqual(progs(Core.buildMidi(p,null,{prog:{c:0,b:34,m:73}})),'0:0 1:34 2:73');
const u=Core.buildMidi(p,null);const name=Buffer.from('봄날 스케치','utf8');
assert(Buffer.from(u).indexOf(name)>0,'title not found');
const q=Core.normalize({bars:4,chords:[0,0,0,0]});assert(Buffer.from(Core.buildMidi(q,null)).indexOf(Buffer.from('PhraseNote'))>0);
console.log('midi programs + title ok');
