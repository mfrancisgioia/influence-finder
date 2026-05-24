# influence-finder
### Director, Product (Labs) - Skills Assessment · May 2026

This repo contains my full response to the Labs skills assessment — a product brief, a working prototype, and documentation on how I'd make this kind of work repeatable at BPI.

---

## What's in here

| | |
|---|---|
| 🔵 **Live Prototype** | [Launch Influence Finder →](https://mfrancisgioia.github.io/influence-finder/prototype/influence_finder.html) |
| 📄 **Product Brief** | [`influence_finder_product_brief.pdf`](brief/Influence_Finder_Product_Brief.docx) |
| 📐 **Approach** | [`APPROACH.md`](APPROACH.md) |
| 🐍 **Data Pipeline** | [`pipeline.py`](pipeline.py) |
| 🛠️ **Prototype Source** | [`prototype/influence_finder.html`](prototype/influence_finder.html) |

---

## Repo structure

```
influence-finder/
├── README.md
├── APPROACH.md
├── pipeline.py                        ← data pipeline: CSV → JSON
├── prototype/
│   ├── influence_finder.html          ← self-contained prototype (data embedded)
└── brief/
    └── influence_finder_product_brief.pdf
```

---

## How this was built

**Step 1 — Data pipeline (`pipeline.py`)**

A Python script ingests the raw CSV and applies three analytical transforms:

- Filters 11,560 accounts down to the ~3,300 with media tags (journalists, outlets, TV news, print, podcasts) — the actionable subset for campaign targeting
- Computes the **affinity index** for each account: policy elite reach ÷ general population reach. This is the primary ranking signal — it surfaces who over-indexes with policy elites, not just who is big
- Classifies **partisan lean** (Democratic / Republican / Bipartisan) from the dem/rep reach ratio, with a median gate to prevent low-signal accounts from defaulting to bipartisan

To run the pipeline locally:

```bash
pip install pandas
python pipeline.py
# → writes prototype/data.json
```

**Step 2 — Prototype (`prototype/influence_finder.html`)**

A single-file HTML/JS interface built on the pipeline output. The full dataset is embedded directly in the file so it runs in any browser with no server, no install, and no dependencies. Filter, rank, shortlist, and export — all client-side.

---

## Suggested reading order

1. **Open the prototype** — spend 5 minutes with the live tool before reading anything
2. **Read the product brief** — what I built, why, and what I deliberately left out
3. **Read `APPROACH.md`** — how I'd scale this into a repeatable practice and what the first 30 days would look like

---

*Michael Gioia · mfrancisgioia@gmail.com · [linkedin.com/in/mfrancisgioia](https://www.linkedin.com/in/mfrancisgioia)*
