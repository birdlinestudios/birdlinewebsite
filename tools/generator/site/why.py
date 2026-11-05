# The Why Us page (October 30, 2026): the mission, four reasons, the content library as a year at Gardyn (the productions and the\n# campaigns cut from them), ROPS and ROCS with the
# Public Rec numbers behind them, the calculator, and the Birdline App. The copy restates Mike's deck (Your Dollar Matters, the
# Gardyn timeline) and his notes on how Birdline works, unlimited deliverables, the content library, ROPS and the app (October 30,
# 2026); the figures are his and the case studies' own. Pieces are named by their source path in content.json, as on the services pages.

HERO_LEDE = ('Our mission is to get brands the most out of every dollar they put into content: top-tier creatives, unlimited deliverables '
             'from every shoot, and a library that keeps working for years, measured in one workspace.')

# why brands choose Birdline: four reasons, each about thirty words
REASONS = [
    ('birds', 'World-Class Creatives',
     'Vetted filmmakers, content creators, photographers, and designers, even production studios, working as one team. Bring your own freelancers in too, so you have one source of creative support.'),
    ('unlimited', 'Unlimited Deliverables',
     'No per-asset pricing, and no cap on deliverables or revisions. Like an in-house hire, we make whatever your goals need, whether that’s 10 assets or 40+ a month.'),
    ('slack', 'Direct Communication',
     'Everything runs through Slack: we tag the right Bird, and they deliver straight to you. Biweekly calls cover what’s working, what’s not, and what to plan next.'),
    ('app', 'The Birdline App',
     'Every brief, deliverable, and result lives in one workspace, so your team can see what was made, what it cost, and what it earned, and build from it.'),
]
REASONS_LINE = 'A content team that works like an employee and scales like an agency.'

# the content library, a year at Gardyn. Three productions, each adding a set of three pieces (a commercial, a UGC-style piece, a
# still) to the library, and five campaigns cut from the sets already in it, with no new shoot. (key, name, month index from June,
# the pieces) and (key, name, month index, the sets it draws on, the piece shown); a month index past 11 is the following year
LIBRARY_INTRO = 'A year at Gardyn: three days on set, endless campaigns cut from them, and production content that will provide value for years.'
PRODUCTIONS = [
    ('summer', 'Summer', 0, ['2024/05/Gardyn-Summer.jpg', '2024/05/Gardyn-Unboxing-1.jpg', '2024/05/Gardyn_7_29_2025_Kitchen_77886.jpeg']),
    ('winter', 'Winter', 5, ['2024/05/thumb-32.jpg', '2024/05/Gardyn-Summer-Delight.jpg', '2024/05/Gardyn_7_29_2025_26229.jpeg']),
    ('spring', 'Spring', 10, ['2024/05/Gardyn-Growing-Symphony-3.jpg', '2024/05/Gardyn-New-Year-New-You-1.jpg', '2024/05/Gardyn-14May2024-GrantPuckett43284-RetouchV1.jpeg']),
]
CAMPAIGNS = [
    ('labor-day', 'Labor Day Sale', 3, ['summer'], '2024/05/thumb-34.jpg'),
    ('ctv', 'CTV Commercial', 6, ['summer', 'winter'], '2024/05/thumb-15-2.jpg'),
    ('spring-fresh', 'Spring Fresh', 10, ['summer', 'spring'], '2024/05/thumb-3-2-e1720505206447.jpg'),
    ('mothers', 'Mother’s Day', 11, ['summer', 'winter', 'spring'], '2024/05/Gardyn-Fresh-247-e1715122740848.jpg'),
    ('holiday-greens', 'Holiday Greens', 17, ['winter', 'spring'], '2024/05/thumb-20-1.jpg'),
]
MONTHS = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
LIBRARY_STATS = [('3', 'days on set in a year'), ('1,000+', 'assets added to the content library'), ('Ongoing', 'return on production spend')]
LIBRARY_STATEMENT = ('Treat creative as an appreciating asset,', 'and you’ll build a library that keeps working for years.')

# ROPS and ROCS: the question, the two definitions, and the Public Rec numbers that answer it
ROPS_INTRO = 'For every $1 you put into production, how much tracked revenue came out? Most teams can’t answer that, because nothing in their stack is built to track it. The Birdline App does, on every campaign.'
METRICS = [
    ('ROPS', 'Return on Production Spend', 'Tracked revenue ÷ production cost. Which shoots paid for themselves.'),
    ('ROCS', 'Return on Campaign Spend', 'Tracked revenue ÷ production and ad spend. The true cost of the campaign.'),
]
# the Public Rec numbers: one spot for ROPS, the TV program for ROCS
PROOF = [
    ('ROPS', 'One nationwide TV spot', [('$40K', 'production'), ('$14.7M', 'TV revenue'), ('367.5×', 'ROPS')]),
    ('ROCS', 'Seven national TV commercials', [('$8M', 'TV spend, all in'), ('$32M', 'TV revenue'), ('4×', 'ROCS')]),
]
PROOF_NOTE = 'Public Rec, 2021 to 2025. Meta ads from the same shoots not counted.'

# the Birdline App: an archive, not a graveyard
APP_SUB = 'The work is there. The team just never goes back to it. The Birdline App turns every campaign into a living library your next one builds from.'
APP_CHAIN = ['What you planned: the brief, the shot list, and the budget', 'What you made: every deliverable, tied to its brief', 'What it cost: production spend, line by line', 'What performed: ad results connected to the campaign', 'What to repeat, evolve, or never do again']
APP_TAIL = 'All connected. All searchable. All compounding.'
