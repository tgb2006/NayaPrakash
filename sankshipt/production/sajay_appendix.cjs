const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const key = 'D024';
const title = 'પરિશિષ્ટ ૯: નય-ચક્ષુ સજ્ઝાય';
const sections = {
  1: {1:'મૂળ ત્રિકાળ નૈગમ જ્ઞાનનય',4:'નૈગમ પ્રતિપાદક વ્યવહાર નય'},
  2: {1:'મૂળ સંગ્રહ દ્રવ્યાર્થિક નય',6:'સંગ્રહ પ્રતિપાદક વ્યવહાર નય'},
  3: {1:'સંગ્રહભેદક વ્યવહાર શાખા',7:'અંતિમ વ્યવહારનય શાખા',13:'શુદ્ધ દ્રવ્યાર્થિક શાખા',16:'અશુદ્ધ દ્રવ્યાર્થિક અને અન્વય શાખા',26:'નિશ્ચય નય શાખા',37:'સદ્ભૂત અને અસદ્ભૂત વ્યવહાર શાખા'},
  4: {1:'સ્થૂલ તેમજ સૂક્ષ્મ ઋજુસૂત્ર શાખા',5:'વિશેષ પર્યાયાર્થિક શાખા',11:'ઋજુસૂત્ર પ્રતિપાદક વ્યવહાર શાખા'},
  5: {1:'મૂળ શબ્દનય અને પ્રતિપાદક વ્યવહાર',3:'સપ્તભંગી વાચિક પર્યાયાર્થિક શાખા'},
  6: {1:'મૂળ સમભિરૂઢ નય અને તેનો વ્યવહાર',3:'સપ્તભંગી પૂર્ણાહુતિ નય',4:'વિકલ્પ અને નામાદિ શાખા',10:'સામાન્ય-વિશેષ સમન્વય શાખા'},
  7: {1:'મૂળ એવંભૂત નય અને પ્રતિપાદક વ્યવહાર',3:'જગત-સ્વરૂપ અને અસ્તિત્વ યુગલો',13:'મોક્ષમાર્ગના પંચ સમવાય યુગલો',19:'આત્મ-સાધના, ચેતના અને પરમ વૈલક્ષણ્ય'}
};
const css = `
.page.sajay-page{padding-top:14mm}
.sajay-page .sajay-title{margin:0 0 3mm;padding-bottom:2mm;border-bottom:.8pt solid #444;font:800 27pt/1.1 'Anek Gujarati',sans-serif}
.sajay-title span{display:block;width:max-content;margin-bottom:1mm;padding:.6mm 2mm;background:#323232;color:#fff;font:700 11pt/1.25 'Anek Gujarati',sans-serif}
.sajay-page .sajay-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5.5mm}
.sajay-page .sajay-column+ .sajay-column{border-left:.55pt solid #bbb;padding-left:2.75mm;margin-left:-2.75mm}
.sajay-page .sajay-entry{padding-bottom:.7mm;margin-bottom:.6mm;border-bottom:.45pt solid #d6d6d6}
.sajay-page .sajay-khanda{margin:0 0 1.3mm;padding:1mm 1.5mm;background:#e7e7e7;font:800 13pt/1.15 'Anek Gujarati',sans-serif}
.sajay-page .sajay-summary{border-left:1pt solid #888;padding:0 0 0 1.8mm;margin:0 0 2mm}
.sajay-page .sajay-summary h3{margin:0 0 .45mm;font:700 10.6pt/1.2 'Anek Gujarati',sans-serif}
.sajay-page .sajay-subgroup{margin:0 0 1.05mm;color:#484848;font:700 10.6pt/1.2 'Anek Gujarati',sans-serif}
.sajay-page .sajay-name{display:flex;align-items:baseline;gap:1.3mm;margin:0 0 .35mm;font:700 11.5pt/1.18 'Anek Gujarati',sans-serif;overflow-wrap:anywhere}
.sajay-page .sajay-number{flex:none;min-width:6.3mm;padding:.3mm .7mm;text-align:center;background:#e6e6e6;color:#333;font-size:9pt}
.sajay-page .sajay-verse{margin:0;font:400 10.7pt/1.29 'Noto Sans Gujarati',sans-serif;text-align:left;text-wrap:pretty;overflow-wrap:anywhere}
.sajay-page .sajay-line{display:block;padding-left:1.5mm;text-indent:-1.5mm}
`;

async function main() {
  const out = path.resolve(process.argv[2]);
  const read = name => JSON.parse(fs.readFileSync(path.join(out,name),'utf8'));
  const write = (name,data) => fs.writeFileSync(path.join(out,name),JSON.stringify(data,null,2)+'\n');
  const manifest = read('source-manifest.json');
  const plan = read('assembly-plan.json');
  const pagination = read('pagination.json');
  const chapters = plan.filter(item => item.type === 'chapter');
  if (chapters.length !== 225 || plan.some(item => item.key === key)) throw Error('Expected 225 chapters and no existing Sajay appendix');
  const poems = Object.fromEntries(manifest.blocks.filter(block => block.kind === 'poem').map(block => [block.id, block.text]));
  const khandas = Object.fromEntries(plan.filter(item => item.type === 'khanda_intro').map(item => [item.khanda,item.title]));
  const summaries = Object.fromEntries(plan.filter(item => item.type === 'khanda_intro').map(item => {
    const index = manifest.blocks.findIndex(block => block.id.startsWith(item.key+'-') && block.kind==='heading' && /સૂત્ર-સાર$/.test(block.text));
    const verse = manifest.blocks[index+1];
    if (index<0 || verse?.kind!=='verse' || !verse.id.startsWith(item.key+'-')) throw Error('Khanda Sutra-Sar missing: '+item.key);
    return [item.khanda,{id:verse.id,text:verse.text}];
  }));
  const file = path.join(out,'naya_chakshu_book.html');
  const browser = await chromium.launch({executablePath:process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try {
    const page = await browser.newPage({viewport:{width:1440,height:1100}});
    await page.emulateMedia({media:'print'});
    await page.goto(pathToFileURL(file).href);
    await page.addStyleTag({content:css});
    const result = await page.evaluate(async ({key,title,chapters,poems,khandas,sections,summaries}) => {
      await document.fonts.ready;
      const book = document.querySelector('#book');
      const oldPages = [...book.querySelectorAll('.page')];
      const start = oldPages.length+1;
      const gu = n => String(n).replace(/[0-9]/g,d=>'૦૧૨૩૪૫૬૭૮૯'[d]);
      const norm = s => s.replace(/\s+/g,'').normalize('NFC');
      const entries = [];
      const notes = [];
      const source = ['# '+title];
      const blocks = [];
      const add = (parent,tag,cls,text,id,kind) => {
        const node = document.createElement(tag);
        node.className = cls;
        if (text !== undefined) node.textContent = text;
        if (id) {
          node.id = id;
          node.dataset.sourceId = id;
          blocks.push({id,kind,text:text??''});
        }
        parent.append(node);
        return node;
      };
      const intro = document.createElement('header');
      const h = add(intro,'h1','sajay-title',undefined,key+'-title','heading');
      add(h,'span','','પરિશિષ્ટ ૯:');
      h.append(' નય-ચક્ષુ સજ્ઝાય');
      blocks.at(-1).text = title;
      let previousKhanda;
      for (const chapter of chapters) {
        const match = chapter.title.match(/^([૦-૯0-9]+)\.\s*(.+)$/);
        if (!match) throw Error('Chapter number missing: '+chapter.key);
        const [,number,name] = match;
        const ordinal = Number(number.replace(/[૦-૯]/g,d=>'૦૧૨૩૪૫૬૭૮૯'.indexOf(d)));
        const poem = document.getElementById(chapter.key+'-poem');
        const lines = poem?.innerText.trim().split(/\r?\n/);
        if (!lines?.length || norm(lines.join(' ')) !== norm(poems[chapter.key+'-poem']||'')) throw Error('Poem source mismatch: '+chapter.key);
        const entry = document.createElement('article');
        entry.className = 'sajay-entry';
        entry.dataset.chapterKey = chapter.key;
        const id = key+'-'+chapter.key;
        if (chapter.khanda !== previousKhanda) {
          add(entry,'h2','sajay-khanda',khandas[chapter.khanda],id+'-khanda','heading');
          source.push('', '## '+khandas[chapter.khanda]);
          const summary=summaries[chapter.khanda];
          const lines=[...document.getElementById(summary.id).querySelectorAll('.verse-line')].map(line=>line.textContent);
          if (lines.length!==2 || norm(lines.join(' '))!==norm(summary.text)) throw Error('Khanda Sutra-Sar source mismatch: '+summary.id);
          const box=add(entry,'div','sajay-summary');
          box.dataset.khanda=chapter.khanda;
          box.dataset.originalVerse=summary.id;
          add(box,'h3','','સૂત્ર-સાર',id+'-summary-title','heading');
          const verse=add(box,'p','sajay-verse',undefined,id+'-summary','verse');
          lines.forEach(line=>{add(verse,'span','sajay-line',line);verse.append(' ');});
          blocks.at(-1).text=lines.join(' ');
          source.push('', '### સૂત્ર-સાર', '', ...lines.map(line=>line+'  '));
          previousKhanda = chapter.khanda;
        }
        const subgroup = sections[chapter.khanda][ordinal];
        if (subgroup) {
          add(entry,'h3','sajay-subgroup',subgroup,id+'-subgroup','heading');
          source.push('', '### '+subgroup);
        }
        const heading = add(entry,'h4','sajay-name',undefined,id+'-name','heading');
        add(heading,'span','sajay-number',number+'.');
        add(heading,'span','sajay-name-text',' '+name);
        blocks.at(-1).text = chapter.title;
        const verse = add(entry,'p','sajay-verse',undefined,id+'-poem','verse');
        lines.forEach(line => {add(verse,'span','sajay-line',line);verse.append(' ');});
        blocks.at(-1).text = lines.join(' ');
        source.push('', '#### '+chapter.title, '', ...lines.map(line=>line+'  '));
        entries.push(entry);
      }
      const pages = [];
      function createPage() {
        const number = start+pages.length;
        const pg = document.createElement('section');
        pg.className = 'page document-page nonchapter-body sajay-page '+(number%2?'odd':'even');
        Object.assign(pg.dataset,{type:'appendix',key,physicalPage:number,khandaLabel:title});
        pg.id = 'page-'+number;
        const content = add(pg,'div','page-content');
        if (!pages.length) content.append(intro);
        const grid = add(content,'div','sajay-grid');
        const cols = [add(grid,'div','sajay-column'),add(grid,'div','sajay-column')];
        const footer = add(pg,'footer','running-footer');
        const folio = '<span class="folio">'+gu(number)+'</span>';
        const label = '<span><b>નય-ચક્ષુ</b> | નયનું જ્ઞાન, સંશયનું સમાધાન</span>';
        footer.innerHTML = number%2 ? '<span><b>'+title+'</b></span>'+folio : folio+label;
        book.append(pg);
        const record = {pg,cols,limit:footer.getBoundingClientRect().top-8};
        pages.push(record);
        return record;
      }
      const bottom = node => node.getBoundingClientRect().bottom;
      function fitName(entry) {
        const name=entry.querySelector('.sajay-name-text');
        name.style.transform='';
        name.style.whiteSpace='nowrap';
        for (const pt of [11.5,11,10.5,10,9.5]) {
          name.style.fontSize=pt+'pt';
          if (name.getBoundingClientRect().right<=entry.getBoundingClientRect().right+.2) return;
        }
        name.style.fontSize='9.5pt';
        const rect=name.getBoundingClientRect();
        const available=entry.getBoundingClientRect().right-rect.left-.5;
        name.style.transformOrigin='left center';
        name.style.transform='scaleX('+available/rect.width+')';
      }
      let current = createPage(), column = 0;
      for (const entry of entries) {
        current.cols[column].append(entry);
        fitName(entry);
        if (bottom(entry)<=current.limit) continue;
        if (column===0) column=1;
        else {current=createPage();column=0;}
        current.cols[column].append(entry);
        fitName(entry);
        if (bottom(entry)>current.limit) throw Error('Sajay entry exceeds page: '+entry.dataset.chapterKey);
      }
      const [left,right] = current.cols;
      while (left.children.length>1) {
        const item=left.lastElementChild;
        const imbalance=Math.abs(bottom(left.lastElementChild)-(right.lastElementChild?bottom(right.lastElementChild):right.getBoundingClientRect().top));
        right.prepend(item);
        if (bottom(right.lastElementChild)>current.limit || Math.abs(bottom(left.lastElementChild)-bottom(right.lastElementChild))>=imbalance) {
          left.append(item);
          break;
        }
      }
      for (const entry of entries) {
        const name=entry.querySelector('.sajay-name-text');
        if (name.getBoundingClientRect().height>parseFloat(getComputedStyle(name).lineHeight)+1) notes.push(entry.dataset.chapterKey);
        if (name.getBoundingClientRect().right>entry.getBoundingClientRect().right+.25
            || entry.querySelector('.sajay-verse').scrollWidth>entry.clientWidth+1) throw Error('Sajay horizontal overflow: '+entry.dataset.chapterKey);
      }
      const tocRow=document.querySelector('[data-target-key="D023"]').cloneNode(true);
      tocRow.dataset.targetKey=key;
      tocRow.href='#page-'+start;
      tocRow.querySelector('.toc-title').textContent=title;
      tocRow.querySelector('.toc-page').textContent=gu(start);
      document.querySelector('[data-target-key="D023"]').after(tocRow);
      if (bottom(tocRow)>bottom(tocRow.closest('.page-content'))) throw Error('Contents page does not fit the Sajay row');
      const overview=[...document.querySelectorAll('.page[data-key="D015"]')];
      const edits=[];
      function replaceText(host,from,to) {
        const walker=document.createTreeWalker(host,NodeFilter.SHOW_TEXT);
        for (let node=walker.nextNode();node;node=walker.nextNode()) {
          if (!node.data.includes(from)) continue;
          node.data=node.data.replace(from,to);
          edits.push({id:host.dataset.sourceId,from,to});
          return;
        }
        throw Error('Appendix overview text missing: '+from);
      }
      const overviewNodes=overview.flatMap(pg=>[...pg.querySelectorAll('[data-source-id]')]);
      const count=overviewNodes.find(node=>node.textContent.includes('૮ વિશિષ્ટ પરિમાણોમાં'));
      replaceText(count,'૮ વિશિષ્ટ પરિમાણોમાં','૯ વિશિષ્ટ પરિમાણોમાં');
      replaceText(count,'પુનરાવર્તન વિના, ','વિષયવાર ');
      replaceText(overviewNodes.find(node=>node.textContent.includes('The 8 Analytical Appendices')),'The 8 Analytical Appendices','The 9 Appendices');
      const lastTable=overview.at(-1).querySelector('.semantic-table tbody');
      const tr=add(lastTable,'tr','',undefined,key+'-overview','table_row');
      const cells=['પરિશિષ્ટ ૯','નય-ચક્ષુ સજ્ઝાય','સાત ખંડના સૂત્ર-સાર અને ૨૨૫ નયોની કાવ્યધારા','કાવ્ય દ્વારા નયના ભાવનું સ્મરણ'];
      cells.forEach((text,i)=>{
        const td=add(tr,'td','');
        if (i===1) {const link=add(td,'a','',text);link.href='#page-'+start;} else td.textContent=text;
      });
      tr.dataset.stripe='white';
      const rowRecord=blocks.pop();rowRecord.text=cells.join(' | ');
      const content=overview.at(-1).querySelector('.page-content');
      const list=content.lastElementChild.cloneNode(true);
      list.id=list.dataset.sourceId=key+'-usage';
      list.querySelector('.generic-list-marker').textContent='૭.';
      list.querySelector('.generic-list-marker').dataset.display='૭';
      const copy=list.querySelector('.generic-list-copy');
      copy.replaceChildren();
      add(copy,'strong','','નયના ભાવનું કાવ્યમય સ્મરણ');
      copy.append(': ');
      add(copy,'a','','પરિશિષ્ટ ૯ — નય-ચક્ષુ સજ્ઝાય').href='#page-'+start;
      copy.append('માં ખંડવાર સૂત્ર-સાર અને દરેક નયની કાવ્યધારા મળે છે.');
      content.append(list);
      const overviewLimit=overview.at(-1).querySelector('.running-footer').getBoundingClientRect().top-8;
      if (bottom(list)>overviewLimit) {
        content.querySelectorAll('.generic-list-item').forEach(item=>item.style.marginBottom='1.4mm');
        if (bottom(list)>overviewLimit) throw Error('Appendix overview does not fit new row and usage note');
      }
      const pageMap=[...book.querySelectorAll('.page')].map(pg=>({physicalPage:+pg.dataset.physicalPage,type:pg.dataset.type,key:pg.dataset.key,khanda:pg.dataset.khandaLabel,sourceIds:[...pg.querySelectorAll('[data-source-id]')].map(n=>n.dataset.sourceId)}));
      const status=document.querySelector('#build-status');
      if(status)status.textContent=gu(pageMap.length)+' પાનાં · સંપૂર્ણ ગ્રંથ';
      return {start,pageMap,notes,source:source.join('\n')+'\n',blocks:[...blocks,rowRecord,{id:key+'-usage',kind:'list_item',text:copy.textContent}],edits,
        entries:entries.map(e=>e.dataset.chapterKey),pages:pages.length};
    }, {key,title,chapters,poems,khandas,sections,summaries});
    const sourceFile='source_snapshot/parishishta/09_nay_chakshu_sajay_gu.md';
    const sourcePath=path.join(out,sourceFile);
    fs.mkdirSync(path.dirname(sourcePath),{recursive:true});
    fs.writeFileSync(sourcePath,result.source);
    const records=new Map([...manifest.blocks,...result.blocks.map(block=>({...block,source_file:sourceFile,source_text:block.text}))].map(block=>[block.id,block]));
    for(const {id,from,to} of result.edits) {
      const record=records.get(id);
      if(!record?.text.includes(from))throw Error('Overview manifest mismatch: '+id);
      record.text=record.text.replace(from,to);
    }
    const ids=result.pageMap.flatMap(pg=>pg.sourceIds);
    if(ids.length!==records.size || new Set(ids).size!==ids.length || ids.some(id=>!records.has(id)))throw Error('Sajay manifest coverage mismatch');
    manifest.blocks=ids.map(id=>records.get(id));
    manifest.sources.push({key,type:'appendix',path:sourceFile,sha256:crypto.createHash('sha256').update(result.source).digest('hex')});
    Object.assign(manifest.counts,{sources:manifest.sources.length,nonchapter_sources:manifest.sources.length-chapters.length,blocks:manifest.blocks.length});
    plan.push({key,title,type:'appendix',khanda:null});
    pagination.docStarts[key]=result.start;
    Object.assign(pagination,{pageMap:result.pageMap,pageCount:result.pageMap.length});
    write('source-manifest.json',manifest);
    write('assembly-plan.json',plan);
    write('pagination.json',pagination);
    write('sajay-audit.json',{start:result.start,pages:result.pages,chapters:result.entries.length,chapterKeys:result.entries,khandaSummaries:summaries,wrappedNames:result.notes});
    fs.writeFileSync(file,'<!doctype html>\n'+await page.evaluate(()=>document.documentElement.outerHTML));
    console.log(JSON.stringify({start:result.start,pages:result.pages,total:pagination.pageCount,poems:result.entries.length,summaries:Object.keys(summaries).length,wrappedNames:result.notes}));
  } finally {
    await browser.close();
  }
}

main().catch(error=>{console.error(error);process.exitCode=1;});
