# HTMLમાં ચિત્ર ગોઠવવાની નોંધ

`chapter-image-map.json`માંથી પ્રકરણનો `key` અથવા ચોક્કસ `source_file` શોધીને `html_src` પસંદ કરવો. માત્ર numeric chapter filename પર join ન કરવો: અલગ ખંડમાં સ્થાનિક ક્રમ ફરી આવી શકે છે.

`html_src` project rootથી relative છે. HTML જો nested folderમાં હોય તો તેના folder મુજબ relative prefix ગણવો. ફાઇલનાં નામ અને ખંડના identifiers બદલવા નહીં.

```html
<img class="katha-art"
     src="Image/press/K01_C001_chapter_001_bhuta_naigam_naya_katha_r01_press.png"
     alt="દાદાજીના સમજાવવાથી પિતા અને પુત્ર વચ્ચે સમાધાન">
```

```css
.katha-art {
  width: 50mm;
  height: 50mm;
  object-fit: contain;
}
```

બંને physical dimensions સમાન રાખવા. `object-fit: cover` કે અસમાન stretchથી ચહેરો/હાથ/મુખ્ય વસ્તુ crop ન કરવી. સફેદ padding ચિત્રનો જ ભાગ છે. Caption/alt લખાણ કથાના અર્થ અને વાસ્તવિક દૃશ્ય પ્રમાણે માનવીય સમીક્ષા પછી નક્કી કરવું.

મૂળ ચિત્રનું requested માપ અને ખરેખર મળેલું માપ જુદાં હોઈ શકે છે. વાસ્તવિક `pixel_qa.width_px`, `height_px` અને `max_width_mm_at_600dpi` વાંચવા. 1254 px માટે 50 mm પર આશરે 637 effective DPI અને 600 DPI પર મહત્તમ 53.086 mm છે. DPI metadata બદલીને વધુ resolution મળતું નથી.

આ asset setને HTMLમાં ગોઠવ્યા પછી font/image load, overlap, crop અને actual PDFમાં contrastની ફરી ચકાસણી કરવી. પુસ્તકનું અંતિમ trim 6.5 × 9.5 ઇંચ છે; ચિત્રનું 1:1 પ્રમાણ પુસ્તકના page sizeથી સ્વતંત્ર છે.

Press PNGનું pixel validation પૂર્ણ હોવા છતાં વાર્તા-સંગતિ, ધાર્મિક ચિત્રણ, 50 mm કાગળ proof અને press certification માનવીય રીતે મંજૂર થયાં નથી.
