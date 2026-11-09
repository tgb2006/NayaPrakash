# સંપૂર્ણ નય-ચક્ષુ HTML/PDF production

આ tools current `sankshipt/output`ના મૂળ લખાણ અને `Image/chapter-image-map.json`થી એક master HTML તથા એક combined PDF બનાવે છે. Pilot originals બદલાતા નથી. [ડિઝાઇન નિયમો](../design/DESIGN_RULES.md) અને [checklist](../design/PRODUCTION_CHECKLIST.md) લાગુ છે.

## મુખ્ય files

- `build_book.py`: 225 chapter sources અને 23 અન્ય sources, current fonts/imagesની local copies, source snapshots/manifest અને browser-build input.
- `chapter_renderer.py`: દરેક chapterનું source-preserving semantic parsing.
- `frontmatter_renderer.py`: prose, verse, semantic tables તથા 14 ASCII +2 Mermaid chartsનું HTML rendering.
- `chapter_paginate.js`: browserમાં માપેલું fit. દરેક પ્રકરણ માટે બરાબર બે સામસામે પાનાં અને 11 pt body.
- `paginate.js`: સમગ્ર પુસ્તકનો ક્રમ, nonchapter measured flow, source/table-row preservation, actual even/odd footers અને regenerated contents.
- `book.css`: page canvas, title, frontmatter, contents, footer અને shared production CSS.
- `polish_book.cjs`: existing page count/order જાળવી title/mંગલાચરણ composition અને sparse khanda endingsનું source-preserving balancing.
- `khanda_intro_layout.cjs`: `Image/khanda-intro/placements.json` મુજબ પહેલાં પાને અલગ ચિત્ર મૂકે છે અને ખંડ પરિચયનું મૂળ લખાણ તથા ચાર્ટ ચાર પાનાંમાં ફરી ગોઠવે છે. Static HTML પર એકવાર ચલાવવું અને પછી HTML audit ચલાવવો.
- `general_chapter_layout.cjs`: પ્રકરણ ૦થી ૫નાં મથાળાં, ક્રમાંક, બુલેટ અને પ્રકરણ ૩ના કોષ્ટકને મેગેઝીન શૈલી આપે છે. મથાળું, ટૂંકી પ્રસ્તાવના અને શરૂઆતની સમજાવટને શક્ય હોય ત્યાં એક જ પાને રાખે છે. ફરી પેજિંગ કર્યા પછી મોટી ખાલી જગ્યા હોય ત્યાં `Image/general-chapters`માંથી વિષયસંગત ચિત્ર ફિટ તથા ૩૦૦ DPI માપીને મૂકે છે. Static HTML પર ચલાવ્યા પછી HTML audit ચલાવવો.
- `export_book.cjs`: fonts/images ready પછી browser source/geometry audit, static master serialization, previews અને Chromium PDF.
- `verse_layout.cjs`: Static HTMLમાં સૂત્રના અર્થપૂર્ણ દંડ-વિરામે પંક્તિ ગોઠવે છે. કાવ્યની મૂળ પંક્તિ તૂટે તો ફૂટર અને સાધનાધારાનું ફિટ ચકાસીને તેની કોલમ પહોળી કરે છે. `verse-layout-audit.json`માં તપાસ નોંધાય છે.
- `appendix_layout.cjs`: પરિશિષ્ટના શીર્ષકો, ક્રમાંક, બુલેટ, વિષય પ્રમાણે પહોળાઈવાળા કોષ્ટકો અને HTML ઇન્ફોગ્રાફિક ગોઠવે છે. જ્યાં ઓછા સ્પેસિંગથી પાનું બચે ત્યાં ચુસ્ત ગોઠવણી વાપરે છે અને ફરી પેજ કર્યા પછી અનુક્રમણિકા અને ફૂટર સુધારે છે.
- `sajay_appendix.cjs`: તૈયાર Static HTMLમાંથી ૨૨૫ મૂળ કાવ્યધારા અને પ્રકરણ ક્રમ ચકાસીને બે કોલમમાં પરિશિષ્ટ ૯ ઉમેરે છે. પરિશિષ્ટની રૂપરેખા અને અનુક્રમણિકા પણ સુધારે છે. `appendix_layout.cjs` પછી એક વાર ચલાવવું.
- `paired_example_layout.cjs`: ચિત્રવાળાં તત્ત્વધારા પાનાંમાં મુદ્દા ૦૩ અને ૦૪ને એક જ લખાણ-કોલમમાં અને ચિત્રને અલગ કોલમમાં ગોઠવે છે. ચિત્ર ઉમેરાયા પછી ચલાવી બંને મુદ્દાની જમણી ધાર, ચિત્ર અને ફૂટરની જગ્યા ચકાસવી.
- `tattva_panorama_layout.cjs`: ઉપરની ગોઠવણી પછી `Image/tattva-panoramas`માં પ્રકરણ ID પ્રમાણે રહેલા ગ્રેસ્કેલ રૂપકચિત્રને ૦૪ અને કાવ્યધારા વચ્ચેની માપેલી પહોળાઈ અને ઊંચાઈમાં મૂકે છે. `--measure-only` ચિત્ર બનાવતાં પહેલાં પ્રમાણ આપે છે. `tattva-panorama-audit.json`માં પાનું, ફાઇલ, માપ અને DPI નોંધાય છે.
- `monochrome_symbols.cjs`: મૂળ Unicode માહિતી જાળવી decorative color emojiને vector monochrome ચિહ્નોમાં બતાવે છે; આખાં પાનાંને rasterize કરતું grayscale filter વાપરતું નથી.
- `pdf_qa.py`: independent PDF MediaBox, count, fonts, image placements/DPI અને rendered samples.

## Rebuild

Project rootમાંથી commands ચલાવો. New release માટે નવું output revision વાપરો; approved artifact ઉપર overwrite ન કરો. Transient profiles/logs project `tmp/codex` અથવા system tempમાં જ રાખો.

```powershell
python sankshipt/production/build_book.py --out sankshipt/output/full_book/r02
node sankshipt/production/export_book.cjs sankshipt/output/full_book/r02 --no-pdf
node sankshipt/production/polish_book.cjs sankshipt/output/full_book/r02
node sankshipt/production/export_book.cjs sankshipt/output/full_book/r02 --static --no-pdf
node sankshipt/production/monochrome_symbols.cjs sankshipt/output/full_book/r02
node sankshipt/production/general_chapter_layout.cjs sankshipt/output/full_book/r02
node sankshipt/production/verse_layout.cjs sankshipt/output/full_book/r02
node sankshipt/production/appendix_layout.cjs sankshipt/output/full_book/r02
node sankshipt/production/export_book.cjs sankshipt/output/full_book/r02 --static --no-pdf
# Rendered HTML inspection પછી:
node sankshipt/production/export_book.cjs sankshipt/output/full_book/r02 --static
python sankshipt/production/pdf_qa.py --pdf sankshipt/output/full_book/r02/naya_chakshu_book.pdf --out sankshipt/output/full_book/r02/pdf-proof --expected-pages ACTUAL_COUNT --sample-pages FIRST LAST CHART_PAGES
```

Bundled environmentમાં Python, Playwright/Chromium, pypdf, Pillow અને Poppler જોઈએ. `PLAYWRIGHT_MODULE` અને `CHROME_PATH` environment overrides Node scriptsમાં આપી શકાય છે. Final HTMLમાં local relative font/image URLs છે; `assets` folder સાથે રાખવો. Build સમયે original pilot font assets અને system-installed Noto Serifમાંથી copies લેવામાં આવે છે; release assets portable છે.

`--no-pdf` audit/build છે. `--static` પહેલેથી paginated static master પરથી audit/export કરે છે; તેથી PDF એ જ HTMLની layout proof રહે છે. HTML audit fail થાય તો exporter PDF બનાવતો નથી. માત્ર IDs નહીં, actual block text અને order પણ સરખાવે છે.

## Status અને મર્યાદા

દરેક પ્રકરણ બરાબર બે સામસામે પાનાં અને દરેક ખંડ પ્રવેશ બરાબર ચાર પાનાં. બનાવતી વખતે અને PDF export પહેલાં આ બંને ગણતરી ચકાસાય છે. નિષ્ફળ વિભાગનો key તપાસીને પાનાની ગોઠવણી ફરી માપવી.

r02માં પ્રકરણોનું 11 pt મુખ્ય લખાણ 1.16 પંક્તિ અંતરે ગોઠવ્યું છે. બાઇન્ડિંગ તરફ 10 mm અને બહાર 8 mm માર્જિન છે. ડાબા પાનાંનું ઉપરનું માર્જિન 10 mm અને જમણા પાનાંનું 9 mm છે. કથાચિત્ર 23 mm છે. વિવેકધારા અને દર્શનધારાના કોષોનું અંતર અને અંદરની જગ્યા વધુ સઘન છે. સપ્તમ ખંડ પ્રવેશનો ચાર્ટ ચાર સમાંતર કોલમમાં છે.

સંપાદન માટે બે શરતો સાથે સાચી હોવી જોઈએ: વિભાગ પોતાના પાનામાં ફિટ થતો નથી અને વિભાગ પોતાની દસ્તાવેજિત શબ્દમર્યાદા વટાવે છે. બંને સાચી હોય ત્યાં અર્થ, દૃષ્ટાંત અને સમજાવટ જાળવીને જરૂરી એટલું ટૂંકાવવું. એકાંત અને અનેકાંતને એક-એક વાક્યમાં સમેટવા નહીં. મર્યાદામાં રહેલા સમજાવટના વિભાગનું મૂળ લખાણ રાખવું. શબ્દમર્યાદા અને fit અલગ તપાસો છે.

HTML source/geometry audit, independent PDF proof, માનવીય design proof અને printer certification અલગ છે. આ runમાં વપરાશકર્તાએ human gates વિના પૂર્ણ કરવાનું કહ્યું છે; human/press review status નોંધાય છે, production અટકાવતું gate નથી. Bleed/ICC/PDF-X specification વગર trim proofને press-certified ન કહેવું.
