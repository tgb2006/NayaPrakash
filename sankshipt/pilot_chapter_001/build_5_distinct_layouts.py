"""
Script to generate 5 completely distinct architectural layout options for Chapter 1 (8x8 inch trim, pure grayscale).
Each option implements a fundamentally different structural layout:
- Option 1: Clean Collage 60/40 Vertical Split (Story 60% Left, Vivekdhara 40% Right) + Artistic Flag Numbering
- Option 2: Side-Hero Image Beside Title on Page 2 + Dual 50/50 Literary Pillars on Page 3
- Option 3: Vertical Outer Margin Ribbon on Page 2 + Inverted 40/60 Vertical Split on Page 3
- Option 4: Giant Artistic Watermark Numeral & Asymmetric Mosaic + 3-Tier Horizontal Hero on Page 3
- Option 5: Bauhaus Geometric Square Badge + True 3-Column Magazine Grid on Page 3
"""

import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(r"d:\PROJECT_WORK\NayaPrakash_Book\sankshipt\pilot_chapter_001")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARTIFACT_DIR = Path(r"C:\Users\Admin\.gemini\antigravity\brain\e55b2621-8c9a-4fa6-ad4e-6e545ad87f2d")

FONT_CSS = """
    @font-face {
      font-family: 'Anek Gujarati';
      font-weight: 700;
      src: url('../assets/fonts/AnekGujarati-Bold.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Anek Gujarati';
      font-weight: 600;
      src: url('../assets/fonts/AnekGujarati-SemiBold.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Anek Gujarati';
      font-weight: 500;
      src: url('../assets/fonts/AnekGujarati-Medium.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Anek Gujarati';
      font-weight: 400;
      src: url('../assets/fonts/AnekGujarati-Regular.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Noto Sans Gujarati';
      font-weight: 700;
      src: url('../assets/fonts/NotoSansGujarati-Bold.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Noto Sans Gujarati';
      font-weight: 600;
      src: url('../assets/fonts/NotoSansGujarati-SemiBold.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Noto Sans Gujarati';
      font-weight: 400;
      src: url('../assets/fonts/NotoSansGujarati-Regular.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Noto Sans Devanagari';
      font-weight: 700;
      src: url('../assets/fonts/NotoSansDevanagari-Bold.ttf') format('truetype');
      font-display: swap;
    }
    @font-face {
      font-family: 'Noto Sans Devanagari';
      font-weight: 400;
      src: url('../assets/fonts/NotoSansDevanagari-Regular.ttf') format('truetype');
      font-display: swap;
    }
"""

COMMON_BASE_CSS = """
    @page { size: 8in 8in; margin: 0; }
    * { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    html, body {
      margin: 0; padding: 0;
      background: #e4e7ec;
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 10.8pt;
      line-height: 1.45;
      color: #1a1a1a;
      -webkit-font-smoothing: antialiased;
    }
    .spread-container {
      display: flex; flex-direction: row; justify-content: center; align-items: flex-start;
      gap: 24px; padding: 30px 20px;
    }
    @media print {
      body { background: transparent; }
      .spread-container { display: block; padding: 0; gap: 0; }
    }
    .page {
      width: 8in; height: 8in;
      background: #ffffff;
      position: relative;
      overflow: hidden;
      page-break-after: always; break-after: page;
      padding: 0;
      box-shadow: 0 6px 24px rgba(0,0,0,0.12);
    }
    @media print { .page { box-shadow: none; margin: 0; } }

    .running-header {
      position: absolute; top: 8.5mm; left: 15mm; right: 15mm; height: 5.5mm;
      display: flex; align-items: center; z-index: 10;
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt;
    }
    .page-even .running-header { justify-content: flex-start; }
    .page-odd .running-header { justify-content: flex-end; }

    .running-footer {
      position: absolute; bottom: 8.5mm; left: 15mm; right: 15mm; height: 5.5mm;
      display: flex; align-items: center; justify-content: space-between; z-index: 10;
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt;
    }
    .running-footer .page-num {
      font-family: 'Noto Sans Gujarati', sans-serif; font-weight: 700; font-size: 10.5pt;
    }
    .running-footer .footer-label { font-weight: 600; letter-spacing: 0.2pt; }
"""

# ==============================================================================
# OPTION 1: 60/40 VERTICAL SPLIT & ARTISTIC FLAG NUMBERING
# ==============================================================================
def generate_option_1():
    opt_dir = BASE_DIR / "arch_option_1_vertical_60_40"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt1.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_BASE_CSS}

    .running-header {{ border-bottom: 0.8pt solid #111; color: #111; }}
    .running-footer {{ border-top: 0.8pt solid #111; color: #111; }}

    .content-area {{
      position: absolute; top: 16mm; left: 15mm; right: 15mm; bottom: 16mm;
      display: flex; flex-direction: column; justify-content: space-between;
    }}

    /* Left Page Masthead with Artistic Flag Number */
    .opt1-masthead {{ margin-bottom: 4pt; }}
    .opt1-hero-num-row {{ display: flex; align-items: center; gap: 8pt; margin-bottom: 2pt; }}
    .opt1-flag-num {{
      background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 14pt; font-weight: 700; padding: 2pt 8pt; border-radius: 2pt;
      display: inline-flex; align-items: center; gap: 3pt;
    }}
    .opt1-kicker {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 9pt; font-weight: 600;
      color: #555; text-transform: uppercase; letter-spacing: 0.5pt;
    }}
    .opt1-dravyarthik {{
      margin-left: auto; border: 0.8pt solid #111; padding: 1.5pt 6pt;
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt; font-weight: 700;
    }}
    .opt1-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 27pt; font-weight: 700;
      line-height: 1.22; color: #111; margin: 2pt 0;
    }}
    .opt1-meta {{ font-size: 8.6pt; color: #555; margin-bottom: 3pt; }}
    .opt1-sutra-bar {{
      background: #f4f4f4; border-left: 3.5pt solid #111; padding: 3pt 8pt;
      display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt1-sutra-txt {{ font-family: 'Noto Sans Devanagari', serif; font-size: 9.8pt; font-weight: 700; color: #111; }}
    .opt1-sutra-lbl {{ font-family: 'Anek Gujarati', sans-serif; font-size: 8.2pt; color: #666; }}

    /* Tattvadhara 2-Col Grid */
    .opt1-tattva-hdr {{
      display: flex; align-items: center; gap: 6pt; margin: 2pt 0 3pt 0;
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10pt; color: #111;
    }}
    .opt1-tattva-hdr::after {{ content: ""; flex: 1; height: 0.8pt; background: #111; }}
    .opt1-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; row-gap: 4pt; }}
    .opt1-card {{ font-size: 10.4pt; line-height: 1.44; text-align: justify; padding: 4pt 6pt; }}
    .opt1-card p {{ margin: 0; }}
    .opt1-card.tint {{ background: #f7f7f7; border: 0.8pt solid #e0e0e0; border-radius: 2pt; }}
    .opt1-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.4pt;
      color: #111; display: block; margin-bottom: 2pt; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    .opt1-vignette {{ padding-left: 8pt; position: relative; margin-bottom: 2pt; font-size: 9.8pt; }}
    .opt1-vignette:last-child {{ margin-bottom: 0; }}
    .opt1-vignette::before {{ content: "•"; position: absolute; left: 0; top: 0; color: #111; }}

    /* Kavyadhara Bottom Bar */
    .opt1-kavya-bar {{
      margin-top: 4pt; border: 1pt solid #111; padding: 4.5pt 8pt; background: #fbfbfb;
      display: flex; align-items: center; gap: 8pt;
    }}
    .opt1-kavya-badge {{
      background: #111; color: #fff; padding: 2pt 6pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 9pt; font-weight: 700; white-space: nowrap;
    }}
    .opt1-kavya-verse {{
      font-size: 11pt; font-weight: 600; color: #111; font-style: italic; margin: 0;
    }}

    /* RIGHT PAGE: 60/40 VERTICAL SPLIT */
    .opt1-split-container {{
      display: flex; gap: 5.5mm; height: 100%; align-items: stretch;
    }}
    .opt1-col-story {{
      flex: 0 0 61%; display: flex; flex-direction: column; justify-content: space-between;
    }}
    .opt1-col-divider {{
      width: 0.8pt; background: #bbb; height: 100%;
    }}
    .opt1-col-vivek {{
      flex: 0 0 36%; display: flex; flex-direction: column; justify-content: space-between;
    }}

    /* Story Elements */
    .opt1-story-hdr {{
      border-bottom: 1.2pt solid #111; padding-bottom: 2pt; margin-bottom: 4pt;
    }}
    .opt1-story-kicker {{ font-family: 'Anek Gujarati', sans-serif; font-size: 11.5pt; font-weight: 700; color: #111; }}
    .opt1-story-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 9.8pt; color: #444; margin-top: 1pt; }}

    .opt1-art-frame {{
      width: 100%; height: 46mm; border: 1pt solid #111; padding: 1.5pt; background: #fff; margin-bottom: 4pt;
    }}
    .opt1-art-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}

    .opt1-pipasa {{
      font-size: 10.2pt; line-height: 1.44; text-align: justify; margin-bottom: 4pt;
    }}
    .opt1-pipasa-badge {{
      background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt; font-weight: 700; padding: 1pt 5pt; display: inline-block; margin-bottom: 2pt;
    }}
    .opt1-drop-cap {{
      float: left; font-family: 'Anek Gujarati', sans-serif; font-size: 26pt; font-weight: 700;
      line-height: 0.9; padding-right: 4pt; color: #111;
    }}

    .opt1-paan {{
      background: #f8f8f8; border-left: 3.5pt solid #111; padding: 4.5pt 7pt;
      font-size: 10.2pt; line-height: 1.44; text-align: justify;
    }}
    .opt1-paan-badge {{
      border-bottom: 1.2pt solid #111; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt; font-weight: 700; display: inline-block; margin-bottom: 2pt;
    }}

    /* Vivekdhara Vertical Column */
    .opt1-vivek-hdr {{
      background: #111; color: #fff; padding: 3pt 6pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 10pt; font-weight: 700; text-align: center; margin-bottom: 4pt;
    }}
    .opt1-vivek-sub {{ font-size: 8pt; color: #ccc; display: block; font-weight: 400; }}

    .opt1-vcard {{
      border: 0.8pt solid #ccc; padding: 5pt 6pt; font-size: 9.8pt; line-height: 1.42;
      text-align: justify; display: flex; flex-direction: column; justify-content: flex-start;
      flex: 1; margin-bottom: 4pt;
    }}
    .opt1-vcard.ekant {{ border-top: 3pt solid #666; background: #fafafa; }}
    .opt1-vcard.anekant {{ border-top: 3pt solid #111; background: #f0f0f0; margin-bottom: 0; }}
    .opt1-vcard-title {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 9.6pt;
      color: #111; margin-bottom: 2pt; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    .opt1-vcard p {{ margin: 0; }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 1: 60/40 Vertical Split & Flag Numbering — પ્રકરણ ૧</title>
  {css}
</head>
<body>
<div class="spread-container">
  <!-- PAGE 2 (LEFT) -->
  <section class="page page-even" id="page-2">
    <header class="running-header">
      <span style="font-weight:700;">નય-ચક્ષુ</span>
      <span style="margin: 0 6pt;">|</span>
      <span>નયનું જ્ઞાન, સંશયનું સમાધાન</span>
    </header>
    <main class="content-area">
      <div class="opt1-masthead">
        <div class="opt1-hero-num-row">
          <span class="opt1-flag-num">◀ ૦૧</span>
          <span class="opt1-kicker">પ્રથમ ખંડ: નૈગમ નય &bull; જ્ઞાનનય</span>
          <span class="opt1-dravyarthik">દ્રવ્યાર્થિક નય</span>
        </div>
        <h1 class="opt1-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
        <div class="opt1-meta" id="p-001-meta">
          BHUTA NAIGAMA NAYA &bull; The Retrospective Standpoint: Seeing Eternal Continuity
        </div>
        <div class="opt1-sutra-bar" id="p-001-sutra">
          <span class="opt1-sutra-txt">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span class="opt1-sutra-lbl">મૂળ આગમિક સૂત્ર</span>
        </div>
      </div>

      <div class="opt1-tattva-hdr">તત્વધારા (ચાર પરિમાણ)</div>

      <div class="opt1-grid">
        <div class="opt1-card" id="p-001-rupak">
          <span class="opt1-card-head">૧. રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
        </div>

        <div class="opt1-card tint" id="p-001-swarup">
          <span class="opt1-card-head">૨. સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
        </div>

        <div class="opt1-card" id="p-001-vyavahar">
          <span class="opt1-card-head">૩. વ્યવહાર-પૃષ્ટિ: જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
          <div class="opt1-vignette"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
          <div class="opt1-vignette"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
          <div class="opt1-vignette"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
        </div>

        <div class="opt1-card tint" id="p-001-marm">
          <span class="opt1-card-head">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt1-kavya-bar" id="p-001-kavya">
        <span class="opt1-kavya-badge">કાવ્યધારા</span>
        <blockquote class="opt1-kavya-verse">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) - 60/40 VERTICAL SPLIT -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt1-split-container">
        <!-- 60% Left Column: Full Story -->
        <div class="opt1-col-story">
          <div class="opt1-story-hdr">
            <span class="opt1-story-kicker" id="p-001-story-sec">✦ કથાધારા</span>
            <div class="opt1-story-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</div>
          </div>

          <div class="opt1-art-frame">
            <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
          </div>

          <div class="opt1-pipasa" id="p-001-pipasa">
            <span class="opt1-pipasa-badge">પિપાસા</span>
            <p style="margin: 0;"><span class="opt1-drop-cap">ર</span>મેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>

          <div class="opt1-paan" id="p-001-paan">
            <span class="opt1-paan-badge">પાન</span>
            <p style="margin: 0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
          </div>
        </div>

        <!-- Vertical Hairline Divider -->
        <div class="opt1-col-divider"></div>

        <!-- 40% Right Column: Vivekdhara Dedicated Column -->
        <div class="opt1-col-vivek">
          <div class="opt1-vivek-hdr" id="p-001-vivek-sec">
            ❖ વિવેકધારા
            <span class="opt1-vivek-sub">સમન્વય અને સાધનાનું વિશ્લેષણ</span>
          </div>

          <div class="opt1-vcard ekant" id="p-001-ekant">
            <span class="opt1-vcard-title">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p>જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>

          <div class="opt1-vcard anekant" id="p-001-anekant">
            <span class="opt1-vcard-title">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p>આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
          </div>
        </div>
      </div>
    </main>
    <footer class="running-footer">
      <span class="footer-label">૧. ભૂતનૈગમ નય</span>
      <span class="page-num">૩</span>
    </footer>
  </section>
</div>
</body>
</html>"""
    html_file.write_text(html, encoding="utf-8")
    return opt_dir, html_file


# ==============================================================================
# OPTION 2: SIDE-HERO IMAGE BESIDE TITLE & DUAL 50/50 LITERARY PILLARS
# ==============================================================================
def generate_option_2():
    opt_dir = BASE_DIR / "arch_option_2_image_beside_title"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt2.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_BASE_CSS}

    .running-header {{ border-bottom: 0.8pt solid #111; color: #111; }}
    .running-footer {{ border-top: 0.8pt solid #111; color: #111; }}

    .content-area {{
      position: absolute; top: 16mm; left: 15mm; right: 15mm; bottom: 16mm;
      display: flex; flex-direction: column; justify-content: space-between;
    }}

    /* PAGE 2: HEADER WITH IMAGE BESIDE TITLE */
    .opt2-hero-header {{
      display: flex; gap: 5.5mm; align-items: stretch; margin-bottom: 4pt;
      border-bottom: 1.2pt solid #111; padding-bottom: 4pt;
    }}
    .opt2-hero-text {{ flex: 1; display: flex; flex-direction: column; justify-content: space-between; }}
    .opt2-badge-row {{ display: flex; align-items: center; justify-content: space-between; }}
    .opt2-num-badge {{
      background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 11pt; font-weight: 700; padding: 1.5pt 6pt;
    }}
    .opt2-cat-tag {{ font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt; font-weight: 600; color: #555; }}
    .opt2-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 25pt; font-weight: 700;
      line-height: 1.2; color: #111; margin: 2pt 0;
    }}
    .opt2-en-sub {{ font-size: 8.5pt; color: #555; margin-bottom: 2pt; }}
    .opt2-sutra-strip {{
      background: #eee; border-left: 3pt solid #111; padding: 2.5pt 6pt;
      font-family: 'Noto Sans Devanagari', serif; font-size: 9.2pt; font-weight: 700; color: #111;
    }}

    .opt2-header-art {{
      width: 62mm; height: 44mm; flex-shrink: 0; border: 1.2pt solid #111;
      padding: 1.5pt; background: #fff;
    }}
    .opt2-header-art img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}

    /* Tattvadhara 4 Cards Grid */
    .opt2-sec-bar {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 9.5pt; font-weight: 700;
      color: #111; margin: 2pt 0; display: flex; align-items: center; gap: 5pt;
    }}
    .opt2-sec-bar::after {{ content: ""; flex: 1; height: 0.8pt; background: #ddd; }}
    .opt2-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; row-gap: 4pt; flex: 1; }}
    .opt2-card {{
      border: 0.8pt solid #ccc; padding: 4pt 6pt; font-size: 10.2pt; line-height: 1.42;
      text-align: justify; background: #fff; display: flex; flex-direction: column; justify-content: flex-start;
    }}
    .opt2-card p {{ margin: 0; }}
    .opt2-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.2pt;
      color: #111; margin-bottom: 2pt; border-bottom: 0.6pt solid #eee; padding-bottom: 1pt;
    }}
    .opt2-vignette {{ padding-left: 8pt; position: relative; margin-bottom: 1.5pt; font-size: 9.6pt; }}
    .opt2-vignette:last-child {{ margin-bottom: 0; }}
    .opt2-vignette::before {{ content: "—"; position: absolute; left: 0; top: 0; color: #111; font-weight: bold; }}

    .opt2-kavya-box {{
      margin-top: 4pt; background: #111; color: #fff; padding: 5pt 10pt;
      display: flex; align-items: center; gap: 10pt;
    }}
    .opt2-kavya-badge {{
      border: 1pt solid #fff; padding: 1.5pt 5pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.8pt; font-weight: 700; white-space: nowrap;
    }}
    .opt2-kavya-verse {{
      font-size: 11pt; font-weight: 600; color: #fff; font-style: italic; margin: 0;
    }}

    /* PAGE 3: 50/50 DUAL PILLAR LITERARY SPREAD (NO IMAGE, PURE TEXT BALANCE) */
    .opt2-page3-top {{
      border-bottom: 1.5pt solid #111; padding-bottom: 3pt; margin-bottom: 4pt;
      display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt2-p3-title {{ font-family: 'Anek Gujarati', sans-serif; font-size: 12pt; font-weight: 700; color: #111; }}
    .opt2-p3-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 9.5pt; color: #555; }}

    .opt2-dual-pillars {{
      display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; height: 100%; align-items: stretch;
    }}

    /* Pillar 1: Full Story */
    .opt2-story-pillar {{
      border-right: 0.8pt solid #ddd; padding-right: 5.8mm;
      display: flex; flex-direction: column; justify-content: space-between;
    }}
    .opt2-pipasa-box {{ font-size: 10.2pt; line-height: 1.45; text-align: justify; margin-bottom: 4pt; }}
    .opt2-badge-story {{
      background: #333; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.2pt; font-weight: 700; padding: 1pt 5pt; display: inline-block; margin-bottom: 2pt;
    }}
    .opt2-paan-box {{
      background: #f7f7f7; border-left: 3pt solid #111; padding: 4.5pt 6.5pt;
      font-size: 10.2pt; line-height: 1.45; text-align: justify;
    }}

    /* Pillar 2: Vivekdhara */
    .opt2-vivek-pillar {{
      display: flex; flex-direction: column; justify-content: space-between; padding-left: 2pt;
    }}
    .opt2-vivek-card {{
      border: 0.8pt solid #bbb; padding: 5pt 7pt; font-size: 10pt; line-height: 1.44;
      text-align: justify; flex: 1; display: flex; flex-direction: column; justify-content: flex-start;
    }}
    .opt2-vivek-card.ekant {{ border-top: 3pt solid #666; background: #fafafa; margin-bottom: 5pt; }}
    .opt2-vivek-card.anekant {{ border-top: 3.5pt solid #111; background: #f2f2f2; }}
    .opt2-vcard-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.2pt;
      color: #111; margin-bottom: 2pt; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    .opt2-vivek-card p {{ margin: 0; }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 2: Image Beside Title & Dual Literary Pillars — પ્રકરણ ૧</title>
  {css}
</head>
<body>
<div class="spread-container">
  <!-- PAGE 2 (LEFT) - IMAGE BESIDE TITLE -->
  <section class="page page-even" id="page-2">
    <header class="running-header">
      <span style="font-weight:700;">નય-ચક્ષુ</span>
      <span style="margin: 0 6pt;">|</span>
      <span>નયનું જ્ઞાન, સંશયનું સમાધાન</span>
    </header>
    <main class="content-area">
      <!-- HEADER WITH IMAGE INTEGRATED BESIDE TITLE -->
      <div class="opt2-hero-header">
        <div class="opt2-hero-text">
          <div class="opt2-badge-row">
            <span class="opt2-num-badge">૦૧</span>
            <span class="opt2-cat-tag">પ્રથમ ખંડ: નૈગમ નય &bull; દ્રવ્યાર્થિક નય</span>
          </div>
          <h1 class="opt2-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="opt2-en-sub" id="p-001-meta">
            Bhuta Naigama Naya &bull; The Retrospective Standpoint: Seeing Eternal Continuity
          </div>
          <div class="opt2-sutra-strip" id="p-001-sutra">
            अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः। <span style="font-family:'Anek Gujarati'; font-weight:normal; font-size:7.8pt; color:#555;">(મૂળ આગમિક સૂત્ર)</span>
          </div>
        </div>
        <div class="opt2-header-art">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>
      </div>

      <div class="opt2-sec-bar">તત્વધારા: ચતુષ્કોણીય દર્શન</div>

      <div class="opt2-grid">
        <div class="opt2-card" id="p-001-rupak">
          <span class="opt2-card-head">૧. રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
        </div>

        <div class="opt2-card" id="p-001-swarup">
          <span class="opt2-card-head">૨. સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
        </div>

        <div class="opt2-card" id="p-001-vyavahar">
          <span class="opt2-card-head">૩. વ્યવહાર-પૃષ્ટિ: જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
          <div class="opt2-vignette"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
          <div class="opt2-vignette"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
          <div class="opt2-vignette"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
        </div>

        <div class="opt2-card" id="p-001-marm">
          <span class="opt2-card-head">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt2-kavya-box" id="p-001-kavya">
        <span class="opt2-kavya-badge">કાવ્યધારા</span>
        <blockquote class="opt2-kavya-verse">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) - 50/50 DUAL PILLARS -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt2-page3-top">
        <span class="opt2-p3-title" id="p-001-story-sec">✦ કથાધારા & વિવેકધારા</span>
        <span class="opt2-p3-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <div class="opt2-dual-pillars">
        <!-- Pillar 1: Full Story Narrative -->
        <div class="opt2-story-pillar">
          <div class="opt2-pipasa-box" id="p-001-pipasa">
            <span class="opt2-badge-story">પિપાસા</span>
            <p style="margin:0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>

          <div class="opt2-paan-box" id="p-001-paan">
            <span class="opt2-badge-story">પાન</span>
            <p style="margin:0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
          </div>
        </div>

        <!-- Pillar 2: Vivekdhara Dual Comparison -->
        <div class="opt2-vivek-pillar">
          <div class="opt2-vivek-card ekant" id="p-001-ekant">
            <span class="opt2-vcard-head">❖ એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p>જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>

          <div class="opt2-vivek-card anekant" id="p-001-anekant">
            <span class="opt2-vcard-head">❖ અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p>આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
          </div>
        </div>
      </div>
    </main>
    <footer class="running-footer">
      <span class="footer-label">૧. ભૂતનૈગમ નય</span>
      <span class="page-num">૩</span>
    </footer>
  </section>
</div>
</body>
</html>"""
    html_file.write_text(html, encoding="utf-8")
    return opt_dir, html_file


# ==============================================================================
# OPTION 3: VERTICAL OUTER MARGIN RIBBON & INVERTED 40/60 VERTICAL SPLIT
# ==============================================================================
def generate_option_3():
    opt_dir = BASE_DIR / "arch_option_3_margin_ribbon_40_60"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt3.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_BASE_CSS}

    .running-header {{ border-bottom: 0.8pt solid #111; color: #111; }}
    .running-footer {{ border-top: 0.8pt solid #111; color: #111; }}

    /* PAGE 2 WITH 24mm VERTICAL MARGIN RIBBON ON LEFT */
    .opt3-p2-page {{ position: relative; }}
    .opt3-ribbon-bar {{
      position: absolute; top: 0; left: 0; bottom: 0; width: 22mm;
      background: #1a1a1a; color: #fff; display: flex; flex-direction: column;
      align-items: center; justify-content: space-between; padding: 12mm 0; z-index: 5;
    }}
    .opt3-ribbon-num {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 20pt; font-weight: 700;
      background: #fff; color: #111; width: 14mm; height: 14mm; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
    }}
    .opt3-ribbon-vtext {{
      writing-mode: vertical-rl; transform: rotate(180deg);
      font-family: 'Anek Gujarati', sans-serif; font-size: 9pt; font-weight: 600;
      letter-spacing: 1.5pt; text-transform: uppercase; color: #ccc;
    }}

    .opt3-p2-content {{
      position: absolute; top: 16mm; left: 28mm; right: 15mm; bottom: 16mm;
      display: flex; flex-direction: column; justify-content: space-between;
    }}

    .opt3-masthead {{ margin-bottom: 3pt; }}
    .opt3-dravyarthik {{
      border: 0.8pt solid #111; padding: 1pt 6pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt; font-weight: 700; display: inline-block; margin-bottom: 2pt;
    }}
    .opt3-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 27pt; font-weight: 700;
      line-height: 1.22; color: #111; margin: 0 0 2pt 0;
    }}
    .opt3-meta {{ font-size: 8.5pt; color: #555; margin-bottom: 3pt; }}
    .opt3-sutra-box {{
      background: #f5f5f5; border: 0.8pt solid #ccc; border-left: 3.5pt solid #111;
      padding: 3pt 7pt; display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt3-sutra-txt {{ font-family: 'Noto Sans Devanagari', serif; font-size: 9.6pt; font-weight: 700; color: #111; }}

    .opt3-tattva-head {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 9.8pt; font-weight: 700;
      color: #111; margin: 2pt 0; border-bottom: 0.8pt solid #111; padding-bottom: 1.5pt;
    }}
    .opt3-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5mm; row-gap: 4pt; flex: 1; }}
    .opt3-card {{
      background: #fff; border: 0.8pt solid #e0e0e0; padding: 4pt 6pt;
      font-size: 10.2pt; line-height: 1.42; text-align: justify;
    }}
    .opt3-card p {{ margin: 0; }}
    .opt3-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.2pt;
      color: #111; margin-bottom: 2pt; display: block; border-bottom: 0.6pt solid #eee; padding-bottom: 1pt;
    }}
    .opt3-vignette {{ padding-left: 8pt; position: relative; margin-bottom: 1.5pt; font-size: 9.6pt; }}
    .opt3-vignette:last-child {{ margin-bottom: 0; }}
    .opt3-vignette::before {{ content: "▸"; position: absolute; left: 0; top: -1pt; color: #111; font-size: 8pt; }}

    .opt3-kavya-bar {{
      margin-top: 4pt; background: #1a1a1a; color: #fff; padding: 4.5pt 8pt;
      display: flex; align-items: center; gap: 8pt;
    }}
    .opt3-kavya-lbl {{
      border: 1pt solid #fff; padding: 1.5pt 5pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.8pt; font-weight: 700;
    }}
    .opt3-kavya-txt {{ font-size: 10.8pt; font-weight: 600; color: #fff; font-style: italic; margin: 0; }}

    /* PAGE 3: INVERTED 40/60 VERTICAL SPLIT (40% Left: Art + Vivek; 60% Right: Story) */
    .opt3-p3-content {{
      position: absolute; top: 16mm; left: 15mm; right: 15mm; bottom: 16mm;
      display: flex; gap: 5.5mm; align-items: stretch;
    }}
    .opt3-col-left {{ flex: 0 0 38%; display: flex; flex-direction: column; justify-content: space-between; }}
    .opt3-col-divider {{ width: 0.8pt; background: #ccc; height: 100%; }}
    .opt3-col-right {{ flex: 0 0 59%; display: flex; flex-direction: column; justify-content: space-between; }}

    .opt3-art-box {{
      width: 100%; height: 46mm; border: 1pt solid #111; padding: 1.5pt; background: #fff; margin-bottom: 4pt;
    }}
    .opt3-art-box img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}

    .opt3-vcard {{
      border: 0.8pt solid #ccc; padding: 4.5pt 6pt; font-size: 9.8pt; line-height: 1.42;
      text-align: justify; flex: 1; display: flex; flex-direction: column; justify-content: flex-start;
      margin-bottom: 4pt;
    }}
    .opt3-vcard.ekant {{ border-top: 3pt solid #666; background: #fafafa; }}
    .opt3-vcard.anekant {{ border-top: 3.5pt solid #111; background: #f2f2f2; margin-bottom: 0; }}
    .opt3-vcard-title {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 9.6pt;
      color: #111; margin-bottom: 2pt; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    .opt3-vcard p {{ margin: 0; }}

    /* Story Column */
    .opt3-story-hdr {{
      border-bottom: 1.5pt solid #111; padding-bottom: 2pt; margin-bottom: 4pt;
    }}
    .opt3-story-title {{ font-family: 'Anek Gujarati', sans-serif; font-size: 12pt; font-weight: 700; color: #111; }}
    .opt3-story-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 9.5pt; color: #555; }}

    .opt3-pipasa-box {{ font-size: 10.4pt; line-height: 1.45; text-align: justify; margin-bottom: 4pt; }}
    .opt3-tag-inline {{
      background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt; font-weight: 700; padding: 1pt 5pt; display: inline-block; margin-bottom: 2pt;
    }}
    .opt3-paan-box {{
      background: #f7f7f7; border-left: 3.5pt solid #111; padding: 5pt 7pt;
      font-size: 10.4pt; line-height: 1.45; text-align: justify;
    }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 3: Vertical Margin Ribbon & Inverted 40/60 Split — પ્રકરણ ૧</title>
  {css}
</head>
<body>
<div class="spread-container">
  <!-- PAGE 2 (LEFT) - VERTICAL MARGIN RIBBON -->
  <section class="page page-even opt3-p2-page" id="page-2">
    <!-- Asymmetric Outer Vertical Ribbon -->
    <div class="opt3-ribbon-bar">
      <div class="opt3-ribbon-num">૦૧</div>
      <div class="opt3-ribbon-vtext">પ્રથમ ખંડ: નૈગમ નય &bull; જ્ઞાનનય</div>
      <div style="font-family:'Anek Gujarati'; font-size:8.5pt; color:#aaa;">P. 02</div>
    </div>

    <header class="running-header" style="left: 28mm;">
      <span style="font-weight:700;">નય-ચક્ષુ</span>
      <span style="margin: 0 6pt;">|</span>
      <span>નયનું જ્ઞાન, સંશયનું સમાધાન</span>
    </header>

    <main class="opt3-p2-content">
      <div class="opt3-masthead">
        <span class="opt3-dravyarthik">દ્રવ્યાર્થિક નય</span>
        <h1 class="opt3-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
        <div class="opt3-meta" id="p-001-meta">
          BHUTA NAIGAMA NAYA &bull; The Retrospective Standpoint: Seeing Eternal Continuity
        </div>
        <div class="opt3-sutra-box" id="p-001-sutra">
          <span class="opt3-sutra-txt">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span style="font-family:'Anek Gujarati'; font-size:8pt; color:#666;">મૂળ આગમિક સૂત્ર</span>
        </div>
      </div>

      <div class="opt3-tattva-head">તત્વધારા: ચતુષ્કોણીય વિશ્લેષણ</div>

      <div class="opt3-grid">
        <div class="opt3-card" id="p-001-rupak">
          <span class="opt3-card-head">૧. રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
        </div>

        <div class="opt3-card" id="p-001-swarup">
          <span class="opt3-card-head">૨. સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
        </div>

        <div class="opt3-card" id="p-001-vyavahar">
          <span class="opt3-card-head">૩. વ્યવહાર-પૃષ્ટિ: જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
          <div class="opt3-vignette"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
          <div class="opt3-vignette"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
          <div class="opt3-vignette"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
        </div>

        <div class="opt3-card" id="p-001-marm">
          <span class="opt3-card-head">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt3-kavya-bar" id="p-001-kavya">
        <span class="opt3-kavya-lbl">કાવ્યધારા</span>
        <blockquote class="opt3-kavya-txt">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer" style="left: 28mm;">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) - INVERTED 40/60 VERTICAL SPLIT -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="opt3-p3-content">
      <!-- 40% Left Column: Illustration + Vivekdhara Stacked -->
      <div class="opt3-col-left">
        <div class="opt3-art-box">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>

        <div class="opt3-vcard ekant" id="p-001-ekant">
          <span class="opt3-vcard-title">❖ એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
          <p>જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
        </div>

        <div class="opt3-vcard anekant" id="p-001-anekant">
          <span class="opt3-vcard-title">❖ અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
          <p>આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
        </div>
      </div>

      <!-- Vertical Divider -->
      <div class="opt3-col-divider"></div>

      <!-- 60% Right Column: Full Kathadhara Narrative -->
      <div class="opt3-col-right">
        <div class="opt3-story-hdr">
          <span class="opt3-story-title" id="p-001-story-sec">✦ કથાધારા</span>
          <div class="opt3-story-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</div>
        </div>

        <div class="opt3-pipasa-box" id="p-001-pipasa">
          <span class="opt3-tag-inline">પિપાસા</span>
          <p style="margin: 0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
        </div>

        <div class="opt3-paan-box" id="p-001-paan">
          <span class="opt3-tag-inline">પાન</span>
          <p style="margin: 0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
        </div>
      </div>
    </main>
    <footer class="running-footer">
      <span class="footer-label">૧. ભૂતનૈગમ નય</span>
      <span class="page-num">૩</span>
    </footer>
  </section>
</div>
</body>
</html>"""
    html_file.write_text(html, encoding="utf-8")
    return opt_dir, html_file


# ==============================================================================
# OPTION 4: GIANT WATERMARK NUMERAL & ASYMMETRIC MOSAIC + 3-TIER HORIZONTAL HERO
# ==============================================================================
def generate_option_4():
    opt_dir = BASE_DIR / "arch_option_4_watermark_mosaic"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt4.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_BASE_CSS}

    .running-header {{ border-bottom: 0.8pt solid #111; color: #111; }}
    .running-footer {{ border-top: 0.8pt solid #111; color: #111; }}

    .content-area {{
      position: absolute; top: 16mm; left: 15mm; right: 15mm; bottom: 16mm;
      display: flex; flex-direction: column; justify-content: space-between;
    }}

    /* PAGE 2: WATERMARK NUMERAL IN HEADER */
    .opt4-header-wrap {{ position: relative; overflow: hidden; margin-bottom: 3pt; }}
    .opt4-watermark-num {{
      position: absolute; right: 0; top: -14pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 78pt; font-weight: 700; color: #ebebeb; line-height: 1; z-index: 1; pointer-events: none;
    }}
    .opt4-header-body {{ position: relative; z-index: 2; }}
    .opt4-kicker-row {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 1pt; }}
    .opt4-kicker-tag {{
      border: 0.8pt solid #111; background: #fff; padding: 1pt 6pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt; font-weight: 700;
    }}
    .opt4-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 28pt; font-weight: 700;
      line-height: 1.2; color: #111; margin: 1pt 0;
    }}
    .opt4-meta {{ font-size: 8.5pt; color: #555; margin-bottom: 2pt; }}
    .opt4-sutra-box {{
      background: #f7f7f7; border-left: 3pt solid #111; padding: 2.5pt 6pt;
      font-family: 'Noto Sans Devanagari', serif; font-size: 9.4pt; font-weight: 700; color: #111;
    }}

    /* ASYMMETRICAL MOSAIC GRID FOR TATTVADHARA */
    .opt4-mosaic-grid {{
      display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.5mm; row-gap: 4pt; flex: 1;
    }}
    /* Point 1: Full-width top hero */
    .opt4-card-full-top {{
      grid-column: 1 / span 2; background: #fdfdfd; border: 0.8pt solid #ccc;
      border-left: 3.5pt solid #111; padding: 3.5pt 6pt; font-size: 10.2pt; line-height: 1.42; text-align: justify;
    }}
    .opt4-card-mid {{
      background: #fff; border: 0.8pt solid #ddd; padding: 3.5pt 6pt;
      font-size: 10.2pt; line-height: 1.42; text-align: justify;
    }}
    /* Point 4: Full-width bottom foundation */
    .opt4-card-full-bot {{
      grid-column: 1 / span 2; background: #f7f7f7; border: 0.8pt solid #ccc;
      padding: 3.5pt 6pt; font-size: 10.2pt; line-height: 1.42; text-align: justify;
    }}
    .opt4-card-full-top p, .opt4-card-mid p, .opt4-card-full-bot p {{ margin: 0; }}
    .opt4-chead {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.2pt;
      color: #111; margin-bottom: 1.5pt; display: block; border-bottom: 0.6pt solid #ddd; padding-bottom: 1pt;
    }}
    .opt4-vignette {{ padding-left: 8pt; position: relative; margin-bottom: 1.5pt; font-size: 9.6pt; }}
    .opt4-vignette:last-child {{ margin-bottom: 0; }}
    .opt4-vignette::before {{ content: "▸"; position: absolute; left: 0; top: -1pt; color: #111; font-size: 8pt; }}

    .opt4-kavya-bar {{
      margin-top: 4pt; background: #111; color: #fff; padding: 4.5pt 8pt;
      display: flex; align-items: center; gap: 8pt;
    }}
    .opt4-kavya-badge {{
      border: 1pt solid #fff; padding: 1.5pt 5pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.8pt; font-weight: 700;
    }}
    .opt4-kavya-verse {{ font-size: 10.8pt; font-weight: 600; color: #fff; font-style: italic; margin: 0; }}

    /* PAGE 3: 3-TIER HORIZONTAL HERO + FULL-WIDTH PAAN + DUAL BOTTOM */
    .opt4-p3-top {{
      border-bottom: 1.2pt solid #111; padding-bottom: 2pt; margin-bottom: 4pt;
      display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt4-p3-kicker {{ font-family: 'Anek Gujarati', sans-serif; font-size: 12pt; font-weight: 700; color: #111; }}
    .opt4-p3-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 9.5pt; color: #555; }}

    /* Tier 1: Wide Art on Left (72mm) + Pipasa on Right */
    .opt4-tier1-hero {{ display: flex; gap: 5.5mm; margin-bottom: 4pt; }}
    .opt4-art-frame {{
      width: 68mm; height: 44mm; flex-shrink: 0; border: 1pt solid #111; padding: 1.5pt; background: #fff;
    }}
    .opt4-art-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .opt4-pipasa {{
      flex: 1; display: flex; flex-direction: column; justify-content: space-between;
      font-size: 10.2pt; line-height: 1.44; text-align: justify;
    }}
    .opt4-tag-story {{
      background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.2pt; font-weight: 700; padding: 1pt 5pt; display: inline-block; margin-bottom: 2pt;
    }}

    /* Tier 2: Paan Spans Full Width */
    .opt4-tier2-paan {{
      background: #f7f7f7; border: 0.8pt solid #ccc; border-left: 3.5pt solid #111;
      padding: 4.5pt 7pt; font-size: 10.2pt; line-height: 1.44; text-align: justify; margin-bottom: 4pt;
    }}

    /* Tier 3: Vivekdhara Dual Grid */
    .opt4-tier3-vivek {{ border-top: 1pt solid #111; padding-top: 3pt; }}
    .opt4-vtitle {{ font-family: 'Anek Gujarati', sans-serif; font-size: 10.5pt; font-weight: 700; margin-bottom: 2pt; }}
    .opt4-vgrid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.5mm; }}
    .opt4-vcard {{
      background: #fafafa; border: 0.8pt solid #ccc; padding: 4.5pt 6.5pt;
      font-size: 9.8pt; line-height: 1.42; text-align: justify;
    }}
    .opt4-vcard.ekant {{ border-top: 2.5pt solid #666; }}
    .opt4-vcard.anekant {{ border-top: 3pt solid #111; background: #f0f0f0; }}
    .opt4-vcard p {{ margin: 0; }}
    .opt4-vhead {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 9.6pt;
      color: #111; margin-bottom: 2pt; display: block; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 4: Watermark Numeral Mosaic & 3-Tier Horizontal Hero — પ્રકરણ ૧</title>
  {css}
</head>
<body>
<div class="spread-container">
  <!-- PAGE 2 (LEFT) - WATERMARK & MOSAIC -->
  <section class="page page-even" id="page-2">
    <header class="running-header">
      <span style="font-weight:700;">નય-ચક્ષુ</span>
      <span style="margin: 0 6pt;">|</span>
      <span>નયનું જ્ઞાન, સંશયનું સમાધાન</span>
    </header>
    <main class="content-area">
      <div class="opt4-header-wrap">
        <div class="opt4-watermark-num">૧</div>
        <div class="opt4-header-body">
          <div class="opt4-kicker-row">
            <span class="opt4-kicker-tag">પ્રથમ ખંડ: નૈગમ નય</span>
            <span class="opt4-kicker-tag">દ્રવ્યાર્થિક નય</span>
          </div>
          <h1 class="opt4-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="opt4-meta" id="p-001-meta">
            BHUTA NAIGAMA NAYA &bull; The Retrospective Standpoint: Seeing Eternal Continuity
          </div>
          <div class="opt4-sutra-box" id="p-001-sutra">
            अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः। <span style="font-family:'Anek Gujarati'; font-weight:normal; font-size:7.8pt; color:#666;">(મૂળ આગમિક સૂત્ર)</span>
          </div>
        </div>
      </div>

      <!-- MOSAIC GRID FOR TATTVADHARA -->
      <div class="opt4-mosaic-grid">
        <!-- Point 1: Full-width top hero card -->
        <div class="opt4-card-full-top" id="p-001-rupak">
          <span class="opt4-chead">૧. રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
        </div>

        <!-- Point 2: Left column card -->
        <div class="opt4-card-mid" id="p-001-swarup">
          <span class="opt4-chead">૨. સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
        </div>

        <!-- Point 3: Right column card -->
        <div class="opt4-card-mid" id="p-001-vyavahar">
          <span class="opt4-chead">૩. વ્યવહાર-પૃષ્ટિ: જીવંત દૃષ્ટાંતો</span>
          <div class="opt4-vignette"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં જીવંત બને છે.</div>
          <div class="opt4-vignette"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુત્રને વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે.</div>
          <div class="opt4-vignette"><strong>બીજ અને જળ:</strong> ગોટલી જોઈ <em>"આ આંબો છે"</em> અને જળ જોઈ <em>"હિમાલયનો બરફ"</em> કહેવાય.</div>
        </div>

        <!-- Point 4: Full-width bottom card -->
        <div class="opt4-card-full-bot" id="p-001-marm">
          <span class="opt4-chead">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt4-kavya-bar" id="p-001-kavya">
        <span class="opt4-kavya-badge">કાવ્યધારા</span>
        <blockquote class="opt4-kavya-verse">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) - 3-TIER HORIZONTAL HERO -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt4-p3-top">
        <span class="opt4-p3-kicker" id="p-001-story-sec">✦ કથાધારા</span>
        <span class="opt4-p3-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <!-- Tier 1: Wide Art on Left (68mm) + Pipasa Narrative on Right -->
      <div class="opt4-tier1-hero">
        <div class="opt4-art-frame">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>
        <div class="opt4-pipasa" id="p-001-pipasa">
          <div>
            <span class="opt4-tag-story">પિપાસા</span>
            <p style="margin:0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>
        </div>
      </div>

      <!-- Tier 2: Paan Spans Full Width -->
      <div class="opt4-tier2-paan" id="p-001-paan">
        <span class="opt4-tag-story">પાન</span>
        <p style="margin:0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
      </div>

      <!-- Tier 3: Vivekdhara Dual Grid -->
      <div class="opt4-tier3-vivek">
        <div class="opt4-vtitle" id="p-001-vivek-sec">❖ વિવેકધારા</div>
        <div class="opt4-vgrid">
          <div class="opt4-vcard ekant" id="p-001-ekant">
            <span class="opt4-vhead">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p>જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>
          <div class="opt4-vcard anekant" id="p-001-anekant">
            <span class="opt4-vhead">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p>આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
          </div>
        </div>
      </div>
    </main>
    <footer class="running-footer">
      <span class="footer-label">૧. ભૂતનૈગમ નય</span>
      <span class="page-num">૩</span>
    </footer>
  </section>
</div>
</body>
</html>"""
    html_file.write_text(html, encoding="utf-8")
    return opt_dir, html_file


# ==============================================================================
# OPTION 5: BAUHAUS SQUARE BADGE & TRUE 3-COLUMN EDITORIAL GRID
# ==============================================================================
def generate_option_5():
    opt_dir = BASE_DIR / "arch_option_5_bauhaus_3_column"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt5.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_BASE_CSS}

    .running-header {{ border-bottom: 0.8pt solid #111; color: #111; }}
    .running-footer {{ border-top: 0.8pt solid #111; color: #111; }}

    .content-area {{
      position: absolute; top: 16mm; left: 15mm; right: 15mm; bottom: 16mm;
      display: flex; flex-direction: column; justify-content: space-between;
    }}

    /* PAGE 2: BAUHAUS GEOMETRIC SPLIT HEADER */
    .opt5-header {{
      display: flex; gap: 4mm; align-items: stretch; margin-bottom: 4pt;
      border-bottom: 1.5pt solid #111; padding-bottom: 4pt;
    }}
    .opt5-num-square {{
      width: 17mm; height: 17mm; background: #111; color: #fff; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center;
      font-family: 'Anek Gujarati', sans-serif; font-size: 20pt; font-weight: 700;
    }}
    .opt5-htext {{ flex: 1; }}
    .opt5-kicker {{ font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt; font-weight: 700; color: #555; text-transform: uppercase; }}
    .opt5-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 26pt; font-weight: 700;
      line-height: 1.2; color: #111; margin: 1pt 0;
    }}
    .opt5-meta {{ font-size: 8.5pt; color: #555; margin-bottom: 2pt; }}
    .opt5-sutra {{
      font-family: 'Noto Sans Devanagari', serif; font-size: 9.4pt; font-weight: 700; color: #111;
      background: #f4f4f4; padding: 2pt 5pt; border-left: 3pt solid #111; display: inline-block; width: 100%;
    }}

    /* TATTVADHARA 4 QUADRANTS WITH CROSSHAIR BORDERS */
    .opt5-quad-grid {{
      display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.5mm; row-gap: 4pt; flex: 1;
    }}
    .opt5-quad {{
      border: 0.8pt solid #ccc; padding: 4pt 6pt; font-size: 10.2pt; line-height: 1.42;
      text-align: justify; background: #fff; position: relative;
    }}
    .opt5-quad p {{ margin: 0; }}
    .opt5-quad-num {{
      display: inline-block; background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8pt; font-weight: 700; padding: 1pt 4pt; margin-right: 3pt;
    }}
    .opt5-qhead {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.2pt;
      color: #111; margin-bottom: 2pt; border-bottom: 0.6pt solid #eee; padding-bottom: 1pt;
    }}
    .opt5-vignette {{ padding-left: 8pt; position: relative; margin-bottom: 1.5pt; font-size: 9.6pt; }}
    .opt5-vignette:last-child {{ margin-bottom: 0; }}
    .opt5-vignette::before {{ content: "•"; position: absolute; left: 0; top: 0; color: #111; }}

    .opt5-kavya-bar {{
      margin-top: 4pt; border-top: 1.2pt solid #111; border-bottom: 1.2pt solid #111;
      padding: 4pt 8pt; display: flex; align-items: center; gap: 8pt; background: #fafafa;
    }}
    .opt5-kavya-quote {{ font-family: 'Anek Gujarati', sans-serif; font-size: 20pt; line-height: 0.8; color: #111; }}
    .opt5-kavya-txt {{ font-size: 11pt; font-weight: 600; font-style: italic; color: #111; margin: 0; }}

    /* PAGE 3: TRUE 3-COLUMN EDITORIAL GRID (Col 1: Art+Pullquote, Col 2: Narrative, Col 3: Vivekdhara) */
    .opt5-p3-top {{
      border-bottom: 1.2pt solid #111; padding-bottom: 2pt; margin-bottom: 4pt;
      display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt5-p3-title {{ font-family: 'Anek Gujarati', sans-serif; font-size: 12pt; font-weight: 700; color: #111; }}
    .opt5-p3-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 9.5pt; color: #555; }}

    .opt5-tri-grid {{
      display: grid; grid-template-columns: 28% 41% 31%; column-gap: 4.5mm; height: 100%; align-items: stretch;
    }}

    /* Col 1: Art + Wisdom Pullquote */
    .opt5-col1 {{ display: flex; flex-direction: column; justify-content: space-between; border-right: 0.8pt solid #ddd; padding-right: 4.5mm; }}
    .opt5-art-box {{
      width: 100%; height: 50mm; border: 1pt solid #111; padding: 1.5pt; background: #fff; margin-bottom: 4pt;
    }}
    .opt5-art-box img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .opt5-pull-box {{
      background: #f7f7f7; border-left: 3pt solid #111; padding: 4.5pt 6pt;
      font-size: 9.8pt; line-height: 1.4; text-align: justify;
    }}
    .opt5-pull-head {{ font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 9pt; color: #111; margin-bottom: 2pt; }}

    /* Col 2: Narrative Pipasa + Paan */
    .opt5-col2 {{
      display: flex; flex-direction: column; justify-content: space-between;
      border-right: 0.8pt solid #ddd; padding-right: 4.5mm;
    }}
    .opt5-pipasa-txt {{ font-size: 10pt; line-height: 1.42; text-align: justify; margin-bottom: 4pt; }}
    .opt5-paan-txt {{
      background: #fafafa; border: 0.8pt solid #ccc; padding: 4.5pt 6pt;
      font-size: 10pt; line-height: 1.42; text-align: justify;
    }}
    .opt5-tag-story {{
      background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8pt; font-weight: 700; padding: 1pt 4pt; display: inline-block; margin-bottom: 2pt;
    }}

    /* Col 3: Vivekdhara */
    .opt5-col3 {{ display: flex; flex-direction: column; justify-content: space-between; }}
    .opt5-vtitle {{
      background: #111; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 9.5pt; font-weight: 700; padding: 2.5pt 5pt; text-align: center; margin-bottom: 4pt;
    }}
    .opt5-vcard {{
      border: 0.8pt solid #ccc; padding: 4.5pt 5.5pt; font-size: 9.5pt; line-height: 1.4;
      text-align: justify; flex: 1; display: flex; flex-direction: column; justify-content: flex-start;
      margin-bottom: 4pt;
    }}
    .opt5-vcard.ekant {{ border-top: 2.5pt solid #666; background: #fafafa; }}
    .opt5-vcard.anekant {{ border-top: 3pt solid #111; background: #f0f0f0; margin-bottom: 0; }}
    .opt5-vhead {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 9.4pt;
      color: #111; margin-bottom: 2pt; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    .opt5-vcard p {{ margin: 0; }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 5: Bauhaus Badge & 3-Column Editorial Grid — પ્રકરણ ૧</title>
  {css}
</head>
<body>
<div class="spread-container">
  <!-- PAGE 2 (LEFT) - BAUHAUS SPLIT -->
  <section class="page page-even" id="page-2">
    <header class="running-header">
      <span style="font-weight:700;">નય-ચક્ષુ</span>
      <span style="margin: 0 6pt;">|</span>
      <span>નયનું જ્ઞાન, સંશયનું સમાધાન</span>
    </header>
    <main class="content-area">
      <div class="opt5-header">
        <div class="opt5-num-square">૧</div>
        <div class="opt5-htext">
          <div class="opt5-kicker">પ્રથમ ખંડ: નૈગમ નય &bull; દ્રવ્યાર્થિક નય</div>
          <h1 class="opt5-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="opt5-meta" id="p-001-meta">
            Bhuta Naigama Naya &bull; The Retrospective Standpoint: Seeing Eternal Continuity
          </div>
          <div class="opt5-sutra" id="p-001-sutra">
            अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः। <span style="font-family:'Anek Gujarati'; font-weight:normal; font-size:7.8pt; color:#666;">(આગમિક સૂત્ર)</span>
          </div>
        </div>
      </div>

      <div class="opt5-quad-grid">
        <div class="opt5-quad" id="p-001-rupak">
          <span class="opt5-qhead"><span class="opt5-quad-num">૧</span>રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
        </div>

        <div class="opt5-quad" id="p-001-swarup">
          <span class="opt5-qhead"><span class="opt5-quad-num">૨</span>સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
        </div>

        <div class="opt5-quad" id="p-001-vyavahar">
          <span class="opt5-qhead"><span class="opt5-quad-num">૩</span>વ્યવહાર-પૃષ્ટિ: જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
          <div class="opt5-vignette"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ જીવંત બને છે.</div>
          <div class="opt5-vignette"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુત્રને વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે.</div>
          <div class="opt5-vignette"><strong>બીજ અને જળ:</strong> ગોટલી જોઈ <em>"આ આંબો છે"</em> અને જળ જોઈ <em>"હિમાલયનો બરફ"</em> કહેવાય.</div>
        </div>

        <div class="opt5-quad" id="p-001-marm">
          <span class="opt5-qhead"><span class="opt5-quad-num">૪</span>મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt5-kavya-bar" id="p-001-kavya">
        <span class="opt5-kavya-quote">“</span>
        <blockquote class="opt5-kavya-txt">અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) - 3-COLUMN EDITORIAL GRID -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt5-p3-top">
        <span class="opt5-p3-title" id="p-001-story-sec">✦ કથાધારા</span>
        <span class="opt5-p3-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <div class="opt5-tri-grid">
        <!-- Col 1: Art + Pull Quote -->
        <div class="opt5-col1">
          <div class="opt5-art-box">
            <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
          </div>
          <div class="opt5-pull-box">
            <div class="opt5-pull-head">બોધ-ચિંતન</div>
            <p style="margin:0;">વર્તમાનની એક નાનકડી ભૂલ પાછળ અતીતના સો સો ઉપકારોને કેમ વિસરી શકાય? અતીત વર્તમાનનું મૂળિયું છે.</p>
          </div>
        </div>

        <!-- Col 2: Pipasa + Paan Story -->
        <div class="opt5-col2">
          <div class="opt5-pipasa-txt" id="p-001-pipasa">
            <span class="opt5-tag-story">પિપાસા</span>
            <p style="margin:0;">રમેશભાઈ પોતાના પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત હતા. પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. મગજમાં નિરંતર વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. રાત્રિના અંધકારમાં તેમના હૃદયમાંથી પોકાર ઊઠ્યો: <strong>"આ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>

          <div class="opt5-paan-txt" id="p-001-paan">
            <span class="opt5-tag-story">પાન</span>
            <p style="margin:0;">તે જ ક્ષણે વૃદ્ધ દાદાજીએ સ્નેહભર્યો હાથ મૂકી શાંત સ્વરે કહ્યું, <em>"બેટા, ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે ભૂલ થઈ, પણ ભૂતકાળમાં આનંદે પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈનો ક્રોધ ઓગળી ગયો અને અંતરમાં પરમ ક્ષમા છવાઈ ગઈ.</p>
          </div>
        </div>

        <!-- Col 3: Vivekdhara Column -->
        <div class="opt5-col3">
          <div class="opt5-vtitle" id="p-001-vivek-sec">❖ વિવેકધારા</div>
          <div class="opt5-vcard ekant" id="p-001-ekant">
            <span class="opt5-vhead">એકાંત દર્શન (કદાગ્રહ)</span>
            <p>જો આ નય-દ્રષ્ટિ જીદ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બને છે. <em>"અમારા જમાનામાં આમ જ થતું"</em> એવી હઠ પકડી વર્તમાન સત્યો નકારે છે, જેનાથી જડતા અને અસહિષ્ણુતા જન્મે છે.</p>
          </div>
          <div class="opt5-vcard anekant" id="p-001-anekant">
            <span class="opt5-vhead">અનેકાંત દર્શન (સમન્વય)</span>
            <p>આ જ દ્રષ્ટિ જો સમન્વય બને, તો અતીતના સારને ગ્રહણ કરી વર્તમાન સમૃદ્ધ બનાવે છે. ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન પ્રગટાવે છે.</p>
          </div>
        </div>
      </div>
    </main>
    <footer class="running-footer">
      <span class="footer-label">૧. ભૂતનૈગમ નય</span>
      <span class="page-num">૩</span>
    </footer>
  </section>
</div>
</body>
</html>"""
    html_file.write_text(html, encoding="utf-8")
    return opt_dir, html_file


# ==============================================================================
# RENDER ENGINE (Headless Chrome PDF & Screenshots)
# ==============================================================================
def render_option(opt_name, opt_dir, html_file, idx):
    print(f"\\nRendering {opt_name}...")
    pdf_path = opt_dir / f"chapter_001_opt{idx}.pdf"
    spread_img = opt_dir / f"spread_chapter_001_opt{idx}.png"
    p2_img = opt_dir / f"page_2_chapter_001_opt{idx}.png"
    p3_img = opt_dir / f"page_3_chapter_001_opt{idx}.png"

    # 1. Print exact 8in x 8in PDF
    cmd_pdf = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file:///{html_file.as_posix()}"
    ]
    subprocess.run(cmd_pdf, capture_output=True)
    print(f"  PDF: {pdf_path.name} ({pdf_path.stat().st_size:,} bytes)")

    # 2. Facing Spread Screenshot
    cmd_spread = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1650,850",
        f"--screenshot={spread_img}",
        f"file:///{html_file.as_posix()}"
    ]
    subprocess.run(cmd_spread, capture_output=True)
    print(f"  Spread Image: {spread_img.name} ({spread_img.stat().st_size:,} bytes)")

    # 3. Page 2 Screenshot
    raw_html = html_file.read_text(encoding="utf-8")
    p2_html = raw_html.replace('id="page-3"', 'id="page-3" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p2_temp = opt_dir / "p2_temp.html"
    p2_temp.write_text(p2_html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--window-size=768,768", f"--screenshot={p2_img}", f"file:///{p2_temp.as_posix()}"], capture_output=True)
    p2_temp.unlink(missing_ok=True)

    # 4. Page 3 Screenshot
    p3_html = raw_html.replace('id="page-2"', 'id="page-2" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
    p3_temp = opt_dir / "p3_temp.html"
    p3_temp.write_text(p3_html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--window-size=768,768", f"--screenshot={p3_img}", f"file:///{p3_temp.as_posix()}"], capture_output=True)
    p3_temp.unlink(missing_ok=True)

    # 5. Copy images to artifact dir for visual review
    for img in [spread_img, p2_img, p3_img]:
        if img.exists() and ARTIFACT_DIR.exists():
            shutil.copy2(img, ARTIFACT_DIR / img.name)

    return {
        "name": opt_name,
        "dir": opt_dir,
        "html": html_file,
        "pdf": pdf_path,
        "spread_img": spread_img,
        "p2_img": p2_img,
        "p3_img": p3_img
    }

def main():
    generators = [
        ("Option 1: 60/40 Vertical Split & Flag Numbering", generate_option_1),
        ("Option 2: Image Beside Title & Dual Literary Pillars", generate_option_2),
        ("Option 3: Vertical Margin Ribbon & Inverted 40/60 Split", generate_option_3),
        ("Option 4: Watermark Numeral Mosaic & 3-Tier Horizontal Hero", generate_option_4),
        ("Option 5: Bauhaus Square Badge & 3-Column Editorial Grid", generate_option_5)
    ]

    results = []
    for idx, (opt_name, gen_fn) in enumerate(generators, 1):
        opt_dir, html_file = gen_fn()
        res = render_option(opt_name, opt_dir, html_file, idx)
        results.append(res)

    print("\\n============================================================")
    print("ALL 5 COMPLETELY DISTINCT ARCHITECTURAL LAYOUTS GENERATED!")
    print("============================================================")

if __name__ == "__main__":
    main()
