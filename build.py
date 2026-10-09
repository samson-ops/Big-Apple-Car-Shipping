#!/usr/bin/env python3
"""Builds the Big Apple Car Shipping site.
  index.html                      from index.template.html
  locations/index.html            from locations-index.template.html + locations.json
  <slug>-car-shipping/index.html  from location.template.html + content/<slug>.json + locations.json
  functions/api/quote/[[path]].js lead proxy with this site's BeRocker key
  robots.txt, sitemap.xml
Run:  python3 build.py
"""
import json, re, pathlib, html, shutil
root = pathlib.Path(__file__).parent
cfg = json.loads((root/'site.config.json').read_text())
DOMAIN = cfg['domain']
offices = json.loads((root/'locations.json').read_text())
embed_src = (root/'vendor'/'pricing-tool-embed.html').read_text()

def setval(src, key, val):
    return re.sub(r"(%s:\s*)'[^']*'" % key, lambda m: m.group(1) + "'" + val.replace("'", "\\'") + "'", src, count=1)

def make_embed(phone_display, phone_tel, site_code):
    e = embed_src
    e = setval(e, 'googleMapsKey', cfg['googleMapsKey'])
    e = setval(e, 'phoneDisplay',  phone_display)
    e = setval(e, 'phoneTel',      phone_tel)
    e = setval(e, 'brandName',     'Big Apple Car Shipping')
    e = setval(e, 'siteUrl',       DOMAIN)
    e = setval(e, 'siteLabel',     DOMAIN.replace('https://', ''))
    e = setval(e, 'siteCode',      site_code)
    e = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', e)   # page already preconnects
    return e

def fill_common(s):
    return (s.replace('__PHONE_DISPLAY__', cfg['phoneDisplay']).replace('__PHONE_TEL__', cfg['phoneTel'])
             .replace('__EMAIL__', cfg['email'])
             .replace('https://bigapplecarshipping.com', DOMAIN))

# ---------- homepage ----------
home_t = (root/'index.template.html').read_text()
office_links = ''.join('<li><a href="/%s-car-shipping/">%s</a></li>' % (o['slug'], o['name']) for o in offices)
home_t = home_t.replace('<li><a href="/locations/">Locations</a></li>', office_links + '<li><a href="/locations/">All locations</a></li>')
import re as _re
_areas = ''.join('<li><a href="/%s-car-shipping/">%s</a></li>' % (o['slug'], o['name']) for o in offices) + '<li><a href="/locations/">All locations</a></li>'
home_t = _re.sub(r'(<div class="areas">\s*<h3>Where we pick up</h3>\s*<ul>).*?(</ul>)', lambda m: m.group(1) + _areas + m.group(2), home_t, flags=_re.S)

home = home_t.replace('<!--PRICING_TOOL-->', make_embed(cfg['phoneDisplay'], cfg['phoneTel'], cfg['siteCode']))
(root/'index.html').write_text(fill_common(home))

# shared pieces for subpages (anchors become absolute so they work off the homepage)
css = re.search(r'<style>.*?</style>', home_t, re.S).group(0)
header = re.search(r'<!--HEADER-->(.*?)<!--/HEADER-->', home_t, re.S).group(1).replace('href="#', 'href="/#')
footer = re.search(r'<!--FOOTER-->(.*?)<!--/FOOTER-->', home_t, re.S).group(1).replace('href="#', 'href="/#')

def geo(o):
    m = re.search(r'!2d(-?[\d.]+)!3d(-?[\d.]+)', o['map']); return m.group(2), m.group(1)

def business_schema(o, extra=None):
    lat, lng = geo(o)
    d = {"@type": ["AutoTransport", "MovingCompany", "LocalBusiness"],
         "@id": "%s/%s-car-shipping/#office" % (DOMAIN, o['slug']),
         "name": "Big Apple Car Shipping - %s" % o['name'],
         "url": "%s/%s-car-shipping/" % (DOMAIN, o['slug']),
         "telephone": o['phoneTel'],
         "image": DOMAIN + "/assets/og-image.jpg", "logo": DOMAIN + "/assets/big-apple-car-shipping-logo.png",
         "parentOrganization": {"@id": DOMAIN + "/#business"},
         "address": {"@type": "PostalAddress", "streetAddress": o['street'], "addressLocality": o['city'],
                     "addressRegion": "NY", "postalCode": o['zip'], "addressCountry": "US"},
         "geo": {"@type": "GeoCoordinates", "latitude": float(lat), "longitude": float(lng)},
         "hasMap": o['map'],
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "00:00", "closes": "23:59"}],
         "priceRange": "$$"}
    if extra: d.update(extra)
    return d

# ---------- location pages ----------
loc_t = (root/'location.template.html').read_text()
for o in offices:
    c = json.loads((root/'content'/(o['slug'] + '.json')).read_text())
    lat, lng = geo(o)
    page_url = "%s/%s-car-shipping/" % (DOMAIN, o['slug'])
    schema = {"@context": "https://schema.org", "@graph": [
        business_schema(o, {"areaServed": [{"@type": "Place", "name": n} for n in c['neighborhoods']],
                            "description": html.unescape(re.sub('<[^>]+>', '', c['intro']))[:300]}),
        {"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url, "name": c['title'],
         "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": page_url + "#office"},
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
             {"@type": "ListItem", "position": 2, "name": "Locations", "item": DOMAIN + "/locations/"},
             {"@type": "ListItem", "position": 3, "name": c['city'] + ", NY", "item": page_url}]}},
        {"@type": "FAQPage", "@id": page_url + "#faq",
         "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in c['faqs']]}
    ]}
    others = [x for x in offices if x['slug'] != o['slug']]
    rep = {
        'title': html.escape(c['title']), 'metaDescription': html.escape(c['metaDescription']),
        'slug': o['slug'], 'domain': DOMAIN, 'lat': lat, 'lng': lng,
        'city': c['city'], 'county': c['county'], 'region': c['region'],
        'h1': c['h1'], 'heroSub': c['heroSub'],
        'phoneTel': o['phoneTel'], 'phoneDisplay': o['phoneDisplay'],
        'street': o['street'], 'addrCity': o['city'], 'zip': o['zip'], 'map': o['map'],
        'schema': json.dumps(schema, ensure_ascii=False), 'css': css, 'header': header, 'footer': footer,
        'intro': c['intro'],
        'sections': ''.join('<h2>%s</h2>%s' % (s['h2'], s['html']) for s in c['sections']),
        'neighborhoods': ''.join('<span>%s</span>' % n for n in c['neighborhoods']),
        'routes': ''.join('<tr><td>%s</td><td>%s</td><td><small>from</small>%s</td></tr>' % (r['dest'], r['transit'], r['price']) for r in c['routes']),
        'faqs': ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', f['q'], f['a']) for i, f in enumerate(c['faqs'])),
        'otherOffices': ''.join('<li><a href="/%s-car-shipping/">%s</a></li>' % (x['slug'], x['name']) for x in others),
        'officeNav': ''.join('<li><a%s href="/%s-car-shipping/">%s<span style="float:right;color:var(--mute);font-size:13px">%s</span></a></li>' % (' class="cur"' if x['slug'] == o['slug'] else '', x['slug'], x['name'], x['phoneDisplay']) for x in offices),
        'ctaLine': c['ctaLine'],
    }
    page = loc_t
    for k, v in rep.items():
        page = page.replace('{{%s}}' % k, v)
    assert '{{' not in page, re.findall(r'\{\{\w+\}\}', page)
    page = page.replace('<!--PRICING_TOOL-->', make_embed(o['phoneDisplay'], o['phoneTel'], cfg['siteCode'] + '-' + o['slug'].upper().replace('-', '')))
    out = root/(o['slug'] + '-car-shipping'); out.mkdir(exist_ok=True)
    (out/'index.html').write_text(fill_common(page))

# ---------- locations index ----------
idx_t = (root/'locations-index.template.html').read_text()
blurbs = {}
for o in offices:
    c = json.loads((root/'content'/(o['slug'] + '.json')).read_text())
    blurbs[o['slug']] = html.unescape(c['heroSub'])
cards = ''.join('''<article class="loc-card"><div class="txt"><h2><a href="/%(slug)s-car-shipping/">%(name)s, NY</a></h2>
<address>%(street)s<br>%(city)s, NY %(zip)s</address><a class="tel" href="tel:%(tel)s">%(phone)s</a><p>%(blurb)s</p>
<a class="btn btn-dark" href="/%(slug)s-car-shipping/">%(name)s car shipping</a></div>
<iframe src="%(map)s" title="Map of Big Apple Car Shipping %(name)s" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe></article>'''
    % dict(slug=o['slug'], name=o['name'], street=o['street'], city=o['city'], zip=o['zip'], tel=o['phoneTel'], phone=o['phoneDisplay'], map=o['map'], blurb=blurbs[o['slug']]) for o in offices)
idx_schema = {"@context": "https://schema.org", "@graph": [
    {"@type": "ItemList", "name": "Big Apple Car Shipping offices", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": business_schema(o)} for i, o in enumerate(offices)]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Locations", "item": DOMAIN + "/locations/"}]}]}
idx = idx_t.replace('{{cards}}', cards).replace('{{schema}}', json.dumps(idx_schema)).replace('{{css}}', css).replace('{{header}}', header).replace('{{footer}}', footer).replace('{{domain}}', DOMAIN)
(root/'locations').mkdir(exist_ok=True)
(root/'locations'/'index.html').write_text(fill_common(idx))


# ---------- article pages (services, routes, guides) ----------
loc_css = re.search(r'<style>\n/\* ---- location page ---- \*/.*?</style>', (root/'location.template.html').read_text(), re.S).group(0)
art_t = (root/'article.template.html').read_text()
ROUTE_SECTION = ('Routes from New York', '/#routes'); SERVICE_SECTION = ('Services', '/#services'); GUIDE_SECTION = ('Guides', '/car-shipping-cost/')
article_slugs = []
for f in sorted((root/'content'/'articles').glob('*.json')):
    c = json.loads(f.read_text()); slug = c['slug']; page_url = '%s/%s/' % (DOMAIN, slug)
    if slug.startswith('new-york-to-'): sec = ROUTE_SECTION
    elif slug in ('car-shipping-cost', 'car-shipping-checklist'): sec = GUIDE_SECTION
    else: sec = SERVICE_SECTION
    article_slugs.append(slug)
    graph = [
        {"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url, "name": c['title'], "description": c['metaDescription'],
         "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
             {"@type": "ListItem", "position": 2, "name": sec[0], "item": DOMAIN + sec[1]},
             {"@type": "ListItem", "position": 3, "name": c['h1'], "item": page_url}]}},
        {"@type": "FAQPage", "@id": page_url + "#faq", "mainEntity": [{"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in c['faqs']]}]
    if sec is SERVICE_SECTION:
        graph.append({"@type": "Service", "@id": page_url + "#service", "name": c['h1'], "serviceType": c['h1'], "provider": {"@id": DOMAIN + "/#business"},
                      "areaServed": {"@type": "Country", "name": "United States"}, "url": page_url, "description": c['metaDescription']})
    else:
        graph.append({"@type": "Article", "@id": page_url + "#article", "headline": c['h1'], "description": c['metaDescription'], "mainEntityOfPage": page_url,
                      "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "image": DOMAIN + "/assets/og-image.jpg",
                      "datePublished": "2026-10-09", "dateModified": "2026-10-09"})
    table_html = ''
    t = c.get('table')
    if t and t.get('rows'):
        table_html = '<h2>%s</h2><table class="routes loc"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (
            t['caption'], ''.join('<th scope="col">%s</th>' % h for h in t['headers']),
            ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % cell for cell in r) for r in t['rows']))
    rep = {'title': html.escape(c['title']), 'metaDescription': html.escape(c['metaDescription']), 'slug': slug, 'domain': DOMAIN,
           'sectionName': sec[0], 'sectionHref': sec[1], 'crumb': c['h1'], 'kicker': c['kicker'], 'h1': c['h1'], 'heroSub': c['heroSub'],
           'schema': json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False), 'css': css, 'pagecss': loc_css,
           'header': header, 'footer': footer, 'intro': c['intro'],
           'sections': ''.join('<h2>%s</h2>%s' % (s_['h2'], s_['html']) for s_ in c['sections']), 'table': table_html,
           'faqTitle': 'Questions about ' + (c['h1'][0].lower() + c['h1'][1:] if not c['h1'].startswith('New York') else c['h1']),
           'faqs': ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q['q'], q['a']) for i, q in enumerate(c['faqs'])),
           'related': ''.join('<li><a href="%s">%s</a></li>' % (r['href'], r['label']) for r in c['related']),
           'ctaTitle': c['ctaTitle'], 'ctaLine': c['ctaLine']}
    page = art_t
    for k, v in rep.items(): page = page.replace('{{%s}}' % k, v)
    assert '{{' not in page, (slug, re.findall(r'\{\{\w+\}\}', page))
    page = page.replace('<!--PRICING_TOOL-->', make_embed(cfg['phoneDisplay'], cfg['phoneTel'], cfg['siteCode'] + '-' + slug.upper().replace('-', '')[:18]))
    out = root/slug; out.mkdir(exist_ok=True); (out/'index.html').write_text(fill_common(page))

# ---------- company and legal pages ----------
simple_t = (root/'simple.template.html').read_text()
office_cards = ''.join('<div class="office-card"><h3><a href="/%s-car-shipping/">%s, NY</a></h3><address>%s<br>%s, NY %s</address><a class="tel" href="tel:%s">%s</a></div>'
                       % (o['slug'], o['name'], o['street'], o['city'], o['zip'], o['phoneTel'], o['phoneDisplay']) for o in offices)
static_slugs = []
for c in json.loads((root/'content'/'static'/'pages.json').read_text()):
    slug = c['slug']; page_url = '%s/%s/' % (DOMAIN, slug); static_slugs.append((slug, c.get('robots', 'index, follow')))
    graph = [{"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url, "name": c['title'], "isPartOf": {"@id": DOMAIN + "/#website"},
              "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                                                                             {"@type": "ListItem", "position": 2, "name": c['crumb'], "item": page_url}]}}]
    if slug == 'about': graph[0]["@type"] = "AboutPage"
    if slug == 'contact': graph[0]["@type"] = "ContactPage"
    rep = {'title': html.escape(c['title']), 'metaDescription': html.escape(c['metaDescription']), 'slug': slug, 'domain': DOMAIN, 'robots': c.get('robots', 'index, follow'),
           'crumb': c['crumb'], 'h1': c['h1'], 'heroSub': c['heroSub'], 'schema': json.dumps({"@context": "https://schema.org", "@graph": graph}),
           'css': css, 'pagecss': loc_css, 'header': header, 'footer': footer, 'body': c['body'].replace('{{OFFICE_CARDS}}', office_cards)}
    page = simple_t
    for k, v in rep.items(): page = page.replace('{{%s}}' % k, v)
    assert '{{' not in page, (slug, re.findall(r'\{\{\w+\}\}', page))
    out = root/slug; out.mkdir(exist_ok=True); (out/'index.html').write_text(fill_common(page))

# ---------- 404 ----------
nf = {'title': 'Page not found | Big Apple Car Shipping', 'metaDescription': 'That page does not exist.', 'slug': '404', 'domain': DOMAIN, 'robots': 'noindex, nofollow',
      'crumb': 'Not found', 'h1': 'That page took a wrong exit', 'heroSub': 'The address you followed does not exist on this site. The links below will get you where you were going.',
      'schema': '{}', 'css': css, 'pagecss': loc_css, 'header': header, 'footer': footer,
      'body': '<p>Try one of these:</p><ul><li><a href="/#quote">Get an instant car shipping quote</a></li><li><a href="/locations/">Find your nearest New York office</a></li><li><a href="/car-shipping-cost/">See what car shipping costs</a></li><li><a href="/new-york-to-florida-car-shipping/">New York to Florida car shipping</a></li><li><a href="/contact/">Contact us</a></li></ul>'}
page = simple_t
for k, v in nf.items(): page = page.replace('{{%s}}' % k, v)
page = page.replace('<link rel="canonical" href="%s/404/">' % DOMAIN, '')
(root/'404.html').write_text(fill_common(page))

# ---------- lead proxy, robots, sitemap ----------
fn = (root/'vendor'/'quote-function.js').read_text().replace("'YOUR_LEAD_SOURCE_KEY'", "'%s'" % cfg['leadSourceKey'])
out = root/'functions'/'api'/'quote'; out.mkdir(parents=True, exist_ok=True)
(out/'[[path]].js').write_text(fn)
(root/'robots.txt').write_text("User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)
urls = ([('/', '1.0', 'weekly'), ('/locations/', '0.8', 'monthly')] + [('/%s-car-shipping/' % o['slug'], '0.9', 'monthly') for o in offices]
        + [('/%s/' % a, '0.8', 'monthly') for a in article_slugs] + [('/%s/' % sl, '0.5', 'yearly') for sl, rb in static_slugs if 'noindex' not in rb])
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join('  <url><loc>%s%s</loc><lastmod>2026-10-09</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>\n' % (DOMAIN, u, f, p) for u, p, f in urls) + '</urlset>\n')
print('built %d pages: home, locations, %d offices, %d articles, %d company/legal, 404' % (3 + len(offices) + len(article_slugs) + len(static_slugs), len(offices), len(article_slugs), len(static_slugs)))
