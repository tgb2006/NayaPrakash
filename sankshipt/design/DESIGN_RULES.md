# નય-ચક્ષુ — સંક્ષિપ્ત આવૃત્તિની ડિઝાઇન નિયમાવલી

આવૃત્તિ: 1.0 · 06-11-2026 · સ્થિતિ: વપરાશકર્તાએ પસંદ કરેલા pilot design નિર્ણયોનું સંકલન.

આ નિયમો `D:/PROJECT_WORK/NayaPrakash_Book/sankshipt`ના તમામ chapter HTML અને તેમાંથી બનતા PDF માટે છે. `vistrut`ના લેખન/ડિઝાઇન માટે આ આપમેળે લાગુ નથી. આ production-design document છે; Codexની વૈશ્વિક memory કે project-context onboarding file નથી.

## કઈ ફાઇલ પહેલાં વાંચવી

1. આ `DESIGN_RULES.md`: વર્તમાન ડિઝાઇનનો મુખ્ય આધાર.
2. [design_tokens.json](design_tokens.json): તે જ નિયમોનાં ચોક્કસ માપ અને strings; renderer માટે reference contract. હાલના generator સાથે આપમેળે જોડાયેલું હોવાનો દાવો નથી.
3. [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md): દરેક edit/build પહેલાં અને પછી કરવાના checks.
4. [ચાલુ pilot](../pilot_chapter_001/chapter_001.html): હાલનો visual reference. તેની અંદરની જૂની CSS declarations કરતાં browserમાં લાગુ થતી અંતિમ computed style અને આ નિયમો વાપરવા.

વપરાશકર્તાની નવી સ્પષ્ટ સૂચના હોય તો તેને અમલમાં મૂકી આ ત્રણ નિયમ ફાઇલો પણ સાથે સુધારવી. અગાઉની A5/8×8 સૂચનાઓ, Antigravity reference, જૂના QA, design plans અને A/B/C samples ઐતિહાસિક છે. તેમની જૂની headers, footer અથવા અલગ બોક્સવાળી ગોઠવણી પાછી લાવવી નહીં. મૂળ લખાણનો આધાર સંબંધિત current `output` file છે; pilotના શબ્દો બધા પ્રકરણોમાં copy કરવા નહીં.

## 1. માપ અને પાનાંનું માળખું

| બાબત | નિયમ |
|---|---|
| Trim/canvas | ચોક્કસ **6.5 × 9.5 ઇંચ**, 165.1 × 241.3 mm |
| PDF MediaBox | **468 × 684 pt**, દરેક પાનું |
| CSS | `@page { size: 6.5in 9.5in; margin: 0; }`; દરેક `<section class="page">` નિશ્ચિત canvas |
| Main inset | ઉપર 17 mm; nominal નીચે 17 mm; binding તરફ 14 mm, બહાર 12.5 mm; સામેના પાને mirror |
| Footer | bottom 8 mm; મુખ્ય લખાણ કરતાં અલગ absolute area; ઉપર .55 pt rule અને 2 mm inner top padding |
| Text/footer clearance | auditમાં ઓછામાં ઓછું લગભગ **2.1 mm**; actual glyphs, table border અને footerમાં overlap નહીં |
| Chapter | બે સામસામે પાનાં; આખું source જરૂરી. ન ફિટ થાય તો reflow અને exception review; body ઘટાડવું, crop કરવું કે text hide કરવું નહીં |

ડાબે: chapter masthead, લક્ષણ સૂત્ર, તત્વધારાના ચાર ક્રમબદ્ધ full-width blocks; નીચે કાવ્યધારા અને સાધનાધારા બાજુબાજુમાં. જમણે: કથાધારા અને તેનું ચિત્ર, વિવેકધારાની બે બાજુબાજુની columns; પછી દર્શનધારા. Sourceમાંના sections અને તેમનો ક્રમ જાળવવા. પ્રકરણ/ખંડની સંખ્યા source catalogueથી લેવી; જૂના READMEના fixed totalsથી page count ન કાઢવો.

## 2. સમાન typography અને ચોક્કસ labels

બધી છ ધારાઓનાં શીર્ષકો **Anek Gujarati 17 pt, weight 800, line-height 1.3**માં, સમાન English નાના text અને પાતળી આગળ વધતી rule સાથે રાખવા. કોઈ એક ધારા eyebrow/નાના label તરીકે રાખવી નહીં.

| ગુજરાતી | English |
|---|---|
| તત્વધારા | THE PRINCIPLE |
| કાવ્યધારા | THE POETRY |
| સાધનાધારા | THE PRACTICE |
| કથાધારા | THE STORY |
| વિવેકધારા | THE DISCERNMENT |
| દર્શનધારા | THE PERSPECTIVE |

English dhara label: 7.5 pt serif, weight 400, line-height 1.15, letter spacing .35 pt, gray #777. હાલના pilotમાં Georgia/generic serif fallback છે; final PDFમાં actual English font અને embedding તપાસવા. Machine font મળ્યું એટલે portable English font નક્કી થઈ ગયું એમ માનવું નહીં.

- મુખ્ય chapter title: Anek Gujarati 28 pt / weight 800 / line-height 1.1. English concept અલગ lineમાં 8 pt. Chapter title વારંવાર ન દોહરાવવો.
- રૂપક-દ્રષ્ટિ, સ્વરૂપ-સૃષ્ટિ, વ્યવહાર-પૃષ્ટિ, મર્મ-તુષ્ટિ; પિપાસા, પાન; એકાંત/અનેકાંત દર્શન; દર્શનધારાના ઉપશીર્ષકો: **Anek Gujarati 13 pt / weight 700 / line-height 1.15**. કથાનું પોતાનું title પણ 13 pt છે.
- તત્વના વર્ણનાત્મક secondary subhead: 10.5 pt / weight 600. આ secondary levelને મુખ્ય subsection સાથે ગૂંચવવો નહીં.
- સામાન્ય body અને table body: **Noto Sans Gujarati 11 pt / line-height 1.38**, body color neutral black/gray. સામાન્ય paragraph spacing લગભગ 6.5 ptને આધાર માની measured fit કરવું; દરેક નાના semantic block પર મોટો margin ફરજિયાત લાદવો નહીં.
- બધા prose paragraphs, examples/list items, સાધના, કથા, વિવેક તથા દર્શન table text **justify**. `text-align-last: start`, `text-justify: inter-word`; છેલ્લી lineને ખેંચવી નહીં. શબ્દો વચ્ચે અસ્વાભાવિક ખાલી જગ્યા renderમાં તપાસવી.
- કાવ્ય prose નથી: મૂળ line breaks સાથે **left aligned**, Anek Gujarati 12 pt / weight 600 / line-height 1.45. Headingને justify ન કરવું.
- સૂત્ર પહેલાં માત્ર **“લક્ષણ સૂત્ર”**. “મૂળ આગમિક લક્ષણ-સૂત્ર” અથવા બીજા લાંબા prefix પાછા ન મૂકવા. સૂત્રના મૂળ શબ્દો બદલવા નહીં; Noto Sans Devanagari 10.5 pt / line-height 1.35. Ellipsis, `nowrap`થી કપાત કે hidden text નહીં.
- Gujarati તથા Sanskrit fonts projectના local assetsમાંથી relative URLથી load કરવા; PDFમાં embedding ચકાસવું.

## 3. પસંદ કરેલી દર્શનધારા: A, joined ૧–૨–૧

```text
┌───────────────────────────────────┐
│ ૦૧  નય-ઉન્મેષ           [gray]    │
├─────────────────┬─────────────────┤
│ ૦૨ પ્રાચીન-વિશેષ│ ૦૩ અર્વાચીન-પ્રવેશ│
│     [white]     │      [white]    │
├─────────────────┴─────────────────┤
│ ૦૪  સમન્વય-અશેષ        [gray]     │
└───────────────────────────────────┘
```

- **A પસંદ કરેલી grayscale**: ઉપર અને નીચે #eaeaea; વચ્ચેની બંને cells #ffffff. B/C alternatives મંજૂર default નથી.
- Top અને bottom full-width; middle columns સરખી width અને height, divider બરાબર centerમાં. `repeat(2,minmax(0,1fr))`, stretch alignment.
- **બોક્સ વચ્ચે row/column gap શૂન્ય**. એક બહારની border, બે horizontal dividers અને માત્ર middle pairમાં એક vertical divider. Double border નહીં. બધી table rules **.55 pt solid #aaa**.
- દરેક cellમાં inner padding **1.2 mm ઉપર/નીચે, 2 mm ડાબે/જમણે**. બોક્સ જોડવા માટે આ internal padding દૂર ન કરવું.
- નંબરો ચોક્કસ **૦૧, ૦૨, ૦૩, ૦૪**, પછી dot નહીં. તત્વધારા જેવા **Anek Gujarati 16 pt / weight 700 / gray #888 / line-height 1**.
- **Hanging layout**: દરેક cellની અંદર નંબર માટે 6.5 mmની અલગ column, પછી 1.2 mm gap અને `minmax(0,1fr)` text column. `.row-copy` block છે. Heading અને body પછીની બધી lines text columnની શરૂઆતથી આવે; નંબરની નીચે નહીં.
- Number અને textની વચ્ચે line તૂટે કે બંને અડે નહીં. છેલ્લાં paragraph-શૈલીવાળા મોટા inline numbers અથવા dotted numbering પાછી ન લાવવી.

## 4. વિવેકધારા અને સંબંધિત spacing

- પાનના લખાણ પછી વિવેકધારાના heading સુધી **લગભગ 4.5 mm** સ્પષ્ટ અંતર. હાલ 1 mm parent gap + 3.5 mm section marginથી મળે છે; બે વખત 4.5 mm ઉમેરવું નહીં.
- વિવેકધારામાં એકાંત અને અનેકાંતની બે columns; વચ્ચે 5.8 mm gap.
- અનેકાંતના gray box (#f2f2f2)માં padding **ઉપર/નીચે 1.8 mm, ડાબે/જમણે 2.5 mm**. 1 mm / 1.5 mmની તંગ જૂની padding પાછી ન કરવી. Larger paddingથી fit બદલાય તો measured reflow કરવો.
- સામાન્ય paired panels/columnsમાં આશરે 5.8 mm gap; દર્શનધારાના joined gridમાં આ gap લાગુ નહીં પડે.

## 5. Headers અને અંતિમ footer ગોઠવણી

**બંને running headers સંપૂર્ણ દૂર છે**—DOM/printમાં પણ નહીં. Chapter masthead અને ધારા headings દૂર કરવાના નથી. Screen-only review toolbar પુસ્તકનું header નથી; printમાં તે છુપાય.

| પાનું | Footerની ડાબી બાજુ | Footerની જમણી બાજુ |
|---|---|---|
| ડાબું facing page / even | બહારની ધાર પર page number | **નય-ચક્ષુ \| નયનું જ્ઞાન, સંશયનું સમાધાન** |
| જમણું facing page / odd | **વર્તમાન ખંડનું નામ**; પ્રકરણ 001 માટે **પ્રથમ ખંડ: નૈગમ નય** | બહારની ધાર પર page number |

Book name અને subtitle વચ્ચે દેખાતી vertical separator line `|` રાખવી. Subtitleને chapter titleથી બદલવો નહીં. Right-page footerમાં chapter name, જેમ કે “ભૂતનૈગમ નય”, પાછું મૂકવું નહીં. ખંડનો footer દરેક ખંડના actual metadataથી લેવાનો છે; “પ્રથમ ખંડ” બધે hardcode કરવું નહીં.

Footer text Anek Gujarati 8.5 pt, book/khanda emphasis weight 600; folio 12 pt / weight 700. Main text સાથે footer જોડાય નહીં. પ્રસ્તાવના/અનુક્રમણિકામાં running header/footer/page number ન રાખવાના અગાઉના નિયમો યથાવત્. અંતિમ assembled PDFમાં સાચી physical parity તપાસવી; pilotનાં ૨–૩ labels standalone PDFનાં 1–2 સ્થાનનો પુરાવો નથી.

## 6. ચિત્રો, source અને portability

દરેક કથાનું પોતાનું square black/white અથવા grayscale clipart `Image/chapter-image-map.json`ના keyથી લેવું. Press asset પસંદ કરવો; filename અનુમાનથી નહીં. હાલના pilotમાં 32 × 32 mm placement અને `object-fit:contain` છે; બદલાવ measured fit અને print-resolution reviewથી કરવો. એક જ ચિત્ર અલગ chaptersમાં ફરી નહીં વાપરવું. Original assets જાળવવા; existing human religious/iconographic review statusને pass માનવું નહીં.

Current sourceના દરેક semantic blockને ID આપી મૂળ શબ્દો/ક્રમ સરખાવવા. દેખાવ માટે sourceમાં ફેરફાર નહીં. **હાલના pilot અને current output વચ્ચે અગાઉ નોંધાયેલ content તફાવત છે**: design style પસંદ થયેલી છે, content sync અથવા આખા પુસ્તકની source audit પૂર્ણ નથી. Latest source sync કર્યા પછી ફરી layout audit કરવી. આ documentationથી નવા chapters બની ગયાનો દાવો નથી.

## 7. દરેક routine edit/buildની પદ્ધતિ

1. પહેલાં ચાલુ ફાઇલની નકલ અલગ `pilot_chapter_001/backups/<named_revision>/`માં; bulk productionમાં સમાન owning-output backup path. અગાઉની backupને overwrite નહીં.
2. વપરાશકર્તાની ચાલુ review file **`pilot_chapter_001/chapter_001.html`માં સીધો સુધારો**, જેથી refreshમાં દેખાય. ફક્ત બીજા sample folderમાં edit કરીને મુખ્ય ફાઇલ જૂની ન છોડવી.
3. અલગ `revisions/<revision>/`માં review copy, previews અને QA રાખવા. Relative assetsને revisionના સ્થાન પ્રમાણે સુધારવા. જૂની copies production input ન બને.
4. આ નિયમો, tokens અને checklist પછી જ CSS/data ફેરફાર. Overrideથી ભૂલ થાય તે માટે computed styleનું audit કરવું; CSSમાં છેલ્લે લાગુ પડતો selector ચકાસવો.
5. Fonts ready અને image decode પછી HTML audit, પછી PDF proof. HTML audit, human design review, PDF proof અને press certification અલગ statuses છે.
6. Source લાંબું હોય તો heading wrapping, sensible spacing અને image placementથી reflow. Body font ઘટાડવું, clipping/ellipsis, અણધાર્યું zoom અથવા શબ્દો કાપવા નહીં. Exception સ્પષ્ટ નોંધવી.
7. PDF export: Chromium print media, `printBackground:true`, `preferCSSPageSize:true`; default browser margins/extra scaling નહીં. સ્વતંત્ર PDF inspection/renderથી માપ, fonts, images, nonblank pages અને footer parity તપાસવી.

છેલ્લો visual આધાર: `pilot_chapter_001/revisions/hanging_20261106_r11/`. પસંદ કરેલી શૈલીનો આધાર આ નિયમો છે; આ pointer ઐતિહાસિક proof છે. નવી આવૃત્તિના auditનો receipt અલગ રાખવો.
