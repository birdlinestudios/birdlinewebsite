"""The How It Works page (November 8, 2026): Mike's copy, section by section. The page is rendered by how_page() in build_site.py;
the visuals beside the copy (the Slack channel, a project thread, the strategy-call agenda, the brief / review / finals cards, the
shoot-day strip and the footage folders) are drawn there."""

HERO = dict(
    eyebrow='How it works',
    h1='Your Creative Team, |One Slack Message Away.',
    lede='Birdline Studios works alongside your in-house team to make the content you need week to week. The Birdline App keeps the work connected, from the first brief to the finished creative and how it performs.',
)

# the Slack channel in the hero: a private channel for the brand and Birdline, with a week of project threads. The names on the
# Birdline side are the Birds; the brand side is a stand-in. (A reference screenshot from a real channel set the shape; none of
# its text is here.)
CHANNEL = 'yourbrand-birdline'
THREADS = [
    # (day label or None, who: a Birds key or ('initials', 'Name', 'role'), time, thread title, reply count, repliers: Birds keys)
    ('Monday', ('DW', 'Dana Whitfield', 'Brand team'), '9:12 AM', 'New briefs | Spring launch · paid social', 14, ['ryan', 'mike']),
    (None, 'ryan', '11:05 AM', 'Hero spot · 30s cutdowns v2', 9, ['ryan', 'bryan']),
    ('Wednesday', 'james', '2:40 PM', 'Product renders · colorway grid', 11, ['james', 'megan']),
    (None, 'mike', '4:18 PM', 'Shoot day · call sheet and shot list', 22, ['mike', 'trevor', 'grant']),
    ('Friday', 'megan', '10:31 AM', 'Email headers · spring drop', 6, ['megan', 'ryan']),
]

SETUP = dict(
    eyebrow='Getting started',
    h2='Get Set Up |with Birdline.',
    sub='We start with a kickoff to meet your team, learn how you work, and decide what to tackle first.',
    steps=[
        ('pm', 'Meet your team', 'You’ll meet your dedicated project manager and the Birds who’ll be making the work.'),
        ('share', 'Share what you have', 'Brand guidelines, past campaigns, raw footage, and working files. We’ll organize what comes in and flag what we can start using right away.'),
        ('workspace', 'Get connected', 'We connect both teams in Slack and set you up in the Birdline App. The app is included in your Monthly Partnership, and your team can use it for its own projects, too.'),
    ],
)

TOUCH = dict(
    eyebrow='Working together',
    h2='Stay Close |to the Work.',
    cards=[
        ('slack', 'Day to day in Slack', 'Each project gets a Slack thread linked to its brief in Birdline. That’s where you can talk directly with the people making the work, share references, and see where things stand.'),
        ('calls', 'Strategy calls every other week, or weekly when needed', 'We review what shipped, what’s in progress, and what’s coming up. We look at which creative is performing and which could use another pass, then decide what to make from the library and what we might need to shoot next.'),
    ],
)
# the project thread in the first card
THREAD = dict(title='Hero spot · 30s cutdowns v2', brief='Open the brief in Birdline', status='In review',
              replies=[(('DW', 'Dana Whitfield'), 'Love the opening. Can we hold the product shot a beat longer?'),
                       ('ryan', 'On it. v3 by tomorrow morning, Frame.io link here when it’s up.')])
# the agenda in the second card
AGENDA = dict(when='Every other week · 30 min', rows=[('Shipped', 'this sprint', 7), ('In progress', 'with the Birds', 4), ('Up next', 'in the queue', 5)],
              perf=[('Hero spot · 30s', 82), ('UGC · round 2', 64), ('Statics · spring', 41)], next='Next: two new cuts from the library, one shoot to scope')

BIRDS = dict(
    eyebrow='The Birds',
    h2='Meet |Your Birds.',
    sub='Our Birds are world-class producers, filmmakers, editors, designers, and animators who work as an extension of your in-house team. You get direct access to the people doing the work while Birdline handles vetting, hiring, onboarding, and day-to-day management.',
    tail='It works for the Birds, too. They get steady work across a variety of brands and can spend more of their time on their craft. Working with your team month after month gives them the context to make creative that feels like you.',
)

FLOW = dict(
    eyebrow='Brief to final',
    h2='Go From Brief |to Final.',
    steps=[
        ('Send us the brief', 'Start in the Birdline App or drop the request in Slack. If you already have a brief in a doc or deck, send us the link. We’ll get aligned on the goal, deliverables, references, and timeline.'),
        ('Review the work', 'Every deliverable is tracked against its brief in the app. We share updates and review links in Slack and upload drafts to Frame.io, where you can leave comments and timecoded notes on video.'),
        ('Find your finals', 'Once approved, the final files go into Birdline and we let you know in Slack. Your team can see what’s ready to launch and find it again when the next campaign comes around.'),
    ],
    q='How do unlimited deliverables work?',
    a='Send as many requests and revisions as you need within the scope of your Monthly Partnership. We agree on what comes first and work through the queue in priority order. A typical first edit takes about a week, depending on complexity and what’s already in the queue.',
)
# the three cards' visuals
BRIEF = dict(title='Spring launch · 15s cutdowns', rows=[('Goal', 'Drive trial sign-ups'), ('Deliverables', '6 × 9:16, 2 × 16:9'), ('Due', 'Mar 14')])
REVIEW = dict(file='SpringLaunch_15s_v2.mp4', at='00:12', note='Hold the product shot a beat longer.', who=('DW', 'Dana Whitfield'))
FINALS = ['SpringLaunch_15s_9x16_FINAL.mp4', 'SpringLaunch_15s_16x9_FINAL.mp4', 'SpringLaunch_Statics_FINAL.zip']

SHOOT = dict(
    eyebrow='Productions',
    h2='Shoot for This Campaign |and the Next One.',
    paras=['New productions are scoped and billed separately. We start with what the campaign needs, agree on the scope and budget, and handle the shot list, crew, talent, locations, schedule, and call sheets as needed.',
           'On set, we capture the hero assets alongside alternate hooks, product details, clean takes, and framing we can use in future edits. Over time, that gives you a library you can pull from for a new paid ad, a product launch, or a TV spot. For Gardyn, we used AI and a single photo from an earlier campaign to create the first ten seconds of a new ad.'],
    photo='new/production-hero.jpg',
    photo_alt='A Birdline crew on set in a kitchen, the camera on a tripod beside a table of produce.',
    strip_k='One shoot day, cut for years',
    # (image, label, alt)
    strip=[('2024/05/Gardyn_7_29_2025_Kitchen_77886.jpeg', 'Hero asset', 'A couple cooking together beside a Gardyn tower, from the hero spot.'),
           ('2024/05/Gardyn_7_29_2025_27427.jpeg', 'Alternate hook', 'A girl leans over a plate of pancakes and strawberries at the kitchen table.'),
           ('2024/05/Gardyn_7_29_2025_26229.jpeg', 'Product detail', 'A woman kneels to tend the plants on a Gardyn tower by a sunlit window.'),
           ('2024/05/Gardyn-14May2024-GrantPuckett43284-RetouchV1.jpeg', 'Clean take', 'A Gardyn tower in a sunlit hallway, no one in frame.'),
           ('ai/gardyn-living-room-2.jpg', 'AI, from one photo', 'Three Gardyn towers in a living room, generated from a single campaign photo.')],
)

FILES = dict(
    eyebrow='The library',
    h2='How We Keep Footage |Easy to Find.',
    paras=['We store active footage on high-capacity SSDs for fast access. Consistent folder structures and clear file names make it easy for an editor to pull a shot from two years ago and cut it alongside something we filmed last month.',
           'In the Birdline App, the approved creative stays connected to the campaign and brief it came from.'],
    drive='Active footage · SSD',
    path=['Gardyn', '2025', '07-29 Kitchen shoot'],
    folders=[('01_Hero_A-cam', '24 clips'), ('02_Alt-hooks', '31 clips'), ('03_Product-details', '18 clips'), ('04_Clean-takes', '12 clips')],
    file=('GDN_250729_Hero_A01_C004.mov', '4K · 23.976 · 2.4 GB'),
    chain=['Campaign', 'Brief', 'Approved creative'],
)

RETURNS = dict(
    eyebrow='ROPS™ & ROCS™',
    h2='See What |the Work Returned.',
    sub='When performance data is connected in Birdline, we can trace ad results back to the creative, the brief, and the production behind it.',
    metrics=[('ROPS', 'Return on Production Spend', 'How much tracked revenue did the creative generate for each dollar spent making it?'),
             ('ROCS', 'Return on Campaign Spend', 'How did the campaign perform when you account for both production and media spend?')],
    tail='We bring those results into the next strategy call. Sometimes the best next move is a new edit from footage you already have. Sometimes the numbers give us a reason to bring a proven setup back for another shoot.',
)

CLOSE = dict(heading='What Are You Making Next?', sub='Tell us what’s in your pipeline and where your team could use another set of hands.')
