const fs=require('node:fs');
const path=require('node:path');
const {createHash}=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const out=path.resolve(process.argv[2]);
const measureOnly=process.argv.includes('--measure-only');
const htmlPath=path.join(out,'naya_chakshu_book.html');
const imageDir=path.resolve('Image/khanda-intro');
const assetMap=measureOnly?{}:Object.fromEntries(JSON.parse(fs.readFileSync(path.join(imageDir,'placements.json'),'utf8').replace(/^\uFEFF/,'')).map(asset=>[asset.key,asset]));
const tattvaDir=path.resolve('Image/khanda-tattva');
const tattvaMapPath=path.join(tattvaDir,'placements.json');
const tattvaBand=process.argv.includes('--tattva-band')||fs.existsSync(tattvaMapPath);
const tattvaMap=measureOnly||!tattvaBand?{}:Object.fromEntries(JSON.parse(fs.readFileSync(tattvaMapPath,'utf8').replace(/^\uFEFF/,'')).map(asset=>[asset.key,asset]));
const photoPreview=measureOnly&&process.argv.includes('--tattva-photo');
const css=`
.page.khanda-editorial{padding-top:13mm}
.khanda-editorial .khanda-hero{display:grid;grid-template-columns:minmax(0,1fr) var(--khanda-art,40mm);align-items:center;gap:6mm;padding-bottom:3mm;margin-bottom:3mm;border-bottom:1.2pt solid #262626}
.khanda-editorial .khanda-hero h1{margin:0;font:800 32pt/1.16 'Anek Gujarati',sans-serif}
.khanda-editorial .khanda-volume{display:block;margin-bottom:3mm;color:#555;font:700 12pt/1.25 'Anek Gujarati',sans-serif}
.khanda-editorial .khanda-art{width:100%;aspect-ratio:1;margin:0}
.khanda-editorial .khanda-art img{display:block;width:100%;height:100%;object-fit:contain}
.khanda-editorial .generic-heading:is(h2,h3){display:flex;align-items:baseline;gap:2mm;margin:2.5mm 0 2mm}
.khanda-editorial .generic-heading:is(h2,h3)::after{content:'';flex:1;min-width:4mm;align-self:center;border-top:.55pt solid #aaa}
.khanda-editorial .khanda-section-number{flex:none;color:#555;background:#eee;padding:.35mm 1.4mm;font:700 14pt/1.25 'Anek Gujarati',sans-serif}
.khanda-editorial .generic-block.generic-quote,.khanda-editorial .generic-block.generic-verse{background:none;border:0;padding:0}
.khanda-editorial .generic-block>.generic-quote{border-left:1.6pt solid #333;background:#f0f0f0;padding:2.3mm 3mm;margin-bottom:2.5mm;text-align:left}
.khanda-editorial .generic-block>.generic-verse{border:0;border-top:1pt solid #444;background:#f1f1f1;padding:2.5mm 3mm}
.khanda-editorial .generic-prose{line-height:1.47;margin-bottom:3mm}
.khanda-editorial .chart-root{background:#242424;color:#fff;border-color:#242424}
.khanda-editorial .generic-list-item .generic-list-marker{color:#4e4e4e}
`;
const definitionCss=`
.khanda-editorial .generic-block>.khanda-definition{padding:3mm 3.5mm;background:#f1f1f1}
.khanda-definition-label{font:700 12pt/1.25 'Anek Gujarati',sans-serif;margin-bottom:1.5mm}
.khanda-definition .generic-inline-code{display:block;padding:0;background:none}
.khanda-sutra-line{display:block;font:400 11pt/1.4 'Noto Sans Devanagari',sans-serif}
.khanda-definition-citation{font-size:9pt;line-height:1.35;color:#555;margin-top:1.5mm}
.khanda-definition-details{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.8fr);gap:4mm;border-top:.55pt solid #aaa;margin-top:2.2mm;padding-top:2mm;font-size:9.5pt;line-height:1.42}
.khanda-definition-details>div+div{border-left:.55pt solid #bbb;padding-left:3mm}
.khanda-definition-field-label{font:700 10.5pt/1.25 'Anek Gujarati',sans-serif;margin-bottom:.7mm}
`;
const tattvaCss=`
.khanda-editorial .khanda-tattva-art{display:flex;align-items:center;justify-content:center;height:var(--tattva-height);margin:4mm 0 0}
.khanda-editorial .khanda-tattva-art img{display:block;max-width:min(100%,var(--tattva-width));max-height:100%;width:auto;height:auto;object-fit:contain}
.khanda-editorial[data-khanda-density="compact"] .generic-prose{line-height:1.4;margin-bottom:2.4mm}
.khanda-editorial[data-khanda-density="dense"] .generic-prose{line-height:1.38;margin-bottom:2.2mm}
.khanda-editorial[data-khanda-density="dense"] :is(.generic-list-item,.generic-list-copy){line-height:1.34}
`;
const tattvaPhotoCss=`
.khanda-editorial .khanda-tattva-photo img{width:var(--photo-width,100%);height:var(--photo-height,100%);max-width:none;max-height:none;object-fit:cover}
`;
const chartNoteCss=`
.khanda-editorial .khanda-chart-note .generic-prose{font-size:10pt;line-height:1.32;margin-bottom:1mm;color:#4b4b4b}
`;

async function main(){
  const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1100}});
    await page.emulateMedia({media:'print'});
    await page.goto(pathToFileURL(htmlPath).href);
    const existing=await page.locator('.khanda-editorial').count()===28;
    const copyAssets=(directory,assets)=>{
      for(const asset of Object.values(assets)){
        if(path.basename(asset.file)!==asset.file)throw Error('Invalid asset filename.');
        const input=path.join(directory,asset.file),destination=path.join(out,'assets/images',asset.file);
        const digest=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
        if(digest(input)!==asset.sha256)throw Error('Art hash mismatch for '+asset.key);
        if(!fs.existsSync(destination))fs.copyFileSync(input,destination,fs.constants.COPYFILE_EXCL);
        if(digest(destination)!==asset.sha256)throw Error('Unexpected existing art for '+asset.key);
      }
    };
    if(!measureOnly&&!existing)copyAssets(imageDir,assetMap);
    if(!measureOnly&&tattvaBand)copyAssets(tattvaDir,tattvaMap);
    if(!existing)await page.addStyleTag({content:css});
    if(!await page.locator('.khanda-definition').count())await page.addStyleTag({content:definitionCss});
    if(tattvaBand&&!await page.locator('.khanda-tattva-art').count())await page.addStyleTag({content:tattvaCss});
    if((photoPreview||Object.values(tattvaMap).some(asset=>asset.style==='grayscale-photo'))&&!await page.locator('.khanda-tattva-photo').count()){
      await page.addStyleTag({content:tattvaPhotoCss});
    }
    if(!await page.locator('.khanda-chart-note').count())await page.addStyleTag({content:chartNoteCss});
    const report=await page.evaluate(async({assetMap,tattvaMap,tattvaBand,measureOnly,existing,photoPreview})=>{
      await document.fonts.ready;
      function formatDefinition(block){
        const box=block.querySelector(':scope > .generic-quote');
        if(!box||box.classList.contains('khanda-definition'))return;
        const original=box.textContent,parts=[[]];
        for(const child of box.childNodes){
          if(child.nodeName==='BR')parts.push([]);
          else parts.at(-1).push(child);
        }
        const code=box.querySelector(':scope > .generic-inline-code');
        if(!code||parts.length!==3)throw Error('Unexpected definition structure: '+block.id);
        const wrap=(className,nodes=[])=>{
          const element=document.createElement('div');
          element.className=className;
          element.append(...nodes);
          return element;
        };
        const start=parts[0].indexOf(code);
        const sentences=code.textContent.split(/(?<=।)(?=\s+\S)/u);
        code.replaceChildren(...sentences.map(sentence=>{
          const line=document.createElement('span');
          line.className='khanda-sutra-line';
          line.lang='sa';
          line.textContent=sentence;
          return line;
        }));
        const fields=parts.slice(1).map(([label,value,...rest])=>{
          if(label.nodeName!=='STRONG'||value.nodeType!==Node.TEXT_NODE||!value.data.startsWith(': '))throw Error('Unexpected field: '+block.id);
          const text=value.splitText(2);
          return wrap('khanda-definition-field',[wrap('khanda-definition-field-label',[label,value]),text,...rest]);
        });
        const heading=wrap('khanda-definition-label',parts[0].slice(0,start));
        const citation=wrap('khanda-definition-citation',parts[0].slice(start+1));
        box.replaceChildren(heading,code,citation,wrap('khanda-definition-details',fields));
        box.classList.add('khanda-definition');
        if(box.textContent!==original)throw Error('Definition wording changed: '+block.id);
      }
      const mm=px=>px*25.4/96;
      const measurements=[];
      const pages=[...document.querySelectorAll('.page[data-type="khanda_intro"]')];
      const groups=Map.groupBy(pages,p=>p.dataset.key);
      if(groups.size!==7)throw Error('Expected seven khanda introductions.');
      for(const [key,group] of groups){
        if(group.length!==4)throw Error(key+' must have four pages.');
        const asset=assetMap[key];
        if(!measureOnly&&(!asset||asset.page!==+group[0].dataset.physicalPage))throw Error('Missing or mismatched art for '+key);
        const containers=group.map(p=>p.querySelector('.page-content'));
        const blocks=containers.flatMap(c=>[...c.children]).filter(block=>!block.matches('.khanda-tattva-art'));
        let hero=blocks[0],units=blocks;
        if(!existing){
        const titleBlock=blocks[0],title=titleBlock.querySelector('h1');
        const split=title?.textContent.match(/^([^:]+:)(\s*)(.+)$/);
        if(!split)throw Error('Unexpected khanda title '+key);
        const volume=document.createElement('span');volume.className='khanda-volume';volume.textContent=split[1];
        title.replaceChildren(volume,split[2]+split[3]);
        hero=document.createElement('div');hero.className='khanda-hero';
        const figure=document.createElement('figure');figure.className='khanda-art';
        if(asset){
          const image=document.createElement('img');
          image.src='assets/images/'+asset.file;image.alt=asset.concept;
          image.width=asset.pixels;image.height=asset.pixels;
          image.dataset.imageKey=key+'-intro';
          figure.append(image);
        }
        hero.append(titleBlock,figure);
        units=[hero,...blocks.slice(1)];
        for(const block of blocks){
          const h=block.querySelector('h2.generic-heading');
          const parts=h?.textContent.match(/^([૦-૯]+\.)(\s+)(.+)$/);
          if(!parts)continue;
          const number=document.createElement('span');number.className='khanda-section-number';number.textContent=parts[1];
          const heading=document.createElement('span');heading.textContent=parts[2]+parts[3];
          h.replaceChildren(number,heading);
        }
        group.forEach(p=>p.classList.add('khanda-editorial'));
        }
        if(!hero.matches('.khanda-hero'))throw Error('Missing khanda hero '+key);
        formatDefinition(units[1]);
        const chapterNote=units.find(unit=>unit.matches('[data-kind="prose"]')&&unit.textContent.includes('પેટાક્રમ ૨૬–૪૨માં'));
        chapterNote?.classList.add('khanda-chart-note');
        containers.forEach(c=>c.replaceChildren());
        containers[0].append(...units);
        const image=hero.querySelector('img');
        if(image)await image.decode();
        const limits=group.map((p,i)=>p.querySelector('.running-footer').getBoundingClientRect().top-containers[i].getBoundingClientRect().top-9);
        const keepsNext=unit=>{
          if(unit.matches('[data-kind="heading"]'))return true;
          const copy=unit.querySelector('.generic-list-copy');
          const label=copy?.firstElementChild;
          return label?.matches('strong')&&copy.textContent.trim()===label.textContent.trim()+':';
        };
        const allowedCut=cut=>cut>=4&&cut<units.length&&!keepsNext(units[cut-1]);
        const branch=units.findIndex(unit=>unit.querySelector('h2')?.textContent.includes('શાખા-પ્રસાર'));
        const chart=units.findIndex(unit=>unit.matches('[data-kind="chart"]'));
        if(tattvaBand&&(branch<0||chart<=branch))throw Error('Missing branch section for '+key);
        const artReserve=tattvaBand?29*96/25.4:0;
        let chosen;
        for(const density of (tattvaBand?['normal','compact','dense']:['normal'])){
        group.forEach(p=>p.dataset.khandaDensity=density);
        for(const size of [46,42,38]){
          hero.style.setProperty('--khanda-art',size+'mm');
          const start=containers[0].getBoundingClientRect().top;
          const offsets=[...units.map(n=>n.getBoundingClientRect().top-start),units.at(-1).getBoundingClientRect().bottom-start];
          for(let a=4;a<units.length-2;a++){
            if(!allowedCut(a))continue;
            for(let b=a+1;b<units.length-1;b++){
              if(!allowedCut(b)||(tattvaBand&&b!==branch))continue;
              for(let c=b+1;c<units.length;c++){
                if(!allowedCut(c)||(tattvaBand&&c<=chart))continue;
                const cuts=[0,a,b,c,units.length];
                const heights=limits.map((_,i)=>offsets[cuts[i+1]]-offsets[cuts[i]]);
                if(heights.some((height,i)=>height+(i===1?artReserve:0)>limits[i]))continue;
                const fill=heights.map((height,i)=>(height+(i===1?artReserve:0))/limits[i]);
                const sparse=fill.reduce((sum,ratio)=>sum+Math.max(0,.72-ratio)**2,0);
                const leadingSpace=(1-fill[0])*4+(1-fill[1])*2+(1-fill[2]);
                const sectionBreaks=[a,b,c].filter(cut=>units[cut].matches('[data-kind="heading"]')).length;
                const score=leadingSpace+100*sparse-.012*sectionBreaks;
                const preferredFirstPage=tattvaBand&&chosen&&a>chosen.cuts[1];
                const sameFirstPage=!tattvaBand||!chosen||a===chosen.cuts[1];
                if(!chosen||preferredFirstPage||(sameFirstPage&&score<chosen.score)){
                  chosen={cuts,score,size,density};
                }
              }
            }
          }
          if(chosen)break;
        }
        if(chosen)break;
        }
        if(!chosen)throw Error('Layout cannot fit four pages for '+key);
        containers.forEach((container,i)=>container.replaceChildren(...units.slice(chosen.cuts[i],chosen.cuts[i+1])));
        let tattvaHeightMm=null;
        if(tattvaBand){
          const asset=tattvaMap[key],secondPage=group[1];
          if(!measureOnly&&(!asset||asset.page!==+secondPage.dataset.physicalPage))throw Error('Missing tattva art for '+key);
          const photo=photoPreview||asset?.style==='grayscale-photo';
          const limit=secondPage.querySelector('.running-footer').getBoundingClientRect().top-9;
          const available=mm(limit-containers[1].lastElementChild.getBoundingClientRect().bottom);
          tattvaHeightMm=photo?Math.floor(available-5):Math.min(64,Math.floor(available-4));
          if(tattvaHeightMm<24)throw Error('Tattva image has insufficient space for '+key);
          const band=document.createElement('figure');band.className='khanda-tattva-art';
          if(photo)band.classList.add('khanda-tattva-photo');
          band.style.setProperty('--tattva-height',tattvaHeightMm+'mm');
          if(asset){
            const art=document.createElement('img');
            band.style.setProperty('--tattva-width',Math.min(135,asset.width*25.4/300)+'mm');
            art.src='assets/images/'+asset.file;art.alt=asset.concept;
            art.width=asset.width;art.height=asset.height;art.dataset.imageKey=key+'-tattva';
            band.append(art);
          }
          containers[1].append(band);
          if(asset){
            const art=band.firstElementChild;
            if(photo){
              const frameWidth=mm(band.getBoundingClientRect().width);
              const printScale=Math.min(1,asset.width*25.4/(301*frameWidth),asset.height*25.4/(301*tattvaHeightMm));
              band.style.setProperty('--photo-width',frameWidth*printScale+'mm');
              band.style.setProperty('--photo-height',tattvaHeightMm*printScale+'mm');
            }
            await art.decode();
            if(photo){
              const rect=art.getBoundingClientRect();
              const dpi=Math.min(art.naturalWidth*96/rect.width,art.naturalHeight*96/rect.height);
              if(dpi<300)throw Error('Photo crop below 300 DPI for '+key);
            }
          }
        }
        const fill=group.map((p,i)=>{
          const top=containers[i].getBoundingClientRect().top;
          const bottom=containers[i].lastElementChild.getBoundingClientRect().bottom;
          const gap=mm(p.querySelector('.running-footer').getBoundingClientRect().top-bottom);
          if(gap<2.1||p.scrollWidth>p.clientWidth+2)throw Error('Khanda page does not fit: '+p.dataset.physicalPage);
          return {page:+p.dataset.physicalPage,footerGapMm:Math.round(gap*100)/100,fill:Math.round(100*(bottom-top)/limits[i]),first:containers[i].querySelector('[data-source-id]').dataset.sourceId,last:[...containers[i].querySelectorAll('[data-source-id]')].at(-1).dataset.sourceId};
        });
        measurements.push({key,sizeMm:chosen.size,density:chosen.density,tattvaHeightMm,pages:fill});
      }
      return measurements;
    },{assetMap,tattvaMap,tattvaBand,measureOnly,existing,photoPreview});
    console.log(JSON.stringify(report));
    if(measureOnly)return;
    const paginationPath=path.join(out,'pagination.json');
    const pagination=JSON.parse(fs.readFileSync(paginationPath,'utf8'));
    pagination.pageMap=await page.evaluate(()=>[...document.querySelectorAll('.page')].map(p=>({physicalPage:+p.dataset.physicalPage,type:p.dataset.type,key:p.dataset.key,khanda:p.dataset.khandaLabel,sourceIds:[...p.querySelectorAll('[data-source-id]')].map(e=>e.dataset.sourceId)})));
    fs.writeFileSync(htmlPath,'<!doctype html>\n'+await page.evaluate(()=>document.documentElement.outerHTML),'utf8');
    fs.writeFileSync(paginationPath,JSON.stringify(pagination,null,2),'utf8');
    fs.writeFileSync(path.join(out,'khanda-intro-layout-audit.json'),JSON.stringify(report,null,2),'utf8');
  }finally{await browser.close();}
}

main().catch(error=>{console.error(error);process.exitCode=1;});
