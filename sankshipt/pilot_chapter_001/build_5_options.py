"""
Build 5 Distinct PURE GRAYSCALE Magazine Layout Options for Chapter 1 Pilot Design
Based on User Layout References (Geometry, Blocks, Ribbons, Modular Boxes, Swiss Grid)
100% Monochrome / Grayscale (Black, Charcoal, Mid-Gray, Light-Gray, White)
"""

import os
import re
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / "assets" / "fonts"
IMAGES_DIR = BASE_DIR / "assets" / "images"
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

COMMON_PAGE_CSS = """
    @page { size: 8in 8in; margin: 0; }
    * { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    html, body {
      margin: 0; padding: 0;
      background: #e4e7ec;
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 11.2pt;
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

    .content-area {
      position: absolute; top: 16.5mm; left: 15mm; right: 15mm; bottom: 16.5mm;
      display: flex; flex-direction: column; justify-content: space-between;
    }
"""

def generate_option_1():
    """Option 1: Solid Hero Block & Asymmetric Card (Inspired by Reference Image 1 Layout)"""
    opt_dir = BASE_DIR / "option_1_architectural_blocks"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt1.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_PAGE_CSS}

    .running-header {{ border-bottom: 1.2pt solid #222; color: #444; }}
    .running-footer {{ border-top: 1.2pt solid #222; color: #444; }}

    /* Large Charcoal Masthead Block */
    .opt1-masthead {{
      border-bottom: 1.5pt solid #222; padding-bottom: 5pt; margin-bottom: 5pt;
    }}
    .opt1-header-block {{
      background: #222; color: #fff; padding: 4pt 8pt; display: flex; justify-content: space-between;
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt; font-weight: 700;
    }}
    .opt1-title-box {{ margin: 4pt 0 2pt 0; }}
    .opt1-main-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 28pt; font-weight: 700; line-height: 1.24;
      color: #111; margin: 0;
    }}
    .opt1-en-meta {{ font-family: sans-serif; font-size: 8.8pt; color: #555; margin-top: 2pt; font-weight: 600; }}
    .opt1-sutra-card {{
      background: #f2f2f2; border-left: 3.5pt solid #222; padding: 4pt 8pt;
      display: flex; justify-content: space-between; align-items: baseline; margin-top: 4pt;
    }}
    .opt1-sutra-text {{ font-family: 'Noto Sans Devanagari', serif; font-size: 9.8pt; font-weight: 700; color: #111; }}
    .opt1-sutra-lbl {{ font-family: 'Anek Gujarati', sans-serif; font-size: 8pt; font-weight: 600; color: #666; }}

    /* Section Ribbon */
    .opt1-ribbon {{ display: flex; align-items: center; gap: 6pt; margin: 2pt 0 4pt 0; }}
    .opt1-ribbon-tag {{
      background: #222; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 10pt; font-weight: 700; padding: 2pt 8pt;
    }}
    .opt1-ribbon-line {{ flex: 1; height: 1pt; background: #222; }}

    /* Asymmetric Grid: Col 1 White, Col 2 Tinted Card */
    .opt1-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; row-gap: 6pt; flex: 1; }}
    .opt1-card {{
      font-size: 10.6pt; line-height: 1.44; text-align: justify; color: #1a1a1a;
    }}
    .opt1-card.shaded {{
      background: #f8f8f8; border: 0.8pt solid #ddd; padding: 5pt 7pt; border-radius: 2pt;
    }}
    .opt1-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.8pt; color: #111;
      display: block; margin-bottom: 2pt; border-bottom: 0.8pt solid #ccc; padding-bottom: 1pt;
    }}
    .opt1-vignette-box {{
      border: 0.8pt solid #ccc; padding: 3.5pt 5.5pt; background: #fafafa; margin-top: 2pt;
    }}
    .opt1-vignette-item {{ position: relative; padding-left: 9pt; margin-bottom: 2.5pt; font-size: 10.2pt; }}
    .opt1-vignette-item:last-child {{ margin-bottom: 0; }}
    .opt1-vignette-item::before {{ content: "■"; position: absolute; left: 0; top: 0; font-size: 6.5pt; color: #222; }}

    /* Prominent Pull-Quote Kavyadhara */
    .opt1-kavya-box {{
      margin-top: 5pt; background: #f4f4f4; border: 1.2pt solid #222; border-left: 4.5pt solid #111;
      padding: 6pt 10pt; display: flex; align-items: center; gap: 10pt;
    }}
    .opt1-kavya-badge {{
      background: #222; color: #fff; padding: 2.5pt 6pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 9.5pt; font-weight: 700; white-space: nowrap;
    }}
    .opt1-kavya-verse {{
      font-family: 'Noto Sans Gujarati', sans-serif; font-size: 11.2pt; font-weight: 600;
      color: #111; font-style: italic; margin: 0;
    }}

    /* Right Page */
    .opt1-story-bar {{
      background: #222; color: #fff; padding: 4.5pt 10pt; display: flex; justify-content: space-between;
      align-items: center; margin-bottom: 5pt;
    }}
    .opt1-story-kicker {{ font-family: 'Anek Gujarati', sans-serif; font-size: 12.5pt; font-weight: 700; }}
    .opt1-story-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 10.5pt; color: #eee; }}

    .opt1-hero-row {{ display: flex; gap: 5.8mm; margin-bottom: 5pt; }}
    .opt1-art-frame {{
      width: 72mm; height: 44mm; flex-shrink: 0; border: 1.2pt solid #222; padding: 1.5pt; background: #fff;
    }}
    .opt1-art-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .opt1-pipasa {{
      flex: 1; display: flex; flex-direction: column; justify-content: space-between;
      font-size: 10.6pt; line-height: 1.45; text-align: justify;
    }}
    .opt1-dhara-badge {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 9pt; font-weight: 700;
      background: #222; color: #fff; padding: 1pt 5pt; display: inline-block; margin-bottom: 2pt;
    }}
    .opt1-paan {{
      border: 1pt solid #ccc; border-left: 4pt solid #222; padding: 5.5pt 8pt;
      background: #f9f9f9; font-size: 10.6pt; line-height: 1.45; text-align: justify; margin-bottom: 5pt;
    }}

    .opt1-vivek-sec {{ border-top: 1.5pt solid #222; padding-top: 4pt; }}
    .opt1-vivek-title {{ font-family: 'Anek Gujarati', sans-serif; font-size: 11.5pt; font-weight: 700; margin-bottom: 3pt; }}
    .opt1-vivek-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; }}
    .opt1-vivek-card {{
      border: 0.8pt solid #ccc; padding: 5pt 7pt; font-size: 10.2pt; line-height: 1.42; text-align: justify;
    }}
    .opt1-vivek-card.anekant {{ background: #f2f2f2; border-top: 3pt solid #111; }}
    .opt1-vivek-card.ekant {{ border-top: 3pt solid #777; }}
    .opt1-vivek-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10pt;
      margin-bottom: 2pt; display: block; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 1: Architectural Block & Asymmetric Card — પ્રકરણ ૧</title>
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
        <div class="opt1-header-block">
          <span>પ્રથમ ખંડ: નૈગમ નય • જ્ઞાનનય</span>
          <span>દ્રવ્યાર્થિક નય</span>
        </div>
        <div class="opt1-title-box">
          <h1 class="opt1-main-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="opt1-en-meta" id="p-001-meta">
            BHUTA NAIGAMA NAYA &bull; The Retrospective Standpoint: Seeing Eternal Continuity
          </div>
        </div>
        <div class="opt1-sutra-card">
          <span class="opt1-sutra-text">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span class="opt1-sutra-lbl">મૂળ આગમિક સૂત્ર</span>
        </div>
      </div>

      <div class="opt1-ribbon">
        <span class="opt1-ribbon-tag">તત્વધારા</span>
        <div class="opt1-ribbon-line"></div>
      </div>

      <div class="opt1-grid">
        <div class="opt1-card" id="p-001-rupak">
          <span class="opt1-card-head">૧. રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
        </div>
        <div class="opt1-card shaded" id="p-001-swarup">
          <span class="opt1-card-head">૨. સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
        </div>
        <div class="opt1-card" id="p-001-vyavahar">
          <span class="opt1-card-head">૩. વ્યવહાર-પૃષ્ટિ: જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
          <div class="opt1-vignette-box">
            <div class="opt1-vignette-item"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
            <div class="opt1-vignette-item"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
            <div class="opt1-vignette-item"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
          </div>
        </div>
        <div class="opt1-card shaded" id="p-001-marm">
          <span class="opt1-card-head">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt1-kavya-box" id="p-001-kavya">
        <span class="opt1-kavya-badge">કાવ્યધારા</span>
        <blockquote class="opt1-kavya-verse">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt1-story-bar">
        <span class="opt1-story-kicker" id="p-001-story-sec">✦ કથાધારા</span>
        <span class="opt1-story-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <div class="opt1-hero-row">
        <div class="opt1-art-frame">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>
        <div class="opt1-pipasa" id="p-001-pipasa">
          <div>
            <span class="opt1-dhara-badge">પિપાસા</span>
            <p style="margin: 0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>
        </div>
      </div>

      <div class="opt1-paan" id="p-001-paan">
        <span class="opt1-dhara-badge">પાન</span>
        <p style="margin: 0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
      </div>

      <div class="opt1-vivek-sec">
        <div class="opt1-vivek-title" id="p-001-vivek-sec">❖ વિવેકધારા</div>
        <div class="opt1-vivek-grid">
          <div class="opt1-vivek-card ekant" id="p-001-ekant">
            <span class="opt1-vivek-head">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p style="margin: 0;">જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>
          <div class="opt1-vivek-card anekant" id="p-001-anekant">
            <span class="opt1-vivek-head">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p style="margin: 0;">આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
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

def generate_option_2():
    """Option 2: Modern Swiss Grid with Hairline Column Dividers (Inspired by Reference Image 2 Layout)"""
    opt_dir = BASE_DIR / "option_2_swiss_hairline_grid"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt2.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_PAGE_CSS}

    .running-header {{ border-bottom: 0.8pt solid #111; color: #111; }}
    .running-footer {{ border-top: 0.8pt solid #111; color: #111; }}

    /* Swiss Masthead */
    .opt2-masthead {{
      border-top: 1.5pt solid #111; border-bottom: 0.8pt solid #111;
      padding: 5pt 0; margin-bottom: 5pt;
    }}
    .opt2-kicker-row {{
      display: flex; justify-content: space-between; font-size: 8.5pt; font-weight: 700;
      letter-spacing: 0.6pt; text-transform: uppercase; color: #555;
    }}
    .opt2-title-box {{ margin: 4pt 0 2pt 0; }}
    .opt2-main-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 28pt; font-weight: 700; line-height: 1.22;
      color: #111; margin: 0; letter-spacing: -0.3pt;
    }}
    .opt2-en-meta {{ font-family: sans-serif; font-size: 8.8pt; color: #666; margin-top: 2pt; }}
    .opt2-sutra-strip {{
      margin-top: 4pt; padding-top: 3pt; border-top: 0.6pt solid #ccc;
      display: flex; justify-content: space-between; font-size: 9.5pt;
    }}
    .opt2-sutra-text {{ font-family: 'Noto Sans Devanagari', serif; font-weight: 700; color: #111; }}

    /* Section Ribbon */
    .opt2-ribbon {{ display: flex; align-items: center; gap: 8pt; margin: 2pt 0 4pt 0; }}
    .opt2-ribbon-tag {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 11pt; font-weight: 700;
      color: #111; letter-spacing: 0.5pt; text-transform: uppercase;
    }}
    .opt2-ribbon-tag::before {{ content: "■"; font-size: 8pt; margin-right: 4pt; }}
    .opt2-ribbon-line {{ flex: 1; height: 0.8pt; background: #111; }}

    /* 2 Column with Vertical Dividing Rule */
    .opt2-grid {{
      display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; row-gap: 6pt; flex: 1;
      position: relative;
    }}
    .opt2-card {{ font-size: 10.6pt; line-height: 1.45; text-align: justify; color: #111; }}
    .opt2-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.8pt; color: #111;
      display: block; margin-bottom: 2pt; border-bottom: 0.6pt solid #111; padding-bottom: 1pt;
    }}
    .opt2-vignette-item {{ position: relative; padding-left: 9pt; margin-bottom: 2.5pt; font-size: 10.2pt; }}
    .opt2-vignette-item:last-child {{ margin-bottom: 0; }}
    .opt2-vignette-item::before {{ content: "—"; position: absolute; left: 0; top: 0; color: #111; font-weight: bold; }}

    /* Inverted Solid Black Kavyadhara */
    .opt2-kavya-box {{
      margin-top: 5pt; background: #111; color: #fff; padding: 6pt 12pt;
      display: flex; align-items: center; gap: 12pt; border: 1pt solid #111;
    }}
    .opt2-kavya-badge {{
      border: 1pt solid #fff; padding: 2pt 6pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 9.5pt; font-weight: 700; white-space: nowrap;
    }}
    .opt2-kavya-verse {{
      font-family: 'Noto Sans Gujarati', sans-serif; font-size: 11.2pt; font-weight: 600;
      color: #fff; font-style: italic; margin: 0;
    }}

    /* Right Page */
    .opt2-story-top {{
      border-bottom: 1.5pt solid #111; padding-bottom: 4pt; margin-bottom: 5pt;
      display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt2-story-kicker {{ font-family: 'Anek Gujarati', sans-serif; font-size: 13pt; font-weight: 700; color: #111; }}
    .opt2-story-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 10.8pt; font-weight: 600; color: #444; }}

    .opt2-hero-row {{ display: flex; gap: 5.8mm; margin-bottom: 5pt; }}
    .opt2-art-frame {{
      width: 72mm; height: 44mm; flex-shrink: 0; border: 1.2pt solid #111; padding: 1.5pt; background: #fff;
    }}
    .opt2-art-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .opt2-pipasa {{
      flex: 1; display: flex; flex-direction: column; justify-content: space-between;
      font-size: 10.6pt; line-height: 1.45; text-align: justify;
    }}
    .opt2-dhara-badge {{
      border-bottom: 1.2pt solid #111; font-family: 'Anek Gujarati', sans-serif;
      font-size: 9.2pt; font-weight: 700; display: inline-block; margin-bottom: 2pt;
    }}
    .opt2-paan {{
      border-left: 3.5pt solid #111; padding: 5.5pt 8pt; background: #f8f8f8;
      font-size: 10.6pt; line-height: 1.45; text-align: justify; margin-bottom: 5pt;
    }}

    .opt2-vivek-sec {{ border-top: 1.2pt solid #111; padding-top: 4pt; }}
    .opt2-vivek-title {{ font-family: 'Anek Gujarati', sans-serif; font-size: 11.5pt; font-weight: 700; margin-bottom: 3pt; }}
    .opt2-vivek-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; }}
    .opt2-vivek-card {{
      border: 0.8pt solid #ccc; padding: 5pt 7pt; font-size: 10.2pt; line-height: 1.42; text-align: justify;
    }}
    .opt2-vivek-card.anekant {{ border-top: 3pt solid #111; background: #f4f4f4; }}
    .opt2-vivek-card.ekant {{ border-top: 3pt solid #888; }}
    .opt2-vivek-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10pt;
      margin-bottom: 2pt; display: block; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 2: Modern Swiss Grid with Hairline Dividers — પ્રકરણ ૧</title>
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
      <div class="opt2-masthead">
        <div class="opt2-kicker-row">
          <span>પ્રથમ ખંડ: નૈગમ નય &bull; જ્ઞાનનય</span>
          <span>મુખ્ય શ્રેણી: દ્રવ્યાર્થિક નય</span>
        </div>
        <div class="opt2-title-box">
          <h1 class="opt2-main-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="opt2-en-meta" id="p-001-meta">
            BHUTA NAIGAMA NAYA &bull; The Retrospective Standpoint: Seeing Eternal Continuity
          </div>
        </div>
        <div class="opt2-sutra-strip">
          <span class="opt2-sutra-text">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span>મૂળ આગમિક સૂત્ર</span>
        </div>
      </div>

      <div class="opt2-ribbon">
        <span class="opt2-ribbon-tag">તત્વધારા</span>
        <div class="opt2-ribbon-line"></div>
      </div>

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
          <div>
            <div class="opt2-vignette-item"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
            <div class="opt2-vignette-item"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
            <div class="opt2-vignette-item"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
          </div>
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

  <!-- PAGE 3 (RIGHT) -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt2-story-top">
        <span class="opt2-story-kicker" id="p-001-story-sec">✦ કથાધારા</span>
        <span class="opt2-story-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <div class="opt2-hero-row">
        <div class="opt2-art-frame">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>
        <div class="opt2-pipasa" id="p-001-pipasa">
          <div>
            <span class="opt2-dhara-badge">પિપાસા</span>
            <p style="margin: 0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>
        </div>
      </div>

      <div class="opt2-paan" id="p-001-paan">
        <span class="opt2-dhara-badge">પાન</span>
        <p style="margin: 0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
      </div>

      <div class="opt2-vivek-sec">
        <div class="opt2-vivek-title" id="p-001-vivek-sec">❖ વિવેકધારા</div>
        <div class="opt2-vivek-grid">
          <div class="opt2-vivek-card ekant" id="p-001-ekant">
            <span class="opt2-vivek-head">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p style="margin: 0;">જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>
          <div class="opt2-vivek-card anekant" id="p-001-anekant">
            <span class="opt2-vivek-head">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p style="margin: 0;">આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
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

def generate_option_3():
    """Option 3: Curved Geometry & Vertical Outer Ribbon (Inspired by Reference Image 3 Layout)"""
    opt_dir = BASE_DIR / "option_3_curved_geometry"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt3.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_PAGE_CSS}

    .running-header {{ border-bottom: 1pt solid #444; color: #444; }}
    .running-footer {{ border-top: 1pt solid #444; color: #444; }}

    /* Outer Accent Ribbon */
    .opt3-outer-ribbon {{
      position: absolute; top: 0; bottom: 0; width: 4mm; background: #222; z-index: 20;
    }}
    .page-even .opt3-outer-ribbon {{ left: 0; }}
    .page-odd .opt3-outer-ribbon {{ right: 0; }}

    /* Rounded Masthead */
    .opt3-masthead {{ border-bottom: 1.2pt solid #ccc; padding-bottom: 5pt; margin-bottom: 5pt; }}
    .opt3-kicker-row {{ display: flex; justify-content: space-between; align-items: center; }}
    .opt3-pill {{
      background: #222; color: #fff; padding: 2.5pt 10pt; border-radius: 12pt;
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt; font-weight: 700;
    }}
    .opt3-cat-pill {{
      border: 0.8pt solid #999; padding: 2pt 8pt; border-radius: 12pt;
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt; color: #444;
    }}
    .opt3-title-box {{ margin: 4pt 0 2pt 0; }}
    .opt3-main-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 28pt; font-weight: 700; line-height: 1.24;
      color: #111; margin: 0;
    }}
    .opt3-en-meta {{ font-family: sans-serif; font-size: 8.8pt; color: #555; margin-top: 2pt; }}
    .opt3-sutra-card {{
      background: #f4f4f4; border-radius: 4pt; padding: 4pt 8pt; margin-top: 4pt;
      display: flex; justify-content: space-between; align-items: baseline; border: 0.8pt solid #e0e0e0;
    }}
    .opt3-sutra-text {{ font-family: 'Noto Sans Devanagari', serif; font-size: 9.8pt; font-weight: 700; color: #111; }}
    .opt3-sutra-lbl {{ font-family: 'Anek Gujarati', sans-serif; font-size: 8pt; color: #666; }}

    /* Section Ribbon */
    .opt3-ribbon {{ display: flex; align-items: center; gap: 6pt; margin: 2pt 0 4pt 0; }}
    .opt3-ribbon-tag {{
      background: #444; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 10pt; font-weight: 700; padding: 2pt 8pt; border-radius: 8pt;
    }}
    .opt3-ribbon-line {{ flex: 1; height: 1pt; background: #ddd; }}

    /* Grid of Rounded Cards */
    .opt3-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; row-gap: 6pt; flex: 1; }}
    .opt3-card {{
      border: 0.8pt solid #ddd; border-radius: 4pt; padding: 5pt 7pt; background: #fff;
      font-size: 10.6pt; line-height: 1.44; text-align: justify;
    }}
    .opt3-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.8pt; color: #111;
      display: block; margin-bottom: 2pt; border-bottom: 0.6pt solid #eee; padding-bottom: 1pt;
    }}
    .opt3-vignette-item {{ position: relative; padding-left: 9pt; margin-bottom: 2.5pt; font-size: 10.2pt; }}
    .opt3-vignette-item:last-child {{ margin-bottom: 0; }}
    .opt3-vignette-item::before {{ content: "•"; position: absolute; left: 0; top: 0; color: #333; font-weight: bold; }}

    /* Rounded Kavyadhara */
    .opt3-kavya-box {{
      margin-top: 5pt; background: #f7f7f7; border: 1pt solid #ccc; border-radius: 6pt;
      padding: 6pt 10pt; display: flex; align-items: center; gap: 10pt;
    }}
    .opt3-kavya-badge {{
      background: #222; color: #fff; padding: 2.5pt 8pt; border-radius: 10pt;
      font-family: 'Anek Gujarati', sans-serif; font-size: 9pt; font-weight: 700; white-space: nowrap;
    }}
    .opt3-kavya-verse {{
      font-family: 'Noto Sans Gujarati', sans-serif; font-size: 11.2pt; font-weight: 600;
      color: #111; font-style: italic; margin: 0;
    }}

    /* Right Page */
    .opt3-story-top {{
      border-bottom: 1.2pt solid #ccc; padding-bottom: 4pt; margin-bottom: 5pt;
      display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt3-story-kicker {{ font-family: 'Anek Gujarati', sans-serif; font-size: 12.5pt; font-weight: 700; color: #222; }}
    .opt3-story-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 10.8pt; color: #555; }}

    .opt3-hero-row {{ display: flex; gap: 5.8mm; margin-bottom: 5pt; }}
    .opt3-art-frame {{
      width: 72mm; height: 44mm; flex-shrink: 0; border: 1pt solid #333; border-radius: 4pt;
      padding: 1.5pt; background: #fff; overflow: hidden;
    }}
    .opt3-art-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; border-radius: 3pt; }}
    .opt3-pipasa {{
      flex: 1; display: flex; flex-direction: column; justify-content: space-between;
      font-size: 10.6pt; line-height: 1.45; text-align: justify;
    }}
    .opt3-dhara-badge {{
      background: #444; color: #fff; padding: 1pt 6pt; border-radius: 6pt;
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.8pt; font-weight: 700; display: inline-block; margin-bottom: 2pt;
    }}
    .opt3-paan {{
      background: #f7f7f7; border: 0.8pt solid #ddd; border-radius: 4pt;
      padding: 5.5pt 8pt; font-size: 10.6pt; line-height: 1.45; text-align: justify; margin-bottom: 5pt;
    }}

    .opt3-vivek-sec {{ border-top: 1pt solid #ccc; padding-top: 4pt; }}
    .opt3-vivek-title {{ font-family: 'Anek Gujarati', sans-serif; font-size: 11.5pt; font-weight: 700; margin-bottom: 3pt; }}
    .opt3-vivek-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; }}
    .opt3-vivek-card {{
      border: 0.8pt solid #ddd; border-radius: 4pt; padding: 5pt 7pt; font-size: 10.2pt;
      line-height: 1.42; text-align: justify; background: #fafafa;
    }}
    .opt3-vivek-card.anekant {{ border-top: 3pt solid #222; background: #f2f2f2; }}
    .opt3-vivek-card.ekant {{ border-top: 3pt solid #888; }}
    .opt3-vivek-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10pt;
      margin-bottom: 2pt; display: block; border-bottom: 0.6pt solid #ddd; padding-bottom: 1pt;
    }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 3: Curved Geometry & Vertical Ribbon — પ્રકરણ ૧</title>
  {css}
</head>
<body>
<div class="spread-container">
  <!-- PAGE 2 (LEFT) -->
  <section class="page page-even" id="page-2">
    <div class="opt3-outer-ribbon"></div>
    <header class="running-header">
      <span style="font-weight:700;">નય-ચક્ષુ</span>
      <span style="margin: 0 6pt;">|</span>
      <span>નયનું જ્ઞાન, સંશયનું સમાધાન</span>
    </header>
    <main class="content-area">
      <div class="opt3-masthead">
        <div class="opt3-kicker-row">
          <div class="opt3-pill">પ્રથમ ખંડ: નૈગમ નય • જ્ઞાનનય</div>
          <div class="opt3-cat-pill">દ્રવ્યાર્થિક નય</div>
        </div>
        <div class="opt3-title-box">
          <h1 class="opt3-main-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="opt3-en-meta" id="p-001-meta">
            BHUTA NAIGAMA NAYA &bull; The Retrospective Standpoint: Seeing Eternal Continuity
          </div>
        </div>
        <div class="opt3-sutra-card">
          <span class="opt3-sutra-text">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span class="opt3-sutra-lbl">મૂળ આગમિક સૂત્ર</span>
        </div>
      </div>

      <div class="opt3-ribbon">
        <span class="opt3-ribbon-tag">તત્વધારા</span>
        <div class="opt3-ribbon-line"></div>
      </div>

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
          <div>
            <div class="opt3-vignette-item"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
            <div class="opt3-vignette-item"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
            <div class="opt3-vignette-item"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
          </div>
        </div>
        <div class="opt3-card" id="p-001-marm">
          <span class="opt3-card-head">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt3-kavya-box" id="p-001-kavya">
        <span class="opt3-kavya-badge">કાવ્યધારા</span>
        <blockquote class="opt3-kavya-verse">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) -->
  <section class="page page-odd" id="page-3">
    <div class="opt3-outer-ribbon"></div>
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt3-story-top">
        <span class="opt3-story-kicker" id="p-001-story-sec">✦ કથાધારા</span>
        <span class="opt3-story-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <div class="opt3-hero-row">
        <div class="opt3-art-frame">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>
        <div class="opt3-pipasa" id="p-001-pipasa">
          <div>
            <span class="opt3-dhara-badge">પિપાસા</span>
            <p style="margin: 0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>
        </div>
      </div>

      <div class="opt3-paan" id="p-001-paan">
        <span class="opt3-dhara-badge">પાન</span>
        <p style="margin: 0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
      </div>

      <div class="opt3-vivek-sec">
        <div class="opt3-vivek-title" id="p-001-vivek-sec">❖ વિવેકધારા</div>
        <div class="opt3-vivek-grid">
          <div class="opt3-vivek-card ekant" id="p-001-ekant">
            <span class="opt3-vivek-head">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p style="margin: 0;">જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>
          <div class="opt3-vivek-card anekant" id="p-001-anekant">
            <span class="opt3-vivek-head">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p style="margin: 0;">આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
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

def generate_option_4():
    """Option 4: Modular Boxed Panels & Speech-Bubble Quote (Inspired by Reference Image 4 Layout)"""
    opt_dir = BASE_DIR / "option_4_modular_boxed_panels"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt4.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_PAGE_CSS}

    .running-header {{ border-bottom: 1pt solid #222; color: #222; }}
    .running-footer {{ border-top: 1pt solid #222; color: #222; }}

    /* Modular Boxed Masthead */
    .opt4-masthead {{
      border: 1pt solid #222; padding: 4pt 8pt; background: #fafafa; margin-bottom: 3pt;
    }}
    .opt4-kicker-row {{ display: flex; justify-content: space-between; align-items: center; }}
    .opt4-tag-dark {{
      background: #222; color: #fff; padding: 2pt 8pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt; font-weight: 700;
    }}
    .opt4-tag-light {{
      border: 0.8pt solid #222; background: #fff; padding: 1.5pt 8pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.5pt; font-weight: 700; color: #222;
    }}
    .opt4-title-box {{ margin: 2pt 0 1pt 0; }}
    .opt4-main-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 26pt; font-weight: 700; line-height: 1.22;
      color: #111; margin: 0;
    }}
    .opt4-en-meta {{ font-family: sans-serif; font-size: 8.5pt; color: #555; margin-top: 1pt; }}
    .opt4-sutra-box {{
      background: #eee; border-left: 3pt solid #222; padding: 3pt 7pt; margin-top: 3pt;
      display: flex; justify-content: space-between; align-items: baseline;
    }}
    .opt4-sutra-text {{ font-family: 'Noto Sans Devanagari', serif; font-size: 9.8pt; font-weight: 700; color: #111; }}
    .opt4-sutra-lbl {{ font-family: 'Anek Gujarati', sans-serif; font-size: 8pt; color: #555; }}

    /* Section Ribbon */
    .opt4-ribbon {{ display: flex; align-items: center; gap: 6pt; margin: 1pt 0 3pt 0; }}
    .opt4-ribbon-tag {{
      border: 1pt solid #222; background: #fff; color: #111; font-family: 'Anek Gujarati', sans-serif;
      font-size: 9.5pt; font-weight: 700; padding: 1pt 7pt;
    }}
    .opt4-ribbon-line {{ flex: 1; height: 1pt; background: #222; }}

    /* Modular 2-Column Boxes with Header Tabs */
    .opt4-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; row-gap: 4pt; }}
    .opt4-panel-box {{
      border: 0.8pt solid #ccc; background: #fff; padding: 3.5pt 6pt; display: flex; flex-direction: column;
    }}
    .opt4-panel-tab {{
      background: #222; color: #fff; padding: 1pt 5pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.2pt; font-weight: 700; align-self: flex-start; margin-bottom: 2pt;
    }}
    .opt4-card {{ font-size: 10.4pt; line-height: 1.42; text-align: justify; }}
    .opt4-card p {{ margin: 0; }}
    .opt4-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.2pt; color: #111;
      display: block; margin-bottom: 2pt; border-bottom: 0.6pt solid #ddd; padding-bottom: 1pt;
    }}
    .opt4-vignette-item {{ position: relative; padding-left: 9pt; margin-bottom: 1.5pt; font-size: 9.8pt; }}
    .opt4-vignette-item:last-child {{ margin-bottom: 0; }}
    .opt4-vignette-item::before {{ content: "▸"; position: absolute; left: 0; top: -1pt; color: #222; font-size: 8pt; }}

    /* Speech Bubble / Quote Callout */
    .opt4-kavya-bubble {{
      margin-top: 4pt; background: #f5f5f5; border: 1pt solid #222; border-left: 4pt solid #222;
      padding: 4pt 10pt; display: flex; align-items: center; gap: 10pt; position: relative;
    }}
    .opt4-kavya-badge {{
      background: #222; color: #fff; padding: 2pt 6pt; font-family: 'Anek Gujarati', sans-serif;
      font-size: 9.5pt; font-weight: 700; white-space: nowrap;
    }}
    .opt4-kavya-verse {{
      font-family: 'Noto Sans Gujarati', sans-serif; font-size: 11.2pt; font-weight: 600;
      color: #111; font-style: italic; margin: 0;
    }}

    /* Right Page */
    .opt4-story-header {{
      background: #222; color: #fff; padding: 4pt 10pt; display: flex; justify-content: space-between;
      align-items: center; margin-bottom: 5pt;
    }}
    .opt4-story-kicker {{ font-family: 'Anek Gujarati', sans-serif; font-size: 12.5pt; font-weight: 700; }}
    .opt4-story-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 10.5pt; color: #ddd; }}

    .opt4-hero-row {{ display: flex; gap: 5.8mm; margin-bottom: 5pt; }}
    .opt4-art-frame {{
      width: 72mm; height: 44mm; flex-shrink: 0; border: 1pt solid #222; padding: 1.5pt; background: #fff;
    }}
    .opt4-art-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .opt4-pipasa {{
      flex: 1; display: flex; flex-direction: column; justify-content: space-between;
      font-size: 10.6pt; line-height: 1.45; text-align: justify;
    }}
    .opt4-dhara-badge {{
      background: #222; color: #fff; font-family: 'Anek Gujarati', sans-serif;
      font-size: 8.8pt; font-weight: 700; padding: 1pt 5pt; display: inline-block; margin-bottom: 2pt;
    }}
    .opt4-paan {{
      background: #f7f7f7; border: 0.8pt solid #ccc; border-left: 3.5pt solid #222;
      padding: 5.5pt 8pt; font-size: 10.6pt; line-height: 1.45; text-align: justify; margin-bottom: 5pt;
    }}

    .opt4-vivek-sec {{ border-top: 1.2pt solid #222; padding-top: 4pt; }}
    .opt4-vivek-title {{ font-family: 'Anek Gujarati', sans-serif; font-size: 11.5pt; font-weight: 700; margin-bottom: 3pt; }}
    .opt4-vivek-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; }}
    .opt4-vivek-card {{
      background: #fafafa; border: 0.8pt solid #ccc; padding: 5pt 7pt; font-size: 10.2pt;
      line-height: 1.42; text-align: justify;
    }}
    .opt4-vivek-card.anekant {{ border-top: 3pt solid #222; background: #f0f0f0; }}
    .opt4-vivek-card.ekant {{ border-top: 3pt solid #666; }}
    .opt4-vivek-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10pt; color: #111;
      margin-bottom: 2pt; display: block; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 4: Modular Boxed Panels & Speech-Bubble Quote — પ્રકરણ ૧</title>
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
      <div class="opt4-masthead">
        <div class="opt4-kicker-row">
          <div class="opt4-tag-dark">પ્રથમ ખંડ: નૈગમ નય • જ્ઞાનનય</div>
          <div class="opt4-tag-light">દ્રવ્યાર્થિક નય</div>
        </div>
        <div class="opt4-title-box">
          <h1 class="opt4-main-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
          <div class="opt4-en-meta" id="p-001-meta">
            BHUTA NAIGAMA NAYA &bull; The Retrospective Standpoint: Seeing Eternal Continuity
          </div>
        </div>
        <div class="opt4-sutra-box">
          <span class="opt4-sutra-text">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span class="opt4-sutra-lbl">મૂળ આગમિક સૂત્ર</span>
        </div>
      </div>

      <div class="opt4-ribbon">
        <span class="opt4-ribbon-tag">તત્વધારા</span>
        <div class="opt4-ribbon-line"></div>
      </div>

      <div class="opt4-grid">
        <div class="opt4-panel-box" id="p-001-rupak">
          <div class="opt4-panel-tab">૧. રૂપક-દ્રષ્ટિ</div>
          <div class="opt4-card">
            <span class="opt4-card-head">ઓલવાયેલા તારકનું જીવંત કિરણ</span>
            <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
          </div>
        </div>

        <div class="opt4-panel-box" id="p-001-swarup">
          <div class="opt4-panel-tab">૨. સ્વરૂપ-સૃષ્ટિ</div>
          <div class="opt4-card">
            <span class="opt4-card-head">કાળના પડદા પાર જોતી આંખ</span>
            <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
          </div>
        </div>

        <div class="opt4-panel-box" id="p-001-vyavahar">
          <div class="opt4-panel-tab">૩. વ્યવહાર-પૃષ્ટિ</div>
          <div class="opt4-card">
            <span class="opt4-card-head">જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
            <div>
              <div class="opt4-vignette-item"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
              <div class="opt4-vignette-item"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
              <div class="opt4-vignette-item"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
            </div>
          </div>
        </div>

        <div class="opt4-panel-box" id="p-001-marm">
          <div class="opt4-panel-tab">૪. મર્મ-તુષ્ટિ</div>
          <div class="opt4-card">
            <span class="opt4-card-head">ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
            <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
          </div>
        </div>
      </div>

      <div class="opt4-kavya-bubble" id="p-001-kavya">
        <span class="opt4-kavya-badge">કાવ્યધારા</span>
        <blockquote class="opt4-kavya-verse">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">|</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt4-story-header">
        <span class="opt4-story-kicker" id="p-001-story-sec">✦ કથાધારા</span>
        <span class="opt4-story-sub" id="p-001-story-title">નવલિકા: ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <div class="opt4-hero-row">
        <div class="opt4-art-frame">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>
        <div class="opt4-pipasa" id="p-001-pipasa">
          <div>
            <span class="opt4-dhara-badge">પિપાસા</span>
            <p style="margin: 0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>
        </div>
      </div>

      <div class="opt4-paan" id="p-001-paan">
        <span class="opt4-dhara-badge">પાન</span>
        <p style="margin: 0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
      </div>

      <div class="opt4-vivek-sec">
        <div class="opt4-vivek-title" id="p-001-vivek-sec">❖ વિવેકધારા</div>
        <div class="opt4-vivek-grid">
          <div class="opt4-vivek-card ekant" id="p-001-ekant">
            <span class="opt4-vivek-head">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p style="margin: 0;">જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>
          <div class="opt4-vivek-card anekant" id="p-001-anekant">
            <span class="opt4-vivek-head">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p style="margin: 0;">આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
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

def generate_option_5():
    """Option 5: Minimalist Brutalist / Swiss Linear Elegance (Inspired by Reference Image 5 Layout)"""
    opt_dir = BASE_DIR / "option_5_minimalist_linear"
    opt_dir.mkdir(parents=True, exist_ok=True)
    html_file = opt_dir / "chapter_001_opt5.html"

    css = f"""
    <style>
    {FONT_CSS}
    {COMMON_PAGE_CSS}

    .running-header {{ border-bottom: 0.6pt solid #222; color: #444; letter-spacing: 0.5pt; }}
    .running-footer {{ border-top: 0.6pt solid #222; color: #444; }}

    /* Minimalist Classical Masthead */
    .opt5-masthead {{
      border-top: 1.5pt solid #111; border-bottom: 0.8pt solid #111;
      padding: 5pt 0; margin-bottom: 5pt; text-align: center;
    }}
    .opt5-kicker {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 8.5pt; font-weight: 700;
      letter-spacing: 1.2pt; text-transform: uppercase; color: #555; margin-bottom: 2pt;
    }}
    .opt5-main-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 28pt; font-weight: 700; line-height: 1.22;
      color: #111; margin: 0; letter-spacing: -0.2pt;
    }}
    .opt5-en-meta {{
      font-family: sans-serif; font-size: 8.8pt; font-style: italic; color: #666; margin-top: 2.5pt;
    }}
    .opt5-sutra-box {{
      margin-top: 4pt; padding: 3pt 0; border-top: 0.5pt solid #ddd;
      display: flex; justify-content: center; gap: 8pt; align-items: baseline;
    }}
    .opt5-sutra-text {{ font-family: 'Noto Sans Devanagari', serif; font-size: 9.8pt; font-weight: 700; color: #111; }}
    .opt5-sutra-tag {{ font-family: 'Anek Gujarati', sans-serif; font-size: 8pt; color: #777; text-transform: uppercase; }}

    /* Section Ribbon */
    .opt5-ribbon {{
      display: flex; align-items: center; justify-content: center; gap: 8pt; margin: 2pt 0 4pt 0;
    }}
    .opt5-ribbon-line {{ flex: 1; height: 0.6pt; background: #111; }}
    .opt5-ribbon-tag {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 11pt; font-weight: 700;
      letter-spacing: 1.2pt; color: #111; text-transform: uppercase;
    }}

    /* 2 Column Clean Linear Prose */
    .opt5-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; row-gap: 6pt; flex: 1; }}
    .opt5-card {{ font-size: 10.6pt; line-height: 1.45; text-align: justify; color: #222; }}
    .opt5-card-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10.8pt; color: #111;
      display: block; margin-bottom: 2pt; border-bottom: 0.6pt solid #ccc; padding-bottom: 1pt;
    }}
    .opt5-vignette-item {{ position: relative; padding-left: 9pt; margin-bottom: 2.5pt; font-size: 10.2pt; }}
    .opt5-vignette-item:last-child {{ margin-bottom: 0; }}
    .opt5-vignette-item::before {{ content: "—"; position: absolute; left: 0; top: 0; color: #555; }}

    /* Centered Diamond Poetic Callout */
    .opt5-kavya-box {{
      margin-top: 5pt; border-top: 0.8pt solid #111; border-bottom: 0.8pt solid #111;
      padding: 5pt 14pt; text-align: center;
    }}
    .opt5-kavya-glyph {{ font-size: 8.5pt; color: #666; margin-bottom: 1pt; letter-spacing: 3pt; }}
    .opt5-kavya-verse {{
      font-family: 'Noto Sans Gujarati', sans-serif; font-size: 11.2pt; font-weight: 600;
      color: #111; font-style: italic; margin: 0;
    }}

    /* Right Page */
    .opt5-story-masthead {{
      border-bottom: 0.8pt solid #111; padding-bottom: 4pt; margin-bottom: 5pt; text-align: center;
    }}
    .opt5-story-kicker {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 9pt; font-weight: 700;
      letter-spacing: 1.5pt; text-transform: uppercase; color: #666; display: block; margin-bottom: 1pt;
    }}
    .opt5-story-sub {{ font-family: 'Anek Gujarati', sans-serif; font-size: 13pt; font-weight: 700; color: #111; }}

    .opt5-hero-row {{ display: flex; gap: 5.8mm; margin-bottom: 5pt; }}
    .opt5-art-frame {{
      width: 72mm; height: 44mm; flex-shrink: 0; border: 0.8pt solid #111; padding: 2pt;
    }}
    .opt5-art-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .opt5-pipasa {{
      flex: 1; display: flex; flex-direction: column; justify-content: space-between;
      font-size: 10.6pt; line-height: 1.45; text-align: justify;
    }}
    .opt5-dhara-badge {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 9pt; font-weight: 700;
      color: #111; border-bottom: 0.8pt solid #111; display: inline-block; margin-bottom: 2pt;
    }}
    .opt5-paan {{
      background: #fafafa; border: 0.6pt solid #ddd; border-left: 3pt solid #111;
      padding: 5.5pt 8pt; font-size: 10.6pt; line-height: 1.45; text-align: justify; margin-bottom: 5pt;
    }}

    .opt5-vivek-sec {{ border-top: 0.8pt solid #111; padding-top: 4pt; }}
    .opt5-vivek-title {{
      font-family: 'Anek Gujarati', sans-serif; font-size: 11pt; font-weight: 700;
      letter-spacing: 1pt; text-transform: uppercase; color: #111; text-align: center; margin-bottom: 3pt;
    }}
    .opt5-vivek-grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 5.8mm; }}
    .opt5-vivek-card {{
      border: 0.6pt solid #ccc; padding: 5pt 7pt; font-size: 10.2pt;
      line-height: 1.42; text-align: justify; background: #fafafa;
    }}
    .opt5-vivek-card.anekant {{ border-top: 2.5pt solid #111; }}
    .opt5-vivek-card.ekant {{ border-top: 2.5pt solid #666; }}
    .opt5-vivek-head {{
      font-family: 'Anek Gujarati', sans-serif; font-weight: 700; font-size: 10pt; color: #111;
      margin-bottom: 2pt; display: block; border-bottom: 0.6pt solid #ddd; padding-bottom: 1pt;
    }}
    </style>
    """

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>Option 5: Minimalist Linear Elegance — પ્રકરણ ૧</title>
  {css}
</head>
<body>
<div class="spread-container">
  <!-- PAGE 2 (LEFT) -->
  <section class="page page-even" id="page-2">
    <header class="running-header">
      <span style="font-weight:700;">નય-ચક્ષુ</span>
      <span style="margin: 0 6pt;">—</span>
      <span>નયનું જ્ઞાન, સંશયનું સમાધાન</span>
    </header>
    <main class="content-area">
      <div class="opt5-masthead">
        <div class="opt5-kicker">પ્રથમ ખંડ: નૈગમ નય • જ્ઞાનનય &bull; દ્રવ્યાર્થિક નય</div>
        <h1 class="opt5-main-title" id="p-001-title">૧. ભૂતનૈગમ નય</h1>
        <div class="opt5-en-meta" id="p-001-meta">Bhuta Naigama Naya — The Retrospective Standpoint: Seeing Eternal Continuity</div>
        <div class="opt5-sutra-box">
          <span class="opt5-sutra-text">अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।</span>
          <span class="opt5-sutra-tag">(મૂળ આગમિક સૂત્ર)</span>
        </div>
      </div>

      <div class="opt5-ribbon">
        <div class="opt5-ribbon-line"></div>
        <span class="opt5-ribbon-tag">તત્વધારા</span>
        <div class="opt5-ribbon-line"></div>
      </div>

      <div class="opt5-grid">
        <div class="opt5-card" id="p-001-rupak">
          <span class="opt5-card-head">૧. રૂપક-દ્રષ્ટિ: ઓલવાયેલા તારકનું જીવંત કિરણ</span>
          <p>અનંત આકાશમાં અબજો વર્ષ પૂર્વે એક તારો ભસ્મીભૂત થઈને ઓલવાઈ ગયો હોય, છતાં આજે રાત્રે તેનું કિરણ આપણી આંખ સામે એટલું જ તેજસ્વી અને જીવંત ચમકે છે. ભૌતિક રૂપે જે વીતી ચૂક્યું છે, તે જ્ઞાતાના જ્ઞાન-ફલક પર આ ક્ષણે પણ પ્રત્યક્ષ પ્રકાશમાન છે. આ જ દ્રષ્ટિ એટલે <strong>'ભૂતનૈગમ નય'</strong>.</p>
        </div>
        <div class="opt5-card" id="p-001-swarup">
          <span class="opt5-card-head">૨. સ્વરૂપ-સૃષ્ટિ: કાળના પડદા પાર જોતી આંખ</span>
          <p>ભૂતકાળમાં જે ઘટના કે પર્યાય પૂર્ણ થઈ ચૂકી છે, તેને સ્મૃતિના બંધ કબાટમાં રાખવાને બદલે જ્ઞાનના સંકલ્પ વડે વર્તમાનમાં એવી રીતે પ્રત્યક્ષ અનુભવવી કે જાણે તે આ પળે જ આપણી નજર સામે ઘટી રહી હોય! આ નય કાળના અંતરને ભૂંસી નાખીને વસ્તુના અખંડ સત્-સાતત્યને જોવાની દિવ્ય બારી છે.</p>
        </div>
        <div class="opt5-card" id="p-001-vyavahar">
          <span class="opt5-card-head">૩. વ્યવહાર-પૃષ્ટિ: જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
          <div>
            <div class="opt5-vignette-item"><strong>દિવાળીનો દીવો:</strong> રાત્રે બાળક પણ હર્ષથી પોકારે: <em>"આજે મહાવીર પ્રભુ મોક્ષ પધાર્યા!"</em> ૨૫૦૦ વર્ષ પૂર્વેની ક્ષણ હૃદયમાં આજના તહેવાર જેવી જ જીવંત બને છે.</div>
            <div class="opt5-vignette-item"><strong>માતાનું વાત્સલ્ય:</strong> ચાલીસ વર્ષના પુખ્ત પુત્રને જોઈ વૃદ્ધ માતા <em>"મારું નાનું બાળક"</em> કહી છાતીએ લગાડે છે. માતાની આંખમાં પુત્રનું અતીત-બાળપણ રમતું હોય છે.</div>
            <div class="opt5-vignette-item"><strong>બીજ અને જળ:</strong> માળી સૂકી ગોટલી જોઈ કહે: <em>"આ મારો આંબો છે,"</em> અને જળને જોઈ કહેવાય: <em>"આ હિમાલયનો બરફ છે."</em></div>
          </div>
        </div>
        <div class="opt5-card" id="p-001-marm">
          <span class="opt5-card-head">૪. મર્મ-તુષ્ટિ: ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
          <p>ઘણાને ભ્રમ થાય છે કે આ તો માત્ર જૂની યાદ કે માનસિક કલ્પના (સ્મૃતિ) છે, પણ વાસ્તવમાં આ કેવળ સ્મૃતિ નથી; આ તો વસ્તુના અખંડ અસ્તિત્વનો સ્વીકાર છે. અતીત એ કાળના અંધકારમાં ડૂબી ગયેલું શૂન્ય નથી, પણ વર્તમાનની પરિપક્વતાનું જીવંત મૂળિયું છે. જે દ્રષ્ટિ અતીતના સત્યને વર્તમાનમાં સન્માની શકે, તે જ સાચી નય-દ્રષ્ટિ છે.</p>
        </div>
      </div>

      <div class="opt5-kavya-box" id="p-001-kavya">
        <div class="opt5-kavya-glyph">◆ ◆ ◆</div>
        <blockquote class="opt5-kavya-verse">“અતીતનો પર્યાય જે, કાળે થઈ વિનષ્ટ; જ્ઞાન તણા સંકલ્પથી, આ પળ ભાસે સ્પષ્ટ.”</blockquote>
      </div>
    </main>
    <footer class="running-footer">
      <span class="page-num">૨</span>
      <span class="footer-label">પ્રથમ ખંડ: નૈગમ નય</span>
    </footer>
  </section>

  <!-- PAGE 3 (RIGHT) -->
  <section class="page page-odd" id="page-3">
    <header class="running-header">
      <span style="font-weight:700;">પ્રથમ ખંડ: નૈગમ નય</span>
      <span style="margin: 0 6pt;">—</span>
      <span>૧. ભૂતનૈગમ નય</span>
    </header>
    <main class="content-area">
      <div class="opt5-story-masthead">
        <span class="opt5-story-kicker" id="p-001-story-sec">કથાધારા</span>
        <span class="opt5-story-sub" id="p-001-story-title">ઓલવાયેલા દીવાનું અમૃત-તેજ</span>
      </div>

      <div class="opt5-hero-row">
        <div class="opt5-art-frame">
          <img src="../assets/images/chapter_001_art.svg" alt="આર્ટવર્ક" />
        </div>
        <div class="opt5-pipasa" id="p-001-pipasa">
          <div>
            <span class="opt5-dhara-badge">પિપાસા</span>
            <p style="margin: 0;">રમેશભાઈ પોતાના યુવાન પુત્ર આનંદની એક વ્યાપારિક ભૂલથી અત્યંત ક્રોધિત અને વ્યથિત હતા. આનંદના એક અવિચારી નિર્ણયથી પેઢીને મોટો આર્થિક ફટકો પડ્યો હતો. રમેશભાઈના મગજમાં નિરંતર નકારાત્મક વલયો ઘૂમરાતા હતા: <em>"આટલો મોટો થઈને આવી નાદાની કેમ કરી? આખી જિંદગીનું પરિશ્રમ એક પળમાં રોળાઈ ગયું!"</em> ક્રોધ ઊંડા વિષાદમાં પલટાઈ ગયો હતો. સંબંધોમાં તીખી તિરાડ પડી ચૂકી હતી. રાત્રિના અંધકારમાં છત તરફ તાકતાં તેમના હૃદયમાંથી વિવશ પોકાર ઊઠ્યો: <strong>"આ વિષમ ગૂંચવણમાંથી બહાર નીકળવાનો હવે શું રસ્તો?"</strong></p>
          </div>
        </div>
      </div>

      <div class="opt5-paan" id="p-001-paan">
        <span class="opt5-dhara-badge">પાન</span>
        <p style="margin: 0;">તે જ ક્ષણે ઘરના એકાંત ખૂણામાં બિરાજમાન વૃદ્ધ દાદાજીએ રમેશભાઈના ખભા પર સ્નેહભર્યો હાથ મૂક્યો અને અત્યંત શાંત સ્વરે કહ્યું, <em>"બેટા, જરા ભૂતનૈગમ દ્રષ્ટિથી જો. આજે ભલે એનાથી ભૂલ થઈ, પણ ભૂતકાળમાં આજ આનંદે રાત-દિવસ એક કરીને તારી પેઢીને સંકટમાંથી ઉગારી હતી અને તારી જીવલેણ બીમારીમાં અવિરત સેવા કરી હતી, તે શું સાવ મિથ્યા થઈ ગયું? વર્તમાનની એક ભૂલ પાછળ તેના અતીતના સો ઉપકારોને કેમ ભૂલી જાય છે?"</em> દાદાજીના આ બોધ-અમૃતનું પાન કરતાં જ રમેશભાઈની ભીતરમાં અતીતનો સ્નેહ સજીવન થઈ ઊઠ્યો. ક્રોધ પળવારમાં ઓગળી ગયો, આંખોમાંથી પશ્ચાત્તાપના આંસુ વહી નીકળ્યા અને અંતરમાં અસીમ ક્ષમા અને પરમ વિશ્રામ છવાઈ ગયો.</p>
      </div>

      <div class="opt5-vivek-sec">
        <div class="opt5-vivek-title" id="p-001-vivek-sec">વિવેકધારા</div>
        <div class="opt5-vivek-grid">
          <div class="opt5-vivek-card ekant" id="p-001-ekant">
            <span class="opt5-vivek-head">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</span>
            <p style="margin: 0;">જો આ નય-દ્રષ્ટિ જીદ કે કદાગ્રહ બને, તો મનુષ્ય ભૂતકાળના જડ વળગણોમાં કેદી બની જાય છે. <em>"અમારા જમાનામાં આમ જ થતું હતું"</em> એવી હઠ પકડીને તે વર્તમાનના નવા સત્યો અને પરિસ્થિતિઓનો અસ્વીકાર કરે છે. જૂના વેર, કડવી સ્મૃતિઓ કે પૂર્વજોના અહંકારને છાતીએ વળગાડી રાખવાથી જીવનમાં જડતા, અસહિષ્ણુતા અને સંબંધોમાં કાયમી સંકુચિતતા જન્મે છે.</p>
          </div>
          <div class="opt5-vivek-card anekant" id="p-001-anekant">
            <span class="opt5-vivek-head">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</span>
            <p style="margin: 0;">આ જ નય-દ્રષ્ટિ જો સમન્વયની યાત્રા બને, તો તે અતીતના સારને ગ્રહણ કરીને વર્તમાનને સમૃદ્ધ બનાવે છે. તે અતીતના તીર્થંકરો અને જ્ઞાનીઓના મુક્તિ-પ્રકાશને આત્મસાત કરી સાધ્ય તરફ સરકવાનું બળ બને છે. અહીં ભૂતકાળ બોજ નથી બનતો, પરંતુ ભવિષ્યના મોક્ષમાર્ગનું મંગલ પ્રસ્થાન અને આધ્યાત્મિક જીવન-યાત્રાનું પરમ સૌંદર્ય પ્રગટાવે છે.</p>
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

def render_option(opt_name, opt_dir, html_file):
    pdf_path = opt_dir / f"{html_file.stem}.pdf"
    spread_img = opt_dir / f"spread_{html_file.stem}.png"
    p2_img = opt_dir / f"page_2_{html_file.stem}.png"
    p3_img = opt_dir / f"page_3_{html_file.stem}.png"

    print(f"\\nRendering {opt_name}...")

    # 1. Print PDF
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

    # 2. Spread Screenshot
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
    options = [
        ("Option 1: Architectural Block & Asymmetric Card (Ref Image 1)", *generate_option_1()),
        ("Option 2: Modern Swiss Grid with Hairline Dividers (Ref Image 2)", *generate_option_2()),
        ("Option 3: Curved Geometry & Vertical Ribbon (Ref Image 3)", *generate_option_3()),
        ("Option 4: Modular Boxed Panels & Speech-Bubble Quote (Ref Image 4)", *generate_option_4()),
        ("Option 5: Minimalist Linear Elegance (Ref Image 5)", *generate_option_5())
    ]

    results = []
    for opt_name, opt_dir, html_file in options:
        res = render_option(opt_name, opt_dir, html_file)
        results.append(res)

    print("\\n" + "=" * 60)
    print("ALL 5 PURE GRAYSCALE PILOT OPTIONS SUCCESSFULLY GENERATED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
