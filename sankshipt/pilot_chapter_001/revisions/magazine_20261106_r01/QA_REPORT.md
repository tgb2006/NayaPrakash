# Magazine pilot — HTML review QA

તારીખ: 06-11-2026 · આવૃત્તિ: magazine_20261106_r01

## પરિણામ

માગેલી `chapter_001.html`માં magazine design લાગુ છે. બે સામસામે portrait પાનાં, મોટા Gujarati headlines, તત્ત્વધારાના ચાર ક્રમબદ્ધ full-width blocks, કાવ્ય/સાધના panel, mapped કથા-ચિત્ર, વિવેક comparison અને દર્શનધારાના ચાર મુદ્દા ગોઠવ્યા છે. સમાન ઊંચાઈની ખાલી cards, abstract placeholder અને text hide કરતી overflow પદ્ધતિ દૂર કરી છે.

## ચકાસણી

- Chromium screen અને print mediaમાં render કર્યું; બંનેના screenshots જોયા.
- દરેક page canvas: **165.1 × 241.3 mm = 6.5 × 9.5 inches**; `@page` margins 0.
- મૂળ outputમાંથી 26 title/subtitle/prose/example/verse blocks: **26/26 text match**, યોગ્ય ક્રમ, duplicate ID નહીં. Markdown formatting દૂર કરીને whitespace normalize કરી સરખાવ્યું છે; શબ્દો ટૂંકાવ્યા નથી. Section labels અને સૂત્ર પણ source પ્રમાણે મૂક્યાં છે; manifest આખા Markdown fileનો byte-for-byte HTML દાવો નથી.
- મુખ્ય body **11 pt**, line-height **1.38**. Body ઘટાડ્યા વિના layout fit કર્યું.
- **0 overflowing containers, 0 text/image collisions, 0 text/footer collisions, 0 browser errors**.
- Contentનો અંત: ડાબે 220.82 mm, જમણે 220.65 mm; footer rule શરૂ 224.42 mm. બંને વચ્ચે લગભગ 3.6–3.8 mm clear gap.
- ઉપયોગમાં આવતા Gujarati અને Devanagari fonts load થયા. URLs project-relative છે. Unused Devanagari bold face browserમાં unloaded છે; વર્તમાન textમાં તેની જરૂર નથી. English માટે સામાન્ય serif fallback છે, dedicated English font file ઉમેરેલી નથી.
- એક chapter-specific image: **K01_C001**, **1254 × 1254 px**, **38 × 38 mm** placement, લગભગ **838 effective DPI**; square aspect અને આખું ચિત્ર જાળવ્યું છે. કોઈ નવી image generation કે image pixel editing નથી.
- મૂળ source, image assets અને જૂના PDFમાં ફેરફાર નથી.

## Review બાકી

- માનવીય graphic-design અને Gujarati proof review બાકી છે.
- Printed folios ૨–૩ final bookની spread position બતાવે છે. Standalone HTMLના પ્રથમ/બીજા page સામે આ numbers physical PDF parityનો પુરાવો નથી; final assembled bookમાં offset પ્રમાણે તપાસવું.
- **હાલનું `chapter_001.pdf` જૂની designનું છે. નવી HTMLનું PDF આ તબક્કે બનાવેલું નથી.** HTML review પછી અલગ PDF proof અને font embedding, MediaBox, actual parity, blank-page તથા grayscale ચકાસણી કરવી.
- Printer bleed, ICC અથવા PDF/X press certification બાકી. Browser auditને press approval ગણવું નહીં.

## Files

બધા નીચેના paths `D:/PROJECT_WORK/NayaPrakash_Book/`થી શરૂ થાય છે.

| Path | સ્થિતિ |
|---|---|
| `sankshipt/pilot_chapter_001/chapter_001.html` | સુધારેલું મુખ્ય review HTML |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/chapter_001.html` | relative asset paths ગોઠવેલી સુરક્ષિત revision |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/before_chapter_001.html` | જૂનું HTML backup |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/before_chapter_001.pdf` | જૂનું PDF backup |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/spread-preview.png` | બે પાનાંનો screen preview |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/page-2-preview.png` | ડાબું print-media page preview |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/page-3-preview.png` | જમણું print-media page preview |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/html-audit.json` | DOM અને asset checks |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/source-manifest.json` | source block comparison આધાર |
| `sankshipt/pilot_chapter_001/revisions/magazine_20261106_r01/QA_REPORT.md` | આ review report |

Task-owned temporary files: `tmp/codex/magazine-pilot-r01/build.py`, `audit.cjs`, `package.py`, `source-manifest.json`, `audit.json`, `spread.png`, `page-1.png`, `page-2.png`. અગાઉનું design plan અને જૂનો root QA report યથાવત્ છે; આ report નવી HTML માટે લાગુ પડે છે.

## Hash receipt

```text
Current HTML SHA256 62bfe72a603328e08a48ec053235ee8d69a95681c74a41b5d013e38aded56b27
Source SHA256       ea00e145ab7d210acc4ad84c54b0c321c41a386d775eb141a165c0f3a742918b
Preserved PDF SHA256 b8b635f9d5de1124a12ca3b3ae759cfc3a96e9d8030cfeea82323438e9bbca8c
```
