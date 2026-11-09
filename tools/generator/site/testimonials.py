"""The Testimonials page (November 9, 2026): every client quote on the site, in full, on one page. Rendered by testimonials_page()
in build_site.py. The people come from the homepage's Client Stories rows (name, title, headshot, logo) in Mike's order; the
words come from each brand's case study where there is one (the long version of the quote), and from the homepage card where
there is not."""

HERO = dict(
    eyebrow='Client stories',
    h1='The Work Speaks. |So Do Our Clients.',
    lede='Fifteen brands on what it is like to have Birdline as their creative team: the first brief, the shoots, the turnaround, and the partnership month after month.',
)

# who is on the page, in order: (homepage name, the case study whose quote to use or None, the brand's case-study slug or None)
PEOPLE = [
    ('Jake Slatnick', 'freepower', 'freepower'),
    ('Kristen Connors', 'gardyn', 'gardyn'),
    ('Zach Goldstein', 'public-rec', 'public-rec'),
    ('Chelsea Moon', 'route', 'route'),
    ('John Bradford', 'edjy', 'edjy'),
    ('Brent Sandor', '686', '686'),
    ('Howie Zisser', 'public-rec', 'public-rec'),
    ('Megan Gray', 'literati', 'literati'),
    ('Nick Sarath', 'patrol', 'patrol'),
    ('Kat Cooper', 'solidroad', 'solidroad'),
    ('Adam Walker', 'willies-remedy', 'willies-remedy'),
    ('Shannon Douglas', None, None),
    ('Leslie Smith', None, None),
    ('FX Rouxel', 'gardyn', 'gardyn'),
    ('Zack McCabe', 'whoop', 'whoop'),
]

STATS = [('15', 'clients, in their own words'), ('12', 'case studies behind them'), ('Since 2021', 'the longest partnership still running')]

WORK = dict(eyebrow='Hear it in the work', h2='The Partnerships |Behind the Words.', slugs=['whoop', 'gardyn', 'public-rec', 'route'])

CLOSE = dict(heading='Let’s Add Your Story.', sub='Tell us what is in your pipeline and where your team could use another set of hands.', photo='2024/05/Gardyn_7_29_2025_Kitchen_77909.jpeg')
