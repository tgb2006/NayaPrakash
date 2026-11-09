const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const out=path.resolve(process.argv[2]);
const file=path.join(out,'naya_chakshu_book.html');
const keys=['D002','D003','D004','D005','D006','D007'];
const chapterOption=process.argv.find(arg=>arg.startsWith('--chapter='));
const selectedKeys=chapterOption ? keys.filter(key=>key===chapterOption.split('=')[1]) : keys;
const pageStarts={
  D005:['નયના વિવિધ પ્રકારો અને તેમના અવાંતર/અપર નામો'],
  D007:[
    'આગમ-આધાર અને શાબ્દિક વ્યુત્પત્તિ','વિવેક-વિચાર (વ્યવહાર અને સાવધાની)','વિભાગ ૨: અર્થ નયનું વિશ્લેષણ',
    '૨.૩ શાખા-પ્રસાર','૨.૫ સાધના-સાક્ષાત્કાર','૩.૨ તત્ત્વ-વિસ્તાર'
  ]
};
const artwork={
  'D003-sparse':{name:'multiple-facets-quartz.png',alt:'એક જ સ્ફટિકની જુદી જુદી સપાટીઓ'},
  'D005-page-1':{index:0,name:'banyan-and-reflection.png',alt:'પાણીની ધાર પર વડ અને તેનું પ્રતિબિંબ'},
  'D005-sparse':{name:'common-trunk-branches.png',alt:'એક થડમાંથી વિસ્તરતી જુદી શાખાઓ'},
  'D007-page-3':{index:2,name:'seed-and-sprout.png',alt:'બીજમાંથી પ્રગટતો નાનો અંકુર'},
  'D007-page-5':{
    index:4,name:'artha-naya-application-and-caution.png',ratio:4/3,
    alt:'યોજના પાસે વાસ્તવિક અનાજ અને બહારની ચમક સામે દીવાની સ્થિર જ્યોત'
  }
};
const css=`
.general-editorial .generic-heading{overflow-wrap:normal}
.general-editorial .general-opener{border-bottom:1.1pt solid #292929;padding-bottom:3mm;margin-bottom:3mm}
.general-editorial .general-opener h1{margin:0}
.general-editorial .general-chapter-number{display:block;font:700 12pt/1.25 'Anek Gujarati',sans-serif;color:#555;margin-bottom:1.3mm}
.general-editorial .general-opener-summary h3.generic-heading{color:#555;font-weight:600;border-left:0;padding-left:0;margin-top:0}
.general-editorial .heading-summary{margin-top:1.8mm}
.general-editorial .general-division h1{font-size:20pt;padding:2mm 3mm;background:#ececec;border-left:1.3pt solid #444}
.general-editorial :is(.generic-heading:is(h2,h3,h4,h5,h6)){margin:2.2mm 0 1.6mm}
.general-editorial h2.generic-heading{font-size:16pt;border-bottom:.55pt solid #aaa;padding-bottom:1mm}
.general-editorial h3.generic-heading{font-size:13pt;border-left:1pt solid #aaa;padding-left:2mm}
.general-editorial :is(h4,h5,h6).generic-heading{font-size:11.5pt;color:#424242;margin-left:3mm}
.general-editorial .general-heading-number{display:inline-block;min-width:5mm;margin-right:1.2mm;padding:.25mm 1mm;background:#e9e9e9;color:#444;font-size:.84em;white-space:nowrap}
.general-editorial .generic-list-marker{color:#4a4a4a;font-weight:800}
.general-editorial .generic-list-marker.general-bullet{font-size:0}
.general-editorial .generic-bullet::before{content:'';display:inline-block;width:1.35mm;height:1.35mm;background:#555;transform:rotate(45deg);vertical-align:middle;margin-top:1.7mm}
.general-editorial .semantic-table{font-size:10.5pt;line-height:1.38}
.general-editorial .semantic-table :is(th,td){padding:1.5mm 1.4mm;overflow-wrap:normal}
.general-editorial .semantic-table th{background:#303030;color:white;font-size:10pt;border-color:#686868}
.general-editorial .semantic-table tbody tr:nth-child(even) td{background:#f0f0f0}
.general-editorial .semantic-table td:first-child{color:#444;text-align:center}
`;

async function main(){
  if(!selectedKeys.length)throw Error('Unknown general chapter: '+chapterOption);
  const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1100}});
    await page.emulateMedia({media:'print'});
    await page.goto(pathToFileURL(file).href);
    const alreadyStyled=await page.locator('.general-editorial').count()>0;
    if(!alreadyStyled)await page.addStyleTag({content:css});
    const placements={};
    for(const [slot,art] of Object.entries(artwork)){
      const original=path.resolve(__dirname,'../../Image/general-chapters',art.name);
      if(!fs.existsSync(original)||process.argv.includes('--measure-only'))continue;
      const relative='assets/general-chapters/'+art.name;
      fs.mkdirSync(path.dirname(path.join(out,relative)),{recursive:true});
      fs.copyFileSync(original,path.join(out,relative));
      placements[slot]={...art,relative};
    }
    const report=await page.evaluate(async ({keys,placements,pageStarts})=>{
      await document.fonts.ready;
      const changes=[];
      function styleHeading(block,first){
        const heading=block.querySelector('.generic-heading');
        if(!heading)return;
        if(first)block.classList.add('general-opener');
        else if(heading.tagName==='H1')block.classList.add('general-division');
        const text=heading.firstChild;
        if(text?.nodeType!==Node.TEXT_NODE)return;
        const pattern=first?/^(પ્રકરણ\s+[૦-૯]+:)\s*/:/^((?:વિભાગ\s+[૦-૯]+:|[૦-૯]+(?:\.[૦-૯]+)*\.?|\([૦-૯ક-હ]+\)))\s+/;
        const m=text.data.match(pattern);
        if(!m)return;
        const badge=document.createElement('span');
        badge.className=first?'general-chapter-number':'general-heading-number';
        badge.textContent=m[1];
        const original=text.data;
        text.data=original.slice(m[1].length);
        heading.insertBefore(badge,text);
      }
      function styleTable(table){
        const headers=[...table.querySelectorAll('thead th')].map(th=>th.textContent.trim());
        if(headers.length!==6||headers[0]!=='નય ક્રમાંક'||headers.at(-1)!=='કેન્દ્રીય લક્ષણ')throw Error('Unmapped general-chapter table');
        const columns=document.createElement('colgroup');
        for(const width of [9,17,17,13,14,30]){
          const col=document.createElement('col');col.style.width=width+'%';columns.append(col);
        }
        table.prepend(columns);
      }
      for(const key of keys){
        const pages=[...document.querySelectorAll('.page[data-key="'+key+'"]')];
        if(!pages.length)throw Error('No pages for '+key);
        pages.forEach(p=>p.classList.add('general-editorial'));
        const containers=pages.map(p=>p.querySelector('.page-content'));
        containers.forEach(c=>c.querySelector('.general-metaphor')?.remove());
        const original=containers.map(c=>[...c.children]);
        const units=original.flat();
        const requiredCuts=(pageStarts[key]||[]).map(title=>{
          const index=units.findIndex(unit=>unit.querySelector('.generic-heading')?.textContent.includes(title));
          if(index<0)throw Error('Page-start heading not found: '+title);
          return index;
        });
        const needsStyling=!units[0].classList.contains('general-opener');
        if(needsStyling)units.forEach((unit,i)=>styleHeading(unit,i===0));
        if(needsStyling&&key==='D002'){

          const title=units[0].querySelector('h1');
          const text=title.firstChild;
          const parts=text?.nodeType===Node.TEXT_NODE&&text.data.match(/^([^:]+:)(\s*)(.+)$/);
          if(parts){
            const subtitle=document.createElement('span');subtitle.className='heading-summary';subtitle.textContent=parts[3];
            text.data=parts[1]+parts[2];title.append(subtitle);
          }
          if(units[1]?.querySelector('h3')?.textContent.startsWith('('))units[1].classList.add('general-opener-summary');
        }
        if(needsStyling)for(const table of pages.flatMap(p=>[...p.querySelectorAll('table.semantic-table')]))styleTable(table);
        for(const p of pages)for(const marker of p.querySelectorAll('.generic-list-marker')){
          if(marker.textContent.trim()==='•')marker.classList.add('general-bullet');
        }
        const limits=pages.map((p,i)=>{
          const footer=p.querySelector('.running-footer');
          return (footer?footer.getBoundingClientRect().top-9:containers[i].getBoundingClientRect().bottom)-containers[i].getBoundingClientRect().top;
        });
        containers.forEach(c=>c.replaceChildren());
        containers[0].append(...units);
        const top=containers[0].getBoundingClientRect().top;
        const offsets=[...units.map(x=>x.getBoundingClientRect().top-top),units.at(-1).getBoundingClientRect().bottom-top];
        const target=Math.min(.95,offsets.at(-1)/limits.reduce((a,b)=>a+b,0));
        const headingLevel=unit=>{
          const heading=unit?.querySelector('.generic-heading');
          return heading ? Number(heading.tagName.slice(1)) : 0;
        };
        const blocksBreakAfter=index=>{
          const unit=units[index];
          if(headingLevel(unit))return true;
          const copy=unit.querySelector('.generic-list-copy'),label=copy?.firstElementChild;
          return label?.matches('strong')&&copy.textContent.trim()===label.textContent.trim()+':';
        };
        const minimumOpening=50;
        const protectedCuts=new Set();
        for(let index=0;index<units.length-1;index++){
          if(blocksBreakAfter(index))protectedCuts.add(index+1);
          const level=headingLevel(units[index]);
          if(!level)continue;
          let bodyHeight=0;
          for(let next=index+1;next<units.length;next++){
            const childLevel=headingLevel(units[next]);
            if(childLevel&&childLevel<=level)break;
            if(!childLevel)bodyHeight+=units[next].getBoundingClientRect().height;
            if(bodyHeight>=minimumOpening)break;
            if(next+1<units.length){
              const followingLevel=headingLevel(units[next+1]);
              if(!followingLevel||followingLevel>level)protectedCuts.add(next+1);
            }
          }
        }
        const memo=new Map();
        function plan(i,start){
          if(i===pages.length)return start===units.length?{cost:0,cuts:[]}:null;
          const key=i+':'+start;
          if(memo.has(key))return memo.get(key);
          let best=null;
          for(let end=start+1;end<=units.length-(pages.length-i-1);end++){
            if(i<requiredCuts.length&&end!==requiredCuts[i])continue;
            const height=offsets[end]-offsets[start];
            if(height>limits[i])break;
            if(protectedCuts.has(end))continue;
            const remainder=plan(i+1,end);
            if(!remainder)continue;
            const fill=height/limits[i],sectionStart=units[end]?.dataset.kind==='heading';
            const gapPenalty=Math.max(0,.76-fill)**2;
            const cost=(fill-target)**2+gapPenalty+remainder.cost-(sectionStart ? .007 : 0);
            if(!best||cost<best.cost)best={cost,cuts:[end,...remainder.cuts]};
          }
          memo.set(key,best);return best;
        }
        const choice=plan(0,0);
        if(!choice)throw Error('General chapter does not fit the existing page count: '+key);
        let start=0;
        containers.forEach((c,i)=>{c.replaceChildren(...units.slice(start,choice.cuts[i]));start=choice.cuts[i];});
        const metrics=pages.map((p,i)=>{
          const c=containers[i],height=c.lastElementChild.getBoundingClientRect().bottom-c.getBoundingClientRect().top;
          if(height>limits[i]+.25||p.scrollWidth>p.clientWidth+2)throw Error('General chapter overflow '+p.dataset.physicalPage);
          return {page:+p.dataset.physicalPage,fill:Math.round(height*100/limits[i])};
        });
        const artSlots=Object.entries(placements)
          .filter(([slot])=>slot.startsWith(key+'-page-'))
          .map(([,art])=>[art.index,art]);
        const sparseArt=placements[key+'-sparse'];
        if(sparseArt){
          const fixedIndices=new Set(artSlots.map(([index])=>index));
          const sparse=metrics.filter((_,i)=>!fixedIndices.has(i)).reduce((a,b)=>a.fill<=b.fill?a:b);
          artSlots.push([metrics.indexOf(sparse),sparseArt]);
        }
        for(const [i,art] of artSlots){
          const metric=metrics[i],c=containers[i];
          if(metric.fill>68)continue;
          const remaining=limits[i]-(c.lastElementChild.getBoundingClientRect().bottom-c.getBoundingClientRect().top);
          const image=document.createElement('img');
          image.dataset.imageKey='general-'+art.name.replace('.png','');
          image.src=art.relative;
          image.alt=art.alt;
          await image.decode();
          const maxWidth=Math.min(c.clientWidth,image.naturalWidth*96/300);
          const height=Math.min(remaining-35,maxWidth/(art.ratio||3.125),image.naturalHeight*96/300);
          const width=art.ratio ? height*art.ratio : maxWidth;
          if(height>=110){
            Object.assign(image.style,{display:'block',width:(width*25.4/96)+'mm',height:(height*25.4/96)+'mm',objectFit:'cover',filter:'grayscale(1)'});
            image.className='general-metaphor';
            image.style.margin='5mm auto 0';
            c.append(image);
            if(image.getBoundingClientRect().bottom-c.getBoundingClientRect().top>limits[i])throw Error('General chapter art overflow '+metric.page);
            metric.art=art.name;
            metric.effectiveDpi=Math.round(Math.min(image.naturalWidth*96/width,image.naturalHeight*96/height));
          }
        }
        changes.push({key,pages:metrics});
      }
      return changes;
    },{keys:selectedKeys,placements,pageStarts});
    console.log(JSON.stringify(report));
    if(process.argv.includes('--measure-only'))return;
    const paginationPath=path.join(out,'pagination.json');
    const pagination=JSON.parse(fs.readFileSync(paginationPath,'utf8'));
    pagination.pageMap=await page.evaluate(()=>[...document.querySelectorAll('.page')].map(p=>({physicalPage:+p.dataset.physicalPage,type:p.dataset.type,key:p.dataset.key,khanda:p.dataset.khandaLabel,sourceIds:[...p.querySelectorAll('[data-source-id]')].map(e=>e.dataset.sourceId)})));
    fs.writeFileSync(file,'<!doctype html>\n'+await page.evaluate(()=>document.documentElement.outerHTML));
    fs.writeFileSync(paginationPath,JSON.stringify(pagination,null,2));
    const auditPath=path.join(out,'general-chapter-layout-audit.json');
    const previous=chapterOption&&fs.existsSync(auditPath)?JSON.parse(fs.readFileSync(auditPath,'utf8')):[];
    const merged=[...previous.filter(item=>!selectedKeys.includes(item.key)),...report].sort((a,b)=>a.key.localeCompare(b.key));
    fs.writeFileSync(auditPath,JSON.stringify(merged,null,2));
  }finally{await browser.close();}
}

main().catch(error=>{console.error(error);process.exitCode=1;});
