const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

async function main() {
  const out = path.resolve(process.argv[2]);
  const file = path.join(out, 'naya_chakshu_book.html');
  const browser = await chromium.launch({executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try {
    const page = await browser.newPage({viewport: {width: 950, height: 950}});
    await page.emulateMedia({media: 'print'});
    await page.goto(pathToFileURL(file).href);
    const result = await page.evaluate(async () => {
      await document.fonts.ready;
      const results = [];
      for (const art of document.querySelectorAll('.chapter-page .example-art')) {
        const page = art.closest('.page');
        const existingGroup = art.closest('.paired-tattva');
        const example = (existingGroup || page).querySelector('[data-component="tattva-3"]');
        const conclusion = example?.nextElementSibling;
        if (!example || conclusion?.dataset.component !== 'tattva-4') throw Error('Tattva 03 and 04 must be consecutive on page ' + page.dataset.physicalPage);
        await art.querySelector('img').decode();
        const group = existingGroup || document.createElement('div');
        const copy = existingGroup?.firstElementChild || document.createElement('div');
        if (!existingGroup) {
          group.className = 'paired-tattva';
          Object.assign(group.style, {display: 'grid', columnGap: '4mm', alignItems: 'center', borderTop: '.6pt solid #cecece'});
          copy.style.minWidth = '0';
          example.before(group);
          copy.append(example, conclusion);
          Object.assign(example.style, {borderTop: '0', paddingTop: '1.8mm'});
          conclusion.style.marginTop = '2.4mm';
          Object.assign(art.style, {float: 'none', margin: '0'});
          group.append(copy, art);
        }
        const box = node => node.getBoundingClientRect();
        const closing = page.querySelector('.closing');
        const footer = page.querySelector('.running-footer');
        let result;
        for (const size of [42, 39, 36, 33, 30]) {
          group.style.gridTemplateColumns = 'minmax(0, 1fr) ' + size + 'mm';
          art.style.width = art.style.height = size + 'mm';
          const rightEdgeDifference = Math.abs(box(example).right - box(conclusion).right);
          const artGap = box(art).left - box(copy).right;
          const closingGap = box(closing).top - box(group).bottom;
          const footerGap = box(footer).top - box(closing).bottom;
          const fits = rightEdgeDifference <= .25 && artGap >= 12 && closingGap >= 3 && footerGap >= 7
            && [example, conclusion].every(block => block.scrollWidth <= block.clientWidth + 1);
          result = {page: Number(page.dataset.physicalPage), size, rightEdgeDifference, artGap, closingGap, footerGap, fits};
          if (fits) break;
        }
        results.push(result);
      }
      return results;
    });
    console.log(JSON.stringify(result));
    if (process.argv.includes('--measure-only')) return;
    if (!result.length || result.some(page => !page.fits)) throw Error('Paired Tattva alignment or clearance failed');
    fs.writeFileSync(file, '<!doctype html>\n' + await page.evaluate(() => document.documentElement.outerHTML));
    const proof = process.argv.find(arg => arg.startsWith('--proof='));
    if (proof) for (const entry of result) await page.locator('#page-' + entry.page).screenshot({path: path.join(proof.slice('--proof='.length), 'r09-paired-tattva-' + entry.page + '.png')});
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
