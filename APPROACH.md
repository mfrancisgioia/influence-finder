# My Approach

## 1. Tech Stack & AI Collaboration:
* **Models:** Claude Sonnet 4.6 / Gemini 3.1 Pro (Used for A/B evaluation across data exploration, script generation, and text synthesis)
* **Applications:** Data parsing, Python + HTML/JS prototype construction, and brief scaffolding.

There are two distinct pieces of source code behind the prototype:
* A Python script that ingested the raw CSV, computed the affinity index, classified partisan lean, filtered to media-tagged accounts, and exported the clean JSON that powers the tool
* The HTML/JS prototype itself — which is the interface, but also is the source in the sense that all the logic lives in it
---

## 2. Finding the Signal in the Sample Data

Before writing code or opening a product document, I spent time querying the dataset to evaluate what was actually there. 

The straightforward approach to an audience dataset like this is to build a basic leaderboard: rank the 11,560 accounts by raw `all_reach`, slap on some category filters, and call it an MVP. 

However, examining the relationship among the four reach vectors (`gen_pop_reach`, `all_reach`, `dem_reach`, `rep_reach`) revealed a much better product hook. The delta between elite reach and general population reach is highly non-linear. Some accounts with near-zero mass-market presence have massive footprint density among policy elites. Conversely, some household-name celebrities have massive general numbers but low tenant-level engagement with insiders. 

Pulling raw reach numbers gives a strategist a generic list they could have guessed themselves. Finding the *disproportionate* weight is where the proprietary BPI value sits. 

**The Product Decision:** I built the core ranking engine around a calculated metric I'm calling the **Affinity Index**:

elite reach divided by general population reach

The tool surfaces and ranks accounts based on their concentration of elite influence, not just their raw popularity.

---

## 3. Defining the Core Interaction

The data can support a dozen features—search bars, audience comparison matrices, or historical tracking dashboards. But I forced myself to anchor on the actual user: an early-career strategist who needs to build a defensible media list on a tight deadline. 

They don't need a playground to explore data; they need a validated shortlist they can confidently hand to a client.

**The Product Decision:** The MVP has exactly one primary workflow. The strategist sets their target audience parameters (media tags and partisan slant), reviews a mathematically ranked matrix, and exports the list to a pitch format. I intentionally left out saved searches, automated client-facing rationales, and multi-audience uploads for V1. We need to validate whether strategists trust the core ranking before building downstream features.

---

## 4. Thorny Trade-offs & Unverified Assumptions

Because this was a rapid sprint, I had to make three specific scoping calls that I’d want to pressure-test with users immediately:

* **Partisan Lean Logic:** I classified accounts as Democratic-leaning if their Dem-to-Rep reach ratio was 2.0 or higher, Republican-leaning at 0.5 or below, and bipartisan anywhere in between. These boundaries feel intuitive, but they aren't empirically grounded yet. I'd want to sit with a strategist to see if these thresholds accurately reflect political realities on the ground.
* **The Denominator Problem:** A few hyper-niche accounts threw off massive affinity index scores — above 40 times — simply because their general population reach was effectively zero, making the math unstable. For V1, I capped the visible index at 20 times to keep the ranking clean, but the long-term fix requires a normalized or log-scaled scoring system.
* **Slicing the Data Noise:** I filtered the dataset down to the roughly 3,300 accounts containing explicit media tags — journalists, outlets, podcasts, and so on — removing the remaining 8,000+ untagged rows entirely. While this fits the immediate use case of media targeting, we may be leaving out highly influential activists or political authors who don't carry a traditional media tag. 

---

## 5. What I’d Address with More Time

The biggest functional gap in `Policy Leader Social Account Data.csv` is the lack of context. You can isolate "journalists," but you can't tell who covers healthcare policy versus defense or tech. For a real campaign, a generic journalist list is only half useful.

**The Next Sprint:** I’d design a lightweight data enrichment pipeline using an LLM. We could pass the names/handles of the top 500 ranked media targets, prompt the model to review their recent coverage or bio data, and return standardized "beat" or "topic" tags. 

I kept this out of the MVP because layering AI-generated classifications on top of unverified ranking metrics makes a product *almost* impossible to debug. We have to prove the math works before we automate the context.

---

## 6. Driving Outcomes in the First 30 Days

In a product role focused on internal tools, the biggest risk is shipping a polished "demo product"—something that looks great in a leadership review slide deck but gets completely abandoned by actual staff because it doesn't solve a real workflow bottleneck. 

My execution plan for the first 30 days wouldn't focus on engineering a final production UI. Instead, I’d take this exact Python-driven prototype, drop it in front of two or three strategists actively building live client pitches, and watch them use it. 

The goal isn't just to ship software; it's to find out if the data output gives them the confidence to stand in front of a client and defend the recommendation. That insight is what we build the actual roadmap on.

---

*Michael Gioia · mfrancisgioia@gmail.com · [linkedin.com/in/mfrancisgioia](https://www.linkedin.com/in/mfrancisgioia)*
