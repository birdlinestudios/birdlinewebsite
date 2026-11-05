# The ROPS™ & ROCS™ page (October 30, 2026): what the two numbers are, why they are measured, what they are worth, and how the
# Birdline App measures them. The copy restates Mike's notes on ROPS and the Public Rec spot (October 30, 2026), the homepage's FAQ
# and calculator, and the Birdline Knowledge Base; every figure is Birdline's own or a case study's.

HERO = dict(
    h1='Know What Your Content |Is Worth.',
    lede='ROAS tells you how media performed. It says nothing about the shoot behind it. ROPS™ and ROCS™ put production on the same page as ad spend, so every campaign shows what the content actually earned.',
)
FORMULAS = [
    ('ROPS', 'Return on Production Spend', 'Tracked revenue', ['Production spend'], 'What the production itself earned, across every campaign that pulled from it, for as long as it keeps working.'),
    ('ROCS', 'Return on Campaign Spend', 'Tracked revenue', ['Production spend', 'Ad spend'], 'The true return on the whole campaign: production and media together, against the revenue they produced.'),
]

# why ROAS is not enough: what each number counts
COMPARE = [
    ('ROAS', 'Revenue ÷ ad spend', [('Ad spend', True), ('Production', False)],
     'How efficiently the media converted. Production isn’t in it, so a $100K shoot and a $5K shoot look exactly the same.'),
    ('ROCS', 'Revenue ÷ production + ad spend', [('Ad spend', True), ('Production', True)],
     'What the campaign cost all in, and what it returned. The number that holds up when finance asks why.'),
    ('ROPS', 'Revenue ÷ production spend', [('Ad spend', False), ('Production', True)],
     'What one day on set earned, counted across every ad, cutdown, and campaign that came from it, this quarter and the next.'),
]
QUESTION = 'For every $1 you put into production over the last 12 months, how much tracked revenue came out?'
QUESTION_SUB = 'Most teams can’t answer that. Not because they’re lazy, but because nothing in their stack is built to track it. Creative budgets get justified by “trust me” or by one campaign’s ROAS, and neither holds up to a serious finance question. ROPS™ does.'

# what tracking it tells you
TELLS = [
    ('target', 'Which shoots paid for themselves', 'And which didn’t, so the next production is scoped on evidence, not instinct.'),
    ('talent', 'Who actually moved revenue', 'Which studios, in-house teams, filmmakers, and creators produced the content that sold.'),
    ('repeat', 'Which budgets compounded', 'The productions that kept earning for years, versus the ones that evaporated in weeks.'),
    ('reviews', 'How to defend the budget', 'A $40K shoot still generating ad variations three years later is an answer finance understands.'),
    ('bolt', 'What to greenlight next', 'Whether to run the next $40K shoot, double it, or rework what’s already in your library.'),
]

# the Public Rec spot, and what happened after it
STORY_STATS = [('$40K', 'production spend'), ('$14.7M', 'TV revenue generated'), ('367.5×', 'ROPS™')]
STORY_LEDE = 'In 2021, our founder directed a nationwide TV spot for Public Rec, in-house. By every measure, the most efficient creative project he had ever worked on, and that doesn’t count the Meta ads cut from the same shoot.'
STORY_THEN = ['Team members left', 'Documentation got scattered across apps', 'New people came in believing an outside agency made it', 'Leadership spent $100K+ on a new agency to recreate the magic', 'The new campaign flopped']
STORY_LESSON = ('None of this happened because the team or leadership were bad. The clarity was gone. The production details, the budget breakdown, the brief, the team that made it, the performance data: none of it lived anywhere the team could quickly analyze, and the receipts to justify producing in-house weren’t there in the moment they were needed.',
                'What if every campaign your team ever produced was a click away? The creative, the logistics, the learnings, all in one system. That question is where the Birdline App started.')

# how the app measures it
MEASURE = [
    ('01', 'Budget the brief', 'Every brief carries a line-item budget: pre-production, production, and post, totaled per brief. That total is the production spend behind ROPS™, entered once, where the work is planned.',
     'app4-brief', 'app4-brief-m', 'A brief in Birdline, Crack Open Summer — Hero Spot Brief, with its text, references and connections.'),
    ('02', 'Connect the ads', 'Connect Meta in Insights and assign each ad to the campaign it came from. The ads supply the revenue and the ad spend; the brief supplies the cost. Nothing is re-keyed.',
     'app6-insights', 'app6-insights-m', 'The Insights page in Birdline with Meta selected: tiles for Campaign Revenue, Total Ad Spend, Production Spend, ROCS and ROPS, above the ad creatives with each ad’s revenue and spend.'),
    ('03', 'Read the return, then brief the next one', 'ROPS™ and ROCS™ sit beside campaign revenue, ad spend, and production spend on every campaign. A Creative Report sums up what worked, and Generate New Brief seeds the next one from its recommendations.',
     'ws-insights', 'ws-insights-m', 'The Insights page of the Birdline App for the Influencer & Whitelisting 2026 campaign: connections, campaign revenue, ad spend, production spend, ROCS and ROPS tiles, and a row of the campaign’s ad creatives.'),
]

# measure your own, by hand
DIY = [
    ('Pick one shoot', 'From the last 18 months.'),
    ('List what came from it', 'Every campaign, ad, or piece of content that pulled from that footage.'),
    ('Add up the tracked revenue', 'Across all of them, not just the launch.'),
    ('Divide by the production cost', 'That’s the shoot’s ROPS™. Do it for three shoots and the pattern that’s been hiding under your campaigns shows up.'),
]

# the numbers so far
NUMBERS = [('175×', 'average ROPS™ across client campaigns'), ('367.5×', 'ROPS™ on a single $40K commercial spot'), ('4×', 'return on $8M of TV spend, production included, for Public Rec'), ('$53M+', 'in returns from under $1M invested in Birdline productions')]
NUMBERS_NOTE = 'Actual figures from Birdline Studios and the Public Rec case study, not forecasts.'

FAQ = [
    ('Is ROPS™ just another name for ROAS?', 'No. ROAS divides revenue by ad spend and leaves production out entirely. ROPS™ divides revenue by what the production cost, and ROCS™ by production and ad spend together. The three answer different questions, and you need all of them to know what a campaign was worth.'),
    ('What counts as tracked revenue?', 'The revenue attributed to the ads you connect to the campaign in the Birdline App. Connect Meta today, with TikTok and YouTube coming soon, and assign each ad to its campaign; the revenue and ad spend flow in from there.'),
    ('Where does the production cost come from?', 'From the line-item budget in the brief: pre-production, production, and post, totaled per brief. Enter it once when the shoot is planned and it carries through to Insights.'),
    ('Do we need the Monthly Partnership to measure it?', 'No. The Birdline App measures ROPS™ and ROCS™ on its own, for any team. Start a free 30-day trial and bring the campaign you’re working on now. The Monthly Partnership adds our creative team to the same workspace.'),
    ('What if a campaign pulls from several shoots?', 'That’s the point of the library. Each brief carries its own budget, so a campaign cut from three productions shows what it earned against what those productions cost, and each production keeps earning across every campaign that uses it.'),
]
