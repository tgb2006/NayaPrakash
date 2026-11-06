import subprocess
from pathlib import Path
from PIL import Image

pilot_dir = Path('sankshipt/pilot_long_title_ch070').resolve()
html_path = pilot_dir / 'chapter_070.html'
pdf_path = pilot_dir / 'chapter_070.pdf'
spread_img = pilot_dir / 'chapter_070_spread_preview.png'
p2_img = pilot_dir / 'page_002_left_preview.png'
p3_img = pilot_dir / 'page_003_right_preview.png'
tattva_zoom = pilot_dir / 'tattvadhara_symmetrical_zoom.png'
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# PDF
res_pdf = subprocess.run([
    chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_path.as_posix()}', f'file:///{html_path.as_posix()}'
], capture_output=True, text=True)

# Spread
res_sp = subprocess.run([
    chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', '--window-size=1360,980',
    f'--screenshot={spread_img.as_posix()}', f'file:///{html_path.as_posix()}'
], capture_output=True, text=True)

# P2
raw_html = html_path.read_text(encoding='utf-8')
p2_html = raw_html.replace('id="page-3"', 'id="page-3" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
p2_temp = pilot_dir / 'p2_temp.html'
p2_temp.write_text(p2_html, encoding='utf-8')
res_p2 = subprocess.run([
    chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', '--window-size=624,912',
    f'--screenshot={p2_img.as_posix()}', f'file:///{p2_temp.as_posix()}'
], capture_output=True, text=True)
p2_temp.unlink(missing_ok=True)

# P3
p3_html = raw_html.replace('id="page-2"', 'id="page-2" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')
p3_temp = pilot_dir / 'p3_temp.html'
p3_temp.write_text(p3_html, encoding='utf-8')
res_p3 = subprocess.run([
    chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', '--window-size=624,912',
    f'--screenshot={p3_img.as_posix()}', f'file:///{p3_temp.as_posix()}'
], capture_output=True, text=True)
p3_temp.unlink(missing_ok=True)

# Crop Tattvadhara + Ribbon
p2_im = Image.open(p2_img)
w, h = p2_im.size
tatt_crop = p2_im.crop((int(w * 0.05), int(h * 0.22), int(w * 0.95), int(h * 0.94)))
tatt_crop.save(tattva_zoom)
print('Re-rendered successfully with absolute paths!')
