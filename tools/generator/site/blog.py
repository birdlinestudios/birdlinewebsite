"""The Birdline blog (November 9, 2026): an index at /blog and a page per post at /blog/<slug>. Rendered by blog_page() and
post_page() in build_site.py. Each post is Mike's thinking as the site already states it (ROPS and ROCS, the content library,
briefs, unlimited deliverables, the Birdline App), written out at article length; a body is a list of blocks:
('p', text), ('h2', text), ('ul', [items]), ('ol', [items]), ('quote', text), ('table', (headers, rows)), ('cta', (label, href)),
('sources', ([dict(text, href=None)], note)), ('calc', 'team') for the team calculator (teamcalc.py), ('figure', (screen, alt, caption))
for a screen of the Birdline App (img/ws-<screen>.webp and its phone capture), ('details', (title, hint, [blocks])) for a part that
stays folded until the reader opens it. A post's `meta` is its search description; without one the dek serves. `takeaways` are
optional: a post short enough to be its own summary goes without the card."""
import teamcalc as TC

# the team calculator's opening figures, for the post that carries it: the prose quotes what the calculator shows as it opens
_TC = TC.figures()
_TCV, _TCM = _TC['v'], _TC['m']
_TCC = TC.CONFIG
_solo = TC.start_state(); _solo.update(size=0, ads=20, shoots=0, design=0)     # one senior editor, nothing else
_SOLO = TC.model(_solo)
_solo_mid = TC.start_state(); _solo_mid.update(size=0, ads=20, shoots=0, design=0); _solo_mid['salary']['editor'] = 75420     # the same seat at the BLS median
_SOLO_MID = TC.model(_solo_mid)
_solo_low = TC.start_state(); _solo_low.update(size=0, ads=20, shoots=0, design=0); _solo_low['salary']['editor'] = 52720     # and at the 25th percentile
_SOLO_LOW = TC.model(_solo_low)
# what the post says about one editor: about $40,000 over the package at senior pay, within $3,000 at the median, under it for a junior
assert _SOLO['heads'] == 1 and 39500 <= _SOLO['in_total'] - _SOLO['bl_total'] < 40500, _SOLO
assert 0 < _SOLO_MID['in_total'] - _SOLO_MID['bl_total'] < 3000, _SOLO_MID
assert _SOLO_LOW['in_total'] < _SOLO_LOW['bl_total'], _SOLO_LOW
# the brand the post describes is the one the calculator opens on: 40 ads a month, half video and half design, four productions a year,
# one of each role; and "That is $X less" is the calculator's own headline figure
assert (_TCC['start']['ads'], _TCC['start']['design'], _TCC['start']['shoots']) == (40, 50, 4), _TCC['start']
assert _TCM['heads'] == 3 and _TCM['n'] == dict(editor=1, designer=1, producer=1), _TCM
assert _TCM['team'] - _TCM['partner'] == _TCM['in_total'] - _TCM['bl_total'] and _TCV['hero'] == TC.money(_TCM['team'] - _TCM['partner']), _TCV['hero']
assert dict((k, v) for k, _n, v in _TCC['roles']) == dict(editor=105310, designer=110500, producer=90360)     # the salaries the notes spell out
assert [k for k, _n, _v in _TCC['roles']] == ['editor', 'designer', 'producer'], _TCC['roles']     # creative strategy is part of the producer's role, not a hire of its own
assert (_TCC['ssd'], _TCC['backup'], _TCC['seat'], _TCC['tools'], _TCC['load'], _TCC['shoot']) == (1900, 280, 2500, 300, 25, 20000)
assert (_TCC['fill'], _TCC['onboard']) == (39, 7) and _TCC['cap'] == dict(editor=20, designer=50)
assert _TCC['price'] == dict(editor=8000, designer=6000)
# the figures the post's prose quotes, as the calculator shows them when it opens
_F = dict(salaries=TC.money(_TCM['salaries']), team=TC.money(_TCM['team']), fill=_TCC['fill'], partner=TC.money(_TCM['partner']),
          monthly=TC.money(_TCM['monthly']), less=TC.money(_TCM['team'] - _TCM['partner']))

HERO = dict(
    eyebrow='The Birdline blog',
    h1='Notes From |the Production Line.',
    lede='How we think about creative that keeps paying off: production, performance, and the workflow in between. Written by the people who make the work.',
)

AUTHOR = dict(name='Mike Pagan', role='Founder and CEO, Birdline', face='mike',
              bio='Mike founded Birdline because too much content was going to waste and brands did not know what their creative was worth. He writes about production, performance and the workflow between them.')

CATEGORIES = ['Performance', 'Production', 'Workflow', 'Strategy']

WORK = dict(eyebrow='In practice', h2='The Ideas, |in the Work.', sub='The thinking above comes from the partnerships below: libraries that keep paying off, briefs that land, and results traced back to the creative.',
            slugs=['gardyn', 'public-rec', 'whoop', 'ufl'])

CLOSE = dict(heading='Put the Ideas to Work.', sub='Tell us what is in your pipeline and where your team could use another set of hands.', photo='2024/05/Gardyn_7_29_2025_27427.jpeg')

POSTS = [
    dict(   # November 15, 2026: the FAQ "Why wouldn't I just hire a full-time editor?", answered with the team calculator.
            # November 17, 2026: cut to the argument (Mike: the same point, simpler, as concise as possible). About 1,900 words became
            # about 300: who it takes, what they cost on payroll, the same team with Birdline, the calculator, what happens when demand
            # moves, and when a hire wins. Everything behind the figures sits folded under "How we got the numbers".
            # What the post still has to say, each from Mike on November 15, 2026: every Birdline editor and designer/animator is senior
            # or expert level, so the hire it compares against is senior; the drives count, the SSDs editors cut from above all; the
            # Birdline App is included and saves time and money (less friction, faster to execution and productions, more and newer
            # content: the calculator's own card says how); a creative strategist for creative marketing is always included and is part
            # of the producer / project manager's role; output per person is an average; and Birdline is not out to replace the people
            # who own the brand.
            # Salaries are BLS figures for May 2025: the 75th percentile for the two makers, the median for the producer. The load on a
            # salary is from BLS's June 2026 employer costs, time to fill is SHRM's 2026 benchmark, the drive prices are B&H's that
            # month, the tools are Asana's and Frame.io's list prices; the staffing rules, the $2,500 seat and the drive counts are
            # Birdline's working assumptions and say so.
        slug='in-house-content-team-cost-calculator',
        title='Why Wouldn’t I Just Hire a Full-Time Team?',
        dek='You could. Here is the math.',
        meta='What an in-house content team costs in salaries, benefits, tools and time, with a calculator that sets it beside a Birdline partnership and the Birdline App.',
        category='Strategy', date='2026-11-15', read=2,
        cover='new/production-set.jpg',
        cover_alt='A Birdline shoot: a camera on a tripod in the foreground, two people in conversation on set, and a producer watching the monitor.',
        body=[
            ('p', 'Sometimes you should. If the work is one skill, forty hours a week, for years, hire the person.'),
            ('p', 'But ads are not one skill. Shipping them every week takes a team.'),
            ('ul', ['A senior video editor.',
                    'A senior designer who animates.',
                    'A producer who runs the work and the creative strategy.']),
            ('p', 'Senior, because that is who you get with us.'),
            ('p', 'Take a brand shipping 40 ads a month, half video and half design. That takes one of each.'),
            ('h2', 'On payroll'),
            ('ul', ['Three salaries. %(salaries)s a year, before anything else.' % _F,
                    'The rest. Benefits, payroll taxes, software, tools and drives bring it to %(team)s.' % _F,
                    'The search. %(fill)d days to fill each seat.' % _F]),
            ('h2', 'With Birdline'),
            ('ul', ['The same team. A dedicated senior editor, a dedicated senior designer/animator and a project manager who is also your creative strategist.',
                    '%(partner)s a year. Both packages, from %(monthly)s a month. That is %(less)s less.' % _F,
                    'No payroll, no search. The Birdline App is included, and work starts within a week.']),
            ('figure', ('tasks', 'The Deliverables page of the Birdline App: filters by assignee, status, due date and campaign beside a table of deliverables with campaign and brief, assignee, name, due date, asset link and status.',
                        'The Birdline App: every request, its owner and its status in one place. Sample data.')),
            ('h2', 'Run your numbers'),
            ('p', 'The calculator opens on that brand, with four productions a year. Productions cost the same either way. Every number is yours to change.'),
            ('calc', 'team'),
            ('h2', 'When demand moves'),
            ('p', 'Need more? We add a dedicated editor or designer/animator. Need less? Scale back. Every partnership is rolling, with 60 days’ notice to cancel.'),
            ('p', 'A salary stays whether the volume does or not.'),
            ('quote', 'A content team that works like an employee and scales like an agency.'),
            ('h2', 'When a hire wins'),
            ('p', 'If the calculator says a hire wins, hire. A mid-level editor costs about what our Video Editing package does. A junior editor costs less. The gap opens at senior level: about $40,000 a year on one seat, and more with every skill you add.'),
            ('p', 'And keep the people who own your brand. We are not there to replace them. We are the production capacity around them.'),
            ('cta', ('See the packages', '{{ROOT}}packages.html')),
            ('details', ('How we got the numbers', 'Salaries, costs, staffing rules and sources', [
                ('ul', ['Salaries. Bureau of Labor Statistics, May 2025, U.S. Senior pay, the 75th percentile, for the editor ($105,310) and the designer/animator ($110,500, the midpoint of graphic designers and animators). The median for the producer ($90,360).',
                        'Benefits and payroll taxes. 25% of salary, from BLS employer costs for June 2026.',
                        'Software and equipment. $2,500 a person a year: Adobe Creative Cloud, a workstation and stock.',
                        'Workflow tools. $300 a person a year for a project tracker and a review tool, at Asana and Frame.io list prices.',
                        'Drives. Two 4TB editing SSDs for each editor a year, $1,900, and one 8TB backup drive for each production, $280. B&H prices.',
                        'Hiring. 39 days to fill a seat: SHRM’s 2026 median for nonexecutive roles.',
                        'Output. On average, one editor ships 20 video ads a month and one designer ships 50 statics or motion pieces. With unlimited deliverables, that moves with your edit requests.',
                        'The producer. One joins at two makers in a company past ten people, three makers anywhere, or six productions a year. Then one for every eight makers, and one more at a production a month.',
                        'Creative strategy. At Birdline, your project manager is also your creative strategist for creative marketing. It is always included, so payroll counts one hire for both jobs.',
                        'Birdline. Starting prices: Video Editing at $8,000 a month and Design & Animation at $6,000 a month, one package for each dedicated creative. The SSDs we edit from are ours.',
                        'Productions. The same budget on both sides: $20,000 each unless you change it.',
                        'One editor. At the median salary, $75,420, a single seat costs within $3,000 a year of the Video Editing package.',
                        'Left out. Recruiting, bonuses, raises, turnover, management time and office space. Each one adds to the payroll side.']),
                ('sources', ([
                    dict(text='U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics, May 2025, as published by CareerOneStop (U.S. Department of Labor): film and video editors, median and 75th percentile.', href='https://www.careeronestop.org/Toolkit/Careers/Occupations/occupation-profile.aspx?keyword=Film+and+Video+Editors&location=US&onetcode=27-4032.00'),
                    dict(text='BLS wages, May 2025, on CareerOneStop: graphic designers, 75th percentile.', href='https://www.careeronestop.org/Toolkit/Careers/Occupations/occupation-profile.aspx?keyword=Graphic+Designers&location=US&onetcode=27-1024.00'),
                    dict(text='BLS wages, May 2025, on CareerOneStop: special effects artists and animators, 75th percentile.', href='https://www.careeronestop.org/Toolkit/Careers/Occupations/occupation-profile.aspx?keyword=Special+Effects+Artists+and+Animators&location=US&onetcode=27-1014.00'),
                    dict(text='BLS, Occupational Outlook Handbook: producers and directors, median pay, May 2025.', href='https://www.bls.gov/ooh/entertainment-and-sports/producers-and-directors.htm'),
                    dict(text='BLS, Employer Costs for Employee Compensation, June 2026 (released September 9, 2026): full-time private industry workers, Table 5.', href='https://www.bls.gov/news.release/ecec.htm'),
                    dict(text='SHRM, 2026 Recruiting Executives Benchmarking: median time-to-fill for nonexecutive positions.', href='https://www.shrm.org/topics-tools/research/recruiting-benchmarking'),
                    dict(text='Adobe: Creative Cloud Pro for teams, U.S. price per license.', href='https://helpx.adobe.com/account/individual/subscriptions-and-plans/plan-types-and-eligibility/changes-to-teams-plan.html'),
                    dict(text='B&H Photo: Samsung 4TB T9 Portable SSD, $936.98.', href='https://www.bhphotovideo.com/c/product/1787602-REG/samsung_mu_pg4t0b_am_4tb_t9_portable_ssd.html'),
                    dict(text='B&H Photo: Seagate 8TB Expansion Desktop Hard Drive, $279.99.', href='https://www.bhphotovideo.com/c/buy/expansion-desktop/ci/41480'),
                    dict(text='Asana: Starter plan, price per user, billed annually.', href='https://asana.com/pricing'),
                    dict(text='Frame.io: Pro plan, price per member.', href='https://frame.io/pricing'),
                ], 'Figures as of November 2026. The calculator gives an estimate, not a quote.')),
            ])),
        ],
    ),
    dict(
        slug='roas-production-spend-rops-rocs',
        title='ROAS Can’t Tell a $5K Shoot From a $100K One.',
        dek='Media gets measured to the dollar. The production behind it gets a line on an invoice. Two more numbers put them on the same page.',
        meta='ROAS measures the media and ignores the shoot. How ROCS and ROPS put production spend back in the math, with a worked example and Birdline’s own figures.',
        category='Performance', date='2026-11-09', read=5,
        cover='2025/09/PublicRec-DTLA-DD-33.jpeg', focal='50% 18%',
        cover_alt='A frame from Public Rec’s All Day Every Day TV spot: a man in Public Rec pants crossing a downtown Los Angeles street.',
        takeaways=['ROAS divides revenue by ad spend. It measures the media and nothing else.',
                   'The creative is the biggest variable in a campaign, and the one cost ROAS leaves out.',
                   'ROCS and ROPS put production in the math. You can calculate both today.'],
        body=[
            ('p', 'Two campaigns finish the quarter with the same ROAS: 5×. One came from a $5K shoot. The other came from a $100K shoot.'),
            ('p', 'On the performance report, they are twins. ROAS cannot tell them apart, because production was never in the formula.'),
            ('h2', 'What ROAS was built to measure'),
            ('p', 'Return on ad spend is revenue divided by ad spend. It tells a media buyer how efficiently a dollar of media converted, and it does that job well.'),
            ('p', 'It was never meant to judge the whole investment. Production got left out for a boring reason. Media arrives with a dashboard. Production arrives as an invoice, usually from a different budget, months before the ad runs.'),
            ('p', 'So the two costs of a campaign live in two places. One is measured to the dollar, every day, by everyone. The other is approved once and rarely looked at again. When budgets tighten, and they always do, the line with a return next to it survives and the line without one gets cut. Production is the line without one.'),
            ('h2', 'The biggest variable has no number'),
            ('p', 'The cost ROAS ignores is the one doing most of the work.'),
            ('p', 'Think about what a media buyer still controls. The platforms have taken over most of the targeting: you hand them a budget and a conversion goal, and the system decides who sees the ad, where, and at what bid. What is left for a person to decide is the creative. And the creative is the only part of the campaign the customer ever sees.'),
            ('p', 'You can watch it in any ad account. Hold the budget and the audience steady, swap the ad, and the numbers move. Hold the ad steady and tweak the audience, and they barely do. Every team that has run a creative test knows which lever is the heavy one.'),
            ('p', 'Yet the heavy lever is the one the industry’s favorite return metric leaves out. Media gets credit for every dollar the campaign makes. The creative that earned the click sits in the denominator of nothing.'),
            ('h2', 'Three numbers, three questions'),
            ('table', (['Metric', 'Formula', 'The question it answers'], [
                ['ROAS', 'Tracked revenue ÷ ad spend', 'How efficiently did the media convert?'],
                ['ROCS™ (Return on Campaign Spend)', 'Tracked revenue ÷ (production + ad spend)', 'What did the campaign return, all in?'],
                ['ROPS™ (Return on Production Spend)', 'Tracked revenue ÷ production spend', 'What did the shoot earn, across everything cut from it?'],
            ])),
            ('p', 'Now run the twins through all three.'),
            ('table', (['', 'Campaign A', 'Campaign B'], [
                ['Production spend', '$5,000', '$100,000'],
                ['Ad spend', '$40,000', '$40,000'],
                ['Tracked revenue', '$200,000', '$200,000'],
                ['ROAS', '5.0×', '5.0×'],
                ['ROCS', '4.44×', '1.43×'],
                ['ROPS', '40.0×', '2.0×'],
            ])),
            ('p', 'Same ROAS. Very different quarter. Campaign A returned $4.44 for every dollar the company put in. Campaign B returned $1.43.'),
            ('p', 'Campaign B is not a failure yet. If its footage feeds four more campaigns, its ROPS climbs with each one. You would want to know that was the plan before the invoice landed.'),
            ('h2', 'What it looks like with real money'),
            ('p', 'These are Birdline figures from our work with Public Rec between 2021 and 2025.'),
            ('p', 'One nationwide TV spot cost $40K to produce and returned $14.7M in tracked TV revenue. That is a ROPS of 367.5×. The Meta ads cut from the same shoots are not counted.'),
            ('p', 'Across seven national TV commercials, TV spend came to $8M with production included. Tracked TV revenue was $32M. That is a ROCS of 4×.'),
            ('p', 'Both numbers describe the same partnership.'),
            ('quote', 'One number makes a production look like a miracle. The other is the number you take to the board.'),
            ('h2', 'Where ROPS can fool you'),
            ('p', 'A ROPS in the hundreds looks too good because, in a sense, it is. Media helped earn that revenue, and ROPS hands production all the credit. That is why it never travels alone.'),
            ('p', 'Three more cautions:'),
            ('ul', ['It is attribution, not incrementality. Tracked revenue is only as good as the tracking behind it.',
                    'It grows with time. A shoot keeps earning as new cuts launch, so compare productions over the same window.',
                    'It rewards small denominators. A cheap shoot with one lucky ad can outscore the library that carried your year.']),
            ('p', 'Use ROAS to steer the media, ROCS to report the campaign, and ROPS to decide what to shoot next.'),
            ('h2', 'Start here'),
            ('p', 'You can do this today with a calculator and last year’s campaigns.'),
            ('ol', ['Pick one shoot from the last 18 months.',
                    'List every campaign, ad and piece of content that pulled from its footage.',
                    'Add up the tracked revenue across all of them, not only the launch.',
                    'Divide by what the production cost.']),
            ('p', 'Do it for three shoots. The pattern that has been hiding under your campaigns shows up.'),
            ('h2', 'Where Birdline fits'),
            ('p', 'In the Birdline App, the brief carries the production budget and your connected ad accounts supply the revenue. ROPS and ROCS sit on every campaign, and nothing is re-keyed into a spreadsheet.'),
            ('cta', ('Try the calculator', '{{ROOT}}rops.html#calculator')),
            ('sources', ([
                dict(text='Birdline figures: the Public Rec case study. Public Rec, 2021 to 2025.', href='{{ROOT}}case-studies/public-rec.html'),
                dict(text='How we measure it: Why Birdline, and the ROPS and ROCS page.', href='{{ROOT}}rops.html'),
            ], 'Figures as of November 2026.')),
        ],
    ),
    dict(
        slug='what-is-return-on-production-spend',
        title='What Is Return on Production Spend?',
        dek='ROAS tells you what your media did. ROPS tells you what your creative did. Here is how we calculate it, and why it changes what you shoot next.',
        category='Performance', date='2026-11-04', read=6,
        cover='2024/05/Gardyn-14May2024-GrantPuckett43284-RetouchV1.jpeg',
        cover_alt='A Gardyn tower in a bright kitchen, from the campaign stills.',
        takeaways=['ROPS = tracked revenue from the creative ÷ what it cost to make.', 'It puts production on the same scoreboard as media.', 'A library of footage makes ROPS climb with every new cut.'],
        body=[
            ('p', 'Most brands can tell you their ROAS to the decimal. Ask what the creative behind those ads returned and the room goes quiet. The production invoice was paid months ago, the footage is on a drive somewhere, and nobody has connected the two numbers.'),
            ('p', 'Return on Production Spend, or ROPS, is the number that connects them. It asks one question: for every dollar you spent making the creative, how much tracked revenue did that creative generate?'),
            ('h2', 'The formula'),
            ('p', 'ROPS is tracked revenue attributed to a piece of creative, divided by the cost of producing it. If a shoot cost $20,000 and the ads cut from it drove $400,000 in tracked revenue, the ROPS is 20. Spend a dollar making it, get twenty back.'),
            ('p', 'Two things make the number honest. First, the revenue has to be attributed at the ad level, which is why the Birdline App connects to the ad platform rather than asking anyone to type in totals. Second, the production cost has to include everything: pre-production, the shoot day, post, talent, the lot. A ROPS built on half the costs is a flattering guess.'),
            ('h2', 'Why ROAS is not enough'),
            ('p', 'ROAS measures the efficiency of media spend. Put a dollar in Meta, get three out. It is a good number, and it is blind to the thing that moved it. Two campaigns with the same media budget can return wildly different ROAS, and the difference is almost always the creative.'),
            ('p', 'Because ROAS ignores production, it quietly pushes teams toward cheap creative. The spreadsheet rewards the $500 edit and the $20,000 shoot equally, as long as the media math works. ROPS fixes the scoreboard. A shoot that produces six months of winning ads looks exactly as good as it is.'),
            ('quote', 'Production is not a cost line above the campaign. It is the campaign, measured.'),
            ('h2', 'What a good ROPS looks like'),
            ('p', 'There is no universal benchmark, and anyone who gives you one is selling something. What we watch is the trend. A production that is cut once and shelved has a ROPS that stops moving the day the campaign ends. A production that feeds a library keeps earning: a new hook here, a seasonal cutdown there, a product shot reused in a static. The numerator keeps growing while the denominator stays put.'),
            ('p', 'That is the pattern behind the partnerships that run for years. Public Rec has been cutting from a growing library since 2021. Gardyn’s hero shoot became a TV spot, a summer cut, a UGC-style series and a dozen statics. Their ROPS is not a snapshot; it is a curve, and it bends up.'),
            ('h2', 'How to start measuring it'),
            ('ul', ['Record what each production actually cost, all in, and tie it to a campaign.', 'Tag the ads cut from that production so revenue can be attributed back to it.', 'Review the number on a cadence, not once. Monthly is enough to steer by.', 'Let it change decisions: recut what is working, reshoot what is not, and stop paying for creative nobody can measure.']),
            ('p', 'If your team does this by hand, it works; it is just slow. The Birdline App does it as part of the workflow: every deliverable is tied to its brief, every brief to a campaign, and the performance data flows back to the creative that earned it. The next strategy call starts with the number instead of a hunch.'),
        ],
    ),
    dict(
        slug='shoot-for-the-library-not-just-the-launch',
        title='Shoot for the Library, Not Just the Launch',
        dek='One shoot day should feed campaigns for years. The difference is what you capture when the hero shot is already in the can.',
        category='Production', date='2026-10-21', read=5,
        cover='2024/05/Gardyn_7_29_2025_Kitchen_77909.jpeg',
        cover_alt='A couple cooking together at a kitchen island beside a Gardyn tower.',
        takeaways=['Plan the shot list for the next six months, not the next launch.', 'Alternate hooks, clean takes and product details are cheap on the day and priceless later.', 'Footage you can find is footage you can reuse.'],
        body=[
            ('p', 'Here is the most expensive habit in content marketing: shooting for one launch. A brand books a day, captures exactly what the campaign brief asks for, cuts the hero spot, and moves on. Six weeks later the next campaign needs new creative, and the whole machine starts again from zero.'),
            ('p', 'The footage from that first day is almost always more valuable than the one spot it produced. The trick is to shoot like you know that.'),
            ('h2', 'What “for the library” means on set'),
            ('p', 'When our Birds plan a shoot, the shot list has two layers. The first is the campaign: the hero shots the brief needs, in the formats it needs them. The second is the library: everything we can capture around those shots while the lights are up and the talent is there.'),
            ('ul', ['Alternate hooks. The first three seconds decide whether anyone watches. We shoot several openings for every concept.', 'Clean takes. A product shot with no hands, no talent and no text leaves room for the next campaign’s message.', 'Details and textures. Hands on the product, the unboxing, the thing in use. These are the cutaways every future edit will need.', 'Framing for every placement. A 16:9 spot and a 9:16 ad are different shots, not a crop. We get both while we are there.']),
            ('p', 'None of this adds a day. Most of it adds minutes. What it adds later is months of edits that never required another production.'),
            ('h2', 'Where the footage goes matters as much as what you shoot'),
            ('p', 'A library you cannot search is a hard drive. Active footage at Birdline lives on organized drives with consistent folder structures and clear file names, so an editor can pull a shot from two years ago and cut it alongside last month’s. In the Birdline App, the approved creative stays connected to its campaign and brief, so when a new request comes in, the first move is to look at what already exists.'),
            ('quote', 'For Gardyn, one photo from an earlier campaign became the first ten seconds of a new ad.'),
            ('h2', 'The payoff shows up in the numbers'),
            ('p', 'Shooting for the library is what makes Return on Production Spend climb instead of plateau. The production cost is paid once. Every new cut from the footage adds revenue to the same investment. That is how a $20,000 shoot day ends up behind a year of paid social, a TV spot and a holiday campaign, and why the brands we work with longest shoot less often than you would think.'),
            ('p', 'Before your next production, ask one question of the shot list: what will we wish we had captured six months from now? Then capture it.'),
        ],
    ),
    dict(
        slug='how-to-brief-a-creative-team',
        title='How to Brief a Creative Team So the First Cut Lands',
        dek='A good brief is not long. It answers four questions and leaves the rest to the people making the work.',
        category='Workflow', date='2026-10-07', read=5,
        cover='new/gardyn-7-29-2025-27361.jpg',
        cover_alt='A Birdline crew around a kitchen table on the Gardyn shoot.',
        takeaways=['Goal, deliverables, references, timeline. Everything else is detail.', 'Send the brief where the work happens, not in a separate tool.', 'Timecoded notes beat paragraphs of feedback every time.'],
        body=[
            ('p', 'The fastest way to get a great first cut is a brief that tells the team what success looks like and then gets out of the way. The slowest way is a twelve-page document that describes the edit frame by frame and still forgets to say what the ad is for.'),
            ('h2', 'The four questions'),
            ('p', 'Every brief we take on at Birdline answers the same four things before anyone opens a timeline.'),
            ('ul', ['The goal. What should this piece make someone do, feel or understand? “Drive trial sign-ups from cold traffic” is a goal. “A video about the product” is not.', 'The deliverables. Formats, lengths and placements. Six 9:16 cuts and two 16:9 is a brief; “some social stuff” is a conversation.', 'References. Two or three examples of the tone, pace or structure you have in mind, including your own past winners. Say what you like about each.', 'The timeline. When it needs to launch, and anything that has to happen first, like a product arriving or a sale going live.']),
            ('p', 'If you already have this in a doc or a deck, send the link. We do not need it re-typed into a form.'),
            ('h2', 'Where the brief lives'),
            ('p', 'A brief in someone’s inbox is a brief that gets lost. Ours start in the Birdline App or in the shared Slack channel, and either way they end up in the app, tied to the campaign they belong to. Each project gets its own Slack thread linked to the brief, so the conversation about the work and the record of the work stay in the same place.'),
            ('quote', 'The best briefs are short because the goal is clear. The worst are long because it is not.'),
            ('h2', 'How to give feedback that moves the cut forward'),
            ('p', 'Drafts go to Frame.io, where you can leave a comment on the exact frame. “Hold the product shot a beat longer at 0:12” takes ten seconds to write and ten seconds to act on. “The middle feels slow” starts a round of guessing.'),
            ('ul', ['Comment on the frame, not in an email.', 'Say what the change is for, not just what to change. “Tighten the intro so the offer lands before the swipe” tells the editor what good looks like.', 'Collect the team’s notes before sending. Three people’s uncoordinated feedback is three different edits.', 'Approve clearly. A thumbs-up in Frame.io is how the file moves from draft to final and into the library.']),
            ('h2', 'What happens after approval'),
            ('p', 'Once you approve, the final files go into the Birdline App and we let you know in Slack. Your team can see what is ready to launch and, when the next campaign comes around, find it again without asking anyone where it went. That is the quiet half of a good brief: six months later, the work it produced is still easy to find.'),
        ],
    ),
    dict(
        slug='the-content-snowball',
        title='The Content Snowball: Why Your Best Ads Come From Footage You Already Have',
        dek='Shoot once, cut many, learn from every cut. The framework behind partnerships that get cheaper and better every month.',
        category='Strategy', date='2026-09-23', read=6,
        cover='2024/05/Gardyn_7_29_2025_26229.jpeg',
        cover_alt='A still from the Gardyn shoot: fresh greens on the kitchen counter.',
        takeaways=['Every production feeds the library; every edit tests a hook; every result informs the next shoot.', 'The cost per winning ad falls as the library grows.', 'The snowball only rolls if the footage and the data live in the same place.'],
        body=[
            ('p', 'Most content calendars are a treadmill. Every campaign starts from a blank page, a new shoot and a new invoice, and when it ends the creative is retired whether or not it worked. We built Birdline around a different shape. We call it the Content Snowball, and it is the reason our longest partnerships are also our most efficient.'),
            ('h2', 'How the snowball rolls'),
            ('p', 'It has three turns, and they repeat.'),
            ('ul', ['Produce for the library. A shoot captures the campaign and everything around it: alternate hooks, clean takes, details, every format. The footage goes into an organized library, not a project folder.', 'Cut, test, learn. Edits go out as ads. Each one tests a hook, a message or a format. The performance data comes back to the creative that earned it, not to a spreadsheet nobody opens.', 'Let the results steer. Winning hooks get recut into new placements. Losing ones get retired early. The next shoot is planned around what the library is missing, not around a blank page.']),
            ('p', 'Each turn makes the next one cheaper. The second campaign from a library needs no shoot. The third knows which hooks work before anyone writes a script. By the time a shoot is scheduled again, it is a precise addition to a body of work, not a restart.'),
            ('h2', 'What it looks like in practice'),
            ('p', 'Gardyn is the clearest example. A hero production in the summer became a TV spot, a summer cut, a UGC-style series and a run of statics. When performance showed which messages landed, we cut more of those, and the next shoot filled the gaps the data had pointed to. Forty-five million organic views later, the brand is spending less per winning ad than it did in year one.'),
            ('quote', 'A treadmill costs the same every month. A snowball gets heavier for free.'),
            ('h2', 'What stops the snowball'),
            ('p', 'Three things, in our experience. Footage nobody can find, so every edit starts from a new shoot. Performance data that never reaches the creative team, so nobody knows what to recut. And a project-based model that ends the engagement the moment the campaign ships, before any of the learning can be used.'),
            ('p', 'Our monthly partnership exists to remove all three. A dedicated team keeps cutting from the library. The Birdline App ties every deliverable to its brief and its results. And unlimited deliverables mean the question is never “can we afford another cut?” but “what should we cut next?”'),
            ('h2', 'Start where you are'),
            ('p', 'You do not need a new shoot to start rolling. Pull together the footage you already own, organize it so an editor can find it, and connect your ad results to the creative that produced them. Then cut three new ads from what is there. Most brands are sitting on a snowball; it just has not been pushed.'),
        ],
    ),
    dict(
        slug='unlimited-deliverables-explained',
        title='Unlimited Deliverables, Explained',
        dek='What “unlimited” means in a Birdline partnership, how the queue works, and what it does not cover.',
        category='Workflow', date='2026-09-09', read=4,
        cover='2024/06/FreePower_Bar_5.jpeg', focal='50% 45%',   # the FreePower bar still replaced the Gardyn kitchen set on November 11, 2026
        cover_alt='Two phones charging on a FreePower bar top beside cocktails, from the FreePower shoot.',
        takeaways=['Unlimited requests and revisions within your plan, worked in priority order.', 'A typical first edit takes a few days.', 'Productions are scoped separately, so the monthly fee never hides a shoot.'],
        body=[
            ('p', '“Unlimited” is a word that makes people reach for the fine print, so here is ours, in plain English.'),
            ('h2', 'What counts as a deliverable'),
            ('p', 'A deliverable is any finished piece within the scope of your plan: an edit, a cutdown, a set of statics, an animation, a resized version for a new placement. Request as many as you need and as many revisions as it takes. There is no monthly cap, no per-asset fee and no clock running on revisions.'),
            ('h2', 'How the queue works'),
            ('p', 'Unlimited does not mean simultaneous. Your dedicated team works through requests in priority order, and the order is set with you. On the strategy call, and in Slack between calls, we agree on what comes first. Urgent things jump the line; the rest move in sequence.'),
            ('p', 'A typical first edit takes a few days, depending on complexity and what’s already in the queue. Simple resizes and iterations usually come back in a day or two. A new concept with motion design takes longer. We confirm the expected turnaround when the brief lands.'),
            ('quote', 'The question is never whether you can afford another cut. It is what to cut next.'),
            ('h2', 'What is not included'),
            ('p', 'New productions. A shoot day, a crew, talent and locations are scoped and billed separately, per project, with a 50% deposit to confirm the dates. We keep it that way on purpose: a production is a real cost with a real scope, and folding it into a monthly fee would mean either overcharging quiet months or underdelivering on busy ones.'),
            ('p', 'What the partnership does include is everything around a production: planning it in the Birdline App, cutting from it for as long as the footage is useful, and measuring what it returned.'),
            ('h2', 'Why we built it this way'),
            ('p', 'We started Birdline because too much content was going to waste. Brands were paying per asset, so they ordered fewer assets, tested fewer ideas and learned less from each campaign. Unlimited deliverables flip the incentive. When another cut costs nothing extra, you make the cut, you test the hook, and the library and the learning both grow. That is the whole point.'),
            ('h2', 'The short version'),
            ('ul', ['Request anything within your plan, as often as you need.', 'We set priorities together and work the queue in order.', 'First edits typically take a few days. Simple resizes and iterations usually take a day or two.', 'Shoots are scoped separately, everything around them is included.', 'Rolling partnership, 60 days’ notice to cancel.']),
        ],
    ),
    dict(
        slug='inside-a-birdline-kickoff',
        title='Inside a Birdline Kickoff',
        dek='The first week of a partnership, and why we spend it learning how you work before we make anything.',
        category='Workflow', date='2026-08-12', read=4,
        cover='new/production-hero.jpg',
        cover_alt='A Birdline crew on set in a kitchen, the director watching the monitor.',
        takeaways=['One call to meet the team and decide what comes first.', 'Share what you have: guidelines, past campaigns, raw footage, working files.', 'A Slack channel and the Birdline App are set up before the first brief.'],
        body=[
            ('p', 'A partnership that starts well is usually one where the first week was spent listening. Here is what ours looks like.'),
            ('h2', 'The kickoff call'),
            ('p', 'About forty-five minutes. You meet your project manager and the Birds who will make your work. We learn how your team runs: who signs off, where the files live, what is coming up on the calendar and what is keeping you up at night. Then we decide, together, what to tackle first. Usually that is the next campaign; sometimes it is a backlog of footage nobody has had time to cut.'),
            ('h2', 'What to share'),
            ('p', 'Everything you have, in whatever shape it is in. Brand guidelines. Past campaigns, the ones that worked and the ones that did not. Raw footage and project files from previous productions. Performance data if you can get it. We organize what comes in and flag what we can start using right away. More than once, the first deliverables of a partnership have been cut entirely from footage the brand already owned.'),
            ('quote', 'The fastest first win is usually sitting on a hard drive you already have.'),
            ('h2', 'Setting up the workflow'),
            ('p', 'Before the first brief, two things are in place. A shared Slack channel connects both teams, with a thread per project so conversations stay attached to the work. And you are set up in the Birdline App, which is included in the partnership and open to your own projects too. Briefs, deliverables and the finished library live there, and when performance data is connected, so do the results.'),
            ('p', 'We deliberately do not work inside your internal tools. Permissions, folder structures and notification settings vary from company to company, and the time spent navigating them is time not spent on the work. Slack for the conversation, Frame.io for review, the Birdline App for everything else.'),
            ('h2', 'The first deliverables'),
            ('p', 'Most partnerships have their first edits in review within the first two weeks, and the first strategy call on the calendar for the week after. From there the rhythm sets in: briefs in, drafts to Frame.io, finals to the library, a call every other week to look at what shipped and decide what is next.'),
            ('p', 'Onboarding is simple and fast on purpose. We can usually start within a week of the first conversation. The work is what takes care; the start should not.'),
        ],
    ),
]
