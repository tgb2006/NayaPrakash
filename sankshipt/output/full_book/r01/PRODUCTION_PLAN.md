# નય-ચક્ષુ — સંપૂર્ણ પુસ્તક ઉત્પાદન યોજના

06-11-2026 · Goal: titleથી પરિશિષ્ટ સુધી એક master HTML અને એક combined PDF.

આ run માટે વપરાશકર્તાએ વચ્ચે human gate/approval/question માટે રોકાયા વિના પૂર્ણ કરવાનું કહ્યું છે. Browser review અને PDF proof સ્વતંત્ર રીતે કરવાના છે; માનવીય design proof તથા printer certificationની બાકી સ્થિતિ અંતે સ્પષ્ટ જણાવવી, તેમને કામ અટકાવતો gate બનાવવો નહીં. સામાન્ય checklistમાંની human-review-before-PDF સૂચનાને આ runની સીધી user સૂચના supersede કરે છે.

## પૂર્ણતાનો આધાર

Current catalogue: 225 chapters; 248 canonical Markdown files. બે prefaces, પાંચ સામાન્ય પ્રકરણો, સાત ખંડ-પરિચય અને નવ appendix files. Fractional IDs સહિત catalogue order જાળવવાનો છે. Images: 225 mapped press assets. જૂના compiled master/TOCને ફરી prose તરીકે ઉમેરી duplicate matter કરવું નહીં.

ક્રમ: title → compilerમાં આપેલું મંગલાચરણ → બે prefaces → generated contents → પાંચ સામાન્ય પ્રકરણો → દરેક ખંડનો introduction અને તમામ chapters → appendix intro અને 01–08 appendices.

## અમલ

1. Originals બદલી નહીં; build-time source snapshots/hashes અને selected design rulesનો આધાર.
2. Chapter parser semantic IDs સાથે આખું current text જાળવે. Nonchapter parser prose/verse/tables/ASCII/Mermaid chartsને અર્થપૂર્ણ HTMLમાં ફેરવે.
3. Fonts અને images તૈયાર થયા પછી browser geometryથી pagination. દરેક page 6.5 × 9.5 inch. Body11pt યથાવત્.
4. Chapter બે પાનાંમાં ન સમાય તો readable compact spacing અને heading/image adjustment; ત્યારબાદ balanced even continuation pages. Source કાપવો/hidden overflow/body shrink નહીં.
5. Actual physical page parity, source coverage/order, tables/charts, images અને contents page numbersની audit.
6. Pass પછી Chromium PDF; independent MediaBox, fonts, images અને rendered-page proof.
7. Final HTML/PDF, QA report, exceptions અને known editorial discrepanciesની links.

## નોંધાયેલા editorial તફાવતો

કેટલાક source prefaces/ખંડ introductionsમાં જૂના 203 અથવા જૂના chapter counts છે. Catalogueમાં 225 છે. Source proseને silently rewrite કરવો નહીં; edition discrepancy QAમાં નોંધવી. બે chaptersમાં Sanskrit સૂત્રને બદલે લેખકૃત ગુજરાતી વ્યાખ્યા-આશય છે; મૂળ attribution સાથે રાખવું, ખોટું સૂત્ર ગઢવું નહીં. Printerનું bleed/PDF-X/ICC specification આપેલું નથી; trim proofને press-certified file કહેવું નહીં.

## Output અને reproducibility

આ folderનું `naya_chakshu_book.html` સંપૂર્ણ static master રહેશે; `naya_chakshu_book.pdf` તે જ buildનું proof. Fonts/images `assets/`માં local અને relative. Source snapshots, source-manifest, pagination map, HTML audit અને PDF QA આ જ revision સાથે રાખવા. Rebuild tools `sankshipt/production/`માં રાખવા. Pilot તથા અગાઉના versions યથાવત્ રહે.
