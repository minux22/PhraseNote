/* exported MIDI: no note-on on a pitch that is still sounding (same channel), for every style, with and without swing */
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=fs.readFileSync(path.join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
function overlaps(u8){
  let i=14,res={};
  while(i<u8.length){const len=(u8[i+4]<<24|u8[i+5]<<16|u8[i+6]<<8|u8[i+7])>>>0;let j=i+8,end=j+len,t=0,run=0,on={},ov=0,name='',notes=0;
    while(j<end){let d=0,b;do{b=u8[j++];d=(d<<7)|(b&127);}while(b&128);t+=d;const st=u8[j];
      if(st===0xFF){const ty=u8[j+1];let k=j+2,l=0;do{b=u8[k++];l=(l<<7)|(b&127);}while(b&128);if(ty===3)name=String.fromCharCode(...u8.slice(k,k+l));j=k+l;continue;}
      if(st&0x80){run=st;j++;}const hi=run&0xF0;if(hi===0xC0){j++;continue;}
      const n=u8[j],v=u8[j+1];j+=2;
      if(hi===0x90&&v>0){if(on[n])ov++;on[n]=(on[n]||0)+1;notes++;}else if(hi===0x80||hi===0x90){if(on[n])on[n]--;}
    }
    res[name]={ov,notes};i=end;}
  return res;
}
let n=0;
for(const [id] of Core.COMPS)for(const sw of [0,60])for(const ts of ['4/4','3/4','6/8']){
  const p=Core.normalize({bars:4,ts:id==='waltz'?'3/4':ts,bpm:90});const M=Core.meter(p);
  p.chords=Array.from({length:4*M.bpb},(_,i)=>[0,10,6,8][Math.floor(i/M.bpb)]);
  Core.applyStyle(p,id);p.swing=sw;
  p.mel=[{s:0,l:960,p:72},{s:480,l:480,p:72},{s:1920,l:480,p:74}];
  const r=overlaps(Core.buildMidi(p,'pop16'));
  for(const k in r){assert.strictEqual(r[k].ov,0,id+' sw'+sw+' '+ts+' '+k+' overlaps '+r[k].ov);n+=r[k].notes;}
  assert(r.Chords.notes>0&&r.Melody.notes===3,id+' notes missing');
}
console.log('no overlaps, notes',n);
