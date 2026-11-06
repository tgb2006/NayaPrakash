from pathlib import Path
import subprocess, re, json

pilot_dir = Path('sankshipt/pilot_chapter_001').resolve()
html_path = pilot_dir / 'chapter_001.html'
raw = html_path.read_text(encoding='utf-8')
p3_html = raw.replace('id="page-2"', 'id="page-2" style="display:none;"').replace('class="spread-container"', 'class="spread-container" style="padding:0; margin:0;"')

script = """
<script>
window.addEventListener('load', () => {
    function getBox(sel) {
        const el = document.querySelector(sel);
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {top: Math.round(r.top), bottom: Math.round(r.bottom), height: Math.round(r.height)};
    }
    const report = {
        page3: getBox('#page-3'),
        canvas: getBox('#page-3 .page-canvas'),
        story_sec: getBox('#p-001-story-sec'),
        split: getBox('.story-hero-split'),
        paan: getBox('#p-001-paan'),
        vivek_title: getBox('.section-divider-title'),
        vivek: getBox('.vivek-container'),
        darshan: getBox('#p-001-darshan-sec'),
        footer: getBox('#page-3 .running-footer')
    };
    console.error('P3_JSON:' + JSON.stringify(report));
});
</script>
"""

test_file = pilot_dir / 'test_p3.html'
test_file.write_text(p3_html.replace('</body>', script + '</body>'), encoding='utf-8')

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
res = subprocess.run([
    chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--window-size=624,912', '--dump-dom', '--enable-logging=stderr',
    f'file:///{test_file.as_posix()}'
], capture_output=True, text=True, timeout=10)

test_file.unlink(missing_ok=True)

match = re.search(r'P3_JSON:(\{.*\})', res.stderr)
if match:
    print(json.dumps(json.loads(match.group(1)), indent=2))
