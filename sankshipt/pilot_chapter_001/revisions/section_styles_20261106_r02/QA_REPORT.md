# સમાન ધારા શીર્ષકો અને striped દર્શનધારા — review r02

તારીખ: 06-11-2026. માપ: 6.5 × 9.5 ઇંચ. વપરાશકર્તાએ C—નંબરવાળા પટ્ટા પસંદ કર્યો છે. મુખ્ય HTMLમાં C લાગુ છે; નવી PDF proof બાકી છે.

## લાગુ કરેલા સુધારા

- તત્વધારા, કાવ્યધારા, સાધનાધારા, કથાધારા, વિવેકધારા અને દર્શનધારા: એક shared style, **Anek Gujarati 17 pt / weight 800 / line-height 1.3**. દરેકમાં સમાન English subtext style 7.5 pt અને પાતળી rule.
- English labels: THE PRINCIPLE, THE POETRY, THE PRACTICE, THE STORY, THE DISCERNMENT, THE PERSPECTIVE.
- રૂપક-દ્રષ્ટિ વગેરે, પિપાસા, પાન, એકાંત/અનેકાંત દર્શન અને દર્શનધારાના ચાર ઉપશીર્ષકો: **Anek Gujarati 13 pt / weight 700 / line-height 1.15**.
- કથાનું પોતાનું શીર્ષક પણ 13 pt છે; ધારા heading તેની ઉપર છે. આમ મોટા ધારા શીર્ષક અને અંદરના વિષય વચ્ચે સમાન hierarchy છે.
- દર્શનધારામાં ૧, ૨, ૩, ૪ ક્રમે ચાર પૂર્ણ પહોળાઈની rows; બીજી અને ચોથી row gray છે. મૂળ શબ્દો, punctuation અને ક્રમ જાળવ્યાં છે.
- A: inline heading સાથે આડા પટ્ટા. B: અલગ શીર્ષક-કોલમ સાથે table જેવા પટ્ટા. C: અલગ numbered rail અને કાળી ધારવાળા પટ્ટા.
- કથાનું square clipart 32 mm કર્યું; body 11 pt / 1.38 યથાવત્ છે. આ ફેરફારથી મોટા સમાન ઉપશીર્ષકો અને ચાર rows વાંચનક્ષમ રીતે fit થાય છે.
- મુખ્ય `chapter_001.html`માં વપરાશકર્તાની પસંદગી C છે. A/B/C અને comparison pageથી બધા વિકલ્પો ખોલી શકાય છે. પસંદગી માત્ર striped styleની છે; આખા પુસ્તક કે press fileની મંજૂરી માનેલી નથી.

## ચકાસણી

ત્રણેય samplesમાં Chromium screen તથા print media તપાસ્યાં; fonts ready અને image decode પછી screenshots અને DOM માપ લીધાં. બધા છ headings તથા બધા subsection headingsના computed font family/size/weight સરખાવ્યાં.

| વિકલ્પ | અગાઉના pilotના text blocks | Canvas | Overflow / collisions / browser errors | જમણું content end / footer top |
|---|---|---|---|---|
| A | 26/26, ક્રમ યોગ્ય | 165.1 × 241.3 mm | 0 / 0 / 0 | 217.96 / 224.42 mm |
| B | 26/26, ક્રમ યોગ્ય | 165.1 × 241.3 mm | 0 / 0 / 0 | 217.17 / 224.42 mm |
| C | 26/26, ક્રમ યોગ્ય | 165.1 × 241.3 mm | 0 / 0 / 0 | 217.96 / 224.42 mm |

ત્રણેયમાં ડાબું content 221.71 mm પર સમાપ્ત થાય છે; footer rule 224.42 mm પર છે. માપેલું clearance લગભગ 2.71 mm છે. Text overflow છુપાવેલું નથી. જૂનું PDF hashથી યથાવત્ હોવાનું ચકાસ્યું છે. આ કામમાં source output file લખેલી નથી. Heading/source-manifest સરખામણી formatting દૂર કરીને whitespace normalize કરે છે; આખા Markdownનો byte-for-byte HTML દાવો નથી.

**લખાણ અંગે નોંધ:** live output sourceનો hash અગાઉના pilot manifestથી અલગ છે. Outputમાં રૂપક, સ્વરૂપ, ઉદાહરણો, મર્મ, કાવ્ય/સાધના અને દર્શનધારાના કેટલાક મુદ્દા બદલાયેલા મળ્યા છે. અહીં 26/26નો અર્થ અગાઉના HTML pilotનું લખાણ જાળવ્યું છે એવો છે; latest output સાથે સંપૂર્ણ source coverage પાસ થયાનું પ્રમાણપત્ર નથી. આ request fonts અને striped layout અંગે હોવાથી નવા outputનું લખાણ આપમેળે merge કરેલું નથી. આગળ final content sync જરૂરી છે.

## બાકી માનવીય review

પટ્ટાની શૈલી, printed-size readability અને Gujarati proofની માનવીય સમીક્ષા બાકી છે. આ roundમાં PDF બનાવેલું નથી. જૂનું `chapter_001.pdf` આ samplesનું પ્રતિનિધિત્વ કરતું નથી. PDF fonts/MediaBox, final book parity તથા press certification નવી PDF બન્યા પછી તપાસવાનાં છે.

## ફાઇલો

નીચેના દરેક pathનું root `D:/PROJECT_WORK/NayaPrakash_Book/` છે. `before_chapter_001.html` માત્ર સુરક્ષિત backup છે; તેનો મૂળ relative asset base pilot folder હતો. Review માટે option files અથવા મુખ્ય HTML ખોલવાં.

- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/before_chapter_001.html`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/html-audit.json`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/index.html`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_a.html`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_a_darshan.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_a_right_page.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_a_spread.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_b.html`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_b_darshan.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_b_right_page.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_b_spread.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_c.html`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_c_darshan.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_c_right_page.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/option_c_spread.png`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/QA_REPORT.md`
- `sankshipt/pilot_chapter_001/revisions/section_styles_20261106_r02/comparison-preview.png`
- `sankshipt/pilot_chapter_001/chapter_001.html`
- `tmp/codex/section-styles-r02/build.py`
- `tmp/codex/section-styles-r02/audit.cjs`
- `tmp/codex/section-styles-r02/package.py`
- `tmp/codex/section-styles-r02/check-gallery.cjs`

## Hash receipt

```text
D:\PROJECT_WORK\NayaPrakash_Book\sankshipt\pilot_chapter_001\chapter_001.html
SHA256 7b8f1cc0f1ace406a3a7fd6a6a487eb1120d48ae3145e5b14d6663552bc0b203
D:\PROJECT_WORK\NayaPrakash_Book\sankshipt\pilot_chapter_001\revisions\section_styles_20261106_r02\before_chapter_001.html
SHA256 62bfe72a603328e08a48ec053235ee8d69a95681c74a41b5d013e38aded56b27
D:\PROJECT_WORK\NayaPrakash_Book\sankshipt\pilot_chapter_001\chapter_001.pdf
SHA256 b8b635f9d5de1124a12ca3b3ae759cfc3a96e9d8030cfeea82323438e9bbca8c
D:\PROJECT_WORK\NayaPrakash_Book\sankshipt\output\khanda_1_naigam\chapter_001_bhuta_naigam_naya_gu.md
SHA256 ac36820fc71625530d77519c6c6cb7180f18c7f82a71a063e5a16bd4965772be
```
