const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const artDirectory = path.resolve(__dirname, '../../Image/tattva-panoramas');
const captions = {
  K01_C001: 'જૂની શાળાની પાટી અને ખડી',
  K01_C002: 'ખરબચડા પથ્થર સાથે છીણી અને હથોડી',
  K01_C005: 'નાનો અંકુર અને ભાવિ વૃક્ષનો પડછાયો',
  K01_C006: 'સાળ પર અડધું વણાયેલું વસ્ત્ર',
  K02_C001: 'એક જ માટીમાંથી બનેલાં ઘડો, વાટકી અને ઈંટ',
  K02_C004: 'એક જ શિખર તરફ જતા બે માર્ગ',
  K03_C026: 'વાદળની પાછળ તેજસ્વી સૂર્ય',
  K03_C027: 'દૂધ અને ઘીની બે વાટકી',
  K03_C028: 'શાંત જળ પર પૂર્ણ ખીલેલું કમળ',
  K03_C029: 'વિસ્તૃત મહાસાગરમાં એક તરંગ',
  K06_C010: 'તૂટેલું માટીનું પાત્ર અને તેના ટુકડા'
};

async function main() {
  const out = path.resolve(process.argv[2]);
  const file = path.join(out, 'naya_chakshu_book.html');
  const browser = await chromium.launch({executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try {
    const page = await browser.newPage({viewport: {width: 950, height: 950}});
    await page.emulateMedia({media: 'print'});
    await page.goto(pathToFileURL(file).href);
    const measureOnly = process.argv.includes('--measure-only');
    const relativeDir = 'assets/tattva-panoramas';
    if (!measureOnly) {
      for (const key of Object.keys(captions)) {
        if (!fs.existsSync(path.join(artDirectory, key + '.png'))) throw Error('Missing panorama ' + key);
      }
      fs.mkdirSync(path.join(out, relativeDir), {recursive: true});
      for (const key of Object.keys(captions)) fs.copyFileSync(path.join(artDirectory, key + '.png'), path.join(out, relativeDir, key + '.png'));
    }
    const report = await page.evaluate(async ({captions, relativeDir, measureOnly}) => {
      await document.fonts.ready;
      const chapters = [...document.querySelectorAll('.chapter-page:has(.paired-tattva)')];
      if (chapters.length !== Object.keys(captions).length) throw Error('Panorama mapping does not match the illustrated pages');
      const results = [];
      for (const page of chapters) {
        const key = page.dataset.key;
        if (!captions[key]) throw Error('Unmapped Tattva panorama: ' + key);
        const group = page.querySelector('.paired-tattva');
        const figure = group.querySelector('.example-art');
        const image = figure.querySelector('img');
        const example = group.querySelector('[data-component="tattva-3"]');
        const conclusion = group.querySelector('[data-component="tattva-4"]');
        const closing = page.querySelector('.closing');
        const footer = page.querySelector('.running-footer');
        const box = node => node.getBoundingClientRect();
        group.style.display = 'block';
        figure.remove();
        const width = box(group).width;
        const height = box(closing).top - box(group).bottom - 30;
        if (height < 60) throw Error('Insufficient space for panorama: ' + key);
        const row = {key, page: +page.dataset.physicalPage, widthMM: width * 25.4 / 96, heightMM: height * 25.4 / 96, ratio: width / height};
        if (!measureOnly) {
          image.src = relativeDir + '/' + key + '.png';
          image.alt = captions[key];
          await image.decode();
          image.width = image.naturalWidth;
          image.height = image.naturalHeight;
          const printWidth = Math.min(width, image.naturalWidth * 96 / 300);
          const printHeight = Math.min(height, image.naturalHeight * 96 / 300);
          figure.classList.add('example-panorama');
          Object.assign(figure.style, {float: 'none', width: (printWidth * 25.4 / 96) + 'mm', height: (printHeight * 25.4 / 96) + 'mm', margin: '3.5mm auto 0'});
          Object.assign(image.style, {objectFit: 'cover', filter: 'grayscale(1)'});
          group.append(figure);
          const artGap = box(closing).top - box(figure).bottom;
          const footerGap = box(footer).top - box(closing).bottom;
          if (Math.abs(box(example).right - box(conclusion).right) > .25 || artGap < 12 || footerGap < 7 || group.scrollWidth > group.clientWidth + 1) {
            throw Error('Panorama geometry failed on page ' + row.page + ': ' + JSON.stringify({artGap, footerGap}));
          }
          Object.assign(row, {file: key + '.png', placedWidthMM: printWidth * 25.4 / 96, placedHeightMM: printHeight * 25.4 / 96,
            pixels: [image.naturalWidth, image.naturalHeight], dpi: Math.round(96 * Math.min(image.naturalWidth / printWidth, image.naturalHeight / printHeight)), artGap, footerGap});
        }
        results.push(row);
      }
      return results;
    }, {captions, relativeDir, measureOnly});
    console.log(JSON.stringify(report));
    if (measureOnly) return;
    const proof = process.argv.find(arg => arg.startsWith('--proof='));
    if (proof) {
      const dir = proof.slice('--proof='.length);
      for (const row of report) {
        const figure = page.locator('#page-' + row.page + ' .example-panorama');
        await figure.screenshot({path: path.join(dir, 'r09-tattva-panorama-crop-' + row.page + '.png')});
      }
      await page.locator('#page-74').screenshot({path: path.join(dir, 'r09-tattva-panorama-74.png')});
    }
    fs.writeFileSync(file, '<!doctype html>\n' + await page.evaluate(() => document.documentElement.outerHTML));
    fs.writeFileSync(path.join(out, 'tattva-panorama-audit.json'), JSON.stringify(report, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
