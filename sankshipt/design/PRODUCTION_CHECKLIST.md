# નય-ચક્ષુ — routine design checklist

મુખ્ય નિયમ: [DESIGN_RULES.md](DESIGN_RULES.md). ચોક્કસ values: [design_tokens.json](design_tokens.json). Checklist એકલી પૂર્ણ નિયમાવલીનું સ્થાન લેતી નથી.

## ફેરફાર પહેલાં

- [ ] સાચો root `D:/PROJECT_WORK/NayaPrakash_Book`; કામ `sankshipt` માટે જ છે.
- [ ] વર્તમાન નિયમો, tokens અને current source chapter વાંચ્યાં; જૂના README/QA/templateને current rule ગણ્યો નથી.
- [ ] Live HTML, source અને image mappingના ચોક્કસ paths નક્કી કર્યા.
- [ ] અલગ `backups/<revision>/`માં અગાઉની આવૃત્તિની નકલ લીધી; કોઈ જૂનો backup overwrite નથી.
- [ ] Source/version mismatch હોય તો નોંધ્યો; pilotનો જૂનો text current output સાથે સરખો છે એવું અનુમાન નથી.

## HTMLમાં દેખાવ અને ચોક્કસ લખાણ

- [ ] 6.5 × 9.5 inch fixed pages; original text/order/semantic block IDs જાળવ્યાં.
- [ ] છેય ધારા headings: સમાન 17 pt, weight 800, English subtext અને સમાન rule style.
- [ ] તમામ subsection headings 13 pt; prose body 11 pt / 1.38, justified, છેલ્લી line start-aligned. કાવ્યમાં મૂળ breaks અને left alignment.
- [ ] સૂત્રનો label ચોક્કસ **લક્ષણ સૂત્ર**; સૂત્ર પૂર્ણ, untruncated.
- [ ] દર્શનધારા A: top/bottom gray, middle white; joined ૧–૨–૧; cell gap 0.
- [ ] Tableની middle columns સમાન width/height; centered divider; એકસરખી .55 pt rules, double border નહીં.
- [ ] ૦૧–૦૪ dot વગર; 16 pt bold gray; 6.5 mm number column + 1.2 mm gap; hanging textની બધી lines યોગ્ય શરૂઆતથી.
- [ ] અનેકાંત padding 1.8 mm vertical / 2.5 mm horizontal; text boxની ધારને અડતું નથી.
- [ ] પાન પછી વિવેકધારા સુધી ~4.5 mm visual gap; heading અગાઉના paragraphને અડતું નથી.
- [ ] Running headers નથી. Chapter/section headings યથાવત્. Review toolbar printમાં નથી.
- [ ] ડાબો footer: number બહાર ડાબે; જમણે **નય-ચક્ષુ | નયનું જ્ઞાન, સંશયનું સમાધાન**.
- [ ] જમણો footer: ડાબે actual current khanda; number બહાર જમણે. Chapter name footerમાં નથી.
- [ ] કથાનું mapped square press clipart સાચું, unique, સંપૂર્ણ visible; relative image/font paths યોગ્ય.

## Browser audit અને live review

- [ ] `document.fonts.ready` અને તમામ `image.decode()` પછી માપ લીધાં.
- [ ] Sourceના actual text, block count અને ક્રમ સરખાવ્યાં; માત્ર IDs હાજર હોવાથી source coverage PASS નથી.
- [ ] Applied computed typography, justification, padding, hanging layout, labels અને colors તપાસ્યાં.
- [ ] `scrollHeight/clientHeight`, horizontal fit, bounding boxes અને actual text/image/footer clearance તપાસ્યાં.
- [ ] Footerથી ઓછામાં ઓછું ~2.1 mm measured clearance; કોઈ clipped/hidden text કે image/text/footer overlap નહીં.
- [ ] Screen અને print media બંનેમાં spread, tight endings અને લાંબા headingsનાં full-size previews જોયાં.
- [ ] મુખ્ય ચાલુ HTMLમાં સુધારો છે; refreshથી latest design દેખાય છે. Revision copiesના asset paths પણ સાચા છે.
- [ ] Revision QAમાં exact files, source/build hashes, results, limitations અને બાકી human review નોંધ્યાં.

## HTML review પછી PDF

- [ ] માનવીય review પછી નવી PDF proof બનાવી; જૂનું PDF નવા HTMLનું છે એવું નથી કહ્યું.
- [ ] Print media, `printBackground:true`, `preferCSSPageSize:true`, વધારાનું scaling/default margin નહીં.
- [ ] Independent PDF inspection: દરેક MediaBox 468 × 684 pt, fonts embedded, યોગ્ય page count અને કોઈ blank page નહીં.
- [ ] Rendered PDFમાં Gujarati/Sanskrit shaping, gray contrast, image sharpness અને long/short endings તપાસ્યાં.
- [ ] Final bookની actual physical parity પ્રમાણે બહારના folios અને footer content; frontmatterનો offset ગણ્યો.
- [ ] HTML audit / human design review / PDF proof / press certification અલગ statuses રાખ્યાં.
- [ ] Printerનું bleed, ICC/grayscale, PDF/X specification હોય તો અલગ final preflight કર્યું.

કોઈ checkbox fail હોય તો માત્ર જગ્યામાં સમાવવા માટે body/source ન બદલવાં. Reflow, exception અને બાકી approval સ્પષ્ટ નોંધવા.
