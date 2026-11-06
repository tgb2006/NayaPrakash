import subprocess
from pathlib import Path
from PIL import Image

pilot_dir = Path('sankshipt/pilot_long_title_ch070')
html_path = pilot_dir / 'chapter_070.html'
p2_img = pilot_dir / 'page_002_left_preview.png'
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# render p2
raw_html = html_path.read_text(encoding='utf-8')
p2_html = raw_html.replace('id="page-3"', 'id="page-3" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
p2_temp = pilot_dir / 'p2_temp.html'
p2_temp.write_text(p2_html, encoding='utf-8')
subprocess.run([
    chrome,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=624,912',
    f'--screenshot={p2_img}',
    f'file:///{p2_temp.as_posix()}'
], capture_output=True)
p2_temp.unlink(missing_ok=True)

# crop card 4
im = Image.open(p2_img)
w, h = im.size
c4 = im.crop((int(w * 0.5), int(h * 0.48), int(w * 0.95), int(h * 0.82)))
c4.save(pilot_dir / 'card4_fixed_zoom.png')

# crop both bottom cards together (Card 3 and Card 4)
both_cards = im.crop((int(w * 0.05), int(h * 0.48), int(w * 0.95), int(h * 0.82)))
both_cards.save(pilot_dir / 'cards_3_4_comparison.png')
print('Rendered and cropped fixed card 4!')
