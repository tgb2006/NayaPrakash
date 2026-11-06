# નય પ્રકાશ — પાઈલોટ પરથી પુસ્તકની ડિઝાઇન યોજના

તારીખ: 06-11-2026 · આવૃત્તિ: r01

સ્થિતિ: વર્તમાન HTMLના કોડ અને તેમાંથી બનેલા PDFનું અવલોકન કરીને તૈયાર કરેલી યોજના. આ નોંધ ડિઝાઇનની માનવીય મંજૂરી કે press certification નથી. આ કામમાં મૂળ HTML/PDFમાં ફેરફાર કરેલો નથી.

## 1. કાર્યક્ષેત્ર અને આધાર

- કાર્યસ્થળ અને પ્રાથમિક project root: `D:\PROJECT_WORK\NayaPrakash_Book`.
- જોવામાં આવેલ HTML: `sankshipt/pilot_chapter_001/chapter_001.html`.
- જોવામાં આવેલ PDF: `sankshipt/pilot_chapter_001/chapter_001.pdf`.
- લખાણ માટેનો આધાર: `sankshipt/output/khanda_1_naigam/chapter_001_bhuta_naigam_naya_gu.md` અને પછી દરેક પ્રકરણની અનુરૂપ મૂળ output file.
- ચિત્ર માટેનો આધાર: `Image/chapter-image-map.json` અને તેના `Image/press/`માં દર્શાવેલા assets.
- વપરાશકર્તાએ નક્કી કરેલું છેલ્લું માપ **6.5 × 9.5 ઇંચ** છે. અગાઉની 8 × 8 ઇંચની સૂચના તેના પર લાગુ પડતી નથી.
- અગાઉ આપેલી Antigravity paging/design નોંધ ઐતિહાસિક reference છે. તેની જૂની square-page/sidebar ગોઠવણી આપમેળે પાછી લાદવાની નથી. આગળના pilot માટે હાલ આપેલા HTML/PDFની રચના આધાર રહેશે; જરૂરી ફેરફારો reviewમાં દેખાડવાના રહેશે.

## 2. હાલ કોડમાં શું છે અને PDFમાં શું મળ્યું

| ભાગ | હાલની રચના / ચકાસણી |
|---|---|
| પાનું | બે નિશ્ચિત 6.5 × 9.5 ઇંચના `.page`; PDFમાં બંને 468 × 684 pt |
| Screen / print | Screen પર સામસામે flex spread; printમાં અલગ પાનાં; `@page` margin 0 |
| Margins | ઉપર/નીચે 11.5 mm; અંદરની બાજુ 14 mm, બહારની બાજુ 12.5 mm; બંને પાને mirror |
| ડાબું પાનું | Masthead, સૂત્ર, તત્ત્વધારાના ચાર 2 × 2 cards, નીચે કાવ્યધારા અને સાધનાધારા |
| જમણું પાનું | કથાધારા: ચિત્ર સાથે પિપાસા, પછી પાન; વિવેકધારાની બે cards; નીચે દર્શનધારાના ચાર મુદ્દા |
| મુખ્ય ફોન્ટ | Anek Gujarati headings અને Noto Sans Gujarati body; body મોટાભાગે 11 pt |
| નાના લખાણવાળા ભાગ | સાધના/વિવેક લગભગ 10.6 pt, દર્શન 10.2 pt; આગળ વાંચનક્ષમતા સરખી કરવાની જરૂર |
| Card height | સરખી ઊંચાઈની બે rows અને `flex: 1`; દરેક card લગભગ 67.89 × 76.64 mm |
| ચિત્ર | હાલ 115 × 78 ptનું inline abstract SVG; તૈયાર square chapter clipart જોડાયેલું નથી |
| પાનાંક્રમ | લખેલા અંક ૨ અને ૩ છે; standalone PDFમાં વાસ્તવિક સ્થાનો 1 અને 2 છે |
| Automation | Standalone hardcoded HTML; measured pagination, paragraph coverage comparison અથવા chapter data renderer નથી |

Fonts load થયા પછી print layoutનું માપ લીધું છે અને PDFનાં બંને પાનાં render કરીને જોયાં છે. વર્તમાન pilotમાં માપેલા text containersમાં clipping અથવા paragraph/footer overlap મળ્યાં નથી. આ નિષ્કર્ષ આ પ્રકરણ સુધી મર્યાદિત છે.

તત્ત્વધારા cardsમાં લખાણ પછી લગભગ **22–28 mm** ખાલી રહે છે. વિવેકધારા અને દર્શનધારા વચ્ચે લગભગ **34.22 mm** અંતર રહે છે. તેનું મુખ્ય કારણ સમાન ઊંચાઈવાળી rows અને દર્શનધારાનું `margin-top: auto` છે. આ જગ્યા content પ્રમાણે ફરી ગોઠવવાની છે.

## 3. લખાણની અખંડિતતા પહેલાં સુધારવાની છે

હાલનું pilot મૂળ outputનું શબ્દશઃ પ્રતિનિધિત્વ કરતું નથી. ઉદાહરણ તરીકે કથાની શરૂઆતમાં મૂળનું “પુત્ર આનંદની વ્યાપારિક ભૂલથી પેઢીને મોટું નુકસાન…” pilotમાં અલગ વાક્યોમાં લખાયું છે. મર્મ અને કેટલાક ઉદાહરણોમાં પણ વધઘટ છે; એક label “બીજ અને બરફ”થી “બીજ અને જળ” થયું છે.

આથી visual layout ફરી વાપરીશું, પરંતુ પ્રકરણનું લખાણ મૂળ outputમાંથી જ લઈશું. જગ્યા માટે શબ્દો ઘટાડવા, અર્થ બદલીને ટૂંકાવવું કે નવા વાક્યો ઉમેરવા નહીં. દરેક paragraph, verse અને list itemને સ્થિર ID આપીને તેની હાજરી, ક્રમ અને મૂળ text સાથે સરખામણી કરવી. માત્ર IDs હાજર હોવાને સંપૂર્ણ source coverage ગણવું નહીં.

## 4. બે સામસામે પાનાંની પ્રસ્તાવિત ગોઠવણી

```text
ડાબું પાનું                         જમણું પાનું
ખંડ / પ્રકરણ masthead               કથાધારા heading
ગુજરાતી શીર્ષક, અલગ English subtext  square ચિત્ર + પિપાસા
સૂત્ર                               પાન
તત્ત્વધારા ૧ / ૨                    વિવેકધારા: એકાંત / અનેકાંત
તત્ત્વધારા ૩ / ૪                    દર્શનધારા: ચાર મુદ્દા
કાવ્યધારા / સાધનાધારા               
બહાર page number + અંદર footer      અંદર footer + બહાર page number
```

આ hierarchy જાળવીશું. સાધનાધારા અને દર્શનધારા updated sourceના ભાગ છે, તેથી તેમને છોડવાના નથી. મુખ્ય title એક જ વખત દેખાશે. લાંબા ગુજરાતી શીર્ષક અને English subtext અલગ linesમાં રહેશે.

### જગ્યા અને typography

1. પહેલા મૂળ લખાણથી pilot ફરી ભરવો; પછી જ વાસ્તવિક ઊંચાઈ પ્રમાણે ગોઠવણી નક્કી કરવી.
2. ચાર તત્ત્વ blocksનો ક્રમ જાળવવો. 2 × 2 cards જ્યાં વાંચનક્ષમ હોય ત્યાં રાખવા; લાંબા blocks માટે content પ્રમાણે row height અથવા ઊભી ગોઠવણી review કરવી.
3. સમાન card height માટેનું અનાવશ્યક stretch અને દર્શનધારાનું મોટું automatic gap દૂર કરવાની દિશામાં સુધારો કરવો. પાનાંના નીચલા ભાગોને headers/footersથી સુરક્ષિત અંતરે રાખવા.
4. Bodyનો આધાર લગભગ **11 pt / 1.38 line-height**, paragraph gap લગભગ 6.5 pt રાખીને માપવું. નાના auxiliary લખાણને પણ વાંચનક્ષમ રાખવું; જગ્યા માટે body shrink ન કરવું.
5. હાલનું મુખ્ય heading 19.5 pt છે. નવા portrait માપમાં તેનો કદ, line breaks અને સ્થાન pilot reviewથી નક્કી કરવાં; જૂના square-page headingનું માપ અંધપણે લાગુ ન કરવું.
6. સૂત્રમાં હાલ `nowrap`, ellipsis અને hidden overflow છે. લાંબા સૂત્રને સંપૂર્ણ બતાવવા wrap અને reserve space આપવાં. Text-containing `.page` અને cardsના `overflow: hidden`ને fitનો પુરાવો ગણવો નહીં.
7. કાળો અને neutral gray palette રાખવો. રંગછાંટવાળા gray valuesને neutral કરવા અને છાપેલા કદે contrast તપાસવું.

### ચિત્રનું સ્થાન

- પ્રકરણની કથાધારા આધારિત તૈયાર ચિત્ર જ વાપરવું; હાલના abstract SVGને તેનાથી બદલવું.
- પ્રથમ પ્રકરણનું mapping key: **K01_C001**.
- Asset: `Image/press/K01_C001_chapter_001_bhuta_naigam_naya_katha_r01_press.png`.
- હાલના pilot folderમાંથી relative HTML path: `../../Image/press/K01_C001_chapter_001_bhuta_naigam_naya_katha_r01_press.png`.
- પ્રારંભિક placement લગભગ **45–50 mm square**, પછી મૂળ કથાના text fit સામે માપવું. `contain`થી સંપૂર્ણ ચિત્ર રાખવું; ચહેરો, હાથ કે મુખ્ય વસ્તુ crop ન કરવી.
- આ asset 1254 × 1254 px છે; 50 mm placement પર લગભગ 637 effective DPI મળે છે. DPI metadataને એકમાત્ર ગુણવત્તાનો પુરાવો ગણવો નહીં; printed size પર રેખા અને contrast પણ જોવાં.
- Mapping documentમાંથી filename લેવું; file નામ અનુમાનથી બનાવવું નહીં. બીજા પ્રકરણનું ચિત્ર ફરી વાપરવું નહીં. હાલના image originals સુરક્ષિત રાખવા.

### Fonts અને portability

હાલ projectના fonts માટે absolute `file:///D:/...` paths છે. આગળ relative project asset paths વાપરવા. Gujaratiના ચોક્કસ weights જાહેર કરવા. Sanskrit માટે local Devanagari fontનું સ્પષ્ટ `@font-face` આપવું. Englishમાં જાહેર કરેલું Cinzel load થતું નથી અને PDFમાં Times New Roman fallback આવ્યું છે; ઇચ્છિત સ્થાનિક English font પસંદ કરીને સ્પષ્ટ કરવું.

વર્તમાન PDFમાં Gujarati અને Devanagari font programs embedded છે. મળેલા Type3 symbol fonts પોતાના CharProcs ધરાવે છે; તેમને ફક્ત FontDescriptorના અભાવથી missing font ન ગણવા. નવી આવૃત્તિમાં પણ PDF font embedding સ્વતંત્ર રીતે તપાસવું.

## 5. Header, footer અને સામસામે પાનાં

મુખ્ય લખાણમાં even headerમાં પુસ્તકનું title અને odd headerમાં subtitle; even footerમાં વર્તમાન section અને odd footerમાં chapter રાખવાની અગાઉની સૂચનાને shared componentમાં સ્પષ્ટ ગોઠવવી. Page number હંમેશાં બહારની ધાર પર રહે. હાલના masthead સાથે headerનું સ્થાન માપીને નક્કી કરવું, જેથી બંને ટકરાય નહીં.

Standalone pilotમાં લખેલા ૨–૩ અને વાસ્તવિક PDF 1–2 વચ્ચેનો તફાવત final book offsetથી ઉકેલવો. અંતિમ જોડાયેલા PDFમાં પ્રથમ chapter કયા વાસ્તવિક પાને શરૂ થાય છે તે પરથી parity કાઢવી. પૂર્વપાનાં પર અંક ન છપાતા હોય છતાં physical position ગણાય છે. માત્ર CSS even/odd class અથવા દેખાતા અંકથી facing-page correctness માનવી નહીં; તેના માટે મનસ્વી blank page પણ ઉમેરવો નહીં.

## 6. બધા પ્રકરણો માટે આગળની coding પદ્ધતિ

- Shared physical-unit design tokens: page size, margins, gap, body, headings, rules અને footer positions.
- Shared components: masthead, તત્ત્વ block, કાવ્ય/સાધના panel, કથા સાથે ચિત્ર, વિવેક block, દર્શન points અને running furniture.
- મૂળ Markdownમાંથી section-aware chapter data; એક જ hardcoded HTMLની 225 જુદી copies હાથથી જાળવવી નહીં.
- TOC/પ્રકરણ ક્રમ અને image mappingથી renderer ચલાવવો. દરેક outputમાં source file અને mapping keyની traceability રાખવી.
- `document.fonts.ready` અને દરેક imageનું `decode()` પૂર્ણ થયા પછી DOM ઊંચાઈ માપવી. દરેક ઉમેરાયેલા block માટે scroll/client size, bounding boxes, heading reserve અને footer clearance તપાસવાં.
- બે પાનાંમાં fit ન થતું મૂળ લખાણ exception તરીકે નોંધવું. પહેલાં reflow/ચિત્ર placement/card રચના સુધારવી. છતાં ન ફિટ થાય તો pilot reviewમાં નિર્ણય લેવો; છુપાવીને, ટૂંકાવીને અથવા નાના bodyથી બે પાનાંનો દાવો કરવો નહીં.
- 225 પ્રકરણો ખરેખર બે પાનાંમાં fit થાય તો મુખ્ય chapter matter 450 પાનાં થાય; પ્રસ્તાવના, અનુક્રમણિકા, ખંડ openings વગેરે પછી ઉમેરાય. હાલ તેને આખા પુસ્તકનો final page count ગણવો નહીં.

## 7. અમલ અને reviewનો ક્રમ

1. અલગ revision folderમાં chapter 001નું મૂળ લખાણ અને mapped image સાથે HTML બનાવવું; હાલનાં originals જાળવવા.
2. Fonts/images load થયા પછી બે પાનાંનું full-size HTML review: text order, fit, card balance, લાંબા headings અને footer distance.
3. Audit પાસ થયા પછી Chromium print mediaથી PDF: `printBackground: true`, `preferCSSPageSize: true`, કોઈ વધારાનું scale નહીં.
4. PDF અલગથી ખોલી બંને પાનાં 468 × 684 pt, page count, nonblank pages, fonts, monochrome appearance અને ચિત્રની sharpness તપાસવી.
5. માનવીય design review પછી template final કરવો. લાંબી કથા, લાંબું title અને ટૂંકા contentવાળા representative chaptersથી templateની મર્યાદા તપાસવી.
6. ત્યારબાદ બધા પ્રકરણો બનાવવાં; exceptions અને source/image mappingની audit સાથે અંતિમ TOC તથા page numbers ફરી ગણવાં.

## 8. ચકાસણીની સ્થિતિ અને સ્વીકાર માપદંડ

| સ્થિતિ | હાલનો નિષ્કર્ષ / આગળ જરૂરી કામ |
|---|---|
| HTML structural observation | આ pilotમાં measured clipping/footer overlap મળ્યાં નથી; બીજા પ્રકરણો માટે પુરાવો નથી |
| Source fidelity | મૂળ output સાથે શબ્દોના ફેરફાર મળ્યા; સુધારવું બાકી |
| Editorial balance | cards અને દર્શન પહેલાં મોટી ખાલી જગ્યા; reflow બાકી |
| PDF proof | બે પાનાં, યોગ્ય trim size; font programs મળ્યાં; image અને content સુધાર્યા પછી નવી proof જરૂરી |
| Human design approval | આ નોંધથી મંજૂરી માનેલી નથી; સુધારેલ pilotનું review બાકી |
| Press certification | printerની bleed, ICC/grayscale અને PDF/X જરૂરિયાત મુજબ અલગ preflight બાકી |

નવી QAમાં શૂન્ય missing/reordered source blocks, શૂન્ય hidden/truncated text, શૂન્ય overlap, કોઈ broken/repeated chapter image નહીં, યોગ્ય actual-PDF parity અને fonts/imagesની સંપૂર્ણ loading જરૂરી છે. વર્તમાન જૂના `QA_REPORT.md`માં 8 × 8 / 576 × 576નાં દાવા છે, તેથી તેને આ આવૃત્તિના pass તરીકે વાપરવો નહીં. દરેક નવી QAને ચોક્કસ build/hash સાથે જોડવી.

## 9. આ અવલોકનનો પુરાવો અને સુરક્ષિત ફાઇલો

અવલોકન snapshot અને transient તપાસો: `tmp/codex/pilot-design-observation/`.

- `observed_chapter_001.html`, `observed_chapter_001.pdf`: વાંચેલી આવૃત્તિની નકલ.
- `html-audit.json`, `pdf-audit.json`: માપ અને font તપાસ.
- `pdf-page-1.png`, `pdf-page-2.png`: PDFમાંથી render કરેલા proof views.
- `inspect.cjs`, `inspect_pdf.py`: આ read-only અવલોકન માટેના સહાયક સાધનો; મૂળ pilot લખતા નથી.

આ નોંધ લખતાં પહેલાં live originals અને snapshotsના hashes સરખા મળ્યા:

```text
HTML SHA256 e8763881e100bdc45169941cc6af7158ece61c1d581e32d25d7641b13572c23c
PDF  SHA256 b8b635f9d5de1124a12ca3b3ae759cfc3a96e9d8030cfeea82323438e9bbca8c
```

આ કાર્યનું retained deliverable આ નવી યોજના છે. મૂળ `chapter_001.html`, `chapter_001.pdf`, source output, જૂના reports અને image assets યથાવત્ છે. આગળનું ઉત્પાદન ઉપરના ક્રમ મુજબ અલગ revisionમાં કરવાનું છે.
