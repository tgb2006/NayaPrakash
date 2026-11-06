from pathlib import Path
import subprocess, re, json

pilot_dir = Path('sankshipt/pilot_long_title_ch070')
raw_html = (pilot_dir / 'chapter_070.html').read_text(encoding='utf-8')
p2_html = raw_html.replace('id="page-3"', 'id="page-3" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')

script = """
<script>
window.addEventListener('load', () => {
    function getBox(el) {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {top: Math.round(r.top), bottom: Math.round(r.bottom), height: Math.round(r.height), left: Math.round(r.left), right: Math.round(r.right)};
    }
    const report = {
        page2: getBox(document.getElementById('page-2')),
        page_canvas: getBox(document.querySelector('.page-even .page-canvas')),
        masthead: getBox(document.querySelector('.chapter-masthead')),
        ribbon: getBox(document.querySelector('.section-ribbon')),
        grid: getBox(document.querySelector('.tattva-infographic-grid')),
        c1: getBox(document.querySelector('.tattva-card-1')),
        c2: getBox(document.querySelector('.tattva-card-2')),
        c3: getBox(document.querySelector('.tattva-card-3')),
        c4: getBox(document.querySelector('.tattva-card-4')),
        duo: getBox(document.querySelector('.bottom-ribbon-shell')),
        footer: getBox(document.querySelector('.page-even .running-footer'))
    };
    console.error('GEOM_JSON:' + JSON.stringify(report));
});
</script>
"""

test_html = p2_html.replace('</body>', script + '</body>')
test_file = pilot_dir / 'test_geom.html'
test_file.write_text(test_html, encoding='utf-8')

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
res = subprocess.run([
    chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--window-size=624,912', '--dump-dom', '--enable-logging=stderr',
    f'file:///{test_file.resolve().as_posix()}'
], capture_output=True, text=True, timeout=10)

test_file.unlink(missing_ok=True)

match = re.search(r'GEOM_JSON:(\{.+\})', res.stderr)
if match:
    data = json.loads(match.group(1))
    print(json.dumps(data, indent=2))
else:
    print('No match, stderr length:', len(res.stderr))
    print(res.stderr[:500])
