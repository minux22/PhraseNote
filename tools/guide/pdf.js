const {chromium}=require('playwright');const ver=process.argv[2];
(async()=>{const b=await chromium.launch();const pg=await b.newPage();
for(const [f,o] of [['en','PhraseNote_UserGuide_EN.pdf'],['ko','PhraseNote_UserGuide_KO.pdf']]){
await pg.goto('file://'+__dirname+'/'+f+'.html');await pg.waitForTimeout(500);
await pg.pdf({path:__dirname+'/'+o,format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:8px;color:#8a929c;width:100%;padding:0 13mm;display:flex;justify-content:space-between;font-family:sans-serif"><span>PhraseNote '+ver+'</span><span class="pageNumber"></span></div>',margin:{top:'13mm',bottom:'15mm',left:'13mm',right:'13mm'}});}
await b.close();})();
