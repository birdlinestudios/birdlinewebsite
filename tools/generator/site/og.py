"""Open Graph cards (November 10, 2026): the 1200×630 picture a shared link shows in Slack, iMessage, LinkedIn and X.

One card per page, drawn from what the page itself leads with, so a new page gets a card with no further work:
  photo  — pages that open on one picture (a case study's hero, a blog post's cover, the About banner, the Why/How/Process heroes):
           the picture, cropped around the page's own focal point, under the site's hero gradient, with the page's eyebrow and
           headline at the bottom left and the Birdline wordmark top left. A case study shows the brand's logo over its headline.
  strip  — pages that open on a row of work (the homepage marquee, the Work reel, the case study grid, the services and their
           hero strips, the blog, the workspace screens...): navy, the wordmark, the headline, and the first tiles of that row.
  plain  — everything else (legal pages, testimonials): navy, the wordmark, the headline and the page's description.
The headline keeps the site's two-tone marker (the periwinkle span) and the fonts are the site's own (Host Grotesk and Inter, from
site/fonts). build_site.py calls card() for every Next.js page and files the result as /og/<page>.<hash>.jpg.
"""
import os, re, io, json, hashlib, shutil
from html.parser import HTMLParser
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY = (15, 26, 74); PERI = (143, 163, 255); WHITE = (255, 255, 255)
M = 64                # the margin
TEXT_W = W - 2 * M    # the headline's measure
VERSION = 4           # bump to redraw every card after a change here (the cache key carries it)

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
CACHE = os.path.join(HERE, '.variants'); os.makedirs(CACHE, exist_ok=True)
FAMILY = {'display': 'host-grotesk-latin-wght.woff2', 'text': 'inter-latin-wght.woff2'}

HERO = ('cs-hero-media', 'blg-cover', 'hero-media', 'ab-banner')   # a page that opens on one picture
SCREEN = ('ws-screens', 'fr-screen', 'app-screen')                # a page that opens on the workspace itself
STRIP = ('m-tile', 'tv-slide', 'cs-media', 'svc-thumb', 'svc-strip', 'blg-feat-media', 'blg-media', 'flow-tile', 'ws-screens', 'fr-screen', 'hw-tiles')
VOID = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'track', 'wbr', 'area', 'base', 'col', 'embed', 'param'}

# ---- fonts: the site's variable woff2 files, unpacked to TrueType once (FreeType reads those) and instanced per weight and size
_ttf, _fonts = {}, {}
def _truetype(kind):
    if kind not in _ttf:
        src = os.path.join(FONTS, FAMILY[kind])
        with open(src, 'rb') as fh: digest = hashlib.md5(fh.read()).hexdigest()[:10]
        dst = os.path.join(CACHE, 'font-%s-%s.ttf' % (kind, digest))
        if not os.path.exists(dst):
            from fontTools.ttLib import TTFont
            f = TTFont(src); f.flavor = None; f.save(dst)
        _ttf[kind] = dst
    return _ttf[kind]

def font(kind, weight, size):
    key = (kind, weight, size)
    if key not in _fonts:
        f = ImageFont.truetype(_truetype(kind), size, layout_engine=ImageFont.Layout.RAQM)
        f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key]

# ---- text with tracking (letter-spacing), drawn glyph by glyph so the site's tight headlines keep their fit
def _kern(f, a, b):
    return f.getlength(a + b) - f.getlength(a) - f.getlength(b)

def text_width(f, text, tracking=0.0):
    return f.getlength(text) + tracking * max(0, len(text) - 1)

def draw_run(draw, x, y, text, f, fill, tracking=0.0):
    """draws text with its first glyph's origin at x and its baseline at y; returns the x after it"""
    prev = ''
    for ch in text:
        if prev: x += _kern(f, prev, ch)
        draw.text((x, y), ch, font=f, fill=fill, anchor='ls')
        x += f.getlength(ch) + tracking
        prev = ch
    return x - (tracking if text else 0)

def wrap(segments, f, tracking, max_w):
    """lines of (word, accent) from the headline's segments; a newline in a segment forces a break"""
    tokens = []
    for text, accent in segments:
        for i, part in enumerate(text.split('\n')):
            words = part.split()
            for j, w in enumerate(words):
                tokens.append((w, accent, i > 0 and j == 0))
    lines, line, width = [], [], 0.0
    space = f.getlength(' ') + tracking
    for w, accent, brk in tokens:
        ww = text_width(f, w, tracking)
        if line and (brk or width + space + ww > max_w):
            lines.append(line); line, width = [], 0.0
        if line: width += space
        line.append((w, accent)); width += ww
    if line: lines.append(line)
    return lines

def fit(segments, sizes, max_w, budget, kind='display', weight=700, track_em=-0.03, leading=1.06):
    """the largest size whose wrapped lines fit the height budget; the last size is cut to fit with an ellipsis"""
    for size in sizes:
        f = font(kind, weight, size); tracking = track_em * size
        lines = wrap(segments, f, tracking, max_w)
        lh = round(size * leading)
        if len(lines) * lh <= budget or size == sizes[-1]:
            n = max(1, int(budget // lh))
            if len(lines) > n:
                lines = lines[:n]
                w, a = lines[-1][-1]; lines[-1][-1] = (w.rstrip('.,;:') + '…', a)
            return f, tracking, lines, lh

def draw_lines(draw, x, y_top, lines, f, tracking, lh):
    """draws wrapped lines from their top; returns the y below them"""
    ascent = f.getmetrics()[0]
    space = f.getlength(' ') + tracking
    y = y_top + ascent + round((lh - (f.getmetrics()[0] + f.getmetrics()[1])) / 2)
    for line in lines:
        cx = x
        for i, (w, accent) in enumerate(line):
            if i: cx += space
            cx = draw_run(draw, cx, y, w, f, PERI if accent else WHITE, tracking)
        y += lh
    return y_top + len(lines) * lh

def draw_eyebrow(draw, x, y_top, text, size=19):
    f = font('text', 600, size); tracking = 0.09 * size
    draw_run(draw, x, y_top + f.getmetrics()[0], text.upper(), f, PERI, tracking)
    return y_top + round(size * 1.2)

# ---- what a page leads with
class _Scan(HTMLParser):
    """the page's eyebrow, its headline (as two-tone segments), its brand logo, and every picture with its surroundings"""
    def __init__(self):
        super().__init__()
        self.stack = []              # (classes, style) per open element
        self.eyebrow, self.h1, self.logo, self.imgs = None, None, None, []
        self._in_h1, self._in_eb, self._span = False, 0, []
    def _classes(self):
        return [c for cls, _ in self.stack for c in cls]
    def _focal(self, style):
        for s in [style] + [st for _, st in reversed(self.stack)]:
            m = re.search(r'(?:--focal|object-position)\s*:\s*([\d.]+)%\s+([\d.]+)%', s or '')
            if m: return float(m.group(1)) / 100, float(m.group(2)) / 100
        return None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get('class') or '').split(); style = a.get('style') or ''
        if tag == 'img':
            src = a.get('src') or ''
            if 'cs-logo' in cls:
                m = re.search(r'--lh\s*:\s*([\d.]+)px', style)
                self.logo = (src, float(m.group(1)) if m else 40.0)
            else:
                try: w, h = int(a.get('width') or 0), int(a.get('height') or 0)
                except ValueError: w, h = 0, 0
                self.imgs.append(dict(src=src, w=w, h=h, classes=self._classes(), focal=self._focal(style)))
            return
        if tag == 'video':
            poster = a.get('poster') or a.get('data-poster')
            if poster: self.imgs.append(dict(src=poster, w=0, h=0, classes=self._classes(), focal=self._focal(style)))
        if tag == 'h1' and self.h1 is None:
            self._in_h1 = True; self.h1 = []; self._span = []
        elif self._in_h1:
            if tag == 'br': self.h1.append(('\n', False))
            else:
                self._span.append(cls)
                if 'h1-l2' in cls: self.h1.append(('\n', False))
        if 'eyebrow' in cls and self.eyebrow is None and self.h1 is None:
            self._in_eb = len(self.stack) + 1; self.eyebrow = ''
        if tag not in VOID: self.stack.append((cls, style))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        if tag == 'h1' and self._in_h1: self._in_h1 = False
        elif self._in_h1 and self._span and tag not in VOID: self._span.pop()
        if tag not in VOID and self.stack:
            if self._in_eb and len(self.stack) == self._in_eb: self._in_eb = 0
            self.stack.pop()
    def handle_data(self, data):
        if self._in_h1: self.h1.append((data, any('ai' in c for c in self._span)))
        if self._in_eb: self.eyebrow += data

PLAIN = {'\u2011': '-', '\u00a0': ' ', '\u2009': ' ', '\u202f': ' ', '\u2060': ''}   # characters the latin subsets lack, as their plain forms

def scan(html):
    sc = _Scan(); sc.feed(html)
    segs = []
    for text, accent in sc.h1 or []:
        text = re.sub(r'[ \t\r\f\v]+', ' ', ''.join(PLAIN.get(ch, ch) for ch in text))
        if segs and segs[-1][1] == accent and text != '\n' and segs[-1][0] != '\n':
            segs[-1] = (segs[-1][0] + text, accent)
        elif text:
            segs.append((text, accent))
    h1, brk = [], False   # a forced break becomes a newline at the head of the segment that follows it
    for t, a in segs:
        if t == '\n': brk = True; continue
        if not t.strip(): continue
        if brk: t = '\n' + t.lstrip(); brk = False
        h1.append((t, a))
    eyebrow = re.sub(r'\s+', ' ', re.sub(r'\s*·\s*', ' · ', sc.eyebrow or '')).strip() or None
    return dict(h1=h1, eyebrow=eyebrow, logo=sc.logo, imgs=sc.imgs)

# ---- pictures
def _file(img_dir, src):
    """the file behind a page's /img/... address, or None"""
    name = src.split('/')[-1]
    p = os.path.join(img_dir, name)
    return p if name and os.path.exists(p) else None

def cover_crop(path, focal):
    """the picture filling the card, cropped to 1200×630 around its focal point"""
    im = Image.open(path).convert('RGB')
    iw, ih = im.size
    fx, fy = focal or (0.5, 0.5)
    scale = max(W / iw, H / ih)
    cw, ch = W / scale, H / scale
    left = min(max(fx * iw - cw / 2, 0), iw - cw); top = min(max(fy * ih - ch / 2, 0), ih - ch)
    return im.crop((round(left), round(top), round(left + cw), round(top + ch))).resize((W, H), Image.LANCZOS)

def gradient(im, stops):
    """the site's hero wash: navy from the top, lifting over the middle, heavy at the bottom (stops: (position, alpha))"""
    import numpy as np
    ys = np.arange(H) / (H - 1)
    pos = [p for p, _ in stops]; alp = [a for _, a in stops]
    alpha = np.interp(ys, pos, alp)[:, None, None]
    arr = np.asarray(im, dtype=np.float32)
    navy = np.array(NAVY, dtype=np.float32)[None, None, :]
    out = arr * (1 - alpha) + navy * alpha
    return Image.fromarray(out.round().astype('uint8'), 'RGB')

def rounded(tile, r=10):
    """an RGBA copy of the tile with rounded corners"""
    mask = Image.new('L', (tile.width * 2, tile.height * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, tile.width * 2 - 1, tile.height * 2 - 1), radius=r * 2, fill=255)
    out = tile.convert('RGBA'); out.putalpha(mask.resize(tile.size, Image.LANCZOS))
    return out

def silhouette(path, height):
    """a brand logo as a white shape at the given height (the site shows the black logos inverted on navy)"""
    if path.lower().endswith('.svg'):
        im = _raster_svg(path)
        if im is None: return None
    else:
        im = Image.open(path).convert('RGBA')
    bbox = im.getbbox()
    if not bbox: return None
    im = im.crop(bbox)
    alpha = im.getchannel('A')
    out = Image.new('RGBA', im.size, WHITE + (0,)); out.putalpha(alpha)
    w = max(1, round(im.width * height / im.height))
    return out.resize((w, height), Image.LANCZOS)

def _raster_svg(path, width=1600):
    """an SVG as a bitmap, drawn by the browser Playwright ships (the only SVG here is one brand logo)"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    import base64
    with open(path, 'rb') as fh: data = base64.b64encode(fh.read()).decode('ascii')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': width, 'height': 400}, device_scale_factor=1)
        pg.set_content('<html><body style="margin:0;background:transparent"><img id="l" src="data:image/svg+xml;base64,%s" style="display:block;width:%dpx"></body></html>' % (data, width))
        png = pg.locator('#l').screenshot(omit_background=True)
        b.close()
    return Image.open(io.BytesIO(png)).convert('RGBA')

# ---- the cards
def _wordmark(img_dir, card):
    for f in os.listdir(img_dir):
        if f.startswith('birdline-wordmark-white'):
            wm = Image.open(os.path.join(img_dir, f)).convert('RGBA')
            w = 192; wm = wm.resize((w, round(wm.height * w / wm.width)), Image.LANCZOS)
            card.alpha_composite(wm, (M, 54))
            return
    draw_run(ImageDraw.Draw(card), M, 54 + 40, 'Birdline', font('display', 800, 44), WHITE, -1.5)

def _photo(spec, img_dir):
    card = gradient(cover_crop(spec['image'], spec.get('focal')), [(0, .42), (.28, .18), (.6, .58), (1, .95)]).convert('RGBA')
    _wordmark(img_dir, card)
    draw = ImageDraw.Draw(card)
    f, tracking, lines, lh = fit(spec['h1'], [72, 64, 56, 48], TEXT_W, 3 * round(72 * 1.06))
    logo = silhouette(spec['logo'][0], round(spec['logo'][1] * 1.1)) if spec.get('logo') else None
    block = len(lines) * lh + (23 + 14 if spec.get('eyebrow') else 0) + (logo.height + 22 if logo else 0)
    y = H - M - block
    if spec.get('eyebrow'): y = draw_eyebrow(draw, M, y, spec['eyebrow']) + 14
    if logo: card.alpha_composite(logo, (M, y)); y += logo.height + 22
    draw_lines(draw, M, y, lines, f, tracking, lh)
    return card

def _strip(spec, img_dir):
    card = Image.new('RGBA', (W, H), NAVY + (255,))
    _wordmark(img_dir, card)
    draw = ImageDraw.Draw(card)
    th, gap = 168, 12
    strip_top = H - 52 - th
    _headline(draw, spec, 118, strip_top - 24)
    x = M
    for path in spec['tiles']:
        im = Image.open(path).convert('RGB')
        asp = min(max(im.width / im.height, 0.5625), 1.9)
        tw = round(th * asp)
        tile = cover_crop_to(im, tw, th)
        card.alpha_composite(rounded(tile), (x, strip_top))
        x += tw + gap
        if x >= W: break
    return card

def _headline(draw, spec, top, bottom, sizes=(64, 56, 48)):
    """the eyebrow and headline, centred between top and bottom"""
    eb = 23 + 14 if spec.get('eyebrow') else 0
    f, tracking, lines, lh = fit(spec['h1'], list(sizes), TEXT_W, bottom - top - eb)
    block = eb + len(lines) * lh
    y = top + max(0, (bottom - top - block) // 2)
    if spec.get('eyebrow'): y = draw_eyebrow(draw, M, y, spec['eyebrow']) + 14
    return draw_lines(draw, M, y, lines, f, tracking, lh)

def _screen(spec, img_dir):
    """a page about the workspace: the headline over the top of an app screen that runs off the bottom of the card"""
    card = Image.new('RGBA', (W, H), NAVY + (255,))
    _wordmark(img_dir, card)
    draw = ImageDraw.Draw(card)
    top = 352
    _headline(draw, spec, 118, top - 28)
    im = Image.open(spec['image']).convert('RGB')
    sw = W - 2 * M; im = im.resize((sw, round(im.height * sw / im.width)), Image.LANCZOS)
    im = im.crop((0, 0, sw, min(im.height, H - top + 20)))
    frame = Image.new('RGBA', (sw + 2, im.height + 2), (255, 255, 255, 40))
    frame.alpha_composite(rounded(im, 14), (1, 1))
    card.alpha_composite(rounded(frame, 15), (M - 1, top - 1))
    return card

def cover_crop_to(im, tw, th):
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    cw, ch = tw / scale, th / scale
    left = (iw - cw) / 2; top = (ih - ch) * 0.4
    return im.crop((round(left), round(top), round(left + cw), round(top + ch))).resize((tw, th), Image.LANCZOS)

def _plain(spec, img_dir):
    card = Image.new('RGBA', (W, H), NAVY + (255,))
    _wordmark(img_dir, card)
    draw = ImageDraw.Draw(card)
    f, tracking, lines, lh = fit(spec['h1'], [76, 64, 56], TEXT_W, 2 * round(76 * 1.06))
    desc = spec.get('description') and fit([(spec['description'], False)], [27, 24], TEXT_W - 80, 2 * round(27 * 1.4), kind='text', weight=500, track_em=0, leading=1.4)
    eb = 23 + 14 if spec.get('eyebrow') else 0
    block = eb + len(lines) * lh + ((26 + len(desc[2]) * desc[3]) if desc else 0)
    y = 118 + max(0, (H - M - 118 - block) // 2)
    if spec.get('eyebrow'): y = draw_eyebrow(draw, M, y, spec['eyebrow']) + 14
    y = draw_lines(draw, M, y, lines, f, tracking, lh) + 26
    if desc:
        f2, t2, lines2, lh2 = desc
        ascent = f2.getmetrics()[0]
        for line in lines2:
            draw_run(draw, M, y + ascent, ' '.join(w for w, _ in line), f2, (205, 212, 240), 0)
            y += lh2
    return card

def spec_for(route, doc, img_dir):
    """what the card shows, from the page's own content"""
    s = scan(doc['html'])
    h1 = s['h1'] or [(re.sub(r':\s*Birdline.*$', '', doc['title']), False)]
    spec = dict(route=route, h1=h1, eyebrow=s['eyebrow'], description=doc['description'])
    cands = [(i, _file(img_dir, i['src'])) for i in s['imgs']]
    cands = [(i, p) for i, p in cands if p and not re.search(r'(^|/)(logo2-|av-|cr-|int-|team-)', i['src']) and not p.lower().endswith('.svg')]
    hero = next(((i, p) for i, p in cands if any(c in HERO for c in i['classes']) and (i['w'] >= 600 or not i['w'])), None)
    if hero:
        spec.update(kind='photo', image=hero[1], focal=hero[0]['focal'])
        if route.startswith('/case-studies/'):
            spec['eyebrow'] = 'Case study'
            if s['logo'] and _file(img_dir, s['logo'][0]):
                spec['logo'] = (_file(img_dir, s['logo'][0]), s['logo'][1])
        return spec
    tiles, seen = [], set()
    for i, p in cands:
        if any(c in STRIP for c in i['classes']) and p not in seen and not re.search(r'-m\.(webp|png|jpe?g)$', p):
            if not tiles and any(c in SCREEN for c in i['classes']):
                spec.update(kind='screen', image=p); return spec
            seen.add(p); tiles.append(p)
        if len(tiles) >= 10: break
    if len(tiles) >= 3:
        spec.update(kind='strip', tiles=tiles)
    else:
        spec['kind'] = 'plain'
    return spec

def card(route, doc, img_dir, out_dir):
    """draws the page's card into out_dir (cached by its ingredients) and returns the file name"""
    spec = spec_for(route, doc, img_dir)
    name = 'home' if route == '/' else route.strip('/').replace('/', '-')
    files = [spec.get('image')] + spec.get('tiles', []) + ([spec['logo'][0]] if spec.get('logo') else [])
    h = hashlib.md5()
    h.update(json.dumps(dict(spec, image=None, tiles=None, logo=spec.get('logo') and spec['logo'][1]), sort_keys=True, default=str).encode())
    for p in files:
        if p:
            with open(p, 'rb') as fh: h.update(hashlib.md5(fh.read()).digest())
    for kind in FAMILY:
        with open(os.path.join(FONTS, FAMILY[kind]), 'rb') as fh: h.update(hashlib.md5(fh.read()).digest())
    h.update(str(VERSION).encode())
    cached = os.path.join(CACHE, 'og-%s.jpg' % h.hexdigest())
    dst = os.path.join(out_dir, name + '.jpg')
    if not os.path.exists(cached):
        im = {'photo': _photo, 'strip': _strip, 'screen': _screen, 'plain': _plain}[spec['kind']](spec, img_dir).convert('RGB')
        im.save(cached, 'JPEG', quality=86, optimize=True, progressive=True)
    shutil.copyfile(cached, dst)
    return name + '.jpg', spec['kind']

if __name__ == '__main__':
    # a look at the cards for the pages the Next.js project holds now: python3 og.py <next project> <out dir>
    import sys
    nxt, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    img_dir = os.path.join(nxt, 'public', 'img')
    for e in json.load(open(os.path.join(nxt, 'content', 'pages.json'))):
        with open(os.path.join(nxt, 'content', 'pages', e['file']), encoding='utf-8') as fh:
            doc = dict(title=e['title'], description=e['description'], html=fh.read())
        name, kind = card(e['route'], doc, img_dir, out)
        print('%-6s %s' % (kind, name))
