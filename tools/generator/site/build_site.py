"""Builds the Birdline site as a folder: the homepage (from ../body.html), the Work page, the Case Studies page and the nine case-study
pages, sharing ../style.css + site.css, ../script.js + site.js, the header and footer from ../body.html, and one img/ folder.
Usage: python3 build_site.py <homepage assets dir> <out dir>
Writes <out>/index.html, portfolio.html, case-studies.html, case-studies/<slug>.html, img/*, plus index-artifact.html (the homepage
without the document skeleton, for publishing)."""
import hashlib, html as H, json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from extras import FALLBACK, WR_CASE, EDJY_CASE, UFL_CASE, ADDED_WORK, AI_WORK, NO_CASE_WORK, ORDER, CARDS, LOGOS, PAGES, HEADSHOTS, WE_CREATE, PHOTO_BRANDS, PACKAGES, WORKFLOW, WORKFLOW_WIDE, PRODUCTION_TYPES, PILLARS, TEAM, WITHOUT, WITH, DELIVER, COLLAB, FAQ_PACKAGES, FAQ_EXTRA, LOOP, FEATURES, AROUND, FAQ_APP, WS_SCREENS, WS_SIZES, FLOATERS, HERO_TILES
from services import SERVICES, GROUPS
from rops import HERO as RP_HERO, FORMULAS, COMPARE, QUESTION, QUESTION_SUB, TELLS, STORY_STATS, STORY_LEDE, STORY_THEN, STORY_LESSON, MEASURE, DIY, NUMBERS, NUMBERS_NOTE, FAQ as RP_FAQ
from production import HERO as PD_HERO, ANYWHERE_H2, ANYWHERE_SUB, PLACES, ANYWHERE, PROCESS_SUB, PROCESS, ADDON
import how as HW
from why import HERO_LEDE, REASONS, REASONS_LINE, LIBRARY_INTRO, PRODUCTIONS, CAMPAIGNS, MONTHS, LIBRARY_STATS, LIBRARY_STATEMENT, ROPS_INTRO, METRICS, PROOF, PROOF_NOTE, APP_SUB, APP_CHAIN, APP_TAIL

ASSETS, OUT = sys.argv[1], sys.argv[2]
GIF = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
EXTS = ['.webp', '.svg', '.png', '.jpg', '.jpeg']
content = json.load(open(os.path.join(HERE, 'content.json')))
content['cases']['willies-remedy'] = WR_CASE  # the case Mike drafted on November 1, 2026, not on the live site yet
content['cases']['edjy'] = EDJY_CASE
content['cases']['ufl'] = UFL_CASE
content['cases']['patrol']['copy']['results'] = [
    ('Brand Commercials', 'We launched two high-quality, narrative-driven brand spots titled “When Seconds Matter” and “Private Patrol” that position Patrol as a game-changing tool for community safety.'),
    ('UGC Campaigns', 'We scripted, shot, and edited multiple user-generated-style videos. Our UGC pieces were designed to feel authentic and relatable, featuring real families, natural settings, and direct-to-camera storytelling.'),
    ('Social Content & Paid Ads', 'We created numerous short-form assets for Instagram and Meta, pulling from both our brand commercials and UGC campaigns. Our Private Patrol spot on X alone generated 12M views, 4K reposts, 8K likes, 3K saves, and 1.5K comments. All in one week.'),
]
imap = json.load(open(os.path.join(HERE, 'img_map.json')))

# ---- the self-hosted video library (November 3, 2026): Mike downloaded every Vimeo original and sorted them into client folders;
# video_index.tsv lists the web transcodes (id | folder | source file | width | height | seconds | bytes). A Vimeo id in the content
# that has a row here plays from video/<id>.mp4; the folders decide which videos each case study shows.
VIDEO_INDEX = {}
_vi = os.path.join(HERE, 'video_index.tsv')
if os.path.exists(_vi):
    for _line in open(_vi, encoding='utf-8'):
        _p = _line.rstrip('\n').split('|')
        if len(_p) >= 7 and _p[0].isdigit():
            VIDEO_INDEX[_p[0]] = dict(folder=_p[1], file=_p[0] + '.mp4', w=int(_p[3]), h=int(_p[4]), dur=float(_p[5]), bytes=int(_p[6]),
                                      title=re.sub(r'^\d+\s*-\s*', '', os.path.splitext(_p[2])[0]))
FOLDER_SLUG = {'686': '686', 'FreePower': 'freepower', 'Gardyn': 'gardyn', 'Literati': 'literati', 'Patrol': 'patrol', 'Public Rec': 'public-rec',
               'Route': 'route', 'Solidroad': 'solidroad', 'WHOOP': 'whoop'}
FOLDER_FIX = {'927324603': 'gardyn'}  # the Gardyn 4.0 starter-pack ad sat in the FreePower folder; it stays with Gardyn
DROPPED_VIDEOS = {'1109212937'}  # the rough sneak-peek intro animation: off the Gardyn case study and the Work page (November 9, 2026)
HOSTED_LABELS = {'1112070841': 'FX, CEO at Gardyn', '1215871520': '360 Product Story · Solidroad'}  # labels for library videos the content has no name for
EXTRA_FOLDERS = {'commercial': 'Additional Commercial Work', 'animation': 'Additional Animation Work', 'profiles': 'Additional Profile Work'}

def vimeo_id(it):
    m = re.search(r'vimeo\.com/(\d+)', (it or {}).get('href', '') or '')
    return m.group(1) if m else None

# every still the content has for a video, by id (the posters and the Work-page tiles come from these). The live site linked a
# couple of stills to the wrong video, so where an id has several stills the one whose brand matches the video wins.
_VIDEO_CANDS = {}
for _pane in content['portfolio']['panes']:
    for _it in _pane['items']:
        _v = vimeo_id(_it)
        if _v and 'src' in _it: _VIDEO_CANDS.setdefault(_v, []).append(_it)
for _slug, _cs in content['cases'].items():
    for _it in _cs.get('gal', []):
        _v = vimeo_id(_it)
        if _v and 'src' in _it: _VIDEO_CANDS.setdefault(_v, []).append(dict(_it, alt=_it.get('alt') or CARDS[_slug]['brand']))
def _best_still(vid, cands):
    if len(cands) == 1: return cands[0]
    info = VIDEO_INDEX.get(vid); words = []
    if info:
        slug = FOLDER_FIX.get(vid) or FOLDER_SLUG.get(info['folder'])
        if slug: words.append(CARDS[slug]['brand'].lower())
        words += re.findall(r'[a-z]{3,}', info['title'].lower())
    for it in cands:
        alt = (it.get('alt') or '').lower()
        if alt and any(alt in w or w in alt for w in words): return it
    return cands[0]
VIDEO_ITEMS = {vid: _best_still(vid, cands) for vid, cands in _VIDEO_CANDS.items()}
if VIDEO_INDEX:
    _by_slug = {}
    for _v, _info in VIDEO_INDEX.items():
        _s = FOLDER_FIX.get(_v) or FOLDER_SLUG.get(_info['folder'])
        if _s: _by_slug.setdefault(_s, []).append(_v)
    for _slug in FOLDER_SLUG.values():
        _cs = content['cases'][_slug]; _keep = set(_by_slug.get(_slug, [])); _seen = set(); _new = []
        for _it in _cs.get('gal', []):
            _v = vimeo_id(_it)
            if not _v: _new.append(_it)                      # photographs stay
            elif _v in DROPPED_VIDEOS: continue
            elif _v in _keep and _v not in _seen: _new.append(dict(_it, alt=HOSTED_LABELS.get(_v) or _it.get('alt') or CARDS[_slug]['brand'])); _seen.add(_v)
        for _v in _by_slug.get(_slug, []):                   # videos Mike added to the client's folder
            if _v in _seen or _v not in VIDEO_ITEMS or _v in DROPPED_VIDEOS: continue
            _new.append(dict(VIDEO_ITEMS[_v], alt=HOSTED_LABELS.get(_v) or VIDEO_ITEMS[_v].get('alt') or CARDS[_slug]['brand'])); _seen.add(_v)
        _cs['gal'] = _new

for _slug, _items in ADDED_WORK.items():  # the videos Mike sent for a case study, newest first
    content['cases'][_slug]['gal'] = list(_items) + content['cases'][_slug].get('gal', [])
# pieces Mike wants lower in a case study's gallery: (slug, file) -> the position they move to (November 9, 2026)
GAL_MOVE = {('freepower', 'freepower-partnership-overview.mp4'): 9}
for (_slug, _file), _at in GAL_MOVE.items():
    _gal = content['cases'][_slug]['gal']
    _i = next((i for i, it in enumerate(_gal) if it.get('video') == _file), None)
    if _i is not None: _gal.insert(min(_at, len(_gal) - 1), _gal.pop(_i))

def hosted(vid):
    """the self-hosted file for a Vimeo id, or None"""
    return VIDEO_INDEX.get(str(vid)) if vid else None

def vid_fallback(file):
    """the attribute naming the file to try when the web encode is not in the store yet: the original, under the name it was uploaded with"""
    orig = FALLBACK.get(file)
    if not orig:
        return ''
    from urllib.parse import quote
    return ' data-fallback="{{ROOT}}video/%s"' % quote(orig, safe="-_.!~*'()")

def play_attrs(vid, title, poster_file=None, file=None, w=None, h=None):
    """the attributes of a link that plays a video in the lightbox: a self-hosted file (file, w, h), a Vimeo id with a hosted
    transcode (from video/), or, failing both, Vimeo's player"""
    v = hosted(vid) if vid else None
    if file:
        v = dict(file=file, w=w, h=h)
    if v:
        site_videos.add(v['file'])
        return ('href="{{ROOT}}video/%s" data-lb="video" data-src="{{ROOT}}video/%s"%s data-asp="%.4f" data-title="%s" data-kind="Video"%s target="_blank"'
                % (v['file'], v['file'], vid_fallback(v['file']), v['w'] / v['h'], esc(title), (' data-poster="{{ROOT}}img/%s"' % poster_file) if poster_file else ''))
    return 'href="https://vimeo.com/%s" data-lb="video" data-vimeo="%s" data-title="%s" data-kind="Video" target="_blank" rel="noopener"' % (vid, vid, esc(title))

style = open(os.path.join(ROOT, 'style.css'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'site.css'), encoding='utf-8').read()
script = open(os.path.join(ROOT, 'script.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'site.js'), encoding='utf-8').read()
body = open(os.path.join(ROOT, 'body.html'), encoding='utf-8').read().replace('{{GIF}}', GIF)

os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'case-studies'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'services'), exist_ok=True)

# ---- images: the homepage assets go in by key name; the images pulled from birdlinestudios.com by their file name
asset_ext = {}
def asset(key):
    """copies a homepage asset into img/ and returns its file name"""
    if key not in asset_ext:
        for ext in EXTS:
            p = os.path.join(ASSETS, key + ext)
            if os.path.exists(p):
                shutil.copyfile(p, os.path.join(OUT, 'img', key + ext))
                asset_ext[key] = ext
                break
        else:
            raise SystemExit('missing asset ' + key)
    return key + asset_ext[key]

site_imgs = set()
site_videos = set()  # self-hosted mp4s (site/video/), copied into out/video/ when a tile points at one
_img_alias, _img_hash = {}, {}  # a live-site image that is byte-for-byte another one goes out once, under the first name
def site_img(orig):
    """an image from the live site: returns (file, w, h)"""
    f = imap[orig]
    if f['file'] not in _img_alias:
        src = os.path.join(HERE, 'img', f['file'])
        with open(src, 'rb') as fh: digest = hashlib.md5(fh.read()).hexdigest()
        if digest in _img_hash:
            _img_alias[f['file']] = _img_hash[digest]
        else:
            shutil.copyfile(src, os.path.join(OUT, 'img', f['file']))
            _img_hash[digest] = _img_alias[f['file']] = f['file']
            site_imgs.add(f['file'])
    return _img_alias[f['file']], f['w'], f['h']

def resolve_imgs(html):
    """<img src=GIF data-img=key> -> a plain src into img/ (the file name; the page's root prefix is added by relink)"""
    return re.sub(r'src="[^"]*" data-img="([^"]+)"', lambda m: 'src="{{ROOT}}img/%s"' % asset(m.group(1)), html)

# ---- links between the pages
def relink(html, root, on_home, hashes=False, local_ids=(), clean=False):
    """points the Work, Case Studies, case-study, Packages, About, app and services links at the new pages; with hashes=True (the artifact,
    one document) at #work, #case-studies, #cs-<slug>, #all-services, #svc-<slug> and so on; with clean=True (the Next.js site) at the
    data-page value itself: /work, /case-studies/<slug>, /services/<slug>, with root '/' so an anchor on a sub-page becomes /#place.
    On a sub-page an anchor stays as it is when the page has that id (its own #plans or #faq); any other anchor is a place on the homepage"""
    def fix(m):
        tag = m.group(0)
        href = re.search(r'\shref="([^"]*)"', tag)
        page = re.search(r'\sdata-page="([^"]*)"', tag)
        if not href:
            return tag
        h, p = href.group(1), page.group(1) if page else ''
        p, _, frag = p.partition('#')   # a place on the page (/work#tv-photo) is kept on the site; the artifact's router shows the page
        new = None
        if clean and p:
            new = p
        elif p == '/work':
            new = '#work' if hashes else root + 'portfolio.html'
        elif p == '/case-studies':
            new = '#case-studies' if hashes else root + 'case-studies.html'
        elif p.startswith('/case-studies/'):
            new = ('#cs-' + p.split('/')[-1]) if hashes else root + 'case-studies/' + p.split('/')[-1] + '.html'
        elif p == '/packages':
            new = '#packages' if hashes else root + 'packages.html'
        elif p == '/about':
            new = '#about' if hashes else root + 'about.html'
        elif p == '/production-workspace':
            new = '#workspace' if hashes else root + 'workspace.html'
        elif p == '/services':
            new = '#all-services' if hashes else root + 'services.html'
        elif p == '/why-us':
            new = '#why-us' if hashes else root + 'why-us.html'
        elif p == '/rops':
            new = '#rops' if hashes else root + 'rops.html'
        elif p == '/how-it-works':
            new = '#how-it-works' if hashes else root + 'how-it-works.html'
        elif p.startswith('/services/'):
            new = ('#svc-' + p.split('/')[-1]) if hashes else root + 'services/' + p.split('/')[-1] + '.html'
        elif h.startswith('#') and not on_home and not (h[1:] in local_ids and h != '#top'):
            new = root + ('' if clean else 'index.html') + ('' if h == '#top' else h)
        if new is None:
            return tag
        if frag and not hashes:
            new += '#' + frag
        return tag.replace(href.group(0), ' href="%s"' % new, 1)
    html = re.sub(r'<a\b[^>]*>', fix, html)
    if clean:  # links written straight to a file ({{ROOT}}packages.html, {{ROOT}}case-studies/ufl.html) become routes too
        html = re.sub(r'\{\{ROOT\}\}((?:case-studies|services)/[a-z0-9-]+|[a-z0-9-]+)\.html', lambda m: route_for(m.group(1) + '.html'), html)
    # the booking buttons: the Calendly link, and data-book so script.js opens the modal instead
    html = re.sub(r'<a\b([^>]*?)href="\{\{CALENDLY\}\}"(?![^>]*\bdata-book\b)', r'<a\1href="{{CALENDLY}}" data-book', html)
    return html.replace('{{ROOT}}', root).replace('{{CALENDLY}}', CALENDLY)

def route_for(name):
    """the Next.js route of a page file: index.html -> /, portfolio.html -> /work, case-studies/ufl.html -> /case-studies/ufl"""
    if name == 'index.html': return '/'
    if name == 'portfolio.html': return '/work'
    if name == 'workspace.html': return '/production-workspace'
    return '/' + name[:-len('.html')]

# ---- fragments from the homepage
header = body[body.index('<span class="top-mark"'):body.index('</header>') + len('</header>')]
footer = body[body.index('<footer'):body.index('</footer>') + len('</footer>')]
tm_start = body.index('<section class="band testimonials"')
testimonials = body[tm_start:body.index('</section>', tm_start) + len('</section>')]
testimonials = re.sub(r'\s*<div class="wrap">\s*<div class="more">.*?</div>\s*</div>\s*(?=</section>)', '\n', testimonials, flags=re.S)
lg_start = body.index('<section class="logos"')
logos_band = body[lg_start:body.index('</section>', lg_start) + len('</section>')]
faq_items = dict(re.findall(r'(<details class="qa"[^>]*>\s*<summary>(.*?)<span class="qa-ic".*?</details>)', body, flags=re.S)[i][::-1] for i in range(len(re.findall(r'<details class="qa"', body))))
for _q, _a in FAQ_EXTRA.items():   # the questions only some pages ask, in the same shape as the home page's
    faq_items[_q] = '<details class="qa" name="faq">\n        <summary>%s<span class="qa-ic" aria-hidden="true"></span></summary>\n        <div class="qa-a">%s</div>\n      </details>' % (H.escape(_q, quote=False), H.escape(_a, quote=False))
why_start = body.index('<section class="band band--navy on-dark why"')
matrix_band = resolve_imgs(body[why_start:body.index('</section>', why_start) + len('</section>')])
calc_start = body.index('<section class="band band--navy on-dark calc"')
calc_band = body[calc_start:body.index('</section>', calc_start) + len('</section>')]
works_start = body.index('<div class="works"')
works_block = resolve_imgs(body[works_start:body.index('<div class="cta-row product-cta">')])
lib_start = body.index('<ul class="lib-tiles"')
lib_tiles = resolve_imgs(body[lib_start:body.index('</ul>', lib_start) + len('</ul>')])
# the Packages hero: the homepage's fourteen library tiles plus twenty-four more pieces from the case studies and the services pages, so
# the columns show the range of the work (TV, paid social, photography, UGC, 3D, motion, design, CTV, profiles, podcasts, illustration,
# film, OOH, events, AI). Each column is one list, top to bottom; the brand goes in the label where it is known.
FLOW_COLUMNS = [
    [('2024/05/HD-Expo-FreePower-Recap.jpg', 'FreePower · Event recap'), ('2024/05/maxresdefault_11zon.webp', 'Public Rec · TV spot'), ('2024/05/Gardyn_7_29_2025_Kitchen_77886.jpeg', 'Gardyn · Photography'),
     ('2024/05/thumb-20-1.jpg', 'Gardyn · Motion graphics'), ('2024/05/Gardyn-Unboxing-1.jpg', 'Gardyn · UGC'), ('2024/05/Protect-Static-v2.jpg', 'Route · Static ad'),
     ('2024/06/Logan-Hollowell-X-Route.jpg', 'Route · Profile video'), ('2026/08/thumb-63.jpg', 'WHOOP · UGC'), ('2024/05/Affirm-Pricing-1x1-v2-1.jpeg', 'Gardyn · Design'),
     ('2026/08/thumb-51.jpg', 'Solidroad · Video podcast')],
    [('2025/06/Screenshot-2025-06-20-at-9.49.44-PM.jpeg', 'Patrol · Commercial'), ('2025/08/GrantPuckett-Product-36.jpeg', 'Product photography'), ('2026/08/thumb-57.jpg', 'WHOOP · Motion graphics'),
     ('2025/09/thumb-27.jpg', 'Literati · Animation'), ('2024/05/thumb-6-4.jpg', 'FreePower · Product demo'), ('2024/05/686-EP.jpg', '686 · Paid social'),
     ('2024/05/Gardyn-Growing-Symphony-3.jpg', 'Gardyn · Brand film'), ('2024/05/IMG_8421.jpg', 'Route · OOH'), ('wr/wr-3d-bottle.jpg', 'Willie’s Remedy · 3D'), ('2026/08/thumb-56.jpg', 'WHOOP · Long-form')],
    [('2024/05/thumb-15-2.jpg', 'Gardyn · CTV spot'), ('2024/06/GrantPuckett-Active-4.jpeg', 'Lifestyle photography'), ('2024/05/LBF-F25043_SocialPost_BookFairAnnouncement_English_2X-2.png', 'Literati · Illustration'),
     ('2025/08/GrantPuckett-Product.jpeg', 'Product photography'), ('2024/06/686-Outerwear-Drop-2023.jpg', '686 · Social'), ('2024/06/686-WINTER-Goggles-Color-Grid.jpg', '686 · Social'),
     ('2024/05/thumb-19.jpg', 'Public Rec · Paid social'), ('2024/06/Route-22In-The-Studio22-with-Elwood.jpg', 'Route · Profile video'),
     ('new/ai-freepower-countertop-16x9.jpg', 'FreePower · AI content'), ('2024/05/thumb-21-1.jpg', 'Humiint · Animation')],
    [('2026/08/thumb-54.jpg', 'WHOOP · Paid social'), ('2024/05/Gardyn-Summer.jpg', 'Gardyn · Hero spot'), ('2025/08/GrantPuckett-Studio-Product.jpeg', 'Studio photography'), ('2024/05/thumb-2-1.jpg', 'Route · 3D / CGI'),
     ('2026/08/thumb-53.jpg', 'WHOOP · VFX'), ('2024/06/IMG1803-R01-012-scaled-1.jpg', 'Shot on film'), ('2024/05/thumb-14-1.jpg', 'Gardyn · Paid social'), ('2025/09/PublicRec-DTLA-DD-33.jpeg', 'Public Rec · Photography')],
]

# ---- the homepage's library tiles (November 3, 2026): fourteen Work-page pieces at their own proportions, one per service, laid
# out as before; each (x, y, width in % of the stage, tilt, delay, source, label)
LIB_TILES = [
    (1, 4, 15, '-4deg', '0s', '2024/05/HD-Expo-FreePower-Recap.jpg', 'OOH'),
    (18.5, 2, 7.5, '3deg', '0.08s', '2024/05/Gardyn-Unboxing-1.jpg', 'UGC'),
    (41, 2, 16, '-2deg', '0.16s', '2024/05/thumb-32.jpg', 'CTV'),
    (73, 4, 17, '3deg', '0.24s', '2024/05/thumb-18-2.jpg', 'Commercial'),
    (3, 29, 10, '2deg', '0.32s', '2025/08/GrantPuckett-Product-36.jpeg', 'Photography'),
    (16, 42, 10, '-5deg', '0.4s', '2026/08/thumb-57.jpg', 'Motion Graphics'),
    (73.5, 31, 11, '5deg', '0.48s', '2024/05/LBF-F25043_SocialPost_BookFairAnnouncement_English_2X-2.png', 'Design'),
    (88.5, 25, 7.5, '-4deg', '0.56s', 'wr/wr-3d-bottle.jpg', '3D / VFX'),
    (3, 64, 8.5, '-3deg', '0.64s', '2024/05/thumb-19.jpg', 'Paid Social'),
    (14.5, 79, 15.5, '4deg', '0.72s', '2025/09/thumb-27.jpg', 'Illustrations'),
    (71.5, 58, 15.5, '-3deg', '0.8s', '2026/08/thumb-56.jpg', 'Profiles'),
    (89, 52, 8.5, '2deg', '0.88s', '2026/08/thumb-62.jpg', 'Video Podcasts'),
    (76, 79, 8, '3deg', '0.96s', '2024/06/IMG1803-R01-012-scaled-1.jpg', 'Film'),
    (43, 81, 16, '3deg', '1.04s', 'ai/gardyn-living-room-2.jpg', 'AI Content'),
]
def lib_tiles_html():
    out = []
    for x, y, w, r, d, src, label in LIB_TILES:
        f, iw, ih = site_img(src)
        out.append('<li class="lib-tile" style="--x:%s;--y:%s;--w:%s;--r:%s;--d:%s"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy"><span>%s</span></li>'
                   % (x, y, w, r, d, f, iw, ih, esc(label + ' — a piece from the content library'), esc(label)))
    return ('<ul class="lib-tiles" aria-label="Work from client content libraries: OOH, UGC, CTV, commercials, photography, motion graphics, design, 3D, paid social, illustration, profiles, video podcasts, film and AI content">\n        '
            + '\n        '.join(out) + '\n      </ul>')

def flow_tiles():
    """the Packages hero's tiles as four columns of (img tag, label) pairs, each a piece from the Work page by its source path"""
    cols = []
    for col in FLOW_COLUMNS:
        out = []
        for src, label in col:
            f, w, h = site_img(src)
            out.append(('<img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s">' % (f, w, h, esc(label)), esc(label)))
        cols.append(out)
    return cols

def flow_column(tiles, direction, dur, delay):
    """one flowing column: the set twice, so the track can slide by one set and loop"""
    items = ''.join('<li class="flow-tile">%s<span>%s</span></li>' % (img, label) for img, label in tiles)
    return ('<div class="flow-col flow-col--%s" style="--dur:%s;--delay:%s"><ul class="flow-set">%s</ul><ul class="flow-set" aria-hidden="true">%s</ul></div>'
            % (direction, dur, delay, items, items))

def hero_tiles():
    """the homepage's library tiles with the Packages hero's own positions"""
    def place(m):
        key = re.search(r'img/([^".]+)\.', m.group(0)).group(1)
        x, y, w, r, depth = HERO_TILES[key]
        tag = re.sub(r'style="[^"]*"', 'style="--x:%s;--y:%s;--w:%s;--r:%s;--d:%s"' % (x, y, w, r, re.search(r'--d:([^;"]+)', m.group(0)).group(1)), m.group(0))
        return tag.replace('<li class="lib-tile"', '<li class="lib-tile lib-tile--%s"' % depth, 1)
    return re.sub(r'<li class="lib-tile"[^>]*>.*?</li>', place, lib_tiles, flags=re.S)
st_start = body.index('<ul class="stats-ed"')
stats_block = body[st_start:body.index('</ul>', st_start) + len('</ul>')]
header, footer, testimonials, logos_band = resolve_imgs(header), resolve_imgs(footer), resolve_imgs(testimonials), resolve_imgs(logos_band)

LIGHTBOX = '''<dialog class="lb" data-lb-dialog aria-label="Media viewer">
  <div class="lb-in">
    <div class="lb-top"><div class="lb-meta"><b data-lb-title></b><span><em data-lb-kind></em><i data-lb-count></i></span></div>
      <button class="lb-x" type="button" data-lb-close><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"></path></svg><span>Close</span></button></div>
    <div class="lb-stage"><button class="lb-nav lb-nav--prev" type="button" data-lb-prev aria-label="Previous"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"></path></svg></button>
      <div class="lb-frame" data-lb-body></div>
      <button class="lb-nav lb-nav--next" type="button" data-lb-next aria-label="Next"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"></path></svg></button></div>
    <div class="lb-rail" data-lb-rail role="list" aria-label="More in this gallery"></div>
  </div>
</dialog>'''
# ---- booking: every "Book a call" / "Book a demo" button carries the Calendly link (the no-script path) and data-book, which
# script.js turns into the modal below: the short form first (its details go to /api/book on the Next.js site, which emails
# them to the team), then Calendly inline, prefilled with the name and email.
CALENDLY = 'https://calendly.com/birdlinestudios/birdline-exploratory-call'
SIZES = ['1-10', '11-50', '51-200', '201-500', '501-1000', '1000+']
SOURCES = ['Referral', 'LinkedIn', 'Instagram or TikTok', 'Google search', 'Saw your work for a brand', 'Podcast or newsletter', 'An event', 'Other']
def options(items, prompt='Select…'):
    return '<option value="">%s</option>' % prompt + ''.join('<option>%s</option>' % x.replace('&', '&amp;') for x in items)
BOOK = '''<dialog class="book" data-book-dialog aria-labelledby="book-title">
  <div class="book-card">
    <button class="book-x" type="button" data-book-close aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"></path></svg></button>
    <div class="book-step" data-book-step="form">
      <span class="eyebrow">Book a call</span>
      <h2 class="book-h" id="book-title">Let’s Scale Your <span class="nowrap">Content Library.</span></h2>
      <form class="lead" data-lead data-book-form novalidate>
        <div class="lead-row">
          <label for="book-name">Full name *<input id="book-name" name="name" type="text" autocomplete="name" required></label>
          <label for="book-email">Work email *<input id="book-email" name="email" type="email" autocomplete="email" inputmode="email" required data-work-email></label>
        </div>
        <div class="lead-row">
          <label for="book-company">Company name *<input id="book-company" name="company" type="text" autocomplete="organization" required></label>
          <label for="book-size">Company size *<select id="book-size" name="size" required>%s</select></label>
        </div>
        <label for="book-source">How did you hear about Birdline?<select id="book-source" name="source" data-source>%s</select></label>
        <label class="book-other" for="book-source-other" hidden>Tell us more<input id="book-source-other" name="source_other" type="text" data-source-other></label>
        <label class="hp" aria-hidden="true">Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
        <button class="btn" type="submit">Pick a time</button>
        <p class="lead-msg" data-lead-msg aria-live="polite"></p>
      </form>
    </div>
    <div class="book-step" data-book-step="calendar" hidden>
      <span class="eyebrow">Pick a time</span>
      <h2 class="book-h">Thanks<span data-book-first></span>. Choose a time that suits you.</h2>
      <div class="book-cal"><iframe title="Book a time with Birdline" data-book-cal></iframe></div>
      <p class="book-fine">Calendar not showing? <a href="{{CALENDLY}}" target="_blank" rel="noopener" data-book-cal-link>Open it in a new tab</a>.</p>
    </div>
  </div>
</dialog>''' % (options(SIZES), options(SOURCES))
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"></path></svg>'
PAUSE = '<svg class="ic-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4.5h4.5v15H6zM13.5 4.5H18v15h-4.5z"></path></svg>'
ZOOM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7"></path></svg>'
ARROW_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"></path></svg>'
CHEV_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"></path></svg>'
CHEV_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"></path></svg>'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@600;700&amp;family=Inter:wght@400;500;600;700&amp;display=swap">')

def tt(s):
    """a two-tone heading, as on the About page: the part after the | marker goes periwinkle"""
    if '|' in s:
        a, b = s.split('|', 1)
        return '%s<span class="ai">%s</span>' % (esc(a), esc(b))
    return esc(s)

def plain(s):
    """a heading without its two-tone marker, for alt text, labels and titles"""
    return s.replace('|', '')

def esc(s):
    return H.escape(s, quote=True)

# ---- the Next.js site: with BIRDLINE_NEXT=<project folder> the pages also go out as fragments (the inner HTML of <main>, links as
# clean routes) under <project>/content/, with the header, footer and lightbox in content/chrome.json, the styles in app/globals.css,
# the scripts in public/js/birdline.js and the images and videos under public/. The app's layout and route files render them.
NEXT = os.environ.get('BIRDLINE_NEXT')
DOCS = []  # (title, description, inner html with clean links), one per page, in the order the pages are built

def document(title, description, inner, root, on_home=False, artifact=False):
    local_ids = set(re.findall(r'\sid="([^"]+)"', inner))
    if NEXT and not artifact:
        DOCS.append(dict(title=title, description=description, html=relink(inner, '/', on_home, local_ids=local_ids, clean=True)))
    page = '<div class="page">\n' + header + '\n<main>\n' + inner + '\n</main>\n' + footer + '\n' + LIGHTBOX + '\n' + BOOK + '\n</div>'
    page = relink(page, root, on_home, local_ids=local_ids)
    if artifact:
        return ('<title>%s</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n%s\n<style>\n%s</style>\n%s\n<script>\n%s</script>\n'
                % (esc(title), FONTS, style, page, script))
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n%s\n<style>\n%s</style>\n</head>\n<body>\n%s\n<script>\n%s</script>\n</body>\n</html>\n'
            % (esc(title), esc(description), FONTS, style, page, script))

# ---- pieces
def cover_loop(slug):
    """the short silent loop some covers carry (CARDS[slug]['loop'], an .mp4 beside the still in the assets): it plays over the still
    in the card and the still stays underneath for the no-motion and no-script cases. Served from img/ with the still, not from the
    video store"""
    c = CARDS[slug]
    if not c.get('loop'):
        return ''
    src = os.path.join(ASSETS, c['loop'])
    if not os.path.exists(os.path.join(OUT, 'img', c['loop'])):
        shutil.copyfile(src, os.path.join(OUT, 'img', c['loop']))
    site_imgs.add(c['loop'])
    return ('<video class="cover-loop" src="{{ROOT}}img/%s" poster="{{ROOT}}img/%s" width="960" height="540" autoplay muted loop playsinline '
            'disablepictureinpicture aria-hidden="true" tabindex="-1"></video>' % (c['loop'], asset(c['cover'])))

def cs_card(slug, light=False):
    c = CARDS[slug]
    return ('<li class="cs"><a href="{{ROOT}}case-studies/%s.html"><span class="cs-media"><img src="{{ROOT}}img/%s" width="960" height="540" alt="%s" loading="lazy">%s</span>'
            '<span class="cs-body"><b class="cs-brand">%s</b><span class="cs-stat">%s</span><span class="cs-tags">%s</span></span></a></li>'
            % (slug, asset(c['cover']), esc(c['alt']), cover_loop(slug), esc(c['brand']), esc(c['stat']), esc(c['tags'])))

def brand_of(src):
    low = src.lower()
    for key, name in PHOTO_BRANDS:
        if key in low:
            return name
    return ''

def shape_of(w, h):
    return 'wide' if w / h >= 1.3 else ('tall' if w / h <= 0.8 else 'square')

# Stills that stand in for the live site's, by Vimeo id: the site's still had other proportions than the video (a square card
# over a vertical or a wide film), so the tile is sized by the video and these frames, cut from the videos themselves, fill it
POSTERS = {
    '892462752': 'new/poster-686-hydra-thermagraph.jpg',               # 686 Hydra Thermagraph jacket, 9:16
    '750741312': 'new/poster-686-atp-trail-running.jpg',               # 686 ATP Collection, trail running, 16:9
    '1095192934': 'new/poster-patrol-like-nothing-ever-happened.jpg',  # Patrol, Like Nothing Ever Happened, 2.39:1
    '881956457': 'new/poster-686-goggles.jpg',                         # 686 Goggles, 9:16: a new cover (November 9, 2026)
    '753024501': 'new/poster-standard-self-care.jpg',                  # Standard Self Care, How to Use: a frame at the video's own 4:3
    '727138751': 'new/cover-publicrec-zero-short.jpg',                 # Public Rec, Zero Short: the cover Mike sent
}

def tile(item, kind):
    """a gallery tile. A self-hosted video (item['video']) is the video itself, muted, showing a frame from its first second and
    previewing on hover; a Vimeo video or a photo is its still from the live site. Each plays or opens in the lightbox."""
    if item.get('video'):
        site_videos.add(item['video'])
        w, h, label = item['w'], item['h'], item['alt']
        poster = ''
        if item.get('poster'):
            pf, _pw, _ph = site_img(item['poster'])
            poster = ' poster="{{ROOT}}img/%s"' % pf
        a = ('<a href="{{ROOT}}video/%s" data-lb="video" data-src="{{ROOT}}video/%s"%s data-shape="%s" data-asp="%.4f" data-title="%s" data-kind="Video" target="_blank" aria-label="%s">'
             % (item['video'], item['video'], vid_fallback(item['video']), shape_of(w, h), w / h, esc(label), esc('Play: ' + label)))
        media = ('<video src="{{ROOT}}video/%s%s"%s width="%d" height="%d" style="aspect-ratio:%d / %d"%s muted playsinline preload="metadata" loop disablepictureinpicture aria-hidden="true" tabindex="-1"></video>'
                 % (item['video'], '' if poster else '#t=0.8', vid_fallback(item['video']), w, h, w, h, poster))
        icon = '<span class="gi-play gi-play--play" aria-hidden="true">%s</span>' % PLAY
        return '<div class="gi gi--video" role="listitem" data-gkind="video">%s%s%s<span class="gi-label">%s</span></a></div>' % (a, media, icon, esc(label))
    f, w, h = site_img(item['src'])
    label = item['alt'] or brand_of(item['src'])
    m = re.match(r'https://vimeo\.com/(\d+)', item['href'])
    if m and hosted(m.group(1)):
        v = hosted(m.group(1)); site_videos.add(v['file']); vw, vh = v['w'], v['h']
        if m.group(1) in POSTERS:   # a frame of the video itself, where the live site's still had different proportions
            f, _, _ = site_img(POSTERS[m.group(1)])
        if not label and not re.search(r'_|\d+x\d+|\bv\d|\bV\d', v['title']): label = v['title']  # a readable Vimeo title, never a file name
        a = '<a %s aria-label="%s">' % (play_attrs(m.group(1), label or v['title'], f).replace('data-asp="', 'data-shape="%s" data-asp="' % shape_of(vw, vh), 1), esc('Play: ' + (label or v['title'])))
        media = ('<video src="{{ROOT}}video/%s" width="%d" height="%d" style="aspect-ratio:%d / %d" poster="{{ROOT}}img/%s" muted playsinline preload="metadata" loop disablepictureinpicture aria-hidden="true" tabindex="-1"></video>'
                 % (v['file'], vw, vh, vw, vh, f))
        icon = '<span class="gi-play gi-play--play" aria-hidden="true">%s</span>' % PLAY
        return '<div class="gi gi--video" role="listitem" data-gkind="video">%s%s%s<span class="gi-label">%s</span></a></div>' % (a, media, icon, esc(label or v['title']))
    if m:
        vid = m.group(1)
        alt = (label + ' — video still') if label else 'Video still'
        a = ('<a href="https://vimeo.com/%s" data-lb="video" data-vimeo="%s" data-shape="%s" data-asp="%.4f" data-title="%s" data-kind="Video" target="_blank" rel="noopener" aria-label="%s">'
             % (vid, vid, shape_of(w, h), w / h, esc(label or 'Video'), esc('Play: ' + label if label else 'Play video')))
        icon = '<span class="gi-play gi-play--play" aria-hidden="true">%s</span>' % PLAY
        gkind = 'video'
    else:
        what = 'Design' if kind == 'design' else 'Photograph'
        alt = (label + ' — ' + what.lower()) if label else what
        a = '<a href="{{ROOT}}img/%s" data-lb="image" data-title="%s" data-kind="%s" target="_blank" aria-label="%s">' % (f, esc(label or what), what, esc((label + ' at full size') if label else 'See at full size'))
        icon = '<span class="gi-play gi-play--zoom" aria-hidden="true">%s</span>' % ZOOM
        gkind = 'photo'
    lab = ('<span class="gi-label">%s</span>' % esc(label)) if label else ''
    return '<div class="gi" role="listitem" data-gkind="%s">%s<img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">%s%s</a></div>' % (gkind, a, f, w, h, esc(alt), icon, lab)

def close_section(second_label, second_href, heading='Let’s Build Your Content Library.',
                  sub='We’ll help you leverage your existing videos, photos, and designs, then scale your library with new productions and monthly deliverables.',
                  first=('Book a call', '{{CALENDLY}}'), note='', photo=None):
    """the close; with photo=(file, w, h) a photograph sits behind it under the navy"""
    media = ('<div class="close-media" aria-hidden="true"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" loading="lazy"></div>\n  ' % photo) if photo else ''
    return ('<section class="close close--simple%s on-dark" id="signup">\n  %s<div class="wrap"><div class="head"><span class="eyebrow">Get started</span>'
            '<h2 class="h2">%s</h2><p class="sub">%s</p>'
            '<div class="cta-row"><a class="btn btn--light" href="%s">%s</a><a class="btn btn--ghost" href="%s">%s</a></div>%s</div></div>\n</section>'
            % (' close--photo' if photo else '', media, esc(heading), esc(sub), first[1], esc(first[0]), second_href, second_label, ('<p class="note">%s</p>' % esc(note)) if note else ''))

# ---- the Work page
# ---- the Work page: laid out like a TV app. A featured hero with slides and a pill nav over it, then shelves that scroll sideways.
TV_FEATURED = [
    # (slide key, slug or None for the reel, eyebrow, title, tags, description, watch: vimeo id or None for the brand's first wide video)
    ('reel', None, 'Birdline · Showreel', 'Our |Bird’s Work', ['Video', 'Photo', 'Design & Animation'],
     'Our creators don’t just make content at scale, but work that makes an impact.', '1049385390'),
    # the case slides, in the order Mike changed them to (twice) on November 9, 2026
    ('patrol', 'patrol', 'Case study · Patrol', None, None, None, None),
    ('686', '686', 'Case study · 686', None, None, None, None),
    ('gardyn', 'gardyn', 'Case study · Gardyn', None, None, None, None),
    ('route', 'route', 'Case study · Route', None, None, None, None),
    ('public-rec', 'public-rec', 'Case study · Public Rec', None, None, None, None),
]
TV_BRAND_WORDS = [('public rec', 'public-rec'), ('route', 'route'), ('gardyn', 'gardyn'), ('freepower', 'freepower'), ('686', '686'),
                  ('patrol', 'patrol'), ('literati', 'literati'), ('solidroad', 'solidroad'), ('whoop', 'whoop')]

def tv_brand(label):
    low = label.lower()
    for word, slug in TV_BRAND_WORDS:
        if word in low:
            return slug
    return None

def tv_videos():
    """every video on the live Work page and in the case-study galleries, once each, in that order: dicts of src, asp, vid, label, slug"""
    out, seen = [], set()
    def add(it, label, slug):
        if 'href' not in it:
            return
        m = re.match(r'https://vimeo\.com/(\d+)', it['href'])
        if not m or m.group(1) in seen or m.group(1) in DROPPED_VIDEOS:
            return
        if m.group(1) in VIDEO_ITEMS and VIDEO_ITEMS[m.group(1)]['src'] != it['src']:
            return  # the live site linked this still to the wrong video; the right still comes with its own entry
        seen.add(m.group(1))
        if m.group(1) in POSTERS:   # a frame of the video itself, at its own proportions
            _f, _w, _h = site_img(POSTERS[m.group(1)])
            out.append(dict(src=POSTERS[m.group(1)], asp=_w / _h, vid=m.group(1), label=label, slug=slug)); return
        out.append(dict(src=it['src'], asp=float(it['asp']), vid=m.group(1), label=label, slug=slug))
    for it in content['portfolio']['panes'][0]['items']:
        label = it['alt'] or brand_of(it['src'])
        add(it, label, tv_brand(label) or tv_brand(it['src']))
    for slug in ORDER:
        for it in content['cases'][slug].get('gal', []):
            if it.get('video') and it.get('poster'):
                if it['video'] in seen: continue
                seen.add(it['video'])
                out.append(dict(src=it['poster'], asp=it['w'] / it['h'], vid=None, file=it['video'], w=it['w'], h=it['h'], label=it.get('alt') or CARDS[slug]['brand'], slug=slug, svc=it.get('svc')))
                continue
            add(it, it.get('alt') or CARDS[slug]['brand'], slug)
    for it in NO_CASE_WORK:   # the pieces with no case study of their own (November 8, 2026)
        if it['video'] not in seen:
            seen.add(it['video'])
            out.append(dict(src=it['poster'], asp=it['w'] / it['h'], vid=None, file=it['video'], w=it['w'], h=it['h'], label=it['alt'], slug=None, svc=it.get('svc')))
    for vid, info in VIDEO_INDEX.items():
        it = VIDEO_ITEMS.get(vid)
        if not it and ('web/%s.jpg' % vid) in imap:  # no still in the content: the frame pulled from the transcode stands in
            it = dict(src='web/%s.jpg' % vid, href='https://vimeo.com/' + vid, alt='', w=info['w'], h=info['h'], asp=info['w'] / info['h'])
        if it and vid not in seen:
            label = HOSTED_LABELS.get(vid) or it.get('alt') or brand_of(it['src']) or (info['title'] if not re.search(r'_|\d+x\d+', info['title']) else '')
            add(it, label or 'Birdline', FOLDER_FIX.get(vid) or FOLDER_SLUG.get(info['folder']) or tv_brand(label))
    return out

def folder_videos(folder, videos):
    """the videos of one of Mike's extra folders, as tv_videos() dicts, in the folder's own (name) order"""
    by_vid = {v['vid']: v for v in videos}
    ids = sorted((vid for vid, info in VIDEO_INDEX.items() if info['folder'] == folder), key=lambda vid: VIDEO_INDEX[vid]['title'].lower())
    return [by_vid[vid] for vid in ids if vid in by_vid]

# the service a Work-page tile is filed under: the first service page that shows the piece, in this order
SVC_PRIORITY = ['commercial', 'profiles', 'ugc', 'video-podcasts', 'motion-graphics', '3d-vfx', 'illustration', 'design', 'ctv', 'film', 'paid-social']
SVC_NAME = {s['slug']: s['name'] for s in SERVICES}
SVC_BY_SRC = {}
for _slug in SVC_PRIORITY:
    _s = next((x for x in SERVICES if x['slug'] == _slug), None)
    if not _s: continue
    for _ref in _s.get('hero', []) + _s.get('gallery', []):
        if isinstance(_ref, str): SVC_BY_SRC.setdefault(_ref, SVC_NAME[_slug])
TAG_SVC = {'Commercial': 'Commercial', 'TV': 'CTV', 'Paid social': 'Paid Social', 'UGC': 'UGC', 'Social': 'Paid Social', 'Animation': 'Motion Graphics', 'VFX': '3D / VFX',
           'Video': 'Film', 'YouTube': 'Film', '3D': '3D / VFX', 'Illustration': 'Illustrations', 'Design': 'Design', 'Photo': 'Photography', 'Production': 'Film'}
UGC_WORDS = re.compile(r'ugc|interview|reactions|mashup|testimonial|review|pov|unboxing|comment', re.I)

def service_for(v):
    """the service line under a Work-page video tile"""
    if v.get('svc'): return v['svc']  # a gallery item that names its service
    if v['src'] in SVC_BY_SRC and SVC_BY_SRC[v['src']] != 'Photography': return SVC_BY_SRC[v['src']]
    info = hosted(v['vid']) if v.get('vid') else None
    title = (info['title'] if info else '') + ' ' + (v.get('label') or '')
    shape = tv_shape(v['asp'])
    tags = CARDS[v['slug']]['tags'].split(' · ') if v.get('slug') in CARDS else []
    if info and info['folder'] == 'Additional Profile Work': return 'Profiles'
    if info and info['folder'] == 'Additional Animation Work': return 'Motion Graphics'
    if info and info['folder'] == 'Additional Commercial Work': return 'Commercial'
    if v.get('slug') == 'willies-remedy': return '3D / VFX' if '3D' in (v.get('label') or '') else 'Motion Graphics'
    if UGC_WORDS.search(title) and ('UGC' in tags or v.get('slug') == 'edjy'): return 'UGC'
    if shape == 'wide':
        for t in ('Commercial', 'Video', 'YouTube', 'TV', 'Paid social', 'Social'):
            if t in tags: return TAG_SVC[t]
        return 'Film'
    for t in ('Paid social', 'Social', 'UGC'):
        if t in tags: return TAG_SVC[t]
    return 'Paid Social'

# what each photograph on the Work page shows (by its position in the live site's photo pane)
PHOTO_KIND = ['Product', 'Lifestyle', 'Active', 'Product', 'Portrait', 'Event', 'Studio', 'Lifestyle', 'Lifestyle', 'Product', 'Lifestyle', 'Product', 'Product', 'Lifestyle', 'Active', 'Lifestyle',
              'Product', 'Lifestyle', 'Lifestyle', 'Lifestyle', 'Lifestyle', 'Studio', 'Lifestyle', 'Product', 'Lifestyle', 'Lifestyle', 'Portrait', 'Product', 'Studio', 'Lifestyle', 'Lifestyle',
              'Portrait', 'Product', 'Lifestyle', 'Lifestyle', 'Portrait', 'Product', 'Portrait', 'Lifestyle', 'Lifestyle', 'Lifestyle', 'Active', 'Product', 'Lifestyle', 'Portrait', 'Lifestyle',
              'Lifestyle', 'Active', 'Lifestyle', 'Lifestyle', 'Lifestyle', 'Lifestyle', 'Lifestyle']
PHOTO_KIND_BY_SRC = {it['src']: PHOTO_KIND[i] for i, it in enumerate(next(p for p in content['portfolio']['panes'] if p['id'] == 'photo')['items']) if i < len(PHOTO_KIND)}

def short_title(label):
    """a tile title without the ' · kind' suffix the galleries carry (the service line says what it is)"""
    return label.split(' · ')[0] if ' · ' in label else label

def tv_shape(asp):
    return 'wide' if asp >= 1.5 else ('tall' if asp <= 0.8 else 'square')

def tv_tile(v, sub, shape='wide'):
    """a video tile: a still that plays the video in the lightbox. shape is the tile: wide (16:9), tall (9:16) or film (the still's own
    proportions, in a row of one height)"""
    f, w, h = site_img(v['src'])
    style = (' style="--asp:%.3f"' % (w / h)) if shape == 'film' else ''
    media = '<img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">' % (f, w, h, esc(v['label'] + ' — video still'))
    return ('<li class="tv-tile tv-tile--%s"%s><a %s aria-label="%s">'
            '<span class="tv-media">%s<span class="tv-play" aria-hidden="true">%s</span></span><span class="tv-cap"><b>%s</b><span>%s</span></span></a></li>'
            % (shape, style, play_attrs(v['vid'], v['label'], f, file=v.get('file'), w=v.get('w'), h=v.get('h')), esc('Play: ' + v['label']), media, PLAY, esc(short_title(v['label'])), esc(sub or service_for(v))))

def tv_still_tile(item, kind):
    """a photo or a design, at its own proportions in a row of one height; it opens at full size"""
    f, w, h = site_img(item['src'])
    label = item['alt'] or brand_of(item['src'])
    what = 'Design' if kind == 'design' else 'Photograph'
    return ('<li class="tv-tile tv-tile--film" style="--asp:%s"><a href="{{ROOT}}img/%s" data-lb="image" target="_blank" aria-label="%s">'
            '<span class="tv-media"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"><span class="tv-play tv-play--zoom" aria-hidden="true">%s</span></span>'
            '<span class="tv-cap"><b>%s</b><span>%s</span></span></a></li>'
            % (('%.3f' % (w / h)), f, esc((label + ' at full size') if label else 'See at full size'), f, w, h, esc((label + ' — ' + what.lower()) if label else what), ZOOM,
               esc(PHOTO_KIND_BY_SRC.get(item['src'], 'Lifestyle') if kind == 'photo' else (label or 'Design')), esc('Photography' if kind == 'photo' else 'Design')))

def tv_shelf(key, heading, tiles, link=None, note=''):
    head_link = ('<a class="shelf-link" href="%s">%s</a>' % (link[1], esc(link[0]))) if link else ''
    return ('<section class="shelf" id="tv-%s" data-carousel aria-label="%s">\n'
            '  <div class="shelf-head"><div><h2>%s</h2>%s</div><div class="shelf-tools">%s<div class="car-nav"><button class="car-btn" type="button" data-carousel-prev aria-label="Scroll back">%s</button>'
            '<button class="car-btn" type="button" data-carousel-next aria-label="Scroll on">%s</button></div></div></div>\n'
            '  <ul class="shelf-track" data-carousel-track>\n%s\n  </ul>\n</section>'
            % (key, esc(heading), esc(heading), ('<p>%s</p>' % esc(note)) if note else '', head_link, CHEV_L, CHEV_R, '\n'.join(tiles)))

# Mike's edits to the Work page's shelves (November 9, 2026): what leaves a shelf, what leads it, what ends it, how it is
# ordered (a round-robin over brands or services, so no run of one brand opens a shelf) and how long it runs.
def vkey(v):
    return v.get('vid') or v.get('file')

def interleave(items, key_of):
    """one from each group in turn, the groups in order of first appearance"""
    groups, order = {}, []
    for it in items:
        k = key_of(it)
        if k not in groups:
            groups[k] = []; order.append(k)
        groups[k].append(it)
    out = []
    while any(groups[k] for k in order):
        for k in order:
            if groups[k]:
                out.append(groups[k].pop(0))
    return out

SHELF_EDITS = {
    'commercial': dict(remove={'876232748', '923557755', '916190740', '916190755'},   # 686 UNWORK, Gardyn 4.0 personas, the two 4:5 Bezel cuts
                       first=['640557935', 'ufl-nobull-what-no-can-do.mp4', 'commercial-chivas-nike-paisa-boys.mp4', 'commercial-nike-paisa-boys-mexico.mp4', '1119136322'],
                       last=['727974264']),                                            # Nestlé closes the shelf
    'profiles': dict(remove={'916190755'}, by='brand'),                                # Bezel
    'social': dict(remove={'1112070841', '686-wntr-goggles-color-jump.mp4'}, by='brand', limit=50),   # FX's testimonial
    'literati': dict(by='svc'),
    'public-rec': dict(keep_first=True, by='svc'),
    'willies-remedy': dict(by='svc'),
}

def edit_shelf(key, items):
    e = SHELF_EDITS.get(key)
    if not e:
        return items
    items = [v for v in items if vkey(v) not in e.get('remove', set())]
    head = []
    if e.get('keep_first') and items:
        head, items = items[:1], items[1:]
    by = e.get('by')
    if by == 'brand':
        items = interleave(items, lambda v: v.get('slug') or tv_brand(v.get('label') or '') or 'other')
    elif by == 'svc':
        items = interleave(items, service_for)
    first = [v for k in e.get('first', []) for v in items if vkey(v) == k]
    last = [v for k in e.get('last', []) for v in items if vkey(v) == k]
    rest = [v for v in items if v not in first and v not in last]
    items = head + first + rest + last
    if e.get('limit'):
        items = items[:e['limit']]
    return items

def portfolio_page():
    pf = content['portfolio']
    videos = tv_videos()
    by_slug = {}
    for v in videos:
        by_slug.setdefault(v['slug'], []).append(v)
    # the featured slides
    slides, dots = [], []
    for i, (key, slug, eyebrow, title, tags, desc, vid) in enumerate(TV_FEATURED):
        if slug:
            pg, c = PAGES[slug], CARDS[slug]
            title, tags, desc = pg['headline'], c['tags'].split(' · '), pg['lede']
            wide = [v for v in by_slug.get(slug, []) if tv_shape(v['asp']) == 'wide']
            vid = (wide or by_slug.get(slug, [{'vid': '1049385390'}]))[0]['vid']
            f, w, h = site_img(content['cases'][slug]['heroBg'])
            img = '<img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" %s>' % (f, w, h, 'fetchpriority="high"' if i == 0 else 'loading="lazy"')
            focal = pg.get('focal', '50% 40%')
            ctas = ('<a class="btn btn--light" %s aria-label="%s">%s Watch</a>'
                    '<a class="btn btn--ghost" href="{{ROOT}}case-studies/%s.html">Go to case study</a>' % (play_attrs(vid, c['brand']), esc('Play: ' + c['brand']), PLAY, slug))
        else:
            img = '<img src="{{ROOT}}img/%s" width="2200" height="1468" alt="" fetchpriority="high">' % asset('hero-moto')
            focal = '50% 45%'
            ctas = ('<a class="btn btn--light" %s aria-label="Play: the Birdline reel">%s Watch the reel</a>'
                    '<a class="btn btn--ghost" href="{{CALENDLY}}">Book a call</a>' % (play_attrs(vid, 'Birdline showreel'), PLAY))
        tag = 'h1' if i == 0 else 'h2'
        slides.append('<div class="tv-slide%s" data-ws-screen="%s" style="--focal:%s">%s<div class="wrap"><div class="tv-copy">'
                      '<span class="tv-eyebrow">%s</span><%s class="tv-title">%s</%s><ul class="tv-tags">%s</ul><p class="tv-desc">%s</p><div class="cta-row">%s</div></div></div></div>'
                      % (' is-on' if i == 0 else '', key, focal, img, esc(eyebrow), tag, tt(title), tag, ''.join('<li>%s</li>' % esc(t) for t in tags), esc(desc), ctas))
        dots.append('<button%s type="button" role="tab" aria-selected="%s" data-ws-tab="%s" aria-label="%s"></button>'
                    % (' class="is-on"' if i == 0 else '', 'true' if i == 0 else 'false', key, esc(plain(title))))
    pills = ''.join('<button%s type="button" data-tv-jump="%s">%s</button>' % (' class="is-on"' if i == 0 else '', target, esc(label))
                    for i, (label, target) in enumerate([('Featured', 'top'), ('Case Studies', 'tv-cases'), ('Commercial', 'tv-commercial'), ('Paid & Social', 'tv-social'), ('Photo', 'tv-photo'), ('Design', 'tv-design'), ('Profiles', 'tv-profiles')]))
    hero = ('<!-- ===== Work, laid out like a TV app: featured slides with a pill nav over them (the pills jump to the shelves below), dots to pick a slide, and the slides advancing on their own ===== -->\n'
            '<section class="tv-hero on-dark" id="top" data-ws-stage data-ws-auto="7000" aria-label="Featured work">\n'
            '  <nav class="tv-nav" aria-label="On this page"><div class="tv-pills">%s</div></nav>\n  %s\n'
            '  <div class="tv-dots" role="tablist" aria-label="Featured">%s</div>\n</section>' % (pills, '\n  '.join(slides), ''.join(dots)))
    # the shelves
    shelves = []
    panes = {p['id']: p['items'] for p in pf['panes']}
    kinds = {'wide': 'Video', 'tall': 'Vertical video', 'square': 'Square cut'}
    # Featured: the newest videos, photographs and designs, interleaved, each at its own proportions in a row of one height
    by_key = {vkey(v): v for v in videos}
    # the Featured videos, reshuffled again on November 9, 2026: Lewis leads, then the new Gardyn :30, What No Can Do, and the rest
    FEATURED_VIDEOS = ['whoop-behind-the-drivers-seat-lewis.mp4', 'gardyn-song-30.mp4', '1087155996', 'ufl-nobull-what-no-can-do.mp4', '844754785', 'whoop-al-standalone-4x5.mp4',
                       '640557935', '1119136322', '1087156021', '833777565']
    recent = [by_key[k] for k in FEATURED_VIDEOS if k in by_key]
    photos = panes['photo'][9:12] + panes['photo'][0:3]
    designs = [it for it in panes['graphic'] if it['src'] != '2024/05/thumb-20-1.jpg'][7:13]   # not the 16:9 Gardyn static
    featured = []
    for i in range(len(recent)):
        if i < len(recent): featured.append(tv_tile(recent[i], None, 'film'))
        if i < len(photos): featured.append(tv_still_tile(photos[i], 'photo'))
        if i < len(designs): featured.append(tv_still_tile(designs[i], 'design'))
    shelves.append(tv_shelf('recent', 'Featured', featured, note='Video, photo and design, the latest from our Birds. Tap a frame to play it or see it at full size.'))
    # Case studies
    cases = []
    for slug in ORDER:
        c = CARDS[slug]
        cases.append('<li class="tv-tile tv-tile--wide"><a href="{{ROOT}}case-studies/%s.html"><span class="tv-media"><img src="{{ROOT}}img/%s" width="960" height="540" alt="%s" loading="lazy" decoding="async">%s</span>'
                     '<span class="tv-cap"><b>%s</b><span>%s</span></span></a></li>' % (slug, asset(c['cover']), esc(c['alt']), cover_loop(slug), esc(c['brand']), esc(c['stat'])))
    shelves.append(tv_shelf('cases', 'Case studies', cases, link=('See all', '{{ROOT}}case-studies.html'), note='The partnerships, the numbers behind them, and what the teams say.'))
    # Commercial: the spots and brand films the Commercial service page shows, in its order, then the other wide videos
    by_src = {v['src']: v for v in videos}
    svc_commercial = next(s for s in SERVICES if s['slug'] == 'commercial')
    refs = [r for r in svc_commercial['hero'] + svc_commercial['gallery'] if isinstance(r, str)]
    commercial, seen = [], set()
    for src in refs:
        v = by_src.get(src)
        if v and v['vid'] not in seen:
            seen.add(v['vid']); commercial.append(v)
    for v in folder_videos(EXTRA_FOLDERS['commercial'], videos):
        if v['vid'] not in seen:
            seen.add(v['vid']); commercial.append(v)
    for v in videos:  # the commercials Mike added by file
        if v.get('file') and v.get('svc') == 'Commercial' and v['file'] not in seen:
            seen.add(v['file']); commercial.append(v)
    commercial = edit_shelf('commercial', commercial)
    shelves.append(tv_shelf('commercial', 'Commercial', [tv_tile(v, 'Commercial', 'film') for v in commercial], link=('The service', '{{ROOT}}services/commercial.html'), note='Hero spots and brand films, from script to final mix.'))
    svc_profiles = next(s for s in SERVICES if s['slug'] == 'profiles')
    profiles, pseen = [], set()
    NOT_PROFILE_IDS = {'773909705', '951398925'}  # 686's 30 Years of Independence and the HD Expo interview with Dala Al-Fuwaires: on the service page, but not profiles
    def take(v):
        key = v['vid'] or v['file']
        if key not in pseen and key not in NOT_PROFILE_IDS:
            pseen.add(key); profiles.append(v)
    for src in [r for r in svc_profiles['hero'] + svc_profiles['gallery'] if isinstance(r, str)]:
        if src in by_src: take(by_src[src])
    for v in folder_videos(EXTRA_FOLDERS['profiles'], videos): take(v)
    PROFILE_WORDS = re.compile(r'in the studio|culture shifters|unwork|podcast|x route|operators vs analysts|challenging|painpoints|pro review', re.I)
    NOT_PROFILE = re.compile(r'9x16|iteration', re.I)  # the vertical ad cuts of the same pieces stay in Paid & Social
    for v in videos:
        info = hosted(v['vid'])
        if (info and PROFILE_WORDS.search(info['title']) and not NOT_PROFILE.search(info['title'])) or (v.get('file') and v.get('svc') == 'Profiles'): take(v)
    profiles = edit_shelf('profiles', profiles)
    profiles_shelf = tv_shelf('profiles', 'Profiles', [tv_tile(v, 'Profiles', 'film') for v in profiles], link=('The service', '{{ROOT}}services/profiles.html'), note='Founders, makers and the people behind the brand, on camera.') if profiles else ''
    # Paid & Social: every vertical, square and 4:5 piece, and the wide ones made for paid social or UGC, each at its own proportions
    social = edit_shelf('social', [v for v in videos if tv_shape(v['asp']) != 'wide' or service_for(v) in ('Paid Social', 'UGC')])
    shelves.append(tv_shelf('social', 'Paid & Social', [tv_tile(v, None, 'film') for v in social], note='Paid ads, UGC and social cuts, each in the ratio it was made for.'))
    shelves.append(tv_shelf('photo', 'Photography', [tv_still_tile(it, 'photo') for it in panes['photo']], note='Stills from our shoots, at full size when tapped.'))
    by_vid = {v['vid']: v for v in videos}
    design_v = [('video', v) for v in folder_videos(EXTRA_FOLDERS['animation'], videos) if v['vid'] != '1109213045']   # Humiint leaves (November 9, 2026)
    design_s = []
    seen_design = {v['vid'] for _, v in design_v}
    for it in panes['graphic']:
        v = by_vid.get(vimeo_id(it))
        if v and hosted(v['vid']) and v['src'] == it['src']:
            if v['vid'] in seen_design or v['vid'] == '1109213045': continue
            seen_design.add(v['vid']); design_v.append(('video', v))
        else:
            design_s.append(('still', it))
    design = []
    for i in range(max(len(design_v), len(design_s))):   # a video, then a still, so the shelf alternates
        if i < len(design_s): design.append(tv_still_tile(design_s[i][1], 'design'))
        if i < len(design_v): design.append(tv_tile(design_v[i][1], SVC_BY_SRC.get(design_v[i][1]['src'], 'Motion Graphics'), 'film'))
    shelves.append(tv_shelf('design', 'Design & animation', design, note='Motion, static ads, social posts and key art.'))
    if profiles_shelf: shelves.append(profiles_shelf)
    for slug in ORDER:
        vs = by_slug.get(slug, [])
        if len(vs) < 3:
            continue
        c = CARDS[slug]
        vs = edit_shelf(slug, vs)
        shelves.append(tv_shelf(slug, c['brand'], [tv_tile(v, None, 'film') for v in vs], link=('Case study', '{{ROOT}}case-studies/%s.html' % slug), note=c['tags']))
    chips = '\n'.join('<li>%s</li>' % esc(x) for x in WE_CREATE)
    create = ('<section class="tv-create" id="we-create" aria-label="What we make"><div class="wrap"><div class="head"><span class="eyebrow">What we make</span><h2 class="h2">We Create</h2>'
              '<p class="sub">From the TV spot to the email that follows it, one team makes every format a campaign needs.</p></div>'
              '<ul class="chips chips--dark" aria-label="Formats">%s</ul></div></section>' % chips)
    tv = '<div class="tv">\n%s\n\n<div class="tv-shelves">\n%s\n</div>\n</div>' % (hero, '\n\n'.join(shelves))
    inner = '\n\n'.join([tv, close_section('Read the case studies', '{{ROOT}}case-studies.html')])
    return document('Work: Birdline', 'Birdline’s work: case studies, commercials, social content, photography, design and animation for brands like Public Rec, Gardyn, FreePower, Route, 686, Patrol, Literati, Solidroad and WHOOP.', inner, '')

# ---- the Case Studies page
ARROW_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'

def index_page():
    cards = '\n'.join(cs_card(s) for s in ORDER)
    hero = ('<!-- ===== Case studies: the ten, in the order of the live page, then Willie’s Remedy ===== -->\n'
            '<section class="hero hero--page hero--grid on-dark" id="top">\n  <div class="wrap"><div class="hero-copy"><span class="eyebrow">Case Studies</span>'
            '<h1>How Brands <span class="ai">Scale Content</span> with Birdline</h1>'
            '<p class="lede">From the first brief to ongoing production: the work, the numbers behind it, and what the teams say about working with us.</p></div>\n'
            '  <ul class="cs-grid">\n%s\n  </ul></div>\n</section>' % cards)
    inner = '\n\n'.join([hero, testimonials, close_section('See the work', '{{ROOT}}portfolio.html')])
    return document('Case Studies: Birdline', 'Twelve Birdline case studies: WHOOP, Gardyn, Literati, Solidroad, 686, Route, FreePower, Public Rec, Willie’s Remedy, Patrol, EDJY and the UFL.', inner, '')

# ---- one case study
NAME_TO_SLUG = {'Public Rec': 'public-rec', 'Route App': 'route', 'Route': 'route', 'Gardyn': 'gardyn', 'FreePower': 'freepower', '686': '686',
                'Patrol': 'patrol', 'Literati': 'literati', 'Solidroad': 'solidroad', 'WHOOP': 'whoop', 'Willie’s Remedy': 'willies-remedy', 'EDJY': 'edjy', 'UFL': 'ufl'}

def radio_block(r):
    """the radio spots as a player: one reel (r['file']) and a button per spot that plays its own stretch (site.js, [data-radio])"""
    site_videos.add(r['file'])
    spots = ''.join('<li class="radio-spot"><button type="button" data-radio-play data-start="%.2f" data-end="%.2f" aria-pressed="false" aria-label="%s">'
                    '<span class="radio-btn" aria-hidden="true">%s%s</span><span class="radio-cap"><b>%s</b><span>%s</span></span><span class="radio-time">%s</span><i class="radio-bar" aria-hidden="true"></i></button></li>'
                    % (sp['start'], sp['end'], esc('Play: %s, %s' % (sp['name'], sp['note'])), PLAY.replace('<svg ', '<svg class="ic-play" ', 1), PAUSE, esc(sp['name']), esc(sp['note']), ':%02d' % round(sp['end'] - sp['start'])) for sp in r['spots'])
    return '<div class="radio" data-radio><audio preload="metadata" src="{{ROOT}}video/%s"></audio><ol class="radio-list" aria-label="Radio spots">%s</ol></div>' % (r['file'], spots)

def radio_section(r, eyebrow='On air', heading=None, sub=None):
    """the radio player as a band of its own (the UFL case study)"""
    return ('<section class="band cs-radio" id="radio">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="sub">%s</p></div>\n'
            '  %s</div>\n</section>' % (esc(eyebrow), tt(heading or r['heading']), esc(sub or r['sub']), radio_block(r)))

def quote_card(q, slug):
    brand = CARDS[slug]['brand']
    paras = [p.strip() for p in q['paras'] if p.strip()]
    paras[0] = paras[0].lstrip('"“ ')
    paras[-1] = paras[-1].rstrip('"” ')
    paras = [p.replace('"', '”') for p in paras]
    paras = [p.replace('assignment to then and', 'assignment to them and').replace('proiect', 'project') for p in paras]
    if not q.get('placeholder'):
        paras[0] = '“' + paras[0]
        paras[-1] = paras[-1] + '”'
    hs = HEADSHOTS.get(q['name'])
    if hs:
        av = '<img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" loading="lazy">' % (asset(hs[0]), hs[1], hs[1])
    else:
        av = ''.join(w[0] for w in q['name'].split()[:2]).upper()
    title = q['title'] if (' at ' in q['title'] or q['title'] == brand) else '%s at %s' % (q['title'], brand)
    key, lw, lh, _, qh = LOGOS[slug]
    logo = '<img class="q-logo" src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" style="--lh:%dpx">' % (asset(key), lw, lh, esc(brand), qh)
    return ('<li class="cs-quote%s"><div class="who"><span class="who-av" aria-hidden="true">%s</span><div class="who-name"><b>%s</b><span>%s</span></div></div>'
            '<div class="q">%s</div><span class="q-foot">%s</span></li>' % (' cs-quote--soon' if q.get('placeholder') else '', av, esc(q['name']), esc(title), ''.join('<p>%s</p>' % esc(p) for p in paras), logo))

def case_page(slug):
    cs = content['cases'][slug]
    ex = PAGES[slug]
    brand = CARDS[slug]['brand']
    copy = cs['copy']
    cover, cw, ch = site_img(cs['heroBg'])
    key, lw, lh, hero_h, _ = LOGOS[slug]
    facts = ['<li><span>Client</span><b>%s</b></li>' % esc(brand), '<li><span>Services</span><b>%s</b></li>' % esc(', '.join(copy['services']))]
    if ex['since']:
        facts.append('<li><span>Partnership</span><b>Since %s</b></li>' % ex['since'])
    hero = ('<!-- ===== Cover: the still from the live case-study page behind the brand’s mark, the headline and the facts ===== -->\n'
            '<section class="cs-hero on-dark" id="top" style="--focal:%s">\n  <div class="cs-hero-media" aria-hidden="true"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" fetchpriority="high"></div>\n'
            '  <div class="wrap cs-hero-in"><a class="crumb" href="{{ROOT}}case-studies.html">%sAll case studies</a>'
            '<img class="cs-logo" src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" style="--lh:%dpx">'
            '<h1>%s</h1><p class="lede">%s</p><ul class="cs-facts">%s</ul></div>\n</section>'
            % (ex['focal'], cover, cw, ch, ARROW_L, asset(key), lw, lh, esc(brand), hero_h, tt(ex['headline']), esc(ex['lede']), ''.join(facts)))
    overview = ('<div class="cs-cols"><div class="cs-side"><span class="eyebrow">Overview</span><h2>What We Do <span class="ai">for %s</span></h2></div>'
                '<div class="cs-text">%s</div></div>' % (esc(brand), ''.join('<p>%s</p>' % esc(p) for p in copy['overview'])))
    stats = results = ''
    challenge = ''
    if copy.get('challenge'):
        challenge = ('<div class="cs-cols cs-cols--next"><div class="cs-side"><span class="eyebrow">The challenge</span><h2>What %s <span class="ai">Needed</span></h2></div>'
                     '<div class="cs-text">%s</div></div>' % (esc(brand), ck_list(copy['challenge'])))
    if copy.get('pending'):
        results = ('<div class="cs-cols cs-cols--next"><div class="cs-side"><span class="eyebrow">Results</span><h2>What It <span class="ai">Earned</span></h2></div>'
                   '<div class="cs-text"><p>The numbers from this partnership are being finalized. They’ll land here as:</p>'
                   '<ul class="cs-stats cs-stats--soon" style="--n:%d" aria-label="Results to come">%s</ul></div></div>'
                   % (len(copy['pending']), ''.join('<li><b aria-hidden="true">—</b><p>%s</p></li>' % esc(t) for t in copy['pending'])))
    if copy['results']:
        if ex['stats']:
            ns = len(ex['stats'])
            stats = '<ul class="cs-stats" style="--n:%d" aria-label="Results in numbers">%s</ul>' % (3 if ns in (3, 6) else min(ns, 4), ''.join('<li><b>%s</b><p>%s</p></li>' % (esc(n), esc(t)) for n, t in ex['stats']))
        parts, points = [], []
        for item in copy['results']:
            if isinstance(item, (tuple, list)):
                points.append('<li><h3>%s</h3><p>%s</p></li>' % (esc(item[0]), esc(item[1])))
            else:
                if points:
                    parts.append('<ol class="cs-points">%s</ol>' % ''.join(points)); points = []
                parts.append('<p>%s</p>' % esc(item))
        if points:
            parts.append('<ol class="cs-points">%s</ol>' % ''.join(points))
        results = ('<div class="cs-cols cs-cols--next"><div class="cs-side"><span class="eyebrow">Results</span><h2>What It <span class="ai">Earned</span></h2></div>'
                   '<div class="cs-text">%s</div></div>' % ''.join(parts))
    story = '<section class="band cs-story">\n  <div class="wrap">%s%s%s%s</div>\n</section>' % (overview, challenge, stats if not copy.get('approach') else '', results if not copy.get('approach') else '')
    approach = why = ''
    if copy.get('approach'):
        steps = ''.join('<li><span class="step-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(copy['approach']))
        approach = ('<section class="band band--navy on-dark svc-process cs-approach">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">How We <span class="ai">Built It.</span></h2></div>'
                    '<ol class="steps">%s</ol></div>\n</section>' % (esc(copy.get('approach_label', 'Our approach')), steps))
        if results:
            approach += '\n\n<section class="band cs-story cs-story--results">\n  <div class="wrap">%s%s</div>\n</section>' % (results.replace(' cs-cols--next', '', 1), stats)
    if copy.get('why'):
        why = ('<section class="band band--wash cs-why">\n  <div class="wrap"><div class="head"><span class="eyebrow">Why it worked</span><h2 class="h2">Why It <span class="ai">Worked.</span></h2></div>'
               '<ul class="pillars">%s</ul></div>\n</section>' % ''.join('<li class="pillar"><span class="svc-ic" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>' % (ICONS[k], esc(t), esc(d)) for k, t, d in copy['why']))
    n = len(copy['quotes'])
    said = ('<section class="band band--tint cs-said">\n  <div class="wrap"><div class="head"><span class="eyebrow">Client Stories</span><h2 class="h2">In <span class="ai">Their Words</span></h2></div>'
            '<ul class="cs-quotes cs-quotes--%d" style="--n:%d">%s</ul></div>\n</section>' % (n, n, ''.join(quote_card(q, slug) for q in copy['quotes'])))
    tiles = '\n'.join(tile(it, 'work') for it in cs['gal'])
    work = ('<section class="band band--wash cs-work" id="work">\n  <div class="wrap"><div class="head"><span class="eyebrow">The work</span><h2 class="h2">Selected Work <span class="ai">for %s</span></h2>'
            '<p class="sub">Tap a frame to play it or see it at full size.</p>%s</div>\n  <div class="masonry masonry--3" data-masonry role="list" aria-label="Work for %s">\n%s\n  </div></div>\n</section>'
            % (esc(brand), '', esc(brand), tiles))
    radio = radio_section(copy['radio']) if copy.get('radio') else ''
    nxt = [NAME_TO_SLUG[nm] for nm in copy['next'] if NAME_TO_SLUG.get(nm) and NAME_TO_SLUG[nm] != slug][:4]
    more = ('<section class="band cs-more">\n  <div class="wrap"><div class="head"><span class="eyebrow">More case studies</span><h2 class="h2">Keep <span class="ai">Reading</span></h2></div>'
            '<ul class="cs-grid cs-grid--4 cs-grid--light">%s</ul><div class="more"><a class="btn" href="{{ROOT}}case-studies.html">All case studies</a></div></div>\n</section>'
            % ''.join(cs_card(s, light=True) for s in nxt))
    inner = '\n\n'.join(x for x in [hero, story, approach, why, said, work if cs['gal'] else '', radio, more, close_section('See more work', '{{ROOT}}portfolio.html')] if x)
    desc = copy['overview'][0]
    if len(desc) > 300:
        desc = desc[:297].rsplit(' ', 1)[0] + '…'
    return document('%s Case Study: Birdline' % brand, desc, inner, '../')


CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
CROSS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"></path></svg>'
ICONS = {
    'outcome': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 17l5-5 4 4 7-8"></path><path d="M14 8h6v6"></path></svg>',
    'talent': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.5"></circle><path d="M2.5 20a6.5 6.5 0 0 1 13 0"></path><path d="M16 4.5a3.5 3.5 0 0 1 0 7"></path><path d="M17.5 13.5a6.5 6.5 0 0 1 4 6.5"></path></svg>',
    'system': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="3"></rect><path d="M3 10h18M9 10v10"></path></svg>',
    'pm': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="3.5"></circle><path d="M5 20a7 7 0 0 1 14 0"></path></svg>',
    'slack': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-5 4z"></path></svg>',
    'integrate': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.5 1.5"></path><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.5-1.5"></path></svg>',
    'calls': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"></rect><path d="M3 10h18M8 3v4M16 3v4"></path></svg>',
    'reviews': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"></path></svg>',
    'tracker': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6h11M9 12h11M9 18h11"></path><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"></path></svg>',
    'workspace': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="14" rx="2"></rect><path d="M8 21h8M12 18v3M7 9h5M7 13h8"></path></svg>',
}
WF_ICONS = ['pm', 'slack', 'integrate', 'calls', 'reviews', 'tracker']
ICONS.update({
    'campaigns': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="8" height="7" rx="1.5"></rect><rect x="13" y="4" width="8" height="7" rx="1.5"></rect><rect x="3" y="13" width="8" height="7" rx="1.5"></rect><rect x="13" y="13" width="8" height="7" rx="1.5"></rect></svg>',
    'budget': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v18M16.5 7.5A3.5 3.5 0 0 0 13 5h-2.5a3 3 0 0 0 0 6h3a3 3 0 0 1 0 6H11a3.5 3.5 0 0 1-3.5-2.5"></path></svg>',
    'brand': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7l8-4 8 4-8 4z"></path><path d="M4 7v10l8 4 8-4V7"></path><path d="M12 11v10"></path></svg>',
    'team': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.5"></circle><path d="M2.5 20a6.5 6.5 0 0 1 13 0"></path><path d="M16 4.5a3.5 3.5 0 0 1 0 7"></path><path d="M17.5 13.5a6.5 6.5 0 0 1 4 6.5"></path></svg>',
    'share': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="2.5"></circle><circle cx="6" cy="12" r="2.5"></circle><circle cx="18" cy="19" r="2.5"></circle><path d="M8.2 10.8l7.6-4.6M8.2 13.2l7.6 4.6"></path></svg>',
})

def ck_list(items, cls='ck-list'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li><span class="ck" aria-hidden="true">%s</span><span>%s</span></li>' % (CHECK, esc(t)) for t in items))

def birds(row=False):
    cards = []
    for key, name, role, brands in TEAM:
        cards.append('<li class="bird"><span class="bird-pic"><img src="{{ROOT}}img/bird-%s.webp" width="400" height="400" alt="%s" loading="lazy"></span><div><b>%s</b><span>%s</span><small>%s</small></div></li>'
                     % (key, esc(name), esc(name), esc(role), esc(brands)))
    return '<ul class="birds%s" aria-label="The Birdline team">%s</ul>' % (' birds--row' if row else '', ''.join(cards))

def bird_loop():
    """the Birds in a row that runs edge to edge and loops: the set sits in the track twice, and the track slides by one set's width"""
    cards = ''.join('<li class="bird"><span class="bird-pic"><img src="{{ROOT}}img/bird-%s.webp" width="400" height="400" alt="%s" loading="lazy"></span><div><b>%s</b><span>%s</span><small>%s</small></div></li>'
                    % (key, esc(name), esc(name), esc(role), esc(brands)) for key, name, role, brands in TEAM)
    return ('<div class="bird-loop" aria-label="The Birdline team"><div class="bird-track"><ul class="bird-set">%s</ul><ul class="bird-set" aria-hidden="true">%s</ul></div></div>' % (cards, cards))

def team_loop():
    """the Birds as a row of cards in four tones that runs edge to edge and loops (the set sits in the track twice): the About page's row, shared with Packages"""
    tones = ['navy', 'tint', 'blue', 'peri']
    cards = ''.join('<li class="bird-card bird-card--%s"><span class="bird-pic"><img src="{{ROOT}}img/bird-%s.webp" width="400" height="400" alt="%s" loading="lazy"></span><div class="bird-name"><b>%s</b><span>%s</span><small>%s</small></div></li>'
                    % (tones[i % 4], key, esc(name), esc(name), esc(role), esc(brands)) for i, (key, name, role, brands) in enumerate(TEAM))
    return '<div class="team-loop" aria-label="The Birdline team"><div class="team-track"><ul class="team-set">%s</ul><ul class="team-set" aria-hidden="true">%s</ul></div></div>' % (cards, cards)

def faq_section(questions, heading):
    items = []
    for i, q in enumerate(questions):
        block = faq_items.get(q) or next((v for k, v in faq_items.items() if q in k), None)
        if not block:
            raise SystemExit('no FAQ item: ' + q)
        block = re.sub(r' open="open"', '', block)
        if i == 0:
            block = block.replace('<details class="qa" name="faq">', '<details class="qa" name="faq" open="open">', 1)
        items.append(block)
    return ('<section class="band band--wash faq" id="faq">\n  <div class="wrap"><div class="head"><span class="eyebrow">FAQ</span><h2 class="h2">%s</h2></div>'
            '<div class="faq-list">%s</div></div>\n</section>' % (tt(heading), '\n'.join(items)))

# ---- the policy and support pages (November 8, 2026): the four documents Mike exported as PDFs (Privacy Policy, Terms of
# Service, Support, Data Deletion Instructions), converted to HTML by legal/pdf2html.py and kept in legal/. Each is a compact navy
# hero (the eyebrow, the title, the date) over one column of text.
DOC_PAGES = [
    ('privacy', 'Legal', 'Privacy Policy', 'November 6, 2026', 'How Birdline collects, uses and shares personal information across the Sites, the App and Birdline Studios, and the choices you have.'),
    ('terms', 'Legal', 'Terms of Service', 'November 6, 2026', 'The terms that govern the Birdline Sites, the Birdline App and Birdline Studios services.'),
    ('support', 'Help', 'Support', 'November 8, 2026', 'How to reach Birdline support, connect integrations, manage your team and billing, and find our privacy and data pages.'),
    ('data-deletion', 'Help', 'Data Deletion Instructions', 'November 8, 2026', 'How to delete your Birdline account, your organization’s workspace, or the data Birdline synced from a platform you connected.'),
]

def doc_page(slug, eyebrow, title, updated, description):
    body_html = open(os.path.join(HERE, 'legal', slug + '.html'), encoding='utf-8').read()
    body_html = re.sub(r'<h1>.*?</h1>\n?', '', body_html, count=1)
    hero = ('<section class="hero hero--page hero--doc on-dark" id="top">\n  <div class="wrap"><div class="hero-copy"><span class="eyebrow">%s</span><h1>%s</h1>'
            '<p class="doc-date">Last updated %s</p></div></div>\n</section>' % (esc(eyebrow), esc(title), esc(updated)))
    doc = '<section class="band doc">\n  <div class="wrap"><article class="doc-body">\n%s\n  </article></div>\n</section>' % body_html
    return document('%s: Birdline' % title, description, hero + '\n\n' + doc, '')

# ---- the Packages page
def packages_page():
    for key, *_ in TEAM:
        site_imgs.add('bird-%s.webp' % key)
    site_imgs.add('production-set.webp')
    cols = flow_tiles()
    left = flow_column(cols[0], 'up', '96s', '0s') + flow_column(cols[1], 'down', '110s', '-20s')
    right = flow_column(cols[2], 'up', '104s', '-35s') + flow_column(cols[3], 'down', '90s', '-12s')
    tiles = [t for col in cols for t in col]
    row = ''.join('<li class="flow-tile">%s<span>%s</span></li>' % (img, label) for img, label in tiles)
    hero = ('<!-- ===== Packages: the copy on navy between columns of work that never stop flowing (two on each side, up and down; on narrower screens one row runs under the copy). The sets are in each track twice, so they loop. ===== -->\n'
            '<section class="hero hero--page hero--flow on-dark" id="top">\n'
            '  <div class="flow flow--l" aria-hidden="true">%s</div>\n  <div class="flow flow--r" aria-hidden="true">%s</div>\n'
            '  <div class="wrap"><div class="hero-copy"><span class="eyebrow">Packages</span>' % (left, right) +
            '<h1><span class="h1-l1">Get Unlimited Creative,</span> <span class="h1-l2 ai">With One Simple Plan</span></h1>'
            '<p class="lede">Plug our world-class talent into your team’s workflow and watch your creative take off. Get unlimited deliverables, seamless collaboration, and weekly creative support—without adding headcount.</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="#plans">See the packages</a></div>'
            '<a class="hero-link" %s aria-label="Play: hear from the CEO at Gardyn">%sHear from the CEO at Gardyn</a>'
            '</div></div>\n  <div class="flow flow--m" aria-hidden="true"><div class="flow-row"><ul class="flow-set">%s</ul><ul class="flow-set">%s</ul></div></div>\n</section>' % (play_attrs('1112070841', 'FX, CEO at Gardyn, on Birdline'), PLAY, row, row))
    pillars = ('<section class="band pillars-band">\n  <div class="wrap"><div class="head"><span class="eyebrow">Monthly Partnership</span><h2 class="h2">Built for Brands <span class="ai">That Can’t Slow Down.</span></h2>'
               '<p class="sub">One partnership covers the three things a content pipeline needs: the output, the people, and the system that keeps both moving.</p></div>'
               '<ul class="pillars">%s</ul></div>\n</section>'
               % ''.join('<li class="pillar"><span class="svc-ic" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>' % (ICONS[k], esc(t), esc(d)) for k, (t, d) in zip(['outcome', 'talent', 'system'], PILLARS)))
    plans = []
    for pk in PACKAGES:
        # the card: a tinted panel on top with the name, the price, the blurb and the button, then the lists on white below it
        plans.append('<li class="plan"><div class="plan-top"><div class="plan-head"><h3>%s</h3><span class="plan-k">Monthly package</span></div>'
                     '<div class="plan-price">%s<b>%s</b><span>%s</span></div><p class="plan-p">%s</p>'
                     '<a class="btn plan-btn" href="{{CALENDLY}}">Book a call</a></div>'
                     '<div class="plan-body">%s<span class="plan-wf">The Birdline Workflow</span>%s<p class="plan-note">Rolling monthly retainer, no fixed term. Cancel anytime with 60 days’ notice.</p></div></li>'
                     % (esc(pk['name']), '<em class="plan-from">Starting at</em>' if pk.get('starting') else '', esc(pk['price']), esc(pk['per']), esc(pk['blurb']), ck_list(pk['items']), ck_list(pk['workflow'])))
    prod = ('<div class="prod prod--navy"><div class="prod-media"><img src="{{ROOT}}img/production-set.webp" width="1600" height="1068" alt="A Birdline shoot: a camera on a tripod, two people in conversation on set, and a producer watching the monitor." loading="lazy"></div>'
            '<div class="prod-body"><span class="plan-k">Scoped separately, per project</span><h3>Productions</h3>'
            '<p>%s</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="{{ROOT}}services/production-process.html">Our production process</a></div></div></div>' % esc(ADDON))
    packages = ('<!-- ===== The packages: two monthly plans, each with the Birdline Workflow in it, and productions scoped per project ===== -->\n'
                '<section class="band band--wash plans-band" id="plans">\n  <div class="wrap"><div class="head"><span class="eyebrow">Choose Your Package</span><h2 class="h2">Start With One, <span class="ai">or Combine Both.</span></h2>'
                '<p class="sub">Each package is a rolling monthly retainer with a dedicated creative, unlimited deliverables, and the Birdline Workflow behind it: no fixed term, cancel anytime with 60 days’ notice. Productions are scoped separately, per project.</p></div>'
                '<ul class="plans">%s</ul>%s</div>\n</section>' % (''.join(plans), prod))
    team = ('<!-- ===== The talent: the Birds as the same row of cards as on the About page, running edge to edge and looping (the set sits in the track twice); pointing at it pauses it ===== -->\n'
            '<section class="band talent the-birds">\n  <div class="wrap"><div class="head"><span class="eyebrow">The Birds</span><h2 class="h2">World-Class Creatives, <span class="ai">All On One Line.</span></h2>'
            '<p class="sub">Skip the bloated agencies, unreliable freelancers, and wasted spend. Get full creative support across video, design, photo, AI, and animation—just a Slack message away.</p></div></div>\n'
            '  %s\n  <div class="wrap"><div class="more"><a class="btn btn--outline" href="{{ROOT}}about.html">Meet the Birds</a></div></div>\n</section>' % team_loop())
    faq = faq_section(FAQ_PACKAGES, 'Questions About |the Packages.')
    inner = '\n\n'.join([hero, logos_band, pillars, packages, team, testimonials, faq, close_section('Read the case studies', '{{ROOT}}case-studies.html')])
    return document('Packages: Birdline', 'Birdline’s monthly packages: Video Editing starting at $8,000/mo and Design & Animation starting at $6,000/mo, each with a dedicated creative, unlimited deliverables and the Birdline Workflow. Productions scoped per project.', inner, '')

# ---- the About page, laid out after superside.com/about-us in Birdline's system: a two-column hero over a full-width still, a
# statement and the brands on navy, the model beside the reel, four reasons, the Birds in a row of cards, client stories with
# their numbers, the values beside a sticky heading, how we deliver in a panel, and a close on a photograph
CLICKS = [
    ('talent', 'Only the best', 'World-class creatives', 'Vetted Birds across video, photo, design, AI, and animation, with credits like Red Bull, Nike, Nestlé, and Marvel, paired with a dedicated project manager.'),
    ('pm', 'Your dedicated team', 'A team that knows your brand', 'A dedicated editor or designer and a project manager who learn your brand and scale with your calendar, up or down, with no deliverable or revision limits.'),
    ('bolt', 'Weekly deliveries', 'Speed without the scramble', 'Initial assets within a week on average, Monday through Friday. Onboarding is simple and fast, so we start executing within a week of the call.'),
    ('workspace', 'One workspace', 'Measured in the Birdline App', 'Briefs, shot lists, deliverables, and ad results live as one connected campaign, with ROPS™ and ROCS™ on every production.'),
]
VALUES = [
    ('repeat', 'Compounding', 'Every deliverable keeps working for you.', 'We’re not here to deliver one-and-done projects. Every piece of content compounds in value, fueling future campaigns and giving you the agility to respond to trends, data, and market changes in real time.'),
    ('bolt', 'Speed', 'Fast onboarding, weekly deliveries, no waiting.', 'Onboarding is simple and fast, so we start within a week and begin executing right away. Initial assets come back within a week on average, Monday through Friday, with unlimited edits and revisions.'),
    ('slack', 'Partnership', 'An extension of your team, not a vendor.', 'We communicate directly in Slack, hold recurring creative and marketing calls, and connect our Birds with your existing team, internal workflow, and the Birdline App.'),
    ('outcome', 'Accountability', 'Measured on every production.', 'Every shoot’s spend and every ad’s revenue live in the Birdline App, so ROPS™ and ROCS™ are visible on every campaign, and ad performance reviews decide what we make next.'),
    ('target', 'Quality', 'Premium, cohesive, and consistent.', 'Top-tier creators, a dedicated project manager, and one system behind every deliverable, so the quality holds across all your content, from the hero spot to the email.'),
]
DELIVER_ROWS = [('calls', 'Ongoing shoots, any size'), ('camera', 'Anywhere, with the Birdline network'), ('tracker', 'A week, on average'), ('layers', 'Consistent quality')]
# client stories: the quotes are the case studies' own, cut to their first sentences; the figures are each study's
STORIES = [   # in the order Mike set on November 8, 2026, with John (EDJY) and Adam (Willie's Remedy) added
    ('gardyn', 'FX Rouxel', 'CEO at Gardyn', 'av-rouxel',
     'Birdline has been one of our key creative partners, helping us design a wide range of assets, videos, and campaigns. They’ve truly taken our brand to places we didn’t think were possible.',
     [('28%', 'year-over-year lift in CTR'), ('50%', 'better watch-through rates'), ('45M+', 'organic views')]),
    ('whoop', 'Zack McCabe', 'Video and Motion GFX Director at WHOOP', 'av-mccabe',
     'Birdline has become an incredibly valuable extension of our team, giving us the flexibility to execute across everything from bespoke long-form content and paid campaign deliverables to high-leverage work across our sports and culture partnerships.',
     []),
    ('solidroad', 'Kat Cooper', 'Head of Marketing at Solidroad', 'av-cooper',
     'They’re collaborative, proactive, and feel like an extension of our own team rather than an outside agency.',
     [('50+', 'pieces of content from one shoot'), ('2', 'days on set')]),
    ('public-rec', 'Zach Goldstein', 'CEO, Founder at Public Rec', 'av-goldstein',
     'They quickly picked up our brand’s look and feel and has consistently executed for us. They have a great eye for what will look good on screen.',
     [('$53M+', 'in returns across TV and Meta'), ('4×', 'return on $8M of TV spend'), ('51.7×', 'ROAS on one 30-second spot')]),
    ('freepower', 'Jake Slatnick', 'CEO, Founder at FreePower', 'av-slatnick',
     'This video production company is full-service and one of a kind. They handle every detail from concept through post-production, making the process seamless and stress-free.',
     [('15M', 'views in 12 months'), ('170K', 'link clicks'), ('23M', 'users reached')]),
    ('patrol', 'Nick Sarath', 'CEO, Founder at Patrol', 'av-sarath',
     'As a founder, delegating video content work to Birdline Studios has been incredibly impactful. Their attention to detail and ability to bring ideas to life have been amazing.',
     [('12M', 'views in one week'), ('4K', 'reposts'), ('8K', 'likes')]),
    ('edjy', 'John Bradford', 'Creative Director at EDJY', 'av-bradford',
     'Mike and the Birdline team have been a thoughtful creative partner for EDJY. They bring a strong editorial eye to our footage and help shape it into engaging, social-first videos.',
     []),
    ('willies-remedy', 'Adam Walker', 'Content Director at Willie’s Remedy', 'av-walker',
     'Super creative. Super fast. Simply put, Birdline gets it done—and makes it fun. Working with them feels like an extension of our team.',
     [('3', 'episodes of The Green Guide'), ('8', '3D product animations')]),
]
REEL = '1049385390'

def about_page():
    for key, *_ in TEAM:
        site_imgs.add('bird-%s.webp' % key)
    site_imgs.add('production-set.webp')
    hero = ('<!-- ===== About: the headline on the left, the lede and the buttons on the right, over a still from a Birdline set that runs edge to edge ===== -->\n'
            '<section class="hero hero--ab on-dark" id="top">\n  <div class="wrap"><div class="ab-hero">'
            '<div class="ab-hero-copy"><span class="eyebrow">About Birdline</span><h1>Endless Content, <span class="ai">Seamless Execution.</span></h1></div>'
            '<div class="ab-hero-side"><p class="lede">We provide brands with top-tier creators, unlimited deliverables, and an in-house production experience to maximize your content and streamline production workflows.</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="{{ROOT}}packages.html">View the packages</a></div></div></div></div>\n'
            '  <div class="ab-banner" aria-hidden="true"><img src="{{ROOT}}img/production-set.webp" width="1600" height="1068" alt="" fetchpriority="high"></div>\n</section>')
    statement = ('<section class="band band--navy on-dark ab-state">\n  <div class="wrap"><p class="ab-statement">Not an agency. Not a bench of freelancers. Your in-house content team, without the overhead, ready whenever, and however, you need it.</p></div>\n</section>')
    marquee = logos_band[logos_band.index('<div class="logo-marquee">'):logos_band.rindex('</section>')]
    logos = '<section class="logos logos--navy on-dark" aria-label="Brands Birdline works with">\n  <p class="logos-k">Brands that build their content with Birdline</p>%s</section>' % marquee
    smart = ('<!-- ===== The model, beside the reel ===== -->\n'
             '<section class="band band--navy on-dark ab-smart">\n  <div class="wrap"><div class="smart">'
             '<div class="smart-copy"><h2 class="h2">A <span class="ai">Smarter</span> Way to Scale Your Content.</h2>'
             '<p>Birdline replaces the one-and-done project with an always-on production model: unlimited deliverables every month from a dedicated team, premium productions scoped per project, and a workspace that turns every shoot into an ever-growing content library.</p>'
             '<blockquote class="smart-q"><p>“We started Birdline because too much content was going to waste, and brands didn’t know the value of their creative. So we built a different model: unlimited deliverables, premium productions, and a workspace that proves the value of everything made.”</p>'
             '<cite>Mike Pagan, Founder and CEO</cite></blockquote></div>'
             '<a class="smart-video" %s aria-label="Play: the Birdline reel">'
             '<img src="{{ROOT}}img/%s" width="2200" height="1468" alt="" loading="lazy"><span class="smart-play" aria-hidden="true">%s</span>'
             '<span class="smart-tag"><b>Our Bird’s Work</b><small>Watch the reel</small></span></a></div></div>\n</section>' % (play_attrs(REEL, 'Birdline showreel'), asset('hero-moto'), PLAY))
    clicks = ('<section class="band band--wash ab-clicks">\n  <div class="wrap"><div class="head"><span class="eyebrow">Built for brands that can’t slow down</span><h2 class="h2">A Content Partner That <span class="ai">Just Clicks.</span></h2></div>'
              '<ul class="clicks">%s</ul></div>\n</section>'
              % ''.join('<li><span class="svc-ic" aria-hidden="true">%s</span><span class="click-k">%s</span><h3>%s</h3><p>%s</p></li>' % (ICONS[k], esc(lab), esc(t), esc(d)) for k, lab, t, d in CLICKS))
    team = ('<!-- ===== The Birds: a row of cards that runs edge to edge and loops (the set sits in the track twice); pointing at it pauses it ===== -->\n'
            '<section class="band the-birds ab-team" id="team">\n  <div class="wrap"><div class="head"><span class="eyebrow">The Birds</span><h2 class="h2">World-Class Creatives, <span class="ai">All On One Line.</span></h2>'
            '<p class="sub">Partner with world-class creatives across video, photo, design, AI, and animation—operating as an extension of your in-house team.</p></div></div>\n'
            '  %s\n</section>' % team_loop())
    tabs, panels = [], []
    for i, (slug, name, title, av, quote, stats) in enumerate(STORIES):
        brand = CARDS[slug]['brand']
        if av:
            hs = HEADSHOTS[name]
            face = '<img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" loading="lazy">' % (asset(hs[0]), hs[1], hs[1])
        else:
            face = ''.join(w[0] for w in name.split()[:2]).upper()
        tabs.append('<button class="st-tab%s" type="button" role="tab" aria-selected="%s" data-story-tab="%d" aria-label="%s"><span class="who-av" aria-hidden="true">%s</span></button>'
                    % (' is-on' if i == 0 else '', 'true' if i == 0 else 'false', i, esc(name + ', ' + brand), face))
        key, lw, lh, _, qh = LOGOS[slug]
        logo = '<img class="st-logo" src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" style="--lh:%dpx">' % (asset(key), lw, lh, esc(brand), qh + 4)
        nums = ('<ul class="st-stats">%s</ul>' % ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(n), esc(t)) for n, t in stats)) if stats else ''
        panels.append('<div class="st%s" role="tabpanel" data-story-panel="%d"%s>%s<blockquote><p>“%s”</p></blockquote><p class="st-who"><b>%s</b>, %s</p>%s'
                      '<a class="st-link" href="{{ROOT}}case-studies/%s.html">Read the %s case study %s</a></div>'
                      % (' is-on' if i == 0 else '', i, '' if i == 0 else ' hidden', logo, esc(quote), esc(name), esc(title), nums, slug, esc(brand), ARROW_R))
    stories = ('<!-- ===== Client stories: the faces pick a story, the arrows step through them (site.js, [data-stories]) ===== -->\n'
               '<section class="band ab-stories" id="stories" data-stories data-story-at="0">\n  <div class="wrap"><div class="head"><span class="eyebrow">Client Stories</span><h2 class="h2">The Work Speaks. <span class="ai">So Do Our Clients.</span></h2></div>'
               '<div class="st-wrap"><div class="st-tabs" role="tablist" aria-label="Clients">%s</div><div class="st-panels">%s</div>'
               '<div class="st-nav"><button class="car-btn" type="button" data-story-prev aria-label="Previous story">%s</button><button class="car-btn" type="button" data-story-next aria-label="Next story">%s</button></div></div></div>\n</section>'
               % (''.join(tabs), ''.join(panels), ICONS['up'], ICONS['down']))
    values = ('<!-- ===== The values: five rows on navy, each with its numeral, the statement and its copy ===== -->\n'
              '<section class="band band--navy on-dark ab-values">\n  <div class="wrap"><div class="head"><span class="eyebrow">How we work</span><h2 class="h2"><span class="ai">Our Values</span> Lead the Way.</h2>'
              '<p class="sub">This is what makes us who we are: content that keeps working, speed you can plan around, a team that feels like yours, and results you can measure.</p></div>'
              '<ol class="vals">%s</ol><div class="more"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="{{ROOT}}packages.html">View the packages</a></div></div>\n</section>'
              % ''.join('<li><span class="val-n" aria-hidden="true">%02d</span><div class="val-head"><span class="v-k">%s</span><h3>%s</h3></div><p>%s</p></li>'
                        % (i + 1, esc(lab), esc(t), esc(d)) for i, (k, lab, t, d) in enumerate(VALUES)))
    rows = ''.join('<li><span class="svc-ic" aria-hidden="true">%s</span><b>%s</b><p>%s</p></li>' % (ICONS[k], esc(t), esc(d)) for (k, t), d in zip(DELIVER_ROWS, DELIVER))
    deliver = ('<section class="band ab-deliver">\n  <div class="wrap"><div class="dpanel"><div class="dpanel-copy"><span class="eyebrow">How we deliver</span><h2>Full-Service, <span class="ai">Start to Finish.</span></h2>'
               '<p>Partner with world-class creatives across video, photo, design, AI, and animation—operating as an extension of your in-house team.</p><ul class="dgrid">%s</ul></div>'
               '<div class="dpanel-media"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="A Birdline crew around a kitchen table on the Gardyn shoot: the director checks the breakfast setup while the camera operator lines up the shot." loading="lazy"></div></div></div>\n</section>'
               % ((rows,) + site_img('new/gardyn-7-29-2025-27361.jpg')))
    cf, cw, ch = site_img('2024/06/GrantPuckett-Lifestyle-67.jpg')
    close = close_section('View the packages', '{{ROOT}}packages.html', photo=(cf, cw, ch))
    inner = '\n\n'.join([hero, statement, logos, smart, clicks, team, library_section(), stories, values, deliver, close])
    return document('About: Birdline', 'Birdline is a premium creative studio and production workspace: top-tier creators, unlimited deliverables, and an in-house production experience for brands that can’t slow down.', inner, '')


def library_section():
    """the content library: the productions on the left, the campaigns cut from them on the right, and the lines between them
    (site.js draws the lines from the cards' positions, [data-flow]); on the Why Us and About pages"""
    # the library: the productions on the left, the campaigns cut from them on the right, and the lines between them (site.js draws
    # the lines from the cards' positions, [data-flow]); pointing at or tapping a card lights what it fed or drew on
    names = {key: name for key, name, _m, _p in PRODUCTIONS}
    def mo(m):
        return MONTHS[m % 12] + (', the next year' if m >= 12 else '')
    fed = {key: [c for c in CAMPAIGNS if key in c[3]] for key, *_ in PRODUCTIONS}
    def join(xs):
        return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]
    def thumb(src):
        it = piece(src)
        f, w, h = site_img(it['src'])
        return '<li style="--asp:%.3f"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" loading="lazy"></li>' % (w / h, f, w, h)
    prods = []
    for key, name, m, pcs in PRODUCTIONS:
        camps = fed[key]
        span = camps[-1][2] - m if camps else 0
        cap = '%s, %s: one day on set, then %s campaign%s cut from it%s.' % (name, mo(m), len(camps), '' if len(camps) == 1 else 's', (', from %s to %s' % (mo(camps[0][2]), mo(camps[-1][2]))) if len(camps) > 1 else '')
        prods.append('<button class="cl-card cl-card--prod" type="button" data-node="%s" data-kind="production" data-order="%d" data-caption="%s">'
                     '<span class="cl-top"><b>%s</b><span>Production · %s</span></span><ul class="cl-thumbs">%s</ul><span class="cl-sub">Commercial · UGC · Stills</span><i class="cl-port" aria-hidden="true"></i></button>'
                     % (key, m, esc(cap), esc(name), mo(m), ''.join(thumb(x) for x in pcs)))
    camps = []
    for key, name, m, srcs, src in CAMPAIGNS:
        it = piece(src)
        f, w, h = site_img(it['src'])
        cap = '%s, %s: cut from the %s set%s, with no new shoot.' % (name, mo(m), join([names[x] for x in srcs]), '' if len(srcs) == 1 else 's')
        camps.append('<button class="cl-card cl-card--camp" type="button" data-node="%s" data-kind="campaign" data-order="%d" data-from="%s" data-caption="%s">'
                     '<i class="cl-port" aria-hidden="true"></i><span class="cl-top"><b>%s</b><span>Campaign · %s</span></span><span class="cl-still"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy"></span>'
                     '<span class="cl-from"><span>Cut from</span>%s</span></button>'
                     % (key, m, ' '.join(srcs), esc(cap), esc(name), mo(m), f, w, h, esc((it['alt'] or 'Gardyn') + ' — still'), ''.join('<em data-ref="%s">%s</em>' % (x, esc(names[x])) for x in srcs)))
    default_cap = 'Point at a production to see every campaign it fed, or at a campaign to see where it came from.'
    library = ('<!-- ===== The content library: a year at Gardyn. The productions on the left, the campaigns cut from them on the right, and\n'
               '     lines between them drawn by site.js ([data-flow]); pointing at or tapping a card lights what it fed or drew on, and\n'
               '     the board walks through the year on its own until someone takes over ===== -->\n'
               '<section class="band band--navy on-dark why-library" id="library">\n'
               '  <div class="wrap"><div class="head"><span class="eyebrow">Content Library</span><h2 class="h2">From a Single Production… <span class="ai">to Evergreen Use.</span></h2>'
               '<p class="sub">%s</p></div>'
               '<div class="cl" data-flow data-flow-auto="3600"><div class="cl-board">'
               '<div class="cl-col cl-col--prod"><h3 class="cl-h"><b>Productions</b><span>Days on set that fill the library</span></h3>%s</div>'
               '<svg class="cl-svg" aria-hidden="true"></svg>'
               '<div class="cl-col cl-col--camp"><h3 class="cl-h"><b>Campaigns</b><span>Cut from the library, no new shoot</span></h3>%s</div></div>'
               '<p class="cl-cap" data-flow-cap data-flow-default="%s" aria-live="polite">%s</p></div>'
               '<ul class="cl-stats" aria-label="The year in numbers">%s</ul>'
               '<p class="tl-statement"><span>%s</span> <em>%s</em></p></div>\n</section>'
               % (esc(LIBRARY_INTRO), ''.join(prods), ''.join(camps), esc(default_cap), esc(default_cap),
                  ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(n), esc(t)) for n, t in LIBRARY_STATS), esc(LIBRARY_STATEMENT[0]), esc(LIBRARY_STATEMENT[1])))
    return library

def calc_form():
    """the homepage's ROPS/ROCS calculator form (script.js binds [data-calc-form] wherever it is)"""
    return calc_band[calc_band.index('<form class="calc-form"'):calc_band.index('</form>') + len('</form>')]

# ---- the Why Us page: the mission, four reasons, the content library as a year at Gardyn (interactive), ROPS and ROCS with the
# Public Rec numbers and the calculator, and the Birdline App
def why_page():
    for key, *_ in TEAM:
        site_imgs.add('bird-%s.webp' % key)
    hf, hw, hh = site_img('2025/09/PublicRec-DTLA-DD-33.jpeg')
    hero = ('<!-- ===== Why us: the mission, over a still from a Public Rec shoot under a navy wash ===== -->\n'
            '<section class="hero hero--page hero--why on-dark" id="top">\n'
            '  <div class="hero-media" aria-hidden="true"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" fetchpriority="high"></div>\n'
            '  <div class="wrap"><div class="hero-copy"><span class="eyebrow">Why Birdline</span>'
            '<h1>Your Dollar <span class="ai">Matters.</span></h1>'
            '<p class="lede">%s</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="{{ROOT}}packages.html">See the packages</a></div></div></div>\n</section>' % (hf, hw, hh, esc(HERO_LEDE)))
    # four reasons, each opening with a picture of the thing: the Birds, the work, a Slack thread, the app
    visuals = {
        'birds': '<span class="rs-vis rs-vis--birds" aria-hidden="true"><span class="rs-avs">%s</span><span class="rs-plus">+ your freelancers</span></span>'
                 % ''.join('<img src="{{ROOT}}img/bird-%s.webp" width="400" height="400" alt="">' % k for k, *_ in TEAM[:5]),
        'unlimited': '<span class="rs-vis rs-vis--inf" aria-hidden="true"><b>∞</b><span>deliverables<br>&amp; revisions</span></span>',
        'slack': ('<span class="rs-vis rs-vis--slack" aria-hidden="true"><span class="rs-msg"><img src="{{ROOT}}img/bird-%s.webp" width="400" height="400" alt=""><span><b>Ryan</b> <small>#gardyn-birdline · 9:41 AM</small><em>Statics and the 9:16 cuts are up for review.</em></span></span></span>' % TEAM[2][0]),
        'app': '<span class="rs-vis rs-vis--app" aria-hidden="true"><img src="{{ROOT}}img/%s" width="2000" height="1368" alt="" loading="lazy"></span>' % asset('app6-insights'),
    }
    reasons = ('<!-- ===== Four reasons ===== -->\n'
               '<section class="band band--wash why-reasons">\n  <div class="wrap"><div class="head"><span class="eyebrow">Why brands choose Birdline</span><h2 class="h2"><span class="nowrap">Premium Content,</span> <span class="ai nowrap">On Demand and On Brand.</span></h2>'
               '<p class="sub">%s</p></div><ul class="rs-grid">%s</ul></div>\n</section>'
               % (esc(REASONS_LINE), ''.join('<li class="rs">%s<h3>%s</h3><p>%s</p></li>' % (visuals[k], esc(t), esc(d)) for k, t, d in REASONS)))
    library = library_section()
    metrics = ''.join('<li><b>%s<sup class="mark-tm">™</sup></b><span>%s</span><p>%s</p></li>' % (esc(k), esc(t), esc(d)) for k, t, d in METRICS)
    proof = ''.join('<li class="pr-row"><div class="pr-head"><b>%s<sup class="mark-tm">™</sup></b><span>%s</span></div><ul class="pr-stats">%s</ul></li>'
                    % (esc(k), esc(t), ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(n), esc(l)) for n, l in stats)) for k, t, stats in PROOF)
    form = calc_form()
    rops = ('<!-- ===== ROPS and ROCS: the two metrics and the Public Rec numbers beside the calculator (script.js, [data-calc-form]) ===== -->\n'
            '<section class="band band--navy on-dark why-rops" id="calculator">\n  <div class="wrap"><div class="head"><span class="eyebrow">ROPS<sup class="mark-tm">™</sup> &amp; ROCS<sup class="mark-tm">™</sup></span>'
            '<h2 class="h2">Don’t Measure ROAS in a Vacuum. <span class="ai">Measure What Production Earned.</span></h2><p class="sub">%s</p></div>'
            '<div class="earn"><div class="earn-side"><ul class="metrics">%s</ul><div class="rops-proof"><span class="pr-k">What it looks like</span><ul class="pr-list">%s</ul><p>%s</p></div></div>'
            '<div class="earn-calc"><p class="calc-hint">Plug in your campaign numbers:</p>%s</div></div>'
            '<div class="more"><a class="btn btn--ghost" href="{{ROOT}}rops.html">How we measure ROPS<sup class="mark-tm">™</sup> &amp; ROCS<sup class="mark-tm">™</sup></a></div></div>\n</section>'
            % (esc(ROPS_INTRO), metrics, proof, esc(PROOF_NOTE), form))
    chain = ''.join('<li>%s</li>' % esc(t) for t in APP_CHAIN)
    app = ('<!-- ===== The Birdline App: an archive, not a graveyard. The five things the library holds run as a chain beside the brief ===== -->\n'
           '<section class="band band--wash why-app" id="app">\n  <div class="wrap"><div class="head"><span class="eyebrow">The Birdline App</span><h2 class="h2">Most Brand Archives <span class="ai">Are Graveyards.</span></h2>'
           '<p class="sub sub--wide">%s</p></div>'
           '<div class="app-panel on-dark"><div class="app-copy"><span class="app-k">What the library holds</span><ol class="app-chain">%s</ol><p class="app-tail">%s</p>'
           '<div class="cta-row"><a class="btn btn--light" href="{{ROOT}}workspace.html">Explore the Birdline App</a><a class="btn btn--ghost" href="https://app.birdline.ai/login?mode=signup">Start free trial</a></div></div>'
           '<figure class="app-screen"><img class="d-only" src="{{ROOT}}img/%s" width="1760" height="1408" alt="%s" loading="lazy"><img class="m-only" src="{{ROOT}}img/%s" width="1330" height="1108" alt="%s" loading="lazy"></figure></div></div>\n</section>'
           % (esc(APP_SUB), chain, esc(APP_TAIL), asset('app4-brief'), esc(FEATURES[0]['alt']), asset('app4-brief-m'), esc(FEATURES[0]['alt'])))
    inner = '\n\n'.join([hero, library, reasons, rops, app, close_section('See the packages', '{{ROOT}}packages.html')])
    return document('Why Birdline', 'Why brands choose Birdline: world-class creatives on Slack, unlimited deliverables, a content library that keeps working for years, ROPS™ and ROCS™ on every production, and the Birdline App that holds it all.', inner, '')

# ---- the Birdline App page
def workspace_page():
    # each page twice: the wide capture for screens over 720px, the narrower one for phones (the .d-only/.m-only helpers show one)
    screens = []
    for i, (key, label, alt) in enumerate(WS_SCREENS):
        for kind, cls, suffix in (('d', 'd-only', ''), ('m', 'm-only', '-m')):
            w, h = WS_SIZES[kind]
            site_imgs.add('ws-%s%s.webp' % (key, suffix))
            screens.append('<img class="%s%s" src="{{ROOT}}img/ws-%s%s.webp" width="%d" height="%d" alt="%s"%s data-ws-screen="%s">'
                           % (cls, ' is-on' if i == 0 else '', key, suffix, w, h, esc(alt), '' if i == 0 else ' loading="lazy"', key))
    switch = ''.join('<button%s type="button" role="tab" aria-selected="%s" data-ws-tab="%s">%s</button>' % (' class="is-on"' if i == 0 else '', 'true' if i == 0 else 'false', key, esc(label)) for i, (key, label, _alt) in enumerate(WS_SCREENS))
    floaters = ''.join('<span class="fl fl--%s" style="--x:%s;--y:%dpx;--r:%s;--k:%s;--s:%dpx;--d:%s"><i><img src="{{ROOT}}img/%s" width="256" height="256" alt="" loading="lazy"></i></span>'
                       % (side, x, y, r, k, size, d, asset(key)) for key, side, x, y, r, k, size, d in FLOATERS)
    hero = ('<!-- ===== The Birdline App: the copy on navy, then the workspace itself, whole and edge to edge, with a switch between its five pages above it.\n'
            '     The connected apps\' logos float beside the headline and, as the page scrolls, drift down behind the workspace (site.js, [data-float]). ===== -->\n'
            '<section class="hero hero--page hero--about hero--app on-dark" id="top">\n'
            '  <div class="float-layer" data-float aria-hidden="true">%s</div>\n'
            '  <div class="wrap"><div class="hero-copy"><span class="eyebrow">Birdline App</span>' % floaters +
            '<h1>The Production Workspace <span class="ai">for In‑House Content Teams</span></h1>'
            '<p class="lede">Birdline is where briefs, deliverables, and performance insights live as one connected campaign—so in-house content teams produce more and prove more.</p>'
            '<div class="cta-row"><a class="btn btn--light" href="https://app.birdline.ai/login?mode=signup">Start free trial</a><a class="btn btn--ghost" href="{{CALENDLY}}">Book a demo</a></div>'
            '<p class="hero-note">Start free for 30 days. No credit card required.</p></div>'
            '<div class="hero-still"><div class="ws-hero" data-ws-stage data-ws-auto="4500" aria-label="The Birdline App">'
            '<div class="ws-bar"><div class="ws-switch" role="tablist" aria-label="Workspace pages">%s</div></div>'
            '<div class="ws-screens">%s</div></div></div></div>\n</section>' % (switch, ''.join(screens)))
    loop = ('<section class="band about-intro">\n  <div class="wrap"><div class="head"><span class="eyebrow">The Loop</span><h2 class="h2">One Continuous Line. <span class="ai">Three Stages.</span></h2>'
            '<p class="sub">Keep context connected across the entire campaign lifecycle, so great work doesn’t get lost after launch. It gets valued, studied, and built on.</p></div>'
            '<ol class="loop">%s</ol></div>\n</section>'
            % ''.join('<li><span class="loop-n">%s</span><h3>%s</h3><p>%s</p></li>' % (esc(n), esc(t), esc(d)) for n, t, d in LOOP))
    rows = []
    for i, f in enumerate(FEATURES):
        d, dw, dh, m, mw, mh = f['img']
        rows.append('<div class="fr%s"><div class="fr-copy"><span class="eyebrow">%s</span><h3>%s</h3><p>%s</p>%s</div>'
                    '<figure class="fr-screen vig--3"><img class="d-only" src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy"><img class="m-only" src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy"></figure></div>'
                    % (' fr--flip' if i % 2 else '', esc(f['label']), esc(f['title']), esc(f['p']), ck_list(f['items']), asset(d), dw, dh, esc(f['alt']), asset(m), mw, mh, esc(f['alt'])))
    product = ('<section class="band band--wash product-rows">\n  <div class="wrap"><div class="head"><span class="eyebrow">The Product</span><h2 class="h2">Made for <span class="ai">In‑House Content Teams.</span></h2>'
               '<p class="sub sub--wide">Keep your workflow. Birdline connects it. From brief to production to performance, every campaign stays connected so content teams can move faster, stay aligned, and build on what’s working.</p></div>'
               '%s<p class="fine">Product screens show sample data from a demo workspace.</p></div>\n</section>' % ''.join(rows))
    around = ('<section class="band app-page around">\n  <div class="wrap"><div class="head"><span class="eyebrow">Also in the workspace</span><h2 class="h2">And Everything <span class="ai">Around It.</span></h2></div>'
              '<ul class="tiles">%s</ul>%s</div>\n</section>'
              % (''.join('<li><div class="svc"><span class="svc-ic" aria-hidden="true">%s</span><b>%s</b><span>%s</span></div></li>' % (ICONS[k], esc(t), esc(d)) for k, t, d in AROUND), works_block))
    tiein = ('<section class="band band--tint tiein">\n  <div class="wrap"><div class="head"><span class="eyebrow">Monthly Partnership</span><h2 class="h2">Want the Birds <span class="ai">In It Too?</span></h2>'
             '<p class="sub sub--wide">Every Monthly Partnership runs through the same workspace: our requests land in your Deliverables with the same owner, due date, and review status, and every shoot’s spend shows up in Insights.</p>'
             '<div class="cta-row"><a class="btn" href="{{ROOT}}packages.html">See the packages</a><a class="btn btn--outline" href="{{ROOT}}case-studies.html">Read the case studies</a></div></div></div>\n</section>')
    faq = faq_section(FAQ_APP, 'Questions About |the App.')
    close = close_section('Book a demo', '{{CALENDLY}}', heading='Build Winning Campaigns with a Bird’s-Eye View',
                          sub='Bring the campaign you’re working on now. Start free for 30 days, no credit card required.',
                          first=('Start free trial', 'https://app.birdline.ai/login?mode=signup'))
    inner = '\n\n'.join([hero, loop, product, around, calc_band, tiein, faq, close])
    return document('Production Workspace: Birdline', 'The Birdline App is the production workspace for in-house content teams: briefs, shot lists, deliverables, and performance insights as one connected campaign, with ROPS™ and ROCS™ measured on every production.', inner, '')

# ---- the Services pages: an index of the fifteen, and a page for each
_IC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
ICONS.update({
    'layers': _IC % '<path d="M12 3l9 5-9 5-9-5z"></path><path d="M3 12.5l9 5 9-5"></path><path d="M3 17l9 5 9-5"></path>',
    'target': _IC % '<circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="5"></circle><circle cx="12" cy="12" r="1"></circle>',
    'grid': _IC % '<rect x="3" y="3" width="7" height="7" rx="1.5"></rect><rect x="14" y="3" width="7" height="7" rx="1.5"></rect><rect x="3" y="14" width="7" height="7" rx="1.5"></rect><rect x="14" y="14" width="7" height="7" rx="1.5"></rect>',
    'phone': _IC % '<rect x="7" y="2.5" width="10" height="19" rx="2.5"></rect><path d="M11 18h2"></path>',
    'camera': _IC % '<path d="M4 8h3l2-3h6l2 3h3v11H4z"></path><circle cx="12" cy="13" r="3.5"></circle>',
    'cube': _IC % '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"></path><path d="M4 7.5l8 4.5 8-4.5M12 12v9"></path>',
    'repeat': _IC % '<path d="M17 2l4 4-4 4"></path><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><path d="M7 22l-4-4 4-4"></path><path d="M21 13v2a4 4 0 0 1-4 4H3"></path>',
    'bolt': _IC % '<path d="M13 2L4 14h7l-1 8 9-12h-7z"></path>',
    'screen': _IC % '<rect x="2" y="4" width="20" height="13" rx="2"></rect><path d="M8 21h8M12 17v4"></path>',
    'pen': _IC % '<path d="M12 20h9"></path><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"></path>',
    'film': _IC % '<rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"></path>',
    'mic': _IC % '<rect x="9" y="3" width="6" height="11" rx="3"></rect><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"></path>',
    'music': _IC % '<path d="M9 18V6l12-2v12"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle>',
    'eye': _IC % '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"></path><circle cx="12" cy="12" r="3"></circle>',
    'up': _IC % '<path d="M12 19V5M5 12l7-7 7 7"></path>',
    'down': _IC % '<path d="M12 5v14M19 12l-7 7-7-7"></path>',
})
SVC = {s['slug']: s for s in SERVICES}
GROUP_NAME = {key: label for key, label, _ in GROUPS}
# the thumbnails' alt text, as the homepage's services grid has it
SVC_ALT = dict(re.findall(r'data-img="([^"]+)" width="\d+" height="\d+" alt="([^"]*)"', body[body.index('<ul class="svc-grid">'):body.index('</ul>', body.index('<ul class="svc-grid">'))]))

# every piece on the Work page and in the case-study galleries, by its source path, with the brand filled in where the gallery left it out
PIECES = {}
for _pane, _kind in (('video', 'video'), ('photo', 'photo'), ('graphic', 'design')):
    for _it in next(p for p in content['portfolio']['panes'] if p['id'] == _pane)['items']:
        PIECES.setdefault(_it['src'], dict(_it, kind=_kind))
for _slug in ORDER:
    for _it in content['cases'][_slug].get('gal', []):
        if 'src' not in _it:
            continue  # a self-hosted video tile; the service pages draw their examples from the stills
        _d = dict(_it, kind='video' if 'vimeo.com' in _it.get('href', '') else 'photo')
        _d['alt'] = _d.get('alt') or CARDS[_slug]['brand']
        PIECES.setdefault(_it['src'], _d)
for _vid, _it in VIDEO_ITEMS.items():  # stills of videos the folders moved or dropped stay available to the service pages
    PIECES.setdefault(_it['src'], dict(_it, kind='video'))

def asset_wh(key):
    from PIL import Image
    with Image.open(os.path.join(OUT, 'img', asset(key))) as im:
        return im.size

def piece(ref):
    """an example as the dict tile() takes: a source path on the live site; ('site', path, label) for a live-site image outside the
    galleries; ('asset', key, label, alt) for one of the homepage's own images"""
    if isinstance(ref, dict):   # a self-hosted video (or a still) declared where the service lists it, as tile() takes it
        d = dict(ref); d.setdefault('kind', 'video' if d.get('video') else 'photo'); d['asp'] = d['w'] / d['h']
        return d
    if isinstance(ref, tuple):
        if ref[0] == 'site':
            f = imap[ref[1]]
            return dict(src=ref[1], href=ref[1], alt=ref[2], asp=f['w'] / f['h'], kind='photo')
        w, h = asset_wh(ref[1])
        return dict(asset=ref[1], label=ref[2], alt=ref[3], asp=w / h, w=w, h=h, kind='photo')
    return PIECES[ref]

def svc_tile(item, strip=False):
    """a piece as a gallery tile; in the hero strip (strip=True) it carries its proportions, so the row can share one height"""
    if 'asset' in item:
        a = '<a href="{{ROOT}}img/%s" data-lb="image" target="_blank" aria-label="%s">' % (asset(item['asset']), esc(item['label'] + ' at full size'))
        html = ('<div class="gi" role="listitem">%s<img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">'
                '<span class="gi-play gi-play--zoom" aria-hidden="true">%s</span><span class="gi-label">%s</span></a></div>'
                % (a, asset(item['asset']), item['w'], item['h'], esc(item['alt']), ZOOM, esc(item['label'])))
    else:
        html = tile(item, item['kind'])
    if strip:
        html = re.sub(r'^<div class="(gi[^"]*)" role="listitem"', lambda m: '<div class="%s" role="listitem" style="--asp:%.3f"' % (m.group(1), float(item['asp'])), html, count=1)
    return html

def svc_card(svc, large=False):
    f = asset(svc['img'])
    w, h = asset_wh(svc['img'])
    go = '<em class="svc-go">Learn more %s</em>' % ARROW_R if large else ''
    return ('<li><a class="svc%s" href="{{ROOT}}services/%s.html"><span class="svc-thumb"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy"></span>'
            '<b>%s</b><span>%s</span>%s</a></li>' % (' svc--lg' if large else '', svc['slug'], f, w, h, esc(SVC_ALT.get(svc['img'], '')), esc(svc['name']), esc(svc['blurb']), go))

def qa_list(items, first_open=True):
    out = []
    for i, (q, a) in enumerate(items):
        out.append('<details class="qa" name="faq"%s><summary>%s<span class="qa-ic" aria-hidden="true"></span></summary><div class="qa-a">%s</div></details>'
                   % (' open="open"' if i == 0 and first_open else '', esc(q), esc(a)))
    return '<div class="faq-list">%s</div>' % ''.join(out)

def services_page():
    hero = ('<!-- ===== Services: the copy on navy, then the fifteen in one grid ===== -->\n'
            '<section class="hero hero--page hero--svcs on-dark" id="top">\n  <div class="wrap"><div class="hero-copy"><span class="eyebrow">Services</span>'
            '<h1>Many Ways <span class="ai">to Make It.</span></h1>'
            '<p class="lede">Every format your channels need, from one team, inside one workspace. Request any of them on the Monthly Partnership, or scope a production on its own.</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="{{ROOT}}packages.html">See the packages</a></div></div></div>\n</section>')
    index = '<section class="band svc-index">\n  <div class="wrap"><ul class="svc-grid svc-grid--3">%s</ul></div>\n</section>' % ''.join(svc_card(s, large=True) for s in SERVICES)
    inner = '\n\n'.join([hero, index, testimonials, close_section('See the work', '{{ROOT}}portfolio.html')])
    return document('Services: Birdline', 'Birdline’s fifteen services: commercials, paid social, photography, UGC, 3D / VFX, motion graphics, design, CTV, profiles, video podcasts, illustration, film, audio, OOH and AI content, on the Monthly Partnership or scoped as a production.', inner, '')

def service_page(svc):
    slug, name = svc['slug'], svc['name']
    strip = ''.join(svc_tile(piece(r), strip=True) for r in svc['hero'])
    hero = ('<!-- ===== %s: the copy on navy, then a strip of the work that runs down into the next band ===== -->\n'
            '<section class="hero hero--page hero--svc on-dark" id="top">\n  <div class="wrap"><div class="hero-copy"><a class="crumb" href="{{ROOT}}services.html">%sAll services</a>'
            '<span class="eyebrow">Services · %s</span><h1>%s</h1><p class="lede">%s</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="#examples">See examples</a></div></div>'
            '<div class="svc-strip" role="list" aria-label="%s">%s</div></div>\n</section>'
            % (name, ARROW_L, esc(GROUP_NAME[svc['cat']]), tt(svc['h1']), esc(svc['lede']), esc('Examples of ' + name.lower() if name not in ('UGC', 'CTV', 'OOH', '3D / VFX', 'AI Content') else 'Examples of ' + name), strip))
    facts = ''.join('<li><span>%s</span><b>%s</b></li>' % (esc(k), esc(v)) for k, v in svc['facts'])
    intro = ('<section class="band svc-intro">\n  <div class="wrap"><div class="cs-cols"><div class="cs-side"><span class="eyebrow">What it is</span><h2>%s</h2></div>'
             '<div class="cs-text">%s<ul class="svc-facts">%s</ul></div></div>'
             '<div class="svc-formats"><span class="works-k">What we deliver</span><ul class="chips chips--tint">%s</ul></div></div>\n</section>'
             % (tt(svc['intro_h2']), ''.join('<p>%s</p>' % esc(p) for p in svc['purpose']), facts, ''.join('<li>%s</li>' % esc(f) for f in svc['formats'])))
    # "Why it works" sits on navy (the one dark band between the hero and the close); the step-by-step process band was retired
    why = ('<section class="band band--navy on-dark svc-why">\n  <div class="wrap"><div class="head"><span class="eyebrow">Why it works</span><h2 class="h2">%s</h2></div>'
           '<ul class="pillars">%s</ul></div>\n</section>'
           % (tt(svc['why_h2']), ''.join('<li class="pillar"><span class="svc-ic" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>' % (ICONS[k], esc(t), esc(d)) for k, t, d in svc['benefits'])))
    tiles = '\n'.join(svc_tile(piece(r)) for r in svc['gallery'])
    work = ('<section class="band svc-work" id="examples">\n  <div class="wrap"><div class="head"><span class="eyebrow">Examples of work</span><h2 class="h2">%s</h2>'
            '<p class="sub">Tap a frame to play it or see it at full size.</p></div>\n  <div class="masonry masonry--3" data-masonry role="list" aria-label="Examples of %s">\n%s\n  </div>'
            '<div class="more"><a class="btn btn--outline" href="{{ROOT}}portfolio.html">See all the work</a></div></div>\n</section>' % (tt(svc['examples_h2']), esc(name), tiles))
    cases = ('<section class="band band--wash svc-cases">\n  <div class="wrap"><div class="head"><span class="eyebrow">Case studies</span><h2 class="h2">Brands <span class="ai">That Use It.</span></h2></div>'
             '<ul class="cs-grid cs-grid--4 cs-grid--light">%s</ul><div class="more"><a class="btn" href="{{ROOT}}case-studies.html">All case studies</a></div></div>\n</section>'
             % ''.join(cs_card(s, light=True) for s in svc['cases']))
    faq = ('<section class="band faq" id="faq">\n  <div class="wrap"><div class="head"><span class="eyebrow">FAQ</span><h2 class="h2">Questions About <span class="ai">%s.</span></h2></div>%s</div>\n</section>'
           % (esc(name), qa_list(svc['faq'])))
    order = [s for s in SERVICES if s['slug'] != slug]
    i = next(n for n, s in enumerate(SERVICES) if s['slug'] == slug)
    others = (order[i:] + order[:i])[:5]
    more = ('<section class="band band--wash svc-more">\n  <div class="wrap"><div class="head"><span class="eyebrow">More services</span><h2 class="h2">Other Ways <span class="ai">to Make It.</span></h2></div>'
            '<ul class="svc-grid">%s</ul><div class="more"><a class="btn btn--outline" href="{{ROOT}}services.html">All services</a></div></div>\n</section>' % ''.join(svc_card(s) for s in others))
    if not svc['gallery']:   # nothing to show yet: no examples section, and no "See examples" button in the hero
        work = ''
        hero = hero.replace('<a class="btn btn--ghost" href="#examples">See examples</a>', '')
    if not svc['cases']:
        cases = ''
    if svc.get('radio') == 'ufl':
        # the Audio page's examples are one section in two parts (Mike, November 9, 2026): the UFL's game-day radio spots first, as on the UFL
        # case study, then the videos under their own heading
        work = ('<section class="band svc-work svc-work--audio" id="examples">\n  <div class="wrap">'
                '<div class="head" id="radio"><span class="eyebrow">On radio</span><h2 class="h2">%s</h2><p class="sub">%s</p></div>\n  %s\n'
                '  <div class="head head--next"><span class="eyebrow">In video</span><h2 class="h2">%s</h2><p class="sub">Tap a frame to play it or see it at full size.</p></div>\n'
                '  <div class="masonry masonry--3" data-masonry role="list" aria-label="Examples of %s">\n%s\n  </div>'
                '<div class="more"><a class="btn btn--outline" href="{{ROOT}}portfolio.html">See all the work</a></div></div>\n</section>'
                % (tt('Game-Day Radio |for the UFL.'), esc('Six of the spots we wrote, voiced and mixed for the league’s teams, most of them turned around in a day. Read how the season ran on the UFL case study.'),
                   radio_block(content['cases']['ufl']['copy']['radio']), tt(svc['examples_h2']), esc(name), tiles))
    inner = '\n\n'.join(x for x in [hero, intro, why, work, cases, faq, more, close_section('See the packages', '{{ROOT}}packages.html')] if x)
    return document('%s: Birdline' % name, svc['lede'], inner, '../')

# ---- the ROPS & ROCS page: what the two numbers are, why they are measured, what they are worth, and how the app measures them
def rops_why_section(eyebrow='Why we measure it', wash=False, heading='ROAS Leaves the Shoot |Out of the Math.', sub='Media gets measured to the dollar. The production that made the ad gets a line on an invoice. Two numbers close the gap.'):
    """why ROAS is not enough: what each number counts, then the question (on the ROPS page and the Production Planning page)"""
    cols = ''.join('<li class="cmp%s"><span class="cmp-k">%s%s</span><span class="cmp-f">%s</span><ul class="cmp-counts">%s</ul><p>%s</p></li>'
                   % (' cmp--ours' if code != 'ROAS' else '', esc(code), '<sup class="mark-tm">™</sup>' if code != 'ROAS' else '', esc(f),
                      ''.join('<li class="%s"><i aria-hidden="true">%s</i>%s</li>' % ('is-in' if on else 'is-out', CHECK if on else CROSS, esc(k)) for k, on in counts), esc(line))
                   for code, f, counts, line in COMPARE)
    return ('<!-- ===== Why ROAS is not enough: what each number counts ===== -->\n'
           '<section class="band%s rp-why">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2>'
           '<p class="sub">%s</p></div><ul class="cmp-row">%s</ul>'
           '<div class="rp-q"><p class="rp-q-main">%s</p></div></div>\n</section>'
           % (' band--wash' if wash else '', esc(eyebrow), tt(heading), esc(sub), cols, esc(QUESTION)))

def rops_diy_section():
    """measure your own, by hand or with the calculator (script.js binds the form); on the ROPS page and the Production Planning page"""
    return ('<!-- ===== Measure your own, by hand or with the calculator ===== -->\n'
           '<section class="band band--navy on-dark rp-diy" id="calculator">\n  <div class="wrap"><div class="head"><span class="eyebrow">Start here</span><h2 class="h2">Find Your ROPS<sup class="mark-tm">™</sup> &amp; ROCS<sup class="mark-tm">™</sup> <span class="ai">Below.</span></h2>'
           '<p class="sub">You can do this today with a calculator and last year’s campaigns. The app does it for every campaign, automatically.</p></div>'
           '<div class="diy"><div class="diy-steps"><span class="diy-k">By hand, for one shoot</span><ol class="steps steps--list">%s</ol></div>'
           '<div class="diy-calc"><span class="diy-k">Or plug in a campaign</span>%s</div></div></div>\n</section>'
           % (''.join('<li><span class="step-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(DIY)), calc_form()))

def rops_page():
    for key in ('ws-insights', 'ws-insights-m'):
        site_imgs.add(key + '.webp')
    def formula(code, name, num, dens, line):
        return ('<li class="fx"><span class="fx-k">%s<sup class="mark-tm">™</sup></span><span class="fx-name">%s</span>'
                '<span class="fx-eq" aria-label="%s equals %s divided by %s"><span class="fx-num">%s</span><span class="fx-den">%s</span></span><p>%s</p></li>'
                % (esc(code), esc(name), esc(code), esc(num), esc(' plus '.join(dens)), esc(num), ''.join('<b>%s</b>' % esc(d) for d in dens), esc(line)))
    hero = ('<!-- ===== ROPS & ROCS: the two numbers, as formulas, on navy ===== -->\n'
            '<section class="hero hero--page hero--rp on-dark" id="top">\n  <div class="wrap"><div class="hero-copy"><span class="eyebrow">ROPS<sup class="mark-tm">™</sup> &amp; ROCS<sup class="mark-tm">™</sup></span>'
            '<h1>%s</h1><p class="lede">%s</p>'
            '<div class="cta-row"><a class="btn btn--light" href="#calculator">Try the calculator</a><a class="btn btn--ghost" href="{{CALENDLY}}">Book a demo</a></div></div>'
            '<ul class="fx-row">%s</ul></div>\n</section>'
            % (tt(RP_HERO['h1']), esc(RP_HERO['lede']), ''.join(formula(*f) for f in FORMULAS)))
    why = rops_why_section()
    tells = ('<section class="band band--wash rp-tells">\n  <div class="wrap"><div class="head"><span class="eyebrow">What it tells you</span><h2 class="h2"><span class="nowrap">Five Things You Can’t See</span> <span class="ai">in Standard Performance Reports.</span></h2></div>'
             '<ol class="tells">%s</ol></div>\n</section>'
             % ''.join('<li><span class="tell-n" aria-hidden="true">%02d</span><div class="tell-body"><h3>%s</h3><p>%s</p></div><span class="svc-ic" aria-hidden="true">%s</span></li>' % (i + 1, esc(t), esc(d), ICONS[k]) for i, (k, t, d) in enumerate(TELLS)))
    story = ('<!-- ===== The $40K spot, and what happened after it ===== -->\n'
             '<section class="band band--navy on-dark rp-story">\n  <div class="wrap"><div class="story-grid"><div class="story-copy"><span class="eyebrow">Why it matters</span>'
             '<h2 class="h2">A $40K Spot. $14.7M Back. <span class="ai">Then the Clarity Was Gone.</span></h2><p>%s</p>'
             '<ul class="story-stats">%s</ul></div>'
             '<div class="story-then"><span class="then-k">What happened over the next three years</span><ol class="then-list">%s</ol></div></div>'
             '<div class="story-lesson"><p>%s</p><p class="story-ask">%s</p></div></div>\n</section>'
             % (esc(STORY_LEDE), ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(n), esc(t)) for n, t in STORY_STATS),
                ''.join('<li>%s</li>' % esc(t) for t in STORY_THEN), esc(STORY_LESSON[0]), esc(STORY_LESSON[1])))
    rows = []
    for i, (n, title, text, d, m, alt) in enumerate(MEASURE):
        if d.startswith('ws-'):
            dimg = '<img class="d-only" src="{{ROOT}}img/%s.webp" width="2400" height="1566" alt="%s" loading="lazy"><img class="m-only" src="{{ROOT}}img/%s.webp" width="1320" height="1153" alt="%s" loading="lazy">' % (d, esc(alt), m, esc(alt))
        else:
            dw, dh = asset_wh(d); mw, mh = asset_wh(m)
            dimg = '<img class="d-only" src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy"><img class="m-only" src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy">' % (asset(d), dw, dh, esc(alt), asset(m), mw, mh, esc(alt))
        rows.append('<div class="fr%s"><div class="fr-copy"><span class="step-n">%s</span><h3>%s</h3><p>%s</p></div><figure class="fr-screen vig--3">%s</figure></div>'
                    % (' fr--flip' if i % 2 else '', esc(n), esc(title), esc(text), dimg))
    measure = ('<!-- ===== How the app measures it ===== -->\n'
               '<section class="band rp-measure" id="how">\n  <div class="wrap"><div class="head"><span class="eyebrow">How we measure it</span><h2 class="h2">Measured Where the Work Happens: <span class="ai">the Birdline App.</span></h2>'
               '<p class="sub">The brief supplies the cost. The ads you connect supply the revenue. Nothing is re-keyed into a spreadsheet, so the number is there on every campaign, every day.</p></div>%s'
               '<p class="fine">Product screens show sample data from a demo workspace.</p></div>\n</section>' % ''.join(rows))
    diy = rops_diy_section()
    numbers = ('<section class="band rp-numbers">\n  <div class="wrap"><div class="head"><span class="eyebrow">What it’s worth</span><h2 class="h2">The Numbers <span class="ai">So Far.</span></h2>'
               '<p class="sub">The brands that keep scaling aren’t the ones generating the most content. They’re the ones who know exactly what their content is worth.</p></div>'
               '<ul class="rp-nums">%s</ul><p class="fine">%s</p></div>\n</section>'
               % (''.join('<li><b>%s</b><p>%s</p></li>' % (esc(n), esc(t)) for n, t in NUMBERS), esc(NUMBERS_NOTE)))
    faq = ('<section class="band band--wash faq" id="faq">\n  <div class="wrap"><div class="head"><span class="eyebrow">FAQ</span><h2 class="h2">Questions About <span class="ai">ROPS<sup class="mark-tm">™</sup> and ROCS<sup class="mark-tm">™</sup>.</span></h2></div>%s</div>\n</section>' % qa_list(RP_FAQ))
    close = close_section('Book a demo', '{{CALENDLY}}', heading='Build Winning Campaigns with a Bird’s-Eye View',
                          sub='Bring the campaign you’re working on now. Start free for 30 days, no credit card required.',
                          first=('Start free trial', 'https://app.birdline.ai/login?mode=signup'))
    inner = '\n\n'.join([hero, why, tells, measure, diy, faq, close])
    return document('ROPS™ & ROCS™: Birdline', 'ROPS™ (Return on Production Spend) and ROCS™ (Return on Campaign Spend): what they are, why Birdline measures them on every campaign, what they are worth, and how the Birdline App measures them.', inner, '')

# ---- the Production Planning page (November 3, 2026): how a shoot runs for commercial, photo and UGC-style work, the content library
# (the board from the About page), the productions add-on, and ROPS & ROCS with the calculator
def production_page():
    hero = ('<!-- ===== Production Planning: the copy on navy, over a still from a Birdline set ===== -->\n'
            '<section class="hero hero--page hero--why hero--prod on-dark" id="top">\n'
            '  <div class="hero-media" aria-hidden="true"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" fetchpriority="high"></div>\n'
            '  <div class="wrap"><div class="hero-copy"><a class="crumb" href="{{ROOT}}services.html">%sAll services</a>'
            '<span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="#library">See a year of content</a></div></div></div>\n</section>'
            % (site_img('new/production-hero.jpg') + (ARROW_L, esc(PD_HERO['eyebrow']), tt(PD_HERO['h1']), esc(PD_HERO['lede']))))
    anywhere = ('<!-- ===== Crews wherever the shoot is ===== -->\n'
                '<section class="band band--wash pd-anywhere" id="anywhere">\n  <div class="wrap"><div class="head"><span class="eyebrow">Anywhere</span><h2 class="h2">%s</h2><p class="sub">%s</p></div>'
                '<ul class="places" aria-label="Where we shoot">%s</ul><ul class="pillars">%s</ul></div>\n</section>'
                % (tt(ANYWHERE_H2), esc(ANYWHERE_SUB), ''.join('<li><i aria-hidden="true"></i>%s</li>' % esc(x) for x in PLACES),
                   ''.join('<li class="pillar"><span class="svc-ic" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>' % (ICONS[k], esc(t), esc(d)) for k, t, d in ANYWHERE)))
    library = library_section()
    steps = ''.join('<li><span class="step-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(PROCESS))
    process = ('<section class="band band--navy on-dark svc-process pd-process" id="process">\n  <div class="wrap"><div class="head"><span class="eyebrow">How a production runs</span><h2 class="h2">From the Call <span class="ai">to the Library.</span></h2>'
               '<p class="sub">%s</p></div><ol class="steps">%s</ol></div>\n</section>' % (esc(PROCESS_SUB), steps))
    pf, pw, ph = site_img('2025/09/PublicRec-DTLA-DD-33.jpeg')
    inner = '\n\n'.join([hero, library, anywhere, process, rops_why_section('How we measure productions', wash=True, heading=RP_HERO['h1'], sub=RP_HERO['lede']), rops_diy_section(), close_section('See the packages', '{{ROOT}}packages.html', photo=(pf, pw, ph))])
    return document('Production Process: Birdline', 'How Birdline plans and runs full-service productions for commercial, photo and UGC-style shoots: scoped per project, planned in the Birdline App, crewed wherever the shoot is, and built so one day on set feeds campaigns for years.', inner, '../')

# ---- How It Works (reworked November 9, 2026): Mike's copy for how a partnership runs, in the site's own vocabulary. A navy hero
# over the set photo; the takeaway first as three pillars and a row of numbers; the six steps on navy; the three tools; three
# production tiles; the Birds beside their copy; ROPS and ROCS as two cards on navy; four case cards; the FAQ; the close.
TEAM_BY_KEY = {k: (name, role) for k, name, role, _ in TEAM}
ARROW_GO = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 10h12M11 5l5 5-5 5"></path></svg>'

def hw_link(label, href):
    return '<a class="hw-link" href="%s">%s%s</a>' % (href, esc(label), ARROW_GO)

def how_page():
    h = HW.HERO
    hero = ('<!-- ===== How it works: the copy on navy, over a still from a Birdline set ===== -->\n'
            '<section class="hero hero--page hero--why hero--how on-dark" id="top">\n'
            '  <div class="hero-media" aria-hidden="true"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="" fetchpriority="high"></div>\n'
            '  <div class="wrap"><div class="hero-copy"><span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p>'
            '<div class="cta-row"><a class="btn btn--light" href="{{CALENDLY}}">Book a call</a><a class="btn btn--ghost" href="{{ROOT}}packages.html">See the packages</a></div></div></div>\n</section>'
            % (site_img(h['photo']) + (esc(h['eyebrow']), tt(h['h1']), esc(h['lede']))))
    sh = HW.SHORT
    moves = ''.join('<li class="pillar hw-move"><span class="hw-n">%d</span><span class="svc-ic" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>'
                    % (i + 1, ICONS[k], esc(t), esc(d)) for i, (k, t, d) in enumerate(sh['steps']))
    stats = ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(n), esc(d)) for n, d in sh['stats'])
    short = ('<!-- ===== The takeaway: three moves, then the numbers ===== -->\n'
             '<section class="band band--wash hw-short" id="in-short">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="sub">%s</p></div>'
             '<ol class="pillars hw-moves">%s</ol><ul class="hw-stats" aria-label="The partnership in numbers">%s</ul></div>\n</section>'
             % (esc(sh['eyebrow']), tt(sh['h2']), esc(sh['sub']), moves, stats))
    rn = HW.RUN
    steps = ''.join('<li><span class="step-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(rn['steps']))
    run = ('<!-- ===== How a partnership runs: six steps on navy ===== -->\n'
           '<section class="band band--navy on-dark svc-process hw-run" id="how">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="sub">%s</p></div><ol class="steps">%s</ol></div>\n</section>'
           % (esc(rn['eyebrow']), tt(rn['h2']), esc(rn['sub']), steps))
    tl = HW.TOOLS
    tools = ('<!-- ===== The three tools ===== -->\n'
             '<section class="band hw-tools" id="tools">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="sub">%s</p></div><ul class="pillars">%s</ul></div>\n</section>'
             % (esc(tl['eyebrow']), tt(tl['h2']), esc(tl['sub']),
                ''.join('<li class="pillar"><span class="svc-ic" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>' % (ICONS[k], esc(t), esc(d)) for k, t, d in tl['pillars'])))
    sp = HW.SHOOT
    tiles = ''.join('<li><figure><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy"></figure><div class="hw-tile-copy"><h3>%s</h3><p>%s</p>%s</div></li>'
                    % (site_img(src) + (esc(sp['alts'][i]), esc(t), esc(d), hw_link(l, href))) for i, (src, t, d, l, href) in enumerate(sp['tiles']))
    shoot = ('<!-- ===== Productions: three tiles ===== -->\n'
             '<section class="band band--wash hw-shoot" id="productions">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="sub">%s</p></div><ul class="hw-tiles">%s</ul></div>\n</section>'
             % (esc(sp['eyebrow']), tt(sp['h2']), esc(sp['sub']), tiles))
    bd = HW.BIRDS
    for k in bd['faces']:
        site_imgs.add('bird-%s.webp' % k)
    faces = ''.join('<li><img src="{{ROOT}}img/bird-%s.webp" width="400" height="400" alt="" loading="lazy"><b>%s</b><span>%s</span></li>' % (k, esc(TEAM_BY_KEY[k][0]), esc(TEAM_BY_KEY[k][1])) for k in bd['faces'])
    birds = ('<!-- ===== The Birds, beside six of them ===== -->\n'
             '<section class="band hw-birds" id="birds">\n  <div class="wrap"><div class="hw-split"><div class="hw-copy"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="sub">%s</p>'
             '<ul class="hw-bullets">%s</ul><a class="btn" href="%s">%s</a></div><ul class="hw-faces" aria-label="Some of the Birds">%s</ul></div></div>\n</section>'
             % (esc(bd['eyebrow']), tt(bd['h2']), esc(bd['para']), ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in bd['bullets']), bd['href'], esc(bd['link']), faces))
    rt = HW.RETURNS
    cards = ''.join('<li><span class="hw-rate-k">%s<sup class="mark-tm">™</sup></span><b>%s</b><p>%s</p></li>' % (esc(k), esc(t), esc(d)) for k, t, d in rt['cards'])
    returns = ('<!-- ===== ROPS and ROCS as two cards on navy ===== -->\n'
               '<section class="band band--navy on-dark hw-returns" id="returns">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="sub">%s</p></div>'
               '<ul class="hw-rates">%s</ul><p class="hw-tail">%s</p><div class="more"><a class="btn btn--light" href="%s">%s</a></div></div>\n</section>'
               % (esc(rt['eyebrow']), tt(rt['h2']), esc(rt['sub']), cards, esc(rt['tail']), rt['href'], esc(rt['link'])))
    cs = HW.CASES
    cases = ('<!-- ===== Four case studies ===== -->\n'
             '<section class="band band--wash svc-cases hw-cases" id="clients">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2></div>'
             '<ul class="cs-grid cs-grid--4 cs-grid--light">%s</ul><div class="more"><a class="btn" href="{{ROOT}}case-studies.html">All case studies</a></div></div>\n</section>'
             % (esc(cs['eyebrow']), tt(cs['h2']), ''.join(cs_card(slug, light=True) for slug in cs['slugs'])))
    fq = HW.FAQ
    qa = []
    for q in fq['items']:
        block = faq_items.get(q) or next((v for k, v in faq_items.items() if q in k), None)
        if not block:
            raise SystemExit('no FAQ item: ' + q)
        qa.append(re.sub(r' open="open"', '', block))
    faq = ('<!-- ===== FAQ ===== -->\n'
           '<section class="band faq" id="faq">\n  <div class="wrap"><div class="head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2></div><div class="faq-list">%s</div></div>\n</section>'
           % (esc(fq['eyebrow']), tt(fq['h2']), '\n'.join(qa)))
    close = close_section('See the packages', '{{ROOT}}packages.html', heading=HW.CLOSE['heading'], sub=HW.CLOSE['sub'], photo=site_img(HW.CLOSE['photo']))
    inner = '\n\n'.join([hero, short, run, tools, shoot, birds, returns, cases, faq, close])
    return document('How It Works: Birdline', 'How a Birdline partnership runs: you send briefs in Slack or the Birdline App, our Birds make the work, finals land in your library, and we meet every other week to decide what is next. Unlimited deliverables, productions shot for the library, and results traced back to the creative.', inner, '')

# ---- the homepage, with its images as files and its links pointing at the new pages
# ---- the homepage hero: two rows of Work-page pieces at their own proportions, each opening in the lightbox (November 3, 2026).
# A video is named by its Vimeo id (its curated still, playing from the library); a photograph or design by its still.
# The hero's two rows (November 5, 2026): the seven photos that were there, and the videos Mike picked, by Vimeo id or by the
# file name of a file-backed piece. Wide, square and vertical frames alternate, and no brand sits next to itself, the loop's
# seam included (a row's first and last frames meet). Public Rec's Zero Short came out November 6, 2026: its still is the same
# DTLA scene as All Day Every Day's, so the two read as one video shown twice.
HOME_HERO = [
    ['1119136322', 'grantpuckett-studio-product.webp', 'whoop-behind-the-drivers-seat-lewis.mp4', '984139678', '1217480327', 'edjy-01.mp4', '1000153543', 'protect-static-v2.webp', '847156288',
     'wr-3d-social.mp4', '1116472030', '1087155996', 'grantpuckett-product.webp', '863369992', '833777565', '753024501', 'grantpuckett-active-4.webp', '727974264'],
    ['640557935', 'gardyn-ugc-hana-new-year.mp4', 'whoop-al-standalone-4x5.mp4', '1217481666', 'grantpuckett-product-36.webp', '776002616', 'literati-f26-promo.mp4', 'publicrec-ugc-anton-dealmaker.mp4',
     '983994096', 'grant-puckett-ab-9.webp', 'wr-3d-bottle-swap.mp4', '876232748', '1000128286', '892462752', 'edjy-16.mp4', 'c4cr-unboxing-moments-1x1-v2-1.webp', '895391449'],
]
HERO_PACE = [7.2, 9.0]   # seconds per tile-height of track, per row: the rows keep the speeds they had with ten tiles each
def hero_marquee():
    by_file = {}
    for _pane in content['portfolio']['panes']:
        for _it in _pane['items']:
            if _it.get('src') in imap: by_file.setdefault(imap[_it['src']]['file'], ('design' if _pane['id'] == 'graphic' else 'photo', _it))
    for _slug, _cs in content['cases'].items():
        for _it in _cs.get('gal', []):
            if _it.get('src') in imap: by_file.setdefault(imap[_it['src']]['file'], ('photo', dict(_it, alt=_it.get('alt') or CARDS[_slug]['brand'])))
    file_items = {}   # the file-backed pieces, by file name
    for _lst in list(ADDED_WORK.values()) + [AI_WORK] + [_cs.get('gal', []) for _cs in content['cases'].values()]:
        for _it in _lst:
            if isinstance(_it, dict) and _it.get('video'): file_items.setdefault(_it['video'], _it)
    def tile(key):
        if key.isdigit():
            it = VIDEO_ITEMS[key]; info = hosted(key)
            f, w, h = site_img(POSTERS[key]) if key in POSTERS else site_img(it['src'])
            label = it.get('alt') or brand_of(it['src']) or info['title']
            return ('<li class="m-tile" style="--asp:%.4f"><a %s aria-label="%s"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy">'
                    '<span class="m-play" aria-hidden="true">%s</span></a></li>' % (w / h, play_attrs(key, label, f), esc('Play: ' + label), f, w, h, esc(label + ' — video still'), PLAY))
        if key.endswith('.mp4'):
            it = file_items[key]; site_videos.add(key); f, w, h = site_img(it['poster'])
            return ('<li class="m-tile" style="--asp:%.4f"><a %s aria-label="%s"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy">'
                    '<span class="m-play" aria-hidden="true">%s</span></a></li>'
                    % (it['w'] / it['h'], play_attrs(None, it['alt'], f, file=key, w=it['w'], h=it['h']), esc('Play: ' + it['alt']), f, w, h, esc(it['alt'] + ' — video still'), PLAY))
        kind, it = by_file[key]; f, w, h = site_img(it['src'])
        label = it.get('alt') or brand_of(it['src']) or ('Design' if kind == 'design' else PHOTO_KIND_BY_SRC.get(it['src'], 'Photograph'))
        what = 'Design' if kind == 'design' else 'Photo'
        return ('<li class="m-tile" style="--asp:%.4f"><a href="{{ROOT}}img/%s" data-lb="image" data-title="%s" data-kind="%s" target="_blank" aria-label="%s"><img src="{{ROOT}}img/%s" width="%d" height="%d" alt="%s" loading="lazy">'
                '<span class="m-play" aria-hidden="true">%s</span></a></li>' % (w / h, f, esc(label), what, esc(label + ' at full size'), f, w, h, esc(label), ZOOM))
    rows = []
    for i, keys in enumerate(HOME_HERO):
        tiles = ''.join(tile(k) for k in keys)
        span = sum(float(x) for x in re.findall(r'--asp:([0-9.]+)', tiles))   # the set's width in tile heights
        rows.append('<div class="m-row m-row--%s"><div class="m-track" style="animation-duration:%ds"><ul class="m-set">%s</ul><ul class="m-set" aria-hidden="true">%s</ul></div></div>'
                    % ('l' if i == 0 else 'r', round(span * HERO_PACE[i]), tiles, tiles.replace('<a ', '<a tabindex="-1" ')))
    return '<div class="marquee" aria-label="Selected work">\n    %s\n  </div>' % '\n    '.join(rows)

def home_page(artifact):
    inner = body[body.index('<main>') + len('<main>'):body.index('</main>')]
    _ms = inner.find('<div class="marquee"'); _me = inner.find('</section>', _ms)
    inner = inner[:_ms] + hero_marquee() + '\n' + inner[_me:]
    _ls = inner.find('<ul class="lib-tiles"'); _le = inner.find('</ul>', _ls) + len('</ul>')
    inner = inner[:_ls] + lib_tiles_html() + inner[_le:]
    inner = resolve_imgs(inner)
    for _slug, _c in CARDS.items():   # the case cards whose cover is a loop get it here too, over the still
        if _c.get('loop'):
            inner = re.sub(r'(<span class="cs-media"><img src="\{\{ROOT\}\}img/%s[^>]*>)' % re.escape(asset(_c['cover'])), lambda m: m.group(1) + cover_loop(_slug), inner, count=1)
    page = '<div class="page">\n' + header + '\n<main>\n' + inner + '\n</main>\n' + footer + '\n' + LIGHTBOX + '\n' + BOOK + '\n</div>'
    page = relink(page, '', True, hashes=artifact)
    title = 'Birdline: Unlimited Deliverables. One Production Workspace.'
    description = ('Birdline pairs a premium creative studio with a production workspace: unlimited deliverables every month, '
                   'and the revenue every production earned, in one place.')
    if NEXT and not artifact:
        DOCS.append(dict(title=title, description=description, html=relink(inner, '/', True, clean=True)))
    if artifact:
        # one document: the router fetches the other pages' content from the files published alongside it
        router = open(os.path.join(HERE, 'spa.js'), encoding='utf-8').read()
        return ('<title>Birdline Homepage</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n%s\n<style>\n%s</style>\n%s\n<script>\n%s\n%s</script>\n'
                % (FONTS, style, page, script, router))
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n%s\n<style>\n%s</style>\n</head>\n<body>\n%s\n<script>\n%s</script>\n</body>\n</html>\n'
            % (title, description, FONTS, style, page, script))

pages = {'index.html': home_page(False), 'index-artifact.html': home_page(True), 'portfolio.html': portfolio_page(), 'case-studies.html': index_page(), 'packages.html': packages_page(), 'about.html': about_page(), 'workspace.html': workspace_page()}
for slug in ORDER:
    pages['case-studies/%s.html' % slug] = case_page(slug)
pages['services.html'] = services_page()
pages['why-us.html'] = why_page()
pages['rops.html'] = rops_page()
pages['services/production-process.html'] = production_page()
pages['how-it-works.html'] = how_page()
for svc in SERVICES:
    pages['services/%s.html' % svc['slug']] = service_page(svc)
for _slug, _eyebrow, _title, _updated, _desc in DOC_PAGES:
    pages[_slug + '.html'] = doc_page(_slug, _eyebrow, _title, _updated, _desc)
if site_videos:
    os.makedirs(os.path.join(OUT, 'video'), exist_ok=True)
    for f in site_videos:
        src = os.path.join(HERE, 'video', f)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(OUT, 'video', f))
    _absent = sorted(f for f in site_videos if not os.path.exists(os.path.join(HERE, 'video', f)))
    with open(os.path.join(OUT, 'video', 'NEEDED.txt'), 'w') as fh:
        fh.write('\n'.join(_absent) + '\n')
    print('videos: %d copied, %d to add from the library (video/NEEDED.txt)' % (len(site_videos) - len(_absent), len(_absent)))
for f in list(site_imgs):
    src = os.path.join(HERE, 'img', f)
    if os.path.exists(src) and not os.path.exists(os.path.join(OUT, 'img', f)):
        shutil.copyfile(src, os.path.join(OUT, 'img', f))
# img/ holds only what the pages use
used = set(asset_ext[k] and k + asset_ext[k] for k in asset_ext) | site_imgs
for f in os.listdir(os.path.join(OUT, 'img')):
    if f not in used:
        os.remove(os.path.join(OUT, 'img', f))

# the artifact's copies of the pages (index-artifact.html and _artifact/<page>) carry the small repeated images (testimonial avatars,
# role-card faces, integration icons, team photos, brand logos) as data URIs rather than files: the artifact holds at most 511
# files. The site's own pages keep them as files in img/.
import base64
INLINE_SMALL = re.compile(r'src="[^"]*?img/((?:av|cr|int|team|logo2)-[a-z0-9-]+\.(?:webp|png|svg)|bird-white\.png)"')
_inline = {}
_MIME = {'webp': 'image/webp', 'png': 'image/png', 'svg': 'image/svg+xml'}
def inline_small(text):
    def rep(m):
        f = m.group(1)
        if f not in _inline:
            with open(os.path.join(OUT, 'img', f), 'rb') as fh:
                _inline[f] = 'data:%s;base64,%s' % (_MIME[f.rsplit('.', 1)[1]], base64.b64encode(fh.read()).decode('ascii'))
        return 'src="%s"' % _inline[f]
    return INLINE_SMALL.sub(rep, text)
os.makedirs(os.path.join(OUT, '_artifact', 'case-studies'), exist_ok=True); os.makedirs(os.path.join(OUT, '_artifact', 'services'), exist_ok=True)
for name, text in pages.items():
    if name == 'index-artifact.html':
        text = inline_small(text)
    elif name != 'index.html':
        with open(os.path.join(OUT, '_artifact', name), 'w', encoding='utf-8') as f:
            f.write(inline_small(text))
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(text)
    print('%-32s %7d bytes' % (name, len(text.encode())))
with open(os.path.join(OUT, '_artifact', 'INLINED.txt'), 'w') as fh:
    fh.write('\n'.join(sorted(_inline)) + '\n')
print('artifact pages inline %d small images (_artifact/INLINED.txt)' % len(_inline))
print('images:', len(used), 'homepage assets:', len(asset_ext), 'site images:', len(site_imgs))

# ---- the Next.js project: content/ (the page fragments, their routes, the header/footer/lightbox), app/globals.css, public/js, public/img,
# public/video (only the files the library has here; the rest come from the Mac's site folder; content/videos.txt lists them all)
if NEXT:
    names = [n for n in pages if n != 'index-artifact.html']
    assert len(names) == len(DOCS), (len(names), len(DOCS))
    cdir = os.path.join(NEXT, 'content', 'pages')
    os.makedirs(cdir, exist_ok=True)
    for f in os.listdir(cdir):
        os.remove(os.path.join(cdir, f))
    # Every image goes out under a name that carries its content hash (bird-mike.3f9c1e2a.webp), and the pages point at that
    # name: a replaced photo is a new address, so no browser or CDN keeps showing the old one, and the files themselves can be
    # cached for good (next.config.ts marks /img immutable).
    fingerprints = {}
    for f in used:
        with open(os.path.join(OUT, 'img', f), 'rb') as fh:
            digest = hashlib.md5(fh.read()).hexdigest()[:8]
        stem, ext = os.path.splitext(f)
        fingerprints[f] = '%s.%s%s' % (stem, digest, ext)
    def fingerprint(text):
        return re.sub(r'/img/([A-Za-z0-9._-]+)', lambda m: '/img/' + fingerprints.get(m.group(1), m.group(1)), text)
    manifest = []
    for name, doc in zip(names, DOCS):
        route = route_for(name)
        file = ('index' if route == '/' else route.strip('/').replace('/', '__')) + '.html'
        with open(os.path.join(cdir, file), 'w', encoding='utf-8') as fh:
            fh.write(fingerprint(doc['html'].strip()) + '\n')
        manifest.append(dict(route=route, file=file, title=doc['title'], description=doc['description']))
    with open(os.path.join(NEXT, 'content', 'pages.json'), 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, indent=1, ensure_ascii=False)
    def element(frag):
        """one element as the layout renders it: its tag, its attributes (class as className) and its inner HTML"""
        frag = frag.strip()
        m = re.match(r'<(\w+)((?:\s+[^\s=>]+(?:="[^"]*")?)*)\s*>', frag)
        attrs = {('className' if k == 'class' else k): v for k, v in re.findall(r'([^\s=]+)(?:="([^"]*)")?', m.group(2))}
        close = '</%s>' % m.group(1)
        return dict(tag=m.group(1), attrs=attrs, html=frag[m.end():frag.rindex(close)].strip())
    _hd = relink(header, '/', False, clean=True)
    chrome = dict(fonts=re.findall(r'href="([^"]+)"', FONTS.replace('&amp;', '&')),
                  topMark=element(_hd[:_hd.index('<header')]), header=element(_hd[_hd.index('<header'):]),
                  footer=element(relink(footer, '/', False, clean=True)), lightbox=element(LIGHTBOX), book=element(relink(BOOK, '/', False, clean=True)))
    with open(os.path.join(NEXT, 'content', 'chrome.json'), 'w', encoding='utf-8') as fh:
        fh.write(fingerprint(json.dumps(chrome, indent=1, ensure_ascii=False)))
    with open(os.path.join(NEXT, 'content', 'videos.txt'), 'w') as fh:
        fh.write('\n'.join(sorted(site_videos)) + '\n')
    os.makedirs(os.path.join(NEXT, 'app'), exist_ok=True)
    with open(os.path.join(NEXT, 'app', 'globals.css'), 'w', encoding='utf-8') as fh:
        fh.write(style)
    os.makedirs(os.path.join(NEXT, 'public', 'js'), exist_ok=True)
    with open(os.path.join(NEXT, 'public', 'js', 'birdline.js'), 'w', encoding='utf-8') as fh:
        fh.write(script)
    pub_img = os.path.join(NEXT, 'public', 'img'); os.makedirs(pub_img, exist_ok=True)
    for f in used:
        dst = os.path.join(pub_img, fingerprints[f])
        if not os.path.exists(dst):
            shutil.copyfile(os.path.join(OUT, 'img', f), dst)
    _keep = set(fingerprints.values())
    for f in os.listdir(pub_img):
        if f not in _keep:
            os.remove(os.path.join(pub_img, f))
    pub_vid = os.path.join(NEXT, 'public', 'video'); os.makedirs(pub_vid, exist_ok=True)
    _vcopied = 0
    for f in sorted(site_videos):
        src, dst = os.path.join(OUT, 'video', f), os.path.join(pub_vid, f)
        if os.path.exists(src) and not (os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src)):
            shutil.copyfile(src, dst); _vcopied += 1
    print('next.js: %d pages -> %s/content, %d images, %d videos listed (%d copied now)' % (len(manifest), NEXT, len(used), len(site_videos), _vcopied))
