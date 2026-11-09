"""Semantic, source-preserving non-chapter Markdown rendering for Naya-Chakshu.

Only stdlib is required.  Public API: render_markdown(text, source_key).
Returns blocks suitable for DOM-measured pagination, CSS and a source manifest.
Charts are actual nested HTML/ordered structures; no pre/ASCII chart rendering.
"""
from __future__ import annotations

import hashlib
import html
import re
from collections import OrderedDict
from pathlib import Path

from chapter_renderer import normalize_script
from khanda_numbering import normalize_references


CSS = r'''
.nonchapter-body{font-family:'Noto Sans Gujarati',sans-serif;font-size:11pt;line-height:1.38;color:#171717}
.generic-block{display:flow-root;break-inside:avoid;overflow-wrap:break-word}
.generic-prose,.generic-list-item,.generic-quote{font-size:11pt;line-height:1.38;text-align:justify;text-align-last:start;margin:0 0 2.3mm}
.generic-heading{font-family:'Anek Gujarati',sans-serif;font-weight:700;text-align:left;line-height:1.25;margin:2.5mm 0 2mm}
h1.generic-heading{font-size:25pt;font-weight:800}h2.generic-heading{font-size:17pt}h3.generic-heading{font-size:13pt}h4.generic-heading,h5.generic-heading,h6.generic-heading{font-size:12pt}
.generic-heading .heading-summary{display:block;font:600 13pt/1.25 'Anek Gujarati',sans-serif;color:#444;margin-top:1.4mm}
.generic-list-item{display:grid;grid-template-columns:5.5mm minmax(0,1fr);gap:1mm}.generic-list-marker{font-family:'Anek Gujarati',sans-serif;font-weight:700;color:#777;text-align:left}.generic-list-copy{min-width:0}
.generic-quote{border-left:1.2pt solid #999;padding:1.5mm 2.5mm;background:#f6f6f6}
.generic-verse{font-family:'Anek Gujarati',sans-serif;font-size:12pt;font-weight:600;line-height:1.45;text-align:left;margin:1mm 0 3mm;padding:2mm 3mm;border-left:1pt solid #aaa}
.generic-verse .verse-line{display:block;min-height:1.45em}.generic-rule{border:0;border-top:.55pt solid #bbb;margin:2mm 0}
.semantic-table{width:100%;table-layout:fixed;border-collapse:collapse;font-size:11pt;line-height:1.38;margin:0;color:#171717}
.semantic-table th,.semantic-table td{border:.55pt solid #aaa;padding:1.3mm 1.5mm;vertical-align:top;overflow-wrap:anywhere;text-align:left}
.semantic-table th{font-family:'Anek Gujarati',sans-serif;font-weight:700;background:#e8e8e8}.semantic-table td{font-family:'Noto Sans Gujarati',sans-serif}.semantic-table-row-even td{background:#f5f5f5}
.semantic-table table{width:100%}.table-piece{margin:0 0 2mm}
.semantic-chart{font-family:'Noto Sans Gujarati',sans-serif;font-size:11pt;line-height:1.38;margin:2mm 0 3mm;break-inside:avoid}
.semantic-chart,.semantic-chart *,.semantic-table,.semantic-table *{box-sizing:border-box}
.chart-root{font-family:'Anek Gujarati',sans-serif;font-size:13pt;font-weight:700;line-height:1.25;text-align:center;background:#e7e7e7;border:.6pt solid #888;padding:2mm 3mm;margin:0 auto;max-width:115mm}
.chart-branches{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:3mm;padding-top:4mm;position:relative}
.chart-branches:before{content:'';position:absolute;top:0;left:50%;height:4mm;border-left:.6pt solid #888}
.chart-branch{position:relative;border-top:.6pt solid #888;padding-top:2mm;min-width:0}
.chart-branch-title{font-family:'Anek Gujarati',sans-serif;font-size:12pt;font-weight:700;line-height:1.25;text-align:center;background:#f0f0f0;border:.55pt solid #aaa;padding:1.8mm 2mm;margin:0 0 2mm}
.chart-node-list{margin:0;padding:0;list-style:none;border-left:.55pt solid #aaa}
.chart-node{padding:1.1mm 1.8mm;border-bottom:.45pt solid #ddd;margin-left:1.5mm;text-align:left;overflow-wrap:break-word}.chart-node:last-child{border-bottom:0}
.chart-dimensions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2mm;margin-top:4mm;padding-top:2mm;border-top:.55pt solid #888}
.chart-dimension{border:.55pt solid #aaa;padding:2mm;background:#f5f5f5}.chart-dimension strong{display:block;font-family:'Anek Gujarati',sans-serif;font-size:12pt;line-height:1.25;margin-bottom:1mm}.chart-dimension span{display:block;text-align:left;font-size:11pt}
.chart-sequence{list-style:none;margin:0;padding:0}.chart-sequence li{margin:0;padding:0;display:flex;flex-direction:column;align-items:center;text-align:center}
.chart-sequence .chart-step{border:.6pt solid #999;background:#f1f1f1;width:100%;padding:1.7mm 3mm;text-align:left;font-size:11pt}.chart-connector{display:block;width:5mm;height:3mm;margin:0 auto}
.chart-subtree{list-style:none;margin:0;padding:0 0 0 2mm;border-left:.55pt solid #bbb}.chart-subtree li{padding:1.1mm 1.5mm;text-align:left;border-bottom:.45pt solid #ddd}.chart-subtree li:last-child{border-bottom:0}
.generic-inline-code{font:inherit;background:#f2f2f2;padding:0 .5mm}
.generic-devanagari{font-family:'Noto Sans Devanagari',sans-serif}
'''


def _plain(text: str) -> str:
    text = re.sub(r'<br\s*/?>', ' ', text, flags=re.I)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[*`]', '', text)
    return html.unescape(re.sub(r'\s+', ' ', text).strip())

def normalize_definition_label(text: str) -> str:
    return re.sub(r'^(\*\*)?મૂળ (?:આગમ(?:િક)? સૂત્રો?|સૂક્તિઓ)(?=(?:\*\*)?:)',
                  r'\1મૂળ લક્ષણ સૂત્ર', text)


def inline(text: str) -> str:
    """Safe inline Markdown; no external code execution or unsanitized HTML."""
    text = html.escape(normalize_definition_label(normalize_script(text)))
    text = re.sub(r'&lt;br\s*/?&gt;', '<br>', text, flags=re.I)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<span class="generic-inline-code">\1</span>', text)
    def link(m):
        target=html.unescape(m.group(2))
        # Root resolves project-relative chapter links into master anchors.
        # Unknown/executable schemes are printed as labels, never executable.
        scheme=re.match(r'^([A-Za-z][A-Za-z0-9+.-]*):',target)
        if scheme and scheme.group(1).lower() not in ('http','https','mailto'):
            return m.group(1)
        return '<a href="'+html.escape(target,quote=True)+'">'+m.group(1)+'</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', link, text)
    # Some canonical appendix cells end mid-emphasis. Formatting delimiters
    # have no printable meaning; retain all words without leaking raw stars.
    text = text.replace('*','')
    return re.sub(r'[\u0900-\u097f]+(?:[ \t]+[\u0900-\u097f]+)*',lambda m:'<span class="generic-devanagari">'+m.group(0)+'</span>',text)


def _arrow() -> str:
    return '<svg class="chart-connector" viewBox="0 0 20 12" aria-hidden="true"><path d="M10 0V9M6 5l4 5 4-5" fill="none" stroke="#888" stroke-width="1"/></svg>'


def _chart_mermaid(code: str) -> tuple[str, list[str], dict]:
    labels: OrderedDict[str, str] = OrderedDict()
    for m in re.finditer(r'([A-Za-z][A-Za-z0-9_]*)\["(.*?)"\]', code):
        labels.setdefault(m.group(1), m.group(2))
    # Replace node declarations by identifiers to expose edges reliably.
    edges_code = re.sub(r'([A-Za-z][A-Za-z0-9_]*)\["(.*?)"\]', r'\1', code)
    edges = re.findall(r'([A-Za-z][A-Za-z0-9_]*)\s*-->\s*([A-Za-z][A-Za-z0-9_]*)', edges_code)
    children: dict[str, list[str]] = {k: [] for k in labels}
    for a, b in edges:
        children.setdefault(a, []).append(b)
    targets = {b for _, b in edges}
    roots = [k for k in labels if k not in targets]
    if len(roots) == 1 and all(len(v) <= 1 for v in children.values()):
        ordered, current, seen = [], roots[0], set()
        while current and current not in seen:
            seen.add(current)
            ordered.append(current)
            current = children.get(current, [None])[0] if children.get(current) else None
        rendered = '<ol class="chart-sequence">' + ''.join(
            '<li><div class="chart-step">' + inline(labels[k]) + '</div>' + (_arrow() if i < len(ordered)-1 else '') + '</li>'
            for i, k in enumerate(ordered)) + '</ol>'
    else:
        def descendants(k: str, seen: set[str]) -> str:
            if k in seen:
                return ''
            seen = seen | {k}
            return '<ul class="chart-subtree">' + ''.join('<li>' + inline(labels.get(c, c)) + descendants(c, seen) + '</li>' for c in children.get(k, [])) + '</ul>' if children.get(k) else ''
        root = roots[0] if roots else next(iter(labels))
        rendered = '<div class="chart-root">' + inline(labels[root]) + '</div><div class="chart-branches">' + ''.join(
            '<section class="chart-branch"><h4 class="chart-branch-title">' + inline(labels.get(c,c)) + '</h4>' + descendants(c, {root}) + '</section>'
            for c in children.get(root, [])) + '</div>'
    return rendered, list(labels.values()), {'type': 'mermaid-semantic', 'edges': edges, 'node_count': len(labels)}


def _chart_ascii(code: str) -> tuple[str, list[str], dict]:
    lines = code.splitlines()
    bracket_rows = [(i, list(re.finditer(r'\[\s*(.*?)\s*\]', line))) for i,line in enumerate(lines) if '[' in line]
    root_i, root_matches = bracket_rows[0]
    root_label = root_matches[0].group(1).strip()
    branch_i, branch_matches = next((i, ms) for i, ms in bracket_rows[1:] if len(ms)>1)
    branch_labels = [m.group(1).strip() for m in branch_matches]
    labels = [root_label] + branch_labels
    if len(branch_labels) == 4:
        # Every following parenthesized group is one description, including
        # embedded spaces or Latin words. Exact source order is retained.
        description_line = next((line for line in lines[branch_i+1:] if '(' in line), '')
        descriptions = re.findall(r'\([^()]*\)', description_line)
        if len(descriptions) != 4:
            descriptions = [part.strip() for part in re.split(r'\s{2,}', description_line.strip())]
        labels += descriptions
        nested: list[list[str]] = [[], [], [], []]
        anchors = [m.start() for m in branch_matches]
        for line in lines[branch_i+1:]:
            matches = list(re.finditer(r'[├└]─\s*', line))
            for j,m in enumerate(matches):
                end = matches[j+1].start() if j+1<len(matches) else len(line)
                item=line[m.end():end].strip()
                col=min(range(4),key=lambda k:abs(m.start()-anchors[k]))
                if item:nested[col].append(item)
        labels += [item for group in nested for item in group]
        rendered = '<div class="chart-root">' + inline(root_label) + '</div><div class="chart-dimensions">' + ''.join(
            '<div class="chart-dimension"><strong>' + inline(title) + '</strong><span>' + inline(descriptions[i] if i < len(descriptions) else '') + '</span>' + ('<ul class="chart-node-list">'+''.join('<li class="chart-node">'+inline(item)+'</li>' for item in nested[i])+'</ul>' if nested[i] else '') + '</div>'
            for i,title in enumerate(branch_labels)) + '</div>'
        return rendered, labels, {'type':'ascii-four-dimensions', 'branches':4,'nested_node_count':sum(map(len,nested))}
    if len(branch_labels) != 2:
        raise ValueError('Unsupported ASCII chart branch count: '+str(len(branch_labels)))
    branches: list[list[str]] = [[], []]
    # Branch glyph positions are structural. A line with just the right branch
    # is assigned to column 2 even though its leading whitespace is stripped.
    for line in lines[branch_i+1:]:
        matches = list(re.finditer(r'[├└]─\s*', line))
        for j,m in enumerate(matches):
            end = matches[j+1].start() if j+1 < len(matches) else len(line)
            label = line[m.end():end].strip()
            col = 0 if len(matches)>1 and j==0 else (1 if m.start()>20 else 0)
            if label:
                branches[col].append(label)
    # Readable graphic uses column order. Manifest also preserves the original
    # source row sequence separately for independently verifiable label coverage.
    labels += [x for b in branches for x in b]
    rendered = '<div class="chart-root">' + inline(root_label) + '</div><div class="chart-branches">' + ''.join(
        '<section class="chart-branch"><h4 class="chart-branch-title">' + inline(title) + '</h4><ul class="chart-node-list">' + ''.join('<li class="chart-node">'+inline(item)+'</li>' for item in branches[i]) + '</ul></section>'
        for i,title in enumerate(branch_labels)) + '</div>'
    return rendered, labels, {'type':'ascii-two-branch-tree', 'branches':2}


def render_chart(code: str, language: str = '') -> dict:
    if language.strip().lower() == 'mermaid':
        rendered, labels, meta = _chart_mermaid(code)
    else:
        rendered, labels, meta = _chart_ascii(code)
    # Whitespace between semantic nodes gives textContent the same boundaries
    # as the visual chart without exposing source connection glyphs.
    rendered=re.sub(r'(</(?:div|li|h4|strong|span|section|ol|ul)>)',r'\1 ',rendered)
    semantic_text=html.unescape(re.sub(r'<[^>]+>',' ',rendered))
    semantic_text=re.sub(r'\s+',' ',semantic_text).strip()
    return {'html': '<div class="semantic-chart">'+rendered+'</div>', 'labels': labels, 'text':semantic_text,'semantic_text':semantic_text,'coverage_mode':'chart_label_multiset_and_semantic_dom_order','chart': meta, 'source_code_sha256': hashlib.sha256(code.encode()).hexdigest()}


def _table_cells(line: str) -> list[str]:
    line = line.strip().strip('|')
    return [c.strip().replace('\\|','|') for c in re.split(r'(?<!\\)\|',line)]


def render_markdown(text: str, source_key: str) -> dict:
    """Return ordered {id,kind,html,text,line_start,line_end,...} blocks.

    Table rows are individually paginatable, with repeated semantic table
    headers. `text` describes only the source row, not the repeated header.
    Section heading blocks carry keep_with_next=True.
    """
    source_key = re.sub(r'[^\w-]+','-',source_key).strip('-')
    lines = text.lstrip('\ufeff').splitlines()
    blocks, manifest = [], []
    i = 0
    def add(kind: str, rendered: str, plain: str, start: int, end: int, **extra):
        ident = f'{source_key}-b{len(blocks)+1:04d}'
        display_text = normalize_definition_label(normalize_script(plain))
        block = {'id':ident,'kind':kind,'text':display_text,'line_start':start+1,'line_end':end+1,**extra}
        if display_text != plain:
            block['source_text'] = plain
        block['html'] = f'<div class="generic-block generic-{kind}" id="{ident}" data-source="{ident}">{rendered}</div>'
        blocks.append(block)
        manifest.append({k:v for k,v in block.items() if k!='html'})
    while i < len(lines):
        raw=lines[i]; line=raw.strip()
        if not line:
            i+=1;continue
        if re.fullmatch(r'[-*_]{3,}',line):
            # Rules separate blocks editorially; no textual source content.
            i+=1;continue
        if line.startswith('```'):
            language=line[3:].strip();start=i;i+=1;code=[]
            while i<len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]);i+=1
            source_code='\n'.join(code)
            if language=='mermaid' or re.search(r'[┌├└┬┴│]',source_code):
                chart=render_chart(source_code,language)
                add('chart',chart.pop('html'),chart.pop('text'),start,i,**chart)
            else:
                rendered='<div class="generic-verse">'+''.join('<span class="verse-line">'+inline(s.strip())+'</span>' for s in code)+'</div>'
                add('verse',rendered,_plain(source_code),start,i,preserve_line_breaks=True)
            i+=1;continue
        heading=re.match(r'^(#{1,6})\s+(.+)',line)
        if heading:
            level=len(heading.group(1));value=heading.group(2)
            summary=re.fullmatch(r'(.+?)\s+(\([^()]+\))',value) if level==1 else None
            content=inline(value)
            if summary:
                title,subtitle=summary.groups()
                content=inline(title)+' <span class="heading-summary">'+inline(subtitle)+'</span>'
            add('heading',f'<h{level} class="generic-heading">'+content+f'</h{level}>',_plain(value),i,i,level=level,keep_with_next=True)
            i+=1;continue
        if line.startswith('|') and i+1<len(lines) and re.match(r'^\s*\|?\s*:?-{2,}',lines[i+1]):
            start=i;headers=_table_cells(line);i+=2;table_id=f'{source_key}-t{sum(b["kind"]=="table_row" for b in blocks)+1:03d}';row_index=0
            header_html='<thead><tr>'+''.join('<th scope="col">'+inline(x)+'</th>' for x in headers)+'</tr></thead>'
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=_table_cells(lines[i]);cells += ['']*(len(headers)-len(cells));row_index+=1
                rendered='<div class="table-piece"><table class="semantic-table '+('semantic-table-row-even' if row_index%2==0 else '')+'">'+header_html+'<tbody><tr>'+''.join('<td>'+inline(x)+'</td>' for x in cells)+'</tr></tbody></table></div>'
                add('table_row',rendered,' | '.join(_plain(c) for c in cells),i,i,table_id=table_id,table_headers=[_plain(x) for x in headers],row_index=row_index,column_count=len(headers))
                i+=1
            if row_index==0:
                add('table_header','<table class="semantic-table">'+header_html+'</table>',' | '.join(_plain(c) for c in headers),start,start,table_id=table_id)
            continue
        list_match=re.match(r'^(?:([-*•])\s+|(\d+|[૦-૯]+)[.)]\s+)(.*)',line)
        if list_match:
            marker='•' if list_match.group(1) else list_match.group(2)+'.';value=list_match.group(3);start=i;i+=1
            while i<len(lines) and lines[i].startswith(('  ','\t')) and lines[i].strip() and not lines[i].strip().startswith(('- ','* ','|')):
                value+=' '+lines[i].strip();i+=1
            add('list_item','<div class="generic-list-item"><span class="generic-list-marker">'+html.escape(marker)+'</span><div class="generic-list-copy">'+inline(value)+'</div></div>',_plain(value),start,i-1,marker=marker)
            continue
        if line.startswith('>'):
            start=i;quote=[]
            while i<len(lines) and lines[i].strip().startswith('>'):
                quote.append(re.sub(r'^\s*>\s?','',lines[i]));i+=1
            add('quote','<div class="generic-quote">'+'<br>'.join(inline(x) for x in quote)+'</div>',_plain(' '.join(quote)),start,i-1)
            continue
        start=i;paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip():
            nxt=lines[i].strip()
            if re.match(r'^(?:#{1,6}\s|```|\||>|[-*•]\s|\d+[.)]\s|[૦-૯]+[.)]\s)',nxt) or re.fullmatch(r'[-*_]{3,}',nxt):break
            paragraph.append(nxt);i+=1
        value=' '.join(paragraph)
        add('prose','<p class="generic-prose">'+inline(value)+'</p>',_plain(value),start,i-1)
    return {'blocks':blocks,'manifest':manifest,'css':CSS,'source_key':source_key,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'chart_count':sum(b['kind']=='chart' for b in blocks)}


def render_file(path: str|Path, source_key: str|None=None) -> dict:
    path=Path(path)
    result=render_markdown(path.read_text(encoding='utf-8-sig'),source_key or path.stem)
    intro=re.match(r'000_khanda_(\d)_',path.name)
    if not intro:
        return result
    khanda=int(intro[1])
    for block,record in zip(result['blocks'],result['manifest'],strict=True):
        old=record['text']
        revised=normalize_references(old,khanda,record['kind'])
        if revised==old:
            continue
        for item in (block,record):
            item.setdefault('source_text',old)
            item['text']=revised
        block['html']=normalize_references(block['html'],khanda,record['kind'])
    return result
