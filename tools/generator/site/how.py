"""The How It Works page (November 8, 2026; cut to half its length the same night): Mike's copy, tightened, section by section.
Rendered by how_page() in build_site.py, which also draws the small UI beside the copy: the brand's channel in the hero, and a
chip per step (the kickoff faces, a project thread, brief → draft → final, the strategy-call counts)."""

HERO = dict(
    eyebrow='How it works',
    h1='Your Creative Team, |One Slack Message Away.',
    lede='Birdline works alongside your in-house team to make the content you need week to week. The Birdline App keeps the work connected, from the first brief to the finished creative and how it performs.',
)

# the channel in the hero: a private channel for the brand and Birdline, with a few project threads. The Birdline side is the
# Birds; the brand side is a stand-in. (A screenshot of a real channel set the shape; none of its text is here.)
CHANNEL = 'yourbrand-birdline'
THREADS = [
    # (day label or None, who: a Birds key or ('initials', 'Name'), time, thread title, reply count, repliers: Birds keys)
    ('Monday', ('DW', 'Dana Whitfield'), '9:12 AM', 'New briefs | Spring launch · paid social', 14, ['ryan', 'mike']),
    (None, 'ryan', '11:05 AM', 'Hero spot · 30s cutdowns v2', 9, ['ryan', 'bryan']),
    ('Thursday', 'mike', '4:18 PM', 'Shoot day · call sheet and shot list', 22, ['mike', 'trevor', 'grant']),
]

STEPS = dict(
    eyebrow='How a partnership runs',
    h2='From Kickoff |to Final.',
    steps=[
        # (chip, title, copy)
        ('faces', 'Kickoff', 'We meet your team, learn how you work, and decide what to tackle first. You’ll meet your project manager and the Birds who’ll be making the work. Send over brand guidelines, past campaigns, and footage; we’ll organize what comes in.'),
        ('thread', 'Slack and the Birdline App', 'Both teams in one channel. Each project gets a thread linked to its brief in Birdline, where you talk directly with the people making the work and see where things stand. The app is included in your Monthly Partnership.'),
        ('stages', 'Brief to final', 'Start a brief in the app or drop a request in Slack. Drafts go to Frame.io for timecoded notes, and every deliverable is tracked against its brief. Approved finals land in Birdline, ready to launch and easy to find again.'),
        ('agenda', 'Strategy calls', 'Every other week, or weekly when needed: what shipped, what’s in progress, what’s performing, and what to make next, from the library or a new shoot.'),
    ],
    note_k='Unlimited deliverables',
    note='Send as many requests and revisions as you need within the scope of your Monthly Partnership. We agree on what comes first and work through the queue in priority order. A typical first edit takes about a week.',
)
THREAD = dict(who='ryan', title='Hero spot · 30s cutdowns v2', replies=9, brief='Brief')
STAGES = [('Brief', 'done'), ('Draft', 'done'), ('Final', 'now')]
AGENDA = [(7, 'shipped'), (4, 'in progress'), (5, 'up next')]

BIRDS = dict(
    eyebrow='The Birds',
    h2='Meet |Your Birds.',
    sub='World-class producers, filmmakers, editors, designers, and animators who work as an extension of your in-house team. You get direct access to the people doing the work; Birdline handles vetting, hiring, onboarding, and day-to-day management.',
    tail='It works for the Birds, too: steady work across brands, month after month, gives them the context to make creative that feels like you.',
)

SHOOT = dict(
    eyebrow='Productions and the library',
    h2='Shoot for This Campaign |and the Next One.',
    # (image, label, alt)
    strip=[('2024/05/Gardyn_7_29_2025_Kitchen_77886.jpeg', 'Hero asset', 'A couple cooking together beside a Gardyn tower, from the hero spot.'),
           ('2024/05/Gardyn_7_29_2025_27427.jpeg', 'Alternate hook', 'A girl leans over a plate of pancakes and strawberries at the kitchen table.'),
           ('2024/05/Gardyn_7_29_2025_26229.jpeg', 'Product detail', 'A woman kneels to tend the plants on a Gardyn tower by a sunlit window.'),
           ('2024/05/Gardyn-14May2024-GrantPuckett43284-RetouchV1.jpeg', 'Clean take', 'A Gardyn tower in a sunlit hallway, no one in frame.'),
           ('ai/gardyn-living-room-2.jpg', 'AI, from one photo', 'Three Gardyn towers in a living room, generated from a single campaign photo.')],
    cols=[('On set', 'New productions are scoped and billed separately. We agree on the scope and budget, then handle the shot list, crew, talent, locations, schedule, and call sheets. On set, we capture the hero assets alongside alternate hooks, product details, and clean takes, so there’s a library to pull from for the next paid ad, product launch, or TV spot. For Gardyn, AI and a single photo from an earlier campaign became the first ten seconds of a new ad.'),
          ('In the library', 'Active footage lives on fast SSDs with consistent folder structures and clear file names, so an editor can pull a shot from two years ago and cut it beside something we filmed last month. In the Birdline App, the approved creative stays connected to the campaign and brief it came from.')],
)

RETURNS = dict(
    h2='See What |the Work Returned.',
    sub='When performance data is connected in Birdline, we trace ad results back to the creative, the brief, and the production behind it.',
    metrics=[('ROPS', 'Return on Production Spend', 'How much tracked revenue did the creative generate for each dollar spent making it?'),
             ('ROCS', 'Return on Campaign Spend', 'How did the campaign perform when you account for both production and media spend?')],
    tail='Those results shape the next strategy call: sometimes a new edit from footage you already have, sometimes a reason to bring a proven setup back for another shoot.',
)

CLOSE = dict(heading='What Are You Making Next?', sub='Tell us what’s in your pipeline and where your team could use another set of hands.')
