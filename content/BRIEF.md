# Location page content brief — Big Apple Car Shipping

You are writing the content for ONE local landing page for Big Apple Car Shipping, a New York–based,
FMCSA-licensed auto transport broker (open & enclosed carriers, door-to-door, nationwide, instant online quote).
Voice: plain, confident, specific, like a dispatcher who knows the area — NOT brochure fluff.
Sentence case headings. No all-caps labels. No "→". No exclamation points. No em-dash overuse (max 3 in whole page).
Never invent reviews, ratings, employee names, or statistics about the company. Transit times and typical prices
below are fine to use. Do not mention competitors by name.

## Hard requirements
- Total words across intro + sections + faqs: 1,450–1,700. Count them.
- Content must be UNIQUE to this place. At least 70% of sentences should be impossible to paste onto another
  town's page: name real local roads, highways, parkways, exits, neighborhoods/hamlets, landmarks, employers,
  colleges, train stations, bridges/ferries, typical weather, typical reasons people here ship cars.
- Do NOT reuse the generic homepage sections (how it works / open vs enclosed explainer) as the backbone.
  You may have ONE short section on open vs enclosed only if it is framed around local conditions.
- Mention the local office address and local phone number naturally once or twice in the body.
- Primary keyword: "car shipping <City>" / "<City> auto transport" / "ship a car from <City> NY". Use natural variants;
  keyword in H1, in the first 100 words, in 2 H2s, in meta title and description. No stuffing.
- H2s must be specific and different in wording from other pages (e.g. not "Why choose us").
- FAQs: 5 questions a real resident of THIS place would ask (mention local specifics). Answers 40–80 words each.
- Routes table: 8 destinations popular from this area with transit (days) and a typical open-carrier price for a
  running sedan. Long Island → Florida ~$650–750, → California ~$1,350–1,500, → Texas ~$1,000–1,100,
  → Carolinas ~$550–650, → Georgia ~$650–750, → Illinois ~$700–800, → Arizona ~$1,250–1,350, → Colorado ~$1,100–1,200.
  Buffalo is ~400 miles further west: Florida ~$800–900, California ~$1,250–1,400, Texas ~$950–1,050,
  Carolinas ~$650–750, Illinois ~$500–600, Arizona ~$1,150–1,300, Colorado ~$1,000–1,100, Georgia ~$700–800.
  NYC/Bronx and Yonkers (Westchester) use the Long Island bands minus about $50.
  Albany/Schenectady (Capital Region, ~150 mi north of NYC): Florida ~$750–850, California ~$1,350–1,450,
  Texas ~$1,000–1,100, Carolinas ~$600–700, Georgia ~$700–800, Illinois ~$650–750, Arizona ~$1,250–1,350,
  Colorado ~$1,100–1,200, Boston/New England short hauls ~$350–450.
- Do not reuse section themes already used on sibling pages (the parkway truck ban, snowbird season as a whole
  section, salt air, Sandy). You may mention them in a sentence but find THIS place's own themes.
- neighborhoods: 10–16 real nearby villages/hamlets/neighborhoods served from this office.
- Also provide a "nearbyOffices" note is NOT needed; I will add internal links.

## Output
Write ONLY valid JSON (no markdown fences, no commentary) to the exact file path given to you. Schema:
{
  "slug": "...",                      // given
  "city": "...", "county": "...", "region": "...",
  "title": "... | Big Apple Car Shipping",   // <= 60 chars before the brand suffix is fine to exceed slightly; total <= 70
  "metaDescription": "...",           // 140–158 chars, includes city + a phone or benefit
  "h1": "...",                        // e.g. "Car shipping in Hempstead, NY"
  "heroSub": "...",                   // 1–2 sentences, <= 45 words
  "intro": "<p>...</p><p>...</p>",    // 2 paragraphs, HTML
  "sections": [ {"h2": "...", "html": "<p>...</p>..."} ],   // 5–7 sections; HTML may use <p>, <ul><li>, <strong>
  "routes": [ {"dest": "Hempstead to Miami, FL", "transit": "2–3 days", "price": "$699"} ],  // 8 rows
  "neighborhoods": ["...", "..."],
  "faqs": [ {"q": "...", "a": "..."} ],   // 5
  "ctaLine": "..."                    // one sentence for the bottom CTA
}
