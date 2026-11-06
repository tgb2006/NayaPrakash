from pathlib import Path

file_path = Path('sankshipt/pilot_long_title_ch070/chapter_070.html')
content = file_path.read_text(encoding='utf-8')

# 1. Update CSS
old_css = """    .tattva-infographic-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 8pt 10pt;
      flex: 1;
      margin-bottom: 5pt;
      min-height: 0;
    }

    .tattva-card-shell {
      position: relative;
      background: #ffffff;
      border: 0.8pt solid #c8c8c8;
      border-radius: 6pt;
      padding: 5.5pt 8pt;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1.5pt 4pt rgba(0, 0, 0, 0.03);
      z-index: 1;
    }"""

new_css = """    .tattva-infographic-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 5pt 8pt;
      flex: 1;
      margin-bottom: 3.5pt;
      min-height: 0;
    }

    .tattva-card-shell {
      position: relative;
      background: #ffffff;
      border: 0.75pt solid #c8c8c8;
      border-radius: 5pt;
      padding: 4.5pt 7pt;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1.2pt 3pt rgba(0, 0, 0, 0.02);
      z-index: 1;
      overflow: hidden;
    }"""

old_top_row = """    .card-top-row {
      display: flex;
      align-items: flex-start;
      gap: 6pt;
      margin-bottom: 4.5pt;
      padding-bottom: 2.5pt;
      border-bottom: 0.6pt solid #eaeaea;
    }"""

new_top_row = """    .card-top-row {
      display: flex;
      align-items: flex-start;
      gap: 5pt;
      margin-bottom: 3.5pt;
      padding-bottom: 2pt;
      border-bottom: 0.6pt solid #eaeaea;
    }"""

old_ribbon = """    .bottom-ribbon-shell {
      margin-top: 5pt;
      background: #fafafa;
      border: 0.6pt solid #d0d0d0;
      border-left: 2.6pt solid #111111;
      border-radius: 0 4pt 4pt 0;
      padding: 4.5pt 8pt;
      margin-bottom: 0;
    }"""

new_ribbon = """    .bottom-ribbon-shell {
      margin-top: 3.5pt;
      background: #fafafa;
      border: 0.6pt solid #d0d0d0;
      border-left: 2.6pt solid #111111;
      border-radius: 0 4pt 4pt 0;
      padding: 3.5pt 7.5pt;
      margin-bottom: 0;
    }"""

# 2. Update Card 1 & Card 3 text in Chapter 070
old_c1_text = """            ઝડપથી વહેતી પહાડી નદીના પાણી પર ક્ષણે ક્ષણે હજારો ફીણ અને પરપોટા જન્મે છે અને બીજી જ ક્ષણે ફૂટીને વિલીન થઈ જાય છે. એક પરપોટો બીજા સમય સુધી ટકતો નથી. સામાન્ય માણસ પાણીની સ્થિરતાને ગૌણ કરીને કેવળ પરપોટાની ક્ષણિકતાને જુએ છે. તેવી જ રીતે ત્રિકાળી ધ્રુવ દ્રવ્યસત્તાને ગૌણ કરી, કેવળ પ્રત્યેક સમયે થતા પર્યાયોના ઉત્પાદ-વ્યયરૂપ વિનાશી સ્વભાવને આગળ રાખીને — <em>"સંસારનો પ્રત્યેક પર્યાય એક સમયનો છે, અનિત્ય અને ક્ષણભંગુર છે"</em> — એમ પ્રતિપાદન કરવામાં આવે ત્યારે તે આ નય કહેવાય છે."""

new_c1_text = """            ઝડપથી વહેતી પહાડી નદીના પાણી પર ક્ષણે ક્ષણે હજારો પરપોટા જન્મે છે અને બીજી જ ક્ષણે ફૂટીને વિલીન થઈ જાય છે; કોઈ પરપોટો બીજા સમય સુધી ટકતો નથી. સામાન્ય દ્રષ્ટિ પાણીના ધ્રુવ પ્રવાહને ગૌણ કરી કેવળ પરપોટાની ક્ષણિકતાને જુએ છે. તેવી જ રીતે ત્રિકાળી ધ્રુવ દ્રવ્યસત્તાને ગૌણ કરી, પ્રત્યેક સમયના ઉત્પાદ-વ્યયરૂપ વિનાશી સ્વભાવને આગળ રાખી—<em>"સંસારનો પ્રત્યેક પર્યાય ક્ષણભંગુર છે"</em>—એમ પ્રતિપાદન કરવું તે આ નય છે."""

old_c3_text = """          <ul class="card-bullet-list">
            <li><strong>અનિત્ય ભાવના:</strong> "ધન યૌવન ને રૂપ વાદળ જેવાં અનિત્ય છે; સર્વ ભોગ ક્ષણભંગુર છે."</li>
            <li><strong>દીપકની જ્યોત:</strong> પ્રત્યેક સમયે જૂની જ્યોતિ બુઝાય છે ને નવો તેજ-પર્યાય પ્રગટે છે.</li>
            <li><strong>આયુષ્યનો ક્ષય:</strong> ઘડિયાળના કાંટાની જેમ દેહનું આયુષ્ય પ્રત્યેક પળે ઘટી રહ્યું છે.</li>
          </ul>"""

new_c3_text = """          <ul class="card-bullet-list">
            <li><strong>અનિત્ય ભાવના:</strong> ધન, યૌવન અને ભોગો વાદળ સમાન ક્ષણભંગુર છે.</li>
            <li><strong>દીપકની જ્યોત:</strong> પ્રત્યેક સમયે જૂની જ્યોતિ બુઝાઈ નવો તેજ-પર્યાય પ્રગટે છે.</li>
            <li><strong>આયુષ્યનો ક્ષય:</strong> ઘડિયાળના કાંટાની જેમ દેહનું આયુષ્ય પળે પળે ઘટી રહ્યું છે.</li>
          </ul>"""

def norm(t): return t.replace('\r\n', '\n')

content_norm = norm(content)
assert norm(old_css) in content_norm, "old_css not found"
assert norm(old_top_row) in content_norm, "old_top_row not found"
assert norm(old_ribbon) in content_norm, "old_ribbon not found"
assert norm(old_c1_text) in content_norm, "old_c1_text not found"
assert norm(old_c3_text) in content_norm, "old_c3_text not found"

content_norm = content_norm.replace(norm(old_css), norm(new_css))
content_norm = content_norm.replace(norm(old_top_row), norm(new_top_row))
content_norm = content_norm.replace(norm(old_ribbon), norm(new_ribbon))
content_norm = content_norm.replace(norm(old_c1_text), norm(new_c1_text))
content_norm = content_norm.replace(norm(old_c3_text), norm(new_c3_text))

file_path.write_text(content_norm, encoding='utf-8')
print("Applied Chapter 070 updates successfully!")
