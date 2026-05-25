# My Approach
### BPI Labs · Director of Product Skills Assessment · May 2026

---

## 1. Tech Stack & AI Collaboration

* **Models:** Claude Sonnet 4.6 / Gemini 2.5 Pro (used for A/B evaluation across data exploration, script generation, and text synthesis)
* **Applications:** Data parsing, Python + HTML/JS prototype construction, and brief scaffolding

There are two distinct pieces of source code behind the prototype: (1) a Python script that ingested the raw CSV, computed the affinity index, classified partisan lean, filtered to media-tagged accounts, and exported the clean JSON that powers the tool and (2) the HTML/JS prototype itself — which is the interface, but also is the source in the sense that all the logic lives in it.

---

## 2. Working with AI vs. Shipping What the Model Gives You

The full repo — pipeline, prototype, product brief, and this document — was built over approximately 8–10 hours across several working sessions. That timeline matters because it reflects something worth naming directly: AI-assisted product work is not the same as AI-generated product work, and the difference shows up in the output.

The first draft of the affinity index framing came from a model prompt. So did the initial pipeline structure, the brief scaffold, and the prototype layout. None of those shipped as-is. Every output required interrogation — pushing back on the signal selection, questioning whether the media tag filter was a finding or an assumption, pressure-testing the partisan lean thresholds against what the data actually showed, and catching places where the model stated conclusions more confidently than the evidence warranted.

A few concrete examples of where that vetting mattered:

* The original brief scenario described "18 journalists who cover healthcare policy" — a claim the dataset cannot support because it has no beat or topic tags. Catching that before submission meant rewriting the scenario around what the data actually delivers rather than what sounds compelling.
* The first version of the APPROACH document read as a prescriptive framework — "here is how I would run your product organization." That register was wrong for a document meant to show thinking, not make promises. It took several rewrites to shift from declarative to reflective.
* The model initially proposed capping the affinity index at 20× as the denominator fix. After questioning that approach, the better solution emerged: a minimum general population reach qualifying gate applied before the index is computed, which eliminates the instability at the source rather than masking it in the display layer.

The most useful thing AI did in this process was accelerate the distance between a blank page and a working draft. The most important thing I did was refuse to let working drafts become final ones without earning it.

---

## 3. Finding the Signal in the Sample Data

Before writing code or opening a product document, I spent time querying the dataset to understand what was actually there — not what I assumed it contained.

The straightforward approach to an audience dataset like this is to build a basic leaderboard: rank the 11,560 accounts by raw `all_reach`, add some category filters, and call it an MVP.

However, examining the relationship among the four reach vectors (`gen_pop_reach`, `all_reach`, `dem_reach`, `rep_reach`) revealed a much better product hook. The delta between elite reach and general population reach is highly non-linear. Some accounts with near-zero mass-market presence have massive footprint density among policy elites. Conversely, some household-name accounts have large general numbers but minimal engagement with policy insiders.

Pulling raw reach numbers gives a strategist a generic list they could have guessed themselves. Finding the *disproportionate* weight is where the proprietary BPI value sits.

**The Product Decision:** I built the core ranking engine around a calculated metric I'm calling the **Affinity Index** — elite reach divided by general population reach. The tool surfaces and ranks accounts based on their concentration of elite influence, not just their raw popularity.

---

## 4. Defining the Core Interaction

The data can support a dozen features — search bars, audience comparison matrices, historical tracking dashboards. But I forced myself to anchor on the actual user: an early-career strategist who needs to build a defensible media list on a tight deadline.

They don't need a playground to explore data; they need a validated shortlist they can confidently hand to a client.

**The Product Decision:** The MVP has exactly one primary workflow. The strategist sets their target audience parameters (media tags and partisan lean), reviews a mathematically ranked list, and exports it to a pitch format. I intentionally left out saved searches, automated client-facing rationales, and multi-audience uploads for V1. We need to validate whether strategists trust the core ranking before building downstream features.

---

## 5. Thorny Trade-offs & Unverified Assumptions

Because this was a rapid sprint, I had to make several scoping calls that I'd want to pressure-test with users immediately:

* **Partisan Lean Logic:** I classified accounts as Democratic-leaning if their dem/rep reach ratio was 2.0 or higher, Republican-leaning at 0.5 or below, and bipartisan anywhere in between. These boundaries feel intuitive but they aren't empirically grounded yet. The way I'd resolve this in week one is a calibration session with two or three senior strategists, using a sample of 20 accounts with known partisan profiles as a test set. Their corrections define the validated thresholds — the goal is to ground the classification in field experience, not intuition.

* **The Denominator Problem:** A few hyper-niche accounts threw off massive affinity index scores — above 40 times — simply because their general population reach was effectively zero, making the math unstable. I capped the display at 20 times for V1, but the right fix isn't a display cap — it's a minimum reach qualifying gate applied before the index is computed at all. Accounts below roughly 5,000 general population followers produce mathematically unstable ratios and should be excluded from ranking entirely rather than masked after the fact. I'd implement that gate in the first engineering sprint and retire the cap alongside it.

* **Filtering to Media-Tagged Accounts:** I narrowed the dataset to the roughly 3,300 accounts carrying an explicit media tag — journalists, outlets, TV news, podcasts — and removed the remaining 8,000+ rows on the assumption that entertainment, sports, and lifestyle accounts weren't relevant to a campaign targeting workflow. That assumption wasn't grounded in anything the assessment materials actually said; the brief left scope entirely open. Influential voices without a traditional media tag — cultural figures with outsized policy elite reach, political authors, prominent activists — are invisible in the current tool even when they'd be genuinely valuable targets. And for brand or corporate campaigns, where BPI also operates, the calculus might be entirely different. The near-term fix is an LLM classification pass on the top 500 untagged accounts by raw reach to surface the most influential non-media voices without a full enrichment sprint. The long-term fix is making this a strategist-controlled toggle rather than a pipeline-level filter.

---

## 6. What I'd Address with More Time

The biggest functional gap in the dataset is the lack of topic context. You can isolate "journalists," but you can't tell who covers healthcare policy versus defense or tech. For a real campaign, a generic journalist list is only half useful.

**The Next Sprint:** I'd design a lightweight data enrichment pipeline using an LLM — pass the names and handles of the top 500 ranked media targets, prompt the model to review their recent coverage or bio data, and return standardized beat or topic tags.

I kept this out of the MVP because layering AI-generated classifications on top of unverified ranking metrics makes a product almost impossible to debug. We have to prove the math works before we automate the context.

---

## 7. Driving Outcomes in the First 30 Days

In a product role focused on internal tools, the biggest risk is shipping a polished demo product — something that looks great in a leadership review but gets abandoned by actual staff because it doesn't solve a real workflow bottleneck.

My execution plan for the first 30 days wouldn't focus on engineering a final production UI. Instead, I'd take this exact prototype, put it in front of two or three strategists actively building live client pitches, and watch them use it without coaching them on how.

The specific signal I'd be looking for: did the strategist feel confident enough in the ranked output to include it in a client-facing document without manually re-validating the list? That's the pass/fail test. If yes, the core ranking has earned trust and the next sprint is downstream features. If no, the problem is ranking explainability and that gets fixed before anything else gets built.

The goal isn't to ship software. It's to find out if the data output gives strategists the confidence to stand in front of a client and defend the recommendation. That insight is what the actual roadmap gets built on.

---

*Michael Gioia · mfrancisgioia@gmail.com · [linkedin.com/in/mfrancisgioia](https://www.linkedin.com/in/mfrancisgioia)*
