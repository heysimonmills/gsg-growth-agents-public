---
name: pain-points
description: >
  Use this skill whenever the user wants to research customer pain points, complaints,
  frustrations, or struggles around a product, service, or category — especially using
  Reddit as a source. Triggers include: "find pain points for X", "what do people
  complain about with X", "research Reddit for X problems", "find customer language for
  X", "pull VOC (voice of customer) for X", "what are people saying about X on Reddit",
  "research ad copy angles for X", "find copy insights for X", "what frustrates people
  about X", or any request to scrape/search Reddit for real customer language, problems,
  or insights to inform marketing copy. Use this skill even if the user just says "research
  [topic] for me" in a marketing or copywriting context.
---

# Perplexity Pain Point Research (Reddit-First)

A skill for extracting real customer pain points and verbatim language from Reddit using
the Perplexity API for discovery and Apify for live post/comment scraping. Output is
structured for direct use in ad copy, landing page copy, email, and creative strategy.

---

## Overview

The goal is not summarized insights — it's **raw, exact customer language** pulled from
real Reddit threads. The output should feel like a swipe file a copywriter would kill for:
real words, real frustration, real desire.

**Phase 1 — Discovery**: Perplexity `sonar` model identifies the right subreddits,
keywords, and thread types, and surfaces initial quotes.  
**Phase 2 — Live Scraping**: Apify `trudax~reddit-scraper-lite` pulls raw posts and
comments from the subreddits Perplexity identifies — unfiltered, sortable by upvotes.  
**Output**: Structured pain point report with copy-ready language drawn from both sources.

---

## Step 1: Clarify the Research Brief

Before running any queries, confirm:

1. **Topic / product / category** — What is being researched? (e.g., "collagen supplements", "project management software", "meal kit delivery")
2. **Target audience** — Who uses this? (e.g., "women 35–55", "startup founders", "busy parents") — if known
3. **Angle** — Are we looking for:
   - Pains with the *category* broadly (e.g., "collagen supplements in general")
   - Pains with a *specific brand* (e.g., "Vital Proteins")
   - Pains that a *new product* solves (e.g., "why don't people stick with collagen")
4. **Output use** — Ad copy? Landing page? Email? UGC brief? (Affects how you frame the output)

If the user's request is clear enough, proceed without asking. Use judgment.

---

## Step 2: Build the Query Set

Construct **5–8 targeted Perplexity queries** designed to surface Reddit threads with high
emotional language and specific complaints. Use a mix of:

### Query Patterns (adapt to topic)

| Intent | Query Template |
|--------|----------------|
| Core complaints | `site:reddit.com [topic] "hate" OR "frustrated" OR "annoying"` |
| Consistency/habit failures | `site:reddit.com [topic] "stopped" OR "gave up" OR "don't bother"` |
| Skepticism | `site:reddit.com [topic] "waste of money" OR "doesn't work" OR "scam"` |
| Comparison pain | `site:reddit.com [topic] vs [alternative] complaints` |
| Positive framing (to find negatives) | `site:reddit.com [topic] "finally found" OR "only thing that worked"` — reveals what failed before |
| Desired outcome | `site:reddit.com [topic] "wish" OR "if only" OR "would be perfect if"` |
| Subreddit-specific | `subreddit:r/[relevant_sub] [topic] problems` |

---

## Step 3: Run Perplexity Queries

Use the Perplexity API with the `sonar` model. Run each query and collect raw results.

### API Call Pattern

```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [
      {
        "role": "system",
        "content": "You are a research assistant. Your job is to find EXACT quotes and language that real people use on Reddit when discussing problems, frustrations, or complaints. Do not paraphrase. Return direct quotes with thread context (subreddit, approximate upvotes if available). Prioritize emotionally charged language, vivid descriptions of pain, and specific phrases people use to describe their problems. At the end of each response, list the subreddit names you found most relevant as a JSON array like: {\"subreddits\": [\"supplement\", \"Nootropics\", \"xxfitness\"]}"
      },
      {
        "role": "user",
        "content": "[INSERT QUERY HERE]"
      }
    ],
    "search_domain_filter": ["reddit.com"],
    "return_citations": true,
    "search_recency_filter": "month"
  }'
```

**Parameters to use:**
- `model`: `sonar` (best for search-grounded responses)
- `search_domain_filter`: `["reddit.com"]` — locks results to Reddit only
- `return_citations`: `true` — keeps sources traceable
- `search_recency_filter`: `"month"` for trending issues; `"year"` for broader coverage

**After all queries run:**
- Collect all raw quotes and initial insights from Perplexity
- Compile the unique subreddits mentioned across all responses into a deduplicated list
- This list becomes the input for Step 3.5

---

## Step 3.5: Pull Live Reddit Data via Apify

Using the subreddits identified by Perplexity in Step 3, run the Apify Reddit Scraper
Lite to pull raw posts and comments directly. This gives unfiltered, live data that
Perplexity may have missed or summarized.

### For each subreddit identified (up to 5 most relevant):

**Step A — Start the scraper run**

```bash
curl -X POST "https://api.apify.com/v2/acts/trudax~reddit-scraper-lite/runs?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startUrls": [
      { "url": "https://www.reddit.com/r/[SUBREDDIT]/search/?q=[KEYWORD]&sort=top&t=year" }
    ],
    "maxItems": 100,
    "proxy": { "useApifyProxy": true }
  }'
```

Replace `[SUBREDDIT]` with each subreddit from Step 3 and `[KEYWORD]` with the core
research topic (URL-encoded). Use `sort=top&t=year` to surface highest-signal posts.

Save the `defaultDatasetId` value from the response JSON — you'll need it in the next call.

**Step B — Wait, then fetch results**

Wait 20–30 seconds for the run to complete, then:

```bash
curl "https://api.apify.com/v2/datasets/[defaultDatasetId]/items?token=$APIFY_API_TOKEN"
```

**Step C — Extract the right fields**

From each result item, extract:

| Field | What it contains | Priority |
|-------|-----------------|----------|
| `title` | Post headline | High — good for hook angles |
| `text` or `body` | Post body text | High — rich pain language |
| `score` | Upvote count | Use as signal strength filter |
| `comments` | Array of comment objects | Highest — most verbatim language lives here |
| `url` | Thread permalink | Keep for source attribution |

**Comment extraction logic:**
- For each post, iterate through `comments` array
- Extract `comment.text` (or `comment.body`) and `comment.score`
- Flag comments with `score > 20` as ⭐ copy-worthy candidates
- Skip: AutoModerator, deleted/removed content, mod posts, bots

**Priority filter:**
- Posts with `score > 50` — surface first
- Comments with `score > 20` — surface first
- Discard items with no text content

### Subreddit loop

Run Steps A–C for each subreddit. You do not need to wait for all runs to finish before
starting the next — start them sequentially and collect all `defaultDatasetId` values,
then fetch results in a second pass.

Label all extracted content with its source: `[Apify — r/subreddit]`

---

## Step 4: Extract and Categorize Pain Points

Combine all content from Perplexity (Step 3) and Apify (Step 3.5) and organize into
structured categories. Label each quote's source.

### Pain Point Categories

**1. Functional Failures**
> Things that literally don't work as expected  
> *"I've been taking it for 3 months and seen zero difference"*

**2. Experience Friction**
> The product works but using it is annoying  
> *"It clumps in cold liquid and I end up with chunks"*

**3. Trust & Skepticism**
> Doubt about claims, ingredients, or industry  
> *"How do I even know this is absorbed? Feels like expensive pee"*

**4. Habit/Consistency Failures**
> Product is fine but they can't stick with it  
> *"I buy it, take it for a week, then forget about it for two months"*

**5. Value Perception**
> Feels overpriced relative to perceived benefit  
> *"$60 a month for something I can't tell is doing anything"*

**6. Emotional/Identity Pain**
> How the problem makes them feel about themselves  
> *"I feel like I'm throwing money at aging and it doesn't care"*

**7. Desired Outcome (Stated)**
> What they actually want — often the flip side of the pain  
> *"I just want to know something is actually working"*

---

## Step 5: Pull Exact Customer Language

For each category, extract **verbatim quotes** — the actual words people typed.

Format each quote as:

```
"[Exact quote]"
— r/[subreddit] · [source: Perplexity or Apify] · score: [upvotes if available]
```

Flag especially copy-worthy phrases with ⭐

**What makes a quote copy-worthy:**
- Specific, visceral, not generic
- Contains a clear emotion (frustration, embarrassment, skepticism, hope)
- Uses language the target audience would recognize immediately
- Short enough to use in a headline or hook
- Reveals an insight about *why* the problem matters, not just *what* it is

---

## Step 6: Synthesize the Report

Deliver a structured report with these sections:

---

### RESEARCH REPORT: [Topic] — Reddit Pain Point Analysis

**Research Date**: [date]  
**Perplexity Queries Run**: [n]  
**Subreddits Scraped via Apify**: [list]  
**Total Quotes Collected**: [n]

---

#### 🔥 Top 5 Copy-Ready Insights
*The highest-leverage findings — each one is a potential headline, hook, or angle*

1. [Insight + supporting quote]
2. [Insight + supporting quote]
3. [Insight + supporting quote]
4. [Insight + supporting quote]
5. [Insight + supporting quote]

---

#### 💬 Exact Customer Language (Swipe File)
*Direct quotes organized by theme — use these verbatim or near-verbatim*

**[Category 1: e.g., Habit Failure]**
- ⭐ "quote" — r/subreddit [Apify · score: 847]
- "quote" — r/subreddit [Perplexity]

**[Category 2: e.g., Skepticism]**
- "quote" — r/subreddit [Apify · score: 312]
- ⭐ "quote" — r/subreddit [Perplexity]

*(continue per category)*

---

#### 🎯 Pain Point Summary
*Synthesized understanding of the core problem — 3–5 sentences max*

---

#### 📣 Suggested Copy Angles
*Derived from the research — each angle is a potential ad concept or LP frame*

1. **Angle name**: Brief description of the concept + example headline
2. **Angle name**: Brief description + example headline
3. **Angle name**: Brief description + example headline

---

#### 📎 Source Threads
*Notable Reddit threads found — for deeper reading*

- [Thread title / URL]

---

## Step 7: Optional — Run a Secondary Broad Search

If Reddit results are thin (niche topic, emerging category), run 2–3 additional Perplexity
queries **without** the `search_domain_filter` to capture:
- Review sites (Trustpilot, Amazon, G2)
- Forum discussions outside Reddit
- Blog comments

Label these clearly as "non-Reddit sources" in the output.

---

## Quality Checks Before Delivering

- [ ] At least 15–20 distinct verbatim quotes collected (combined Perplexity + Apify)
- [ ] At least 5 quotes sourced directly from Apify live scrape (highest signal)
- [ ] At least 3 pain point categories populated
- [ ] Apify quotes are filtered by score — no low-signal noise
- [ ] Copy angles are specific, not generic
- [ ] Quotes are real-sounding, not AI-paraphrased
- [ ] Top 5 insights section is punchy and immediately usable
- [ ] All quotes labeled with source (Perplexity vs Apify) and subreddit

---

## Notes for Claude Code

- `$PERPLEXITY_API_KEY` and `$APIFY_API_TOKEN` are available in the environment
- Default Perplexity model: `sonar`; use `sonar-pro` if the user wants deeper results
- Run Perplexity queries sequentially if parallel execution causes rate limit issues
- Apify runs are async — start all runs first, collect dataset IDs, then fetch results
- If the Apify run hasn't completed after 30s, retry the fetch after another 15s
- If a subreddit returns < 10 results, widen the keyword or try a related subreddit
- The actor field names may be `text`, `body`, or `selftext` depending on post type — check the first result and adapt
- If a query returns no Reddit results from Perplexity, widen it (remove `site:reddit.com`, add broader terms)
- Final output can be written to a `.md` file for easy sharing or import into Notion