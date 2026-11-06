import re
from pathlib import Path

html_path = Path("sankshipt/pilot_chapter_001/chapter_001.html")
html = html_path.read_text(encoding="utf-8")

# CSS replacement: Replace tattva-magazine-grid through duo-ribbon
old_tattva_css = """    /* Tattvadhara 2-Column Magazine Grid */
    .tattva-magazine-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 5.8mm; /* Standard 5.8mm column gap */
      row-gap: 7pt;
      flex: 1;
    }

    .tattva-feature-block {
      font-size: 10.2pt;
      line-height: 1.38;
      color: #222222;
      text-align: justify;
      text-justify: inter-word;
    }

    .tattva-feature-block .block-kicker {
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.2pt;
      color: #0d0d0d;
      display: block;
      margin-bottom: 2pt;
      border-bottom: 0.6pt solid #e0e2e6;
      padding-bottom: 1.5pt;
      letter-spacing: 0.1pt;
    }

    .tattva-feature-block p {
      margin: 0;
    }

    /* Real-Life Vignettes Card (Point 3) */
    .vignettes-card {
      background: #fafbfc;
      border: 0.6pt solid #d8dbdf;
      border-radius: 2pt;
      padding: 4pt 6pt;
      margin-top: 2pt;
    }

    .vignette-item {
      position: relative;
      padding-left: 9pt;
      margin-bottom: 2pt;
      font-size: 9.6pt;
      line-height: 1.34;
    }

    .vignette-item:last-child {
      margin-bottom: 0;
    }

    .vignette-item::before {
      content: "▪";
      position: absolute;
      left: 0;
      top: 0;
      color: #333333;
      font-size: 7pt;
    }

    .vignette-item strong {
      color: #111111;
    }"""

new_tattva_css = """    /* =============================================================
       TATTVADHARA: 4-QUADRANT EDITORIAL INFOGRAPHIC CARDS
       Monochrome / Grayscale Editorial Design with Center Crossroads Icons
       ============================================================= */
    .tattva-magazine-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 5.8mm;
      row-gap: 7pt;
      margin-top: 2pt;
      margin-bottom: 2pt;
    }

    .tattva-card-shell {
      position: relative;
      background: #ffffff;
      border: 0.75pt solid #d0d4da;
      border-radius: 6pt;
      padding: 6pt 8pt;
      box-shadow: 0 1.5pt 4pt rgba(0,0,0,0.03);
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      box-sizing: border-box;
      min-height: 98pt;
    }

    /* Outer offset corner backing layer (Grayscale accent) */
    .tattva-card-1::before {
      content: "";
      position: absolute;
      top: -2.5pt;
      left: -2.5pt;
      width: 100%;
      height: 100%;
      background: #111111;
      border-radius: 7pt;
      z-index: -1;
    }

    .tattva-card-2::before {
      content: "";
      position: absolute;
      top: -2.5pt;
      right: -2.5pt;
      width: 100%;
      height: 100%;
      background: #2b2e33;
      border-radius: 7pt;
      z-index: -1;
    }

    .tattva-card-3::before {
      content: "";
      position: absolute;
      bottom: -2.5pt;
      left: -2.5pt;
      width: 100%;
      height: 100%;
      background: #3a3e45;
      border-radius: 7pt;
      z-index: -1;
    }

    .tattva-card-4::before {
      content: "";
      position: absolute;
      bottom: -2.5pt;
      right: -2.5pt;
      width: 100%;
      height: 100%;
      background: #1a1a1a;
      border-radius: 7pt;
      z-index: -1;
    }

    /* Center crossroads icon tabs */
    .center-icon-tab {
      position: absolute;
      width: 19pt;
      height: 19pt;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2;
    }

    .center-icon-tab svg {
      width: 10.5pt;
      height: 10.5pt;
      fill: #ffffff;
    }

    /* Card 1: Bottom-Right (facing center) */
    .tattva-card-1 .center-icon-tab {
      bottom: 0;
      right: 0;
      background: #111111;
      border-radius: 7pt 0 5pt 0;
    }

    /* Card 2: Bottom-Left (facing center) */
    .tattva-card-2 .center-icon-tab {
      bottom: 0;
      left: 0;
      background: #2b2e33;
      border-radius: 0 7pt 0 5pt;
    }

    /* Card 3: Top-Right (facing center) */
    .tattva-card-3 .center-icon-tab {
      top: 0;
      right: 0;
      background: #3a3e45;
      border-radius: 0 5pt 0 7pt;
    }

    /* Card 4: Top-Left (facing center) */
    .tattva-card-4 .center-icon-tab {
      top: 0;
      left: 0;
      background: #1a1a1a;
      border-radius: 5pt 0 7pt 0;
    }

    /* Card Headers */
    .card-top-row {
      display: flex;
      align-items: center;
      gap: 4.5pt;
      margin-bottom: 3.5pt;
      padding-bottom: 2pt;
      border-bottom: 0.6pt solid #e6e9ee;
    }

    .tattva-card-3 .card-top-row {
      padding-right: 20pt; /* clearance for top-right icon tab */
    }

    .tattva-card-4 .card-top-row {
      padding-left: 20pt; /* clearance for top-left icon tab */
      justify-content: flex-end;
    }

    .card-step-badge {
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 7.2pt;
      font-weight: 700;
      padding: 1.5pt 4pt;
      border-radius: 2pt;
      color: #ffffff;
      letter-spacing: 0.3pt;
      line-height: 1.1;
      flex-shrink: 0;
    }

    .tattva-card-1 .card-step-badge { background: #111111; }
    .tattva-card-2 .card-step-badge { background: #2b2e33; }
    .tattva-card-3 .card-step-badge { background: #3a3e45; }
    .tattva-card-4 .card-step-badge { background: #1a1a1a; }

    .card-header-titles {
      display: flex;
      align-items: baseline;
      gap: 4pt;
      overflow: hidden;
    }

    .card-main-heading {
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 9.8pt;
      font-weight: 700;
      color: #111111;
      line-height: 1.25;
      letter-spacing: 0.1pt;
      white-space: nowrap;
    }

    .card-sub-kicker {
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt;
      font-weight: 600;
      color: #555555;
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .card-body-text {
      font-size: 9.2pt;
      line-height: 1.34;
      color: #222222;
      text-align: justify;
      text-justify: inter-word;
      margin: 0;
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
      font-size: 8.9pt;
      line-height: 1.32;
      color: #222222;
    }

    .card-vignette-item::before {
      content: "▪";
      position: absolute;
      left: 0;
      top: 0;
      font-size: 6.5pt;
      color: #333333;
    }

    .card-vignette-item strong {
      color: #111111;
    }"""

# HTML replacement: Replace tattva-magazine-grid inner contents
old_grid_html = """      <!-- 2-Column Tattvadhara Grid -->
      <div class="tattva-magazine-grid">
        <!-- 1. Rupak Drishti -->
        <div class="tattva-feature-block" id="p-001-rupak">
          <span class="block-kicker">૧. રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>
            અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.
          </p>
        </div>

        <!-- 2. Swarup Srishti -->
        <div class="tattva-feature-block" id="p-001-swarup">
          <span class="block-kicker">૨. સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>
            ભૂતકાળમાં જે ઘટના ઘટી ગઈ છે કે જે પર્યાય પૂર્ણ થઈ ગયો છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.
          </p>
        </div>

        <!-- 3. Vyavahar Prishti (Stylized Vignettes) -->
        <div class="tattva-feature-block" id="p-001-vyavahar">
          <span class="block-kicker">૩. વ્યવહાર-પૃષ્ટિ: જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
          <div class="vignettes-card">
            <div class="vignette-item">
              <strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.
            </div>
            <div class="vignette-item">
              <strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.
            </div>
            <div class="vignette-item">
              <strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em>
            </div>
          </div>
        </div>

        <!-- 4. Marm Tushti -->
        <div class="tattva-feature-block" id="p-001-marm">
          <span class="block-kicker">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>
            ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.
          </p>
        </div>
      </div>"""

new_grid_html = """      <!-- 2-Column Tattvadhara Infographic Grid (Grayscale 4-Quadrant Design) -->
      <div class="tattva-magazine-grid">
        <!-- 1. Rupak Drishti -->
        <div class="tattva-card-shell tattva-card-1" id="p-001-rupak">
          <!-- Center Crossroads Icon Tab (Bottom-Right) -->
          <div class="center-icon-tab">
            <svg viewBox="0 0 24 24"><polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/></svg>
          </div>
          <div class="card-top-row">
            <span class="card-step-badge">૦૧</span>
            <div class="card-header-titles">
              <span class="card-main-heading">રૂપક-દ્રષ્ટિ:</span>
              <span class="card-sub-kicker">ઓલવાયેલા તારકનું જીવંત કિરણ</span>
            </div>
          </div>
          <p class="card-body-text">
            અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.
          </p>
        </div>

        <!-- 2. Swarup Srishti -->
        <div class="tattva-card-shell tattva-card-2" id="p-001-swarup">
          <!-- Center Crossroads Icon Tab (Bottom-Left) -->
          <div class="center-icon-tab">
            <svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
          </div>
          <div class="card-top-row">
            <span class="card-step-badge">૦૨</span>
            <div class="card-header-titles">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">કાળના પડદા પાર જોતી આંખ</span>
            </div>
          </div>
          <p class="card-body-text">
            ભૂતકાળમાં જે ઘટના ઘટી ગઈ છે કે જે પર્યાય પૂર્ણ થઈ ગયો છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.
          </p>
        </div>

        <!-- 3. Vyavahar Prishti -->
        <div class="tattva-card-shell tattva-card-3" id="p-001-vyavahar">
          <!-- Center Crossroads Icon Tab (Top-Right) -->
          <div class="center-icon-tab">
            <svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>
          </div>
          <div class="card-top-row">
            <span class="card-step-badge">૦૩</span>
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

        <!-- 4. Marm Tushti -->
        <div class="tattva-card-shell tattva-card-4" id="p-001-marm">
          <!-- Center Crossroads Icon Tab (Top-Left) -->
          <div class="center-icon-tab">
            <svg viewBox="0 0 24 24"><path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99zM11 10h2v4h-2zm0 6h2v2h-2z"/></svg>
          </div>
          <div class="card-top-row">
            <span class="card-step-badge">૦૪</span>
            <div class="card-header-titles">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
            </div>
          </div>
          <p class="card-body-text">
            ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.
          </p>
        </div>
      </div>"""

# Normalize
html_norm = html.replace("\r\n", "\n")
old_css_norm = old_tattva_css.replace("\r\n", "\n")
new_css_norm = new_tattva_css.replace("\r\n", "\n")
old_grid_norm = old_grid_html.replace("\r\n", "\n")
new_grid_norm = new_grid_html.replace("\r\n", "\n")

if old_css_norm in html_norm:
    html_norm = html_norm.replace(old_css_norm, new_css_norm)
    print("SUCCESS: Replaced Tattvadhara CSS")
else:
    print("ERROR: old_css_norm not found")

if old_grid_norm in html_norm:
    html_norm = html_norm.replace(old_grid_norm, new_grid_norm)
    print("SUCCESS: Replaced Tattvadhara HTML Grid")
else:
    print("ERROR: old_grid_norm not found")

html_path.write_text(html_norm, encoding="utf-8")
print("Saved updated chapter_001.html")
