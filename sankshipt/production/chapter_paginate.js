/* Measured chapter flow. ctx.newPage -> appended .page.chapter-page with
   .page-content and footer; ctx.fit -> boolean (or {fits:boolean});
   ctx.removePage removes provisional pages from DOM and its page registry. */
(function(global){
  'use strict';
  const pause=()=>Promise.resolve();
  async function ready(page){
    await document.fonts.ready;
    await Promise.all([...page.querySelectorAll('img')].map(img=>img.decode().catch(error=>{throw new Error('Chapter image failed: '+img.src+' '+error.message)})));
    await pause();
  }
  async function fits(page,ctx){const r=await ctx.fit(page);return typeof r==='boolean'?r:!!(r&&('fits'in r?r.fits:('fit'in r?r.fit:r.ok)));}
  function content(page){const c=page.querySelector('.page-content');if(!c)throw Error('Chapter page requires .page-content');return c;}
  function applyTier(page,tier){
    page.dataset.chapterFitTier=String(tier);
    if(!tier||page.dataset.chapterPart==='2')return;
    const c=content(page);c.style.gap='1mm';
    page.querySelectorAll('.idea').forEach(e=>e.style.paddingTop=e.dataset.component==='tattva-1'?'0':'1.2mm');
    page.querySelectorAll('.idea-header').forEach(e=>e.style.marginBottom='1.2mm');
    page.querySelectorAll('.source-block + .source-block,.source-list li + li').forEach(e=>e.style.marginTop='1.2mm');
    page.querySelectorAll('.closing').forEach(e=>e.style.paddingTop='2mm');
    page.querySelectorAll('.chapter-head').forEach(e=>e.style.paddingBottom='2mm');
    page.querySelectorAll('.sutra').forEach(e=>e.style.marginTop='1mm');
    page.querySelectorAll('.chapter-meta').forEach(e=>e.style.marginTop='.5mm');
    if(tier>=2){
      page.querySelectorAll('.chapter-title').forEach(e=>{e.style.fontSize='24pt';e.style.lineHeight='1.1'});
      page.querySelectorAll('.story-title').forEach(e=>e.style.marginTop='0');
      page.querySelectorAll('.story-head .section-heading').forEach(e=>e.style.marginBottom='0');
      page.querySelectorAll('.darshan').forEach(e=>e.style.paddingTop='1mm');
    }
    if(tier>=3)page.querySelectorAll('.chapter-title').forEach(e=>e.style.fontSize='22pt');
  }
  function metadata(record){return record.metadata||record;}
  function create(record,ctx,part){
    const m=metadata(record),page=ctx.newPage({type:'chapter',khanda:m.khanda,label:m.khanda_label,key:m.key,chapterTitle:m.title,part});
    page.classList.add('chapter-page');page.dataset.chapterKey=m.key;page.dataset.chapterPart=String(part);
    return page;
  }
  async function fill(page,html,tier){content(page).innerHTML=html;applyTier(page,tier);await ready(page);}
  async function improveStoryLayout(page,checkFit){
    const story=page.querySelector('.story'),art=story?.querySelector('.story-art');
    const footer=page.querySelector('.running-footer');
    if(!art||!footer||story.classList.contains('story-beside-art'))return false;
    const pxPerMm=96/25.4;
    const clearance=()=>footer.getBoundingClientRect().top-content(page).lastElementChild.getBoundingClientRect().bottom;
    if(clearance()<12*pxPerMm)return false;
    const originalWidth=art.getBoundingClientRect().width/pxPerMm;
    const copy=document.createElement('div');
    copy.className='story-copy';
    copy.append(...[...story.childNodes].filter(node=>node!==art));
    story.append(copy);
    story.classList.add('story-beside-art');
    for(const size of [36,32,28]){
      if(size<originalWidth+3)continue;
      story.style.setProperty('--story-wide-size',size+'mm');
      if(clearance()>=4*pxPerMm&&await checkFit(page))return true;
    }
    story.classList.remove('story-beside-art');
    story.style.removeProperty('--story-wide-size');
    if(!story.getAttribute('style'))story.removeAttribute('style');
    copy.replaceWith(...copy.childNodes);
    return false;
  }
  /** Source-preserving measured flow, returning appended DOM pages. */
  async function paginateChapter(record,ctx){
    if(!ctx||!ctx.newPage||!ctx.fit||!ctx.removePage)throw Error('paginateChapter requires newPage, fit, removePage');
    const sides=[record.left_components||[record.left],record.right_components||[record.right]];
    const pages=[create(record,ctx,1),create(record,ctx,2)];
    for(let i=0;i<pages.length;i++){
      const page=pages[i],maxTier=i===0?3:9;
      let fitted=false;
      for(let tier=0;tier<=maxTier;tier++){
        await fill(page,sides[i].join(''),tier);
        if(!await fits(page,ctx))continue;
        page.dataset.paginationException='none';
        fitted=true;
        break;
      }
      if(fitted)continue;
      for(const provisional of pages)await ctx.removePage(provisional);
      throw Error('Chapter '+metadata(record).key+' does not fit its required two facing pages (side '+(i+1)+'). Review the layout or source before exporting.');
    }
    await improveStoryLayout(pages[1],page=>fits(page,ctx));
    return pages;
  }
  global.paginateChapter=paginateChapter;
  global.improveStoryLayout=improveStoryLayout;
})(typeof window!=='undefined'?window:globalThis);
