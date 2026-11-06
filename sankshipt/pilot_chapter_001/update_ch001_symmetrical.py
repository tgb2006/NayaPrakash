import re
from pathlib import Path

file_path = Path('sankshipt/pilot_chapter_001/chapter_001.html')
content = file_path.read_text(encoding='utf-8')

# 1. Update CSS in Chapter 001
# Replace card styling
css_pattern = re.compile(r'/\* Outer offset corner backing layer[\s\S]*?\.card-vignette-item strong\s*\{[^}]*\}', re.MULTILINE)

new_card_css = """    /* Symmetrical Header Rows */
    .card-top-row {
      display: flex;
      align-items: flex-start;
      gap: 5pt;
      margin-bottom: 3.5pt;
      padding-bottom: 2pt;
      border-bottom: 0.6pt solid #eaeaea;
    }

    /* Left column cards (01 & 03): Badge on Left */
    .card-top-row.header-left {
      justify-content: flex-start;
      text-align: left;
    }

    /* Right column cards (02 & 04): Badge on Right (Mirrored Symmetry) */
    .card-top-row.header-right {
      justify-content: flex-end;
      text-align: right;
    }

    /* Step Badges */
    .step-badge {
      background: #111111;
      color: #ffffff;
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt;
      font-weight: 700;
      padding: 1.5pt 4.2pt;
      border-radius: 2.2pt;
      letter-spacing: 0.2pt;
      flex-shrink: 0;
      line-height: 1.1;
      margin-top: 1pt;
    }

    .card-header-titles {
      display: flex;
      flex-direction: column;
    }

    .card-header-titles.text-right {
      align-items: flex-end;
      text-align: right;
    }

    .card-main-heading {
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.5pt;
      color: #0d0d0d;
      line-height: 1.15;
    }

    .card-sub-kicker {
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 600;
      font-size: 9.3pt;
      color: #444444;
      line-height: 1.18;
    }

    /* MANDATORY 11.0 PT BODY TEXT */
    .card-body-text {
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.35;
      color: #222222;
      text-align: justify;
      hyphens: auto;
      margin: 0;
      flex: 1;
    }

    /* Card 3 Vignette Bullets */
    .card-vignette-list {
      margin: 0;
      padding: 0;
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 2pt;
    }

    .card-vignette-item {
      position: relative;
      padding-left: 8pt;
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.34;
      color: #222222;
      text-align: justify;
    }

    .card-vignette-item::before {
      content: "•";
      position: absolute;
      left: 0;
      top: -0.5pt;
      font-size: 9.5pt;
      color: #333333;
    }

    .card-vignette-item strong {
      font-weight: 700;
      color: #111111;
    }"""

content = css_pattern.sub(new_card_css, content)

# Also update .tattva-card-shell in Chapter 001
content = re.sub(
    r'\.tattva-card-shell\s*\{[^}]*\}',
    """.tattva-card-shell {
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
    }""",
    content
)

# Also update .tattva-infographic-grid in Chapter 001
content = re.sub(
    r'\.tattva-infographic-grid\s*\{[^}]*\}',
    """.tattva-infographic-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 5pt 8pt;
      flex: 1;
      margin-bottom: 3.5pt;
      min-height: 0;
    }""",
    content
)

# 2. Update 4 Cards HTML in Chapter 001
grid_pattern = re.compile(r'<div class="tattva-infographic-grid">[\s\S]*?</div>\s*<!-- Kavyadhara', re.MULTILINE)

new_grid_html = """<div class="tattva-infographic-grid">
        <!-- 1. Rupak Drishti (Left Aligned Badge 01) -->
        <div class="tattva-card-shell tattva-card-1" id="p-001-rupak">
          <div class="card-top-row header-left">
            <span class="step-badge">૦૧</span>
            <div class="card-header-titles">
              <span class="card-main-heading">રૂપક-દ્રષ્ટિ:</span>
              <span class="card-sub-kicker">ઓલવાયેલા તારકનું જીવંત કિરણ</span>
            </div>
          </div>
          <p class="card-body-text">
            અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.
          </p>
        </div>

        <!-- 2. Swarup Srishti (Right Aligned Badge 02) -->
        <div class="tattva-card-shell tattva-card-2" id="p-001-swarup">
          <div class="card-top-row header-right">
            <div class="card-header-titles text-right">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">કાળના પડદા પાર જોતી આંખ</span>
            </div>
            <span class="step-badge">૦૨</span>
          </div>
          <p class="card-body-text">
            ભૂતકાળમાં જે ઘટના ઘટી ગઈ છે કે જે પર્યાય પૂર્ણ થઈ ગયો છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.
          </p>
        </div>

        <!-- 3. Vyavahar Pushti (Left Aligned Badge 03) -->
        <div class="tattva-card-shell tattva-card-3" id="p-001-vyavahar">
          <div class="card-top-row header-left">
            <span class="step-badge">૦૩</span>
            <div class="card-header-titles">
              <span class="card-main-heading">વ્યવહાર-પૃષ્ટિ:</span>
              <span class="card-sub-kicker">જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
            </div>
          </div>
          <ul class="card-vignette-list">
            <li class="card-vignette-item">
              <strong>દિવાળીનો દીવો:</strong> બાળક પોકારે: <em>"આજે પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજ જેવી જ જીવંત બને છે.
            </li>
            <li class="card-vignette-item">
              <strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુત્રને વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી હૈયે ચાંપે છે; આંખમાં અતીત-બાળપણ રમે છે.
            </li>
            <li class="card-vignette-item">
              <strong>બીજ અને જળ:</strong> ગોટલી જોઈ <em>"આ મારો આંબો છે"</em> અને જળ જોઈ <em>"આ હિમાલયનો બરફ છે"</em> કહેવાય.
            </li>
          </ul>
        </div>

        <!-- 4. Marm Tushti (Right Aligned Badge 04) -->
        <div class="tattva-card-shell tattva-card-4" id="p-001-marm">
          <div class="card-top-row header-right">
            <div class="card-header-titles text-right">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
            </div>
            <span class="step-badge">૦૪</span>
          </div>
          <p class="card-body-text">
            ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.
          </p>
        </div>
      </div>

      <!-- Kavyadhara"""

content = grid_pattern.sub(new_grid_html, content)

file_path.write_text(content, encoding='utf-8')
print("Chapter 001 updated successfully!")
