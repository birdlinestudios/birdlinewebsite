# Hand-set details for the Work and case-study pages. Everything written in words here is drawn from the live case-study pages
# (birdlinestudios.com, October 28, 2026); the headlines and stat captions restate figures from each page's Results copy.

# the nine, in the order of the Case Studies page on birdlinestudios.com
ORDER = ['whoop', 'gardyn', 'literati', 'solidroad', '686', 'route', 'freepower', 'public-rec', 'willies-remedy', 'patrol', 'edjy', 'ufl']

# the card for each study (the homepage's case-study grid uses the same lines): brand, one result, the services, the still (a homepage asset)
CARDS = {
    'public-rec': dict(brand='Public Rec', stat='$53M+ in tracked revenue', tags='Commercial · TV · Paid social', cover='cs-publicrec',
                       alt='A Public Rec mural on a building: a seated man in a white shirt and a couple walking, beside the Public Rec wordmark.'),
    'route': dict(brand='Route', stat='Paid social, on time and on concept', tags='Paid social · Design · Video', cover='cs-route',
                  alt='A woman in an Adirondack chair checks her phone in golden light, from a Route spot.'),
    'gardyn': dict(brand='Gardyn', stat='45M+ organic views', tags='Commercial · Paid social · Photo', cover='cs-gardyn',
                   alt='A Gardyn tower full of greens and herbs in a bright kitchen.'),
    'freepower': dict(brand='FreePower', stat='15M views, 170K clicks', tags='Paid social · UGC · Photo', cover='cs-freepower',
                      alt='Drinks on a bar top with a phone charging on a FreePower surface.'),
    '686': dict(brand='686', stat='Recurring shoots, weekly post-production', tags='Paid social · Social · Animation', cover='cs-686',
                alt='A snowboarder in a black 686 balaclava and goggles.'),
    'patrol': dict(brand='Patrol', stat='12M views in one week', tags='Commercial · UGC · Paid social', cover='cs-patrol',
                   alt='A Patrol vehicle parked on a tree-lined street in front of a mid-century house.'),
    'literati': dict(brand='Literati', stat='An always-on creative pipeline', tags='Paid social · Animation · Design', cover='cs-literati-f27', loop='cs-literati-f27.mp4',
                     alt='Literati’s Adventure Park book fair graphic: an illustrated theme-park map with a dragon-headed train along the bottom.'),
    'solidroad': dict(brand='Solidroad', stat='50+ pieces from one two-day shoot', tags='Social · Paid social · Photo · Animation', cover='cs-solidroad',
                      alt='Two men talking as they walk past a brick office building, from the Solidroad shoot.'),
    'whoop': dict(brand='WHOOP', stat='From a social series to a full partnership', tags='Social · Paid social · Animation · VFX', cover='cs-whoop',
                  alt='A WHOOP band with sleep, recovery and strain readouts.'),
    'willies-remedy': dict(brand='Willie’s Remedy', stat='A three-episode explainer series', tags='YouTube · Animation · Illustration · 3D', cover='cs-willies',
                           alt='A frosted bottle of Willie’s Remedy THC-infused social tonic, lit warm and close.'),
    'edjy': dict(brand='EDJY', stat='From one launch to a full video engine', tags='Paid social · UGC · Photo · Production', cover='cs-edjy-colors',
                 alt='EDJY fingernail cutters in pink, blue, black and silver on cream blocks, from the new colors launch.'),
    'ufl': dict(brand='UFL', stat='A full season of content, at game speed', tags='Broadcast TV · Social · In-stadium · Radio', cover='cs-ufl',
                alt='A Storm player in a black and orange uniform grins and points across the field before a UFL game.'),
}

# the brand's mark (the black logo files from the homepage; shown white on the cover) and its height on the cover and in the quote cards
LOGOS = {
    'public-rec': ('logo2-publicrec', 1560, 210, 34, 17),
    'route': ('logo2-route', 1319, 220, 44, 19),
    'gardyn': ('logo2-gardyn', 884, 220, 50, 23),
    'freepower': ('logo2-freepower', 1630, 220, 38, 17),
    '686': ('logo2-686', 282, 220, 68, 28),
    'patrol': ('logo2-patrol', 939, 220, 52, 22),
    'literati': ('logo2-literati', 540, 145, 54, 24),
    'solidroad': ('logo2-solidroad', 800, 100, 38, 19),
    'whoop': ('logo2-whoop', 1399, 220, 40, 18),
    'willies-remedy': ('logo2-willies-mark', 538, 440, 96, 40),
    'edjy': ('logo2-edjy', 878, 220, 44, 22),
    'ufl': ('logo2-ufl', 358, 220, 72, 30),
}

# the headline on each cover, a line under it, the year the copy names, where the cover photo should sit, and the figures from Results
PAGES = {
    'public-rec': dict(
        headline='Under $1M In. |Over $53M Back.',
        lede='A dedicated content team for Public Rec since 2021: recurring shoots, national TV commercials, and performance-driven edits for Instagram, Facebook, TikTok and YouTube.',
        since='2021', focal='50% 45%',
        stats=[('$53M+', 'in returns across TV and Meta, from under $1M invested'),
               ('4×', 'return on $8M of TV spend, production included'),
               ('51.7×', 'ROAS on one 30-second spot, cut from existing footage'),
               ('7', 'national TV commercials')]),
    'route': dict(
        headline='An Always-On Content Team |for Route.',
        lede='Video, photography and animation for Route’s social channels, website, app and live events, from profile features and how-to tutorials to B2B commercials.',
        since='', focal='55% 55%', stats=[]),
    'gardyn': dict(
        headline='45M+ Organic Views and |a Faster-Growing Brand.',
        lede='A dedicated Bird team producing Gardyn’s video, photography and graphics every month: commercials, UGC-style assets, stills and custom design for social, web and paid.',
        since='2024', focal='50% 50%',
        stats=[('28%', 'year-over-year lift in CTR from paid content'),
               ('50%', 'better watch-through rates'),
               ('45M+', 'organic views from the social assets'),
               ('111%', 'follower growth')]),
    'freepower': dict(
        headline='Launching Wireless Charging |to 23M People.',
        lede='Monthly video, photography and VFX for FreePower’s social, website and paid campaigns: branded commercials, explainers, product demos and custom animation.',
        since='2024', focal='50% 50%',
        stats=[('15M', 'total views over the past 12 months'),
               ('170K', 'link clicks from Birdline’s content'),
               ('23M', 'users reached'),
               ('25K+', 'new followers for FreePower')]),
    '686': dict(
        headline='A Seamless Content Workflow |for 686.',
        lede='Recurring shoots and weekly post-production for 686: paid ads, social content and website videos that show the full product line, the riders and the brand story.',
        since='', focal='50% 35%', stats=[]),
    'patrol': dict(
        headline='12M Views |in One Week.',
        lede='Full-service creative development and production for the Patrol app: narrative brand commercials, authentic UGC storytelling, and short-form assets for Instagram, Meta and X.',
        since='', focal='50% 55%',
        stats=[('12M', 'views for the Private Patrol spot on X, in one week'),
               ('4K', 'reposts'),
               ('8K', 'likes'),
               ('3K', 'saves')]),
    'literati': dict(
        headline='Content That Inspires |a Love of Reading.',
        lede='Literati’s dedicated content production team: video editing, graphic design, campaign content and animation for paid ads, web assets and their B2B model.',
        since='', focal='50% 50%', stats=[]),
    'solidroad': dict(
        headline='50+ Pieces of Content |from One Two-Day Shoot.',
        lede='From a first brand and product video to an embedded content partnership: on-site productions, founder and team storytelling, event coverage, customer interviews and ongoing post.',
        since='', focal='50% 40%',
        stats=[('50+', 'pieces of content from one two-day shoot'),
               ('2', 'days on set, feeding organic, paid, events and ongoing campaigns')]),
    'whoop': dict(
        headline='A Flexible Extension |of WHOOP’s In-House Team.',
        lede='What began as a social series and a handful of paid ads now spans Ferrari content, video podcasts, paid social, design, animation and VFX.',
        since='2026', focal='50% 50%', stats=[]),
    'willies-remedy': dict(
        headline='Making Cannabis Education |Approachable.',
        lede='The Green Guide: a Vox-style YouTube series that explains THC drinks to newcomers, built for Willie’s Remedy in halftone, black-and-white texture and a washed green, with 3D product animation alongside it.',
        since='2026', focal='50% 50%',
        stats=[('3', 'episodes, delivered monthly'), ('2–3 min', 'per Vox-style explainer'), ('1.2×', 'voiceover pace, now the series standard')]),
    'edjy': dict(
        headline='One Product Launch, |a Full Video Engine.',
        lede='How a creative partnership turned one product launch into a full video engine.',
        since='', focal='55% 55%', stats=[]),
    'ufl': dict(
        headline='A Full Season of Content, |Delivered at Game Speed.',
        lede='Birdline became the United Football League’s content partner for a new season: a broadcast TV spot, Media Day, a weekly social slate, stadium screens and game-day radio for all 8 teams.',
        since='', focal='42% 30%',
        stats=[('1', 'month from kickoff to a finished broadcast TV spot with two of the league’s stars'),
               ('10', 'weeks of social content, delivered on schedule'),
               ('8', 'teams supported with custom content'),
               ('22+', 'radio spots produced, including playoff promos'),
               ('4', 'channels: broadcast TV, social, in-stadium and radio'),
               ('Ongoing', 'the UFL came back after the season for Media Day footage for new content')]),
}

# who said it: the headshots the homepage carries (from birdlinestudios.com; a name without one shows its initials)
HEADSHOTS = {
    'Jake Slatnick': ('av-slatnick', 96), 'Zach Goldstein': ('av-goldstein', 98), 'Chelsea Moon': ('av-moon', 98), 'Brent Sandor': ('av-sandor', 98),
    'Howie Zisser': ('av-zisser', 98), 'Megan Gray': ('av-gray', 98), 'FX Rouxel': ('av-rouxel', 192), 'Zack McCabe': ('av-mccabe', 192),
    'Kat Cooper': ('av-cooper', 192), 'Kristen Connors': ('av-connors', 98), 'Nick Sarath': ('av-sarath', 192), 'Shannon Douglas': ('av-douglas', 192),
    'Adam Walker': ('av-walker', 192), 'John Bradford': ('av-bradford', 192),
}

# the thirteen formats on the Work page, as listed on birdlinestudios.com/portfolio
WE_CREATE = ['TV Commercials', 'UGC-style Videos', 'Static & Motion Ads', 'PDP & PLP Content', 'Brand Films', 'Social Content', 'Video Banners',
             'Explainer Animations', 'Product Photography', 'Founder & Profile Videos', 'Product Launch Videos', 'OOH Content', 'Email Visuals']

# the brands behind the untitled photos in the Work gallery, read from the file names; the rest show no label
PHOTO_BRANDS = [('gardyn', 'Gardyn'), ('freepower', 'FreePower'), ('publicrec', 'Public Rec'), ('public-rec', 'Public Rec'), ('wolfandshepherd', 'Wolf & Shepherd'),
                ('patrol', 'Patrol'), ('literati', 'Literati'), ('solidroad', 'Solidroad')]

# ---- Packages and About (October 28, 2026). Package names, prices and lines are from Mike's deck slide; the descriptions, pillars,
# team and page copy are from birdlinestudios.com/packages and /about.
PACKAGES = [
    dict(key='video', name='Video Editing', price='$8,000', per='/mo', starting=True,
         blurb='Get unlimited video edits across commercials, paid social, and brand content—all managed by your dedicated post-production team.',
         items=['Unlimited Edits & Revisions', 'Dedicated Video Editor', 'Dedicated Project Manager', 'VFX & Text Animations', 'Color Correcting & Grading', 'Sound Design & Mix', 'Music Licensing', 'Script & Copywriting'],
         workflow=['Birdline App', 'Slack Communication', 'Ongoing File Storage', 'Production Planning', 'Ad Performance Reviews', 'Recurring Strategy Calls', 'Weekly Project Tracker']),
    dict(key='design', name='Design & Animation', price='$6,000', per='/mo', starting=True,
         blurb='Scale your visuals with unlimited design and animations for paid ads, emails, and brand content—delivered fast, on-brand, and built to perform.',
         items=['Unlimited Designs & Animations', 'Dedicated Designer/Animator', 'Dedicated Project Manager', 'Graphic Design & Illustration', 'VFX, 3D, & Animation', 'Motion Graphics', 'Music Licensing', 'Copywriting'],
         workflow=['Birdline App', 'Slack Communication', 'Ongoing File Storage', 'Production Planning', 'Ad Performance Reviews', 'Recurring Strategy Calls', 'Weekly Project Tracker']),
]
WORKFLOW = ['Dedicated Project Manager', 'Slack Communication', 'Birdline App Integration', 'Recurring Strategy Calls', 'Ad Performance Reviews', 'Weekly Project Tracker']
WORKFLOW_WIDE = 'Campaign Workspace: every brief, deliverable, and result in the Birdline App'
PRODUCTION_TYPES = ['Commercials', 'UGC Videos', 'Paid Ads', 'Social Content', 'Profile Videos', 'Webpage Videos', 'Product Photography', 'Lifestyle Shoots', 'Studio Shoots', 'Webpage Images', 'Campaign Photos']
PILLARS = [
    ('The Outcome', 'Get unlimited deliverables each month with fast turnarounds and scalable production, so your content pipeline and team never slows down.'),
    ('The Birds', 'Partner with world-class creatives across video, photo, design, AI, and animation—operating as an extension of your in-house team.'),
    ('The System', 'Streamline your workflow in Slack with a dedicated PM, recurring creative and marketing calls, and weekly tracking to keep every project moving smoothly.'),
]
TEAM = [
    ('mike', 'Mike Pagan', 'Filmmaker', 'Red Bull, Fender, Nestle'),
    ('miles', 'Miles Jones', 'Content Creator', 'Blueprint, Gardyn, Champion'),
    ('ryan', 'Ryan Goeglein', 'Designer & Animator', 'Route, 686, Literati'),
    ('zac', 'Zachariah Jones', 'Filmmaker', 'Louis Vuitton, Suja, Pull&Bear'),
    ('grant', 'Grant Puckett', 'Photographer', 'Athletic Brewing, Cuts, Alo'),
    ('trevor', 'Trevor Hollander', 'Producer / DP', 'Nike, Clippers, Fender'),
    ('rebecca', 'Rebecca Hedayat', 'Photographer', 'Ford, Aviator Nation, Route'),
    ('bryan', 'Bryan Bartleson', 'Video Editor', 'Marvel, Disney, Sony'),
    ('james', 'James Mackenzie', 'Designer & 3D Animator', 'Jaguar, Hume, Willie’s Remedy'),
    ('joey', 'Joey Breese', 'Filmmaker', 'Nike, Adidas, Chivas'),
    ('megan', 'Megan Gray', 'Creative Director & Designer', 'Mattel, Casper, Netflix'),
]
WITHOUT = ['Limited deliverables from expensive shoots', 'Fragmented workflows', 'Scattered production emails', 'Slow turnaround times', 'Assets sent through email and random links', 'No system for iterations or measuring ROI', 'Juggling multiple agencies and contractors']
WITH = ['Unlimited deliverables', 'Dedicated project manager & creators', 'Direct communication via Slack', 'Weekly project tracker', 'Premium assets delivered via Frame.io', 'Biweekly creative & marketing meetings', 'World-class creators, all under one roof']
DELIVER = ['Organize and schedule ongoing shoots, regardless of the project size', 'Capture content anywhere with our extensive Birdline network', 'Provide initial assets within a week on average, Monday through Friday', 'Ensure cohesive and consistent quality throughout all your content']
COLLAB = ['Communicate directly via Slack and schedule recurring meetings with our Birds', 'Funnel all your content into our system for centralized access and fast iterations', 'Connect our Birds with your existing team, internal workflow, and the Birdline App', 'Maximize your marketing content with no deliverable or revision limits']
FAQ_PACKAGES = ['What counts as a deliverable?', 'How fast do deliverables come back?', 'Why wouldn\'t I just hire a full-time editor?', 'Do I own the media and the project files?',
                'What do we cover on recurring strategy calls?', 'Can I cancel?', 'How do we start?']
# questions that are not on the home page's FAQ (which the other lists draw on): added November 8, 2026
FAQ_EXTRA = {
    'What do we cover on recurring strategy calls?': 'We meet every other week, with weekly calls as needed. We review what’s been delivered, what’s in progress, and what’s coming up. '
                                                     'We also discuss which content is performing well and where there’s room to improve, then use what we learn to set the next creative priorities. '
                                                     'That could mean creating new deliverables from existing assets or planning a new production.',
}

# ---- the Birdline App page (October 28, 2026): copy from birdline.ai and the Birdline Knowledge Base
LOOP = [
    ('01 · Campaign', 'Brief the campaign', 'Draft with your AI copilot, edit as a team, and turn concepts into clear, actionable direction.'),
    ('02 · Deliverables', 'Produce together', 'Generate shot lists, manage deliverables, and keep every asset connected back to the original brief.'),
    ('03 · Insights', 'Measure & compound', 'Tie every ad back to its campaign, track your return on production spend, and turn insights into your next brief.'),
]
FEATURES = [
    dict(key='brief', label='Smart Brief', title='Build Clear, Actionable Briefs', img=('app4-brief', 1760, 1408, 'app4-brief-m', 1330, 1108),
         alt='A brief in Birdline, Crack Open Summer — Hero Spot Brief, with its Connections dropdown open: Creative Reports, Google and Notion connected, Figma coming soon, and PDF upload, beside the brief’s text and reference images.',
         p='Draft with AI or sync the docs you already have, then turn the concept into direction production can run with.',
         items=['Syncs Google Docs, Sheets, Slides, Notion, and PDFs', 'Tabs you add, rename, and reorder', 'An AI Assistant that drafts, rewrites, and fills the gaps', 'Images, video, audio, and fonts kept beside the brief']),
    dict(key='shots', label='Shot list', title='Generate Shot Lists Instantly', img=('app2-shots', 1760, 1408, 'app2-shots-m', 1230, 1026),
         alt='The Shot list tab of a brief in gallery view: generated shots, each with a visual, its framing and a short description, under buttons for Generate All Visuals, Props, Wardrobe and Locations.',
         p='AI turns the brief into a shot-by-shot plan, with a visual for every shot.',
         items=['Shots drafted straight from the brief', 'A visual for every shot; regenerate any one', 'Framing, lighting, wardrobe, props, and VO on each shot', 'Props, wardrobe, and locations rolled up for the shoot']),
    dict(key='deliverables', label='Deliverables', title='Track All of Your Creative', img=('app5-deliverables', 2000, 1375, 'app5-deliverables-m', 1330, 1108),
         alt='The Deliverables page in Birdline: a table of deliverables with campaign and brief, assignee, name, due date, asset link and status, above a switch between all and my deliverables and a list or calendar view.',
         p='Every deliverable with its owner, due date, and status, tied back to the brief it came from.',
         items=['Owner, due date, channel, type, and sizes', 'Status from Not Started to Launched', 'List or calendar; everything or just yours', 'Share by invite, by email, or with a read-only link']),
    dict(key='insights', label='Insights', title='Turn Insights Into Your Next Brief', img=('app6-insights', 2000, 1368, 'app6-insights-m', 1300, 1083),
         alt='The Insights page in Birdline with Meta selected: tiles for Campaign Revenue, Total Ad Spend, Production Spend, ROCS and ROPS, above the ad creatives with each ad’s revenue and spend.',
         p='Connect your ads, see what each campaign earned, and brief the next one from the results.',
         items=['Connect Meta and assign each ad to its campaign', 'ROPS™ and ROCS™ on every campaign', 'A Creative Report of what worked, ready to send', 'Generate New Brief starts the next one from the report']),
]
AROUND = [
    ('campaigns', 'Campaigns', 'One home per initiative: its briefs, overview, tasks, and budget.'),
    ('budget', 'Line-item budget', 'Pre-production, production, and post per brief: the spend behind ROPS™.'),
    ('brand', 'Brand library', 'Logos and products that keep shot lists and visuals on-brand.'),
    ('team', 'Team & roles', 'Owner, Admin, and Member seats, with tasks assigned by name.'),
    ('share', 'Sharing', 'Invite teammates, or send a read-only link that expires in 30 days.'),
    ('slack', 'Slack', 'Post a brief to a channel and get task updates where your team works.'),
]
FAQ_APP = ['What is Birdline?', 'Do I have to use the studio to use the app?', 'Do I have to move my docs out of Google or Notion?', 'Which ad platforms can I connect?', 'What are ROPS', 'How do we start?']

# the five pages in the app page's hero switch, in the order of the loop: whole screens of the redesign (proto/redesign.html, the
# rehaul (15) prototype), captured by proto_shots.js at 1600×1044 for wide screens (img/ws-<key>.webp) and at 1200×1048 for phones
# (img/ws-<key>-m.webp). The heights end the Insights page on the rule above each creative's metrics, so no screen is cut through text.
WS_SCREENS = [
    ('campaigns', 'Campaigns', 'The Campaigns page of the Birdline App: a sidebar with Campaigns, Deliverables and Insights, recent briefs, and eight campaign cards with cover photos, owner and deliverable count.'),
    ('brief', 'Smart Brief', 'A brief in Birdline, Crack Open Summer — Hero Spot Brief: its sections in a rail on the left (Concept, Hook, Visual Direction, On-Screen Copy, Distribution), the brief’s text in the editor, and four reference stills on the right.'),
    ('shots', 'Shot list', 'The Shot list tab of the same brief in gallery view: eighteen generated shots, each with a visual, its framing and a short description, with Story and Production ordering.'),
    ('tasks', 'Deliverables', 'The Deliverables page of the Birdline App: filters by assignee, status, due date and campaign beside a table of deliverables with campaign and brief, assignee, name, due date, asset link and status.'),
    ('insights', 'Insights', 'The Insights page of the Birdline App for the Influencer & Whitelisting 2026 campaign: Meta and Google Ads connections, campaign revenue, ad spend, production spend, ROCS and ROPS tiles, the metric and date filters, and a row of the campaign’s ad creatives.'),
]
WS_SIZES = {'d': (2400, 1566), 'm': (1320, 1153)}

# the logos that float beside the app page's headline and drift down into the workspace on scroll: (asset key, side, x from that
# side as a share of the hero's width, y from the top in px, tilt, drift rate, tile size in px, bob delay). site.js moves each one
# along the line from where it rests to the centre of the workspace and fades it out as it reaches the workspace's top edge.
FLOATERS = [
    ('int-gdocs',   'l', '5%',  170, '-6deg', .42, 64, '0s'),
    ('int-slack',   'l', '14%', 295, '5deg',  .58, 58, '-1.6s'),
    ('int-meta',    'l', '6%',  420, '4deg',  .36, 66, '-3.1s'),
    ('int-notion',  'l', '14%', 545, '-5deg', .50, 60, '-2.0s'),
    ('int-wave',    'l', '6%',  665, '6deg',  .46, 56, '-0.8s'),
    ('int-gsheets', 'r', '5%',  195, '6deg',  .48, 62, '-2.4s'),
    ('int-gads',    'r', '14%', 335, '-4deg', .38, 60, '-4.0s'),
    ('int-gslides', 'r', '7%',  480, '-6deg', .56, 66, '-1.2s'),
    ('int-pdf',     'r', '13%', 625, '5deg',  .44, 56, '-3.6s'),
]

# the Packages hero: where each of the homepage's library tiles sits around the copy (x and y as a share of the stage, width in cqw,
# tilt), spread wider than on the homepage because the headline is on two long lines
HERO_TILES = {
    # (x, y, width in cqw, tilt, depth), laid out on a ring around the copy, each tile mirrored by one of the same shape on the other
    # side: one at the top and one at the bottom on the centre line, then six mirrored pairs down the sides
    'cov-3': (44, 5, 12, '0deg', 'far'),                                                               # top centre
    'work-gardyn-wine': (25.6, 7.7, 12, '-3deg', 'near'), 'cs-literati': (62.4, 7.7, 12, '3deg', 'near'),       # ±26°
    'work-sneaker': (13.4, 17.7, 7, '-4deg', 'far'), 'work-panel': (79.6, 17.7, 7, '4deg', 'far'),               # ±52°
    'cs-publicrec': (2.1, 37.1, 13, '-4deg', 'near'), 'cs-whoop': (85, 37.1, 13, '4deg', 'near'),                # ±80°
    'work-deadlift': (5.9, 55.9, 8.5, '-5deg', 'far'), 'work-gauge': (85.6, 55.9, 8.5, '5deg', 'far'),           # ±108°
    'work-tequila': (16, 70.7, 7.5, '-3deg', 'near'), 'alt-pancakes': (76.5, 72.4, 7.5, '3deg', 'near'),         # ±134°
    'work-hamilton': (31.2, 79.2, 6, '-3deg', 'far'), 'work-cauliflower': (62.8, 79.2, 6, '3deg', 'far'),        # ±158°
    'work-fivepockets': (47, 79, 6, '0deg', 'near'),                                                   # bottom centre
}

# ---- Willie's Remedy (November 1, 2026): the Green Guide series and James's 3D product animation, from Mike's draft. The stills are frames
# pulled from the delivered episodes and the 3D clips; the cover is the frame Mike supplied. Adam Walker's testimonial and photo came in
# on November 5, 2026.
def _wr(src, alt, w, h):
    return dict(src=src, asp=round(w / h, 2), href=src, alt=alt, w=w, h=h)
WR_CASE = dict(
    url='/portfolio/willies-remedy/', title='Willie’s Remedy', heroBg='wr/cover.jpg', logo='', logoSet=[],
    copy=dict(
        overview=[
            'Willie’s Remedy wanted an educational, entertaining YouTube series for a broad audience, including viewers who are older or new to cannabis. The brief: Vox-style explainers of two to three minutes each, with AI voiceover, that make THC drinks easy to understand.',
            'We presented two visual directions in Figma. The client chose the first: halftone and black-and-white textures, illustrations that pay homage to the Willie mascot, a slightly western theme, and a subtle washed green. The animation mixes illustration, texture, lifestyle footage, and motion-heavy text slides.',
            'After Episode 1, the client asked for a faster pace. We retimed the animation to a 1.2× voiceover, which cut 20 to 30 seconds, and that became the standard. By Episode 2 the intro and pacing were locked, so later episodes came together faster.',
            'Alongside the series, our 3D animator built product animations for social: the Willie’s Remedy+ bottle, the social tonic trio, and the Sleep Like a Legend gummies.',
        ],
        results=[
            'Three episodes, delivered monthly: Episode 1, What Are THC Drinks? (March 2), Episode 2, THC Drinks vs Alcohol (April 7), and Episode 3, Finding Your Perfect THC Drink Dose (May 8). A repeatable template, from the intro to the pacing, now carries the series forward.',
        ],
        services=['YouTube Series', 'GFX/Animations', 'Illustration', '3D / VFX'],
        quotes=[dict(name='Adam Walker', title='Content Director',
                     paras=['Super creative. Super fast. Simply put, Birdline gets it done—and makes it fun. Working with them feels like an extension of our team. '
                            'Besides just being ridiculously talented on the tools, they’re great communicators. Guesswork never enters the picture. '
                            'Clear direction, effective collaboration and deliverables that help move the needle. Peace of mind, by design.'])],
        next=['Literati', 'Gardyn', 'WHOOP', 'Public Rec'],
    ),
    gal=[
        dict(video='wr-ep1.mp4', poster='wr/wr-ep1-title.jpg', alt='The Green Guide · Ep. 1, What Are THC Drinks?', w=1280, h=720),
        dict(video='wr-3d-social.mp4', poster='wr/wr-3d-bottle.jpg', alt='Willie’s Remedy+ · 3D product animation', w=720, h=1280),
        dict(video='wr-ep2.mp4', poster='wr/wr-ep2-title.jpg', alt='The Green Guide · Ep. 2, THC Drinks vs Alcohol', w=1280, h=720),
        dict(video='wr-3d-gummies.mp4', poster='wr/wr-3d-gummies.jpg', alt='Sleep Like a Legend gummies · 3D', w=1024, h=1280),
        dict(video='wr-ep3.mp4', poster='wr/wr-ep3-how.jpg', alt='The Green Guide · Ep. 3, Finding Your Perfect THC Drink Dose', w=1280, h=720),
        dict(video='wr-3d-newdrop.mp4', poster='wr/wr-3d-newdrop.jpg', alt='New drop · 3D', w=720, h=1280),
        dict(video='wr-3d-room.mp4', poster='wr/wr-3d-room.jpg', alt='Willie’s Remedy · 3D', w=1280, h=600),
        dict(video='wr-3d-bag.mp4', poster='wr/wr-3d-bag.jpg', alt='Sleep Like a Legend · 3D', w=1024, h=1280),
        # the three 3D pieces Mike sent on November 3, 2026: the bottle-to-cans swap, the can "new coat of paint" and the Social Tonic snap pack
        dict(video='wr-3d-bottle-swap.mp4', poster='wr/wr-3d-bottle-swap.jpg', alt='New get ’up, same great taste · 3D', w=1024, h=1280),
        dict(video='wr-3d-can-bob.mp4', poster='wr/wr-3d-can-bob.jpg', alt='New coat of paint on an old favorite · 3D', w=1280, h=720),
        dict(video='wr-3d-snap-pack.mp4', poster='wr/wr-3d-snap-pack.jpg', alt='Social Tonic snap pack · 3D', w=1280, h=1280),
    ],
)

# ---- EDJY (November 2, 2026): the case Mike wrote, with the challenge, the four-step approach and why it worked (the Results section
# waits for the numbers). The gallery is frames pulled from the ads in Mike's EDJY Content folder; the cover is the new-colours launch still.
EDJY_CASE = dict(
    url='/portfolio/edjy/', title='EDJY', heroBg='edjy/cover-colors.jpg', logo='', logoSet=[],   # the new-colours launch still, as on the case card (November 9, 2026)
    copy=dict(
        overview=[
            'EDJY makes precision-engineered personal care tools, including a single-blade nail cutter and tweezers. They were taking on a category still defined by an 1881 design. They had great footage and bold ideas, but they needed a partner to turn them into a steady stream of ads that win attention and drive sales.',
        ],
        challenge=['Launch two new products with a high volume of fresh video, fast.', 'Find out which messages and formats resonate, and double down on them.', 'Build a library of lasting brand footage, not just one-off ads.'],
        approach=[
            ('Edit at speed, in every format', 'We turned EDJY’s footage into social-first videos built for each platform and placement. Formats included street interviews across multiple cities, real-reaction videos, product demos and photography series.'),
            ('Explore creative beyond the brief', 'We came to EDJY with our own concepts, built around the real frustrations of traditional clippers and the clean-cut difference EDJY makes. Each idea came in several versions, so EDJY could test hooks, formats and voices.'),
            ('Let the data steer', 'We joined EDJY’s weekly performance reviews and began a regular cycle of data-informed re-edits. Each round, we studied what was working, rebuilt the strongest ideas with sharper hooks and tested again. This showed us which videos earned attention and which turned that attention into purchases.'),
            ('Go from edit bay to set', 'EDJY wanted lasting footage, so we planned and produced a full lifestyle photo and video shoot. It covered casting, location, crew, scheduling and post-production. The goal was a deep library of product-in-use footage that EDJY can keep drawing on in future edits.'),
        ],
        results=[],   # no Results section until the numbers are in (Mike, November 9, 2026)
        why=[('workspace', 'One shared workflow', 'Briefs, feedback and priorities all live in the Birdline app, so nothing gets lost.'),
             ('repeat', 'A creative loop that never stops', 'We make the work, measure it, learn from it and make it better.'),
             ('camera', 'Creative and production under one roof', 'The same team that edits the ads also plans the shoots that feed them.')],
        services=['Paid Ads', 'Social Content', 'UGC', 'Photography', 'Video Production'],
        quotes=[dict(name='John Bradford', title='Creative Director', paras=['"Mike and the Birdline team have been a thoughtful creative partner for EDJY. They bring a strong editorial eye to our footage and help shape it into engaging, social-first videos. Mike is collaborative, communicative, and open to feedback, which makes it easy to work through ideas and keep improving the work together. We’ve appreciated Birdline’s flexibility and creative input as we take our video program to the next level."'])],
        next=['Patrol', 'Gardyn', 'FreePower', 'Route'],
    ),
    gal=[
        dict(video='edjy-01.mp4', poster='edjy/01.jpg', alt='1881 vs 2026 · Vertical ad', w=720, h=1280),
        dict(video='edjy-04.mp4', poster='edjy/04.jpg', alt='Beginner grooming · Ad', w=1280, h=720),
        dict(video='edjy-05.mp4', poster='edjy/05.jpg', alt='Crush vs slice · Vertical ad', w=720, h=1280),
        dict(video='edjy-16.mp4', poster='edjy/16.jpg', alt='Real reactions · Ad', w=1280, h=720),
        dict(video='edjy-06.mp4', poster='edjy/06.jpg', alt='Tweezers launch · Hook 1', w=720, h=1280),
        dict(video='edjy-19.mp4', poster='edjy/19.jpg', alt='Lunar Rock · Product photo series', w=720, h=1280),
        dict(video='edjy-09.mp4', poster='edjy/09.jpg', alt='Hate filing your nails? · 4:5 ad', w=720, h=900),
        dict(video='edjy-10.mp4', poster='edjy/10.jpg', alt='LA street interviews · Mashup', w=720, h=1280),
        dict(video='edjy-02.mp4', poster='edjy/02.jpg', alt='New colors · Launch', w=720, h=1280),
        dict(video='edjy-07.mp4', poster='edjy/07.jpg', alt='Tweezers launch · Hook 2', w=720, h=1280),
        dict(video='edjy-21.mp4', poster='edjy/21.jpg', alt='Quartz Pink · Product photo series', w=720, h=1280),
        dict(video='edjy-03.mp4', poster='edjy/03.jpg', alt='Street interviews · Ad', w=1280, h=720),
        dict(video='edjy-17.mp4', poster='edjy/17.jpg', alt='The cleanest slice · Vertical ad', w=720, h=1280),
        dict(video='edjy-12.mp4', poster='edjy/12.jpg', alt='NY street interviews · Mashup', w=720, h=900),
        dict(video='edjy-15.mp4', poster='edjy/15.jpg', alt='Quartz Pink · Launch', w=720, h=1280),
        dict(video='edjy-08.mp4', poster='edjy/08.jpg', alt='Tweezers launch · Hook 3', w=720, h=1280),
        dict(video='edjy-23.mp4', poster='edjy/23.jpg', alt='Two colors · Product photo series', w=720, h=1280),
        dict(video='edjy-14.mp4', poster='edjy/14.jpg', alt='Pro tips · Ad', w=1280, h=720),
        dict(video='edjy-18.mp4', poster='edjy/18.jpg', alt='Us vs them · Ad', w=1280, h=720),
        dict(video='edjy-11.mp4', poster='edjy/11.jpg', alt='Lunar Rock · Launch', w=720, h=1280),
        dict(video='edjy-24.mp4', poster='edjy/24.jpg', alt='Two colors · Product photo series', w=720, h=1280),
        dict(video='edjy-13.mp4', poster='edjy/13.jpg', alt='NY street interviews · Mashup v2', w=720, h=900),
        dict(video='edjy-20.mp4', poster='edjy/20.jpg', alt='Lunar Rock · Product photo series', w=720, h=1280),
        dict(video='edjy-22.mp4', poster='edjy/22.jpg', alt='Quartz Pink · Product photo series', w=720, h=1280),
    ],
)

# ---- work Mike sends for a case study by file (November 3, 2026): transcoded for the web (video/<name>.mp4) with a frame of each as its
# still (img_map 'new/<name>.jpg'). Newest first; the build puts these ahead of the gallery the live site and the folders shaped. svc names
# the service line the Work page shows (Commercial pieces join the Commercial shelf, Profiles the Profiles shelf).
def _new(name, alt, w, h, svc=None):
    d = dict(video=name + '.mp4', poster='new/' + name + '.jpg', alt=alt, w=w, h=h)
    if svc: d['svc'] = svc
    return d
# ---- the AI Content page (November 5, 2026): the AI work from Mike's AI Content folder, brand first in every caption. Videos
# are web encodes of the originals (public/video on the Next.js site, the Blob store in production); the two renders are stills.
def _ai(name, alt, w, h):
    return dict(video=name + '.mp4', poster='new/' + name + '.jpg', alt=alt, w=w, h=h, svc='AI Content')
AI_WORK = [
    _ai('ai-luxonis-oak4-hero', 'Luxonis · OAK 4 Series hero film', 1280, 720),
    _ai('ai-venus-et-fleur-roses', 'Venus et Fleur · Eternity roses', 720, 1280),
    _ai('ai-freepower-wayfair', 'FreePower · Wayfair vanity spot', 1280, 1280),
    _ai('ai-gardyn-limited-edition', 'Gardyn · Limited-edition fall launch', 1024, 1280),
    _ai('ai-freepower-countertop-16x9', 'FreePower · Power, built into your countertop', 1280, 720),
    _ai('ai-gardyn-kelby-harvest-happiness', 'Gardyn · Harvest happiness anywhere', 720, 1280),
    ('site', 'ai/gardyn-living-room-1.jpg', 'Gardyn · Living room render'),
    _ai('ai-freepower-countertop-4x5', 'FreePower · Built into your countertop', 1024, 1280),
    _ai('ai-gardyn-24-7-care', 'Gardyn · 24/7 care with Kelby', 1024, 1280),
    _ai('ai-gardyn-real-mom-talk', 'Gardyn · Real mom talk', 720, 1280),
    _ai('ai-freepower-countertop-glow', 'FreePower · Countertop charging', 1280, 720),
    _ai('ai-gardyn-home-vs-competition', 'Gardyn · Gardyn Home vs. the competition', 720, 1280),
    _ai('ai-gardyn-spring-savings', 'Gardyn · Spring savings', 720, 1280),
    ('site', 'ai/gardyn-living-room-2.jpg', 'Gardyn · Living room render'),
    _ai('ai-gardyn-diy-horror', 'Gardyn · DIY horror', 720, 1280),
    _ai('ai-gardyn-grocery-store-rebel', 'Gardyn · Grocery store rebel', 720, 1280),
    _ai('ai-gardyn-variety-showcase', 'Gardyn · Variety showcase', 720, 1280),
    _ai('ai-gardyn-ypod-lettuce', 'Gardyn · yPod variety, lettuce', 1080, 1080),
    _ai('ai-gardyn-ypod-variety-cream', 'Gardyn · yPod variety, year-round', 1080, 1080),
]
AI_HERO = [AI_WORK[0], AI_WORK[1], AI_WORK[2]]   # Luxonis, Venus et Fleur, FreePower across the hero

# ---- November 8, 2026: the pieces Mike sent that day, transcoded for the web (video/<name>.mp4) with a frame of each as its still.
# svc names the service line the Work page shows under the tile.
NOV8 = {k: _new(k, alt, w, h, svc) for k, alt, w, h, svc in [
    ('commercial-chivas-nike-paisa-boys', 'Chivas × Nike × Paisa Boys · Commercial', 1280, 960, 'Commercial'),
    ('commercial-nike-paisa-boys-mexico', 'Nike × Paisa Boys, Mexico · Commercial', 1280, 880, 'Commercial'),
    ('publicrec-ugc-dealmaker-pant-interview', 'Deal Maker pant interview · UGC', 720, 1280, 'UGC'),
    ('whoop-dr-eric-verdin-trailer', 'Dr. Eric Verdin · Podcast trailer', 720, 1280, 'Audio'),
    ('whoop-refreshed-creator-comp-9x16', 'Refreshed creator compilation · UGC', 720, 1280, 'UGC'),
    ('impactce-intro', 'ImpactCE · Intro animation', 1280, 720, 'Motion Graphics'),
    ('literati-treasured-tales-intro', 'Treasured Tales · Intro animation', 1280, 720, 'Motion Graphics'),
    ('literati-treasured-tales-store-promo', 'Treasured Tales · Store promo', 1280, 720, 'Motion Graphics'),
    ('whoop-al-standalone-4x5', 'Advanced Labs · Paid media', 1024, 1280, 'Paid Social'),
    ('whoop-refreshed-creator-july-16x9', 'Refreshed creator compilation, July · Paid social', 1280, 720, 'Paid Social'),
    ('whoop-psg-giant-screen-ad', 'PSG giant-screen ad · OOH', 1280, 720, 'OOH'),
    ('whoop-behind-the-drivers-seat-lewis', 'From Behind the Driver’s Seat, Lewis Hamilton · Cutdown', 720, 1280, 'Profiles'),
    ('whoop-perfmedia-customizable-4x5', 'Customizable · Performance media', 1024, 1280, 'Paid Social'),
    ('whoop-perfmedia-product-render-16x9', 'Refreshed product render · Performance media', 1280, 720, '3D / VFX'),
    ('whoop-peloton-partnership-launch-4x5', 'Peloton partnership launch · Paid social', 1024, 1280, 'Paid Social'),
]}
UNWORK_KEEGAN = _new('686-unwork-keegan-hosefros', 'UNWORK: Keegan Hosefros · Profile', 1280, 720, 'Profiles')   # on the 686 case study and the Profiles page
# the five Gardyn pieces Mike sent on November 9, 2026 (web encodes of the finals; the originals' names are in FALLBACK)
GARDYN_NOV9 = {k: _new(k, alt, w, h, svc) for k, alt, w, h, svc in [
    ('gardyn-song-30', 'The Gardyn Song · :30 commercial', 1280, 720, 'Commercial'),
    ('gardyn-fresh-got-easier', 'Fresh Got Easier · Commercial', 1280, 720, 'Commercial'),
    ('gardyn-ctv-2026-grow-something', 'Grow Something · :15 CTV spot, 2026', 1280, 720, 'Commercial'),
    ('gardyn-grow-it-at-home', 'Grow It at Home · Commercial', 1280, 720, 'Commercial'),
    ('gardyn-if-youve-been-waiting-9x16', 'If You’ve Been Waiting, summer sign · Paid social', 720, 1280, 'Paid Social'),
]}
# the pieces Mike sent on the evening of November 9, 2026 (web encodes of the finals; the originals' names are in FALLBACK)
NOV9_PM = {k: _new(k, alt, w, h, svc) for k, alt, w, h, svc in [
    ('686-the-hundreds-logo-collab', '686 × The Hundreds logo collab · Social', 720, 1280, 'Paid Social'),
    ('publicrec-nobull-built-for-this', 'Built for This · Public Rec × NOBULL', 1280, 720, 'Commercial'),
    ('publicrec-gamechanger-tv-2024', 'Gamechanger · :30 TV commercial, 2024', 1280, 720, 'Commercial'),
    ('publicrec-dad-reel-daymakers', 'Dad Reel: Daymakers · Lifestyle', 1280, 720, 'Paid Social'),
    ('publicrec-dad-reel-gamechangers', 'Dad Reel: Gamechangers · Lifestyle', 1280, 720, 'Paid Social'),
    ('publicrec-dad-reel-dealmaker', 'Dad Reel: Dealmaker · Lifestyle', 1280, 720, 'Paid Social'),
    ('publicrec-dad-reel-mashup', 'Dad Reel: Mashup · Lifestyle', 1280, 720, 'Paid Social'),
    ('publicrec-dealmakers-anniversary-sale-4x5', 'Dealmakers, Anniversary Sale · 4:5 ad', 1024, 1280, 'Paid Social'),
    ('publicrec-aded-pant-drawstring-4x5', 'ADED pant, drawstring · 4:5 ad', 1024, 1280, 'Paid Social'),
    ('nike-la-dunk', 'Nike LA Dunk · Brand film', 1280, 720, 'Commercial'),
    ('wolf-and-shepherd-gift-giving', 'Wolf & Shepherd, gift giving · Paid social', 1080, 1080, 'Paid Social'),
    ('gardyn-health-enthusiasts', 'Health enthusiasts · Paid social', 1280, 720, 'Paid Social'),
    ('tag-scrubs-quality', 'TAG Scrubs: Quality · Commercial', 1280, 720, 'Commercial'),
    ('tag-scrubs-perks', 'TAG Scrubs: Perks · Commercial', 1280, 720, 'Commercial'),
    # the three that followed later that night: the Warmer spot (its still is the frame Mike sent), the Wolf & Shepherd styling square and 686's colour-change square
    ('warmer-real-advice', 'Warmer: Real Advice From People Who Lived It · Commercial', 1280, 720, 'Commercial'),
    ('wolf-and-shepherd-styling', 'Wolf & Shepherd, styling · Paid social', 1080, 1080, 'Paid Social'),
    ('686-features-color-change-2023', 'Features, colour change · Social', 1080, 1080, 'Paid Social'),
    # the Literati Content folder Mike connected at the end of the night: fourteen videos, encoded the same way
    ('literati-about-book-fairs', 'About Literati Book Fairs · Brand film', 1280, 720, 'Film'),
    ('literati-book-fair-sizzle', 'Book Fair Sizzle · Brand film', 1280, 720, 'Film'),
    ('literati-start-your-book-fair', 'Start Your Book Fair · Explainer', 1280, 720, 'Film'),
    ('literati-ease-of-setup', 'Ease of Setup & Operations · Explainer', 1280, 720, 'Film'),
    ('literati-librarian-testimonials', 'Librarian testimonials · Mashup', 1280, 720, 'UGC'),
    ('literati-storytime-reimagined-1x1', 'Storytime Reimagined · Animated ad', 1080, 1080, 'Motion Graphics'),
    ('literati-bfa-event-sizzle-9x16', 'Book Fair event sizzle · Social', 720, 1280, 'Paid Social'),
    ('literati-make-reading-fun-again-9x16', 'Make Reading Fun Again · Paid social', 720, 1280, 'Paid Social'),
    ('literati-green-screen-ad-9x16', 'Green-screen ad · Paid social', 720, 1280, 'Paid Social'),
    ('literati-custom-book-box-9x16', 'Custom Book Box · Paid social', 720, 1280, 'Paid Social'),
    ('literati-favorite-book-series-9x16', 'Favorite book series · UGC', 720, 1280, 'UGC'),
    ('literati-unboxing-moments-9x16', 'Unboxing moments · UGC', 720, 1280, 'UGC'),
    ('literati-pov-best-day-9x16', 'POV: best day of the school year · UGC', 720, 1280, 'UGC'),
    ('literati-rejoined-9x16', 'Rejoined Literati · UGC', 720, 1280, 'UGC'),
    # two more UFL team episodes
    ('ufl-defenders-rankings-ep1', 'Rankings, Ep. 1 · Defenders', 720, 1280, 'Paid Social'),
    ('ufl-battlehawks-rock-and-roll-ep2', 'Rock & Roll Ricky, Ep. 2 · Battlehawks', 720, 1280, 'Paid Social'),
]}
# the Literati statics from the same folder (flyers, posters, signs and social statics), for the case study and the Design page
def _lit(name, alt, w, h):
    return dict(src='new/%s.jpg' % name, asp=w / h, href='new/%s.jpg' % name, alt=alt, w=w, h=h)
LITERATI_STATICS = [
    _lit('literati-f26-featured-book-flyer', 'Go for Gold · Featured book flyer', 1641, 2000),
    _lit('literati-flyer-pages-2-3', 'Picture Books & Chapter Books · Flyer spread', 2000, 1219),
    _lit('literati-s27-fair-announcement-poster', 'Get a Kick Out of Reading · Fair poster', 1296, 1728),
    _lit('literati-f26-store-poster', 'There’s S’more to Explore · Store poster', 1332, 1764),
    _lit('literati-flyer-pages-4-5', 'Graphic Novels & Fun and Games · Flyer spread', 2000, 1219),
    _lit('literati-s27-checkout-sign-3', 'The Book Fair Is Coming · Checkout sign', 1296, 1656),
    _lit('literati-f26-online-fair-flyer-front', 'Our Book Fair Is Open · Online fair flyer', 1260, 1512),
    _lit('literati-hey-mom-static', 'Hey, Mom · Static ad', 2000, 2000),
    _lit('literati-flyer-pages-5-6', 'Middle Grade & Support Your School · Flyer spread', 2000, 1219),
    _lit('literati-f26-library-checkout-sign', 'Gear Up for Our Book Fair · Library sign', 1238, 1588),
    _lit('literati-volunteer-social-post', 'Book Fair Volunteer · Social post', 1999, 2000),
    _lit('literati-explore-new-worlds-9x16', 'Explore New Worlds · Story ad', 1125, 2000),
    _lit('literati-f26-online-fair-flyer-back', 'Zip Online for More Favorites · Online fair flyer', 1260, 1512),
    _lit('literati-smart-value', 'Screen time, story time · Static ad', 2000, 2000),
    _lit('literati-s27-acrylic-sign', 'Free Bookmark · Acrylic sign', 850, 1110),
    _lit('literati-flyer-back-cover', 'Make a Book Fair Game Plan · Flyer back', 1641, 2000),
    _lit('literati-social-proof-1x1', 'Social proof · Static ad', 1080, 1080),
    _lit('literati-s27-checkout-sign-1', 'Create Your Digital Wallet · Checkout sign', 1296, 1656),
    _lit('literati-12-days-of-giveaways', '12 Days of Giveaways · Social template', 1600, 2000),
    _lit('literati-volunteers-social-post', 'Book Fair Volunteers · Social post', 1999, 2000),
    _lit('literati-smart-value-alt', 'Literati vs. digital subscriptions · Static ad', 2000, 2000),
    _lit('literati-social-proof-9x16', 'Social proof · Story ad', 1080, 1920),
    _lit('literati-s27-checkout-sign-2', 'Create Your Digital Wallet · Checkout sign', 648, 828),
]
# the Literati GIFs: email and web loops, their own block under the case study's work (served as they are, animated)
LITERATI_GIFS = [
    ('new/literati-gif-book-fairs.gif', 'Literati Book Fairs · Logo loop'),
    ('new/literati-gif-book-stack.gif', 'Book stack'),
    ('new/literati-gif-gift-card-stack.gif', 'Gift card stack'),
    ('new/literati-gif-checklist.gif', 'Checklist rotation'),
    ('new/literati-gif-card-stack.gif', 'Card stack'),
    ('new/literati-gif-gift-card-scale.gif', 'Gift card scale'),
    ('new/literati-gif-kid-book.gif', 'Kid with a book'),
    ('new/literati-gif-logo-color-change.gif', 'Logo colour change'),
    ('new/literati-gif-logo-hover.gif', 'Logo hover'),
]
# the six Public Rec stills Mike sent the same evening, for the case study's gallery
def _still(name, alt, w, h):
    return dict(src='new/%s.jpg' % name, asp=w / h, href='new/%s.jpg' % name, alt=alt, w=w, h=h)
PUBLICREC_STILLS = [
    _still('publicrec-still-dealmaker-street', 'Public Rec · Downtown', 1334, 2000),
    _still('publicrec-still-bar-wave', 'Public Rec · At the bar', 2000, 1334),
    _still('publicrec-still-stretch', 'Public Rec · The stretch', 1334, 2000),
    _still('publicrec-still-bar-stool', 'Public Rec · Bar stool', 2000, 1334),
    _still('publicrec-still-office-coffee', 'Public Rec · Office', 1334, 2000),
    _still('publicrec-still-ledge', 'Public Rec · On the ledge', 1000, 1200),
]
# the stills Mike sent on November 10, 2026: the shorts shoot (digital, in the studio and on the stairs) and the film frames from
# the same rolls as IMG1803-R01-012 and -033 (the stairs and the boxing gym) and the women's roll (IMG8682). The film frames
# also show on the Film service page (services.py), with the House Beer frame that is film too but not Public Rec.
PUBLICREC_NOV10 = [
    _still('publicrec-film-stairs', 'Public Rec · On film', 1336, 2000),
    _still('publicrec-still-kettlebell-grip', 'Public Rec · Kettlebell', 1334, 2000),
    _still('publicrec-film-field', 'Public Rec · On film', 2000, 1340),
    _still('publicrec-still-shorts-studio', 'Public Rec · The shorts', 1334, 2000),
    _still('publicrec-film-boxer', 'Public Rec · On film', 1336, 2000),
    _still('publicrec-still-backpack-stairs', 'Public Rec · The backpack', 2000, 1334),
    _still('publicrec-film-coat', 'Public Rec · On film', 1340, 2000),
    _still('publicrec-still-kettlebell-swing', 'Public Rec · The swing', 1334, 2000),
]
HOUSE_BEER_FILM = _still('house-beer-forest', 'House Beer · On film', 1500, 2000)
GARDYN_NOV10 = [
    _still('gardyn-kitchen-wide', 'Gardyn · In the kitchen', 2000, 1334),
    _still('gardyn-product-studio', 'Gardyn · The tower', 1334, 2000),
    _still('gardyn-kitchen-tall', 'Gardyn · In the kitchen', 1334, 2000),
]

def _spread(items, extra, start=1, every=3):
    """items with the extra pieces dealt in among them, one every few places from start, so stills and videos mix"""
    out, extra = list(items), list(extra)
    at = start
    while extra and at <= len(out):
        out.insert(at, extra.pop(0)); at += every
    return out + extra
# library videos a new piece replaces, in place, on the case study and the Work page (November 9, 2026): the 686 Gore-Tex Pro
# review gives way to the 686 × The Hundreds collab; the Gardyn 4.0 twin that sat in the FreePower folder (the same spot as
# 923557755) gives way to the Health enthusiasts ad
REPLACE_VIDEOS = {'787075185': NOV9_PM['686-the-hundreds-logo-collab'], '927324603': NOV9_PM['gardyn-health-enthusiasts']}
# the pieces with no case study of their own (the Paisa Boys spots, the ImpactCE intro): on the service pages and the Work page's shelves
# The files Mike uploaded to the store on November 8, 2026 are the originals under their own names, not the web encodes; until the
# encodes are there, a tile or the player falls back to the original (data-fallback, site.js) when the encode is not found.
FALLBACK = {
    '686-the-hundreds-logo-collab.mp4': '686_logo_collab_-_final_v1 (1080p).mp4',
    'publicrec-nobull-built-for-this.mp4': 'Public-Rec_BuiltForThis_Ad1_16x9_V6Rev.mp4',
    'publicrec-gamechanger-tv-2024.mp4': 'PublicRec_Gamechanger_TV_Commercial_2024_16x9_30_Broadcast_NoSaleEndCard (1).mp4',
    'publicrec-dad-reel-daymakers.mp4': 'Public-Rec__DadReel_Daymakers_Lifestyle_16x9_Draft1_V1.mp4',
    'publicrec-dad-reel-gamechangers.mp4': 'Public-Rec__DadReel_Gamechangers_Lifestyle_16x9_Draft1_V1.mp4',
    'publicrec-dad-reel-dealmaker.mp4': 'Public-Rec__DadReel_Dealmaker_Lifestyle_16x9_Draft1_V1.mp4',
    'publicrec-dad-reel-mashup.mp4': 'Public-Rec__DadReel_Mashup_16x9_Draft1_V1.mp4',
    'publicrec-dealmakers-anniversary-sale-4x5.mp4': 'Public-Rec_Dealmakers_AnniversarySale2024_4x5_V1.mp4',
    'publicrec-aded-pant-drawstring-4x5.mp4': 'PublicRec_aded_pant_ad_-_4x5_drawstring_v4_v1 (1080p).mp4',
    'nike-la-dunk.mp4': 'nike,_la_dunk_v1 (1080p).mp4',
    'wolf-and-shepherd-gift-giving.mp4': 'wolf_&_shepherd_-_gift_giving_v1 (1080p).mp4',
    'gardyn-health-enthusiasts.mp4': 'gardyn_-_health_enthusiasts_v1 (1080p).mp4',
    'tag-scrubs-quality.mp4': 'tag_quality_16x9_v2_1_v1 (1080p).mp4',
    'tag-scrubs-perks.mp4': 'tag_perks_16x9_v2_v1 (1080p).mp4',
    'warmer-real-advice.mp4': 'warmer_-_real_advice_from_people_who_lived_it_v1 (1080p).mp4',
    'wolf-and-shepherd-styling.mp4': 'WS_styling_1x1_v2_v1 (1080p).mp4',
    '686-features-color-change-2023.mp4': '686_featurescolorchange_2023rev_finalcopy3_v3_1x1 (1)_v1 (1080p).mp4',
    'literati-about-book-fairs.mp4': 'About Literati Book Fairs FIX 16x9 V2.mp4',
    'literati-book-fair-sizzle.mp4': 'Book Fair Sizzle 16x9 V2.mp4',
    'literati-start-your-book-fair.mp4': 'StartYourBookfair 16x9 V4.mp4',
    'literati-ease-of-setup.mp4': 'Ease of Setup & Operations_16x9_V3.mp4',
    'literati-librarian-testimonials.mp4': 'Librarian Testimonial MashUp New 16x9 V4.mp4',
    'literati-storytime-reimagined-1x1.mp4': 'Storytime_Reimagined_Ad_1x1_v7_Purple.mp4',
    'literati-bfa-event-sizzle-9x16.mp4': 'BFA Event Sizzle 9x16 V5.mp4',
    'literati-make-reading-fun-again-9x16.mp4': 'MakeReadingFunAgain 9x16 V3Rev.mp4',
    'literati-green-screen-ad-9x16.mp4': 'GreenScreenAd Short1 9x16 V4 (1).mp4',
    'literati-custom-book-box-9x16.mp4': 'Custom Book Box 9x16 V1 (1).mp4',
    'literati-favorite-book-series-9x16.mp4': 'Favorite Book Series 9x16 V1.mp4',
    'literati-unboxing-moments-9x16.mp4': 'Unboxing Moments 9x16 V2Rev.mp4',
    'literati-pov-best-day-9x16.mp4': 'POVBestDayOfTheSchoolYear 9x16 V1.mp4',
    'literati-rejoined-9x16.mp4': 'Rejoined Literati 9x16 V3.mp4',
    'ufl-defenders-rankings-ep1.mp4': 'UFL_Defenders_Rankings_Ep_1_9x16_V1.mp4',
    'ufl-battlehawks-rock-and-roll-ep2.mp4': 'UFL_Battlehawks_Rock__Roll_Ep_2_9x16_V1.mp4',
    'gardyn-song-30.mp4': 'GardynSong_30_16x9_V7Rev.mp4',
    'gardyn-fresh-got-easier.mp4': 'Gardyn_FreshGotEasier_16x9_V5.mp4',
    'gardyn-ctv-2026-grow-something.mp4': 'Gardyn_CTV2026_GrowSomething_15_16x9_V4_VO_Broadcast.mp4',
    'gardyn-grow-it-at-home.mp4': 'Gardyn_GrowItAtHome_16x9_V1_1.mp4',
    'gardyn-if-youve-been-waiting-9x16.mp4': 'Gardyn_IfYouveBeenWaiting_SummerSign_9x16_V1Rev.mp4',
    'commercial-chivas-nike-paisa-boys.mp4': 'Chivas x Nike x Paisa Boys.mp4',
    'commercial-nike-paisa-boys-mexico.mp4': 'Nike x Paisa Boys - Mexico.mp4',
    'publicrec-ugc-dealmaker-pant-interview.mp4': 'DealmakerPant Interview 9x16 V1.mov',
    'whoop-dr-eric-verdin-trailer.mp4': 'WHOOP_Dr. Eric Verdin - Trailer - RND 3 - 9x16.mp4',
    'whoop-refreshed-creator-comp-9x16.mp4': 'WHOOP_RefreshedCreatorComp_9x16_V4.mp4',
    'impactce-intro.mp4': 'impactce-intro-v3_v1 (1080p).mp4',
    'literati-treasured-tales-intro.mp4': 'Literati Treasured Tales Intro.mp4',
    'literati-treasured-tales-store-promo.mp4': 'Literati Treasured Tales Store Promo.mp4',
    'whoop-al-standalone-4x5.mp4': 'WHOOP_ALStandalone_PaidMedia_4-5_FINAL (1).mp4',
    'whoop-refreshed-creator-july-16x9.mp4': 'WHOOP_Refreshed Creator July 16x9 V2Rev TempText.mp4',
    'whoop-psg-giant-screen-ad.mp4': 'WHOOP_PSG Giant Screen Ad 25fps - v10Rev - NoMusic (1).mp4',
    'whoop-behind-the-drivers-seat-lewis.mp4': 'WHOOP_FromBehindTheDriversSeat_LewisCutdown_9x16_V10 (2).mp4',
    'whoop-perfmedia-customizable-4x5.mp4': 'WHOOP_PerfMedia_Customizable_4x5_V4.mp4',
    'whoop-perfmedia-product-render-16x9.mp4': 'WHOOP_PerfMedia_RefreshedProductRender_16x9_V5.mp4',
    'whoop-peloton-partnership-launch-4x5.mp4': 'WHOOP_PelotonPartnershipLaunch_4x5_Final.mp4',
}

NO_CASE_WORK = [NOV9_PM['warmer-real-advice'], NOV9_PM['nike-la-dunk'], NOV8['commercial-chivas-nike-paisa-boys'], NOV8['commercial-nike-paisa-boys-mexico'], NOV8['impactce-intro'],
                NOV9_PM['wolf-and-shepherd-gift-giving'], NOV9_PM['wolf-and-shepherd-styling'], NOV9_PM['tag-scrubs-quality'], NOV9_PM['tag-scrubs-perks']]
# Willie's Remedy's 3D product animations, for the 3D / VFX page
WR_3D = [it for it in WR_CASE['gal'] if it['video'].startswith('wr-3d')]

ADDED_WORK = {
    'whoop': [NOV8[k] for k in ('whoop-behind-the-drivers-seat-lewis', 'whoop-al-standalone-4x5', 'whoop-refreshed-creator-comp-9x16', 'whoop-psg-giant-screen-ad', 'whoop-perfmedia-product-render-16x9',
                                'whoop-peloton-partnership-launch-4x5', 'whoop-perfmedia-customizable-4x5', 'whoop-refreshed-creator-july-16x9', 'whoop-dr-eric-verdin-trailer')],
    'literati': [NOV9_PM['literati-about-book-fairs'], LITERATI_STATICS[0], NOV9_PM['literati-bfa-event-sizzle-9x16'], NOV9_PM['literati-book-fair-sizzle'], LITERATI_STATICS[1],
                 NOV9_PM['literati-storytime-reimagined-1x1'], NOV9_PM['literati-make-reading-fun-again-9x16'], LITERATI_STATICS[2], NOV9_PM['literati-start-your-book-fair'], LITERATI_STATICS[3],
                 NOV9_PM['literati-green-screen-ad-9x16'], NOV9_PM['literati-librarian-testimonials'], LITERATI_STATICS[4], NOV9_PM['literati-custom-book-box-9x16'], LITERATI_STATICS[5],
                 NOV9_PM['literati-ease-of-setup'], LITERATI_STATICS[6], NOV9_PM['literati-favorite-book-series-9x16'], LITERATI_STATICS[7], LITERATI_STATICS[8], NOV9_PM['literati-unboxing-moments-9x16'],
                 LITERATI_STATICS[9], LITERATI_STATICS[10], NOV9_PM['literati-pov-best-day-9x16'], LITERATI_STATICS[11], LITERATI_STATICS[12], NOV9_PM['literati-rejoined-9x16']] + LITERATI_STATICS[13:] + [
                 NOV8['literati-treasured-tales-intro'], NOV8['literati-treasured-tales-store-promo'],
                 _new('literati-f26-promo', 'Fall ’26 store promo · Animation', 1280, 720, 'Motion Graphics')],
    '686': [NOV9_PM['686-features-color-change-2023'], UNWORK_KEEGAN],   # the WNTR goggles colour jump left on November 9, 2026
    'public-rec': _spread([NOV9_PM['publicrec-nobull-built-for-this'], NOV9_PM['publicrec-gamechanger-tv-2024'], PUBLICREC_STILLS[0], NOV9_PM['publicrec-dad-reel-daymakers'],
                   NOV9_PM['publicrec-dealmakers-anniversary-sale-4x5'], PUBLICREC_STILLS[1], NOV9_PM['publicrec-dad-reel-gamechangers'], PUBLICREC_STILLS[2],
                   NOV9_PM['publicrec-aded-pant-drawstring-4x5'], NOV9_PM['publicrec-dad-reel-dealmaker'], PUBLICREC_STILLS[3], PUBLICREC_STILLS[4],
                   NOV9_PM['publicrec-dad-reel-mashup'], PUBLICREC_STILLS[5],
                   NOV8['publicrec-ugc-dealmaker-pant-interview'],
                   _new('publicrec-comfort-rules-anthem', 'Comfort Rules · Anthem', 1280, 720, 'Commercial'),
                   _new('publicrec-ugc-anton-gamechanger', 'Gamechanger Rec pants · UGC with Anton', 720, 1280, 'UGC'),
                   _new('publicrec-ugc-anton-dealmaker', 'Deal Maker 5 pants · UGC with Anton', 720, 1280, 'UGC')],
                  PUBLICREC_NOV10, start=2, every=3),   # the November 10 stills dealt in after Built for This and the TV spot
    'freepower': [_new('freepower-partnership-overview', 'The Cosentino partnership · Interview at KBIS', 1280, 720, 'Profiles'),
                  _new('freepower-your-charger-looks-different', 'Your charger looks different now · Paid social', 720, 1280, 'Paid Social'),
                  _new('freepower-ugc-hana-script-2', 'Hana tries FreePower · UGC', 720, 1280, 'UGC')],
    'gardyn': _spread([GARDYN_NOV9[k] for k in ('gardyn-song-30', 'gardyn-fresh-got-easier', 'gardyn-ctv-2026-grow-something', 'gardyn-grow-it-at-home', 'gardyn-if-youve-been-waiting-9x16')] + [
               _new('gardyn-taste-of-the-holidays', 'Taste of the Holidays · Commercial', 1280, 720, 'Commercial'),
               _new('gardyn-pays-for-itself', 'Gardyn pays for itself · Black Friday ad', 720, 1280, 'Paid Social'),
               _new('gardyn-kelby-script', 'Kelby, the AI gardening assistant · UGC', 720, 1280, 'UGC'),
               _new('gardyn-ugc-hana-new-year', 'New Year with Hana · UGC', 720, 1280, 'UGC'),
               _new('gardyn-give-mom-gardyn', 'Give Mom Gardyn · Mother’s Day UGC', 720, 1280, 'UGC'),
               _new('gardyn-around-the-gardyn', 'Around the Gardyn · 4:5 ad', 1024, 1280, 'Paid Social')],
              GARDYN_NOV10, start=1, every=3),   # the three product stills Mike sent on November 10, 2026
}

# ---- UFL (November 2, 2026): the case Mike wrote. The challenge, the six parts of the solution, the results in numbers, and a quote still
# to come from Vince Pannozzo or Michael Leibowitz. The cover is the game-day still Mike sent.
UFL_WNCD = dict(video='ufl-nobull-what-no-can-do.mp4', poster='ufl/nobull-what-no-can-do.jpg', alt='What No Can Do · NOBULL × UFL broadcast spot', w=1280, h=544, svc='Commercial')
UFL_CASE = dict(
    url='/portfolio/ufl/', title='UFL', heroBg='ufl/cover.jpg', logo='', logoSet=[],
    copy=dict(
        overview=[
            'The United Football League was launching a new season across 8 teams. They needed fresh, high-quality content for every team, every week. It had to work on social feeds, on stadium screens, on the radio and on broadcast TV, and it had to arrive in time for game day.',
            'Birdline became the UFL’s content partner from start to finish.',
        ],
        challenge=['Fresh, high-quality content for every team, every week, across a new 8-team season.',
                   'Work that fits social feeds, stadium screens, radio and broadcast TV.',
                   'Every piece in time for game day.'],
        approach_label='The solution',
        approach=[
            ('A broadcast TV spot with NOBULL', 'In under a month, we produced “What No Can Do,” a broadcast TV spot for the UFL × NOBULL partnership. It features Jordan Ta’amu and Hakeem Butler.'),
            ('Media Day production', 'Our crew captured player interviews and content for the league’s teams in one high-energy shoot at the Arlington, TX stadium.'),
            ('A weekly content engine', 'We turned that footage into a 10-week slate of social videos. Each week was planned around the league’s game schedule.'),
            ('Made for the stadium', 'We produced widescreen edits for in-stadium screens. Fans saw the players on the big screen on game day.'),
            ('Radio that moves fast', 'We created game-day radio spots for teams across the league. Many were turned around in a day, including playoff promos with last-minute changes.'),
            ('A true partnership', 'The UFL kept bringing us more work as the season went on. The radio program grew well beyond its original scope.'),
        ],
        results=['A season of content across four channels, delivered on schedule for all 8 teams, and a relationship that carried on after the final game.'],
        services=['Production', 'Broadcast TV Spot', 'Social Video', 'In-Stadium Video', 'Radio'],
        quotes=[],   # the placeholder testimonial left on November 9, 2026; the Client Stories section stays off until a quote comes
        next=['WHOOP', 'Public Rec', 'Patrol', 'Gardyn'],
        # the radio spots (November 3, 2026): six :30s from Mike's UFL folder, joined into one reel with a second between them; each
        # entry plays its own stretch. The names come from the scripts: four Week 10 home finales, a playoff promo and the "$10 bill" ticket spot.
        radio=dict(file='ufl-radio.mp3', heading='On the |Radio.', sub='Six of the game-day spots: written, voiced and mixed for the teams, most of them turned around in a day.',
                   spots=[dict(name='“$10 Bill”', note='League ticket promo', start=0.0, end=30.03),
                          dict(name='Stallions', note='Week 10 home finale', start=31.03, end=61.06),
                          dict(name='Aviators', note='Week 10 home finale', start=62.06, end=92.09),
                          dict(name='Defenders', note='Week 10 home finale', start=93.09, end=123.12),
                          dict(name='Battlehawks', note='Week 10 home finale', start=124.12, end=154.15),
                          dict(name='Defenders vs. Kings', note='Playoff promo', start=155.15, end=185.18)]),
    ),
    # the work (November 3, 2026): the videos from Mike's UFL folder, transcoded for the web (video/ufl-*.mp4) with a frame of each as its
    # still. svc names the service line the Work page shows under the tile; the vertical episodes fall to Paid Social on their own.
    gal=[
        UFL_WNCD,
        dict(video='ufl-blandino-response.mp4', poster='new/ufl-blandino-response.jpg', alt='Blandino responds · Social video', w=1280, h=720, svc='Paid Social'),
        dict(video='ufl-sizzle-reel.mp4', poster='ufl/sizzle-reel.jpg', alt='UFL Sizzle Reel', w=720, h=1280),
        dict(video='ufl-battlehawks-battle-cry-ep1.mp4', poster='ufl/battlehawks-battle-cry-ep1.jpg', alt='Battle Cry, Ep. 1 · Battlehawks', w=720, h=1280),
        dict(video='ufl-kings-st6g-ep1.mp4', poster='ufl/kings-st6g-ep1.jpg', alt='Smarter Than a 6th Grader, Ep. 1 · Kings, in-stadium', w=1280, h=720, svc='OOH'),
        dict(video='ufl-aviators-call-sign-ep1.mp4', poster='ufl/aviators-call-sign-ep1.jpg', alt='Call Sign, Ep. 1 · Aviators', w=720, h=1280),
        dict(video='ufl-defenders-defend-this-ep2.mp4', poster='ufl/defenders-defend-this-ep2.jpg', alt='Defend This, Ep. 2 · Defenders', w=720, h=1280),
        dict(video='ufl-storm-forecast-ep1.mp4', poster='ufl/storm-forecast-ep1.jpg', alt='Forecast, Ep. 1 · Storm', w=720, h=1280),
        dict(video='ufl-battlehawks-rankings-ep1.mp4', poster='ufl/battlehawks-rankings-ep1.jpg', alt='Rankings, Ep. 1 · Battlehawks', w=720, h=1280),
        NOV9_PM['ufl-defenders-rankings-ep1'],
        dict(video='ufl-battlehawks-rock-and-roll-ep1.mp4', poster='ufl/battlehawks-rock-and-roll-ep1.jpg', alt='Rock & Roll Ricky, Ep. 1 · Battlehawks', w=720, h=1280),
        NOV9_PM['ufl-battlehawks-rock-and-roll-ep2'],
        dict(video='ufl-storm-forecast-ep2.mp4', poster='ufl/storm-forecast-ep2.jpg', alt='Forecast, Ep. 2 · Storm', w=720, h=1280),
    ],
)
