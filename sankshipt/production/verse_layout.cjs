const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

async function main() {
  const out = path.resolve(process.argv[2]);
  const file = path.join(out, 'naya_chakshu_book.html');
  const browser = await chromium.launch({executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1100}});
    await page.emulateMedia({media: 'print'});
    await page.goto(pathToFileURL(file).href);
    const report = await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(image => image.decode()));
      const pageOf = element => element.closest('.page');
      const pageNumber = element => Number(pageOf(element).dataset.physicalPage);
      const fitsPage = element => {
        const page = pageOf(element);
        const end = page.querySelector('.page-content').lastElementChild.getBoundingClientRect().bottom;
        const footer = page.querySelector('.running-footer').getBoundingClientRect().top;
        return end <= footer - 7;
      };
      const bounds = element => {
        const range = document.createRange();
        range.selectNodeContents(element);
        return [...range.getClientRects()].filter(rect => rect.width > 1);
      };
      const lineCount = element => new Set(bounds(element).map(rect => Math.round(rect.top))).size;
      const checked = {
        poems: document.querySelectorAll('.poem').length,
        authoredVerseLines: document.querySelectorAll('.generic-verse .verse-line').length,
        chapterSutras: document.querySelectorAll('.sutra-text').length,
        khandaSutraLines: document.querySelectorAll('.khanda-sutra-line').length
      };
      const changes = [];
      const issues = [];
      const sutraSpans = [...document.querySelectorAll('.generic-block[data-kind="quote"] .generic-inline-code .generic-devanagari')];
      checked.quotedSutraRuns = sutraSpans.length;
      for (const run of sutraSpans) {
        if (!/[\u0904-\u0963]/u.test(run.textContent)) continue;
        const quote = run.closest('.generic-quote');
        quote.style.textAlign = 'start';
        const groups = [...run.textContent.matchAll(/[^।॥]*[।॥]+\s*|[^।॥]+$/gu)].map(match => match[0]);
        if (groups.length < 2 || run.querySelector('br')) continue;
        const number = pageNumber(run);
        // On the four-clause taxonomy sutra, keep the short premise and first category together.
        const lines = groups.length === 4 ? [groups[0] + groups[1], ...groups.slice(2)] : groups;
        run.replaceChildren(...lines.flatMap((line, index) => index ? [document.createElement('br'), line] : [line]));
        if (!fitsPage(run)) {
          const outer = run.closest('.generic-block[data-kind="quote"]');
          Object.assign(outer.style, {padding: '0', border: '0', background: 'none'});
          quote.style.marginBottom = '0';
        }
        if (!fitsPage(run)) {
          const page = pageOf(run);
          const content = page.querySelector('.page-content');
          const footer = page.querySelector('.running-footer');
          issues.push({page: number, type: 'sutra_page_fit', gap: footer.getBoundingClientRect().top - content.lastElementChild.getBoundingClientRect().bottom});
        }
        changes.push({page: number, type: 'sutra_breaks', lines: lines.length});
      }
      for (const poem of document.querySelectorAll('.poem')) {
        const expected = poem.querySelectorAll('br').length + 1;
        if (lineCount(poem) <= expected) continue;
        const closing = poem.closest('.closing');
        const gap = parseFloat(getComputedStyle(closing).columnGap);
        const available = closing.clientWidth - gap;
        poem.style.whiteSpace = 'nowrap';
        const width = Math.ceil(Math.max(...bounds(poem).map(rect => rect.width))) + 1;
        poem.style.removeProperty('white-space');
        const previous = closing.style.gridTemplateColumns;
        if (width <= available * .62) {
          closing.style.gridTemplateColumns = (width * 25.4 / 96) + 'mm minmax(0, 1fr)';
          if (lineCount(poem) === expected && fitsPage(poem)) {
            changes.push({page: pageNumber(poem), type: 'poem_column', lines: expected});
            continue;
          }
          closing.style.gridTemplateColumns = previous;
        }
        issues.push({page: pageNumber(poem), type: 'poem_wrap', width, available});
      }
      for (const line of document.querySelectorAll('.generic-verse .verse-line,.khanda-sutra-line')) {
        if (lineCount(line) > 1) issues.push({page: pageNumber(line), type: 'authored_line_wrap'});
      }
      for (const sutra of document.querySelectorAll('.sutra-text:not(.author-definition)')) {
        if (lineCount(sutra) <= 1) continue;
        const box = sutra.closest('.sutra');
        Object.assign(box.style, {flexDirection: 'column', alignItems: 'stretch', gap: '.6mm'});
        if (lineCount(sutra) > 1 || !fitsPage(sutra)) issues.push({page: pageNumber(sutra), type: 'chapter_sutra_fit'});
        else changes.push({page: pageNumber(sutra), type: 'sutra_full_width', lines: 1});
      }
      return {checked, changes, issues};
    });
    console.log(JSON.stringify(report));
    if (process.argv.includes('--measure-only')) return;
    if (report.issues.length) throw Error('Verse layout checks failed');
    const html = await page.evaluate(() => document.documentElement.outerHTML);
    fs.writeFileSync(file, '<!doctype html>\n' + html);
    fs.writeFileSync(path.join(out, 'verse-layout-audit.json'), JSON.stringify(report, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
