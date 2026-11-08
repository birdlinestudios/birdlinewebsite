"""The four policy/support PDFs (Claude Docs exports) -> the inner HTML of a document page on the site.
Headings come from the serif sizes (24 title, 16.5 section, 13.5 sub-section), bullets from the DejaVu glyphs, numbered
lists from the "1. " text, bold from the semibold spans, tables from PyMuPDF's table finder (cell text re-read from the
page so the spaces survive), links from the PDF's link annotations. Run: pdf2html.py <pdf> <out.html>"""
import sys, re, html, json
import pymupdf as fitz

SITE_LINKS = {'https://birdlinestudios.com/privacy': '{{ROOT}}privacy.html', 'https://birdlinestudios.com/terms': '{{ROOT}}terms.html',
              'https://birdlinestudios.com/support': '{{ROOT}}support.html', 'https://birdlinestudios.com/data-deletion': '{{ROOT}}data-deletion.html'}

def esc(s):
    return html.escape(s, quote=False)

def span_html(s, links):
    text = s['text']
    if not text.strip() and not text:
        return ''
    r = fitz.Rect(s['bbox'])
    href = None
    for lr, uri in links:
        if lr.intersects(r) and (lr & r).width > r.width * 0.5:
            href = uri; break
    out = esc(text)
    if 'Mono' in s['font']:
        out = '<code>%s</code>' % out
    if 'Semib' in s['font'] or 'Bold' in s['font']:
        out = '<strong>%s</strong>' % out
    if href:
        href = SITE_LINKS.get(href, href)
        out = '<a href="%s">%s</a>' % (href, out)
    return out

def convert(path):
    doc = fitz.open(path)
    items = []   # (kind, payload)
    date = None
    for page in doc:
        H = page.rect.height
        links = [(fitz.Rect(l['from']), l['uri']) for l in page.get_links() if l.get('uri')]
        tables = []
        try:
            for tb in page.find_tables().tables:
                tables.append((fitz.Rect(tb.bbox), tb))
        except Exception:
            pass
        emitted = set()
        lines = []
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                spans = [s for s in l['spans'] if s['text'] != '']
                if not spans: continue
                lines.append(dict(x=l['bbox'][0], y=l['bbox'][1], y1=l['bbox'][3], spans=spans, bbox=fitz.Rect(l['bbox'])))
        lines.sort(key=lambda l: (round(l['y']), l['x']))
        # the bullets are small filled squares drawn beside the lines (x about 64 for the first level, deeper for nested ones)
        dots = [fitz.Rect(d['rect']) for d in page.get_drawings() if d['rect'].width < 8 and d['rect'].height < 8 and d.get('fill') and max(d['fill']) < 0.5]
        bullets = []
        bullet_ys = [((r.y0 + r.y1) / 2, r.x0) for r in dots]
        for l in lines:
            if l in bullets: continue
            text = ''.join(s['text'] for s in l['spans']).strip()
            size = max(s['size'] for s in l['spans'])
            # running header / footer
            if l['y'] < 40 or l['y1'] > H - 40:
                continue
            if any(s['size'] < 10 for s in l['spans']) and ('@' in text or re.match(r'^\w{3} \d{1,2}, \d{4}', text)):
                m = re.match(r'^(\w{3} \d{1,2}, \d{4})', text)
                if m: date = m.group(1)
                continue
            # a table: emit once where its first line sits
            ti = next((i for i, (rect, tb) in enumerate(tables) if rect.intersects(l['bbox']) and (rect & l['bbox']).height > l['bbox'].height * 0.5), None)
            if ti is not None:
                if ti not in emitted:
                    emitted.add(ti)
                    rect, tb = tables[ti]
                    rows = []
                    for row in tb.rows:
                        cells = []
                        for c in row.cells:
                            if c is None: cells.append(''); continue
                            t = page.get_text('text', clip=fitz.Rect(c)).strip()
                            cells.append(re.sub(r'\s+', ' ', t))
                        rows.append(cells)
                    items.append(('table', rows))
                continue
            if size >= 20:
                items.append(('h1', text)); continue
            if 16 <= size < 20:
                items.append(('h2', text)); continue
            if 13 <= size < 16:
                items.append(('h3', text)); continue
            content = ''.join(span_html(s, links) for s in l['spans'])
            # a short line that is bold from end to end is a run-in heading ("In the App", "By email")
            if len(text) < 70 and all(('Semib' in s['font'] or 'Bold' in s['font'] or not s['text'].strip()) for s in l['spans']) and not re.match(r'^\d+\.\s', text) and l['x'] < 60:
                items.append(('h4', text)); continue
            ymid = (l['y'] + l['y1']) / 2
            dot = next((bx for by, bx in bullet_ys if abs(by - ymid) < 5 and bx < l['x']), None)
            is_bullet = dot is not None
            level = 1 if l['x'] < 90 else 2
            num = re.match(r'^(\d+)\.\s', text)
            if is_bullet:
                items.append(('li', level, content, 'ul')); continue
            if num and l['x'] > 56:
                items.append(('li', level, content, 'ol')); continue
            if l['x'] > 70 and items and items[-1][0] in ('li', 'cont'):
                items.append(('cont', content)); continue
            # a plain line: joins the previous paragraph when it follows closely
            # lines 18pt apart are one paragraph; a 25pt step is a new one
            if items and items[-1][0] == 'p' and l['y'] - items[-1][2] < 22 and items[-1][3] == page.number:
                items[-1] = ('p', items[-1][1] + ' ' + content, l['y'], page.number); continue
            if items and items[-1][0] == 'p' and page.number != items[-1][3] and l['y'] < 110 and not re.match(r'^[A-Z]', text.lstrip('“"(')) :
                # the first line of a page that continues a paragraph from the page before
                items[-1] = ('p', items[-1][1] + ' ' + content, l['y'], page.number); continue
            items.append(('p', content, l['y'], page.number))
    # assemble
    out = []
    i = 0
    def flush_list(lst, kind):
        return '<%s>%s</%s>' % (kind, ''.join('<li>%s</li>' % x for x in lst), kind)
    while i < len(items):
        it = items[i]
        if it[0] == 'h1': out.append('<h1>%s</h1>' % esc(it[1]))
        elif it[0] == 'h2': out.append('<h2>%s</h2>' % esc(it[1]))
        elif it[0] == 'h3': out.append('<h3>%s</h3>' % esc(it[1]))
        elif it[0] == 'h4': out.append('<h4>%s</h4>' % esc(it[1]))
        elif it[0] == 'p': out.append('<p>%s</p>' % it[1])
        elif it[0] == 'table':
            rows = it[1]
            while i + 1 < len(items) and items[i + 1][0] == 'table' and items[i + 1][1][0] == rows[0]:   # a table split over a page break
                rows = rows + items[i + 1][1][1:]; i += 1
            head = '<tr>%s</tr>' % ''.join('<th>%s</th>' % esc(c) for c in rows[0])
            body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % esc(c) for c in r) for r in rows[1:])
            out.append('<table><thead>%s</thead><tbody>%s</tbody></table>' % (head, body))
        elif it[0] == 'li':
            kind = it[3]; lst = []
            while i < len(items) and items[i][0] in ('li', 'cont'):
                if items[i][0] == 'li':
                    if items[i][3] != kind: break
                    txt = items[i][2]
                    if kind == 'ol': txt = re.sub(r'^(<strong>)?\d+\.\s*', r'\1', txt)
                    lst.append(txt)
                else:
                    lst[-1] += ' ' + items[i][1]
                i += 1
            out.append(flush_list(lst, kind)); continue
        elif it[0] == 'cont':
            out[-1] = out[-1][:-4] + ' ' + it[1] + '</p>' if out and out[-1].endswith('</p>') else out.append('<p>%s</p>' % it[1]) or out[-1]
        i += 1
    body = '\n'.join(out)
    body = body.replace('​', '')
    return body, date

if __name__ == '__main__':
    body, date = convert(sys.argv[1])
    open(sys.argv[2], 'w', encoding='utf-8').write(body)
    print(sys.argv[2], 'date:', date, 'chars:', len(body), 'h2:', body.count('<h2>'), 'h3:', body.count('<h3>'), 'ul:', body.count('<ul>'), 'ol:', body.count('<ol>'), 'tables:', body.count('<table>'), 'links:', body.count('<a '))
