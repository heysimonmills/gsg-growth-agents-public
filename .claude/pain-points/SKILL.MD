---
name: perplexity-pain-research
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
the Perplexity API. Output is structured for direct use in ad copy, landing page copy,
email, and creative strategy.

---

## Overview

The goal is not summarized insights — it's **raw, exact customer language** pulled from
real Reddit threads. The output should feel like a swipe file a copywriter would kill for:
real words, real frustration, real desire.

**Primary source**: Reddit (via Perplexity `sonar` model with focused Reddit queries)  
**Secondary source**: Perplexity web search (for broader VOC when Reddit is thin)  
**Output**: Structured pain point report with copy-ready language

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
|--------|---------------|
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
        "content": "You are a research assistant. Your job is to find EXACT quotes and language that real people use on Reddit when discussing problems, frustrations, or complaints. Do not paraphrase. Return direct quotes with thread context (subreddit, approximate upvotes if available). Prioritize emotionally charged language, vivid descriptions of pain, and specific phrases people use to describe their problems."
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

Run all 5–8 queries. Save raw outputs before synthesizing.

---

## Step 4: Extract and Categorize Pain Points

After collecting raw results, process them into structured categories.

### Pain Point Categories

Organize findings into these buckets (use only what applies):

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
— r/[subreddit], [approximate context]
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
**Queries Run**: [n]  
**Sources**: Reddit (via Perplexity)

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
- ⭐ "quote" — r/subreddit
- "quote" — r/subreddit

**[Category 2: e.g., Skepticism]**
- "quote" — r/subreddit
- ⭐ "quote" — r/subreddit

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

- [Thread title / URL if available]

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

- [ ] At least 15–20 distinct verbatim quotes collected
- [ ] At least 3 pain point categories populated
- [ ] Copy angles are specific, not generic ("collagen that you'll actually take" not "convenient supplement")
- [ ] Quotes are real-sounding, not AI-paraphrased
- [ ] Top 5 insights section is punchy and immediately usable
- [ ] Citations/sources noted for at least the best quotes

---

## Notes for Claude Code

- The Perplexity API key is available as `$PERPLEXITY_API_KEY` in the environment
- Default to `sonar` model; use `sonar-pro` if the user wants deeper/longer results
- Run queries sequentially if parallel execution causes rate limit issues
- If a query returns no Reddit results, widen it (remove `site:reddit.com`, add broader terms)
- The user may want to iterate — offer to run additional queries on sub-themes that emerge
- Final output can be written to a `.md` file for easy sharing or import into Notion