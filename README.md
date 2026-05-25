# README.md/influence-finder
### Director, Product (Labs) - Skills Assessment · May 2026

I'm Michael Gioia — a Senior Product Manager with a decade of experience building data integration and media technology products, currently interviewing for the Director, Product (Labs) role at BPI.

This repo is my submission to the Skills Assessment, and it's structured to demonstrate three things the role requires: the ability to think deeply about data, make product decisions under ambiguity, and ship something that drives a real outcome. The assessment material provided a dataset of 11,560 policy elite social accounts and asked me to identify the problem worth solving and build something that addressed it.

My thesis is that the most valuable signal in this data isn't raw reach; it's the ratio between how much an account over-indexes with policy elites versus the general population. That ratio, which I've called the affinity index, is what separates a recommendation a BPI strategist can defend to a client from a list they could have pulled themselves. Everything in this repo, from the data pipeline, the prototype, the product brief, and the approach document, is built around proving that thesis and showing what it would look like in practice.

---

## What's in here

| | |
|---|---|
| 🔵 **Live Prototype** | [Launch `influence_finder.html` →](https://mfrancisgioia.github.io/influence-finder/prototype/influence_finder.html) |
| 📄 **Product Brief** | [Read `influence_finder_product_brief.pdf`](brief/influence_finder_product_brief.pdf) |
| 📐 **Approach** | [Read `APPROACH.md`](APPROACH.md) |
| 🐍 **Data Pipeline** | [Download `pipeline.py`](pipeline.py) |

## Suggested reading order

1. **Open the `influence_finder.html` prototype** — spend 5 minutes with the live tool before reading anything
2. **Read the `influence_finder_product_brief.pdf`** — what I built, why, and what I deliberately left out
3. **Read `APPROACH.md`** — how I'd scale this into a repeatable practice and what the first 30 days would look like

---

## How this prototype was built

**Step 1 — Data pipeline (`pipeline.py`)**

A Python script ingests the raw CSV and applies three analytical transforms:

- Filters 11,560 accounts down to ~3,300 with media tags (journalists, outlets, TV news, print, podcasts) — the actionable subset for campaign targeting
- Computes the **affinity index** for each account: policy elite reach ÷ general population reach. This is the primary ranking signal — it surfaces who over-indexes with policy elites, not just who is big
- Classifies **partisan lean** (Democratic / Republican / Bipartisan) from the dem/rep reach ratio, with a median gate to prevent low-signal accounts from defaulting to bipartisan

To run the pipeline locally:

```bash
pip install pandas
python pipeline.py
# → writes prototype/data.json
```

**Step 2 — Prototype (`prototype/influence_finder.html`)**

A single-file HTML/JS interface built on the pipeline output. The full dataset is embedded directly in the file, so it runs in any browser with no server, no install, and no dependencies. Filter, rank, shortlist, and export — all client-side.

---

*Michael Gioia · mfrancisgioia@gmail.com · [linkedin.com/in/mfrancisgioia](https://www.linkedin.com/in/mfrancisgioia)*
