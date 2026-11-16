"""The team calculator (November 15, 2026), in the blog post "Why Wouldn't I Just Hire a Full-Time Team?": the team a brand
would need on payroll for its ad volume and shoots, what that team costs, and the same output on a Birdline partnership.

One model, written twice: here (model() and view(), which render the calculator as it opens and supply the figures the post
quotes) and in site.js (the same two functions, which redraw it as the inputs move). CONFIG goes to the page as JSON in
data-teamcalc, so the numbers live in one place. The two must agree line for line; the check in the build notes runs both
over a grid of inputs.

CONFIG['v'] is the model's version, and site.js carries the same number (TEAMCALC_V; the build stops if they differ). A page and
a script from different deployments can meet in a visitor's browser (a cached script, a restored tab): when the roles changed
on November 15, 2026 that pairing drew "$NaN". The script now leaves alone a calculator whose version is not its own and loads
the page again once, so the two match. Raise the number whenever the roles, the fields or the names of the figures change.

The figures and where they come from:
- salaries: BLS Occupational Employment and Wage Statistics, May 2025, U.S. The two makers are priced at senior level, the
  75th percentile, because every Birdline editor and designer/animator is senior or expert level (Mike, November 15, 2026):
  film and video editors $105,310 (median $75,420); graphic designers $81,830 and special effects artists and animators
  $139,130, whose midpoint, $110,480, rounded to $110,500, stands for a senior designer who also animates. The one support
  role, the producer / project manager, stays at the median: producers and directors $90,360. The copywriter and the creative
  director left on November 15, 2026 (Mike: Birdline is not out to replace them), and creative strategy is not a seat of its
  own: a creative strategist for creative marketing is always included with Birdline and is part of the producer / project
  manager's role (Mike, the same day), so the payroll side counts one hire for both
- benefits and payroll taxes: BLS Employer Costs for Employee Compensation, June 2026, full-time private industry workers:
  insurance $4.58 + retirement and savings $1.94 + legally required $3.76 = $10.28 an hour, against $36.97 in wages plus $4.40
  in paid leave (which a salary already includes) = $41.37, or 24.8%. Bonuses and other supplemental pay are left out.
- software and equipment: $2,500 a seat a year (Adobe Creative Cloud Pro for teams lists at $99.99 a month; the rest is a
  workstation over a few years and stock)
- workflow tools: $300 a person a year, a project tracker and a review tool (Asana Starter lists at $10.99 a user a month billed
  annually, Frame.io Pro at $15 a member a month: $311.88 a year). On the Birdline side the Birdline App and Frame.io review are
  included in every partnership (the Packages page)
- the start (November 15, 2026, with the Birdline App): a seat takes 39 days to fill at the median (SHRM, 2026), and Birdline
  starts within a week (the Packages and How It Works pages). "Ads shipped in the first 90 days" gives each side its full
  monthly rate from the day it starts, every seat searched at once: generous to the payroll side
- drives: editors cut from portable SSDs and the footage is backed up to hard drives. Two 4TB SSDs per video editor a year
  ($936.98 each at B&H, November 2026: $1,900) and one 8TB desktop hard drive per production ($279.99 at B&H: $280). On the
  Birdline side the drives are ours
- Birdline: the starting prices on the Packages page, one package per dedicated creative
- productions: one budget per shoot, the same on both sides
- output per person is an average (Mike, November 15, 2026): 20 finished video ads a month for an editor, 50 statics or motion
  pieces for a designer. With unlimited deliverables the real number moves with the edit requests
- the rules that staff the team are Birdline's working assumptions, stated in the post and open to change in the calculator"""
import json
from math import ceil, floor

CONFIG = dict(
    sizes=['1–10', '11–50', '51–200', '201–500', '501–1,000', '1,000+'],     # employees, as the booking form asks
    v=5,                                       # the model's version; site.js carries the same number (see the note above)
    roles=[('editor', 'Senior video editor', 105310), ('designer', 'Senior designer / animator', 110500), ('producer', 'Producer / project manager', 90360)],
    cap=dict(editor=20, designer=50),          # finished ads one person ships a month, on average
    load=25,                                   # benefits and payroll taxes, percent of salary
    seat=2500,                                 # software and equipment, per person per year
    tools=300,                                 # workflow tools, per person per year: a project tracker and a review tool
    ssd=1900,                                  # editing SSDs, per video editor per year: two 4TB portable SSDs
    backup=280,                                # a backup hard drive for each production's footage: one 8TB desktop drive
    shoot=20000,                               # budget per production: crew, talent, locations, gear
    fill=39,                                   # days to fill a seat: SHRM's 2026 median time-to-fill, nonexecutive roles
    onboard=7,                                 # days before a Birdline partnership starts: within a week
    window=90,                                 # the days counted in "ads shipped in the first 90 days"
    price=dict(editor=8000, designer=6000),    # Birdline, per dedicated creative per month (Video Editing, Design & Animation)
    ads=(5, 200, 5), shoots=(0, 24, 1), design=(0, 100, 25),      # the sliders: min, max, step
    start=dict(size=2, ads=40, shoots=4, design=50),              # how the calculator opens
)
ROLE_KEYS = [k for k, _n, _s in CONFIG['roles']]
SUPPORT = ['producer']

def start_state():
    s = dict(CONFIG['start'])
    s.update(salary={k: v for k, _n, v in CONFIG['roles']}, cap=dict(CONFIG['cap']), load=CONFIG['load'], seat=CONFIG['seat'],
             tools=CONFIG['tools'], ssd=CONFIG['ssd'], backup=CONFIG['backup'], shoot=CONFIG['shoot'], fill=CONFIG['fill'],
             over={k: None for k in SUPPORT})
    return s

def rnd(x):
    """round half up, as Math.floor(x + 0.5) does in site.js"""
    return int(floor(x + 0.5))

def money(n):
    return '$' + format(int(n), ',')

def model(s):
    video = rnd(s['ads'] * (100 - s['design']) / 100)
    design = s['ads'] - video
    n = dict(editor=ceil(video / s['cap']['editor']) if video else 0, designer=ceil(design / s['cap']['designer']) if design else 0)
    makers = n['editor'] + n['designer']
    auto = dict(producer=0)
    two = makers >= 2     # a lone maker is managed by whoever hired them, at any company size
    if (s['size'] >= 1 and two) or makers >= 3 or s['shoots'] >= 6:      # someone has to run the queue, the shoots and the creative strategy
        auto['producer'] = max(1, ceil(makers / 8)) + (1 if s['shoots'] >= 12 else 0)   # a shoot a month is a job of its own
    for k in SUPPORT:
        o = s['over'][k]
        n[k] = auto[k] if o is None else (max(auto[k], 1) if o else 0)
    heads = sum(n.values())
    salaries = sum(n[k] * s['salary'][k] for k in ROLE_KEYS)
    benefits = rnd(salaries * s['load'] / 100)
    seats = heads * s['seat']
    drives = n['editor'] * s['ssd'] + s['shoots'] * s['backup']     # SSDs to edit from, and a backup of each production's footage
    flow = heads * s['tools']     # a tracker and a review tool for each person; the Birdline App covers it on a partnership
    team = salaries + benefits + seats + flow + drives
    shoots = s['shoots'] * s['shoot']
    monthly = n['editor'] * CONFIG['price']['editor'] + n['designer'] * CONFIG['price']['designer']
    partner = monthly * 12
    # the first 90 days: each side ships at its full monthly rate from the day it starts (a search on payroll, a week with Birdline)
    ramp_in = rnd(s['ads'] * max(0, CONFIG['window'] - s['fill']) / 30)
    ramp_bl = rnd(s['ads'] * (CONFIG['window'] - CONFIG['onboard']) / 30)
    return dict(video=video, design=design, n=n, auto=auto, makers=makers, heads=heads, salaries=salaries, benefits=benefits, seats=seats,
                flow=flow, drives=drives, team=team, shoots=shoots, monthly=monthly, partner=partner, in_total=team + shoots, bl_total=partner + shoots,
                ramp_in=ramp_in, ramp_bl=ramp_bl)

def plural(n, one, many=None):
    return '%d %s' % (n, one if n == 1 else (many or one + 's'))

def view(s):
    """every figure and line the calculator shows, by the name of the element that shows it (data-tc), plus the bar widths (w-*),
    the rows that are empty (off) and the head count for the dots"""
    m = model(s)
    n = m['n']
    v = {}
    v['ads-out'] = str(s['ads'])
    v['shoots-out'] = str(s['shoots'])
    v['mix-out'] = ('%d video' % s['ads']) if s['design'] == 0 else ('%d design' % s['ads']) if s['design'] == 100 else '%d video, %d design' % (m['video'], m['design'])
    diff = m['in_total'] - m['bl_total']
    if diff > 0:
        pct = rnd(diff / m['in_total'] * 100)
        v['lead'], v['hero'] = 'Birdline saves you', money(diff)
        team = 'one hire' if m['heads'] == 1 else 'a team of %d' % m['heads']
        v['tail'] = ('a year, %d%% less than %s on payroll.' % (pct, team)) if pct >= 3 else 'a year. Close to even.'
    elif diff < 0:
        pct = rnd(-diff / m['bl_total'] * 100)
        v['lead'], v['hero'] = ('One hire on payroll saves you' if m['heads'] == 1 else 'A team on payroll saves you'), money(-diff)
        v['tail'] = ('a year, %d%% less than Birdline.' % pct) if pct >= 3 else 'a year. Close to even.'
    else:
        v['lead'], v['hero'], v['tail'] = 'Both come to', money(m['in_total']), 'a year. Even on cost.'
    v['in-total-bar'], v['bl-total-bar'] = money(m['in_total']), money(m['bl_total'])
    v['heads'] = str(m['heads'])
    v['heads-l'] = plural(m['heads'], 'person', 'people')
    for k in ROLE_KEYS:
        v['n-' + k] = str(n[k])
    months = s['ads'] * 12
    v['perad-in'], v['perad-bl'] = money(rnd(m['team'] / months)), money(rnd(m['partner'] / months))
    v['start-in'] = str(s['fill'])
    v['ramp-in'], v['ramp-bl'] = str(m['ramp_in']), str(m['ramp_bl'])
    off = []
    for k in ROLE_KEYS:
        if n[k]:
            v['in-' + k], v['in-%s-n' % k] = money(n[k] * s['salary'][k]), '%d × %s' % (n[k], money(s['salary'][k]))
        else:
            off.append(k)
            v['in-' + k] = '—'
            v['in-%s-n' % k] = ('No video in the mix' if k == 'editor' else 'No design in the mix' if k == 'designer'
                                else 'Not at this size' if s['over'][k] is None else 'Left out')
    for k, pack, who, whos in (('editor', 'Video Editing', 'dedicated senior editor', 'dedicated senior editors'),
                               ('designer', 'Design & Animation', 'dedicated senior designer/animator', 'dedicated senior designers/animators')):
        if n[k]:
            v['bl-' + k] = money(n[k] * CONFIG['price'][k] * 12)
            v['bl-%s-x' % k] = '%s, %s, ' % (pack, plural(n[k], who, whos))
            v['bl-%s-n' % k] = '%s/mo' % money(n[k] * CONFIG['price'][k])
        else:
            v['bl-' + k], v['bl-%s-x' % k], v['bl-%s-n' % k] = '—', '', ''
    v['in-benefits'], v['in-benefits-n'] = money(m['benefits']), '%s%% of salaries' % s['load']
    v['in-seats'], v['in-seats-n'] = money(m['seats']), '%d × %s' % (m['heads'], money(s['seat']))
    v['in-flow'], v['in-flow-n'] = money(m['flow']), '%d × %s' % (m['heads'], money(s['tools']))
    # each term holds together and the line breaks before the plus (no-break spaces), so a narrow column reads "1 × $1,900 / + 4 × $280"
    terms = (['%d\u00a0×\u00a0%s' % (n['editor'], money(s['ssd']))] if n['editor'] else []) + (['%d\u00a0×\u00a0%s' % (s['shoots'], money(s['backup']))] if s['shoots'] else [])
    if terms:
        v['in-drives'], v['in-drives-n'] = money(m['drives']), ' +\u00a0'.join(terms)
    else:     # nothing to cut and nothing shot: no drives to buy
        off.append('drives')
        v['in-drives'], v['in-drives-n'] = '—', 'No video or productions'
    v['in-team'], v['bl-team'], v['bl-team-n'] = money(m['team']), money(m['partner']), '%s/mo' % money(m['monthly'])
    v['in-shoots'] = v['bl-shoots'] = money(m['shoots'])
    v['in-shoots-n'] = v['bl-shoots-n'] = '%d × %s' % (s['shoots'], money(s['shoot']))
    v['in-total'], v['bl-total'] = money(m['in_total']), money(m['bl_total'])
    birds = [plural(n['editor'], 'dedicated senior editor')] if n['editor'] else []
    if n['designer']:
        birds.append(plural(n['designer'], 'dedicated senior designer/animator', 'dedicated senior designers/animators'))
    v['birds'] = ('With Birdline that is %s and %s. We hire and manage them. You send the briefs.'
                  % (', '.join(birds), 'a project manager who is also your creative strategist' if m['makers'] <= 3
                     else 'the project management and creative strategy to run them'))
    v['sr'] = 'On payroll: %s, %s a year. With Birdline: %s a year.' % (plural(m['heads'], 'person', 'people'), money(m['in_total']), money(m['bl_total']))
    top = max(m['in_total'], m['bl_total'], 1)
    w = {'in-team': m['team'] / top * 100, 'in-shoot': m['shoots'] / top * 100, 'bl-team': m['partner'] / top * 100, 'bl-shoot': m['shoots'] / top * 100}
    return v, w, off, m

def pct(x):
    return ('%.2f' % x).rstrip('0').rstrip('.')

def figures():
    """the opening figures as the post's prose needs them"""
    s = start_state()
    v, _w, _off, m = view(s)
    return dict(v=v, m=m, s=s)

# ---- the markup: every figure in it is the opening state's; site.js rewrites the elements marked data-tc
INCLUDED = dict(producer='A dedicated project manager who is also your creative strategist for creative marketing')
ALSO = dict(producer='Also the creative strategist')     # a second line under the role's name
# the Birdline App, which every partnership runs through: the three ways it saves time and money, in the app page's own terms
# (Smart Brief, shot list, deliverables, Insights and the Generate New Brief button)
APP = [('Less friction', 'Every brief, deliverable and final file lives in one place, tied to its campaign. Nobody digs through an inbox for the latest version.'),
       ('Faster to execution', 'A Smart Brief becomes a shot list and assigned deliverables, so edits and productions start sooner.'),
       ('More, newer content', 'Ad results sit beside the creative that earned them, and the next brief starts from what worked. New ads launch faster.')]

def render(esc):
    c = CONFIG
    s = start_state()
    v, w, off, m = view(s)
    names = {k: nm for k, nm, _s in c['roles']}
    def t(key):   # a figure, in the element site.js rewrites
        return '<span data-tc="%s">%s</span>' % (key, esc(v[key]))
    def fill(val, lo, hi):   # how far along its track a slider sits, 0 to 1
        return pct((val - lo) / (hi - lo))
    # every control is named with the model's version, so a browser that restores typed figures after a reload restores them to the
    # same fields of the same version and to nothing else
    nm = 'tc%d-' % c['v']
    pills = ''.join('<label><input type="radio" name="%ssize" value="%d" data-tc-in="size"%s><span>%s</span></label>'
                    % (nm, i, ' checked' if i == s['size'] else '', esc(x)) for i, x in enumerate(c['sizes']))
    def slider(key, label, hint, val, rng, out, mix=False):
        lo, hi, step = rng
        return ('<div class="tc-f"><div class="tc-fl"><label for="tc-%s">%s</label><output for="tc-%s" data-tc="%s"%s>%s</output></div>'
                '<input class="tc-range%s" id="tc-%s" name="%s%s" type="range" min="%d" max="%d" step="%d" value="%d" data-tc-in="%s" style="--f:%s">%s</div>'
                % (key, esc(label), key, out, ' class="tc-o-mix"' if mix else '', esc(v[out]), ' tc-range--mix' if mix else '', key, nm, key, lo, hi, step, val, key, fill(val, lo, hi), hint))
    head = ('<div class="tc-head"><h3 class="tc-h">Build your content team</h3>'
            '<p class="tc-sub">Set your size and your volume. The team, what it costs and the Birdline equivalent follow.</p></div>')
    inputs = ('<div class="tc-in" role="group" aria-label="Your inputs">'
              '<div class="tc-f tc-size" role="radiogroup" aria-labelledby="tc-size-l"><div class="tc-fl"><span id="tc-size-l">Company size</span><small>Employees</small></div><div class="tc-pills">%s</div></div>%s%s%s'
              '<p class="tc-nojs">Turn on JavaScript to change the inputs. The figures shown are for the settings above.</p></div>'
              % (pills,
                 slider('ads', 'Ads a month', '<small>Finished ads, variations included</small>', s['ads'], c['ads'], 'ads-out'),
                 slider('shoots', 'Productions a year', '<small>Shoots with a crew</small>', s['shoots'], c['shoots'], 'shoots-out'),
                 slider('design', 'Video or design', '<small class="tc-ends"><span>All video</span><span>All design</span></small>', s['design'], c['design'], 'mix-out', mix=True)))
    summary = ('<div class="tc-sum"><span class="tc-lead" data-tc="lead">%s</span> <b class="tc-hero" data-tc="hero">%s</b> <span class="tc-tail" data-tc="tail">%s</span></div>'
               % (esc(v['lead']), esc(v['hero']), esc(v['tail'])))
    def bar(cls, label, a, b, total):
        return ('<div class="tc-bar%s"><span class="tc-bk">%s</span><span class="tc-track"><i class="tc-seg" data-tc-w="%s" style="flex-basis:%s%%"></i>'
                '<i class="tc-seg tc-seg--2" data-tc-w="%s" style="flex-basis:%s%%"></i></span><b data-tc="%s">%s</b></div>'
                % (cls, label, a, pct(w[a]), b, pct(w[b]), total, esc(v[total])))
    chips = ''.join('<span class="tc-chip" data-tc-chip="%s"%s>%s <b data-tc="n-%s">%s</b></span>' % (k, ' hidden' if k in off else '', esc(names[k]), k, esc(v['n-' + k])) for k in ROLE_KEYS)
    out = ('<div class="tc-out"><div class="tc-bars%s" role="img" data-tc-bars aria-label="%s">%s%s'
           '<p class="tc-key"><i aria-hidden="true"></i>The lighter end of each bar is productions, the same either way.</p></div>'
           '<div class="tc-team"><div class="tc-team-h"><span>The team this takes</span><b data-tc="heads-l">%s</b></div><div class="tc-chips">%s</div></div>'
           '<table class="tc-kpis"><thead><tr><td></td><th scope="col">On payroll</th><th scope="col">Birdline</th></tr></thead><tbody>'
           '<tr><th scope="row">People to hire and manage</th><td>%s</td><td>0</td></tr>'
           '<tr><th scope="row">Cost per finished ad</th><td>%s</td><td>%s</td></tr>'
           '<tr><th scope="row">Days until the work starts</th><td>%s</td><td>%d</td></tr>'
           '<tr><th scope="row">Ads shipped in the first %d days</th><td>%s</td><td>%s</td></tr></tbody></table></div>'
           % ('' if m['shoots'] else ' is-flat', esc(v['sr']), bar('', 'On payroll', 'in-team', 'in-shoot', 'in-total-bar'), bar(' tc-bar--bl', 'Birdline', 'bl-team', 'bl-shoot', 'bl-total-bar'),
              esc(v['heads-l']), chips, t('heads'), t('perad-in'), t('perad-bl'), t('start-in'), c['onboard'], c['window'], t('ramp-in'), t('ramp-bl')))
    def cell(amount, note, extra=None, cls=''):
        x = ('<span class="tc-x" data-tc="%s">%s</span>' % (extra, esc(v[extra]))) if extra else ''
        return '<td%s><b data-tc="%s">%s</b><small>%s<span data-tc="%s">%s</span></small></td>' % (cls, amount, esc(v[amount]), x, note, esc(v[note]))
    def fixed(amount, note):   # a Birdline cell that never changes: included, or nothing to pay
        return '<td class="tc-bl"><b>%s</b><small class="tc-x">%s</small></td>' % (esc(amount), esc(note))
    rows = []
    for k in ROLE_KEYS:
        bl = cell('bl-' + k, 'bl-%s-n' % k, 'bl-%s-x' % k, ' class="tc-bl"') if k in c['price'] else fixed('Included', INCLUDED[k])
        # a role Birdline always includes keeps its row on a phone when the payroll side has no such hire (tc-keep)
        cls = ' '.join(x for x in ('tc-keep' if k in INCLUDED else '', 'is-off' if k in off else '') if x)
        rows.append('<tr data-tc-row="%s"%s><th scope="row">%s%s</th>%s%s</tr>'
                    % (k, (' class="%s"' % cls) if cls else '', esc(names[k]), ('<small>%s</small>' % esc(ALSO[k])) if k in ALSO else '', cell('in-' + k, 'in-%s-n' % k), bl))
    rows.append('<tr><th scope="row">Benefits and payroll taxes</th>%s%s</tr>' % (cell('in-benefits', 'in-benefits-n'), fixed('$0', 'No payroll to run')))
    rows.append('<tr><th scope="row">Software and equipment</th>%s%s</tr>' % (cell('in-seats', 'in-seats-n'), fixed('Included', 'Licenses and workstations')))
    rows.append('<tr><th scope="row">Workflow tools</th>%s%s</tr>' % (cell('in-flow', 'in-flow-n'), fixed('Included', 'The Birdline App and Frame.io review')))
    rows.append('<tr data-tc-row="drives"%s><th scope="row">Editing SSDs and backup drives</th>%s%s</tr>'
                % (' class="is-off"' if 'drives' in off else '', cell('in-drives', 'in-drives-n'), fixed('Included', 'We edit from our own SSDs')))
    rows.append('<tr class="tc-r tc-r--sub"><th scope="row">Team, a year</th><td><b data-tc="in-team">%s</b></td><td class="tc-bl"><b data-tc="bl-team">%s</b><small data-tc="bl-team-n">%s</small></td></tr>'
                % (esc(v['in-team']), esc(v['bl-team']), esc(v['bl-team-n'])))
    rows.append('<tr><th scope="row">Productions</th>%s<td class="tc-bl"><b data-tc="bl-shoots">%s</b><small><span data-tc="bl-shoots-n">%s</span><span class="tc-x">, scoped per project</span></small></td></tr>'
                % (cell('in-shoots', 'in-shoots-n'), esc(v['bl-shoots']), esc(v['bl-shoots-n'])))
    rows.append('<tr class="tc-r tc-r--total"><th scope="row">Total, a year</th><td><b data-tc="in-total">%s</b></td><td class="tc-bl"><b data-tc="bl-total">%s</b></td></tr>'
                % (esc(v['in-total']), esc(v['bl-total'])))
    ledger = ('<div class="tc-ledger"><table><caption class="sr">The team on payroll and the same output with Birdline, line by line</caption>'
              '<thead><tr><td></td><th scope="col">On payroll</th><th scope="col" class="tc-bl"><span class="tc-x">With </span>Birdline</th></tr></thead><tbody>%s</tbody></table>'
              '<p class="tc-birds" data-tc="birds">%s</p>'
              '<div class="tc-app"><div class="tc-app-h"><h4>The Birdline App comes with it</h4>'
              '<p>One production workspace for your team and our Birds, where the brief, the shot list, every deliverable and its ad results stay connected. It saves time and money three ways.</p>'
              '<a href="{{ROOT}}workspace.html">Explore the Birdline App</a></div>'
              '<ul class="tc-app-l">%s</ul></div></div>'
              % (''.join(rows), esc(v['birds']), ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in APP)))
    def field(key, label, val, unit='$', after=''):
        return ('<label class="tc-field"><span>%s</span><span class="tc-inp">%s<input type="text" name="%s%s" inputmode="numeric" autocomplete="off" value="%s" data-tc-set="%s" aria-label="%s">%s</span></label>'
                % (esc(label), ('<i aria-hidden="true">%s</i>' % unit) if unit else '', nm, key, format(val, ','), key, esc(label), ('<i aria-hidden="true">%s</i>' % after) if after else ''))
    checks = ''.join('<label class="tc-check"><input type="checkbox" name="%srole-%s" data-tc-role="%s"%s><span>%s</span></label>' % (nm, k, k, '' if k in off else ' checked', esc(names[k])) for k in SUPPORT)
    adv = ('<details class="tc-adv"><summary><span>Adjust the assumptions</span> <small>Salaries, roles, output per person, costs, hiring time</small></summary><div class="tc-adv-in">'
           '<div class="tc-g"><b>Salaries, a year</b><div class="tc-fields">%s</div></div>'
           '<div class="tc-g tc-g--tall"><b>Roles on the team</b><div class="tc-checks">%s</div><p>Editors and designers follow your volume. The producer, who also carries creative strategy, follows team size, company size and productions until you set it.</p></div>'
           '<div class="tc-g tc-g--tall"><b>Output and costs</b><div class="tc-fields">%s%s%s%s%s%s%s%s</div>'
           '<p>Output is an average. With unlimited deliverables, it moves with your edit requests.</p></div>'
           '<div class="tc-g"><b>Hiring time</b><div class="tc-fields">%s</div><p>The median for a nonexecutive role. Birdline starts within a week.</p></div>'
           '<button class="tc-reset" type="button" data-tc-reset>Reset everything</button></div></details>'
           % (''.join(field('salary.' + k, names[k], s['salary'][k]) for k in ROLE_KEYS), checks,
              field('cap.editor', 'Average ads an editor ships a month', s['cap']['editor'], unit=''),
              field('cap.designer', 'Average ads a designer ships a month', s['cap']['designer'], unit=''),
              field('load', 'Benefits and payroll taxes', s['load'], unit='', after='%'),
              field('seat', 'Software and equipment, per person', s['seat']),
              field('tools', 'Workflow tools, per person', s['tools']),
              field('ssd', 'Editing SSDs, per editor a year', s['ssd']),
              field('backup', 'Backup drive, per production', s['backup']),
              field('shoot', 'Budget per production', s['shoot']),
              field('fill', 'Days to fill a seat', s['fill'], unit='', after='days')))
    foot = ('<div class="tc-foot"><p class="tc-note">An estimate, not a quote. Salaries are U.S. figures from the Bureau of Labor Statistics: senior pay, the 75th percentile, for the editor and the designer, and the median for the producer. Birdline figures use our starting prices, '
            'one package per dedicated creative. Productions use the same budget on both sides. The first 90 days assume every seat is filled at once and both sides ship at full rate from their first day.</p>'
            '<div class="tc-cta"><a class="btn" href="{{CALENDLY}}">Book a call</a><a class="btn btn--outline" href="{{ROOT}}packages.html">See the packages</a></div></div>')
    cfg = dict(v=c['v'], roles=[[k, sal] for k, _n, sal in c['roles']], cap=c['cap'], load=c['load'], seat=c['seat'], tools=c['tools'], ssd=c['ssd'], backup=c['backup'], shoot=c['shoot'],
               fill=c['fill'], onboard=c['onboard'], window=c['window'], price=c['price'], start=c['start'])
    return ('<figure class="tc" id="calculator" data-teamcalc="%s" aria-label="Team calculator">\n<div class="tc-top on-dark">%s<div class="tc-body">%s%s%s</div></div>\n%s\n%s\n%s\n'
            '<p class="sr" aria-live="polite" data-tc-live></p>\n</figure>'
            % (esc(json.dumps(cfg, separators=(',', ':'))), head, inputs, summary, out, ledger, adv, foot))
