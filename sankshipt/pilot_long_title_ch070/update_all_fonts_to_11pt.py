import re
import subprocess
from pathlib import Path
from PIL import Image

def build_symmetrical_11pt_ch070():
    pilot_dir = Path("sankshipt/pilot_long_title_ch070").resolve()
    html_path = pilot_dir / "chapter_070.html"
    pdf_path = pilot_dir / "chapter_070.pdf"
    spread_img = pilot_dir / "chapter_070_spread_preview.png"
    p2_img = pilot_dir / "page_002_left_preview.png"
    p3_img = pilot_dir / "page_003_right_preview.png"
    tattva_zoom = pilot_dir / "tattvadhara_symmetrical_zoom.png"
    
    fonts_dir = Path("sankshipt/pilot_chapter_001/assets/fonts").resolve()
    
    html_content = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>૭૦. સત્તાગૌણ ઉત્પાદ-વ્યયગ્રાહક અશુદ્ધ પર્યાયાર્થિક પ્રતિપાદક વ્યવહાર — નય-ચક્ષુ (Symmetrical 11pt Edition)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* -------------------------------------------------------------
       LOCAL PROJECT FONTS
       ------------------------------------------------------------- */
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 400;
      font-display: swap;
      src: url('{fonts_dir.as_uri()}/AnekGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 600;
      font-display: swap;
      src: url('{fonts_dir.as_uri()}/AnekGujarati-SemiBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 700;
      font-display: swap;
      src: url('{fonts_dir.as_uri()}/AnekGujarati-Bold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 400;
      font-display: swap;
      src: url('{fonts_dir.as_uri()}/NotoSansGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 600;
      font-display: swap;
      src: url('{fonts_dir.as_uri()}/NotoSansGujarati-SemiBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 700;
      font-display: swap;
      src: url('{fonts_dir.as_uri()}/NotoSansGujarati-Bold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Devanagari';
      font-style: normal;
      font-weight: 700;
      font-display: swap;
      src: url('{fonts_dir.as_uri()}/NotoSansDevanagari-Bold.ttf') format('truetype');
    }}

    /* -------------------------------------------------------------
       PAGE GEOMETRY: 6.5in x 9.5in Portrait
       Spread: 13in x 9.5in
       ------------------------------------------------------------- */
    @page {{
      size: 6.5in 9.5in;
      margin: 0;
    }}

    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    body {{
      margin: 0;
      padding: 0;
      background-color: #e5e5e5;
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11pt; /* MANDATORY 11PT BASE */
      color: #1a1a1a;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
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

    /* Margin Standards: Gutter 14mm, Outer 12.5mm, Top 11.5mm, Bottom 11.5mm */
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

    /* -------------------------------------------------------------
       RUNNING FOOTERS
       ------------------------------------------------------------- */
    .running-footer {{
      margin-top: auto;
      padding-top: 5pt;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 0.6pt solid #cfcfcf;
      font-size: 9.5pt;
      color: #555555;
      position: relative;
      z-index: 10;
    }}

    .running-footer .page-num {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-weight: 700;
      color: #111111;
      font-size: 11.5pt;
    }}

    .running-footer .footer-label {{
      display: flex;
      align-items: center;
      gap: 5pt;
      max-width: 330pt;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }}

    .running-footer .footer-book {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      color: #222222;
      letter-spacing: 0.2pt;
    }}

    .running-footer .footer-sep {{
      color: #888888;
    }}

    .running-footer .footer-sub {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-weight: 400;
      color: #444444;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    /* -------------------------------------------------------------
       PAGE 2: MASTHEAD
       ------------------------------------------------------------- */
    .chapter-masthead {{
      margin-bottom: 5pt;
    }}

    .kicker-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3.5pt;
    }}

    .khanda-pill {{
      display: inline-flex;
      align-items: center;
      background: #111111;
      color: #ffffff;
      padding: 2pt 6.5pt;
      border-radius: 2pt;
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 9.2pt;
      letter-spacing: 0.3pt;
      gap: 5pt;
    }}

    .khanda-pill-sub {{
      font-weight: 400;
      color: #e2e2e2;
      font-size: 8.5pt;
    }}

    .category-tag {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 600;
      font-size: 8.8pt;
      color: #333333;
      background: #f1f2f4;
      padding: 1.8pt 6pt;
      border-radius: 2pt;
      border: 0.5pt solid #d5d7dc;
    }}

    /* Adaptive Title Row */
    .chapter-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 4pt;
      margin-bottom: 3.5pt;
      gap: 8pt;
    }}

    .chapter-main-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      color: #0d0d0d;
      margin: 0;
      padding: 0;
      letter-spacing: -0.2pt;
      line-height: 1.20;
    }}

    .chapter-main-title.title-long {{
      font-size: 15.0pt;
      max-width: 60%;
    }}

    .chapter-sub-meta-right {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      text-align: right;
      gap: 1.5pt;
      max-width: 40%;
    }}

    .chapter-sub-meta-right .gu-general-term {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      color: #111111;
      font-size: 10.2pt;
      line-height: 1.22;
      letter-spacing: 0.1pt;
    }}

    .chapter-sub-meta-right .en-concept {{
      font-family: sans-serif;
      font-size: 8.6pt;
      font-weight: 500;
      color: #555555;
      font-style: italic;
      line-height: 1.20;
      letter-spacing: 0.1pt;
    }}

    /* Sacred Sutra Feature Card */
    .sutra-showcase {{
      margin-top: 3.5pt;
      background: #f8f9fa;
      border-left: 2.8pt solid #111111;
      padding: 2.5pt 6pt;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-radius: 0 2pt 2pt 0;
      gap: 8pt;
    }}

    .sutra-devanagari {{
      font-family: 'Noto Sans Devanagari', serif;
      font-size: 9.2pt;
      font-weight: 700;
      color: #1a1a1a;
      letter-spacing: 0.1pt;
      line-height: 1.25;
      flex: 1;
    }}

    .sutra-label {{
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.4pt;
      font-weight: 600;
      color: #555555;
      white-space: nowrap;
      flex-shrink: 0;
    }}

    /* Section Ribbon */
    .section-ribbon {{
      display: flex;
      align-items: center;
      gap: 6pt;
      margin-top: 4pt;
      margin-bottom: 5pt;
    }}

    .ribbon-badge {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.0pt;
      color: #111111;
      letter-spacing: 0.3pt;
      display: flex;
      align-items: center;
      gap: 4pt;
    }}

    .ribbon-badge::before {{
      content: "■";
      font-size: 8.0pt;
      color: #111111;
    }}

    .ribbon-rule {{
      flex: 1;
      height: 0.6pt;
      background: #cfcfcf;
    }}

    /* -------------------------------------------------------------
       TATTVA-DHARA 4-QUADRANT GRID (SYMMETRICAL NUMBERING & 11 PT)
       ------------------------------------------------------------- */
    .tattva-infographic-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 8pt 10pt;
      flex: 1;
      margin-bottom: 6pt;
      min-height: 0;
    }}

    .tattva-card-shell {{
      position: relative;
      background: #ffffff;
      border: 0.8pt solid #c8c8c8;
      border-radius: 6pt;
      padding: 7pt 9pt;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1.5pt 4pt rgba(0, 0, 0, 0.03);
      z-index: 1;
    }}

    /* Symmetrical Header Rows */
    .card-top-row {{
      display: flex;
      align-items: flex-start;
      gap: 6pt;
      margin-bottom: 4.5pt;
      padding-bottom: 2.5pt;
      border-bottom: 0.6pt solid #eaeaea;
    }}

    /* Left column cards (01 & 03): Badge on Left */
    .card-top-row.header-left {{
      justify-content: flex-start;
      text-align: left;
    }}

    /* Right column cards (02 & 04): Badge on Right (Mirrored Symmetry) */
    .card-top-row.header-right {{
      justify-content: flex-end;
      text-align: right;
    }}

    /* Step Badges */
    .step-badge {{
      background: #111111;
      color: #ffffff;
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt;
      font-weight: 700;
      padding: 1.8pt 4.5pt;
      border-radius: 2.5pt;
      letter-spacing: 0.2pt;
      flex-shrink: 0;
      line-height: 1.1;
      margin-top: 1pt;
    }}

    .card-header-titles {{
      display: flex;
      flex-direction: column;
    }}

    .card-header-titles.text-right {{
      align-items: flex-end;
      text-align: right;
    }}

    .card-main-heading {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.8pt;
      color: #0d0d0d;
      line-height: 1.15;
    }}

    .card-sub-kicker {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 600;
      font-size: 9.6pt;
      color: #444444;
      line-height: 1.20;
    }}

    /* MANDATORY 11.0 PT BODY TEXT */
    .card-body-text {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.36;
      color: #222222;
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
      line-height: 1.35;
      color: #222222;
    }}

    .card-bullet-list li {{
      position: relative;
      padding-left: 10pt;
      margin-bottom: 2pt;
      text-align: justify;
    }}

    .card-bullet-list li:last-child {{
      margin-bottom: 0;
    }}

    .card-bullet-list li::before {{
      content: "•";
      position: absolute;
      left: 1pt;
      top: -0.5pt;
      font-size: 10pt;
      color: #333333;
    }}

    .card-bullet-list strong {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-weight: 700;
      color: #0d0d0d;
    }}

    /* -------------------------------------------------------------
       DUO-RIBBON: KAVYADHARA & SADHANADHARA (11.0 PT BODY)
       ------------------------------------------------------------- */
    .bottom-ribbon-shell {{
      margin-top: auto;
      background: #fafafa;
      border: 0.6pt solid #d0d0d0;
      border-left: 2.6pt solid #111111;
      border-radius: 0 4pt 4pt 0;
      padding: 5pt 8pt;
      margin-bottom: 2pt;
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

    /* -------------------------------------------------------------
       PAGE 3: KATHADHARA, VIVEKDHARA & DARSHANDHARA (11.0 PT)
       ------------------------------------------------------------- */
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

    /* Katha Split */
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
    }}

    .dhara-badge-pill {{
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 9.5pt;
      color: #111111;
      border-bottom: 1.2pt solid #111111;
      display: inline-block;
      width: fit-content;
      margin-bottom: 2pt;
      padding-bottom: 0.5pt;
    }}

    .story-pipasa-article p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.36;
      color: #222222;
      margin: 0;
      text-align: justify;
      hyphens: auto;
    }}

    /* Paan */
    .story-paan-article {{
      background: #ffffff;
      border: 0.6pt solid #c8c8c8;
      border-left: 2.4pt solid #111111;
      border-radius: 0 4pt 4pt 0;
      padding: 4.5pt 7pt;
      margin-bottom: 5pt;
    }}

    .story-paan-article p {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.0pt !important;
      line-height: 1.36;
      color: #222222;
      margin: 0;
      text-align: justify;
    }}

    /* Vivekdhara Split */
    .vivek-master-section {{
      margin-bottom: 5pt;
    }}

    .vivek-header-row {{
      display: flex;
      align-items: center;
      gap: 4pt;
      font-family: 'Anek Gujarati', sans-serif;
      font-weight: 700;
      font-size: 11.0pt;
      color: #111111;
      margin-bottom: 3.5pt;
    }}

    .vivek-cards-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8pt;
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

    /* Darshandhara */
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

      <!-- 2-Column Tattvadhara Infographic Grid (Symmetrical Badges 01/03 Left, 02/04 Right) -->
      <div class="tattva-infographic-grid">
        
        <!-- 1. Rupak Drishti (Left Aligned Badge 01) -->
        <div class="tattva-card-shell tattva-card-1" id="p-070-rupak">
          <div class="card-top-row header-left">
            <span class="step-badge">૦૧</span>
            <div class="card-header-titles">
              <span class="card-main-heading">રૂપક-દ્રષ્ટિ:</span>
              <span class="card-sub-kicker">નદીના પ્રવાહમાં ક્ષણે ક્ષણે ફૂટતા પરપોટા</span>
            </div>
          </div>
          <p class="card-body-text">
            ઝડપથી વહેતી પહાડી નદીના પાણી પર ક્ષણે ક્ષણે હજારો ફીણ અને પરપોટા જન્મે છે અને બીજી જ ક્ષણે ફૂટીને વિલીન થઈ જાય છે. એક પરપોટો બીજા સમય સુધી ટકતો નથી. સામાન્ય માણસ પાણીની સ્થિરતાને ગૌણ કરીને કેવળ પરપોટાની ક્ષણિકતાને જુએ છે. તેવી જ રીતે ત્રિકાળી ધ્રુવ દ્રવ્યસત્તાને ગૌણ કરી, કેવળ પ્રત્યેક સમયે થતા પર્યાયોના ઉત્પાદ-વ્યયરૂપ વિનાશી સ્વભાવને આગળ રાખીને — <em>"સંસારનો પ્રત્યેક પર્યાય એક સમયનો છે, અનિત્ય અને ક્ષણભંગુર છે"</em> — એમ પ્રતિપાદન કરવામાં આવે ત્યારે તે આ નય કહેવાય છે.
          </p>
        </div>

        <!-- 2. Swarup Srishti (Right Aligned Badge 02) -->
        <div class="tattva-card-shell tattva-card-2" id="p-070-swarup">
          <div class="card-top-row header-right">
            <div class="card-header-titles text-right">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">ક્ષણભંગુરતાનો વાસ્તવિક બોધ</span>
            </div>
            <span class="step-badge">૦૨</span>
          </div>
          <p class="card-body-text">
            આ નય દ્રવ્યની શાશ્વતતાને ક્યારેય નકારતો નથી, પરંતુ તે ક્ષણે તેને ગૌણ કરીને કેવળ પર્યાયની ક્ષણિકતાને વાણીના કેન્દ્રમાં લાવે છે. 'અશુદ્ધ' એટલા માટે કારણ કે તે પર્યાયના પરિવર્તનશીલ અંશને પકડે છે. આ નય સાધકના અંતરમાં સંસાર પ્રત્યે ઊંડો વૈરાગ્ય જગાડવા માટે સર્વોચ્ચ આધ્યાત્મિક ઔષધ સમાન છે, જે મોહના બંધનોને મૂળથી તોડે છે.
          </p>
        </div>

        <!-- 3. Vyavahar Pushti (Left Aligned Badge 03) -->
        <div class="tattva-card-shell tattva-card-3" id="p-070-vyavahar">
          <div class="card-top-row header-left">
            <span class="step-badge">૦૩</span>
            <div class="card-header-titles">
              <span class="card-main-heading">વ્યવહાર-પૃષ્ટિ:</span>
              <span class="card-sub-kicker">બાર ભાવનાઓ અને અનિત્યતા ચિંતન</span>
            </div>
          </div>
          <ul class="card-bullet-list">
            <li><strong>અનિત્ય ભાવના:</strong> "ધન યૌવન ને રૂપ વાદળ જેવાં અનિત્ય છે; સર્વ ભોગ ક્ષણભંગુર છે."</li>
            <li><strong>દીપકની જ્યોત:</strong> પ્રત્યેક સમયે જૂની જ્યોતિ બુઝાય છે ને નવો તેજ-પર્યાય પ્રગટે છે.</li>
            <li><strong>આયુષ્યનો ક્ષય:</strong> ઘડિયાળના કાંટાની જેમ દેહનું આયુષ્ય પ્રત્યેક પળે ઘટી રહ્યું છે.</li>
          </ul>
        </div>

        <!-- 4. Marm Tushti (Right Aligned Badge 04) -->
        <div class="tattva-card-shell tattva-card-4" id="p-070-marm">
          <div class="card-top-row header-right">
            <div class="card-header-titles text-right">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">મોહની ઊંઘમાંથી આત્મજાગરણ</span>
            </div>
            <span class="step-badge">૦૪</span>
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
            <circle cx="110" cy="122" r="2" fill="#111"/>
            <circle cx="135" cy="120" r="7" fill="none" stroke="#111" stroke-width="1.5"/>
            <circle cx="133" cy="118" r="1.5" fill="#fff"/>
            <circle cx="160" cy="124" r="4" fill="none" stroke="#111" stroke-width="1.2"/>
            <path d="M 105,65 C 105,58 112,58 112,65 C 112,72 105,72 105,65 Z" fill="#222"/>
            <path d="M 102,74 L 115,74 L 120,115 L 98,115 Z" fill="#333"/>
            <line x1="115" y1="85" x2="132" y2="112" stroke="#111" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M 170,72 C 170,66 176,66 176,72 C 176,78 170,78 170,72 Z" fill="#222"/>
            <path d="M 162,80 L 178,80 L 175,115 L 158,115 Z" fill="#111"/>
            <rect x="188" y="25" width="6" height="115" fill="#555"/>
          </svg>
        </div>
        <div class="story-pipasa-article" id="p-070-pipasa">
          <span class="dhara-badge-pill">પિપાસા</span>
          <p>
            ધર્મક્ષેત્રના વૈભવી રાજા ચંદ્રપ્રભ યુવાની, સંપત્તિ અને સૈન્યના અહંકારમાં ગળાડૂબ હતા. તેઓ માનતા હતા કે આ સુખ અને રાજ્ય સદાકાળ મારી સાથે જ રહેશે. સંઘના ધર્માચાર્યોની ક્ષણિકતા અંગેની ચેતવણીઓની પણ તેઓ મજાક ઉડાવતા. એક દિવસ રાજાએ મંત્રીને કહ્યું, <em>"મને એવું સુખ જોઈએ જે ક્યારેય ઓછું ન થાય. શું આ સંસારમાં કોઈ પણ વૈભવ નષ્ટ થઈ શકે ખરો?"</em>
          </p>
        </div>
      </div>

      <!-- Paan -->
      <div class="story-paan-article" id="p-070-paan">
        <span class="dhara-badge-pill">પાન</span>
        <p>
          ચોમાસામાં મુનિરાજ મહેલના ઉપવનમાં પધાર્યા. મુનિશ્રીએ સરોવર તરફ ઈશારો કર્યો; વરસાદના ટીપાં પડતાં પાણી પર મોટા ગોળ પરપોટા ઊપસતા હતા અને પળવારમાં ફૂટી જતા હતા! મુનિશ્રીએ કહ્યું, <em>"રાજન્! આ પરપોટો કેટલો મોટો દેખાય છે, પણ તેનું આયુષ્ય કેવળ એક ક્ષણ છે! આ નય આ જ રહસ્ય પોકારીને કહે છે! તારી આ યુવાની, સંપત્તિ અને દેહ પાણીના પરપોટા જેવા ક્ષણભંગુર છે. પ્રત્યેક ક્ષણે આયુષ્યનો પર્યાય નષ્ટ થઈ રહ્યો છે. સંસારના તમામ ભોગપર્યાયો સમય-સમયમાં વિનાશ પામનારા છે; તો ક્ષણિક વૈભવમાં અહંકાર શા માટે?"</em> આ અમૃતવચનોનું પાન કરતાં જ રાજાનો મોહ ક્ષણવારમાં ઓગળી ગયો અને અંતરમાં સંસારની ક્ષણિકતા સ્વીકારી ધર્મનો સાચો આશ્રય લીધો.
        </p>
      </div>

      <!-- Vivekdhara Master Section -->
      <div class="vivek-master-section" id="p-070-vivek-sec">
        <div class="vivek-header-row">
          <span>❖ વિવેકધારા</span>
        </div>
        <div class="vivek-cards-grid">
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
      </div>

      <!-- Darshandhara -->
      <div class="darshan-section" id="p-070-darshan-sec">
        <div class="darshan-header">
          <span>⟡ દર્શનધારા</span>
        </div>
        <div class="darshan-pillars-grid">
          <div class="darshan-pillar-item">
            <strong>૧. નય-ઉન્મેષ:</strong> ધ્રુવ સત્તાને ગૌણ કરી ક્ષણે ક્ષણે થતા નવા ઉત્પાદ-વ્યયને જ મુખ્ય રાખી સંસારને ક્ષણભંગુર કહેવો તે આ નયની દ્રષ્ટિ છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૨. પ્રાચીન-વિશેષ:</strong> બૌદ્ધ દર્શનનો <strong>ક્ષણિકવાદ</strong> ('સર્વં ક્ષણિકં ક્ષણિકમ્') નિત્ય સત્તાનો છેદ ઉડાવી કેવળ વિનાશી પ્રવાહને જ સત્ય સ્વીકારે છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૩. અર્વાચીન-પ્રવેશ:</strong> ડેવિડ હ્યુમ (David Hume)નો <strong>બંડલ થિયરી (Bundle Theory)</strong> દર્શાવે છે કે સ્થિર આત્મા નથી, કેવળ બદલાતી સંવેદનાઓનો પ્રવાહ છે.
          </div>
          <div class="darshan-pillar-item">
            <strong>૪. સમન્વય-અશેષ:</strong> સ્યાદવાદ આ દર્શનોને આ નયમાં સમન્વિત કરી સ્થાપે છે કે વૈરાગ્ય દૃઢ કરવા ઉત્પાદ-વ્યયનું પ્રતિપાદન પરમ હિતકારી છે.
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
    html_path.write_text(html_content, encoding="utf-8")
    print("Written Symmetrical 11pt HTML.")
    
    # Render PDF via Chrome
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    print("Rendering PDF...")
    subprocess.run([
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file:///{html_path.as_posix()}"
    ], capture_output=True)
    print(f"PDF generated: {pdf_path.stat().st_size:,} bytes")
    
    # Render Spread
    print("Rendering Spread Preview...")
    subprocess.run([
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1360,980",
        f"--screenshot={spread_img}",
        f"file:///{html_path.as_posix()}"
    ], capture_output=True)
    
    # Render Left Page
    print("Rendering Left Page...")
    p2_html = html_content.replace('id="page-3"', 'id="page-3" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p2_temp = pilot_dir / "p2_temp.html"
    p2_temp.write_text(p2_html, encoding="utf-8")
    subprocess.run([
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=624,912",
        f"--screenshot={p2_img}",
        f"file:///{p2_temp.as_posix()}"
    ], capture_output=True)
    p2_temp.unlink(missing_ok=True)
    
    # Render Right Page
    print("Rendering Right Page...")
    p3_html = html_content.replace('id="page-2"', 'id="page-2" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p3_temp = pilot_dir / "p3_temp.html"
    p3_temp.write_text(p3_html, encoding="utf-8")
    subprocess.run([
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=624,912",
        f"--screenshot={p3_img}",
        f"file:///{p3_temp.as_posix()}"
    ], capture_output=True)
    p3_temp.unlink(missing_ok=True)
    
    # Crop Tattvadhara 4 cards zoom
    p2_im = Image.open(p2_img)
    w, h = p2_im.size
    tatt_crop = p2_im.crop((int(w * 0.05), int(h * 0.22), int(w * 0.95), int(h * 0.85)))
    tatt_crop.save(tattva_zoom)
    
    print("Symmetrical 11pt build and zoom completed successfully!")

if __name__ == "__main__":
    build_symmetrical_11pt_ch070()
