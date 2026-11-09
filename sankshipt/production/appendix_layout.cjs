const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const columnWidths = {
  'પરિશિષ્ટ|શીર્ષક': [12, 28, 35, 25],
  'ભારતીય દર્શન|કેન્દ્રીય સિદ્ધાંત / માન્યતા': [17, 22, 14, 21, 26],
  'પાશ્ચાત્ય ચિંતક|દાર્શનિક વાદ / સિદ્ધાંત': [19, 27, 17, 37],
  'ક્રમ|નયનું નામ': [6, 15, 11, 21, 21, 26],
  'ક્રમ|શાસ્ત્રીય પરિભાષા': [7, 19, 36, 38],
  'ખંડ ક્રમ|ખંડનું નામ': [8, 13, 15, 13, 12, 12, 27],
  'જીવનની પરિસ્થિતિ / સંઘર્ષ|પ્રચલિત એકાંત ભૂલ (હઠાગ્રહ)': [19, 22, 14, 30, 15],
  'પ્રતીક / રૂપક શ્રેણી|તાત્ત્વિક રહસ્ય અને નય-સંકેત': [23, 32, 45],
  'ક્રમ|મૂળ નય': [7, 13, 17, 28, 35],
  'જૈન નયાભાસ|આધુનિક જ્ઞાનાત્મક પૂર્વગ્રહ (Cognitive Bias)': [16, 25, 26, 33]
};

const css = `
.appendix-editorial .appendix-opener h1{font-size:26pt;line-height:1.18;margin:0 0 1.5mm}
.appendix-editorial .appendix-kicker{display:block;width:max-content;max-width:100%;background:#282828;color:#fff;padding:1mm 3mm;margin-bottom:2.5mm;font-size:12pt;line-height:1.3}
.appendix-editorial .appendix-deck{display:block;font-size:.64em;line-height:1.3;color:#555;margin-top:1mm}
.appendix-editorial .generic-heading.appendix-opener-subtitle :is(h2,h3,h4){font-size:11pt;line-height:1.28;color:#555;margin:0 0 4mm;padding:0 0 2.5mm;border:0;border-bottom:1pt solid #333}
.appendix-editorial .generic-heading :is(h2,h3,h4,h5,h6){margin:2.1mm 0 1.4mm;line-height:1.26}
.appendix-editorial .generic-heading h2{font-size:16pt;border-bottom:.55pt solid #aaa;padding-bottom:.8mm}
.appendix-editorial .generic-heading h3{font-size:13pt;border-left:1pt solid #a0a0a0;padding-left:2mm}
.appendix-editorial .generic-heading :is(h4,h5,h6){font-size:11.5pt;margin-left:3mm;color:#3d3d3d}
.appendix-editorial .appendix-heading-number{display:inline-block;min-width:5mm;margin-right:1mm;padding:.35mm 1mm;background:#e8e8e8;color:#444;font-size:.85em;text-align:center;white-space:nowrap}
.appendix-editorial .appendix-heading-translation{display:block;font-size:.69em;font-weight:600;color:#585858;margin-top:.8mm}
.appendix-editorial .generic-list-item{grid-template-columns:6.5mm minmax(0,1fr);gap:1.8mm}
.appendix-editorial .appendix-list-marker{display:grid;place-items:center;align-self:start;min-height:5mm;background:#e8e8e8;color:#333;font-size:0;line-height:1}
.appendix-editorial .appendix-list-marker::before{content:attr(data-display);font-size:9pt}
.appendix-editorial .appendix-bullet{font-size:0;text-align:center}
.appendix-editorial .appendix-bullet::before{content:'';display:inline-block;width:1.3mm;height:1.3mm;margin-top:1.9mm;background:#555;transform:rotate(45deg)}
.appendix-editorial .semantic-table{font-size:10.5pt;line-height:1.36}
.appendix-editorial .semantic-table :is(th,td){padding:1.45mm 1.4mm;border-color:#b1b1b1}
.appendix-editorial .semantic-table th{background:#303030;color:#fff;border-color:#737373;font-size:10pt;line-height:1.25}
.appendix-editorial .semantic-table tr[data-stripe=gray] td{background:#f0f0f0}
.appendix-editorial .semantic-table[data-index-column] :is(th,td):first-child{text-align:center}
.appendix-editorial .semantic-table[data-index-column] td:first-child{font-weight:700;color:#494949}
.appendix-editorial .semantic-chart{margin:2mm 0 3mm}
.appendix-editorial .chart-root{background:#303030;color:white;border-color:#303030}
.appendix-editorial .chart-branch{background:#f5f5f5;border-color:#aaa}
.appendix-editorial .chart-branch-title{background:#e2e2e2;border-bottom:1pt solid #555}
.appendix-editorial .chart-subtree li::marker{color:#535353}
.appendix-editorial .chart-sequence .chart-step{display:flex;align-items:baseline;gap:2.4mm;background:#f0f0f0;border:.55pt solid #aaa;border-left:1.1pt solid #444;padding:1.4mm 2mm;font-size:11pt}
.appendix-editorial .chart-sequence li:nth-child(even) .chart-step{background:#fafafa}
.appendix-editorial .appendix-step-number{flex:none;min-width:6mm;padding:1mm;background:#3d3d3d;color:#fff;text-align:center;font:700 10pt/1 'Anek Gujarati',sans-serif}
`;
const compactCss = `
.appendix-compact .generic-list-item,.appendix-compact p.generic-prose{line-height:1.29;margin-bottom:1mm}
.appendix-compact .generic-heading :is(h2,h3,h4,h5,h6){margin-top:1.45mm;margin-bottom:1mm}
.appendix-compact .semantic-table{line-height:1.32}
.appendix-compact .semantic-table :is(th,td){padding-top:1mm;padding-bottom:1mm}
.appendix-compact .semantic-chart{margin-top:1.5mm;margin-bottom:2mm}
`;

async function main() {
  const out = path.resolve(process.argv[2]);
  const file = path.join(out, 'naya_chakshu_book.html');
  const paginationFile = path.join(out, 'pagination.json');
  const pagination = JSON.parse(fs.readFileSync(paginationFile, 'utf8'));
  const manifest = JSON.parse(fs.readFileSync(path.join(out, 'source-manifest.json'), 'utf8'));
  const tablesByRow = Object.fromEntries(manifest.blocks.filter(block => block.table_id).map(block => [block.id, block.table_id]));
  const browser = await chromium.launch({executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1100}});
    await page.emulateMedia({media: 'print'});
    await page.goto(pathToFileURL(file).href);
    if (!await page.locator('.appendix-editorial').count()) await page.addStyleTag({content: css});
    if (!await page.locator('#appendix-compact-styles').count()) {
      const style = await page.addStyleTag({content: compactCss});
      await style.evaluate(node => { node.id = 'appendix-compact-styles'; });
    }
    const compactKeys = (process.argv.find(arg => arg.startsWith('--compact=')) || '--compact=D016,D018,D021,D023').split('=')[1].split(',');
    const result = await page.evaluate(async ({columnWidths, oldStarts, tablesByRow, compactKeys}) => {
      await document.fonts.ready;
      const oldPages = [...document.querySelectorAll('.page[data-type=appendix]')];
      if (!oldPages.length) throw Error('No appendix pages');
      const groups = Map.groupBy(oldPages, page => page.dataset.key);
      const firstNumber = Number(oldPages[0].dataset.physicalPage);
      const report = [];
      const docStarts = {...oldStarts};
      const gu = value => String(value).replace(/[0-9]/g, digit => '૦૧૨૩૪૫૬૭૮૯'[digit]);

      function badge(textNode, prefix, className) {
        const span = document.createElement('span');
        span.className = className;
        span.textContent = prefix;
        textNode.before(span);
        textNode.data = textNode.data.slice(prefix.length);
      }

      function deck(heading, pattern, className) {
        const tail = heading.lastChild;
        const match = tail?.nodeType === Node.TEXT_NODE && tail.data.match(pattern);
        if (!match) return;
        tail.data = tail.data.slice(0, match.index);
        const span = document.createElement('span');
        span.className = className;
        span.textContent = match[0];
        heading.append(span);
      }

      function styleBlock(block, index) {
        const heading = block.querySelector('.generic-heading');
        if (heading) {
          if (index === 0) {
            block.classList.add('appendix-opener');
            const prefix = heading.firstChild.textContent.match(/^પરિશિષ્ટ\s+(?:વિભાગ|[૦-૯]+)\s*:/);
            if (prefix && heading.firstChild.nodeType === Node.TEXT_NODE) badge(heading.firstChild, prefix[0], 'appendix-kicker');
            deck(heading, /\s+\([^()]+\)\s*$/, 'appendix-deck');
          } else if (index === 1 && /^\([A-Za-z]/.test(heading.textContent.trim())) {
            block.classList.add('appendix-opener-subtitle');
          } else {
            const text = [...heading.childNodes].find(node => node.nodeType === Node.TEXT_NODE);
            const prefix = text?.data.match(/^\s*[૦-૯0-9]+(?:\.[૦-૯0-9]+)*\.(?=\s)/);
            if (prefix) badge(text, prefix[0], 'appendix-heading-number');
            deck(heading, /\s+\((?:[0-9]+\s+)?[A-Za-z][^()]*\)\s*$/, 'appendix-heading-translation');
          }
        }
        for (const marker of block.querySelectorAll('.generic-list-marker')) {
          const number = marker.textContent.trim().match(/^([0-9૦-૯]+)\.$/);
          if (number) {
            marker.classList.add('appendix-list-marker');
            marker.dataset.display = gu(number[1]);
          } else if (marker.textContent.trim() === '•') marker.classList.add('appendix-bullet');
        }
        for (const step of block.querySelectorAll('.chart-step')) {
          const first = step.firstChild;
          const prefix = first?.nodeType === Node.TEXT_NODE && first.data.match(/^[૦-૯]+\./);
          if (prefix) badge(first, prefix[0], 'appendix-step-number');
        }
      }

      function tableStyle(group) {
        const table = group.querySelector('table');
        const headers = [...table.querySelectorAll('thead th')].map(header => header.textContent.trim());
        const widths = columnWidths[headers.slice(0, 2).join('|')];
        if (!widths || widths.length !== headers.length) throw Error('Unmapped appendix table: ' + headers.join(' | '));
        const cols = document.createElement('colgroup');
        for (const width of widths) {
          const col = document.createElement('col');
          col.style.width = width + '%';
          cols.append(col);
        }
        if (!table.querySelector('colgroup')) table.prepend(cols);
        if (['ક્રમ', 'ખંડ ક્રમ', 'પરિશિષ્ટ'].includes(headers[0])) table.dataset.indexColumn = '';
        return widths;
      }

      let nextNumber = firstNumber;
      for (const [key, pages] of groups) {
        const blocks = pages.flatMap(page => [...page.querySelector('.page-content').children]);
        const template = pages[0].cloneNode(true);
        const styled = template.classList.contains('appendix-editorial');
        template.classList.add('appendix-editorial');
        template.classList.toggle('appendix-compact', compactKeys.includes(key));
        template.querySelector('.page-content').replaceChildren();
        const previousPages = pages.length;
        const rows = new Map();
        const units = [];
        for (const [index, block] of blocks.entries()) {
          if (!block.classList.contains('table-group')) {
            if (!styled) styleBlock(block, index);
            units.push({node: block});
            continue;
          }
          const widths = tableStyle(block);
          for (const row of block.querySelectorAll('tbody tr')) {
            const tableId = tablesByRow[row.dataset.sourceId] || block.querySelector('thead').textContent;
            if (!rows.has(tableId)) {
              const shell = block.cloneNode(true);
              shell.querySelector('tbody').replaceChildren();
              rows.set(tableId, {shell, widths, count: 0});
            }
            const table = rows.get(tableId);
            row.dataset.stripe = table.count++ % 2 ? 'gray' : 'white';
            units.push({node: row, tableId});
          }
        }
        let current;
        let content;
        let activeTable;
        const rendered = [];
        const pageBatches = [];
        function newPage() {
          current = template.cloneNode(true);
          content = current.querySelector('.page-content');
          activeTable = null;
          const n = nextNumber++;
          current.id = 'page-' + n;
          current.dataset.physicalPage = n;
          current.classList.toggle('even', n % 2 === 0);
          current.classList.toggle('odd', n % 2 === 1);
          const number = '<span class="folio">' + gu(n) + '</span>';
          const book = '<span><b>નય-ચક્ષુ</b> | નયનું જ્ઞાન, સંશયનું સમાધાન</span>';
          const label = document.createElement('span');
          label.append(document.createElement('b'));
          label.firstChild.textContent = current.dataset.khandaLabel;
          current.querySelector('.running-footer').innerHTML = n % 2 ? label.outerHTML + number : number + book;
          pages[0].before(current);
          rendered.push(current);
          pageBatches.push([]);
        }
        function append(unit) {
          if (!unit.tableId) {
            content.append(unit.node);
            activeTable = null;
            return;
          }
          if (activeTable !== unit.tableId) {
            content.append(rows.get(unit.tableId).shell.cloneNode(true));
            activeTable = unit.tableId;
          }
          content.lastElementChild.querySelector('tbody').append(unit.node);
        }
        function fits() {
          const footer = current.querySelector('.running-footer').getBoundingClientRect().top;
          const bottom = content.lastElementChild.getBoundingClientRect().bottom;
          return bottom <= footer - 8 && content.scrollWidth <= content.clientWidth + 2;
        }
        function fill(page) {
          const content = page.querySelector('.page-content');
          const top = content.getBoundingClientRect().top;
          const bottom = content.lastElementChild.getBoundingClientRect().bottom;
          const limit = page.querySelector('.running-footer').getBoundingClientRect().top - 8;
          return (bottom - top) / (limit - top);
        }
        function redraw(page, batches) {
          current = page;
          content = page.querySelector('.page-content');
          content.replaceChildren();
          activeTable = null;
          for (const batch of batches) for (const unit of batch) append(unit);
          return fits();
        }
        docStarts[key] = nextNumber;
        newPage();
        for (let index = 0; index < units.length;) {
          let end = index + 1;
          if (units[index].node.dataset.kind === 'heading') {
            while (units[end]?.node.dataset.kind === 'heading') end++;
            if (units[end]) {
              const lead = units[end].node;
              end++;
              if (units[end] && (lead.textContent.trim().endsWith(':') || (units[end - 1].tableId && units[end - 1].tableId === units[end].tableId))) end++;
            }
          }
          const batch = units.slice(index, end);
          const hadContent = content.childElementCount > 0;
          for (const unit of batch) append(unit);
          if (!fits()) {
            if (!hadContent) throw Error('Appendix block too tall: ' + key + '/' + batch[0].node.id);
            for (const unit of batch) unit.node.remove();
            for (const empty of content.querySelectorAll('.table-group:not(:has(tbody tr))')) empty.remove();
            newPage();
            for (const unit of batch) append(unit);
            if (!fits()) throw Error('Appendix block too tall after page break: ' + key + '/' + batch[0].node.id);
          }
          pageBatches.at(-1).push(batch);
          index = end;
        }
        if (rendered.length > 1 && fill(rendered.at(-1)) < .55) {
          const before = rendered.at(-2);
          const last = rendered.at(-1);
          const left = pageBatches.at(-2);
          const right = pageBatches.at(-1);
          let best = left.length;
          let difference = Math.abs(fill(before) - fill(last));
          for (let split = left.length - 1; split > 0; split--) {
            const fitsLast = redraw(last, [...left.slice(split), ...right]);
            const fitsBefore = redraw(before, left.slice(0, split));
            if (!fitsLast || !fitsBefore) continue;
            const imbalance = Math.abs(fill(before) - fill(last));
            if (imbalance < difference) {
              best = split;
              difference = imbalance;
            }
          }
          redraw(last, [...left.slice(best), ...right]);
          redraw(before, left.slice(0, best));
        }
        for (const page of pages) page.remove();
        const fills = rendered.map(page => Math.round(100 * fill(page)));
        report.push({key, start: docStarts[key], before: previousPages, after: rendered.length, fills, tables: [...rows.values()].map(({widths,count}) => ({widths, count}))});
      }
      const redirects = new Map([...groups.keys()].map(key => ['#page-' + oldStarts[key], '#page-' + docStarts[key]]));
      for (const link of document.querySelectorAll('a[href^="#page-"]')) {
        const key = link.dataset.targetKey;
        const page = docStarts[key];
        if (page) {
          link.setAttribute('href', '#page-' + page);
          link.querySelector('.toc-page').textContent = gu(page);
        } else if (redirects.has(link.getAttribute('href'))) {
          link.setAttribute('href', redirects.get(link.getAttribute('href')));
        }
      }
      const pageMap = [...document.querySelectorAll('.page')].map(page => ({
        physicalPage: +page.dataset.physicalPage, type: page.dataset.type, key: page.dataset.key, khanda: page.dataset.khandaLabel,
        sourceIds: [...page.querySelectorAll('[data-source-id]')].map(node => node.dataset.sourceId)
      }));
      return {report, pageMap, docStarts};
    }, {columnWidths, oldStarts: pagination.docStarts, tablesByRow, compactKeys});
    console.log(JSON.stringify(result.report));
    if (process.argv.includes('--measure-only')) return;
    const afterIds = result.pageMap.flatMap(page => page.sourceIds);
    const beforeIds = pagination.pageMap.flatMap(page => page.sourceIds);
    if (JSON.stringify(afterIds) !== JSON.stringify(beforeIds)) throw Error('Appendix source order changed');
    fs.writeFileSync(file, '<!doctype html>\n' + await page.evaluate(() => document.documentElement.outerHTML));
    Object.assign(pagination, {pageMap: result.pageMap, docStarts: result.docStarts, pageCount: result.pageMap.length});
    fs.writeFileSync(paginationFile, JSON.stringify(pagination, null, 2));
    fs.writeFileSync(path.join(out, 'appendix-layout-audit.json'), JSON.stringify(result.report, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
