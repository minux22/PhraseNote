// rhythm types: every pattern has a type, kits per type, 808/909 note maps, percussion lanes
const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const types=Core.DTYPES.map(t=>t[0]);
Core.DPATS.forEach(d=>assert(types.indexOf(d[3])>=0,d[0]));
assert(!Core.DPATS.some(d=>d[0]==='trot'),'trot removed');
types.forEach(t=>{assert(Core.DPATS.filter(d=>d[3]===t).length>=4,t);assert(Core.TKITS[t].length>=1);});
const p=Core.normalize({bars:1});
const notes=(pat,kit)=>{p.dpat=pat;p.dkit=kit;const o=[];for(let s=0;s<8;s++)Core.drumsAt(p,s,pat).forEach(e=>o.push(e.n));return o;};
// 808: kick 35 and snare 38; 909: kick 36 and snare 40
const a=notes('electro','k808'), b=notes('electro','k909');
assert(a.indexOf(35)>=0&&a.indexOf(36)<0&&a.indexOf(38)>=0,'808 '+a);
assert(b.indexOf(36)>=0&&b.indexOf(35)<0&&b.indexOf(40)>=0&&b.indexOf(38)<0,'909 '+b);
// a kit that does not belong to the type falls back to the type's first kit
assert.strictEqual(Core.kitOf({dpat:'swing',dkit:'k808'}),'jazz');
// percussion: hand percussion only
const pc=notes('tumbao','std');assert(pc.every(n=>[62,63,64,82].indexOf(n)>=0),pc);
console.log('rhythm ok');
