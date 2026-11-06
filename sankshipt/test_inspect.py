from pathlib import Path
import re

text = Path('sankshipt/pilot_long_title_ch070/update_all_fonts_to_11pt.py').read_text(encoding='utf-8')
m = re.search(r'html_content\s*=\s*r?["\']{3}([\s\S]*?)["\']{3}', text)
if m:
    content = m.group(1)
    print("Found html_content length:", len(content))
    pos = content.find('tattva-infographic-grid')
    print(content[pos-100:pos+600])
else:
    print("Not found")
