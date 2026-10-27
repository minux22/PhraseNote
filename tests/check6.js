const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
for(const ts of ['2/4','3/4','4/4','5/4','6/8']){
  const p=Core.normalize({bars:2,ts}),M=Core.meter(p),S=M.bar/240;
  for(const [pat] of Core.DPATS){
    const kicks=[];
    for(let s=0;s<S;s++)if(Core.drumsAt(p,s,pat).some(e=>e.n===36))kicks.push(s/M.sps);
    console.log(ts,pat.padEnd(7),'kick beats',kicks.join(','));
    if(pat!=='onedrop')assert(kicks.includes(0),'downbeat');
  }
}
