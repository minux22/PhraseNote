// genres: every pattern parses in its mode, every result is valid chord codes of the right length, the genre's
// styles, patterns and basses exist, and each genre gives some variety
const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(html.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
const assert=require('assert');
const compIds=Core.COMPS.map(c=>c[0]), drumIds=Core.DPATS.map(d=>d[0]), bassIds=Core.BASSES.map(b=>b[0]);
let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647;};
const all=new Set();
Core.GENRES.forEach(G=>{
  ['M','m'].forEach(mode=>(G[mode]||[]).forEach(pat=>pat.split('|').forEach(bar=>bar.trim().split(/\s+/).forEach(t=>Core.gTok(t,mode)))));
  G.comp.forEach(id=>assert(compIds.indexOf(id)>=0,G.id+' comp '+id));
  G.drums.forEach(id=>assert(drumIds.indexOf(id)>=0,G.id+' drum '+id));
  G.bass.forEach(b=>{assert(bassIds.indexOf(b[0])>=0,G.id+' bass '+b[0]);assert(Core.BASS_BY_KIND[b[1]].indexOf(b[0])>=0,G.id+' bass kind '+b);});
  ['major','minor','harm'].forEach(sc=>[false,true].forEach(sev=>{
    const p=Core.normalize(Core.defaults());p.scale=sc;p.key=sc==='major'?0:9;p.sev=sev;
    [4,8].forEach(bars=>{p.bars=bars;const seen=new Set();let last=null;
      for(let i=0;i<20;i++){const r=Core.genreChords(p,rnd,G.id,last);last=r.sig;
        assert.strictEqual(r.chords.length,bars*4);
        r.chords.forEach(c=>{const inf=Core.chordInfo(c,p.key,p.scale);assert(inf&&inf.label&&inf.tones.every(x=>isFinite(x)),G.id+' '+c);});
        seen.add(r.names);all.add(r.names);}
      if(!G.pool)assert(seen.size>=2,G.id+' '+sc+' no variety');});
  }));
});
// a written 7th stays, a triad follows the 7th switch; slash chords keep their bass
{const p=Core.normalize(Core.defaults());p.scale='major';p.key=0;
 assert.strictEqual(Core.gCode(Core.gTok('V7','M'),'major'),9);assert.strictEqual(Core.gCode(Core.gTok('IVmaj7','M'),'major'),7);
 assert(Core.gCode(Core.gTok('I7','M'),'major')>=1000,'I7 is chromatic in major');
 const vb=Core.chordInfo(Core.gCode(Core.gTok('V/7','M'),'major'),0,'major');assert.strictEqual(((vb.bassTone%12)+12)%12,11);
 assert.strictEqual(Core.chordInfo(Core.gCode(Core.gTok('#ivo7','M'),'major'),0,'major').label.indexOf('°7')>=0,true);}
console.log('genres ok',Core.GENRES.length,'genres,',all.size,'different progressions');
