# Google RSA Specs & Best Practices

## Character Limits (Hard Limits — Google will truncate)

| Component | Limit | Notes |
|---|---|---|
| Headline | 30 characters | Includes spaces |
| Description | 90 characters | Includes spaces |
| Display URL path 1 | 15 characters | Each path field |
| Display URL path 2 | 15 characters | Each path field |

## Volume Requirements

| Component | Min | Recommended | Max |
|---|---|---|---|
| Headlines | 3 | 10–15 | 15 |
| Descriptions | 2 | 4 | 4 |

Google's Ad Strength score improves significantly with 10+ unique headlines.

## Pinning

Headlines and descriptions can be pinned to specific positions:
- **Position 1**: First headline shown — use for brand name or primary value prop
- **Position 2**: Second headline — strongest differentiator or keyword
- **Position 3**: Third headline — CTA or secondary benefit

**Use pinning sparingly.** Pinning reduces Google's ability to optimize combinations.
Only pin when brand compliance or message control is critical.

## RSA Combination Logic

Google autonomously mixes headlines and descriptions. Every headline must work with every other
headline. Write modularly:

**Good (modular):**
- "Free Shipping on Orders $50+"
- "Dermatologist-Tested Formula"
- "Try Risk-Free for 30 Days"

**Bad (sequential logic that breaks when mixed):**
- "Step 1: Visit Our Site"
- "Step 2: Choose Your Plan"

## Keyword Inclusion

- Include the **exact match keyword** in at least 2–3 headlines naturally
- Use **dynamic keyword insertion** `{KeyWord:Default Text}` for high-volume campaigns
  where exact phrasing helps quality score
- Don't force keywords — a natural headline beats a stuffed one

## Ad Strength Checklist

- [ ] 15 unique headlines (no duplicates or near-duplicates)
- [ ] 4 descriptions
- [ ] Keywords appear naturally in 3+ headlines
- [ ] At least one headline is the brand name or URL
- [ ] CTAs appear in 2–3 headlines (not more — avoid repetition)
- [ ] Descriptions are standalone and don't rely on a specific headline
- [ ] No repeated phrases across headlines (Google flags this)

## SERP Formatting Tips

- Numbers and symbols stand out: use %, #, $, |
- ALL CAPS sparingly for single words ("FREE", "NEW") — not whole headlines
- Punctuation at the end of a headline carries over to next: "Fast. Easy. Effective."
- Sentence case performs as well as title case; be consistent within a campaign

## Common RSA Mistakes to Avoid

| Mistake | Fix |
|---|---|
| Generic CTAs ("Click Here") | Specific CTAs ("Start Your Free Trial") |
| Feature-led headlines ("Made with Hyaluronic Acid") | Benefit-led ("Plumper Skin in 2 Weeks") |
| Repeating the same idea 3 ways | True variety across benefit, proof, CTA, urgency |
| Headlines that only work in sequence | Each headline standalone-strong |
| Ignoring mobile — long descriptions truncate | Front-load the key message in first 60 chars |