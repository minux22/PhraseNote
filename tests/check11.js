const fs=require('fs');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const p=Core.normalize({bars:2});
for(const pat of ['rock8','pop16','half','four','ballad']){
  const m=Core.buildMidi(p,pat);const u=m instanceof Uint8Array?m:new Uint8Array(m);
  const by={};for(let i=0;i<u.length-2;i++)if(u[i]===0x99&&u[i+1]<128&&u[i+2]>0&&u[i+2]<128){by[u[i+1]]=by[u[i+1]]||new Set();by[u[i+1]].add(u[i+2]);}
  console.log(pat,Object.entries(by).map(([n,s])=>n+':'+[...s].join('/')).join('  '));
}
