import re
import json
import time
from pathlib import Path
from typing import Dict, Any, List

# Local gender sanitizer
try:
    from .gender_fixer import sanitize_paryaya_gender
except ImportError:
    from gender_fixer import sanitize_paryaya_gender


def clean_markdown_inline(text: str) -> str:
    """Removes bold/italic markdown markers from inline text if needed, or converts to <strong>/<em>."""
    # Convert **bold** to <strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Convert *italic* to <em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    return text.strip()


def parse_chapter(md_path: Path, img_record: Dict[str, Any], global_page_even: int) -> Dict[str, Any]:
    raw_text = md_path.read_text(encoding="utf-8")
    text, fixes = sanitize_paryaya_gender(raw_text)

    # 1. Title & Meta
    title_m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else md_path.stem

    meta_m = re.search(r'^\*\((.+?)\)\*', text, re.MULTILINE)
    khanda_pill = "નૈગમ નય"
    aspect_label = "જ્ઞાનનય"
    category_label = "મુખ્ય શ્રેણી: દ્રવ્યાર્થિક નય"
    sutra_text = "अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।"

    if meta_m:
        meta_str = meta_m.group(1)
        parts = [p.strip() for p in meta_str.split('|')]
        for p in parts:
            if 'મૂળ નય:' in p:
                khanda_pill = p.replace('મૂળ નય:', '').strip()
            elif 'મુખ્ય શ્રેણી:' in p:
                cat_val = p.replace('મુખ્ય શ્રેણી:', '').strip()
                if '-' in cat_val:
                    cparts = cat_val.split('-')
                    category_label = f"મુખ્ય શ્રેણી: {cparts[0].strip()}"
                    aspect_label = cparts[1].strip()
                else:
                    category_label = f"મુખ્ય શ્રેણી: {cat_val}"
            elif 'વ્યાખ્યા-સૂત્ર:' in p:
                sutra_text = p.replace('વ્યાખ્યા-સૂત્ર:', '').strip()

    # Meta right: English concept & Gujarati general term
    # Deriving general terms from chapter context
    gu_term = "વસ્તુના સ્વરૂપને સમજવાની દ્રષ્ટિ"
    en_term = "The Analytical Standpoint"
    if "ભૂતનૈગમ" in title:
        gu_term = "ભૂતકાળને વર્તમાનમાં જોવાની દ્રષ્ટિ"
        en_term = "The Retrospective Standpoint: Continuity"
    elif "ભાવિનૈગમ" in title:
        gu_term = "ભવિષ્યના સત્યને વર્તમાનમાં જોવાની દ્રષ્ટિ"
        en_term = "The Prospective Standpoint: Potentiality"
    elif "વર્તમાનનૈગમ" in title or "વર્તમાન" in title:
        gu_term = "આરંભમાં પૂર્ણતા જોવાની દ્રષ્ટિ"
        en_term = "The Intentional Standpoint: Teleology"
    elif "સંગ્રહ" in title:
        gu_term = "અભેદ અને એકતા જોવાની દ્રષ્ટિ"
        en_term = "The Synthetic Standpoint: Universality"
    elif "વ્યવહાર" in title:
        gu_term = "ભેદ અને પ્રયોજન સાધવાની દ્રષ્ટિ"
        en_term = "The Practical Standpoint: Differentiation"
    elif "ઋજુસૂત્ર" in title:
        gu_term = "વર્તમાન એક સમયના પર્યાયની દ્રષ્ટિ"
        en_term = "The Instantaneous Standpoint: Pure Present"
    elif "શબ્દ" in title:
        gu_term = "શબ્દ-વ્યુત્પત્તિ અને ભાષાની દ્રષ્ટિ"
        en_term = "The Verbal Standpoint: Linguistics"
    elif "સમભિરૂઢ" in title:
        gu_term = "પર્યાયવાચી શબ્દોના સૂક્ષ્મ ભેદની દ્રષ્ટિ"
        en_term = "The Etymological Standpoint: Nuance"
    elif "એવંભૂત" in title:
        gu_term = "તત્ક્ષણ ક્રિયાન્વિત વાસ્તવિકતાની દ્રષ્ટિ"
        en_term = "The Actualized Standpoint: Action"

    # 2. Tattvadhara (4 Cards)
    c1_m = re.search(r'\*\*૧\.\s*રૂપક-દ્રષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\*\*૨\.|\n##)', text)
    c1_sub = c1_m.group(1).strip() if c1_m else ""
    c1_body = clean_markdown_inline(c1_m.group(2).strip()) if c1_m else ""

    c2_m = re.search(r'\*\*૨\.\s*સ્વરૂપ-સૃષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\*\*૩\.|\n##)', text)
    c2_sub = c2_m.group(1).strip() if c2_m else ""
    c2_body = clean_markdown_inline(c2_m.group(2).strip()) if c2_m else ""

    c3_m = re.search(r'\*\*૩\.\s*વ્યવહાર-પૃષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\*\*૪\.|\n##)', text)
    c3_sub = c3_m.group(1).strip() if c3_m else ""
    c3_raw_body = c3_m.group(2).strip() if c3_m else ""

    # Parse Card 3 bullets
    c3_bullets = []
    for line in c3_raw_body.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Remove blockquote '>' and list '-' or '•'
        line = re.sub(r'^[>\s\-•\*]+', '', line).strip()
        if line:
            c3_bullets.append(clean_markdown_inline(line))

    c4_m = re.search(r'\*\*૪\.\s*મર્મ-તુષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\n##|---)', text)
    c4_sub = c4_m.group(1).strip() if c4_m else ""
    c4_body = clean_markdown_inline(c4_m.group(2).strip()) if c4_m else ""

    # 3. Kavyadhara & Sadhanadhara
    kavya_m = re.search(r'\|\s*📜\s*કાવ્યધારા\s*\|\s*✦\s*સાધનાધારા\s*\|\s*\n\|[-:| ]+\|\s*\n\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', text)
    if kavya_m:
        kavya_text = kavya_m.group(1).strip().replace('<br>', '\n').replace('<br/>', '\n')
        sadhana_text = clean_markdown_inline(kavya_m.group(2).strip())
    else:
        kavya_text = "સહજ નય પ્રકાશે, આતમ રસ ભાસે."
        sadhana_text = "પર્યાયની ક્ષણિકતા જાણી અવિનાશી આત્મસ્વભાવમાં લીન થવું."

    # 4. Kathadhara
    katha_sec_m = re.search(r'## કથાધારા[\s\S]*?###\s*([^\n]+)\s*\n\s*###\s*પિપાસા\s*\n([\s\S]*?)\s*###\s*પાન\s*\n([\s\S]*?)(?=\n##|---)', text)
    if katha_sec_m:
        story_title = katha_sec_m.group(1).strip()
        pipasa_body = clean_markdown_inline(katha_sec_m.group(2).strip())
        paan_body = clean_markdown_inline(katha_sec_m.group(3).strip())
    else:
        story_title = img_record.get('story_title', 'કથા વિષય') if img_record else "કથા વિષય"
        pipasa_body = "પિપાસા વિવરણ..."
        paan_body = "પાન વિવરણ..."

    # 5. Vivekdhara
    vivek_m = re.search(r'## વિવેકધારા[\s\S]*?###\s*એકાંત દર્શન\s*\n([\s\S]*?)\s*###\s*અનેકાંત દર્શન\s*\n([\s\S]*?)(?=\n##|---)', text)
    if vivek_m:
        ekant_body = clean_markdown_inline(vivek_m.group(1).strip())
        anekant_body = clean_markdown_inline(vivek_m.group(2).strip())
    else:
        ekant_body = "એકાંત દર્શન વિવરણ..."
        anekant_body = "અનેકાંત દર્શન વિવરણ..."

    # 6. Darshandhara (4 pillars)
    darshan_m1 = re.search(r'-\s*\*\*૧\.\s*નય-ઉન્મેષ\*\*:\s*([^\n]+)', text)
    darshan_m2 = re.search(r'-\s*\*\*૨\.\s*પ્રાચીન-વિશેષ\*\*:\s*([^\n]+)', text)
    darshan_m3 = re.search(r'-\s*\*\*૩\.\s*અર્વાચીન-પ્રવેશ\*\*:\s*([^\n]+)', text)
    darshan_m4 = re.search(r'-\s*\*\*૪\.\s*સમન્વય-અશેષ\*\*:\s*([^\n]+)', text)

    darshan_p1 = clean_markdown_inline(darshan_m1.group(1).strip()) if darshan_m1 else ""
    darshan_p2 = clean_markdown_inline(darshan_m2.group(1).strip()) if darshan_m2 else ""
    darshan_p3 = clean_markdown_inline(darshan_m3.group(1).strip()) if darshan_m3 else ""
    darshan_p4 = clean_markdown_inline(darshan_m4.group(1).strip()) if darshan_m4 else ""

    # Image
    image_rel = img_record.get('html_src', '') if img_record else ''
    image_key = img_record.get('key', 'K01_C001') if img_record else 'K01_C001'

    # Long title detection
    is_long_title = len(title) > 28

    return {
        "title": title,
        "is_long_title": is_long_title,
        "khanda_pill": khanda_pill,
        "aspect_label": aspect_label,
        "category_label": category_label,
        "gu_term": gu_term,
        "en_term": en_term,
        "sutra_text": sutra_text,
        "c1_sub": c1_sub,
        "c1_body": c1_body,
        "c2_sub": c2_sub,
        "c2_body": c2_body,
        "c3_sub": c3_sub,
        "c3_bullets": c3_bullets,
        "c4_sub": c4_sub,
        "c4_body": c4_body,
        "kavya_text": kavya_text,
        "sadhana_text": sadhana_text,
        "story_title": story_title,
        "pipasa_body": pipasa_body,
        "paan_body": paan_body,
        "ekant_body": ekant_body,
        "anekant_body": anekant_body,
        "darshan_p1": darshan_p1,
        "darshan_p2": darshan_p2,
        "darshan_p3": darshan_p3,
        "darshan_p4": darshan_p4,
        "image_rel": image_rel,
        "image_key": image_key,
        "page_even": global_page_even,
        "page_odd": global_page_even + 1,
        "gender_fixes": fixes,
        "source_file": md_path.name
    }


def render_chapter_spread_html(data: Dict[str, Any], img_prefix: str = "../../../") -> str:
    """Renders the 2-page spread HTML for a single chapter."""
    img_src = f"{img_prefix}{data['image_rel']}" if data['image_rel'] else ""
    
    title_class = "chapter-main-title title-long" if data['is_long_title'] else "chapter-main-title"

    c3_items_html = "\n".join([f'            <li>{b}</li>' for b in data['c3_bullets']])

    kavya_lines = data['kavya_text'].replace('\n', '<br>\n              ')

    return f"""
<!-- =============================================================
     CHAPTER: {data['title']} (PAGES {data['page_even']} & {data['page_odd']})
     ============================================================= -->
<div class="spread-container" id="spread-{data['image_key']}">

  <!-- ==================== LEFT PAGE ({data['page_even']}) ==================== -->
  <section class="page page-even">
    <div class="page-canvas">

      <!-- Chapter Masthead -->
      <div class="chapter-masthead">
        <div class="kicker-row">
          <div class="khanda-pill">
            <span>{data['khanda_pill']}</span>
            <span class="khanda-pill-sub">{data['aspect_label']}</span>
          </div>
          <div class="category-tag">{data['category_label']}</div>
        </div>

        <div class="chapter-title-row">
          <h1 class="{title_class}">{data['title']}</h1>
          <div class="chapter-sub-meta-right">
            <span class="gu-general-term">{data['gu_term']}</span>
            <span class="en-concept">{data['en_term']}</span>
          </div>
        </div>

        <div class="sutra-showcase">
          <span class="sutra-devanagari">{data['sutra_text']}</span>
          <span class="sutra-label">મૂળ આગમિક લક્ષણ-સૂત્ર</span>
        </div>
      </div>

      <!-- Section Ribbon -->
      <div class="section-ribbon">
        <span class="ribbon-badge">તત્વધારા</span>
        <div class="ribbon-rule"></div>
      </div>

      <!-- Tattvadhara 4-Card Grid (Left-to-Right Natural Reading Axis, 11pt) -->
      <div class="tattva-infographic-grid">
        
        <!-- 1. Rupak Drishti -->
        <div class="tattva-card-shell tattva-card-1">
          <div class="card-top-row">
            <span class="step-badge">૦૧</span>
            <div class="card-header-titles">
              <span class="card-main-heading">રૂપક-દ્રષ્ટિ:</span>
              <span class="card-sub-kicker">{data['c1_sub']}</span>
            </div>
          </div>
          <p class="card-body-text">{data['c1_body']}</p>
        </div>

        <!-- 2. Swarup Srishti -->
        <div class="tattva-card-shell tattva-card-2">
          <div class="card-top-row">
            <span class="step-badge">૦૨</span>
            <div class="card-header-titles">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">{data['c2_sub']}</span>
            </div>
          </div>
          <p class="card-body-text">{data['c2_body']}</p>
        </div>

        <!-- 3. Vyavahar Pushti -->
        <div class="tattva-card-shell tattva-card-3">
          <div class="card-top-row">
            <span class="step-badge">૦૩</span>
            <div class="card-header-titles">
              <span class="card-main-heading">વ્યવહાર-પૃષ્ટિ:</span>
              <span class="card-sub-kicker">{data['c3_sub']}</span>
            </div>
          </div>
          <ul class="card-bullet-list">
{c3_items_html}
          </ul>
        </div>

        <!-- 4. Marm Tushti -->
        <div class="tattva-card-shell tattva-card-4">
          <div class="card-top-row">
            <span class="step-badge">૦૪</span>
            <div class="card-header-titles">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">{data['c4_sub']}</span>
            </div>
          </div>
          <p class="card-body-text">{data['c4_body']}</p>
        </div>
      </div>

      <!-- Duo-Ribbon -->
      <div class="bottom-ribbon-shell">
        <div class="duo-ribbon-grid">
          <div class="duo-col">
            <span class="duo-label">• કાવ્યધારા</span>
            <p class="kavya-quote">
              {kavya_lines}
            </p>
          </div>
          <div class="duo-col duo-divider-col">
            <span class="duo-label">✦ સાધનાધારા</span>
            <p class="sadhana-statement">{data['sadhana_text']}</p>
          </div>
        </div>
      </div>

    </div>

    <!-- Running Footer: Left Page -->
    <footer class="running-footer">
      <span class="page-num">{data['page_even']}</span>
      <div class="footer-label">
        <span class="footer-book">નય-ચક્ષુ</span>
        <span class="footer-sep">|</span>
        <span class="footer-sub">નયનું જ્ઞાન, સંશયનું સમાધાન</span>
      </div>
    </footer>
  </section>


  <!-- ==================== RIGHT PAGE ({data['page_odd']}) ==================== -->
  <section class="page page-odd">
    <div class="page-canvas">

      <!-- Top Story Header Bar -->
      <div class="top-story-header">
        <span class="story-kicker">+ કથાધારા</span>
        <span class="story-title-main">નવલિકા: {data['story_title']}</span>
      </div>

      <!-- Split Story Hero: 1:1 Press Illustration + Pipasa -->
      <div class="story-hero-split">
        <div class="story-artwork-box">
          <img class="katha-art-img" src="{img_src}" alt="{data['story_title']}" loading="lazy">
        </div>
        <div class="story-pipasa-article">
          <span class="pipasa-badge">પિપાસા</span>
          <p>{data['pipasa_body']}</p>
        </div>
      </div>

      <!-- Paan Block -->
      <div class="story-paan-article">
        <span class="pipasa-badge">પાન</span>
        <p>{data['paan_body']}</p>
      </div>

      <!-- Vivekdhara Section -->
      <div class="section-divider-title">વિવેકધારા</div>
      <div class="vivek-container">
        <div class="vivek-card">
          <div class="vivek-card-title">એકાંત દર્શન (કદાગ્રહનો ગેરલાભ)</div>
          <p>{data['ekant_body']}</p>
        </div>
        <div class="vivek-card">
          <div class="vivek-card-title">અનેકાંત દર્શન (સમન્વયનું સૌંદર્ય)</div>
          <p>{data['anekant_body']}</p>
        </div>
      </div>

      <!-- Darshandhara Section (4 Rhyming Pillars) -->
      <div class="darshan-section">
        <div class="darshan-header">❖ દર્શનધારા</div>
        <div class="darshan-pillars-grid">
          <div class="darshan-pillar-item">
            <strong>૧. નય-ઉન્મેષ:</strong> {data['darshan_p1']}
          </div>
          <div class="darshan-pillar-item">
            <strong>૨. પ્રાચીન-વિશેષ:</strong> {data['darshan_p2']}
          </div>
          <div class="darshan-pillar-item">
            <strong>૩. અર્વાચીન-પ્રવેશ:</strong> {data['darshan_p3']}
          </div>
          <div class="darshan-pillar-item">
            <strong>૪. સમન્વય-અશેષ:</strong> {data['darshan_p4']}
          </div>
        </div>
      </div>

    </div>

    <!-- Running Footer: Right Page -->
    <footer class="running-footer">
      <div class="footer-label">
        <span class="footer-book">{data['khanda_pill']}</span>
        <span class="footer-sep">|</span>
        <span class="footer-sub">{data['title']}</span>
      </div>
      <span class="page-num">{data['page_odd']}</span>
    </footer>
  </section>

</div>
"""


def get_shared_css(fonts_rel: str = "../../pilot_chapter_001/assets/fonts") -> str:
    return f"""
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 400;
      src: url('{fonts_rel}/AnekGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 600;
      src: url('{fonts_rel}/AnekGujarati-SemiBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 700;
      src: url('{fonts_rel}/AnekGujarati-Bold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Anek Gujarati';
      font-style: normal;
      font-weight: 800;
      src: url('{fonts_rel}/AnekGujarati-ExtraBold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 400;
      src: url('{fonts_rel}/NotoSansGujarati-Regular.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'Noto Sans Gujarati';
      font-style: normal;
      font-weight: 700;
      src: url('{fonts_rel}/NotoSansGujarati-Bold.ttf') format('truetype');
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
      padding: 24px 16px;
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
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
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
      font-size: 19.0pt;
      line-height: 1.15;
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
      max-width: 50%;
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
      padding: 2.0pt;
      border-radius: 2pt;
      overflow: hidden;
    }}

    .katha-art-img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
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
"""


def build_all_html():
    t0 = time.time()
    base_dir = Path(".").resolve()
    sankshipt_dir = base_dir / "sankshipt"
    out_dir = sankshipt_dir / "output"
    img_map_file = base_dir / "Image" / "chapter-image-map.json"

    html_root = out_dir / "html"
    chapters_dir = html_root / "chapters"
    khandas_dir = html_root / "khandas"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    khandas_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("📖 BUILDING WHOLE BOOK HTML (225 CHAPTERS)")
    print("=" * 60)

    # 1. Load Image Map
    with open(img_map_file, 'r', encoding='utf-8') as f:
        img_records = json.load(f)
    img_by_src = {rec['source_file'].replace('\\', '/'): rec for rec in img_records}

    # 2. Collect and parse chapters
    md_files = sorted([f for f in out_dir.glob("khanda_*/*.md") if not f.name.startswith("000_")])
    print(f"Loaded {len(md_files)} markdown chapters.")

    parsed_list = []
    page_counter = 2  # Book starts on Page 2 (Left page of Chapter 1)
    khanda_groups: Dict[str, List[Dict[str, Any]]] = {}

    for idx, md_path in enumerate(md_files, 1):
        rel_src = md_path.relative_to(base_dir).as_posix()
        img_rec = img_by_src.get(rel_src, {})
        parsed = parse_chapter(md_path, img_rec, page_counter)
        parsed['chapter_num'] = idx
        parsed['khanda_folder'] = md_path.parent.name
        parsed_list.append(parsed)

        khanda_key = md_path.parent.name
        if khanda_key not in khanda_groups:
            khanda_groups[khanda_key] = []
        khanda_groups[khanda_key].append(parsed)

        # Advance page numbers: each chapter is 2 pages (even + odd)
        page_counter += 2

    # 3. Write individual chapter HTML files
    css_ch = get_shared_css(fonts_rel="../../../../pilot_chapter_001/assets/fonts")
    for ch in parsed_list:
        ch_spread_html = render_chapter_spread_html(ch, img_prefix="../../../../")
        ch_full_html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>{ch['title']} — નય-ચક્ષુ</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
{css_ch}
  </style>
</head>
<body>
{ch_spread_html}
</body>
</html>
"""
        ch_file = chapters_dir / f"{Path(ch['source_file']).stem}.html"
        ch_file.write_text(ch_full_html, encoding="utf-8")

    print(f"✓ Generated {len(parsed_list)} standalone chapter HTMLs in sankshipt/output/html/chapters/")

    # 4. Write Khanda-level HTML files
    css_khanda = get_shared_css(fonts_rel="../../../pilot_chapter_001/assets/fonts")
    for k_name, k_chapters in khanda_groups.items():
        k_spreads = "\n".join([render_chapter_spread_html(c, img_prefix="../../../") for c in k_chapters])
        k_html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>{k_name} — નય-ચક્ષુ (Khanda Volume)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
{css_khanda}
  </style>
</head>
<body>
{k_spreads}
</body>
</html>
"""
        k_file = khandas_dir / f"{k_name}.html"
        k_file.write_text(k_html, encoding="utf-8")

    print(f"✓ Generated {len(khanda_groups)} Khanda-level HTML volumes in sankshipt/output/html/khandas/")

    # 5. Write Complete Unified Whole Book HTML
    css_complete = get_shared_css(fonts_rel="../../pilot_chapter_001/assets/fonts")
    all_spreads = "\n".join([render_chapter_spread_html(c, img_prefix="../../") for c in parsed_list])
    complete_book_html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>નય-ચક્ષુ: ૨૦૩ નય મહાગ્રંથ (સંપૂર્ણ આવૃત્તિ)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
{css_complete}
  </style>
</head>
<body>
{all_spreads}
</body>
</html>
"""
    complete_book_file = html_root / "NayaPrakash_Complete_Book.html"
    complete_book_file.write_text(complete_book_html, encoding="utf-8")
    print(f"✓ Generated Complete Unified Book HTML: {complete_book_file} ({complete_book_file.stat().st_size:,} bytes)")

    # 6. Generate Interactive Book Reviewer Dashboard
    reviewer_html = generate_reviewer_dashboard(parsed_list)
    reviewer_file = html_root / "book_reviewer.html"
    reviewer_file.write_text(reviewer_html, encoding="utf-8")
    print(f"✓ Generated Interactive Book Reviewer: {reviewer_file}")

    t_end = time.time() - t0
    print("\n" + "=" * 60)
    print(f"🎉 WHOLE BOOK HTML SUITE GENERATED IN {t_end:.2f} SECONDS!")
    print("=" * 60)


def generate_reviewer_dashboard(chapters: List[Dict[str, Any]]) -> str:
    """Generates a modern, interactive HTML reviewer dashboard to browse all 225 chapters."""
    ch_json = json.dumps([{
        "id": c['chapter_num'],
        "key": c['image_key'],
        "title": c['title'],
        "khanda": c['khanda_folder'],
        "khanda_pill": c['khanda_pill'],
        "story": c['story_title'],
        "file": f"chapters/{Path(c['source_file']).stem}.html",
        "page_even": c['page_even'],
        "page_odd": c['page_odd']
    } for c in chapters], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="utf-8">
  <title>નય-ચક્ષુ: પ્રકરણ સમીક્ષા ડેશબોર્ડ (Whole Book HTML Reviewer)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Anek+Gujarati:wght@400;600;700;800&family=Noto+Sans+Gujarati:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Noto Sans Gujarati', sans-serif;
      display: flex;
      height: 100vh;
      overflow: hidden;
      background: #1e1e24;
      color: #e0e0e0;
    }}
    /* Sidebar */
    .sidebar {{
      width: 380px;
      background: #141419;
      border-right: 1px solid #2d2d38;
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .sidebar-header {{
      padding: 16px;
      border-bottom: 1px solid #2d2d38;
      background: #0f0f13;
    }}
    .sidebar-header h1 {{
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .sidebar-header .sub {{
      font-size: 11px;
      color: #9090a0;
      margin-top: 4px;
    }}
    .search-box {{
      padding: 10px 16px;
      border-bottom: 1px solid #2d2d38;
      background: #181820;
    }}
    .search-box input {{
      width: 100%;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid #333344;
      background: #0d0d12;
      color: #ffffff;
      font-family: 'Noto Sans Gujarati', sans-serif;
      font-size: 13px;
      outline: none;
    }}
    .search-box input:focus {{
      border-color: #6366f1;
    }}
    .quick-links {{
      display: flex;
      gap: 6px;
      padding: 8px 16px;
      border-bottom: 1px solid #2d2d38;
      overflow-x: auto;
      background: #141419;
    }}
    .khanda-btn {{
      padding: 4px 8px;
      border-radius: 4px;
      border: 1px solid #333344;
      background: #1e1e26;
      color: #b0b0c0;
      font-size: 11px;
      font-family: 'Anek Gujarati', sans-serif;
      cursor: pointer;
      white-space: nowrap;
    }}
    .khanda-btn:hover, .khanda-btn.active {{
      background: #6366f1;
      color: #ffffff;
      border-color: #6366f1;
    }}
    .chapter-list {{
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }}
    .ch-card {{
      padding: 10px 12px;
      border-radius: 6px;
      border: 1px solid transparent;
      margin-bottom: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
      background: #191922;
    }}
    .ch-card:hover {{
      background: #232330;
      border-color: #3b3b4d;
    }}
    .ch-card.active {{
      background: #2b2b3d;
      border-color: #6366f1;
    }}
    .ch-num {{
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 10px;
      font-weight: 700;
      color: #818cf8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .ch-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: #f1f1f5;
      margin-top: 2px;
    }}
    .ch-meta {{
      font-size: 11px;
      color: #8e8ea0;
      margin-top: 4px;
      display: flex;
      justify-content: space-between;
    }}
    /* Main View Area */
    .viewer {{
      flex: 1;
      display: flex;
      flex-direction: column;
      background: #2b2c34;
    }}
    .viewer-topbar {{
      height: 48px;
      padding: 0 20px;
      background: #141419;
      border-bottom: 1px solid #2d2d38;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .viewer-title {{
      font-family: 'Anek Gujarati', sans-serif;
      font-size: 14px;
      font-weight: 700;
      color: #ffffff;
    }}
    .viewer-actions {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .viewer-actions a, .viewer-actions button {{
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid #444455;
      background: #20202a;
      color: #e0e0e0;
      text-decoration: none;
      cursor: pointer;
    }}
    .viewer-actions a:hover, .viewer-actions button:hover {{
      background: #6366f1;
      color: #ffffff;
      border-color: #6366f1;
    }}
    .preview-frame {{
      flex: 1;
      border: none;
      width: 100%;
      height: 100%;
      background: #50525d;
    }}
  </style>
</head>
<body>

  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>◈ નય-ચક્ષુ: ૨૦૩ નય મહાગ્રંથ</h1>
      <div class="sub">સંપૂર્ણ ૨૨૫ પ્રકરણોનું લાઈવ HTML રિવ્યૂ ડેશબોર્ડ (6.5" × 9.5")</div>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="પ્રકરણ અથવા નય શોધો..." oninput="filterChapters()">
    </div>
    <div class="quick-links">
      <button class="khanda-btn active" onclick="filterKhanda('all')">બધા (૨૨૫)</button>
      <button class="khanda-btn" onclick="filterKhanda('khanda_1_naigam')">ખંડ ૧</button>
      <button class="khanda-btn" onclick="filterKhanda('khanda_2_sangrah')">ખંડ ૨</button>
      <button class="khanda-btn" onclick="filterKhanda('khanda_3_vyavahar')">ખંડ ૩</button>
      <button class="khanda-btn" onclick="filterKhanda('khanda_4_rjusutra')">ખંડ ૪</button>
      <button class="khanda-btn" onclick="filterKhanda('khanda_5_shabda')">ખંડ ૫</button>
      <button class="khanda-btn" onclick="filterKhanda('khanda_6_samabhirudh')">ખંડ ૬</button>
      <button class="khanda-btn" onclick="filterKhanda('khanda_7_evambhut')">ખંડ ૭</button>
    </div>
    <div class="chapter-list" id="chapterList"></div>
  </aside>

  <main class="viewer">
    <header class="viewer-topbar">
      <div class="viewer-title" id="currentTitle">૧. ભૂતનૈગમ નય</div>
      <div class="viewer-actions">
        <a id="openNewTab" href="chapters/chapter_001_bhuta_naigam_naya_gu.html" target="_blank">નવી વિન્ડોમાં ખોલો ↗</a>
        <a href="NayaPrakash_Complete_Book.html" target="_blank" style="background:#4338ca; border-color:#6366f1;">સંપૂર્ણ પુસ્તક HTML 📖</a>
      </div>
    </header>
    <iframe class="preview-frame" id="previewFrame" src="chapters/chapter_001_bhuta_naigam_naya_gu.html"></iframe>
  </main>

  <script>
    const chapters = {ch_json};
    let currentKhanda = 'all';

    function renderList() {{
      const query = document.getElementById('searchInput').value.toLowerCase();
      const listEl = document.getElementById('chapterList');
      listEl.innerHTML = '';

      const filtered = chapters.filter(c => {{
        const matchKhanda = (currentKhanda === 'all') || (c.khanda === currentKhanda);
        const matchQuery = !query || c.title.toLowerCase().includes(query) || c.story.toLowerCase().includes(query) || c.khanda_pill.toLowerCase().includes(query);
        return matchKhanda && matchQuery;
      }});

      filtered.forEach((c, idx) => {{
        const card = document.createElement('div');
        card.className = 'ch-card' + (idx === 0 && !query && currentKhanda === 'all' ? ' active' : '');
        card.onclick = () => selectChapter(c, card);
        card.innerHTML = `
          <div class="ch-num">${{c.khanda_pill}} • પ્રકરણ ${{c.id}}</div>
          <div class="ch-title">${{c.title}}</div>
          <div class="ch-meta">
            <span>📖 પાના ${{c.page_even}}-${{c.page_odd}}</span>
            <span>🖼️ ${{c.story}}</span>
          </div>
        `;
        listEl.appendChild(card);
      }});
    }}

    function selectChapter(c, cardEl) {{
      document.querySelectorAll('.ch-card').forEach(el => el.classList.remove('active'));
      if (cardEl) cardEl.classList.add('active');
      document.getElementById('currentTitle').innerText = `${{c.title}} (પાના ${{c.page_even}}-${{c.page_odd}})`;
      document.getElementById('previewFrame').src = c.file;
      document.getElementById('openNewTab').href = c.file;
    }}

    function filterChapters() {{
      renderList();
    }}

    function filterKhanda(khanda) {{
      currentKhanda = khanda;
      document.querySelectorAll('.khanda-btn').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
      renderList();
    }}

    // Init
    renderList();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    build_all_html()
