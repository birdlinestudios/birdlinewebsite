"""The How It Works page (November 8, 2026; laid out after Klarna's "What is Klarna?" page the same night): Mike's copy, section by
section. Rendered by how_page() in build_site.py, which draws the UI beside it: a rounded hero card with the set photo, a pinned
panel whose visual follows the five parts of a partnership as the reader scrolls, three photo tiles for productions, the Birds
beside their copy, ROPS and ROCS as two big cards, the client tiles, and the FAQ."""

HERO = dict(
    eyebrow='How it works',
    h1='Your Creative Team, One Slack Message Away.',
    paras=['Birdline works alongside your in-house team to make the content you need week to week.',
           'The Birdline App keeps the work connected, from the first brief to the finished creative and how it performs.'],
    photo='new/production-hero.jpg',
    photo_alt='A Birdline crew on set in a kitchen: the camera on a tripod beside a table of produce, the director watching the monitor.',
)

# the five parts of a partnership: the pinned panel shows one visual per part as the list scrolls (title, copy, link text, link)
FEAT_H2 = 'How a Partnership Runs.'
FEATURES = [
    ('kickoff', 'Kickoff',
     'We meet your team, learn how you work, and decide what to tackle first. You’ll meet your dedicated project manager and the Birds who’ll be making the work. Share your brand guidelines, past campaigns, raw footage, and working files; we’ll organize what comes in and flag what we can start using right away.',
     'See the packages', '{{ROOT}}packages.html'),
    ('slack', 'Slack and the Birdline App',
     'We connect both teams in Slack and set you up in the Birdline App, which is included in your Monthly Partnership and open to your own projects, too. Each project gets a Slack thread linked to its brief in Birdline. That’s where you talk directly with the people making the work, share references, and see where things stand.',
     'Explore the app', '{{ROOT}}workspace.html'),
    ('flow', 'Brief to final',
     'Start in the Birdline App or drop the request in Slack; if you already have a brief in a doc or deck, send us the link, and we’ll get aligned on the goal, deliverables, references, and timeline. Drafts go to Frame.io, where you leave comments and timecoded notes, and every deliverable is tracked against its brief in the app. Once approved, the final files go into Birdline and we let you know in Slack, so your team can see what’s ready to launch and find it again when the next campaign comes around.',
     'See the work', '{{ROOT}}work.html'),
    ('calls', 'Strategy calls',
     'We meet every other week, with weekly calls as needed. We review what shipped, what’s in progress, and what’s coming up, look at which creative is performing and which could use another pass, then decide what to make from the library and what we might need to shoot next.',
     'How we measure results', '{{ROOT}}rops.html'),
    ('queue', 'Unlimited deliverables',
     'Send as many requests and revisions as you need within the scope of your Monthly Partnership. We agree on what comes first and work through the queue in priority order. A typical first edit takes about a week, depending on complexity and what’s already in the queue.',
     'Compare the packages', '{{ROOT}}packages.html'),
]
# what the panel shows for each part
KICKOFF = dict(title='Kickoff', when='45 min · this week', people=[('DW', 'Dana Whitfield'), 'mike', 'ryan', 'james'],
               agenda=[('How you work', 'Who signs off, where the files live, what’s coming up'), ('What to tackle first', 'The next campaign, and what the library already has'), ('Your files', 'Brand guidelines, past campaigns, raw footage')])
CHANNEL = 'yourbrand-birdline'
THREADS = [  # (day label or None, who: a Birds key or ('initials', 'Name'), time, thread title, reply count, repliers)
    ('Monday', ('DW', 'Dana Whitfield'), '9:12 AM', 'New briefs | Spring launch · paid social', 14, ['ryan', 'mike']),
    (None, 'ryan', '11:05 AM', 'Hero spot · 30s cutdowns v2', 9, ['ryan', 'bryan']),
    ('Thursday', 'mike', '4:18 PM', 'Shoot day · call sheet and shot list', 22, ['mike', 'trevor', 'grant']),
]
BRIEF = dict(title='Spring launch · 15s cutdowns', rows=[('Goal', 'Drive trial sign-ups'), ('Deliverables', '6 × 9:16, 2 × 16:9'), ('Due', 'Mar 14')])
REVIEW = dict(file='SpringLaunch_15s_v2.mp4', at='00:12', note='Hold the product shot a beat longer.', who=('DW', 'Dana Whitfield'))
FINALS = ['SpringLaunch_15s_9x16_FINAL.mp4', 'SpringLaunch_15s_16x9_FINAL.mp4']
AGENDA = dict(when='Every other week · 30 min', rows=[('Shipped', 7), ('In progress', 4), ('Up next', 5)],
              perf=[('Hero spot · 30s', 82), ('UGC · round 2', 64), ('Statics · spring', 41)], next='Next: two new cuts from the library, one shoot to scope')
QUEUE = dict(rows=[('Hero spot · 30s cutdowns v2', 'In progress'), ('Spring statics · round 2', 'Up next'), ('UGC scripts · April', 'Queued'), ('Email headers · spring drop', 'Queued')],
             note='A first edit takes about a week')

SHOOT = dict(
    h2='Shoot for This Campaign and the Next One.',
    sub='New productions are scoped and billed separately, and shot so the footage keeps paying off.',
    tiles=[  # (photo, title, copy, link text, link)
        ('2024/05/Gardyn_7_29_2025_Kitchen_77909.jpeg', 'Scoped for the campaign',
         'We start with what the campaign needs, agree on the scope and budget, and handle the shot list, crew, talent, locations, schedule, and call sheets as needed.',
         'See the work', '{{ROOT}}work.html'),
        ('2024/05/Gardyn_7_29_2025_27427.jpeg', 'Shot for the library',
         'On set, we capture the hero assets alongside alternate hooks, product details, clean takes, and framing we can use in future edits. Over time, that gives you a library to pull from for a new paid ad, a product launch, or a TV spot.',
         'The Gardyn case study', '{{ROOT}}case-studies/gardyn.html'),
        ('ai/gardyn-living-room-2.jpg', 'Easy to find again',
         'Active footage lives on high-capacity SSDs with consistent folder structures and clear file names, so an editor can pull a shot from two years ago and cut it alongside last month’s. In the Birdline App, the approved creative stays connected to its campaign and brief. For Gardyn, AI and a single photo from an earlier campaign became the first ten seconds of a new ad.',
         'Explore the app', '{{ROOT}}workspace.html'),
    ],
    alts=['A couple cooking together at a kitchen island beside a Gardyn tower, from the hero spot.',
          'A girl leans over a plate of pancakes and strawberries at the kitchen table.',
          'Three Gardyn towers in a living room, generated from a single campaign photo.'],
)

BIRDS = dict(
    h2='Meet Your Birds.',
    para='Our Birds are world-class producers, filmmakers, editors, designers, and animators who work as an extension of your in-house team.',
    bullets=['Direct access to the people doing the work', 'Birdline handles vetting, hiring, onboarding, and day-to-day management', 'Steady work across brands, month after month, gives them the context to make creative that feels like you'],
    faces=['ryan', 'megan', 'james', 'grant'],
    link='Meet the Birds', href='{{ROOT}}about.html#team',
)

RETURNS = dict(
    h2='See What the Work Returned.',
    sub='When performance data is connected in Birdline, we trace ad results back to the creative, the brief, and the production behind it.',
    cards=[('ROPS', 'Return on Production Spend', 'How much tracked revenue did the creative generate for each dollar spent making it?'),
           ('ROCS', 'Return on Campaign Spend', 'How did the campaign perform when you account for both production and media spend?')],
    tail='Those results come into the next strategy call. Sometimes the best next move is a new edit from footage you already have; sometimes the numbers give us a reason to bring a proven setup back for another shoot.',
    link='How we measure it', href='{{ROOT}}rops.html',
)

BRANDS_H2 = 'Trusted by Brands You Know.'
BRANDS = ['whoop', 'gardyn', 'public-rec', 'route', 'ufl', 'literati', 'freepower', 'patrol', '686', 'edjy', 'willies-remedy', 'solidroad']

FAQ_H2 = 'Frequently Asked Questions.'
FAQ = ['What counts as a deliverable?', 'How fast do deliverables come back?', 'Do I own the media and the project files?', 'What do we cover on recurring strategy calls?', 'Can I cancel?', 'How do we start?']

CLOSE = dict(heading='What Are You Making Next?', sub='Tell us what’s in your pipeline and where your team could use another set of hands.')
