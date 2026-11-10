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
// legato and inner lines: four voices sound on every beat (held notes chain across chords), inner lines keeps
// the inner voices moving with chord tones on strong beats, and stays in range
{['legato','lines','lines2'].forEach(function(st){
  const p=Core.defaults();Core.applyStyle(p,'pad');p.str=st;p.bass=false;
  const prog=[0,10,6,8,0,4,6,8];p.chords=[];prog.forEach(c=>{for(let i=0;i<4;i++)p.chords.push(c)});p.bars=8;
  const M=Core.meter(p), ev=[];
  for(let s=0;s<p.chords.length*M.sps;s++)Core.eventsAt(p,s).forEach(e=>{if(e.k==='s')ev.push({t:s*0.5+(e.off||0),m:e.midi,d:e.dur});});
  for(let b=0;b<32;b++){const t=b+0.5, n=ev.filter(e=>e.t<=t&&e.t+e.d>t).length;assert.strictEqual(n,4,st+' voices at beat '+b+': '+n);}
  ev.forEach(e=>assert(e.m>=36&&e.m<=84,st+' range '+e.m));
  const late=ev.filter(e=>e.t%4!==0);
  if(st==='lines2'){assert(late.length>=8&&ev.every(e=>e.t%2===0),'lines2 moves on half notes');}
  else if(st==='lines'){
    // the inner voices move on most beats; on beats 1 and 3 every sounding string note is a tone of the chord
    assert(late.length>=16,'too little movement '+late.length);
    for(let b=0;b<32;b+=2){const inf=Core.chordInfo(p.chords[b],0,'major'), pcs=inf.tones.slice(0,inf.sev?4:3).map(x=>x%12);
      ev.filter(e=>e.t===b).forEach(e=>assert(pcs.indexOf(e.m%12)>=0,'non-chord tone on a strong beat '+e.m+' at '+b));}
  }else assert.strictEqual(late.length,0);
});console.log('strings lines ok');}
