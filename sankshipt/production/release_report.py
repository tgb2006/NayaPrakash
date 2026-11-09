from pathlib import Path
import json,hashlib,collections,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'sankshipt/output/full_book/r01'
def j(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    html=j(OUT/'html-audit.json');pdf=j(OUT/'pdf-proof/pdf-qa.json');source=j(OUT/'source-manifest.json');pagination=j(OUT/'pagination.json')
    assert not html['problems'] and not html['browserErrors'] and pdf['passed']
    evidence=OUT/'qa-evidence';evidence.mkdir(exist_ok=True)
    copies={'chapter-semantic-coverage.json':'tmp/codex/full-book/chapters/semantic-coverage.json','chapter-dom-coverage.json':'tmp/codex/full-book/chapters/actual-dom-coverage.json','frontmatter-semantic-coverage.json':'tmp/codex/full-book/frontmatter/semantic-coverage.json','source-inventory.json':'tmp/codex/full-book/source-inventory/inventory.json'}
    for dest,src in copies.items():shutil.copy2(ROOT/src,evidence/dest)
    chapter_dom=j(evidence/'chapter-dom-coverage.json')
    counts=collections.Counter(p['type'] for p in html['pages']);spans=collections.Counter(p['key'] for p in html['pages'] if p['type']=='chapter');span_counts=collections.Counter(spans.values())
    editorial=j(ROOT/'tmp/codex/full-book/frontmatter/semantic-coverage.json')
    report=f'''# નય-ચક્ષુ — સંપૂર્ણ પુસ્તક QA અને ઉત્પાદન નોંધ

તારીખ: 06-11-2026 · Revision r01 · Project root: D:/PROJECT_WORK/NayaPrakash_Book.

## તૈયાર થયેલું પુસ્તક

એક static master HTML અને તે જ layoutમાંથી એક combined PDF તૈયાર છે. Title, compilerનું મંગલાચરણ, બંને પ્રસ્તાવના/પરિચય, generated અનુક્રમણિકા, પાંચ સામાન્ય પ્રકરણો, સાત ખંડ-પરિચય સાથે તમામ 225 પ્રકરણો અને પરિશિષ્ટ 00–08 સામેલ છે. Assets સ્થાનિક relative pathsથી load થાય છે. Source snapshots અને અગાઉના build proofs સુરક્ષિત છે.

| બાબત | પરિણામ |
|---|---|
| Canonical Markdown files | {len(source['sources'])}: 225 chapters +23 અન્ય files |
| કુલ પાનાં | {pdf['pages']} |
| દરેક PDF MediaBox | 468 × 684 pt =6.5 ×9.5 inch |
| DOM source blocks | {html['actualSourceBlocks']}/{html['expectedSourceBlocks']}; missing/duplicate/text mismatch 0 |
| મૂળ source order | PASS |
| Semantic charts | {html['semanticCharts']}:14 ASCII +2 Mermaid, actual HTML/CSS/SVG |
| Semantic table segments | {html['semanticTables']}; repeatedthead માત્ર pagination માટે |
| અલગ chapter images | {len(html['images'])}, બધાં mapped press assets |
| Browser overflow/errors | 0 |
| Final TOC page-number errors | {len(html['tocErrors'])} |
| PDF fonts | {len(pdf['fonts'])}; embedded અથવા self-contained Type3 |
| Independent PDF sample renders | {len(pdf['sample_renders'])}, બધા16 chart pages સહિત |
| Source inventory hash changes | {len(pdf['source_changes'])} |

## પસંદ કરેલી ડિઝાઇન

છેય ધારા headings17pt; subsection13pt; prose/table body11pt/1.38 justified, છેલ્લી line start-aligned. લક્ષણનું label “લક્ષણ સૂત્ર”. દર્શનધારા A: gray top/bottom, white middle pair, joined1–2–1, symmetricrules, dot વગર ૦૧–૦૪ hanging columns. અનેકાંત boxpadding1.8mm/2.5mm અને પાનથી વિવેક સુધી4.5mm gap જાળવ્યાં. Running headers નથી. Even-page footerમાં બહાર નંબર અને અંદર bookname/subtitle; odd-page footerમાં અંદર currentkhanda અને બહાર નંબર. Finalactualphysicalparity ચકાસી છે.

## Pagination અને વધારાનાં પાનાં

બે પાનાંનું original target દરેક લાંબા source માટે body11ptમાં શક્ય નહોતું. Source અથવા fonts ઘટાડ્યા નથી: {span_counts.get(2,0)} chapters બે પાનાં અને {span_counts.get(4,0)} chapters ચાર balanced continuation પાનાંમાં છે. તમામ225 chapter starts even અને spans even/contiguous છે. Chapter matter {counts['chapter']} pages છે. બાકીનાં pages: {json.dumps({k:v for k,v in counts.items() if k!='chapter'},ensure_ascii=False)}.

ખંડ transition માટે બે intentional reading-guide pages છે. પાંચ intro endingsમાં existing last-three pagesની content balance સુધારેલી છે; blank filler નથી. Continuation pagesમાં semantic blocksનો મૂળ ક્રમ જાળવ્યો છે. Longtitlesને જરૂર મુજબ24/22pt અને ચિત્રને28mm સુધી ગોઠવ્યાં; body11pt છે. બધા chapter layoutsને કાપીને બે પાનાંમાં ફિટ કર્યાં હોવાનો દાવો નથી.

## સ્વતંત્ર source અને PDF QA

- Chapter source-to-render lexical audit:225/225;158,029 tokens અને3,768 ordered prose/list/verse sequences. Actual serialized chapter DOMનું પણ સ્વતંત્ર audit થયું છે; માત્ર inputJSON/IDsનો pass નથી.
- Nonchapter audit:23/23 filesનાં words/counts/chartlabels/tablecells જાળવ્યાં. Sourceમાંના tableheadersને auditમાં એક જ વખત ગણ્યાં; final repeatedheaders વાંચનની સગવડ માટે છે.
- PDF: તમામ પાનાંનું માપ અને extractable nonblank text, fonts/Type3, image placements/effective DPI અને resource pixels તપાસ્યાં. 50 sample pagesમાં title/last, openings, paired parity, long/dense ends, charts અને appendices તપાસ્યાં.
- Sourceના રંગીન emojiના presentationને monochrome vector symbolsમાં ફેરવ્યું છે. મૂળ Unicode `data-original-symbol`/accessible labelમાં જાળવ્યું છે; source-text audit તેને reconstruct કરે છે. આખાં textpages rasterize કર્યાં નથી.
- જૂના sourceમાંના203/જૂના ખંડ-count સંદર્ભો મૂળરૂપે જાળવ્યા છે. મૂળ doctrine/sourcewordsમાં silent rewrite નથી.
- K02_C003/K02_C008માં Sanskrit સૂત્રના બદલે આપેલી લેખકૃત Gujarati વ્યાખ્યાને attributionસાથે જાળવી છે; નવું શાસ્ત્રીય સૂત્ર ગઢ્યું નથી.

## અલગ verification statuses

| સ્થિતિ | નોંધ |
|---|---|
| HTML audit | PASS: બધા sources/blocks/order, images, geometry, contents અને footer parity |
| PDF proof | PASS: independent structural/font/image/render checks |
| Human design/source proof | બાકી; વપરાશકર્તાની સૂચના મુજબ gate વગર કામ પૂર્ણ કર્યું |
| Press certification | બાકી: printer bleed/ICC/PDF-X specifications આપેલ નથી; આ trim-size grayscale proof છે |

Sourceમાંની ઐતિહાસિક સંખ્યાઓ/તાર્કિક સંપાદનની માનવીય સમીક્ષા publication પહેલાં ઉપયોગી રહેશે. આ report pass એટલે printer-certified PDF/X નથી.

## મુખ્ય review links

- [પૂર્ણ HTML](naya_chakshu_book.html)
- [પૂર્ણ PDF](naya_chakshu_book.pdf)
- [PDF proof gallery](pdf-proof/index.html)
- [Source manifest](source-manifest.json)
- [HTML audit](html-audit.json)
- [PDF audit](pdf-proof/pdf-qa.json)
- [Pagination map](pagination.json)
- [Production plan](PRODUCTION_PLAN.md)

## Hash receipt

```text
HTML SHA256 {sha(OUT/'naya_chakshu_book.html')}
PDF SHA256  {sha(OUT/'naya_chakshu_book.pdf')}
```

ચોક્કસ retained files/hashes [artifact-manifest.json](artifact-manifest.json)માં છે. Source originals અને approvedpilot બદલ્યા નથી. Tools `sankshipt/production/`માં છે; [rebuild સૂચનાઓ](../../../production/README.md)માં commands આપેલ છે.
'''
    (OUT/'QA_REPORT.md').write_text(report,encoding='utf-8')
    cards=''.join(f'<a href="page-{r["page"]:04d}.png"><figure><img loading="lazy" src="page-{r["page"]:04d}.png" alt="PDF page {r["page"]}"><figcaption>Page {r["page"]} · grayscale Δ {r["max_channel_difference"]}</figcaption></figure></a>' for r in pdf['sample_renders'])
    gallery='<!doctype html><html><head><meta charset="utf-8"><title>નય-ચક્ષુ PDF proof</title><style>body{font:16px sans-serif;margin:28px;background:#e8e8e8;color:#222}h1{font-size:25px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}a{color:inherit;text-decoration:none}figure{margin:0;padding:12px;background:white}img{display:block;width:100%;height:auto}figcaption{padding-top:10px}</style></head><body><h1>નય-ચક્ષુ · independent PDF proof</h1><p><a href="../naya_chakshu_book.html">Master HTML</a> · <a href="../naya_chakshu_book.pdf">Full PDF</a> · <a href="../QA_REPORT.md">QA report</a></p><div class="grid">'+cards+'</div></body></html>'
    (OUT/'pdf-proof/index.html').write_text(gallery,encoding='utf-8')
    artifacts=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file() and p.name!='artifact-manifest.json':artifacts.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    tools=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}for p in sorted((ROOT/'sankshipt/production').glob('*'))if p.is_file()]
    (OUT/'artifact-manifest.json').write_text(json.dumps({'root':str(ROOT),'artifacts':artifacts,'production_tools':tools},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pages':pdf['pages'],'artifacts':len(artifacts),'pdf_pass':pdf['passed'],'report':str(OUT/'QA_REPORT.md')},ensure_ascii=False))
if __name__=='__main__':main()
