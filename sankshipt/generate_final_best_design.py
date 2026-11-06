import subprocess
from pathlib import Path
from PIL import Image

def generate_chapter_070():
    pilot_dir = Path("sankshipt/pilot_long_title_ch070").resolve()
    fonts_dir = Path("sankshipt/pilot_chapter_001/assets/fonts").resolve()
    html_path = pilot_dir / "chapter_070.html"
    pdf_path = pilot_dir / "chapter_070.pdf"
    spread_img = pilot_dir / "chapter_070_spread_preview.png"
    p2_img = pilot_dir / "page_002_left_preview.png"
    p3_img = pilot_dir / "page_003_right_preview.png"
    tattva_zoom = pilot_dir / "tattvadhara_best_design_zoom.png"
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>૭૦. સત્તાગૌણ ઉત્પાદ-વ્યયગ્રાહક અશુદ્ધ પર્યાયાર્થિક પ્રતિપાદક વ્યવહાર — નય-ચક્ષુ (Best Editorial Design)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 400;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 600;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-SemiBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 700;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-Bold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 800;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-ExtraBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 400;
      src: url('file:///{fonts_dir.as_posix()}/NotoSansGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 700;
      src: url('file:///{fonts_dir.as_posix()}/NotoSansGujarati-Bold.ttf') format('truetype');
    }}

    @page {{
      size: 6.5in 9.5in;
      margin: 0;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      padding: 0;
      background: #e9eaec;
      font-family: 'Noto Sans Gujarati', sans-serif;
      color: #1a1a1a;
      -webkit-font-smoothing: antialiased;
    }}

    .spread-container {{
      display: flex;
      justify-content: center;
      gap: 16px;
      padding: 24px;
      margin: 0 auto;
    }}

    .page {{
      width: 6.5in;
      height: 9.5in;
      background: #ffffff;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }}

    @media print {{
      body {{
        background: none;
      }}
      .spread-container {{
        padding: 0;
        gap: 0;
        display: block;
      }}
      .page {{
        box-shadow: none;
        page-break-after: always;
        break-after: page;
        float: none;
      }}
    }}

    .page-even {{
      padding: 11.5mm 14mm 11.5mm 12.5mm;
    }}

    .page-odd {{
      padding: 11.5mm 12.5mm 11.5mm 14mm;
    }}

    .page-canvas {{
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: 0;
    }}

    /* Footers */
    .running-footer {{
      margin-top: auto;
      padding-top: 4.5pt;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 0.6pt solid #cfcfcf;
      font-size: 9.2pt;
      color: #555555;
      position: relative;
      z-index: 10;
    }}

    .running-footer .page-num {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-weight: 700;
      color: #111111;
      font-size: 11.0pt;
    }}

    .running-footer .footer-label {{
      display: flex;
      align-items: center;
      gap: 5pt;
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 500;
    }}

    .running-footer .footer-book {{
      font-weight: 700;
      color: #222222;
    }}

    .running-footer .footer-sep {{
      color: #888888;
    }}

    /* Chapter Masthead */
    .chapter-masthead {{
      margin-bottom: 3.5pt;
    }}

    .kicker-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2.5pt;
    }}

    .khanda-pill {{
      background: #111111;
      color: #ffffff;
      padding: 2.2pt 6.5pt;
      border-radius: 2pt;
      font-size: 8.8pt;
      font-weight: 700;
      letter-spacing: 0.2pt;
      display: inline-flex;
      align-items: center;
      gap: 4pt;
    }}

    .khanda-pill-sub {{
      color: #b0b0b0;
      font-weight: 500;
      font-size: 8.2pt;
      border-left: 0.6pt solid #555555;
      padding-left: 4pt;
    }}

    .category-tag {{
      font-size: 8.8pt;
      color: #333333;
      font-weight: 600;
      border: 0.6pt solid #b0b0b0;
      padding: 1.8pt 5.5pt;
      border-radius: 2pt;
      background: #f7f7f7;
    }}

    .chapter-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 8pt;
      margin-top: 1.5pt;
      margin-bottom: 2pt;
    }}

    .chapter-main-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 800;
      color: #000000;
      letter-spacing: -0.3pt;
      margin: 0;
      flex: 1;
    }}

    .chapter-main-title.title-long {{
      font-size: 14.8pt;
      line-height: 1.16;
    }}

    .chapter-sub-meta-right {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      text-align: right;
      gap: 1.5pt;
      flex-shrink: 0;
      max-width: 48%;
    }}

    .gu-general-term {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.2pt;
      color: #111111;
      line-height: 1.18;
    }}

    .en-concept {{
      font-family: 'Cinzel', serif;
      font-size: 8.0pt;
      font-weight: 600;
      color: #666666;
      font-style: italic;
      line-height: 1.18;
      letter-spacing: 0.15pt;
    }}

    .sutra-showcase {{
      margin-top: 2.5pt;
      background: #f8f9fa;
      border-left: 2.8pt solid #111111;
      padding: 2pt 5.5pt;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-radius: 0 2pt 2pt 0;
      gap: 8pt;
    }}

    .sutra-devanagari {{
      font-family: 'Noto Sans Devanagari', 'Anek Devanagari', serif;
      font-size: 9.8pt;
      font-weight: 600;
      color: #111111;
      letter-spacing: 0.2pt;
      line-height: 1.22;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    .sutra-label {{
      font-size: 7.6pt;
      font-weight: 600;
      color: #666666;
      text-transform: uppercase;
      letter-spacing: 0.4pt;
      flex-shrink: 0;
    }}

    .section-ribbon {{
      display: flex;
      align-items: center;
      gap: 6pt;
      margin-top: 2.5pt;
      margin-bottom: 3.5pt;
    }}

    .ribbon-badge {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 800;
      font-size: 9.8pt;
      color: #000000;
      letter-spacing: 0.3pt;
      display: flex;
      align-items: center;
      gap: 4.5pt;
    }}

    .ribbon-badge::before {{
      content: "■";
      font-size: 7.2pt;
      color: #000000;
    }}

    .ribbon-rule {{
      flex: 1;
      height: 0.6pt;
      background: #d8d8d8;
    }}

    /* -------------------------------------------------------------
       BEST GRAPHIC DESIGN: TATTVADHARA 4-CARD GRID
       Harmonious Left-to-Right Reading Hierarchy, 11.0 pt Body
       ------------------------------------------------------------- */
    .tattva-infographic-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 5pt 8pt;
      flex: 1;
      margin-bottom: 3.5pt;
      min-height: 0;
    }}

    .tattva-card-shell {{
      position: relative;
      background: #ffffff;
      border: 0.75pt solid #c8cbcf;
      border-radius: 4.5pt;
      padding: 4.5pt 7pt;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1.2pt 3pt rgba(0, 0, 0, 0.02);
      z-index: 1;
      overflow: hidden;
    }}

    /* Clean Uniform Header Row (Left-to-Right Natural Flow) */
    .card-top-row {{
      display: flex;
      align-items: flex-start;
      gap: 5.5pt;
      margin-bottom: 3.5pt;
      padding-bottom: 2.2pt;
      border-bottom: 0.6pt solid #e6e8eb;
    }}

    .step-badge {{
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
    }}

    .card-header-titles {{
      display: flex;
      flex-direction: column;
      min-width: 0;
    }}

    .card-main-heading {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.5pt;
      color: #0d0d0d;
      line-height: 1.15;
    }}

    .card-sub-kicker {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 600;
      font-size: 9.3pt;
      color: #4b5563;
      line-height: 1.18;
    }}

    /* STRICT MANDATORY 11.0 PT BODY TEXT */
    .card-body-text {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.34;
      color: #1f2937;
      margin: 0;
      text-align: justify;
      hyphens: auto;
      flex: 1;
    }}

    .card-bullet-list {{
      list-style: none;
      padding: 0;
      margin: 0;
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.32;
      color: #1f2937;
    }}

    .card-bullet-list li {{
      position: relative;
      padding-left: 9pt;
      margin-bottom: 2pt;
      text-align: justify;
    }}

    .card-bullet-list li:last-child {{
      margin-bottom: 0;
    }}

    .card-bullet-list li::before {{
      content: "•";
      position: absolute;
      left: 0;
      top: -0.5pt;
      font-size: 9.5pt;
      color: #333333;
    }}

    .card-bullet-list strong {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-weight: 700;
      color: #0d0d0d;
    }}

    /* DUO-RIBBON (11.0 PT BODY) */
    .bottom-ribbon-shell {{
      margin-top: 3.5pt;
      background: #fafafa;
      border: 0.6pt solid #d0d0d0;
      border-left: 2.6pt solid #111111;
      border-radius: 0 4pt 4pt 0;
      padding: 3.5pt 7.5pt;
      margin-bottom: 0;
    }}

    .duo-ribbon-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12pt;
      align-items: center;
    }}

    .duo-col {{
      display: flex;
      flex-direction: column;
      gap: 1.5pt;
    }}

    .duo-divider-col {{
      border-left: 0.6pt solid #d8d8d8;
      padding-left: 10pt;
    }}

    .duo-label {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 9.0pt;
      color: #333333;
      letter-spacing: 0.3pt;
      display: flex;
      align-items: center;
      gap: 3.5pt;
    }}

    .kavya-quote {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 600;
      font-size: 11.0pt !important;
      line-height: 1.30;
      color: #111111;
      font-style: italic;
      margin: 0;
    }}

    .sadhana-statement {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 10.6pt !important;
      line-height: 1.32;
      color: #222222;
      margin: 0;
      text-align: justify;
    }}

    /* PAGE 3: KATHADHARA, VIVEKDHARA & DARSHANDHARA (11.0 PT) */
    .top-story-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4.5pt;
      padding-bottom: 2.5pt;
      border-bottom: 0.8pt solid #111111;
    }}

    .top-story-header .story-kicker {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.0pt;
      color: #111111;
      letter-spacing: 0.3pt;
    }}

    .top-story-header .story-title-main {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.5pt;
      color: #111111;
    }}

    .story-hero-split {{
      display: grid;
      grid-template-columns: 125pt 1fr;
      gap: 9pt;
      margin-bottom: 5pt;
    }}

    .story-artwork-box {{
      width: 125pt;
      height: 98pt;
      border: 0.6pt solid #c8c8c8;
      background: #fafafa;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 3.5pt;
      border-radius: 2pt;
    }}

    .story-artwork-box svg {{
      width: 100%;
      height: 100%;
    }}

    .story-pipasa-article {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .pipasa-badge {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 8.8pt;
      color: #111111;
      border-bottom: 1.1pt solid #111111;
      display: inline-block;
      margin-bottom: 2.5pt;
      padding-bottom: 0.5pt;
      align-self: flex-start;
    }}

    .story-pipasa-article p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.35;
      color: #242424;
      margin: 0;
      text-align: justify;
    }}

    .story-paan-article {{
      background: #f7f8f9;
      border-left: 2.5pt solid #111111;
      border-top: 0.6pt solid #cfcfcf;
      border-right: 0.6pt solid #cfcfcf;
      border-bottom: 0.6pt solid #cfcfcf;
      padding: 4.5pt 7pt;
      margin-bottom: 4.5pt;
      border-radius: 0 3pt 3pt 0;
    }}

    .story-paan-article p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.35;
      color: #242424;
      margin: 0;
      text-align: justify;
    }}

    .section-divider-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 10.5pt;
      color: #111111;
      margin-bottom: 3.5pt;
      display: flex;
      align-items: center;
      gap: 4.5pt;
    }}

    .section-divider-title::before {{
      content: "❖";
      font-size: 8.5pt;
      color: #111111;
    }}

    .vivek-container {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8pt;
      margin-bottom: 4.5pt;
    }}

    .vivek-card {{
      border: 0.6pt solid #cfcfcf;
      border-radius: 3pt;
      padding: 4.5pt 6pt;
      background: #ffffff;
    }}

    .vivek-card-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 10.2pt;
      color: #111111;
      padding-bottom: 1.5pt;
      border-bottom: 0.6pt solid #e0e0e0;
      margin-bottom: 3pt;
    }}

    .vivek-card p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 10.8pt !important;
      line-height: 1.34;
      color: #242424;
      margin: 0;
      text-align: justify;
    }}

    .darshan-section {{
      margin-top: auto;
      border-top: 0.6pt solid #d0d0d0;
      padding-top: 4pt;
      margin-bottom: 2pt;
    }}

    .darshan-header {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.0pt;
      color: #111111;
      margin-bottom: 3pt;
      display: flex;
      align-items: center;
      gap: 4pt;
    }}

    .darshan-pillars-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3.5pt 8pt;
    }}

    .darshan-pillar-item {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 10.5pt !important;
      line-height: 1.32;
      color: #242424;
      text-align: justify;
    }}

    .darshan-pillar-item strong {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      color: #111111;
    }}
  </style>
</head>
<body>

<div class="spread-container">

  <!-- =============================================================
       LEFT PAGE: PAGE 2 (EVEN PAGE)
       ============================================================= -->
  <section class="page page-even" id="page-2">
    <div class="page-canvas">

      <!-- Chapter Masthead -->
      <div class="chapter-masthead">
        <div class="kicker-row">
          <div class="khanda-pill">
            <span>તૃતીય ખંડ: વ્યવહાર નય</span>
            <span class="khanda-pill-sub">અર્થનય</span>
          </div>
          <div class="category-tag">મુખ્ય શ્રેણી: ઉપચાર - સદ્ભૂત વ્યવહાર</div>
        </div>

        <!-- Adaptive Title Row -->
        <div class="chapter-title-row">
          <h1 class="chapter-main-title title-long" id="p-070-title">૭૦. સત્તાગૌણ ઉત્પાદ-વ્યયગ્રાહક<br>અશુદ્ધ પર્યાયાર્થિક પ્રતિપાદક વ્યવહાર</h1>
          <div class="chapter-sub-meta-right" id="p-070-meta">
            <span class="gu-general-term">અનિત્ય-ક્ષણભંગુર પર્યાયની દ્રષ્ટિ</span>
            <span class="en-concept">The Transient-Mode Standpoint: Flux</span>
          </div>
        </div>

        <!-- Sacred Sutra Epigraph Card -->
        <div class="sutra-showcase">
          <span class="sutra-devanagari">पर्यायविनश्वरत्वप्रतिपादकः सत्तागौणउत्पादव्ययग्राहकअशुद्धपर्यायार्थिकप्रतिपादकव्यवहारः।</span>
          <span class="sutra-label">મૂળ આગમિક લક્ષણ-સૂત્ર</span>
        </div>
      </div>

      <!-- Tattvadhara Section Ribbon -->
      <div class="section-ribbon">
        <span class="ribbon-badge">તત્વધારા</span>
        <div class="ribbon-rule"></div>
      </div>

      <!-- 2-Column Tattvadhara 4-Card Grid (Left-to-Right Natural Reading Flow) -->
      <div class="tattva-infographic-grid">
        
        <!-- 1. Rupak Drishti (Badge 01 Left) -->
        <div class="tattva-card-shell tattva-card-1" id="p-070-rupak">
          <div class="card-top-row">
            <span class="step-badge">૦૧</span>
            <div class="card-header-titles">
              <span class="card-main-heading">રૂપક-દ્રષ્ટિ:</span>
              <span class="card-sub-kicker">નદીના પ્રવાહમાં ક્ષણે ક્ષણે ફૂટતા પરપોટા</span>
            </div>
          </div>
          <p class="card-body-text">
            ઝડપથી વહેતી પહાડી નદીના પાણી પર ક્ષણે ક્ષણે હજારો પરપોટા જન્મે છે અને બીજી જ ક્ષણે ફૂટીને વિલીન થઈ જાય છે; કોઈ પરપોટો બીજા સમય સુધી ટકતો નથી. સામાન્ય દ્રષ્ટિ પાણીના ધ્રુવ પ્રવાહને ગૌણ કરી કેવળ પરપોટાની ક્ષણિકતાને જુએ છે. તેવી જ રીતે ત્રિકાળી ધ્રુવ દ્રવ્યસત્તાને ગૌણ કરી, પ્રત્યેક સમયના ઉત્પાદ-વ્યયરૂપ વિનાશી સ્વભાવને આગળ રાખી—<em>"સંસારનો પ્રત્યેક પર્યાય ક્ષણભંગુર છે"</em>—એમ પ્રતિપાદન કરવું તે આ નય છે.
          </p>
        </div>

        <!-- 2. Swarup Srishti (Badge 02 Left) -->
        <div class="tattva-card-shell tattva-card-2" id="p-070-swarup">
          <div class="card-top-row">
            <span class="step-badge">૦૨</span>
            <div class="card-header-titles">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">ક્ષણભંગુરતાનો વાસ્તવિક બોધ</span>
            </div>
          </div>
          <p class="card-body-text">
            આ નય દ્રવ્યની શાશ્વતતાને ક્યારેય નકારતો નથી, પરંતુ તે ક્ષણે તેને ગૌણ કરીને કેવળ પર્યાયની ક્ષણિકતાને વાણીના કેન્દ્રમાં લાવે છે. 'અશુદ્ધ' એટલા માટે કારણ કે તે પર્યાયના પરિવર્તનશીલ અંશને પકડે છે. આ નય સાધકના અંતરમાં સંસાર પ્રત્યે ઊંડો વૈરાગ્ય જગાડવા માટે સર્વોચ્ચ આધ્યાત્મિક ઔષધ સમાન છે, જે મોહના બંધનોને મૂળથી તોડે છે.
          </p>
        </div>

        <!-- 3. Vyavahar Pushti (Badge 03 Left) -->
        <div class="tattva-card-shell tattva-card-3" id="p-070-vyavahar">
          <div class="card-top-row">
            <span class="step-badge">૦૩</span>
            <div class="card-header-titles">
              <span class="card-main-heading">વ્યવહાર-પૃષ્ટિ:</span>
              <span class="card-sub-kicker">બાર ભાવનાઓ અને અનિત્યતા ચિંતન</span>
            </div>
          </div>
          <ul class="card-bullet-list">
            <li><strong>અનિત્ય ભાવના:</strong> ધન, યૌવન અને ભોગો વાદળ સમાન ક્ષણભંગુર છે.</li>
            <li><strong>દીપકની જ્યોત:</strong> પ્રત્યેક સમયે જૂની જ્યોતિ બુઝાઈ નવો તેજ-પર્યાય પ્રગટે છે.</li>
            <li><strong>આયુષ્યનો ક્ષય:</strong> ઘડિયાળના કાંટાની જેમ દેહનું આયુષ્ય પળે પળે ઘટી રહ્યું છે.</li>
          </ul>
        </div>

        <!-- 4. Marm Tushti (Badge 04 Left) -->
        <div class="tattva-card-shell tattva-card-4" id="p-070-marm">
          <div class="card-top-row">
            <span class="step-badge">૦૪</span>
            <div class="card-header-titles">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">મોહની ઊંઘમાંથી આત્મજાગરણ</span>
            </div>
          </div>
          <p class="card-body-text">
            જ્યાં સુધી જીવ પર્યાયને શાશ્વત માનીને વળગી રહે છે ત્યાં સુધી તે અહંકાર અને મમત્વમાં ડૂબેલો રહે છે. આ નય ક્ષણભંગુરતા બતાવીને જીવને પરમાર્થ તરફ જગાડે છે. વિનાશી પર્યાયનો મોહ છૂટે ત્યારે જ અવિનાશી ત્રિકાળી આત્મતત્વની સાચી ઉપાસના પ્રગટ થઈ શકે છે.
          </p>
        </div>
      </div>

      <!-- Duo-Ribbon -->
      <div class="bottom-ribbon-shell">
        <div class="duo-ribbon-grid">
          <div class="duo-col" id="p-070-kavya">
            <span class="duo-label">• કાવ્યધારા</span>
            <p class="kavya-quote">
              "પરપોટા જળ મધ્ય જેમ, ક્ષણે ક્ષણે વિલાય;<br>
              સત્તા ગૌણ વ્યવહારથી, અનિત્યતા જણાય."
            </p>
          </div>
          <div class="duo-col duo-divider-col" id="p-070-sadhana">
            <span class="duo-label">✦ સાધનાધારા</span>
            <p class="sadhana-statement">
              પર્યાયની ક્ષણિકતા જાણી અહંકાર અને આસક્તિ તજી, અવિનાશી આત્મસ્વભાવમાં લીન થઈ પરમ શાંતિ અનુભવવી.
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- Running Footer: Left Page -->
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <div class="footer-label">
        <span class="footer-book">નય-ચક્ષુ</span>
        <span class="footer-sep">|</span>
        <span class="footer-sub">નયનું જ્ઞાન, સંશયનું સમાધાન</span>
      </div>
    </footer>
  </section>


  <!-- =============================================================
       RIGHT PAGE: PAGE 3 (ODD PAGE)
       ============================================================= -->
  <section class="page page-odd" id="page-3">
    <div class="page-canvas">

      <!-- Top Story Header Bar -->
      <div class="top-story-header" id="p-070-story-sec">
        <span class="story-kicker">+ કથાધારા</span>
        <span class="story-title-main" id="p-070-story-title">નવલિકા: પાણીના પરપોટા અને રાજાનો વૈરાગ્ય</span>
      </div>

      <!-- Split Story Hero -->
      <div class="story-hero-split">
        <div class="story-artwork-box">
          <svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
            <rect width="200" height="150" fill="#f8f9fa"/>
            <path d="M 20,140 L 20,45 A 25,25 0 0,1 70,45 L 70,140 Z" fill="#111111" opacity="0.9"/>
            <line x1="30" y1="20" x2="25" y2="35" stroke="#777" stroke-width="1.2"/>
            <line x1="50" y1="15" x2="45" y2="30" stroke="#777" stroke-width="1.2"/>
            <line x1="40" y1="35" x2="35" y2="50" stroke="#777" stroke-width="1.2"/>
            <path d="M 85,125 Q 115,120 145,125 T 195,125" fill="none" stroke="#222" stroke-width="1.5"/>
            <path d="M 95,135 Q 125,130 155,135 T 195,135" fill="none" stroke="#444" stroke-width="1.2"/>
            <circle cx="110" cy="122" r="5" fill="none" stroke="#111" stroke-width="1.4"/>
            <circle cx="135" cy="120" r="3.5" fill="none" stroke="#333" stroke-width="1.2"/>
            <circle cx="160" cy="123" r="6" fill="none" stroke="#111" stroke-width="1.4"/>
            <circle cx="120" cy="80" r="14" fill="#222"/>
            <path d="M 120,95 L 120,135 M 120,105 L 105,120 M 120,105 L 135,115" stroke="#222" stroke-width="3" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="story-pipasa-article" id="p-070-pipasa">
          <span class="pipasa-badge">પિપાસા</span>
          <p>
            ધર્મક્ષેત્રના વૈભવી રાજા ચંદ્રપ્રભ યુવાની, સંપત્તિ અને સૈન્યના અહંકારમાં ગળાડૂબ હતા. તેઓ માનતા હતા કે આ સુખ અને રાજ્ય સદાકાળ મારી સાથે જ રહેશે. સંઘના ધર્માચાર્યોની ક્ષણિકતા અંગેની ચેતવણીઓની પણ તેઓ મજાક ઉડાવતા. એક દિવસ રાજાએ મંત્રીને કહ્યું, <em>"મને એવું સુખ જોઈએ જે ક્યારેય ઓછું ન થાય. શું આ સંસારમાં કોઈ પણ વૈભવ નષ્ટ થઈ શકે ખરો?"</em>
          </p>
        </div>
      </div>

      <!-- Paan Block -->
      <div class="story-paan-article" id="p-070-paan">
        <span class="pipasa-badge">પાન</span>
        <p>
          ચોમાસામાં મુનિરાજ મહેલના ઉપવનમાં પધાર્યા. મુનિશ્રીએ સરોવર તરફ ઈશારો કર્યો; વરસાદના ટીપાં પડતાં પાણી પર મોટા ગોળ પરપોટા ઊપસતા હતા અને પળવારમાં ફૂટી જતા હતા! મુનિશ્રીએ કહ્યું, <em>"રાજન્! આ પરપોટો કેટલો મોટો દેખાય છે, પણ તેનું આયુષ્ય કેવળ એક ક્ષણ છે! આ નય આ જ રહસ્ય પોકારીને કહે છે! તારી આ યુવાની, સંપત્તિ અને દેહ પાણીના પરપોટા જેવા ક્ષણભંગુર છે. પ્રત્યેક ક્ષણે આયુષ્યનો પર્યાય નષ્ટ થઈ રહ્યો છે. સંસારના તમામ ભોગપર્યાયો સમય-સમયમાં વિનાશ પામનારા છે; તો ક્ષણિક વૈભવમાં અહંકાર શા માટે?"</em> આ અમૃતવચનોનું પાન કરતાં જ રાજાનો મોહ ક્ષણવારમાં ઓગળી ગયો અને અંતરમાં સંસારની ક્ષણિકતા સ્વીકારી ધર્મનો સાચો આશ્રય લીધો.
        </p>
      </div>

      <!-- Vivekdhara Section -->
      <div class="section-divider-title" id="p-070-vivek-sec">વિવેકધારા</div>
      <div class="vivek-container">
        <div class="vivek-card" id="p-070-ekant">
          <div class="vivek-card-title">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</div>
          <p>
            જો આ નયને એકાંત સત્ય માનીને ત્રિકાળી ધ્રુવ આત્મસત્તાનો સર્વથા લોપ કરી દેવામાં આવે, તો જીવ બૌદ્ધ ક્ષણિકવાદી બનીને અધઃપતનમાં સરી પડે છે. આવી જડતાથી જીવ નિત્ય આત્મતત્વની સાધના ભૂલીને ઘોર શૂન્યતા અને વિષાદમાં ડૂબી જાય છે.
          </p>
        </div>
        <div class="vivek-card" id="p-070-anekant">
          <div class="vivek-card-title">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</div>
          <p>
            આ નય જ્યારે ધ્રુવ દ્રવ્યાર્થિક નય સાથે જોડાય છે, ત્યારે સાધક પર્યાયની ક્ષણભંગુરતા જાણી સંસારથી અનાસક્ત બને છે અને અવિનાશી આત્મસ્વભાવમાં સ્થિર થાય છે. પર્યાયનો વિવેક ધ્રુવ તત્વના આશ્રયનું બળવાન સાધન બને છે.
          </p>
        </div>
      </div>

      <!-- Darshandhara Section (4 Rhyming Pillars) -->
      <div class="darshan-section" id="p-070-darshan-sec">
        <div class="darshan-header">❖ દર્શનધારા</div>
        <div class="darshan-pillars-grid">
          <div class="darshan-pillar-item">
            <strong>૧. નય-ઉન્મેષ:</strong> ધ્રુવ સત્તાને ગૌણ કરી ક્ષણે ક્ષણે થતા નવા ઉત્પાદ-વ્યયને જ મુખ્ય રાખી સંસારને ક્ષણભંગુર કહેવો તે આ નયની દ્રષ્ટિ છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૨. પ્રાચીન-વિશેષ:</strong> બૌદ્ધ દર્શનનો <strong>ક્ષણિકવાદ</strong> ('સર્વ ક્ષણિકં ક્ષણિકમ્') નિત્ય સત્તાનો છેદ ઉડાવી કેવળ વિનાશી પ્રવાહને જ સત્ય સ્વીકારે છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૩. અર્વાચીન-પ્રવેશ:</strong> ડેવિડ હ્યુમ (David Hume)નો <strong>બંડલ થિયરી (Bundle Theory)</strong> દર્શાવે છે કે સ્થિર આત્મા નથી, કેવળ બદલાતી સંવેદનાઓનો પ્રવાહ છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૪. સમન્વય-અશેષ:</strong> સ્યાદ્વાદ આ દર્શનોને આ નયમાં સમન્વિત કરી સ્થાપે છે કે વૈરાગ્ય દૃઢ કરવા ઉત્પાદ-વ્યયનું પ્રતિપાદન પરમ હિતકારી છે.
          </div>
        </div>
      </div>

    </div>

    <!-- Running Footer: Right Page -->
    <footer class="running-footer">
      <div class="footer-label">
        <span class="footer-book">તૃતીય ખંડ: વ્યવહાર નય</span>
        <span class="footer-sep">|</span>
        <span class="footer-sub">૭૦. સત્તાગૌણ ઉત્પાદ-વ્યયગ્રાહક અશુદ્ધ પર્યાયાર્થિક વ્યવહાર</span>
      </div>
      <span class="page-num">૩</span>
    </footer>
  </section>

</div>

</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    print("Chapter 070 HTML rewritten successfully!")

    # Render PDF
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.as_posix()}", f"file:///{html_path.as_posix()}"
    ], capture_output=True)

    # Render Spread
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1360,980",
        f"--screenshot={spread_img.as_posix()}", f"file:///{html_path.as_posix()}"
    ], capture_output=True)

    # Render P2
    raw = html_path.read_text(encoding="utf-8")
    p2_html = raw.replace('id="page-3"', 'id="page-3" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p2_temp = pilot_dir / "p2_temp.html"
    p2_temp.write_text(p2_html, encoding="utf-8")
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=624,912",
        f"--screenshot={p2_img.as_posix()}", f"file:///{p2_temp.as_posix()}"
    ], capture_output=True)
    p2_temp.unlink(missing_ok=True)

    # Render P3
    p3_html = raw.replace('id="page-2"', 'id="page-2" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p3_temp = pilot_dir / "p3_temp.html"
    p3_temp.write_text(p3_html, encoding="utf-8")
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=624,912",
        f"--screenshot={p3_img.as_posix()}", f"file:///{p3_temp.as_posix()}"
    ], capture_output=True)
    p3_temp.unlink(missing_ok=True)

    # Crop Tattvadhara Zoom
    p2_im = Image.open(p2_img)
    w, h = p2_im.size
    tatt_crop = p2_im.crop((int(w * 0.05), int(h * 0.22), int(w * 0.95), int(h * 0.94)))
    tatt_crop.save(tattva_zoom)
    print("Chapter 070 PDF and images generated successfully!")


def generate_chapter_001():
    pilot_dir = Path("sankshipt/pilot_chapter_001").resolve()
    fonts_dir = pilot_dir / "assets/fonts"
    html_path = pilot_dir / "chapter_001.html"
    pdf_path = pilot_dir / "chapter_001.pdf"
    spread_img = pilot_dir / "chapter_001_spread_preview.png"
    p2_img = pilot_dir / "page_002_left_preview.png"
    p3_img = pilot_dir / "page_003_right_preview.png"
    tattva_zoom = pilot_dir / "ch001_tattvadhara_best_zoom.png"
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>૧. ભૂતનૈગમ નય — નય-ચક્ષુ (Best Editorial Design)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 400;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 600;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-SemiBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 700;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-Bold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 800;
      src: url('file:///{fonts_dir.as_posix()}/AnekGujarati-ExtraBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 400;
      src: url('file:///{fonts_dir.as_posix()}/NotoSansGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 700;
      src: url('file:///{fonts_dir.as_posix()}/NotoSansGujarati-Bold.ttf') format('truetype');
    }}

    @page {{
      size: 6.5in 9.5in;
      margin: 0;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      padding: 0;
      background: #e9eaec;
      font-family: 'Noto Sans Gujarati', sans-serif;
      color: #1a1a1a;
      -webkit-font-smoothing: antialiased;
    }}

    .spread-container {{
      display: flex;
      justify-content: center;
      gap: 16px;
      padding: 24px;
      margin: 0 auto;
    }}

    .page {{
      width: 6.5in;
      height: 9.5in;
      background: #ffffff;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }}

    @media print {{
      body {{
        background: none;
      }}
      .spread-container {{
        padding: 0;
        gap: 0;
        display: block;
      }}
      .page {{
        box-shadow: none;
        page-break-after: always;
        break-after: page;
        float: none;
      }}
    }}

    .page-even {{
      padding: 11.5mm 14mm 11.5mm 12.5mm;
    }}

    .page-odd {{
      padding: 11.5mm 12.5mm 11.5mm 14mm;
    }}

    .page-canvas {{
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: 0;
    }}

    /* Footers */
    .running-footer {{
      margin-top: auto;
      padding-top: 4.5pt;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 0.6pt solid #cfcfcf;
      font-size: 9.2pt;
      color: #555555;
      position: relative;
      z-index: 10;
    }}

    .running-footer .page-num {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-weight: 700;
      color: #111111;
      font-size: 11.0pt;
    }}

    .running-footer .footer-label {{
      display: flex;
      align-items: center;
      gap: 5pt;
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 500;
    }}

    .running-footer .footer-book {{
      font-weight: 700;
      color: #222222;
    }}

    .running-footer .footer-sep {{
      color: #888888;
    }}

    /* Chapter Masthead */
    .chapter-masthead {{
      margin-bottom: 3.5pt;
    }}

    .kicker-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2.5pt;
    }}

    .khanda-pill {{
      background: #111111;
      color: #ffffff;
      padding: 2.2pt 6.5pt;
      border-radius: 2pt;
      font-size: 8.8pt;
      font-weight: 700;
      letter-spacing: 0.2pt;
      display: inline-flex;
      align-items: center;
      gap: 4pt;
    }}

    .khanda-pill-sub {{
      color: #b0b0b0;
      font-weight: 500;
      font-size: 8.2pt;
      border-left: 0.6pt solid #555555;
      padding-left: 4pt;
    }}

    .category-tag {{
      font-size: 8.8pt;
      color: #333333;
      font-weight: 600;
      border: 0.6pt solid #b0b0b0;
      padding: 1.8pt 5.5pt;
      border-radius: 2pt;
      background: #f7f7f7;
    }}

    .chapter-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 8pt;
      margin-top: 1.5pt;
      margin-bottom: 2pt;
    }}

    .chapter-main-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 800;
      font-size: 19.5pt;
      line-height: 1.15;
      color: #000000;
      letter-spacing: -0.3pt;
      margin: 0;
      flex: 1;
    }}

    .chapter-sub-meta-right {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      text-align: right;
      gap: 1.5pt;
      flex-shrink: 0;
      max-width: 52%;
    }}

    .gu-general-term {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.2pt;
      color: #111111;
      line-height: 1.18;
    }}

    .en-concept {{
      font-family: 'Cinzel', serif;
      font-size: 8.0pt;
      font-weight: 600;
      color: #666666;
      font-style: italic;
      line-height: 1.18;
      letter-spacing: 0.15pt;
    }}

    .sutra-showcase {{
      margin-top: 2.5pt;
      background: #f8f9fa;
      border-left: 2.8pt solid #111111;
      padding: 2pt 5.5pt;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-radius: 0 2pt 2pt 0;
      gap: 8pt;
    }}

    .sutra-devanagari {{
      font-family: 'Noto Sans Devanagari', 'Anek Devanagari', serif;
      font-size: 9.8pt;
      font-weight: 600;
      color: #111111;
      letter-spacing: 0.2pt;
      line-height: 1.22;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    .sutra-label {{
      font-size: 7.6pt;
      font-weight: 600;
      color: #666666;
      text-transform: uppercase;
      letter-spacing: 0.4pt;
      flex-shrink: 0;
    }}

    .section-ribbon {{
      display: flex;
      align-items: center;
      gap: 6pt;
      margin-top: 2.5pt;
      margin-bottom: 3.5pt;
    }}

    .ribbon-badge {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 800;
      font-size: 9.8pt;
      color: #000000;
      letter-spacing: 0.3pt;
      display: flex;
      align-items: center;
      gap: 4.5pt;
    }}

    .ribbon-badge::before {{
      content: "■";
      font-size: 7.2pt;
      color: #000000;
    }}

    .ribbon-rule {{
      flex: 1;
      height: 0.6pt;
      background: #d8d8d8;
    }}

    /* -------------------------------------------------------------
       BEST GRAPHIC DESIGN: TATTVADHARA 4-CARD GRID
       Harmonious Left-to-Right Reading Hierarchy, 11.0 pt Body
       ------------------------------------------------------------- */
    .tattva-infographic-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 5pt 8pt;
      flex: 1;
      margin-bottom: 3.5pt;
      min-height: 0;
    }}

    .tattva-card-shell {{
      position: relative;
      background: #ffffff;
      border: 0.75pt solid #c8cbcf;
      border-radius: 4.5pt;
      padding: 4.5pt 7pt;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1.2pt 3pt rgba(0, 0, 0, 0.02);
      z-index: 1;
      overflow: hidden;
    }}

    /* Clean Uniform Header Row (Left-to-Right Natural Flow) */
    .card-top-row {{
      display: flex;
      align-items: flex-start;
      gap: 5.5pt;
      margin-bottom: 3.5pt;
      padding-bottom: 2.2pt;
      border-bottom: 0.6pt solid #e6e8eb;
    }}

    .step-badge {{
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
    }}

    .card-header-titles {{
      display: flex;
      flex-direction: column;
      min-width: 0;
    }}

    .card-main-heading {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.5pt;
      color: #0d0d0d;
      line-height: 1.15;
    }}

    .card-sub-kicker {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 600;
      font-size: 9.3pt;
      color: #4b5563;
      line-height: 1.18;
    }}

    /* STRICT MANDATORY 11.0 PT BODY TEXT */
    .card-body-text {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.34;
      color: #1f2937;
      margin: 0;
      text-align: justify;
      hyphens: auto;
      flex: 1;
    }}

    .card-bullet-list {{
      list-style: none;
      padding: 0;
      margin: 0;
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.32;
      color: #1f2937;
    }}

    .card-bullet-list li {{
      position: relative;
      padding-left: 9pt;
      margin-bottom: 2pt;
      text-align: justify;
    }}

    .card-bullet-list li:last-child {{
      margin-bottom: 0;
    }}

    .card-bullet-list li::before {{
      content: "•";
      position: absolute;
      left: 0;
      top: -0.5pt;
      font-size: 9.5pt;
      color: #333333;
    }}

    .card-bullet-list strong {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-weight: 700;
      color: #0d0d0d;
    }}

    /* DUO-RIBBON (11.0 PT BODY) */
    .bottom-ribbon-shell {{
      margin-top: 3.5pt;
      background: #fafafa;
      border: 0.6pt solid #d0d0d0;
      border-left: 2.6pt solid #111111;
      border-radius: 0 4pt 4pt 0;
      padding: 3.5pt 7.5pt;
      margin-bottom: 0;
    }}

    .duo-ribbon-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12pt;
      align-items: center;
    }}

    .duo-col {{
      display: flex;
      flex-direction: column;
      gap: 1.5pt;
    }}

    .duo-divider-col {{
      border-left: 0.6pt solid #d8d8d8;
      padding-left: 10pt;
    }}

    .duo-label {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 9.0pt;
      color: #333333;
      letter-spacing: 0.3pt;
      display: flex;
      align-items: center;
      gap: 3.5pt;
    }}

    .kavya-quote {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 600;
      font-size: 11.0pt !important;
      line-height: 1.30;
      color: #111111;
      font-style: italic;
      margin: 0;
    }}

    .sadhana-statement {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 10.6pt !important;
      line-height: 1.32;
      color: #222222;
      margin: 0;
      text-align: justify;
    }}

    /* PAGE 3: KATHADHARA, VIVEKDHARA & DARSHANDHARA */
    .top-story-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3.0pt;
      padding-bottom: 2.0pt;
      border-bottom: 0.8pt solid #111111;
    }}

    .top-story-header .story-kicker {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 10.5pt;
      color: #111111;
      letter-spacing: 0.3pt;
    }}

    .top-story-header .story-title-main {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.2pt;
      color: #111111;
    }}

    .story-hero-split {{
      display: grid;
      grid-template-columns: 115pt 1fr;
      gap: 8pt;
      margin-bottom: 3.0pt;
    }}

    .story-artwork-box {{
      width: 115pt;
      height: 78pt;
      border: 0.6pt solid #c8c8c8;
      background: #fafafa;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 3.0pt;
      border-radius: 2pt;
    }}

    .story-artwork-box svg {{
      width: 100%;
      height: 100%;
    }}

    .story-pipasa-article {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .pipasa-badge {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 8.5pt;
      color: #111111;
      border-bottom: 1.1pt solid #111111;
      display: inline-block;
      margin-bottom: 1.5pt;
      padding-bottom: 0.5pt;
      align-self: flex-start;
    }}

    .story-pipasa-article p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.32;
      color: #242424;
      margin: 0;
      text-align: justify;
    }}

    .story-paan-article {{
      background: #f7f8f9;
      border-left: 2.5pt solid #111111;
      border-top: 0.6pt solid #cfcfcf;
      border-right: 0.6pt solid #cfcfcf;
      border-bottom: 0.6pt solid #cfcfcf;
      padding: 3.0pt 6.5pt;
      margin-bottom: 3.0pt;
      border-radius: 0 3pt 3pt 0;
    }}

    .story-paan-article p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.32;
      color: #242424;
      margin: 0;
      text-align: justify;
    }}

    .section-divider-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 10.2pt;
      color: #111111;
      margin-bottom: 2.0pt;
      display: flex;
      align-items: center;
      gap: 4.5pt;
    }}

    .section-divider-title::before {{
      content: "❖";
      font-size: 8.0pt;
      color: #111111;
    }}

    .vivek-container {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7pt;
      margin-bottom: 2.5pt;
    }}

    .vivek-card {{
      border: 0.6pt solid #cfcfcf;
      border-radius: 3pt;
      padding: 3.5pt 5.5pt;
      background: #ffffff;
    }}

    .vivek-card-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 9.8pt;
      color: #111111;
      padding-bottom: 1.2pt;
      border-bottom: 0.6pt solid #e0e0e0;
      margin-bottom: 2.0pt;
    }}

    .vivek-card p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 10.6pt !important;
      line-height: 1.32;
      color: #242424;
      margin: 0;
      text-align: justify;
    }}

    .darshan-section {{
      margin-top: auto;
      border-top: 0.6pt solid #d0d0d0;
      padding-top: 2.5pt;
      margin-bottom: 1.0pt;
    }}

    .darshan-header {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 10.5pt;
      color: #111111;
      margin-bottom: 2.0pt;
      display: flex;
      align-items: center;
      gap: 4pt;
    }}

    .darshan-pillars-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2.5pt 7pt;
    }}

    .darshan-pillar-item {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 10.2pt !important;
      line-height: 1.30;
      color: #242424;
      text-align: justify;
    }}

    .darshan-pillar-item strong {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      color: #111111;
    }}
  </style>
</head>
<body>

<div class="spread-container">

  <!-- =============================================================
       LEFT PAGE: PAGE 2 (EVEN PAGE)
       ============================================================= -->
  <section class="page page-even" id="page-2">
    <div class="page-canvas">

      <!-- Chapter Masthead -->
      <div class="chapter-masthead">
        <div class="kicker-row">
          <div class="khanda-pill">
            <span>પ્રથમ ખંડ: નૈગમ નય</span>
            <span class="khanda-pill-sub">જ્ઞાનનય</span>
          </div>
          <div class="category-tag">મુખ્ય શ્રેણી: દ્રવ્યાર્થિક નય</div>
        </div>

        <!-- Title Row -->
        <div class="chapter-title-row">
          <h1 class="chapter-main-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="chapter-sub-meta-right" id="p-001-meta">
            <span class="gu-general-term">ભૂતકાળને વર્તમાનમાં જોવાની દ્રષ્ટિ</span>
            <span class="en-concept">The Retrospective Standpoint: Seeing Continuity</span>
          </div>
        </div>

        <!-- Sacred Sutra Epigraph Card -->
        <div class="sutra-showcase">
          <span class="sutra-devanagari">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span class="sutra-label">મૂળ આગમિક લક્ષણ-સૂત્ર</span>
        </div>
      </div>

      <!-- Tattvadhara Section Ribbon -->
      <div class="section-ribbon">
        <span class="ribbon-badge">તત્વધારા</span>
        <div class="ribbon-rule"></div>
      </div>

      <!-- 2-Column Tattvadhara 4-Card Grid (Left-to-Right Natural Reading Flow) -->
      <div class="tattva-infographic-grid">
        
        <!-- 1. Rupak Drishti (Badge 01 Left) -->
        <div class="tattva-card-shell tattva-card-1" id="p-001-rupak">
          <div class="card-top-row">
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

        <!-- 2. Swarup Srishti (Badge 02 Left) -->
        <div class="tattva-card-shell tattva-card-2" id="p-001-swarup">
          <div class="card-top-row">
            <span class="step-badge">૦૨</span>
            <div class="card-header-titles">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">કાળના પડદા પાર જોતી આંખ</span>
            </div>
          </div>
          <p class="card-body-text">
            ભૂતકાળમાં જે ઘટના ઘટી ગઈ છે કે જે પર્યાય પૂર્ણ થઈ ગયો છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.
          </p>
        </div>

        <!-- 3. Vyavahar Pushti (Badge 03 Left) -->
        <div class="tattva-card-shell tattva-card-3" id="p-001-vyavahar">
          <div class="card-top-row">
            <span class="step-badge">૦૩</span>
            <div class="card-header-titles">
              <span class="card-main-heading">વ્યવહાર-પૃષ્ટિ:</span>
              <span class="card-sub-kicker">જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
            </div>
          </div>
          <ul class="card-bullet-list">
            <li><strong>દિવાળીનો દીવો:</strong> ૨૫૦૦ વર્ષ પૂર્વે પ્રભુ નિર્વાણ પામ્યા, પણ આજે પણ તે ક્ષણ હૈયે જીવંત છે.</li>
            <li><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુત્રને વૃદ્ધ માતા "મારું નાનું બાળક" કહી હૈયે ચાંપે છે.</li>
            <li><strong>બીજ અને જળ:</strong> ગોટલી જોઈ "આ મારો આંબો છે" અને જળ જોઈ "આ હિમાલયનો બરફ છે" કહેવાય.</li>
          </ul>
        </div>

        <!-- 4. Marm Tushti (Badge 04 Left) -->
        <div class="tattva-card-shell tattva-card-4" id="p-001-marm">
          <div class="card-top-row">
            <span class="step-badge">૦૪</span>
            <div class="card-header-titles">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
            </div>
          </div>
          <p class="card-body-text">
            ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.
          </p>
        </div>
      </div>

      <!-- Duo-Ribbon -->
      <div class="bottom-ribbon-shell">
        <div class="duo-ribbon-grid">
          <div class="duo-col" id="p-001-kavya">
            <span class="duo-label">• કાવ્યધારા</span>
            <p class="kavya-quote">
              "અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ;<br>
              જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ."
            </p>
          </div>
          <div class="duo-col duo-divider-col" id="p-001-sadhana">
            <span class="duo-label">✦ સાધનાધારા</span>
            <p class="sadhana-statement">
              અતીતના પશ્ચાત્તાપ કે મોહમાં અટવાયા વિના, તેના પરિપાકને વર્તમાન આત્મજાગૃતિનું સબળ પ્રેરકબળ બનાવવું.
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- Running Footer: Left Page -->
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <div class="footer-label">
        <span class="footer-book">નય-ચક્ષુ</span>
        <span class="footer-sep">|</span>
        <span class="footer-sub">નયનું જ્ઞાન, સંશયનું સમાધાન</span>
      </div>
    </footer>
  </section>


  <!-- =============================================================
       RIGHT PAGE: PAGE 3 (ODD PAGE)
       ============================================================= -->
  <section class="page page-odd" id="page-3">
    <div class="page-canvas">

      <!-- Top Story Header Bar -->
      <div class="top-story-header" id="p-001-story-sec">
        <span class="story-kicker">+ કથાધારા</span>
        <span class="story-title-main" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <!-- Split Story Hero -->
      <div class="story-hero-split">
        <div class="story-artwork-box">
          <svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
            <rect width="200" height="150" fill="#f8f9fa"/>
            <path d="M 20,140 L 20,45 A 25,25 0 0,1 70,45 L 70,140 Z" fill="#111111" opacity="0.9"/>
            <circle cx="45" cy="45" r="14" fill="#ffffff" opacity="0.9"/>
            <path d="M 45,35 Q 48,25 45,18 Q 42,25 45,35 Z" fill="#111111"/>
            <path d="M 85,125 Q 115,120 145,125 T 195,125" fill="none" stroke="#222" stroke-width="1.5"/>
            <circle cx="120" cy="80" r="14" fill="#222"/>
            <path d="M 120,95 L 120,135 M 120,105 L 105,120 M 120,105 L 135,115" stroke="#222" stroke-width="3" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="story-pipasa-article" id="p-001-pipasa">
          <span class="pipasa-badge">પિપાસા</span>
          <p>
            રમેશભાઈ પુત્ર આનંદની વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત હતા. આનંદના અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં વિચારો ઘૂમરાતા: <em>"આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong>
          </p>
        </div>
      </div>

      <!-- Paan Block -->
      <div class="story-paan-article" id="p-001-paan">
        <span class="pipasa-badge">પાન</span>
        <p>
          તે જ ક્ષણે વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂકી શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી બીમારીમાં અવિરત સેવા કરી હતી; તે શું મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ અતીતના સો ઉપકારો કેમ ભૂલે છે?"</em> દાદાજીના બોધામૃતથી ભીતરમાં અતીતનો સ્નેહ સજીવન થયો, ક્રોધ ઓગળી ગયો અને અંતરમાં પરમ વિશ્રામ છવાઈ ગયો.
        </p>
      </div>

      <!-- Vivekdhara Section -->
      <div class="section-divider-title" id="p-001-vivek-sec">વિવેકધારા</div>
      <div class="vivek-container">
        <div class="vivek-card" id="p-001-ekant">
          <div class="vivek-card-title">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</div>
          <p>
            જો આ નય-દ્રષ્ટિ કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બને છે. <em>"અમારા જમાનામાં આમ જ થતું"</em> એવી હઠથી તે વર્તમાન સત્યો નકારે છે. જૂના વેર અને પૂર્વજોના અહંકારને વળગાડી રાખવાથી જીવનમાં જડતા અને કાયમી સંકુચિતતા જન્મે છે.
          </p>
        </div>
        <div class="vivek-card" id="p-001-anekant">
          <div class="vivek-card-title">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</div>
          <p>
            આ જ દ્રષ્ટિ જો સમન્વય બને, તો અતીતના સાર વડે વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પણ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન બને છે.
          </p>
        </div>
      </div>

      <!-- Darshandhara Section (4 Rhyming Pillars) -->
      <div class="darshan-section" id="p-001-darshan-sec">
        <div class="darshan-header">❖ દર્શનધારા</div>
        <div class="darshan-pillars-grid">
          <div class="darshan-pillar-item">
            <strong>૧. નય-ઉન્મેષ:</strong> અતીતમાં વિનષ્ટ કે વ્યય પામેલા પર્યાયને જ્ઞાતા પોતાના જ્ઞાન-સંકલ્પ વડે વર્તમાનમાં એવી રીતે સાક્ષાત્ અનુભવે છે કે જાણે તે આ પળે જ ઉપસ્થિત હોય.
          </div>
          <div class="darshan-pillar-item">
            <strong>૨. પ્રાચીન-વિશેષ:</strong> સાંખ્ય દર્શનનો <strong>સત્કાર્યવાદ</strong> (ઈશ્વરકૃષ્ણ) ખોલે છે કે અસત્ ક્યારેય ઉપજતું નથી, અતીત કાર્ય કારણમાં તિરોહિત રહે છે; ન્યાય દર્શનનું <strong>પ્રત્યભિજ્ઞાન</strong> ('તદેવેદમ્') પૂર્વ અનુભવથી વર્તમાન જ્ઞાનને જીવંત કરે છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૩. અર્વાચીન-પ્રવેશ:</strong> હેનરી બર્ગસન (Henri Bergson)નો <strong>મેટર એન્ડ મેમરી (Duration)</strong> સિદ્ધાંત સિદ્ધ કરે છે કે અતીત એ ગબડતા હિમગોળાની જેમ વર્તમાન ચેતનામાં સંચિત થઈને સક્રિય રહે છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૪. સમન્વય-અશેષ:</strong> સ્યાદવાદ આ સર્વ શાખાઓને ભૂતનૈગમ નયમાં સાંકળી સ્થાપે છે કે અતીત શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનો આધારસ્તંભ છે.
          </div>
        </div>
      </div>

    </div>

    <!-- Running Footer: Right Page -->
    <footer class="running-footer">
      <div class="footer-label">
        <span class="footer-book">પ્રથમ ખંડ: નૈગમ નય</span>
        <span class="footer-sep">|</span>
        <span class="footer-sub">૧. ભૂતનૈગમ નય</span>
      </div>
      <span class="page-num">૩</span>
    </footer>
  </section>

</div>

</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    print("Chapter 001 HTML rewritten successfully!")

    # Render PDF
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.as_posix()}", f"file:///{html_path.as_posix()}"
    ], capture_output=True)

    # Render Spread
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1360,980",
        f"--screenshot={spread_img.as_posix()}", f"file:///{html_path.as_posix()}"
    ], capture_output=True)

    # Render P2
    raw = html_path.read_text(encoding="utf-8")
    p2_html = raw.replace('id="page-3"', 'id="page-3" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p2_temp = pilot_dir / "p2_temp.html"
    p2_temp.write_text(p2_html, encoding="utf-8")
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=624,912",
        f"--screenshot={p2_img.as_posix()}", f"file:///{p2_temp.as_posix()}"
    ], capture_output=True)
    p2_temp.unlink(missing_ok=True)

    # Render P3
    p3_html = raw.replace('id="page-2"', 'id="page-2" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p3_temp = pilot_dir / "p3_temp.html"
    p3_temp.write_text(p3_html, encoding="utf-8")
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=624,912",
        f"--screenshot={p3_img.as_posix()}", f"file:///{p3_temp.as_posix()}"
    ], capture_output=True)
    p3_temp.unlink(missing_ok=True)

    # Crop Tattvadhara Zoom
    p2_im = Image.open(p2_img)
    w, h = p2_im.size
    tatt_crop = p2_im.crop((int(w * 0.05), int(h * 0.22), int(w * 0.95), int(h * 0.94)))
    tatt_crop.save(tattva_zoom)
    print("Chapter 001 PDF and images generated successfully!")


if __name__ == "__main__":
    generate_chapter_070()
    generate_chapter_001()
