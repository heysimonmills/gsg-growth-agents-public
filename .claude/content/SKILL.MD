---
name: simon-linkedin-writer
description: >
  Use this skill whenever Simon wants to write a LinkedIn post, create content for
  LinkedIn, repurpose content to Twitter/X, or adapt existing posts for social media.
  Triggers include: "write a LinkedIn post about X", "turn this into a LinkedIn post",
  "write a post about X", "I want to post about X", "repurpose this for LinkedIn",
  "write a thread about X", "make a tweet about X", or any request to create
  founder/marketing/entrepreneurship content for social media. Always use this skill
  for social content — do not write LinkedIn or Twitter posts without consulting it first,
  even for simple topics. The skill contains Simon's voice examples and must be used
  to match his tone and hook style.
---

# Simon Mills — LinkedIn Writer + Twitter Repurposer

Writes LinkedIn posts in Simon's exact voice, with heavy attention to the hook. Then
automatically produces a Twitter/X single tweet and thread version of each post.

---

## Directory Structure

```
simon-linkedin-writer/
├── SKILL.md                  ← this file
├── examples/
│   ├── posts-source.pdf      ← original PDF with 32 posts (source of truth)
│   ├── posts.md              ← extracted plain text posts (generated from PDF)
│   └── hooks.md              ← extracted hook patterns (auto-generated, update periodically)
└── references/
    └── voice-guide.md        ← distilled voice rules (generated from examples)
```

**Always read `examples/posts.md` before writing any post.** If `references/voice-guide.md`
exists, read it too — it's a distilled cheat sheet. If it doesn't exist yet, generate it
after reading the examples (see Step 1).

---

## Step 1: Load Voice Reference

Read `examples/posts.md` in full. Then extract and internalize:

### What to look for in the examples

**Hook patterns** — How does Simon open posts?
- Does he open with a bold statement, a counter-intuitive claim, a number, a question, a story beat?
- What's the average hook length (words before first line break)?
- Does he use "I" statements, "we" statements, or third-person observations?
- Are hooks conversational or declarative?

**Structural patterns** — How are posts built?
- Single idea, expanded? Story → insight? List format? Contrarian take → evidence?
- How long are paragraphs? (Line breaks after 1–2 sentences, or longer blocks?)
- Does he use bullet points, numbered lists, or prose?
- Where does the payoff land — middle, end, or distributed?

**Voice markers** — What makes it sound like Simon?
- Vocabulary choices (what words repeat? what words are never used?)
- Level of formality (casual? precise? both?)
- Does he hedge or state things directly?
- Humor style — dry, self-deprecating, observational?
- How does he reference personal experience vs. general insight?

**Endings** — How do posts close?
- CTA? Reflective statement? Question to audience? Punchy one-liner?
- Does he ask for engagement explicitly?

If `references/voice-guide.md` doesn't exist, create it now with your findings using
this format:

```markdown
# Simon's Voice Guide (auto-generated)

## Hook Patterns
[patterns observed]

## Structure
[structure observations]

## Voice Markers
[vocabulary, tone, style notes]

## Endings
[closing patterns]

## What to Avoid
[anything that appears 0 times in his examples — generic LinkedIn phrases, etc.]
```

Save it to `references/voice-guide.md` for future speed.

---

## Step 2: Understand the Brief

Before writing, confirm (or infer from context):

| Parameter | What to determine |
|-----------|------------------|
| **Topic** | What is the post about? |
| **Core insight** | What's the one thing the reader should walk away with? |
| **Personal angle** | Is there a personal story, experience, or Simon-specific angle? |
| **Audience** | Who is this for? (Founders, marketers, CPG/DTC, general?) |
| **Tone target** | Story-driven? Tactical/listicle? Contrarian take? Motivational? |
| **Twitter format** | Single tweet by default. Write a thread only if explicitly asked. |

If the user's prompt is thin (e.g., "write a post about collagen"), ask for the core
insight or personal angle before writing. A post with no specific POV will be generic.

If the prompt is rich enough, proceed without asking.

---

## Step 3: Write the LinkedIn Post

### The Hook — Treat This as the Whole Job

The hook is the first 1–3 lines before the "see more" cutoff. It determines whether
the post gets read. Spend disproportionate effort here.

**Hook writing process:**
1. Write 3–5 hook options by combining two inputs:
   - **Simon's observed patterns** — what structures/tones appear in his examples
   - **LinkedIn best practice knowledge** — high-performing hook frameworks (see below)
2. Score each against: (a) would stop the scroll? (b) sounds like Simon? (c) creates tension/curiosity without being clickbait?
3. Select the best one and build the post from it

**High-performing LinkedIn hook frameworks** (apply these in Simon's voice):

| Framework | Example structure |
|-----------|------------------|
| **The Contrarian** | "[Widely believed thing] is wrong." |
| **The Specific Number** | "I spent $47,000 on ads last quarter. Here's what actually worked." |
| **The Uncomfortable Truth** | "Most [founders/marketers/etc.] do X. It's why they fail at Y." |
| **The Pattern Interrupt** | Opens with something unexpected — a failure, a weird fact, a reversal |
| **The Story Beat** | One sentence that drops you into the middle of a moment: "It was 11pm and our CAC had just tripled." |
| **The Direct Insight** | Lead with the conclusion, let the post prove it: "Consistency is a system problem, not a willpower problem." |
| **The Stakes Frame** | "The difference between X and Y isn't [what people think]. It's [the real thing]." |
| **The Relatable Moment** | A specific, named situation the audience has been in — creates instant "that's me" recognition |

**Rules for hooks regardless of framework:**
- First line must work completely on its own — it's all most people will read
- Avoid punctuation that screams "LinkedIn post" (no "…" cliff-hangers as a crutch)
- Specificity > generality always. "34%" beats "significant growth"
- The hook should create a question in the reader's mind that only the post can answer

**Hook anti-patterns to avoid:**
- "I'm excited to share..."
- "Hot take:"
- Rhetorical questions that don't land ("Have you ever wondered...?")
- Starting with a humble brag without substance
- Generic inspirational openers
- Overused openers: "Unpopular opinion:", "Let's talk about X.", "This is your reminder to..."

### Post Body

Follow the structural pattern most common in Simon's examples. General principles:

- **Short paragraphs.** 1–2 sentences, then line break. LinkedIn punishes walls of text.
- **One idea per post.** Resist the urge to say everything. One sharp insight > three blunt ones.
- **Specific over general.** "Our CAC dropped 34% in 6 weeks" > "our results improved significantly"
- **Show, don't tell.** If the claim is "focus matters", show a moment where lack of focus cost something real.
- **Earn the insight.** Ground it in experience, data, or story before stating the conclusion.

### Closing

Match Simon's closing pattern from examples. If he tends to:
- Ask a question → close with a genuine question to the reader
- Drop a one-liner → write a punchy final line
- Soft CTA → suggest an action without being pushy

### Length

Match the median post length from the examples. Do not write longer posts than Simon
typically writes unless the topic genuinely demands it.

---

## Step 4: Produce Twitter/X Version

After the LinkedIn post, automatically produce a single tweet. Write a thread only if
Simon explicitly requests it.

### Default — Single Tweet

Condense the entire post into one tweet (≤280 characters).

Rules:
- Must contain the core insight, not just the topic
- Reads as a standalone thought — not a teaser or summary blurb
- Matches Simon's voice: direct, no filler, no corporate-speak
- No "🧵" or thread language
- Punchy, not truncated — if you can't fit the insight cleanly, reframe it

### Optional — Thread (only if requested)

Convert the LinkedIn post into a Twitter thread (typically 4–8 tweets).

Thread structure:
- **Tweet 1 (Hook)**: Strong enough to stand alone AND pull someone into the rest
- **Tweets 2–N (Body)**: Each tweet = one idea. No tweet should require the previous one to make sense.
- **Final tweet**: The sharpest line. Payoff or soft CTA.

Numbering: Use `1/`, `2/` etc. at the end of each tweet if the thread is 5+.

---

## Step 5: Deliver the Output

Format the final output exactly like this every time:

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN POST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Full LinkedIn post here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TWEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Single tweet here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOOK ALTERNATES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In case the hook doesn't land, here are 2 alternates:

A) [alternate hook]
B) [alternate hook]
```

---

## Iteration Protocol

If Simon asks to revise:
- "Make the hook stronger" → rewrite hook only, offer 3 options
- "More personal" → add a specific story beat or first-person experience
- "Shorter" → cut body, preserve hook and closing
- "Less listy" → convert bullets to prose
- "More punchy" → tighten every sentence, remove hedging language, cut last 20%
- "Different angle" → reframe the core insight, rebuild from scratch

Do not ask clarifying questions during iteration — just execute the direction and deliver.

---

## What to Never Write (Voice Anti-Patterns)

Unless explicitly observed in Simon's examples:

- ❌ "Excited to announce..."
- ❌ "Grateful for..."
- ❌ "In today's fast-paced world..."
- ❌ "Let that sink in."
- ❌ Excessive emoji
- ❌ "Drop a 🔥 if you agree"
- ❌ Posts that are secretly just humble brags
- ❌ Vague inspirational language with no grounded insight
- ❌ Starting every bullet with a verb in the same tense (listicle fatigue)
- ❌ Hedging phrases: "might", "could potentially", "in some cases"

---

## File Setup Instructions

Simon's 32 post examples live in `examples/posts-source.pdf`.

**First-time setup:**
1. Place the PDF in `examples/posts-source.pdf`
2. Run: *"Extract my LinkedIn posts from the PDF and generate the voice guide."*
   Claude Code will:
   - Read the PDF and extract all posts into `examples/posts.md` (plain text, separated by `---`)
   - Analyze the posts and write `references/voice-guide.md`
3. All future post requests use `posts.md` + `voice-guide.md` directly (no need to re-read the PDF each time)

**Adding new posts over time:**
Append directly to `examples/posts.md` separated by `---`. Delete `references/voice-guide.md`
every 5–10 additions so it regenerates with the fuller sample.

**Threshold for reliable voice matching:** ~10 posts. Below that, output is a good
starting point but will need more iteration.