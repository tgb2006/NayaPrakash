from pathlib import Path
import re

# 1. Update Chapter 070
p70 = Path('sankshipt/pilot_long_title_ch070/chapter_070.html')
content70 = p70.read_text(encoding='utf-8')

def norm(t): return t.replace('\r\n', '\n')
content70 = norm(content70)

# Clean CSS
content70 = re.sub(
    r'\.card-top-row\.header-left\s*\{[^}]*\}',
    '',
    content70
)
content70 = re.sub(
    r'\.card-top-row\.header-right\s*\{[^}]*\}',
    '',
    content70
)
content70 = re.sub(
    r'\.card-header-titles\.text-right\s*\{[^}]*\}',
    '',
    content70
)

# Update card top row CSS for professional editorial typography
old_top_row_css = """.card-top-row {
      display: flex;
      align-items: flex-start;
      gap: 5pt;
      margin-bottom: 3.5pt;
      padding-bottom: 2pt;
      border-bottom: 0.6pt solid #eaeaea;
    }"""

new_top_row_css = """.card-top-row {
      display: flex;
      align-items: flex-start;
      gap: 5.5pt;
      margin-bottom: 3.5pt;
      padding-bottom: 2.5pt;
      border-bottom: 0.6pt solid #e6e8eb;
    }"""

if old_top_row_css in content70:
    content70 = content70.replace(old_top_row_css, new_top_row_css)

# Card 01
content70 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?<span class="step-badge">૦૧</span>[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૧</span>
            <div class="card-header-titles">
              <span class="card-main-heading">રૂપક-દ્રષ્ટિ:</span>
              <span class="card-sub-kicker">નદીના પ્રવાહમાં ક્ષણે ક્ષણે ફૂટતા પરપોટા</span>
            </div>
          </div>""",
    content70
)

# Card 02
content70 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?સ્વરૂપ-સૃષ્ટિ:[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૨</span>
            <div class="card-header-titles">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">ક્ષણભંગુરતાનો વાસ્તવિક બોધ</span>
            </div>
          </div>""",
    content70
)

# Card 03
content70 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?<span class="step-badge">૦૩</span>[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૩</span>
            <div class="card-header-titles">
              <span class="card-main-heading">વ્યવહાર-પૃષ્ટિ:</span>
              <span class="card-sub-kicker">બાર ભાવનાઓ અને અનિત્યતા ચિંતન</span>
            </div>
          </div>""",
    content70
)

# Card 04
content70 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?મર્મ-તુષ્ટિ:[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૪</span>
            <div class="card-header-titles">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">મોહની ઊંઘમાંથી આત્મજાગરણ</span>
            </div>
          </div>""",
    content70
)

p70.write_text(content70, encoding='utf-8')
print("Chapter 070 updated to uniform left-aligned editorial layout!")


# 2. Update Chapter 001
p01 = Path('sankshipt/pilot_chapter_001/chapter_001.html')
content01 = p01.read_text(encoding='utf-8')
content01 = norm(content01)

# Clean CSS
content01 = re.sub(
    r'\.card-top-row\.header-left\s*\{[^}]*\}',
    '',
    content01
)
content01 = re.sub(
    r'\.card-top-row\.header-right\s*\{[^}]*\}',
    '',
    content01
)
content01 = re.sub(
    r'\.card-header-titles\.text-right\s*\{[^}]*\}',
    '',
    content01
)

# Card 01
content01 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?<span class="step-badge">૦૧</span>[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૧</span>
            <div class="card-header-titles">
              <span class="card-main-heading">રૂપક-દ્રષ્ટિ:</span>
              <span class="card-sub-kicker">ઓલવાયેલા તારકનું જીવંત કિરણ</span>
            </div>
          </div>""",
    content01
)

# Card 02
content01 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?સ્વરૂપ-સૃષ્ટિ:[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૨</span>
            <div class="card-header-titles">
              <span class="card-main-heading">સ્વરૂપ-સૃષ્ટિ:</span>
              <span class="card-sub-kicker">કાળના પડદા પાર જોતી આંખ</span>
            </div>
          </div>""",
    content01
)

# Card 03
content01 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?<span class="step-badge">૦૩</span>[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૩</span>
            <div class="card-header-titles">
              <span class="card-main-heading">વ્યવહાર-પૃષ્ટિ:</span>
              <span class="card-sub-kicker">જીવન-વ્યવહારના જીવંત દૃષ્ટાંતો</span>
            </div>
          </div>""",
    content01
)

# Card 04
content01 = re.sub(
    r'<div class="card-top-row[^"]*">[\s\S]*?મર્મ-તુષ્ટિ:[\s\S]*?</div>\s*</div>',
    """<div class="card-top-row">
            <span class="step-badge">૦૪</span>
            <div class="card-header-titles">
              <span class="card-main-heading">મર્મ-તુષ્ટિ:</span>
              <span class="card-sub-kicker">ભીતરી સત્ય અને ભ્રમણા-નિવારણ</span>
            </div>
          </div>""",
    content01
)

p01.write_text(content01, encoding='utf-8')
print("Chapter 001 updated to uniform left-aligned editorial layout!")
