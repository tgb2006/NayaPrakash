# નય-ચક્ષુ — HTML r01 સ્થિતિ

આ પૂર્ણ મૂળ પાઠ ધરાવતી પ્રારંભિક HTML layout આવૃત્તિ છે. આ આવૃત્તિ સંપૂર્ણ illustrated review, approved design, PDF proof કે press-certified release નથી.

## સ્રોત અને પાઠ

- સ્રોત: આ જ projectનું `sankshipt/output`: 225 chapter files, 7 ખંડપરિચય અને 5 સામાન્ય પ્રકરણ.
- જૂની compiled files ફરી ઉમેરવામાં આવી નથી. સ્રોત બદલાયા નથી.
- `source-manifest.json`માં દરેક fileનો relative path, normalized UTF-8 contentનો SHA-256 અને દરેક blockની ઓળખ/મૂળ Markdown છે.
- Browser audit: 4,901/4,901 block IDs હાજર, મૂળ ક્રમ યથાવત્. આ block coverage છે; શબ્દશઃ rendered-text comparison અને સ્વતંત્ર proofreading હજી બાકી છે.

## HTML તપાસ

- Chromiumમાં Gujarati regular/bold, Gujarati display અને Devanagari fonts load થયા. Fonts revisionના `assets/fonts`માં છે; HTML machine-specific font path વાપરતું નથી.
- દરેક page canvas અને CSS print size 8 × 8 inch; body 11 pt, line-height 1.38, side margins 15 mm, column gap 5.8 mm.
- 740 HTML pages. આ provisional pagination છે; ચિત્રો ઉમેરાયા પછી page count અને contents ફરી ગણવાના છે.
- DOM auditમાં text-column overflow: 0; block placement errors: 0.
- Cover અને contentsમાં running header/footer/page number નથી. અન્ય પાનાંમાં ભવિષ્યના PDF physical page sequence પરથી odd/even સ્થાન અપાયું છે; વાસ્તવિક PDF parity હજી તપાસાઈ નથી.
- Title/header/footerના દરેક સંભવિત overlap, દરેક paragraphની widow/orphan સ્થિતિ, દરેક page-start rule અને સંપૂર્ણ પુસ્તકના screenshotsની સમીક્ષા હજી બાકી છે. Auditમાં zero overflowનો અર્થ આ બધી તપાસો pass થાય એવો નથી.
- ટૂંકા અંતવાળા પાનાં ફરી ગોઠવ્યાં. Auditમાં હજી 3 ઓછા ભરાયેલા body pages: 119, 167, 188; તેમની editorial સમીક્ષા બાકી છે.

## ચિત્ર અને ડિઝાઇન — બાકી

- 225 કથાઓ માટે source-linked art preparation records `art-briefs.json`માં છે. તેમાં મૂળ કથા, ભૂમિકા, grayscale/અહિંસા સંબંધિત શરતો અને crop reviewની જરૂરિયાત છે.
- આ records final individual art briefs નથી: દરેક માટે મુખ્ય વિચાર, ચોક્કસ દૃશ્ય, પાત્ર/વસ્તુ અને ભાવનું સંપાદકીય નિર્ધારણ કરવાનું બાકી છે.
- 225 અલગ કથાચિત્રો હજી બનાવ્યાં નથી. HTMLમાં gray image placeholders કે દોહરાવેલાં pilot illustrations મૂક્યાં નથી.
- આપેલા design photographની copy `design-reference.png`માં છે. હાલની typographic layout તેની ચોક્કસ reproduction નથી; composition, illustration placement અને section treatmentનું અંતિમ મિલાન બાકી છે.
- તેથી આ HTML પર અંતિમ design approval લેવાનો તબક્કો હજી આવ્યો નથી.

## અલગ approval સ્થિતિઓ

| સ્થિતિ | પરિણામ |
|---|---|
| Source block coverage/order | પાસ — browserમાં IDs આધારિત |
| Text-column overflow | પાસ — હાલના DOM માપ મુજબ |
| સંપૂર્ણ HTML/design audit | અધૂરું |
| દરેક કથાનું illustration | બાકી |
| માનવીય HTML/design approval | બાકી |
| PDF proof | બનાવ્યું નથી; HTML સમીક્ષા પછી |
| PDF MediaBox/font embedding/grayscale/images/parity | PDF બન્યા પછી તપાસવાનું |
| Press certification | બાકી; bleed/profile/PDF-X specification મળેલી નથી |

## આગળનું ઉત્પાદન

દરેક art briefને ચોક્કસ દૃશ્યમાં વિકસાવવું, અલગ high-resolution grayscale illustration બનાવવું, placement/cropનું નિરીક્ષણ કરવું, તમામ block coverage અને pagination ફરી માપવાં, title/footer અને orphan audits પૂર્ણ કરવા, પછી સંપૂર્ણ HTML માનવીય સમીક્ષામાં આપવું. તે સમીક્ષા પછી જ Chromium PDF export અને સ્વતંત્ર PDF proof કરવો.

## આ revisionમાં બનાવેલી files

`book.html`, `QA_REPORT.md`, `browser-audit.json`, `source-manifest.json`, `art-briefs.json`, `design-reference.png`, `assets/fonts/*.ttf`, અને `page-*.png` browser screenshots. બધું `sankshipt/output/magazine_review/r01`માં છે. પુનઃઉત્પાદન માટેના helpers `tmp/codex/magazine-review`માં છે. મૂળ પાઠ અને અગાઉના pilot outputs બદલ્યાં નથી.

