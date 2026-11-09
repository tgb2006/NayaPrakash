"""Build the full current-source book; browser performs measured pagination."""
from pathlib import Path
import json,hashlib,re,shutil,html,argparse
from chapter_renderer import load_chapters,render_chapter,chapter_css,KHANDAS
from frontmatter_renderer import render_file,CSS as FRONT_CSS
from gujarati_spelling import publication_paths,require_clean

ROOT=Path(__file__).resolve().parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    require_clean(publication_paths())
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='sankshipt/output/full_book/r01');a=ap.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
    assets=out/'assets';fonts=assets/'fonts';fonts.mkdir(parents=True,exist_ok=True)
    for p in (ROOT/'sankshipt/pilot_chapter_001/assets/fonts').glob('*.ttf'):shutil.copy2(p,fonts/p.name)
    for src,name in [('C:/Windows/Fonts/NotoSerif-Regular.ttf','BookSerif-Regular.ttf'),('C:/Windows/Fonts/NotoSerif-Bold.ttf','BookSerif-Bold.ttf')]:shutil.copy2(src,fonts/name)
    frontmatter_images=assets/'images'
    frontmatter_images.mkdir(exist_ok=True)
    for name in ('opening-poems-flower.png','magazine-botanical-grayscale.png'):
        shutil.copy2(Path(__file__).parent/'assets'/name,frontmatter_images/name)
    chapters=load_chapters(ROOT);chapter_records=[];manifest=[];sources=[]
    for c in chapters:
        record=render_chapter(c);src=ROOT/c.mapping['html_src'];dest=assets/'images'/Path(c.mapping['html_src']).name;dest.parent.mkdir(exist_ok=True);shutil.copy2(src,dest)
        old=record['metadata']['image_src'];new='assets/images/'+dest.name
        for field in ['left','right']:record[field]=record[field].replace(old,new)
        for field in ['left_components','right_components']:record[field]=[x.replace(old,new) for x in record[field]]
        record['metadata']['image_src']=new
        chapter_records.append(record);manifest.extend(record['manifest']);sources.append({'path':c.source_file,'sha256':c.source_sha256,'type':'chapter','key':c.key})
    documents=[]
    paths=[]
    paths+=sorted((ROOT/'sankshipt/output/preface').glob('*.md'))
    paths+=sorted((ROOT/'sankshipt/output/samanya_prakaran').glob('*.md'))
    for k in range(1,8):paths+=sorted((ROOT/'sankshipt/output').glob(f'khanda_{k}_*/000_*.md'))
    paths+=sorted((ROOT/'sankshipt/output/parishishta').glob('*.md'))
    for i,p in enumerate(paths):
        rel=p.relative_to(ROOT).as_posix();key='D'+str(i+1).zfill(3);r=render_file(p,key);first=next((b['text'] for b in r['blocks'] if b['kind']=='heading'),p.stem)
        typ='preface' if '/preface/' in rel else 'general' if '/samanya_prakaran/' in rel else 'appendix' if '/parishishta/' in rel else 'khanda_intro'
        k=int(re.search(r'khanda_(\d)',rel).group(1)) if typ=='khanda_intro' else None
        for b in r['blocks']:b['source_file']=rel
        for b in r['manifest']:b['source_file']=rel
        doc={'key':key,'source_file':rel,'title':first,'type':typ,'khanda':k,'blocks':r['blocks'],'manifest':r['manifest'],'chart_count':r['chart_count']}
        documents.append(doc);manifest.extend(r['manifest']);sources.append({'path':rel,'sha256':digest(p),'type':typ,'key':key})
    sequence=[]
    sequence += [d for d in documents if d['type']=='preface']
    sequence += [{'type':'toc','key':'CONTENTS','title':'અનુક્રમણિકા'}]
    sequence += [d for d in documents if d['type']=='general']
    for k in range(1,8):
        sequence += [d for d in documents if d['type']=='khanda_intro' and d['khanda']==k]
        sequence += [{'type':'chapter','key':r['metadata']['key'],'record':r,'title':r['metadata']['source_title'],'khanda':k} for r in chapter_records if r['metadata']['khanda']==k]
    sequence += [d for d in documents if d['type']=='appendix']
    toc=[{'key':d['key'],'title':d['title'],'type':d['type'],'khanda':d.get('khanda')} for d in sequence if d['type']!='toc']
    manifest=[b for item in sequence if item['type']!='toc' for b in (item['record']['manifest'] if item['type']=='chapter' else item['manifest'])]
    for record in sources:
        original=ROOT/record['path']
        if digest(original)!=record['sha256']:raise RuntimeError('Source changed while assembling: '+record['path'])
        snapshot=out/'source_snapshot'/Path(record['path']).relative_to('sankshipt/output')
        snapshot.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,snapshot)
    payload={'sequence':sequence,'toc':toc,'khanda':KHANDAS,'manifest':manifest,'sources':sources,'book_title':'નય-ચક્ષુ','book_subtitle':'નયનું જ્ઞાન, સંશયનું સમાધાન'}
    fontcss=''
    for family,prefix,weights in [('Anek Gujarati','AnekGujarati',[(400,'Regular'),(600,'SemiBold'),(700,'Bold'),(800,'ExtraBold')]),('Noto Sans Gujarati','NotoSansGujarati',[(400,'Regular'),(700,'Bold')]),('Noto Sans Devanagari','NotoSansDevanagari',[(400,'Regular'),(700,'Bold')]),('Book Serif','BookSerif',[(400,'Regular'),(700,'Bold')])]:
        for weight,suffix in weights:fontcss+=f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:normal;src:url('assets/fonts/{prefix}-{suffix}.ttf') format('truetype');font-display:block}}\n"
    css=(Path(__file__).parent/'book.css').read_text(encoding='utf-8')
    scripts=(Path(__file__).parent/'chapter_paginate.js').read_text(encoding='utf-8')+'\n'+(Path(__file__).parent/'paginate.js').read_text(encoding='utf-8')
    doc='<!doctype html><html lang="gu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>નય-ચક્ષુ — સંપૂર્ણ ગ્રંથ</title><style>'+fontcss+css+FRONT_CSS+chapter_css()+'</style></head><body><div class="review-toolbar"><b>નય-ચક્ષુ</b><span id="build-status">પાનાં ગોઠવાઈ રહ્યાં છે…</span><button onclick="window.print()">Print / Save PDF</button></div><main id="book"></main><script id="book-data" type="application/json">'+json.dumps(payload,ensure_ascii=False).replace('</','<\/')+'</script><script id="build-script">'+scripts+'</script></body></html>'
    (out/'book.build.html').write_text(doc,encoding='utf-8')
    (out/'source-manifest.json').write_text(json.dumps({'sources':sources,'blocks':manifest,'counts':{'sources':len(sources),'chapters':len(chapters),'nonchapter_sources':len(documents),'blocks':len(manifest),'charts':sum(d['chart_count'] for d in documents)}},ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'assembly-plan.json').write_text(json.dumps(toc,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'out':str(out),'chapters':len(chapters),'sources':len(sources),'blocks':len(manifest)},ensure_ascii=False))
if __name__=='__main__':main()
