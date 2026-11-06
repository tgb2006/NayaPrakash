# ભૂતનૈગમ નય — બે સામસામેના પાનાંનો પાઈલોટ r01

સ્થિતિ: **HTML design review candidate**. માનવીય મંજૂરી, PDF proof અને press certification હજી બાકી છે.

## અનુસરેલા સ્રોત

- મૂળ Antigravity પાઈલોટ: `D:/PROJECT_WORK/NayaPrakash_Book/sankshipt/pilot_chapter_001/user_approved_design_replica/chapter_001_user_replica.html`.
- વપરાશકર્તાએ આપેલા paging rulesની આ revisionમાં read-only source copy: `PAGING_RULES_AND_DESIGN_SPECS.source.md`.
- તાજેતરના reference photographની copy: `design-reference.png`.
- આ book-specific paging rulesના body font sizes અને margins પહેલાંના સામાન્ય 11 pt/15 mm સૂચન કરતાં વધુ ચોક્કસ છે, તેથી આ પાઈલોટમાં book-specific માપ અપનાવ્યાં છે.
- નિયમો “14 IDs” કહે છે, પરંતુ યાદીમાં 16 છે; તમામ 16 સામેલ કર્યાં છે.

## કરેલા સુધારા

- ડાબું પાનું: તત્વધારા અને કાવ્યધારા; જમણું પાનું: ડાબી columnમાં ચિત્ર/વિવેકધારા, જમણી columnમાં કથાધારા.
- બંને પાનાં જોડીને facing spread preview; printમાં અલગ 8 × 8 inch પાનાં. કોઈ zoom, crop, stretch કે overflow clipping નથી.
- Sidebarનું ગુજરાતી લખાણ હવે પંક્તિ તરીકે ફેરવે છે; અક્ષર-અક્ષર writing-modeનો વિઘ્ન દૂર કર્યો. Gujarati જોડાક્ષર માટે letter-spacing 2.2 ptથી .3 pt કરાયું છે.
- કલિગ્રાફી headingsને ફોટામાંની visual prominence નજીક લાવવા મોટાં કર્યાં છે. મૂળ graphicનું લખાણ જાળવ્યું છે.
- Labelsને ફોટા મુજબ flat gray bars, quotationને upright text, કાવ્યને light-gray panel અને footerને નીચે નિશ્ચિત સ્થાન આપ્યું.
- Column gutter બાદ બાકી પહોળાઈ 37.5:60 ગુણોત્તરમાં વહેંચી; મૂળ ટકાવારી + gutterથી થતું horizontal overrun દૂર કર્યું.
- દાદાજી–પિતા–પુત્રનું અલગ high-resolution ink illustration બનાવ્યું. મૂળ reference સાથે composition નજીક રાખી છે; આ નવી rendition છે, મૂળ bitmapની pixel-identical upscale નથી. તેના ચહેરા/હાથ/ભાવની માનવીય સમીક્ષા બાકી છે.
- મૂળ HTML, મૂળ assets અને પહેલાંના book-wide draft બદલ્યાં નથી. આ revision માત્ર પ્રકરણ ૧ માટે છે.

## કથાચિત્રનું art brief

મુખ્ય વિચાર: વર્તમાનની એક ભૂલની પાછળ ભૂતકાળના ઉપકાર ભૂલવા નહીં; સ્મરણથી ક્ષમા અને સંબંધમાં શાંતિ.

દૃશ્ય: વૃદ્ધ દાદાજી પાછળ ડાબે, પિતા મધ્યમાં, યુવાન પુત્ર જમણે. દાદાજીનો આશ્વાસક હાથ પિતાના ખભા પર; પિતાના હાથ છાતી નજીક; પુત્ર ધ્યાનથી સાંભળે. સામાન્ય ભારતીય ગૃહસ્થો, ધાર્મિક વેશ નહીં. સફેદ પૃષ્ઠભૂમિ, કાળું ink line art, કોઈ lettering નહીં. માથાં અને હાથ અખંડ. Placement: વિવેકધારા ઉપર 52 mm ઊંચાઈ, contain; કોઈ object crop નહીં.

## Chromiumમાં મળેલું પુરાવું

| તપાસ | પરિણામ |
|---|---|
| HTML pages | 2 |
| દરેક canvas | 768 × 768 CSS px = 8 × 8 inch |
| Print media canvas | બંને 768 × 768 CSS px |
| Semantic IDs | 16/16 હાજર, IDs અનન્ય |
| Paragraph IDs | 12/12 હાજર |
| મૂળ pilotના ID આધારિત normalized textની સરખામણી | 0 તફાવત |
| Page boundary violations | 0 |
| Column–footer overlaps | 0 |
| Gutter | 6.499 mm |
| Right column content boundsમાં | હા |
| Fonts અને images load | પૂર્ણ |
| નવું કથાચિત્ર | 1226 × 1283 px; placement પર આશરે 627 DPI |

Screen spread અને બન્ને single-page screenshots તપાસ્યાં છે. આ DOM/HTML પુરાવા છે; PDF embedding કે PDF MediaBox માટેનો પુરાવો નથી.

## સમીક્ષા અને print માટે બાકી બાબતો

1. આપેલા ફોટા સામે layout અને નવા ચિત્રની માનવીય design review.
2. ચાર મૂળ કલિગ્રાફી heading bitmaps માત્ર 86–102 px પહોળાં છે. હાલના મોટા placement પર આશરે 61–65 DPI મળે છે અને edges pixelated દેખાઈ શકે છે. Press file માટે એ જ letteringનાં high-resolution originals અથવા મંજૂર vector/font alternative જરૂરી છે. આને press-quality pass આપ્યો નથી.
3. નિયમોમાં દર્શાવેલી ચોક્કસ line counts column/font shaping સાથે દરેક જગ્યાએ મળતી નથી. મૂળ શબ્દો કાપ્યા નથી અને line counts મેળવવા body font ઘટાડ્યો નથી. હાલની text wrapping માનવીય review માટે છે.
4. Sidebar 22 mm અને અન્ય મુખ્ય માપ paging specification મુજબ છે; ફોટાના અલગ pixel proportionsની નિરપેક્ષ નકલ કરી નથી. Section-heading prominence, bar treatment, sidebar rotation અને decorationમાં ઉપર જણાવેલા photo-driven ફેરફારો છે.
5. `Page • 002 - 003` પુસ્તકમાં આ spreadનું label છે. Standalone 2-page PDFમાં physical page numbers 1/2 આવશે; પુસ્તકમાં જોડતી વખતે actual PDF parity ફરી ચકાસવાની છે. કૃત્રિમ blank page ઉમેરેલું નથી.
6. HTML મંજૂરી પછી PDF export; ત્યારબાદ 576 × 576 pt MediaBox, page count, embedded fonts, grayscale, image clarity અને સ્વતંત્ર PDF render proof કરવાના છે.

## Files અને provenance

આ revisionની બધી files આ જ folderમાં છે. મૂળ સ્રોતનો SHA-256 `source-receipt.json`માં છે. Browserનું વિગતવાર પરિણામ `qa-audit.json`માં છે. `files-manifest.json`માં retained filesના absolute paths અને hashes છે. પુનઃઉત્પાદન helpers projectના `tmp/codex/magazine-review`માં છે.
