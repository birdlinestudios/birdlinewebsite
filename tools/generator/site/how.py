"""The How It Works page (reworked November 9, 2026, in the site's own vocabulary: a navy hero over a set photo, centred heads,
pillar cards, the numbered steps grid on navy, case cards, the FAQ and the close). Mike's copy, section by section; rendered by
how_page() in build_site.py.

The page says one thing several ways: Birdline is your creative team on a monthly partnership. You send briefs in Slack or the
Birdline App, the Birds make the work, finals land in your library, and the two of us meet every other week to decide what's next."""

HERO = dict(
    eyebrow='How it works',
    h1='Your Creative Team, |One Slack Message Away.',
    lede='Birdline works alongside your in-house team on a monthly partnership. You send the briefs, our Birds make the work, and the Birdline App keeps every project connected, from the first request to the finished creative and how it performed.',
    photo='new/production-hero.jpg',
)

# the takeaway, first: the partnership in three moves
SHORT = dict(
    eyebrow='In short',
    h2='Three Moves, |Every Week.',
    sub='Everything on this page comes down to this.',
    steps=[
        ('slack', 'Send a brief', 'Drop a request in Slack or the Birdline App. We align on the goal, the deliverables, references and the timeline.'),
        ('talent', 'We make it', 'Your Birds produce the work. Drafts land in Frame.io for timecoded notes, and a first edit takes about a week.'),
        ('workspace', 'It lands in your library', 'Approved files go into the Birdline App, tied to their brief and campaign, ready to launch and easy to find again.'),
    ],
    # the numbers under the three moves
    stats=[('Unlimited', 'deliverables and revisions within your plan'), ('~1 week', 'for a typical first edit'), ('Every 2 weeks', 'a strategy call, weekly when needed'), ('1 team', 'a project manager and the Birds who make your work')],
)

# how a partnership runs, step by step (the numbered grid on navy)
RUN = dict(
    eyebrow='How a partnership runs',
    h2='From Kickoff |to Finals.',
    sub='Six steps, the same for every brand we work with.',
    steps=[
        ('Kickoff', 'We meet your team, learn how you work and decide what to tackle first. You meet your project manager and the Birds who will make the work, and share brand guidelines, past campaigns, raw footage and working files. We organize what comes in and flag what we can start using right away.'),
        ('Slack and the Birdline App', 'We connect both teams in one Slack channel and set you up in the Birdline App, which is included in your partnership and open to your own projects too. Each project gets a thread linked to its brief, where you talk directly with the people making the work.'),
        ('Brief', 'Start in the app or drop the request in Slack. If you already have a brief in a doc or a deck, send the link. We get aligned on the goal, deliverables, references and timeline before anyone opens a timeline.'),
        ('Drafts and review', 'Drafts go to Frame.io, where you leave comments and timecoded notes. Every deliverable is tracked against its brief in the app, so nothing gets lost between rounds.'),
        ('Finals', 'Once approved, the final files go into the Birdline App and we let you know in Slack. Your team can see what is ready to launch and find it again when the next campaign comes around.'),
        ('Strategy calls', 'Every other week, weekly when needed: what shipped, what is in progress and what is coming up. We look at what is performing and decide what to make next from the library, and what we might need to shoot.'),
    ],
)

# where the work lives: the three tools, as pillars
TOOLS = dict(
    eyebrow='Where the work lives',
    h2='Three Tools, |One Workflow.',
    sub='No new software to learn on your side. Slack for the conversation, Frame.io for review, the Birdline App for everything else.',
    pillars=[
        ('slack', 'Slack', 'One shared channel and a thread per project. You talk directly with the people making the work, share references and see where things stand.'),
        ('reviews', 'Frame.io', 'Every draft lands here. Leave comments and timecoded notes on the frame, and approve when it is right.'),
        ('workspace', 'The Birdline App', 'Briefs, deliverables, the finished library and, when performance data is connected, how each piece of creative performed.'),
    ],
)

# productions: shot for this campaign and the next one
SHOOT = dict(
    eyebrow='Productions',
    h2='Shoot for This Campaign |and the Next One.',
    sub='New productions are scoped and billed separately, and shot so the footage keeps paying off.',
    tiles=[  # (photo, title, copy, link text, link)
        ('2024/05/Gardyn_7_29_2025_Kitchen_77909.jpeg', 'Scoped for the campaign',
         'We start with what the campaign needs, agree on the scope and budget, and handle the shot list, crew, talent, locations, schedule and call sheets.',
         'Our production process', '{{ROOT}}services/production-process.html'),
        ('2024/05/Gardyn_7_29_2025_27427.jpeg', 'Shot for the library',
         'On set we capture the hero assets alongside alternate hooks, product details, clean takes and framing we can use in future edits. Over time that gives you a library to pull from for a new paid ad, a product launch or a TV spot.',
         'The Gardyn case study', '{{ROOT}}case-studies/gardyn.html'),
        ('ai/gardyn-living-room-2.jpg', 'Easy to find again',
         'Active footage lives on organized drives, and in the Birdline App the approved creative stays connected to its campaign and brief. For Gardyn, one photo from an earlier campaign became the first ten seconds of a new ad.',
         'Explore the app', '{{ROOT}}workspace.html'),
    ],
    alts=['A couple cooking together at a kitchen island beside a Gardyn tower, from the hero spot.',
          'A girl leans over a plate of pancakes and strawberries at the kitchen table.',
          'Three Gardyn towers in a living room, generated from a single campaign photo.'],
)

BIRDS = dict(
    eyebrow='Your Birds',
    h2='The People |Making Your Work.',
    para='Our Birds are world-class producers, filmmakers, editors, designers and animators who work as an extension of your in-house team.',
    bullets=[('Direct access', 'You talk to the people doing the work, in your Slack channel, not through an account manager.'),
             ('We handle the team', 'Vetting, hiring, onboarding and day-to-day management are on us.'),
             ('Context that compounds', 'Steady work across brands, month after month, gives them the context to make creative that feels like you.')],
    faces=['ryan', 'megan', 'james', 'grant', 'trevor', 'bryan'],
    link='Meet the Birds', href='{{ROOT}}about.html#team',
)

RETURNS = dict(
    eyebrow='Results',
    h2='See What |the Work Returned.',
    sub='When performance data is connected in the Birdline App, we trace ad results back to the creative, the brief and the production behind it.',
    cards=[('ROPS', 'Return on Production Spend', 'How much tracked revenue did the creative generate for each dollar spent making it?'),
           ('ROCS', 'Return on Campaign Spend', 'How did the campaign perform once you account for both production and media spend?')],
    tail='Those numbers come into the next strategy call. Sometimes the best next move is a new edit from footage you already have; sometimes they give us a reason to bring a proven setup back for another shoot.',
    link='How we measure it', href='{{ROOT}}rops.html',
)

CASES = dict(eyebrow='Who works this way', h2='Brands That Run |on Birdline.', slugs=['whoop', 'gardyn', 'public-rec', 'ufl'])

FAQ = dict(eyebrow='FAQ', h2='Questions About |How It Works.',
           items=['What counts as a deliverable?', 'How fast do deliverables come back?', 'Do I own the media and the project files?', 'What do we cover on recurring strategy calls?', 'Can I cancel?', 'How do we start?'])

CLOSE = dict(heading='What Are You Making Next?', sub='Tell us what is in your pipeline and where your team could use another set of hands.', photo='2025/09/PublicRec-DTLA-DD-33.jpeg')
