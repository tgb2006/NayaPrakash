const fs=require('fs'),path=require('path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=path.resolve(process.argv[2]||'sankshipt/output/full_book/r01'),noPdf=process.argv.includes('--no-pdf'),fromStatic=process.argv.includes('--static');
const pdfOption=process.argv.find(arg=>arg.startsWith('--pdf-output='));
const pdfOutput=pdfOption?path.resolve(pdfOption.slice('--pdf-output='.length)):path.join(out,'naya_chakshu_book.pdf');
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,timeout:120000});try{
const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>{errors.push(e.message);console.log('PAGEERROR '+e.message)});page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure().errorText));page.on('console',m=>{if(m.type()==='log')console.log(m.text())});
await page.emulateMedia({media:'print'});await page.goto('file:///'+(out+(fromStatic?'/naya_chakshu_book.html':'/book.build.html')).replaceAll('\\','/'),{waitUntil:'load',timeout:120000});
await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()))});
const result=fromStatic?JSON.parse(fs.readFileSync(out+'/pagination.json','utf8')):await page.evaluate(()=>window.bookReady);
const manifest=JSON.parse(fs.readFileSync(out+'/source-manifest.json','utf8'));
const actualPages=await page.locator('.page').evaluateAll(pages=>pages.map(
  (element,index)=>({key:element.dataset.key,type:element.dataset.type,number:index+1})
));
const fixedSections=new Map(manifest.sources.filter(
  source=>source.type==='chapter'||source.type==='khanda_intro'
).map(source=>[source.key,{type:source.type,pages:[]}]));
for(const entry of actualPages){
  if(entry.type!=='chapter'&&entry.type!=='khanda_intro')continue;
  const section=fixedSections.get(entry.key);
  if(!section||section.type!==entry.type)throw Error('Unknown fixed-length section: '+entry.key);
  section.pages.push(entry.number);
}
const invalid=[...fixedSections].filter(([,section])=>{
  const expected=section.type==='chapter'?2:4;
  return section.pages.length!==expected
    ||section.pages.some((number,index)=>number!==section.pages[0]+index)
    ||(section.type==='chapter'&&section.pages[0]%2!==0);
});
if(invalid.length)throw Error('Fixed pagination failed for '+invalid.length+' sections. First: '+invalid.slice(0,5).map(([key,section])=>key+' ('+section.pages.length+' pages)').join(', '));
fs.writeFileSync(out+'/pagination.json',JSON.stringify(result,null,2));
console.log('PAGINATED '+result.pageCount+' pages');
const audit=await page.evaluate(manifest=>{const norm=s=>s.replace(/[\s|]+/g,'').normalize('NFC'),problems=[],mismatches=[],missing=[],duplicates=[];
const allSourceNodes=[...document.querySelectorAll('[data-source-id]')],byId=new Map();for(const e of allSourceNodes){const k=e.dataset.sourceId;if(!byId.has(k))byId.set(k,[]);byId.get(k).push(e)}const ids=allSourceNodes.map(e=>e.dataset.sourceId);for(const b of manifest.blocks){const nodes=byId.get(b.id)||[];if(!nodes.length){missing.push(b.id);continue}if(nodes.length>1)duplicates.push(b.id);const el=nodes[0],clone=el.cloneNode(true);clone.querySelectorAll('.monochrome-symbol').forEach(n=>n.replaceWith(document.createTextNode(n.dataset.originalSymbol)));clone.querySelectorAll('.generic-list-marker,thead,.row-number').forEach(n=>n.remove());let actual=clone.textContent;if(norm(actual)!==norm(b.text)){mismatches.push({id:b.id,kind:b.kind,expected:b.text,actual});}}
if(missing.length)problems.push('missing_source_blocks');if(duplicates.length)problems.push('duplicate_source_blocks');if(mismatches.length)problems.push('source_text_mismatch');const expectedIds=manifest.blocks.map(b=>b.id);const sourceOrderMatches=JSON.stringify(ids)===JSON.stringify(expectedIds);if(!sourceOrderMatches)problems.push('source_order');
const pages=[...document.querySelectorAll('.page')].map((pg,i)=>{const r=pg.getBoundingClientRect(),c=pg.querySelector('.page-content'),f=pg.querySelector('.running-footer'),last=c.lastElementChild,limit=f?f.getBoundingClientRect().top-8:c.getBoundingClientRect().bottom,over=[];for(const el of pg.querySelectorAll('[data-source-id],img,.darshan-table')){const b=el.getBoundingClientRect();if(b.bottom>limit+1||b.right>r.right+1||b.left<r.left-1)over.push(el.id||el.className)}const phys=i+1,footerText=f?[...f.children].map(e=>e.textContent.trim()):null;let footerParity=true;if(f){const num=String(phys).replace(/[0-9]/g,d=>'૦૧૨૩૪૫૬૭૮૯'[d]);footerParity=phys%2===0?footerText[0]===num&&footerText[1]==='નય-ચક્ષુ | નયનું જ્ઞાન, સંશયનું સમાધાન':footerText[1]===num&&footerText[0]===pg.dataset.khandaLabel;}if(over.length)problems.push('page_overflow_'+phys);if(!footerParity)problems.push('footer_parity_'+phys);return{page:phys,key:pg.dataset.key,type:pg.dataset.type,widthPt:r.width*.75,heightPt:r.height*.75,footerParity,overflows:over,contentRatio:last?(last.getBoundingClientRect().bottom-c.getBoundingClientRect().top)/c.getBoundingClientRect().height:0,sourceBlocks:pg.querySelectorAll('[data-source-id]').length,fitTier:pg.dataset.chapterFitTier||null,paginationException:pg.dataset.paginationException||null};});
const images=[...document.images].map(i=>({key:i.dataset.imageKey,loaded:i.complete&&i.naturalWidth>0,width:i.naturalWidth,height:i.naturalHeight,placementMM:i.getBoundingClientRect().width*25.4/96,dpi:i.naturalWidth/(i.getBoundingClientRect().width/96)}));if(images.some(i=>!i.loaded))problems.push('broken_images');if(new Set(images.map(i=>i.key)).size!==images.length)problems.push('repeated_chapter_images');const tocErrors=[];for(const a of document.querySelectorAll('[data-target-key]')){const target=document.querySelector(a.getAttribute('href')),expected=target?.dataset.physicalPage,actual=a.querySelector('.toc-page').textContent.replace(/[૦-૯]/g,d=>'૦૧૨૩૪૫૬૭૮૯'.indexOf(d));if(String(expected)!==actual)tocErrors.push(a.dataset.targetKey)}if(tocErrors.length)problems.push('toc_page_numbers');const ascii=[...document.querySelectorAll('#book *')].filter(e=>e.children.length===0&&/[┌┐└┘├┤┬┴│]/.test(e.textContent)).map(e=>e.textContent.slice(0,100));if(ascii.length)problems.push('raw_ascii_charts');
return{pageCount:pages.length,expectedSourceBlocks:manifest.blocks.length,actualSourceBlocks:ids.length,missing,duplicates,mismatches,sourceOrderMatches,pages,images,tocErrors,asciiCharts:ascii,semanticCharts:document.querySelectorAll('.semantic-chart').length,semanticTables:document.querySelectorAll('.semantic-table').length,fonts:[...document.fonts].map(f=>({family:f.family,weight:f.weight,status:f.status})),problems:[...new Set(problems)]};},manifest);
audit.browserErrors=errors;fs.writeFileSync(out+'/html-audit.json',JSON.stringify(audit,null,2));console.log('AUDIT '+JSON.stringify({blocks:audit.actualSourceBlocks,missing:audit.missing.length,mismatch:audit.mismatches.length,problems:audit.problems,errors}));
if(!process.argv.includes('--skip-previews')){
  const selected=new Set([1,2,result.pageCount,...result.generated.filter(x=>x.page).map(x=>x.page),...audit.pages.filter(p=>p.overflows.length||p.contentRatio<.28||p.fitTier==='3').slice(0,20).map(p=>p.page),...Object.values(result.docStarts).filter((_,i)=>i%25===0)]);
  fs.mkdirSync(out+'/html-previews',{recursive:true});
  for(const n of selected){
    if(n<1||n>result.pageCount)continue;
    await page.locator('.page').nth(n-1).screenshot({path:out+'/html-previews/page-'+String(n).padStart(4,'0')+'.png'});
  }
}
const staticHtml=await page.evaluate(()=>{document.getElementById('book-data')?.remove();document.getElementById('build-script')?.remove();return '<!doctype html>\n'+document.documentElement.outerHTML});fs.writeFileSync(out+'/naya_chakshu_book.html',staticHtml,'utf8');
if(!noPdf){if(audit.problems.length||errors.length)throw Error('Refusing PDF until HTML audit passes.');await page.pdf({path:pdfOutput,printBackground:true,preferCSSPageSize:true,timeout:300000});console.log('PDF exported');}
console.log('DONE '+JSON.stringify({pageCount:result.pageCount,html:out+'/naya_chakshu_book.html',pdf:!noPdf}));
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
