const fs=require('fs');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Sf2=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Sf2;')();
const buf=fs.readFileSync('/home/claude/mrbumpy409/generaluser-gs/GeneralUser-GS.sf2');
const sf=Sf2.parse(buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength));
console.log(sf.kits.map(k=>k.num+':'+k.name).join(' | '));
const pi=sf.indexOf(128,0);
for(const n of [36,37,38,39,42,44,46,49,51,53,57,59]){
  const miss=[];for(let v=1;v<=127;v++)if(!sf.find(pi,n,v).length)miss.push(v);
  console.log(n,'missing vels',miss.length,miss.slice(0,3));
}
console.log('--- reverb send (gen16) per default preset');
for(const [b,n,m] of [[0,4,60],[0,33,40],[0,73,72],[0,0,60],[0,48,60],[128,0,36],[128,0,38]]){
  const pi=sf.indexOf(b,n);if(pi<0){console.log(b,n,'none');continue;}
  const rs=sf.find(pi,m,100);console.log(b+':'+n,sf.presets[pi].name,rs.map(r=>r.g[16]));
}
console.log('--- per-key effective loudness (rms of first 0.25s * attenuation) in dB, preset 0:4 vel 80');
function eff(pi,m,v){const rs=sf.find(pi,m,v);let sum=0;for(const r of rs){const h=sf.sample(r.s);const n=Math.min(h.end-h.start,Math.floor(h.rate*0.25));let a=0;for(let i=0;i<n;i++){const x=sf.pcm[h.start+i]/32768;a+=x*x;}const rms=Math.sqrt(a/n);const att=Math.pow(10,-Math.max(0,r.g[48]||0)/200);sum+=(rms*att)**2;}return 10*Math.log10(sum+1e-12);}
for(const [b,n,name] of [[0,4,'EP'],[0,33,'Bass']]){const pi=sf.indexOf(b,n);let line=name+': ';for(let m=36;m<=84;m+=3)line+=m+':'+eff(pi,m,80).toFixed(0)+' ';console.log(line);}
console.log('--- loudness vs velocity (dB incl. play() velocity curve ^1.5), EP note 60/72, vel step');
const pi4=sf.indexOf(0,4);
for(const m of [55,64,72]){let line='m'+m+': ',prev=null;for(let v=40;v<=127;v+=1){const rs=sf.find(pi4,m,v);const key=rs.map(r=>r.s).join('+');if(key!==prev){const e=eff(pi4,m,v)+30*Math.log10(v/127);line+=' v'+v+'['+rs.length+'r]='+e.toFixed(1);prev=key;}}console.log(line);}
