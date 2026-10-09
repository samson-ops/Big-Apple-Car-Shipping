# Big Apple Car Shipping — website

Static site, 38 pages, ready for Cloudflare Pages (the pricing tool's lead proxy is a Pages Function).

## Deploy (Cloudflare Pages)
1. Cloudflare dashboard → Workers & Pages → Create → Pages → "Upload assets".
2. Upload the CONTENTS of this folder (index.html must be at the root). Include the `functions` folder.
3. Project settings → Environment variables → add `BEROCKER_LEAD_KEY = 6ac838d7a3d4f` (it is also set as the
   default inside functions/api/quote/[[path]].js, so the tool works either way).
4. Custom domains → add bigapplecarshipping.com and www (Cloudflare handles the redirect and HTTPS).
5. Google Cloud console → the Maps API key in site.config.json → add `bigapplecarshipping.com/*` to its HTTP
   referrer restrictions (ZIP suggestions only; the quote tool works without it).

## After it is live
- Run one test quote from a phone and confirm the lead lands in BeRocker under the Big Apple lead source
  (secondary_id starts with BIGAPPLE-…).
- Google Search Console → add property → submit https://bigapplecarshipping.com/sitemap.xml
- Google Business Profile for each of the 13 offices → website field = that office's page
  (e.g. https://bigapplecarshipping.com/brooklyn-car-shipping/).
- Replace the three placeholder reviews on the homepage with real ones (index.template.html, "reviews" section).

## Editing
- Phone, email, domain, lead key: `site.config.json`
- Offices (address, phone, map): `locations.json` + a content file in `content/<slug>.json`
- Service / route / guide pages: `content/articles/*.json`
- About, contact, licensing, privacy, terms: `content/static/pages.json`
- Design and homepage: `index.template.html` (shared CSS lives here), `location.template.html`,
  `article.template.html`, `simple.template.html`
- Rebuild everything: `python3 build.py`  (requires Python 3; no other dependencies)

## Pages
/  /locations/  /about/  /contact/  /licensing-insurance/  /privacy/  /terms/  /404.html
13 office pages: /<city>-car-shipping/
6 services, 9 routes, 2 guides: see sitemap.xml
