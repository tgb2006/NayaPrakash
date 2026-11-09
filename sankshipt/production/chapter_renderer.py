"""Current-source chapter parser and selected magazine renderer.

Public API: load_chapters(root), render_chapter(chapter, start_page=2,
asset_prefix=''), chapter_css(). left/right are page INNER HTML, not page wrappers.
Source prose is never rewritten. Rendered ordinal transformations are explicit.
"""
from pathlib import Path
import re,html,json,hashlib
from dataclasses import dataclass,field
from typing import Any

GU='૦૧૨૩૪૫૬૭૮૯'
EN='0123456789'
TO_GU=str.maketrans(EN,GU)
TO_EN=str.maketrans(GU,EN)
KHANDAS={1:'પ્રથમ ખંડ: નૈગમ નય',2:'દ્વિતીય ખંડ: સંગ્રહ નય',3:'તૃતીય ખંડ: વ્યવહાર નય',4:'ચતુર્થ ખંડ: ઋજુસૂત્ર નય',5:'પંચમ ખંડ: શબ્દ નય',6:'ષષ્ઠ ખંડ: સમભિરૂઢ નય',7:'સપ્તમ ખંડ: એવંભૂત નય'}
ENGLISH={'તત્ત્વધારા':'THE PRINCIPLE','કાવ્યધારા':'THE POETRY','સાધનાધારા':'THE PRACTICE','કથાધારા':'THE STORY','વિવેકધારા':'THE DISCERNMENT','દર્શનધારા':'THE PERSPECTIVE'}

def normalize_script(text):
    """Repair known mixed-script spellings for display and keep the source text."""
    return (text.replace('नैगम\u0a83', 'नैगम\u0903')
                .replace('भिन्नमर्थ\u0a82', 'भिन्नमर्थ\u0902')
                .replace('અनेकાંત', 'અનેકાંત'))

def gu_number(n,zero_pad=False):return (f'{n:02d}' if zero_pad else str(n)).translate(TO_GU)
def plain(s):
    s=re.sub(r'<br\s*/?>',' ',s,flags=re.I)
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1',s)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'[*`_]','',s))).strip()
def inline(s):
    # Author-supplied inline markup only; no script or arbitrary HTML passes through.
    s=s.replace('\\|','|')
    s=html.escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)',r'<em>\1</em>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',s)
    return re.sub(r'&lt;br\s*/?&gt;','<br>\n',s,flags=re.I)

@dataclass
class Chapter:
    key:str
    sequence:int
    source_file:str
    source_sha256:str
    title:str
    ordinal:str
    meta:dict
    tattva:list
    poem:str
    practice:str
    story_title:str
    pipasa:list
    paan:list
    ekant:list
    anekant:list
    darshan:list
    mapping:dict
    khanda:int
    extra:dict=field(default_factory=dict)

def split_prose(s):
    out=[];buf=[]
    def flush():
        if buf:out.append({'type':'prose','text':' '.join(buf).strip()});buf.clear()
    for raw in s.strip().splitlines():
        line=raw.strip()
        if not line or re.fullmatch(r'[-*_]{3,}',line):flush();continue
        line=re.sub(r'^>\s*','',line)
        bullet=re.match(r'^(?:[•*-]|[૦-૯0-9]+[.)])\s+(.+)',line)
        if bullet:flush();out.append({'type':'list_item','text':bullet.group(1).strip()})
        else:buf.append(line)
    flush();return out

def parse_chapter(root,row):
    source=root/row['source_file'];raw=source.read_bytes();s=raw.decode('utf-8-sig').replace('\r\n','\n')
    titleline=re.search(r'^#\s+(.+)',s,re.M).group(1).strip()
    tm=re.match(r'([૦-૯0-9]+)[.、)]\s*(.*)',titleline)
    ordinal,title=(tm.group(1),tm.group(2)) if tm else (str(row['chapter_in_khanda']).translate(TO_GU),titleline)
    meta_line=next((x.strip().strip('*').strip() for x in s.splitlines()[1:] if x.strip().startswith('*(')), '')
    meta={}
    for part in meta_line.strip('()').split('|'):
        if ':' in part:
            k,v=part.split(':',1);meta[k.strip()]=v.strip()
    parts=re.split(r'^##\s+(.+?)\s*$',s,flags=re.M);sections={parts[i].strip():parts[i+1].strip().strip('-').strip() for i in range(1,len(parts),2)}
    prefix_lines=[];primary_meta_seen=False
    for line in parts[0].splitlines():
        if line.startswith('# '):continue
        if not primary_meta_seen and line.strip().startswith('*(મૂળ નય:'):
            primary_meta_seen=True;continue
        if re.fullmatch(r'\s*[-*_]{3,}\s*',line):continue
        prefix_lines.append(line)
    prefatory_blocks=split_prose('\n'.join(prefix_lines))
    tattva_raw=sections.get('તત્ત્વધારા',sections.get('તત્ત્વધારા',''))
    tp=re.split(r'^\*\*([૦-૯0-9]+[.、)]?.+?)\*\*\s*$',tattva_raw,flags=re.M)
    tattva=[]
    for i in range(1,len(tp),2):
        heading=re.sub(r'^[૦-૯0-9]+[.、)]?\s*','',tp[i]).strip()
        a,b=(heading.split(':',1)+[''])[:2] if ':' in heading else (heading,'')
        tattva.append({'heading':a.strip(),'subtitle':b.strip(),'blocks':split_prose(tp[i+1]),'source_heading':tp[i]})
    if len(tattva)!=4:raise ValueError(f'{row["key"]}: expected four Tattva blocks, got {len(tattva)}')
    kp=sections['કાવ્યધારા અને સાધનાધારા'];data=[]
    for line in kp.splitlines():
        if not line.strip().startswith('|'):continue
        cells=[c.strip() for c in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
        if len(cells)>=2 and not cells[0].startswith(('📜',':','-')):data.append(cells)
    if len(data)!=1:raise ValueError(f'{row["key"]}: unexpected Kavya table rows {len(data)}')
    def subs(name):
        parts=re.split(r'^###\s+(.+?)\s*$',sections[name],flags=re.M)
        return {parts[i].strip():parts[i+1].strip() for i in range(1,len(parts),2)}
    story=subs('કથાધારા');st=next(k for k in story if k not in ['પિપાસા','પાન'])
    if story[st].strip():raise ValueError(f'{row["key"]}: prose before Pipasa requires explicit handling')
    vivek=subs('વિવેકધારા')
    ek=next(k for k in vivek if k.startswith('એકાંત દર્શન'));an=next(k for k in vivek if k.startswith('અનેકાંત દર્શન'))
    darshan=[]
    for item in split_prose(sections['દર્શનધારા']):
        text=item['text'];m=re.match(r'\*\*(.+?)\*\*\s*:\s*(.*)',text,re.S)
        if not m:raise ValueError(f'{row["key"]}: unrecognized Darshan {text[:80]}')
        heading=re.sub(r'^[૦-૯0-9]+[.、)]?\s*','',m.group(1)).strip()
        darshan.append({'heading':heading,'body':m.group(2).strip(),'source_text':text})
    if len(darshan)!=4:raise ValueError(f'{row["key"]}: expected four Darshan blocks')
    return Chapter(row['key'],row['sequence'],row['source_file'],hashlib.sha256(raw).hexdigest(),title,ordinal,meta,tattva,data[0][0],data[0][1],st,split_prose(story['પિપાસા']),split_prose(story['પાન']),split_prose(vivek[ek]),split_prose(vivek[an]),darshan,row,int(row['khanda']),{'source_title':titleline,'source_meta':meta_line,'prefatory_blocks':prefatory_blocks,'ekant_heading':ek,'anekant_heading':an})

def load_chapters(root):
    root=Path(root);rows=json.loads((root/'Image/chapter-image-map.json').read_text(encoding='utf-8-sig'))
    return [parse_chapter(root,row) for row in sorted(rows,key=lambda r:r['sequence'])]

def render_chapter(chapter,start_page=2,asset_prefix='',**kwargs):
    c=chapter;manifest=[];prefix=c.key
    def mark(tag,ident,text,cls='',display=None,source_text=None):
        ident=f'{prefix}-{ident}'
        rendered=normalize_script(text if display is None else display)
        expected=plain(rendered)
        manifest.append({'id':ident,'text':expected,'source_file':c.source_file,'source_text':plain(source_text or text),'kind':cls or tag})
        return f'<{tag} id="{ident}" data-source-id="{ident}" class="{cls}">{inline(rendered)}</{tag}>'
    def heading(gu,ident):return f'<h2 class="section-heading" id="{prefix}-{ident}"><span>{gu}</span><small lang="en">{ENGLISH[gu]}</small></h2>'
    def prose(blocks,ident):
        out=[];ul=False
        for i,b in enumerate(blocks):
            if b['type']=='list_item':
                if not ul:out.append('<ul class="source-list">');ul=True
                out.append(mark('li',f'{ident}-{i+1}',b['text'],'source-block'))
            else:
                if ul:out.append('</ul>');ul=False
                out.append(mark('p',f'{ident}-{i+1}',b['text'],'source-block'))
        if ul:out.append('</ul>')
        return ''.join(out)
    original=mark('span','meta-original','મૂળ નય: '+c.meta.get('મૂળ નય',''),'meta-original')
    category=mark('span','meta-category','મુખ્ય શ્રેણી: '+c.meta.get('મુખ્ય શ્રેણી',''),'meta-category')
    title=mark('h1','title',c.title,'chapter-title',source_text=c.extra['source_title'])
    author_definition=c.meta.get('લેખકૃત વ્યાખ્યા-આશય')
    sutra_text=c.meta.get('વ્યાખ્યા-સૂત્ર') or ('લેખકૃત વ્યાખ્યા-આશય: '+author_definition if author_definition else '')
    if not sutra_text:raise ValueError(f'{c.key}: no sutra or attributed author definition')
    sutra=mark('p','sutra',sutra_text,'sutra-text author-definition' if author_definition else 'sutra-text')
    masthead=f'<header class="chapter-masthead component" data-component="masthead"><div class="chapter-head"><div>{category}{title}</div><span class="chapter-index" aria-label="પ્રકરણ {c.ordinal}">{gu_number(int(c.ordinal.translate(TO_EN)),True)}</span></div><div class="chapter-meta">{original}</div><div class="sutra"><small>મૂળ લક્ષણ સૂત્ર</small>{sutra}</div></header>'
    left_components=[masthead]
    if c.extra.get('prefatory_blocks'):
        left_components.append('<section class="source-note component" data-component="source-note">'+prose(c.extra['prefatory_blocks'],'source-note')+'</section>')
    for i,idea in enumerate(c.tattva):
        title=mark('h3',f'tattva-{i+1}-heading',idea['heading'],'idea-heading')
        sub=mark('h4',f'tattva-{i+1}-subtitle',idea['subtitle'],'idea-subtitle') if idea['subtitle'] else ''
        top=heading('તત્ત્વધારા','tattva-heading') if i==0 else ''
        comp=f'<article class="idea component" data-component="tattva-{i+1}">{top}<div class="idea-header"><span class="idea-number">{gu_number(i+1,True)}</span>{title}{sub}</div>{prose(idea["blocks"],f"tattva-{i+1}-body")}</article>'
        left_components.append(comp)
    poem=mark('p','poem',c.poem,'poem');practice=mark('p','practice',c.practice,'practice-text')
    left_components.append(f'<section class="closing component" data-component="closing"><div>{heading("કાવ્યધારા","poem-heading")}{poem}</div><div class="practice">{heading("સાધનાધારા","practice-heading")}{practice}</div></section>')
    story_title=mark('h3','story-title',c.story_title,'story-title')
    story_head=f'<header class="story-head component" data-component="story-head">{heading("કથાધારા","story-heading")}{story_title}</header>'
    right_components=[story_head]
    image_src=asset_prefix+c.mapping['html_src']
    image=f'<figure class="story-art"><img src="{html.escape(image_src,quote=True)}" width="1254" height="1254" alt="{html.escape(c.story_title,quote=True)}" data-image-key="{c.key}"></figure>'
    pp=prose(c.pipasa,'pipasa');pa=prose(c.paan,'paan')
    right_components.append(f'<section class="story component" data-component="story">{image}<h3 class="small-label">પિપાસા</h3>{pp}<div class="paan"><h3 class="small-label">પાન</h3>{pa}</div></section>')
    ekant=prose(c.ekant,'ekant');anekant=prose(c.anekant,'anekant')
    right_components.append(f'<section class="vivek component" data-component="vivek">{heading("વિવેકધારા","vivek-heading")}<div class="comparison"><article><h3>{inline(c.extra["ekant_heading"])}</h3>{ekant}</article><article class="positive"><h3>{inline(c.extra["anekant_heading"])}</h3>{anekant}</article></div></section>')
    cells=[]
    for i,item in enumerate(c.darshan):
        h=mark('span',f'darshan-{i+1}-heading',item['heading'],'row-title')
        body=mark('span',f'darshan-{i+1}-body',item['body'],'row-body')
        cells.append(f'<div class="darshan-row"><span class="row-number">{gu_number(i+1,True)}</span><div class="row-copy">{h}<span class="source-colon">: </span>{body}</div></div>')
    right_components.append(f'<section class="darshan component" data-component="darshan">{heading("દર્શનધારા","darshan-heading")}<div class="darshan-table">{"".join(cells)}</div></section>')
    # Manifest is DOM reading order; metadata was constructed before H1 but H1 precedes original-name line.
    left=''.join(left_components);right=''.join(right_components);combined=left+right
    manifest.sort(key=lambda b:combined.index('id="'+b['id']+'"'))
    metadata={'key':c.key,'sequence':c.sequence,'title':c.title,'source_title':c.extra['source_title'],'source_file':c.source_file,'source_sha256':c.source_sha256,'khanda':c.khanda,'khanda_label':KHANDAS[c.khanda],'image_key':c.key,'image_src':image_src,'start_page':start_page}
    return {'left':left,'right':right,'left_components':left_components,'right_components':right_components,'manifest':manifest,'metadata':metadata}

def chapter_css():
    return CSS

CSS=r'''
.chapter-page{--ink:#171717;--muted:#626262;--rule:#cecece;--wash:#f2f2f2;--component-gap:2mm;--idea-gap:1.8mm;--image-size:32mm}
.chapter-page .page-content{display:flex;flex-direction:column;gap:var(--component-gap);min-height:0}
.chapter-page.odd .page-content{gap:1mm}
.chapter-page h1,.chapter-page h2,.chapter-page h3,.chapter-page h4,.chapter-page p,.chapter-page figure{margin:0}
.chapter-page h1,.chapter-page h2,.chapter-page h3,.chapter-page h4{font-family:'Anek Gujarati',sans-serif}
.chapter-page p,.chapter-page li,.chapter-page .row-copy{font:400 11pt/1.38 'Noto Sans Gujarati',sans-serif;text-align:justify;text-align-last:start;text-justify:inter-word;overflow-wrap:normal}
.chapter-page .source-block+.source-block{margin-top:2mm}
.chapter-page .section-heading{font:800 17pt/1.3 'Anek Gujarati',sans-serif;display:flex;align-items:center;gap:2mm;margin:0 0 1mm;white-space:nowrap}
.chapter-page .section-heading::after{content:'';height:.55pt;background:#cecece;flex:1;min-width:1mm}
.chapter-page .section-heading small{font:400 7.5pt/1.15 'Book Serif',Georgia,serif;letter-spacing:.35pt;color:#777;flex:none}
.chapter-page .chapter-head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2mm;border-bottom:1.4pt solid #171717;padding-bottom:2.5mm}
.chapter-page .chapter-title{font:800 28pt/1.1 'Anek Gujarati',sans-serif;letter-spacing:-.3pt;overflow-wrap:normal}
.chapter-page .chapter-index{font:800 34pt/1 'Anek Gujarati',sans-serif;color:#dedede;text-align:right;align-self:center;min-width:16mm}
.chapter-page .meta-category,.chapter-page .meta-original{display:block;font:600 8.5pt/1.3 'Anek Gujarati',sans-serif;color:#626262}
.chapter-page .meta-category{position:relative;top:-2.5mm;margin-bottom:1mm}.chapter-page .chapter-meta{margin-top:1mm}
.chapter-page .sutra{display:flex;align-items:center;justify-content:space-between;gap:2mm;border-left:1.5pt solid #222;padding-left:3mm;margin-top:1.5mm}
.chapter-page .sutra small{font:600 8pt/1.2 'Anek Gujarati',sans-serif;color:#626262;flex:none}
.chapter-page .sutra p{font:400 10.5pt/1.35 'Noto Sans Devanagari',sans-serif;text-align:left;min-width:0;overflow-wrap:anywhere}
.chapter-page .sutra p.author-definition{font-family:'Noto Sans Gujarati',sans-serif}
.chapter-page .idea{border-top:.6pt solid #cecece;padding-top:1.8mm}
.chapter-page .idea:first-of-type{border-top:0;padding-top:0}
.chapter-page .idea-header{margin-bottom:var(--idea-gap)}
.chapter-page .idea-number,.chapter-page .row-number{font:700 16pt/1 'Anek Gujarati',sans-serif;color:#888}
.chapter-page .idea-number{display:inline-block;min-width:9mm;margin-right:1mm}
.chapter-page .idea-heading{font:700 13pt/1.15 'Anek Gujarati',sans-serif;display:inline}
.chapter-page .idea-subtitle{font:600 10.5pt/1.2 'Anek Gujarati',sans-serif;color:#5b5b5b;display:inline;margin-left:2mm}
.chapter-page .source-list{list-style:none;margin:0;padding:0}.chapter-page .source-list li+li{margin-top:2mm}
.chapter-page .closing{display:grid;grid-template-columns:1fr 1fr;gap:5.8mm;border-top:1.4pt solid #222;padding-top:3mm;margin-top:auto;margin-bottom:1mm}
.chapter-page .practice{border-left:.55pt solid #cecece;padding-left:3mm}
.chapter-page .poem{font:600 12pt/1.45 'Anek Gujarati',sans-serif;text-align:left;text-align-last:start}
.chapter-page .story-title,.chapter-page .small-label,.chapter-page .comparison h3,.chapter-page .row-title{font:700 13pt/1.15 'Anek Gujarati',sans-serif;color:#171717}
.chapter-page .story-title{margin-top:1mm}.chapter-page .small-label{margin-bottom:1.2mm}
.chapter-page .story{display:flow-root}.chapter-page .story-art{float:left;width:var(--image-size);height:var(--image-size);margin:0 4mm 1mm 0}
.chapter-page .story-art img{display:block;width:100%;height:100%;object-fit:contain}
.chapter-page .story.story-beside-art{display:grid;grid-template-columns:var(--story-wide-size) minmax(0,1fr);align-items:start;gap:4mm}
.chapter-page .story.story-beside-art .story-art{float:none;width:100%;height:auto;aspect-ratio:1;margin:0}
.chapter-page .story.story-beside-art .paan{margin-top:2mm}
.chapter-page .paan{clear:both;border-left:1.5pt solid #222;padding-left:2.5mm;margin-top:1mm;display:flow-root}
.chapter-page .vivek{margin-top:3.5mm}
.chapter-page .comparison{display:grid;grid-template-columns:1fr 1fr;gap:5.8mm}
.chapter-page .comparison article{border-top:.8pt solid #444;padding-top:2mm}
.chapter-page .comparison h3{margin-bottom:1.9mm}
.chapter-page .comparison .positive{background:#f2f2f2;border-top:1.3pt solid #222;padding:2.4mm 2.5mm 1.8mm}
.chapter-page .darshan{border-top:.8pt solid #777;padding-top:2.4mm}
.chapter-page .darshan-table{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;border:.55pt solid #aaa}
.chapter-page .darshan-row{display:grid;grid-template-columns:6.5mm minmax(0,1fr);column-gap:1.8mm;align-items:start;padding:1.45mm 2mm 1.3mm;min-width:0}
.chapter-page .darshan-row:nth-child(-n+3){border-bottom:.55pt solid #aaa}.chapter-page .darshan-row:nth-child(2){border-right:.55pt solid #aaa}
.chapter-page .darshan-row:first-child,.chapter-page .darshan-row:last-child{grid-column:1/-1;background:#eaeaea}
.chapter-page .row-copy{min-width:0}.chapter-page .row-title{display:inline-block;max-width:100%;text-align:left}
.chapter-page .row-copy .source-colon{margin-right:.5mm}
.chapter-page .row-body{font:400 11pt/1.38 'Noto Sans Gujarati',sans-serif}
.chapter-page .component{break-inside:avoid}

/* Preserve the existing left page and fit the right page independently. */
.page.chapter-page.even{padding-top:10mm;padding-left:8mm;padding-right:10mm}
.page.chapter-page.odd{padding-top:var(--right-top,9mm);padding-left:var(--right-inner,10mm);padding-right:var(--right-outer,8mm)}
.chapter-page.even .running-footer{left:8mm;right:10mm}
.chapter-page.odd .running-footer{left:10mm;right:8mm}
.chapter-page.even :is(p.source-block,li.source-block,.practice-text){line-height:1.16}
.chapter-page.even .section-heading{line-height:1.08;margin-bottom:.6mm}
.chapter-page .chapter-masthead .sutra{padding-left:1.5mm}

/* Keep box padding and the section breaks at every measured density. */
.chapter-page.odd :is(p.source-block,.row-copy,.row-body){line-height:var(--right-leading,1.38);letter-spacing:var(--right-tracking,normal)}
.chapter-page.odd .comparison{gap:var(--right-column-gap,5.8mm)}
.chapter-page.odd[data-chapter-fit-tier]:not([data-chapter-fit-tier="0"]) .story-art{margin-right:3mm}
.chapter-page.odd[data-chapter-fit-tier="1"]{--right-leading:1.32;--image-size:26mm}
.chapter-page.odd[data-chapter-fit-tier="2"]{--right-leading:1.26;--image-size:23mm}
.chapter-page.odd:is([data-chapter-fit-tier="3"],[data-chapter-fit-tier="4"]){--right-top:8mm;--right-inner:9mm;--right-outer:7mm;--image-size:23mm}
.chapter-page.odd[data-chapter-fit-tier="3"]{--right-leading:1.23}
.chapter-page.odd[data-chapter-fit-tier="4"]{--right-leading:1.20}
.chapter-page.odd[data-chapter-fit-tier="5"]{--right-leading:1.18;--right-top:7mm;--right-inner:8mm;--right-outer:7mm;--image-size:21mm}
.chapter-page.odd:is([data-chapter-fit-tier="6"],[data-chapter-fit-tier="7"]){--right-leading:1.16;--right-top:7mm;--right-inner:8mm;--right-outer:6mm;--image-size:20mm;--right-column-gap:4.5mm;--right-tracking:-.12pt}
.chapter-page.odd[data-chapter-fit-tier="7"]{--image-size:18mm;--right-top:6.5mm}
.chapter-page.odd:is([data-chapter-fit-tier="8"],[data-chapter-fit-tier="9"]){--right-leading:1.16;--right-top:6mm;--right-inner:7.5mm;--right-outer:6mm;--image-size:17mm;--right-column-gap:4.5mm;--right-tracking:-.17pt}
.chapter-page.odd[data-chapter-fit-tier="9"]{--right-inner:7mm;--right-outer:5.8mm;--right-top:5.2mm}
.chapter-page.odd[data-chapter-fit-tier="9"] .story p{line-height:1.13}
'''

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',default='D:/PROJECT_WORK/NayaPrakash_Book');p.add_argument('--out',default='tmp/codex/full-book/chapters');args=p.parse_args()
    root=Path(args.root);out=root/args.out;out.mkdir(parents=True,exist_ok=True)
    chapters=load_chapters(root);records=[render_chapter(c) for c in chapters]
    (out/'chapters.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'chapter.css').write_text(chapter_css(),encoding='utf-8')
    (out/'parse-receipt.json').write_text(json.dumps({'chapters':len(chapters),'blocks':sum(len(r['manifest']) for r in records),'sources':[{**r['metadata'],'left_chars':len(plain(re.sub(r'<[^>]+>',' ',r['left']))),'right_chars':len(plain(re.sub(r'<[^>]+>',' ',r['right'])))} for r in records]},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(chapters)} chapters parsed; {sum(len(r["manifest"]) for r in records)} source blocks rendered.')
