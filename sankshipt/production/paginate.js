window.bookReady=(async()=>{
const data=JSON.parse(document.getElementById('book-data').textContent),book=document.getElementById('book'),status=document.getElementById('build-status');
await Promise.all([...document.fonts].map(f=>f.load()));await document.fonts.ready;
const pages=[],exceptions=[],generated=[],docStarts={},gu=n=>String(n).replace(/[0-9]/g,d=>'૦૧૨૩૪૫૬૭૮૯'[d]);
function renumber(start=0){pages.forEach((p,i)=>{if(i<start)return;const n=i+1;p.dataset.physicalPage=n;p.id='page-'+n;p.classList.toggle('even',n%2===0);p.classList.toggle('odd',n%2===1);const f=p.querySelector('.running-footer');if(f){const number='<span class="folio">'+gu(n)+'</span>',label=n%2===0?'<span><b>નય-ચક્ષુ</b> | નયનું જ્ઞાન, સંશયનું સમાધાન</span>':'<span><b>'+(p.dataset.khandaLabel||'નય-ચક્ષુ')+'</b></span>';f.innerHTML=n%2===0?number+label:label+number;}})}
function newPage(meta={}){const p=document.createElement('section');p.className='page '+(meta.type==='chapter'?'chapter-page':'document-page nonchapter-body')+(meta.frontmatter?' frontmatter':'');p.dataset.type=meta.type||'document';p.dataset.key=meta.key||'';p.dataset.khandaLabel=meta.khandaLabel||data.khanda[meta.khanda]||'નય-ચક્ષુ';p._meta=meta;const c=document.createElement('div');c.className='page-content';p.append(c);if(!meta.frontmatter||meta.type==='preface'){const f=document.createElement('footer');f.className='running-footer';p.append(f)}book.append(p);pages.push(p);renumber(pages.length-1);return p;}
function removePage(p){const i=pages.indexOf(p);if(i>=0)pages.splice(i,1);p.remove();renumber(Math.max(0,i))}
function fit(p){const c=p.querySelector('.page-content'),f=p.querySelector('.running-footer'),b=p.getBoundingClientRect(),limit=f?f.getBoundingClientRect().top-8:c.getBoundingClientRect().bottom,last=c.lastElementChild;if(!last)return true;return last.getBoundingClientRect().bottom<=limit+.3&&p.scrollHeight<=p.clientHeight+2&&p.scrollWidth<=p.clientWidth+2&&c.scrollWidth<=c.clientWidth+2;}
function node(html){const t=document.createElement('template');t.innerHTML=html.trim();return t.content.firstElementChild;}
function pushBlock(p,el){p.querySelector('.page-content').append(el);return fit(p)}
function paginateDocument(doc){const meta={type:doc.type,frontmatter:doc.type==='preface',key:doc.key,khanda:doc.khanda,khandaLabel:doc.khanda?data.khanda[doc.khanda]:doc.title};let p=newPage(meta);docStarts[doc.key]=p;let activeTable=null,tableGroup=null;
for(let i=0;i<doc.blocks.length;i++){const block=doc.blocks[i];let el=node(block.html);el.dataset.sourceId=block.id;el.dataset.kind=block.kind;if(block.kind==='table_row'){
 const sourceRow=el.querySelector('tbody tr');sourceRow.id=block.id;sourceRow.dataset.sourceId=block.id;sourceRow.dataset.kind='table_row';sourceRow.dataset.sourceFile=doc.source_file;
 if(activeTable!==block.table_id||!tableGroup||!p.contains(tableGroup)){tableGroup=document.createElement('div');tableGroup.className='table-group';const tbl=document.createElement('table');tbl.className='semantic-table';tbl.innerHTML=el.querySelector('thead').outerHTML+'<tbody></tbody>';tableGroup.append(tbl);p.querySelector('.page-content').append(tableGroup);activeTable=block.table_id;}
 tableGroup.querySelector('tbody').append(sourceRow);
 if(!fit(p)){sourceRow.remove();if(!tableGroup.querySelector('tbody').children.length)tableGroup.remove();p=newPage(meta);tableGroup=document.createElement('div');tableGroup.className='table-group';const tbl=document.createElement('table');tbl.className='semantic-table';tbl.innerHTML=el.querySelector('thead').outerHTML+'<tbody></tbody>';tbl.querySelector('tbody').append(sourceRow);tableGroup.append(tbl);p.querySelector('.page-content').append(tableGroup);if(!fit(p))exceptions.push({type:'oversized_table_row',id:block.id,key:doc.key});}continue;
 }
 activeTable=null;tableGroup=null;
 p.querySelector('.page-content').append(el);
 if(!fit(p)){el.remove();const content=p.querySelector('.page-content'),carry=[];while(content.lastElementChild&&content.lastElementChild.dataset.keepWithNext==='true'){carry.unshift(content.lastElementChild);content.lastElementChild.remove();}if(!content.children.length){removePage(p)}p=newPage(meta);for(const h of carry)p.querySelector('.page-content').append(h);p.querySelector('.page-content').append(el);if(!fit(p))exceptions.push({type:'oversized_block',id:block.id,key:doc.key,kind:block.kind});}
 if(block.keep_with_next)el.dataset.keepWithNext='true';
 }
 return pages.filter(pg=>pg.dataset.key===doc.key);
}
const titlePageContent=`
<div class="cover-invocations" lang="sa">
  <p>॥ श्री शङ्खेश्वरपार्श्वनाथाय नमः ॥</p>
  <p>।। श्री गीतार्थ-संविग्न-स्द्गुरु परम्परायै नमः ।।</p>
  <p>॥ ऐं नमः ॥</p>
</div>
<div class="cover-masthead">
  <div class="title-mark"></div>
  <p class="title-kicker">નયનું દર્શન · જીવનનો સમન્વય</p>
  <h1 class="book-title">નય-ચક્ષુ</h1>
  <p class="book-subtitle">નયનું જ્ઞાન, સંશયનું સમાધાન</p>
</div>
<div class="cover-credits cover-credit-rows">
  <div><h2>કૃપા સ્રોત</h2><p style="font-size: 11.5pt">શ્રમણ ભગવાન <strong>શ્રી મહાવીરસ્વામી</strong></p></div>
  <div><h2>અનુગ્રહ-સ્રોત</h2><p>આત્મનિમગ્ર પરમનિર્મળ<br><strong>સદ્ગુરુપરંપરા</strong></p></div>
  <div><h2>રચના-પ્રસ્તુતિ</h2><p>શ્રી પ્રેમ-ભુવનભાનુ-જયઘોષ-રાજેન્દ્ર-જિતેન્દ્રસુરિ કૃપાપાત્ર<br>451 દીક્ષાદાનેશ્વરી પ.પૂ.આ.ભ.શ્રી વિ. <strong>ગુણરત્નસૂરીશ્વરજી</strong> મહારાજાના શિષ્ય<br>પ્રવચનપ્રભાવક પ.પૂ.આ.ભ.શ્રી વિ. <strong>રશ્મિરત્નસૂરીશ્વરજી</strong> મહારાજાના શિષ્ય<br><span style="font-size: 11.5pt">પંન્યાસશ્રી <strong>યશરત્ન</strong> વિજય</span></p></div>
  <div><h2>સંયોજન-સંપાદનાદિ</h2><p lang="en">Atmarpit Team with Advance Technology</p></div>
</div>
<div class="cover-publisher"><h2>પ્રકાશન</h2><p>પરમ-રસ</p></div>
`;
function title(){
  const p=newPage({type:'title',frontmatter:true,key:'TITLE'});
  p.classList.add('title-page');
  p.querySelector('.page-content').innerHTML=titlePageContent;
  docStarts.TITLE=p;
  generated.push({type:'title',page:1,reason:'Book title and credits supplied by the user'});
}
const publicationPageContent=`
<h1>પરિમિત-પરિચય</h1>
<div class="publication-facts">
  <div><strong>કૃતિ</strong><span>નય-ચક્ષુ — નયનું જ્ઞાન, સંશયનું સમાધાન</span></div>
  <div><strong>ભાષા</strong><span>સંસ્કૃત / ગુજરાતી</span></div>
  <div><strong>વિષય</strong><span>જૈન દર્શનના સપ્ત નય અને તેમના ઉપભેદોની તાત્ત્વિક તથા પ્રાયોગિક સમજ</span></div>
  <div><strong>ધ્યેય</strong><span>નયદૃષ્ટિથી સંશયનું સમાધાન અને જીવનમાં અનેકાંતનો વિનિયોગ</span></div>
  <div><strong>વિશેષસંયોજન</strong><span>મૂળ લક્ષણ સૂત્ર, તત્ત્વધારા, કાવ્યધારા, સાધનાધારા, કથાધારા, વિવેકધારા અને દર્શનધારા</span></div>
  <div><strong>અગોચર-કૃપા</strong><span>તીર્થંકરો, ગણધરો, પૂર્વધરો, શ્રુતધરો, યોગી મહર્ષિઓ</span></div>
  <div><strong>અહેતુક-અનુગ્રહ</strong><span>પરમાત્માના જીવંત અવતારરૂપ, અકારણવત્સલ સદ્ગુરૂચેતનાઓ</span></div>
  <div><strong>નિષ્કામ-સખા</strong><span>રત્નાધિક વડીલો, ઉપકારી વિદ્યાગુરુઓ, પ્રેમી કલ્યાણમિત્રો, સ્નેહી સહવર્તીઓ, આત્માર્પિત આશ્રિતવૃંદ</span></div>
  <div><strong>રચના-બીજ</strong><span>સત્યાન્વેષી યાત્રિકોની મુમુક્ષાપૂર્ણ જિજ્ઞાસા</span></div>
  <div><strong>વિશિષ્ટ-વાત્સલ્ય</strong><span>પ.પૂ.પં.પ્ર.શ્રી તીર્થરત્નવિજયજી મ.સા. (પિતાજી મ.સા.)<br>પ.પૂ.સા.શ્રી નિરુપમરેખાશ્રીજી મ.સા. (માતાજી મ.સા.)</span></div>
  <div><strong>વરિષ્ઠ-સહયોગ</strong><span>તેજસ ભાવસાર</span></div>
  <div><strong>પ્રકાશનવર્ષ</strong><span>વિ.સં. 2083, વીર સં. 2553, ઈ.સ. 2027</span></div>
</div>
<div class="publication-edition"><strong>આવૃત્તિ</strong><div class="publication-edition-values"><span>પ્રથમ</span><span><strong>નકલ</strong> 1000</span><span><strong>મૂલ્ય</strong> 500</span></div></div>
<div class="publication-facts publication-details">
  <div><strong>સૂચન</strong><span>આ ગ્રંથનું પ્રકાશન જ્ઞાનનિધિના સદ્વ્યયથી થયું હોવાથી ગૃહસ્થોએ મૂલ્ય ચૂકવ્યા વગર માલિકી કરવી નહીં.</span></div>
  <div><strong>પ્રિન્ટિંગ-ડિઝાઇનિંગ</strong><span>નવરંગ પ્રિન્ટર્સ – અપૂર્વ શાહ (મો. 9428500401)</span></div>
  <div><strong>પ્રાપ્તિસ્થાન</strong><span><strong>સુરત</strong> · શ્રી મહાવિદેહધામ – મો. 7448817000<br><strong>અમદાવાદ</strong> · શ્રી અપૂર્વશાહ – મો. 9428500401</span></div>
</div>
`;
const dedicationPageContent = `
      <img class="ornament" src="assets/images/magazine-botanical-grayscale.png" data-image-key="dedication-botanical" alt="">
      <section class="dedication">
  <h2>સાદર સમર્પણ</h2>
  <p>જિનપરમાત્મા અને ગણધર ભગવંતોને,<br>પૂર્વકાળના પૂજ્ય મહાપુરુષોને,<br>મધ્યસ્થ અને તટસ્થ વિદ્વાનોને,</p>
  <p><strong>મુક્તિના યાત્રિકોને, તત્ત્વજિજ્ઞાસુઓને,</strong><br><strong>સત્યપિપાસુઓને</strong> અને એ પરમ મંજિલ ભણી<br>પગલું માંડનારા સૌ પ્રવાસીઓને.</p>
  <p class="offering">એ સૌનાં હસ્તકમળોમાં</p>
  <p class="book">નય-ચક્ષુ</p>
  <p class="offering">વિનયપૂર્વક અર્પણ.</p>
</section>
      <section class="acknowledgment">
  <h2>અહો સુકૃતમ્</h2>
  <p>વિષયવૈવિધ્યથી સમૃદ્ધ વિભાગો અને સાત ખંડોમાં વિસ્તરેલા <strong>નય-ચક્ષુ</strong>ની જ્ઞાનજ્યોત જિજ્ઞાસુઓ સુધી પહોંચે, એ મંગલ ભાવનાથી</p>
  <p class="patron">એક સમર્પિત સદ્ગૃહસ્થે</p>
  <p><strong>આત્માર્પણના ભાવે</strong> આ ગ્રંથના<br><strong>પ્રકાશનનો લાભ</strong> લીધો છે.</p>
  <p class="tribute">એમના આત્મસમર્પણને અંતઃકરણપૂર્વક</p>
  <p class="salute">અનુમોદના <span>·</span> અભિનંદન <span>·</span> ધન્યવાદ</p>
</section>
    `;
function addFrontPage(type,key,markup){
  const page=newPage({type,frontmatter:true,key});
  page.classList.add(type+'-page');
  page.querySelector('.page-content').innerHTML=markup;
  docStarts[key]=page;
  generated.push({type,page:pages.length,reason:'User-supplied front matter'});
}
const openingPoemsPageContent = `
  <div class="poems">
    <article aria-labelledby="utsav">
      <img class="flower engraving" data-image-key="opening-poems-flower" src="assets/images/opening-poems-flower.png" alt="ખીલેલું ફૂલ અને ખરતી પાંખડીઓ">
      <h1 id="utsav">જોવાનો ઉત્સવ</h1>
      <p>આ સંસારમાં કોઈ ખોટું નથી —<br>
        ભૂલ ત્યારે થઈ જ્યારે<br>
        <em>જોવાનું</em> ભૂલ્યા ને <em>ઠેરવવાનું</em> શીખ્યા.</p>
      <p>ફૂલ ખીલ્યું — કહ્યું <em>'ક્ષણિક છે'</em>,<br>
        ન જોયું કે ખૂબ ખીલ્યું.<br>
        ફૂલ ઝર્યું — કહ્યું <em>'ખોવાઈ ગયું'</em>,<br>
        ન જોયું કે ખૂબ ઝર્યું.</p>
      <p>ભૂખ્યો ભિખારી — કહ્યું <em>'ભાગ્યહીન'</em>,<br>
        ન જોઈ ભૂખ.<br>
        સોનાની થાળ પકડેલો — કહ્યું <em>'ધન્ય'</em>,<br>
        ન જોઈ ભૂખ.<br>
        ઓઢણ જ જુદી — ભૂખ એક!</p>
      <p class="closing">સત્ય ક્યાંય છુપાયેલું નથી,<br>
        ચારે કોર ઊઘડ્યું જ છે —<br>
        <em>કહેવાની</em> ટેવ ઓગળે ત્યારે<br>
        <strong>જોવાનો ઉત્સવ</strong> ઊઘડે,<br>
        <strong>એ ઉત્સવ એટલે જ નય-ચક્ષુ.</strong></p>
    </article>
    <article aria-labelledby="fakta">
      <h2 id="fakta"><svg class="dove" viewBox="0 0 32 28" aria-hidden="true"><path d="M30 8l-4 2c-1 5-4 9-9 11-4 2-8 1-12 4l1-5-5-2 9-1C7 13 5 8 6 2c4 4 7 7 12 8-1-3 0-6 2-8 1 4 2 6 4 6 2-2 4-2 6 0z" fill="#000"/></svg> ફક્ત</h2>
      <p>નદી વહે છે —<br>
        કાંઠો કહે <em>'મારી'</em>,<br>
        ખેડૂત કહે <em>'જીવન'</em>,<br>
        સમુદ્ર કહે <em>'આવ'</em> —<br>
        નદી ફક્ત... વહે છે.</p>
      <p>ઝાડ ઊભું છે —<br>
        ઉનાળો કહે <em>'છાંય'</em>,<br>
        વાયરો કહે <em>'ઝૂલ'</em>,<br>
        કુહાડો કહે <em>'ઇંધણ'</em> —<br>
        ઝાડ ફક્ત... ઊભું છે.</p>
      <p>માણસ ઊભો છે —<br>
        સ્ત્રી કહે <em>'ધણી'</em>,<br>
        સંતાન કહે <em>'બાપ'</em>,<br>
        દુશ્મન કહે <em>'કાંટો'</em> —<br>
        માણસ ફક્ત... છે.</p>
      <p class="closing"><em>'ફક્ત'</em> ની ખબર પડે ત્યારે<br>
        ઠેરવ્યા ઓઢણ ખરે;<br>
        ત્યારે ઊઘડે —<br>
        <strong>નય-ચક્ષુ.</strong></p>
    </article>
  </div>
  <svg class="petal engraving" viewBox="631 1081 404 225" role="img" aria-label="ફૂલની ખરી પડેલી વળેલી પાંખડી">
      <image href="assets/images/opening-poems-flower.png" width="1169" height="1345"/>
    </svg>
`;
function toc(){
  const meta={type:'toc',frontmatter:true,key:'CONTENTS'};
  let p=newPage(meta);
  docStarts.CONTENTS=p;
  p.querySelector('.page-content').innerHTML='<h1 class="contents-heading">અનુક્રમણિકા</h1>';
  for(const entry of data.toc){
    const row=document.createElement('a');
    row.className='contents-row '+entry.type;
    row.dataset.targetKey=entry.key;
    row.innerHTML='<span class="toc-title"></span><span class="toc-page">૦૦૦</span>';
    row.firstElementChild.textContent=entry.title;
    const content=p.querySelector('.page-content');
    const previous=content.lastElementChild;
    content.append(row);
    if(fit(p))continue;
    row.remove();
    const carry=previous?.classList.contains('khanda_intro')?[previous]:[];
    p=newPage(meta);
    p.querySelector('.page-content').append(...carry,row);
    if(!fit(p))throw Error('Contents entry does not fit: '+entry.key);
  }
}
function requireFacingStart(item){
  if((pages.length+1)%2!==0)throw Error('Chapter '+item.key+' must start on an even page. Reflow the preceding material.');
}
function balanceSectionPages(sectionPages,target){
  while(sectionPages.length<target){
    let best=null;
    for(const page of sectionPages){
      const content=page.querySelector('.page-content');
      const blocks=[...content.children];
      const top=blocks[0]?.getBoundingClientRect().top;
      const bottom=blocks.at(-1)?.getBoundingClientRect().bottom;
      for(let i=1;i<blocks.length;i++){
        const previous=blocks[i-1];
        if(previous.dataset.keepWithNext==='true'||previous.classList.contains('contents-heading')||previous.classList.contains('khanda_intro'))continue;
        const boundary=blocks[i].getBoundingClientRect().top;
        const balance=Math.min(boundary-top,bottom-boundary);
        if(balance>0&&(!best||balance>best.balance))best={page,moved:blocks.slice(i),balance};
      }
    }
    if(!best)break;
    const extra=newPage(best.page._meta);
    extra.querySelector('.page-content').append(...best.moved);
    const index=pages.indexOf(best.page);
    pages.pop();
    pages.splice(index+1,0,extra);
    best.page.after(extra);
    sectionPages.splice(sectionPages.indexOf(best.page)+1,0,extra);
    renumber(index);
    if(!fit(best.page)||!fit(extra))throw Error('Measured section split overflowed '+best.page.dataset.key);
  }
}
title();
addFrontPage('publication','PUBLICATION',publicationPageContent);
addFrontPage('opening-poems','OPENING_POEMS',openingPoemsPageContent);
addFrontPage('dedication','DEDICATION',dedicationPageContent);
const ctx={newPage,removePage,fit,exceptions,gu};
for(let i=0;i<data.sequence.length;i++){const item=data.sequence[i];status.textContent=(i+1)+' / '+data.sequence.length+' વિભાગો';if(item.type==='toc'){toc();continue}if(item.type==='chapter'){requireFacingStart(item);const before=pages.length;await window.paginateChapter(item.record,ctx);docStarts[item.key]=pages[before];}else{
  const sectionPages=paginateDocument(item);
  if(item.type==='khanda_intro')balanceSectionPages(sectionPages,4);
  if(item.type==='khanda_intro'&&sectionPages.length!==4){
    throw Error('Khanda introduction '+item.key+' requires exactly four pages. Measured '+sectionPages.length+'.');
  }
}if(i%8===0){console.log('BUILD '+(i+1)+'/'+data.sequence.length+' pages='+pages.length);await new Promise(requestAnimationFrame);}}
renumber();for(const a of document.querySelectorAll('[data-target-key]')){const pg=docStarts[a.dataset.targetKey];if(pg){a.href='#'+pg.id;a.querySelector('.toc-page').textContent=gu(pg.dataset.physicalPage)}}
const sourceKeys=new Map(data.sources.map(s=>[s.path.split('/').at(-1),s.key]));for(const a of document.querySelectorAll('#book a[href]')){const href=a.getAttribute('href');if(href&&!href.startsWith('#')&&!/^https?:|^mailto:/i.test(href)){const file=decodeURIComponent(href.split('#')[0]).split('/').at(-1),key=sourceKeys.get(file),pg=docStarts[key];if(pg)a.href='#'+pg.id;}}
await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));
const pageMap=pages.map(p=>({physicalPage:+p.dataset.physicalPage,type:p.dataset.type,key:p.dataset.key,khanda:p.dataset.khandaLabel,sourceIds:[...p.querySelectorAll('[data-source-id]')].map(e=>e.dataset.sourceId)}));
window.bookResult={pageCount:pages.length,exceptions,generated,pageMap,docStarts:Object.fromEntries(Object.entries(docStarts).map(([k,p])=>[k,+p.dataset.physicalPage]))};status.textContent=gu(pages.length)+' પાનાં · સંપૂર્ણ ગ્રંથ';return window.bookResult;
})();
