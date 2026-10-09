# Article page brief — Big Apple Car Shipping (services, routes, guides)

Big Apple Car Shipping: New York–based, FMCSA-licensed auto transport broker, 10 NY offices (Bronx, Yonkers, Hempstead,
North Hempstead, Babylon, Islip, Brookhaven, Albany, Schenectady, Buffalo), open & enclosed carriers, door-to-door,
nationwide, instant online quote (the quote tool sits beside the H1 on every page; refer to it as "the quote tool").
Voice: plain, confident, specific, like a dispatcher explaining it to a neighbor. Sentence case headings. No all-caps
labels, no "→", no exclamation points, at most 3 em dashes per page. Never invent reviews, ratings, employee names,
company statistics, or legal guarantees. Do not name competitors. Do not use "we are the best". Prices are typical ranges.

## Hard requirements
- Word count across intro + sections + faqs: the target given in your assignment (±100). Count it.
- Content must be specific to THIS page's topic and must NOT recycle the generic "how it works / open vs enclosed /
  why choose us" homepage material as its backbone. Every section should teach something a person deciding on THIS
  service or route actually needs: real numbers, real road names, real timing, real trade-offs, real paperwork.
- Primary keyword given in the assignment: in H1, first 100 words, 2 H2s, title, meta description. Natural variants.
- H2s must be concrete and specific (not "Benefits", not "Why choose us", not "Overview").
- 5 FAQs a real customer would ask about THIS topic; answers 40–80 words each.
- Optional "table": a small data table (3 columns, 5–9 rows) only if it carries real information (price bands,
  transit by distance, seasonal pricing, size surcharges, route legs). Give it a caption and column headers.
- Mention the 10 New York offices or a specific office where it is natural (e.g. a route page can say pickups run from
  the Bronx and Long Island offices daily). Do not list all ten in every page.
- Internal links: in the HTML you may link ONLY to these paths: / , /locations/ , /car-shipping-cost/ ,
  /car-shipping-checklist/ , /open-car-transport/ , /enclosed-auto-transport/ , /door-to-door-car-shipping/ ,
  /expedited-car-shipping/ , /snowbird-car-shipping/ , /military-car-shipping/ , /new-york-to-florida-car-shipping/ ,
  /new-york-to-california-car-shipping/ , /new-york-to-texas-car-shipping/ , /new-york-to-north-carolina-car-shipping/ ,
  /new-york-to-georgia-car-shipping/ , /new-york-to-illinois-car-shipping/ , /new-york-to-arizona-car-shipping/ ,
  /new-york-to-colorado-car-shipping/ , /new-york-to-washington-car-shipping/ , /<office>-car-shipping/ for
  hempstead, north-hempstead, babylon, islip, brookhaven, bronx, yonkers, albany, schenectady, buffalo.
  Use 3–6 internal links per page, in-sentence, with descriptive anchor text.

## Pricing reference (open carrier, running mid-size sedan, booked ~1 week out, from the NYC metro)
Florida $650–750 · Carolinas $550–650 · Georgia $650–750 · Illinois $700–800 · Texas $1,000–1,100 ·
Colorado $1,100–1,200 · Arizona $1,250–1,350 · California $1,350–1,500 · Washington state $1,400–1,550.
Enclosed adds 30–50%. SUVs/pickups add $100–250. Inoperable adds $100–200. Expedited adds $150–300.
Peak: Jan–Mar southbound snowbird, Jun–Aug everything, holiday weeks. Deposit at booking, balance to driver on delivery.

## Output
Write ONLY valid JSON (no fences, no commentary) to the file path given. Schema:
{
  "slug": "...", "title": "... | Big Apple Car Shipping", "metaDescription": "...",   // 140–158 chars
  "h1": "...", "heroSub": "...",                       // heroSub <= 40 words
  "kicker": "...",                                     // 3–6 words shown above H1, e.g. "Service", "Route guide", "Pricing guide"
  "intro": "<p>...</p><p>...</p>",
  "sections": [ {"h2": "...", "html": "<p>...</p>"} ],  // 5–7
  "table": {"caption": "...", "headers": ["...","...","..."], "rows": [["...","...","..."]]}  or null,
  "faqs": [ {"q": "...", "a": "..."} ],
  "related": [ {"label": "...", "href": "/..."} ],    // 4–6 from the allowed list, most relevant first
  "ctaTitle": "...", "ctaLine": "..."
}
