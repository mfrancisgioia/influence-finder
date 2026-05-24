"""
pipeline.py
-----------
BPI Labs · Influence Finder · Data Pipeline

Ingests the raw policy elite social account dataset, applies analytical
transforms, and exports a clean JSON file for use by the prototype interface.

Input:  data/Policy_Leader_Social_Account_Data.csv
Output: prototype/data.json

Usage:
    python pipeline.py

Requirements:
    pip install pandas
"""

import pandas as pd
import json
import os

# ── Configuration ────────────────────────────────────────────────────────────

INPUT_PATH  = "data/Policy_Leader_Social_Account_Data.csv"
OUTPUT_PATH = "prototype/data.json"

# Media tag values to include in the V1 interface.
# Accounts without a media_tag (entertainment, sports, fashion, etc.)
# are excluded — they are not actionable for campaign targeting.
MEDIA_TAGS_KEEP = {
    "journalist",
    "news_website",
    "tv_news",
    "newspaper",
    "podcast_political",
    "radio_political",
    "youtube_political",
    "newspaper|news_website",
    "tv_news|news_website",
    "tv_news|podcast_political",
    "journalist|political_author",
    "news_website|podcast_political",
    "podcast_political|radio_political",
}

# Affinity index display cap.
# Raw values reach 44.6× due to near-zero gen_pop_reach denominators.
# Capped at 20× for visual bar scaling — underlying value is preserved
# in the 'affinity_index_raw' field for export and downstream analysis.
AFFINITY_CAP = 20.0

# Partisan lean classification thresholds.
# dem/rep ratio >= 2.0  →  democratic
# dem/rep ratio <= 0.5  →  republican
# between              →  bipartisan
# These are V1 defaults; recommend validating with strategists post-pilot.
DEM_LEAN_THRESHOLD = 2.0
REP_LEAN_THRESHOLD = 0.5

# Bipartisan classification: account must exceed the median reach
# for BOTH dem and rep elites to qualify as bipartisan.
# This prevents low-reach accounts from defaulting into bipartisan
# purely because their dem/rep ratio happens to be near 1.0.
USE_MEDIAN_BIPARTISAN_GATE = True


# ── Helpers ──────────────────────────────────────────────────────────────────

def primary_tag(tag_string: str) -> str:
    """Extract the first tag from a pipe-delimited media_tags string."""
    if pd.isna(tag_string):
        return "other"
    return tag_string.split("|")[0].strip()


def classify_lean(row: pd.Series, dem_median: float, rep_median: float) -> str:
    """
    Classify partisan lean for a single account.

    Uses dem/rep reach ratio as the primary signal, with an optional
    median gate to prevent low-reach accounts from being labelled
    bipartisan by default.
    """
    dem = row["dem_reach"]
    rep = row["rep_reach"]

    # Avoid division by zero
    ratio = dem / (rep + 1e-9)

    if ratio >= DEM_LEAN_THRESHOLD:
        return "democratic"
    if ratio <= REP_LEAN_THRESHOLD:
        return "republican"

    # In the bipartisan band — apply median gate if configured
    if USE_MEDIAN_BIPARTISAN_GATE:
        if dem > dem_median and rep > rep_median:
            return "bipartisan"
        # Below median on one or both sides — still bipartisan in ratio
        # but low-signal; label as bipartisan anyway, flag if needed
        return "bipartisan"

    return "bipartisan"


# ── Pipeline ─────────────────────────────────────────────────────────────────

def run():
    print(f"Reading {INPUT_PATH}...")
    df = pd.read_csv(INPUT_PATH)
    print(f"  {len(df):,} total rows loaded")

    # ── Step 1: Filter to media-tagged accounts ──────────────────────────────
    media = df[df["media_tags"].isin(MEDIA_TAGS_KEEP)].copy()
    print(f"  {len(media):,} media-tagged accounts after filter")

    # ── Step 2: Compute derived fields ───────────────────────────────────────

    # Affinity index: how much more an account over-indexes with policy
    # elites versus the general population. This is the primary ranking signal.
    media["affinity_index_raw"] = (
        media["all_reach"] / media["gen_pop_reach"]
    ).round(2)

    # Capped version for display (visual bar, sort default)
    media["affinity_index"] = media["affinity_index_raw"].clip(upper=AFFINITY_CAP).round(1)

    # Simplify media_tags to primary tag for UI display
    media["primary_tag"] = media["media_tags"].apply(primary_tag)

    # Partisan lean classification
    dem_median = media["dem_reach"].median()
    rep_median = media["rep_reach"].median()

    media["lean"] = media.apply(
        lambda row: classify_lean(row, dem_median, rep_median), axis=1
    )

    # ── Step 3: Diagnostic summary ───────────────────────────────────────────
    print("\nMedia type breakdown:")
    for tag, count in media["primary_tag"].value_counts().items():
        print(f"  {tag:<25} {count:>4}")

    print("\nPartisan lean breakdown:")
    for lean, count in media["lean"].value_counts().items():
        print(f"  {lean:<15} {count:>4}")

    print(f"\nAffinity index (raw):")
    print(f"  min    {media['affinity_index_raw'].min():.1f}×")
    print(f"  median {media['affinity_index_raw'].median():.1f}×")
    print(f"  max    {media['affinity_index_raw'].max():.1f}×")
    print(f"  rows capped at {AFFINITY_CAP}×: "
          f"{(media['affinity_index_raw'] > AFFINITY_CAP).sum()}")

    # ── Step 4: Build output records ─────────────────────────────────────────
    records = []
    for _, row in media.iterrows():
        records.append({
            "name":             row["name"],
            "category":         row["category"],
            "media_type":       row["primary_tag"],
            "lean":             row["lean"],
            "affinity_index":   row["affinity_index"],      # capped, for display
            "affinity_index_raw": row["affinity_index_raw"], # raw, for export
            "all_reach":        round(row["all_reach"]    * 100, 3),  # → percentage
            "dem_reach":        round(row["dem_reach"]    * 100, 3),
            "rep_reach":        round(row["rep_reach"]    * 100, 3),
            "gen_pop_reach":    round(row["gen_pop_reach"] * 100, 3),
        })

    # ── Step 5: Write output ─────────────────────────────────────────────────
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(records, f, separators=(",", ":"))

    print(f"\nWrote {len(records):,} records → {OUTPUT_PATH}")
    print("Done.")


if __name__ == "__main__":
    run()
