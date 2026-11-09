# નય-ચક્ષુ — સંપૂર્ણ પુસ્તક QA અને ઉત્પાદન નોંધ

તારીખ: 06-11-2026 · Revision r01 · Project root: D:/PROJECT_WORK/NayaPrakash_Book.

## તૈયાર થયેલું પુસ્તક

એક static master HTML અને તે જ layoutમાંથી એક combined PDF તૈયાર છે. Title, compilerનું મંગલાચરણ, બંને પ્રસ્તાવના/પરિચય, generated અનુક્રમણિકા, પાંચ સામાન્ય પ્રકરણો, સાત ખંડ-પરિચય સાથે તમામ 225 પ્રકરણો અને પરિશિષ્ટ 00–08 સામેલ છે. Assets સ્થાનિક relative pathsથી load થાય છે. Source snapshots અને અગાઉના build proofs સુરક્ષિત છે.

| બાબત | પરિણામ |
|---|---|
| Canonical Markdown files | 248: 225 chapters +23 અન્ય files |
| કુલ પાનાં | 1022 |
| દરેક PDF MediaBox | 468 × 684 pt =6.5 ×9.5 inch |
| DOM source blocks | 8518/8518; missing/duplicate/text mismatch 0 |
| મૂળ source order | PASS |
| Semantic charts | 16:14 ASCII +2 Mermaid, actual HTML/CSS/SVG |
| Semantic table segments | 27; repeatedthead માત્ર pagination માટે |
| અલગ chapter images | 225, બધાં mapped press assets |
| Browser overflow/errors | 0 |
| Final TOC page-number errors | 0 |
| PDF fonts | 10; embedded અથવા self-contained Type3 |
| Independent PDF sample renders | 50, બધા16 chart pages સહિત |
| Source inventory hash changes | 0 |

## પસંદ કરેલી ડિઝાઇન

છેય ધારા headings17pt; subsection13pt; prose/table body11pt/1.38 justified, છેલ્લી line start-aligned. લક્ષણનું label “લક્ષણ સૂત્ર”. દર્શનધારા A: gray top/bottom, white middle pair, joined1–2–1, symmetricrules, dot વગર ૦૧–૦૪ hanging columns. અનેકાંત boxpadding1.8mm/2.5mm અને પાનથી વિવેક સુધી4.5mm gap જાળવ્યાં. Running headers નથી. Even-page footerમાં બહાર નંબર અને અંદર bookname/subtitle; odd-page footerમાં અંદર currentkhanda અને બહાર નંબર. Finalactualphysicalparity ચકાસી છે.

## Pagination અને વધારાનાં પાનાં

બે પાનાંનું original target દરેક લાંબા source માટે body11ptમાં શક્ય નહોતું. Source અથવા fonts ઘટાડ્યા નથી: 2 chapters બે પાનાં અને 223 chapters ચાર balanced continuation પાનાંમાં છે. તમામ225 chapter starts even અને spans even/contiguous છે. Chapter matter 896 pages છે. બાકીનાં pages: {"title": 1, "mangal": 1, "preface": 9, "toc": 10, "general": 31, "khanda_intro": 29, "navigation": 2, "appendix": 43}.

ખંડ transition માટે બે intentional reading-guide pages છે. પાંચ intro endingsમાં existing last-three pagesની content balance સુધારેલી છે; blank filler નથી. Continuation pagesમાં semantic blocksનો મૂળ ક્રમ જાળવ્યો છે. Longtitlesને જરૂર મુજબ24/22pt અને ચિત્રને28mm સુધી ગોઠવ્યાં; body11pt છે. બધા chapter layoutsને કાપીને બે પાનાંમાં ફિટ કર્યાં હોવાનો દાવો નથી.

## સ્વતંત્ર source અને PDF QA

- Chapter source-to-render lexical audit:225/225;158,029 tokens અને3,768 ordered prose/list/verse sequences. Actual serialized chapter DOMનું પણ સ્વતંત્ર audit થયું છે; માત્ર inputJSON/IDsનો pass નથી.
- Nonchapter audit:23/23 filesનાં words/counts/chartlabels/tablecells જાળવ્યાં. Sourceમાંના tableheadersને auditમાં એક જ વખત ગણ્યાં; final repeatedheaders વાંચનની સગવડ માટે છે.
- PDF: તમામ પાનાંનું માપ અને extractable nonblank text, fonts/Type3, image placements/effective DPI અને resource pixels તપાસ્યાં. 50 sample pagesમાં title/last, openings, paired parity, long/dense ends, charts અને appendices તપાસ્યાં.
- Sourceના રંગીન emojiના presentationને monochrome vector symbolsમાં ફેરવ્યું છે. મૂળ Unicode `data-original-symbol`/accessible labelમાં જાળવ્યું છે; source-text audit તેને reconstruct કરે છે. આખાં textpages rasterize કર્યાં નથી.
- જૂના sourceમાંના203/જૂના ખંડ-count સંદર્ભો મૂળરૂપે જાળવ્યા છે. Title pageની editorial note current225 અને sourcehistoricalcounts વચ્ચેનો ભેદ સમજાવે છે. મૂળ doctrine/sourcewordsમાં silent rewrite નથી.
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
HTML SHA256 8cbe2ae0e380a6aa67ef260fdf956fd39eb403be8e03650baf3ad1cbc28d51a6
PDF SHA256  bd68cf9cc6feb76a46213213148db12f99dd715aae7d2a28be51e68f68b51565
```

ચોક્કસ retained files/hashes [artifact-manifest.json](artifact-manifest.json)માં છે. Source originals અને approvedpilot બદલ્યા નથી. Tools `sankshipt/production/`માં છે; [rebuild સૂચનાઓ](../../../production/README.md)માં commands આપેલ છે.
