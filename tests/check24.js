// strings: four voices in range, held common tones in 4-part legato, every style sounds
const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const core=html.match(/<script id="core">([\s\S]*?)<\/script>/)[1];
const Core=new Function(core+';return Core;')();
const assert=require('assert');
const sv=(code,key,reg)=>Core.strVoicing(Core.chordInfo(code,key,'major'),key,reg||'mid');
for(let k=0;k<12;k++)for(let c=0;c<14;c++)['low','mid','high'].forEach(function(r){const v=sv(c,k,r);assert.strictEqual(v.length,4);assert(v[0]<v[1]&&v[1]<v[2]&&v[2]<v[3],v);assert(v[0]>=36&&v[3]<=84,r+' '+v);});
console.log('C',sv(0,0),'Am',sv(10,0),'F',sv(6,0),'G',sv(8,0));
function ev(str,chords){const p=Core.defaults();Core.applyStyle(p,'beat');p.str=str;p.chords=chords;p.bars=chords.length/4;p.bass=false;
  const o=[];for(let s=0;s<chords.length*2;s++)Core.eventsAt(p,s).forEach(e=>{if(e.k==='s')o.push(Object.assign({t:s*0.5},e));});return o;}
Core.STRS.forEach(function(x){assert(ev(x[0],[0,0,0,0,10,10,10,10]).length>0,x[0]);});
assert.strictEqual(ev('off',[0,0,0,0]).length,0);
// C -> Am share C and E: legato strikes them once and holds them over
const L=ev('legato',[0,0,0,0,10,10,10,10]);
const cStruck=L.filter(e=>e.t===0), aStruck=L.filter(e=>e.t===4);
const shared=sv(0,0).filter(m=>sv(10,0).indexOf(m)>=0);
assert(shared.length>0,'C and Am share voices');
assert.strictEqual(aStruck.length,4-shared.length);
shared.forEach(m=>{const e=cStruck.filter(x=>x.midi===m)[0];assert(e&&e.dur>7,'held '+m);});
assert.strictEqual(Core.strPatch('pizz'),45);
console.log('strings ok',L.map(e=>e.t+':'+e.midi).join(' '));
