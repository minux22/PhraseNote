/* song form: sections, slots, the melody following form edits, song playback and MIDI */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
// legacy project: one 4-bar loop, 10-bar melody -> A repeated 3 times
let p=Core.normalize({bars:4,chords:[0,0,0,0,8,8,8,8,10,10,10,10,6,6,6,6],comp:'pop',mel:[{s:0,l:480,p:60},{s:9*1920,l:480,p:62}]});
assert.deepStrictEqual(p.form,['A','A','A']);assert.strictEqual(p.secs.length,1);assert.strictEqual(p.comp,'pop');assert.strictEqual(Core.formTicks(p),12*1920);
// two sections with their own style and drums
p=Core.normalize({bars:4,ts:'4/4',chords:[0,0,0,0,8,8,8,8,10,10,10,10,6,6,6,6],
  secs:[{id:'A',role:'Verse',bars:4,chords:[0,0,0,0,8,8,8,8,10,10,10,10,6,6,6,6],comp:'ballad',drum:true,dpat:'half'},
        {id:'B',role:'Chorus',bars:2,chords:[6,6,6,6,8,8,8,8],comp:'pop',drum:true,dpat:'rock8'}],
  form:['A','B','A','B'],slot:0,mel:[]});
assert.strictEqual(p.secs[1].role,'Chorus');assert.strictEqual(p.bars,4);
const L=Core.layout(p);assert.deepStrictEqual(L.map(x=>[x.id,x.start/1920,x.len/1920]),[['A',0,4],['B',4,2],['A',6,4],['B',10,2]]);
let a=Core.songAt(p,4*8);assert.strictEqual(a.id,'B');assert.strictEqual(a.local,0);assert.strictEqual(a.view.comp,'pop');assert.strictEqual(Core.secDrums(a.view,null),'rock8');
a=Core.songAt(p,6*8+3);assert.strictEqual(a.id,'A');assert.strictEqual(a.local,3);assert.strictEqual(a.view,p);
assert.strictEqual(Core.songAt(p,12*8),null);assert.strictEqual(Core.songAt(p,-1),null);
// top-level edits of the current section win over the stored copy
p.comp='funk';assert.strictEqual(Core.songAt(p,0).view.comp,'funk');
const p2=Core.normalize(JSON.parse(JSON.stringify(p)));assert.strictEqual(p2.secs[0].comp,'funk');
// switching the edited section: store, move slot, load
Core.storeCur(p);p.slot=1;Core.loadCur(p);assert.strictEqual(p.comp,'pop');assert.strictEqual(p.bars,2);assert.strictEqual(p.secs[0].comp,'funk');
// melody helpers
const m=[{s:0,l:480,p:60},{s:1800,l:480,p:61},{s:3840,l:480,p:62},{s:-240,l:240,p:59}];
assert.deepStrictEqual(Core.melInsert(m,1920,1920).map(n=>[n.s,n.l]),[[0,480],[1800,120],[5760,480],[-240,240]]);
assert.deepStrictEqual(Core.melDelete(m,1920,3840).map(n=>[n.s,n.l]),[[0,480],[1800,120],[1920,480],[-240,240]]);
assert.deepStrictEqual(Core.melSlice(m,1920,4000).map(n=>[n.s,n.l]),[[1920,160]]);
// resize section B 2 -> 4 bars: notes after each B slot move by 2 bars, in place inside it
p=Core.normalize(JSON.parse(JSON.stringify(p2)));
p.mel=[{s:4*1920+10,l:100,p:70},{s:6*1920,l:100,p:71},{s:10*1920,l:100,p:72},{s:11*1920,l:100,p:73}];
let mel=Core.resizeSec(p,'B',4);assert.deepStrictEqual(mel.map(n=>n.s/1920),[4+10/1920,8,12,13]);
mel=Core.resizeSec(p,'B',1);assert.deepStrictEqual(mel.map(n=>[n.p,n.s/1920]),[[70,4+10/1920],[71,5],[72,9]]);
// MIDI follows the form, with each section's drums
const q=Core.normalize(JSON.parse(JSON.stringify(p2)));
const u8=Core.buildMidi(q,null);
function drumNotesPerBar(u8){let i=14,out={};while(i<u8.length){const len=(u8[i+4]<<24|u8[i+5]<<16|u8[i+6]<<8|u8[i+7])>>>0;let j=i+8,end=j+len,t=0,run=0;
  while(j<end){let d=0,b;do{b=u8[j++];d=(d<<7)|(b&127);}while(b&128);t+=d;const st=u8[j];if(st===0xFF){let k=j+2,l=0;do{b=u8[k++];l=(l<<7)|(b&127);}while(b&128);j=k+l;continue;}
    if(st&0x80){run=st;j++;}const hi=run&0xF0;if(hi===0xC0){j++;continue;}const n=u8[j],v=u8[j+1];j+=2;if(run===0x99&&v>0){const bar=Math.floor(t/1920);out[bar]=out[bar]||{};out[bar][n]=(out[bar][n]||0)+1;}}
  i=end;}return out;}
const dn=drumNotesPerBar(u8);
assert.strictEqual(dn[0][38],1,'half-time: one snare per bar in A');assert.strictEqual(dn[4][38],2,'rock 8th: two snares per bar in B');
assert.strictEqual(Object.keys(dn).length,12,'drums in all 12 bars only');
// 2-bar sections are allowed; caps: 32 slots / 128 bars
const big=Core.normalize({secs:[{id:'A',bars:16,chords:[]}],form:Array(20).fill('A'),chords:null});
assert.strictEqual(big.form.length,8);
console.log('song form ok');
