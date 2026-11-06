import re
from pathlib import Path

file_path = Path('sankshipt/pilot_chapter_001/chapter_001.html')
content = file_path.read_text(encoding='utf-8')

# Tune Page 3 spacing
content = content.replace('margin-bottom: 4pt;\n    }\n\n    .story-illustration-frame', 'margin-bottom: 2.5pt;\n    }\n\n    .story-illustration-frame')
content = content.replace('padding: 4.5pt 8pt;\n      margin-bottom: 4pt;', 'padding: 3.5pt 7pt;\n      margin-bottom: 2.5pt;')
content = content.replace('padding-top: 3.5pt;\n      margin-bottom: 4pt;', 'padding-top: 2.5pt;\n      margin-bottom: 2.5pt;')
content = content.replace('border-top: 1.1pt solid #111111;\n      padding-top: 3.5pt;\n      margin-top: 2pt;', 'border-top: 1.1pt solid #111111;\n      padding-top: 2.5pt;\n      margin-top: 1.5pt;')

file_path.write_text(content, encoding='utf-8')
print("Page 3 spacing tuned successfully!")
