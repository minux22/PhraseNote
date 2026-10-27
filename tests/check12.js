const fs=require('fs');
const h=fs.readFileSync(require('path').join(__dirname,'../src/chord-sketch.html'),'utf8');
const Core=new Function(h.match(/<script id="core">([\s\S]*?)<\/script>/)[1]+';return Core;')();
console.log(Core.fileStem(Core.normalize({key:0,scale:'minor',bpm:120})),Core.fileStem(Core.normalize({key:6,scale:'major',bpm:88})),Core.fileStem(Core.normalize({key:9,scale:'harm',bpm:100})));
