"""
prepare_data.py — turns the raw downloads into the small, tidy files the charts read.

Run from the project folder:
    python scripts/prepare_data.py

Inputs (data/raw/):
    chocolate_ratings.csv        Flavors of Cacao export (newest available). Falls back to the
                                 2021 copy if the new export is not there yet.
    fao_cocoa_production.csv     FAOSTAT download: Crops and livestock products, Element
                                 "Production", Item "Cocoa beans", all countries (optional).
    countries-110m.json          World map shapes (world-atlas 2.0.2, from Natural Earth).
    centroids_110m.csv           Centre point of each country (made once with d3-geo).

Outputs (data/processed/):
    chocolate.csv                One row per bar, with standard country names, ISO codes,
                                 regions, rating bands, cocoa bands and recipe flags.
    tasting_words.csv            One row per (bar, memorable word), for the word chart.
    world-110m.json              Map shapes with an ISO alpha-3 code on every country.
    country_points.csv           Centre point (lon/lat) for every country we need to plot.
    fao_cocoa_production.csv     Cocoa bean production in tonnes by country and year.
    bean_country_summary.csv     Number of bars and average rating per bean country.

Only light cleaning is done: renaming countries to one standard name and grouping
values into bands. No ratings or production figures are changed.
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd
import pycountry

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Country names -> one standard name + ISO alpha-3 code
# ---------------------------------------------------------------------------
# Names in the chocolate data that a plain lookup cannot match.
# Regions (Sulawesi, Trinidad, Scotland...) are mapped to the country they belong to.
OVERRIDES = {
    "Blend": None,
    "Burma": "MMR", "Myanmar": "MMR",
    "Congo": "COG", "Republic of Congo": "COG",
    "DR Congo": "COD", "D.R. Congo": "COD", "Democratic Republic of the Congo": "COD",
    "Ivory Coast": "CIV", "Cote d'Ivoire": "CIV", "Côte d'Ivoire": "CIV",
    "Principe": "STP", "Sao Tome": "STP", "Sao Tome & Principe": "STP", "Sao Tome and Principe": "STP",
    "Sulawesi": "IDN", "Sumatra": "IDN", "Bali": "IDN", "Java": "IDN",
    "Trinidad": "TTO", "Tobago": "TTO", "Trinidad & Tobago": "TTO", "Trinidad and Tobago": "TTO",
    "U.S.A.": "USA", "USA": "USA", "Hawaii": "USA",
    "St. Lucia": "LCA", "St.Lucia": "LCA", "Saint Lucia": "LCA",
    "St.Vincent-Grenadines": "VCT", "St. Vincent-Grenadines": "VCT", "St. Vincent": "VCT",
    "Taiwan": "TWN", "Tanzania": "TZA", "Bolivia": "BOL", "Venezuela": "VEN", "Vietnam": "VNM",
    "Russia": "RUS", "South Korea": "KOR", "Czech Republic": "CZE", "Czechia": "CZE",
    "U.K.": "GBR", "UK": "GBR", "Scotland": "GBR", "Wales": "GBR", "England": "GBR", "Northern Ireland": "GBR",
    "U.A.E.": "ARE", "UAE": "ARE", "Amsterdam": "NLD", "Netherlands": "NLD",
    "Martinique": "MTQ", "Puerto Rico": "PRI", "Turkey": "TUR",
    # Names used in the 2026 export
    "France (Martinique)": "MTQ", "France (Reunion)": "REU", "U.S.A. (Puerto Rico)": "PRI",
    "Nicaraqua": "NIC",   # spelling mistake in the source
}
# Short, familiar display names for an Australian audience.
DISPLAY = {
    "MMR": "Myanmar", "COG": "Congo", "COD": "DR Congo", "CIV": "Côte d'Ivoire",
    "STP": "São Tomé and Príncipe", "TTO": "Trinidad and Tobago", "USA": "United States",
    "GBR": "United Kingdom", "LCA": "St Lucia", "VCT": "St Vincent and the Grenadines",
    "TWN": "Taiwan", "TZA": "Tanzania", "BOL": "Bolivia", "VEN": "Venezuela", "VNM": "Vietnam",
    "RUS": "Russia", "KOR": "South Korea", "CZE": "Czechia", "ARE": "United Arab Emirates",
    "NLD": "Netherlands",
}
CENTRAL_AM_CARIB = {"BLZ", "CRI", "CUB", "DOM", "SLV", "GRD", "GTM", "HTI", "HND", "JAM", "MTQ",
                    "NIC", "PAN", "PRI", "LCA", "VCT", "TTO", "DMA", "BHS", "BRB", "ATG", "KNA"}
CONTINENT = {"AF": "Africa", "AS": "Asia", "EU": "Europe", "NA": "North America",
             "SA": "South America", "OC": "Oceania"}

unmatched = set()


def to_iso3(name):
    if pd.isna(name):
        return None
    name = str(name).strip()
    if name in OVERRIDES:
        return OVERRIDES[name]
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        unmatched.add(name)
        return None


def display_name(iso3):
    if iso3 is None or pd.isna(iso3):
        return None
    if iso3 in DISPLAY:
        return DISPLAY[iso3]
    c = pycountry.countries.get(alpha_3=iso3)
    return getattr(c, "common_name", None) or c.name


def region(iso3):
    if iso3 is None or pd.isna(iso3):
        return None
    if iso3 in CENTRAL_AM_CARIB:
        return "Central America & Caribbean"
    import pycountry_convert as pc
    a2 = pycountry.countries.get(alpha_3=iso3).alpha_2
    try:
        return CONTINENT[pc.country_alpha2_to_continent_code(a2)]
    except KeyError:
        return "Other"


# ---------------------------------------------------------------------------
# 2. Load chocolate ratings (newest export if present)
# ---------------------------------------------------------------------------
def snake(col):
    return re.sub(r"[^a-z0-9]+", "_", col.lower()).strip("_")


new_file = RAW / "chocolate_ratings.csv"
old_file = RAW / "chocolate_ratings_2021_copy.csv"
src = new_file if new_file.exists() else old_file
if src is old_file:
    print("NOTE: using the 2021 copy. Put the newest export at data/raw/chocolate_ratings.csv and re-run.")
raw = pd.read_csv(src)
raw.columns = [snake(c) for c in raw.columns]
raw = raw.rename(columns={
    "company": "company_manufacturer", "manufacturer": "company_manufacturer",
    "broad_bean_origin": "country_of_bean_origin",
    "specific_bean_origin": "specific_bean_origin_or_bar_name",
})
need = ["ref", "company_manufacturer", "company_location", "review_date", "country_of_bean_origin",
        "specific_bean_origin_or_bar_name", "cocoa_percent", "ingredients",
        "most_memorable_characteristics", "rating"]
missing = [c for c in need if c not in raw.columns]
if missing:
    sys.exit(f"Missing columns in {src.name}: {missing}. Found: {list(raw.columns)}")

df = pd.DataFrame({
    "ref": raw["ref"].astype(int),
    "maker": raw["company_manufacturer"].astype(str).str.strip(),
    "maker_location_raw": raw["company_location"].astype(str).str.strip(),
    "review_year": pd.to_numeric(raw["review_date"], errors="coerce").astype("Int64"),
    "bean_origin_raw": raw["country_of_bean_origin"].astype(str).str.strip(),
    "bar_name": raw["specific_bean_origin_or_bar_name"].astype(str).str.strip(),
    "cocoa_pct": pd.to_numeric(raw["cocoa_percent"].astype(str).str.replace("%", ""), errors="coerce"),
    "ingredients_raw": raw["ingredients"],
    "characteristics": raw["most_memorable_characteristics"].astype(str).str.strip(),
    "rating": pd.to_numeric(raw["rating"], errors="coerce"),
})

df["maker_iso3"] = df["maker_location_raw"].map(to_iso3)
df["maker_country"] = df["maker_iso3"].map(display_name)
df["maker_region"] = df["maker_iso3"].map(region)
df["bean_iso3"] = df["bean_origin_raw"].map(to_iso3)
df["bean_country"] = df["bean_iso3"].map(display_name)
df.loc[df["bean_origin_raw"].eq("Blend"), "bean_country"] = "Blend (several countries)"
df["bean_region"] = df["bean_iso3"].map(region)
df.loc[df["bean_origin_raw"].eq("Blend"), "bean_region"] = "Blend"

# Rating bands = the official Flavors of Cacao scale
def rating_band(r):
    if r >= 4.0: return "Outstanding"
    if r >= 3.5: return "Highly recommended"
    if r >= 3.0: return "Recommended"
    if r >= 2.0: return "Disappointing"
    return "Unpleasant"
BAND_ORDER = ["Outstanding", "Highly recommended", "Recommended", "Disappointing", "Unpleasant"]
df["rating_band"] = df["rating"].map(rating_band)
df["rating_band_order"] = df["rating_band"].map(BAND_ORDER.index) + 1

# Cocoa bands (41% of bars are exactly 70%, so 70% gets its own band)
def cocoa_band(p):
    if pd.isna(p): return None
    if p < 65: return "Under 65%"
    if p < 70: return "65–69%"
    if p == 70: return "70%"
    if p < 75: return "71–74%"
    if p < 80: return "75–79%"
    return "80%+"
df["cocoa_band"] = df["cocoa_pct"].map(cocoa_band)

# Recipe: "4- B,S,C,L" -> flags and a readable label
CODES = [("B", "Beans"), ("S", "Sugar"), ("S*", "Other sweetener"), ("C", "Cocoa butter"),
         ("V", "Vanilla"), ("L", "Lecithin"), ("Sa", "Salt")]
def parse_ingredients(s):
    if pd.isna(s) or "-" not in str(s):
        return []
    return [p.strip() for p in str(s).split("-", 1)[1].split(",") if p.strip()]
parts = df["ingredients_raw"].map(parse_ingredients)
for code, label in CODES:
    df["has_" + label.lower().replace(" ", "_")] = parts.map(lambda p, c=code: int(c in p))
df["n_ingredients"] = parts.map(len)
df["recipe"] = parts.map(lambda p: " + ".join(lbl for c, lbl in CODES if c in p) if p else "Not listed")

cols = ["ref", "maker", "maker_country", "maker_iso3", "maker_region", "review_year",
        "bean_country", "bean_iso3", "bean_region", "bean_origin_raw", "bar_name",
        "cocoa_pct", "cocoa_band", "recipe", "n_ingredients"] + \
       [c for c in df.columns if c.startswith("has_")] + \
       ["characteristics", "rating", "rating_band", "rating_band_order"]
df[cols].sort_values("ref").to_csv(OUT / "chocolate.csv", index=False)

# Tasting words: one row per (bar, word)
words = df[["ref", "rating", "characteristics"]].copy()
words["word"] = words["characteristics"].str.lower().str.split(",")
words = words.explode("word")
words["word"] = words["word"].str.strip()
words = words[words["word"].str.len() > 0]
words[["ref", "word", "rating"]].to_csv(OUT / "tasting_words.csv", index=False)

# ---------------------------------------------------------------------------
# 3. Map shapes with ISO alpha-3 codes, and a centre point for each country
# ---------------------------------------------------------------------------
topo = json.loads((RAW / "countries-110m.json").read_text())
for g in topo["objects"]["countries"]["geometries"]:
    c = pycountry.countries.get(numeric=str(g.get("id", "")).zfill(3)) if g.get("id") else None
    g.setdefault("properties", {})["iso3"] = c.alpha_3 if c else None
(OUT / "world-110m.json").write_text(json.dumps(topo, separators=(",", ":")))

pts = pd.read_csv(RAW / "centroids_110m.csv", dtype={"iso_n3": str})
pts = pts.dropna(subset=["iso_n3"])
pts["iso3"] = pts["iso_n3"].map(lambda n: getattr(pycountry.countries.get(numeric=n.zfill(3)), "alpha_3", None))
pts = pts.dropna(subset=["iso3"])[["iso3", "lon", "lat"]]
# Small islands are missing from the low-detail map, so add their centre points by hand.
ISLANDS = pd.DataFrame([
    ("GRD", -61.68, 12.12), ("LCA", -60.98, 13.91), ("VCT", -61.20, 13.25), ("STP", 6.61, 0.19),
    ("MTQ", -61.02, 14.64), ("WSM", -172.10, -13.76), ("SGP", 103.82, 1.35), ("TTO", -61.22, 10.45),
    ("DMA", -61.37, 15.41), ("MUS", 57.55, -20.35), ("PRI", -66.50, 18.22), ("FJI", 178.07, -17.71),
    ("VUT", 167.95, -15.38), ("SLB", 160.16, -9.64), ("BRB", -59.54, 13.19), ("COM", 43.87, -11.88),
    ("REU", 55.54, -21.12),
], columns=["iso3", "lon", "lat"])
pts = pd.concat([pts[~pts["iso3"].isin(ISLANDS["iso3"])], ISLANDS], ignore_index=True)
pts["country"] = pts["iso3"].map(display_name)
pts["region"] = pts["iso3"].map(region)
needed = set(df["bean_iso3"].dropna()) | set(df["maker_iso3"].dropna())
pts[pts["iso3"].isin(needed)].sort_values("iso3").to_csv(OUT / "country_points.csv", index=False)
no_point = needed - set(pts["iso3"])

# Summary per bean country (used by the FAO charts, which look ratings up by country)
summary = (df.dropna(subset=["bean_iso3"]).groupby(["bean_iso3", "bean_country"])
             .agg(n_bars=("rating", "size"), avg_rating=("rating", "mean")).reset_index()
             .rename(columns={"bean_iso3": "iso3"}))
summary["avg_rating"] = summary["avg_rating"].round(3)
summary.to_csv(OUT / "bean_country_summary.csv", index=False)

# ---------------------------------------------------------------------------
# 4. FAO cocoa bean production (if downloaded)
# ---------------------------------------------------------------------------
fao_file = RAW / "fao_cocoa_production.csv"                 # direct FAOSTAT download
owid_file = RAW / "fao_cocoa_production_owid_2024.csv"     # FAOSTAT figures as published by Our World in Data
fao = None
if fao_file.exists():
    fao = pd.read_csv(fao_file)
    fao = fao[(fao["Element"] == "Production") & (fao["Item"].str.contains("Cocoa", case=False))]
    code_col = "Area Code (M49)" if "Area Code (M49)" in fao.columns else None
    def fao_iso3(row):
        if code_col:
            m49 = str(row[code_col]).strip("'").zfill(3)
            c = pycountry.countries.get(numeric=m49)
            if c: return c.alpha_3
        return to_iso3(row["Area"])
    fao["iso3"] = fao.apply(fao_iso3, axis=1)
    fao = fao.dropna(subset=["iso3", "Value"]).rename(columns={"Year": "year", "Value": "tonnes"})
elif owid_file.exists():
    fao = pd.read_csv(owid_file).rename(columns={"code": "iso3", "cocoa_beans_production_tonnes": "tonnes"})
    fao = fao[fao["iso3"].str.len() == 3]        # drop regions such as "World" or "Africa"

if fao is not None:
    fao = fao[["iso3", "year", "tonnes"]].groupby(["iso3", "year"], as_index=False)["tonnes"].sum()
    fao["country"] = fao["iso3"].map(display_name)
    fao = fao.merge(pts[["iso3", "lon", "lat"]], on="iso3", how="left")
    fao.to_csv(OUT / "fao_cocoa_production.csv", index=False)
    print(f"FAO: {fao['iso3'].nunique()} countries, years {fao['year'].min()}–{fao['year'].max()}")

    # Growers compared: share of the world's cocoa vs share of the single-origin bars reviewed
    latest = fao[fao["year"] == fao["year"].max()].copy()
    latest["world_share"] = latest["tonnes"] / latest["tonnes"].sum()
    single = df.dropna(subset=["bean_iso3"])
    bar_share = single.groupby("bean_iso3").size() / len(single)
    latest["bar_share"] = latest["iso3"].map(bar_share).fillna(0)
    top = set(latest.nlargest(6, "world_share")["iso3"]) | set(latest.nlargest(5, "bar_share")["iso3"])
    comp = latest[latest["iso3"].isin(top)].copy()
    comp["direction"] = comp.apply(lambda r: "More popular with craft makers" if r["bar_share"] > r["world_share"]
                                   else "Less popular with craft makers", axis=1)

    def spread(values, gap, rounds=200):
        """Push label positions apart (both up and down) until they are at least `gap` apart."""
        pos = list(values)
        order = sorted(range(len(pos)), key=lambda i: pos[i])
        for _ in range(rounds):
            moved = False
            for a, b in zip(order, order[1:]):
                d = pos[b] - pos[a]
                if d < gap:
                    shift = (gap - d) / 2
                    pos[a] -= shift; pos[b] += shift; moved = True
            if not moved:
                break
        return pos
    # Only label the end of a line where the share is big enough to matter (5% or more); the rest show on hover
    for side, col in [("left", "world_share"), ("right", "bar_share")]:
        show = comp[col] >= 0.05
        gap = max(comp["world_share"].max(), comp["bar_share"].max()) * 0.05   # both sides share one scale
        comp[f"label_{side}"] = None
        comp.loc[show, f"label_{side}"] = spread(list(comp.loc[show, col]), gap)
    comp = comp[["iso3", "country", "year", "tonnes", "world_share", "bar_share", "direction", "label_left", "label_right"]]
    comp.sort_values("world_share", ascending=False).to_csv(OUT / "grower_compare.csv", index=False)
else:
    print("NOTE: no FAO file found in data/raw. Skipping production data.")

# Makers by country, for the maker map
makers = (df.dropna(subset=["maker_iso3"]).groupby(["maker_iso3", "maker_country", "maker_region"])
            .agg(n_bars=("rating", "size"), avg_rating=("rating", "mean"), n_makers=("maker", "nunique"))
            .reset_index().rename(columns={"maker_iso3": "iso3"}))
makers["avg_rating"] = makers["avg_rating"].round(3)
makers = makers.merge(pts[["iso3", "lon", "lat"]], on="iso3", how="left")
makers.to_csv(OUT / "maker_countries.csv", index=False)

# Keep the year slider on the choropleth in step with the newest review year
spec_path = ROOT / "specs" / "02_choropleth.vl.json"
if spec_path.exists():
    spec_text = spec_path.read_text()
    new_text = re.sub(r'("input": "range",\s*"min": 2006,\s*"max": )\d{4}', rf'\g<1>{int(df["review_year"].max()) - 5}', spec_text)
    if new_text != spec_text:
        spec_path.write_text(new_text)
        print(f"Updated the year slider in {spec_path.name} to end at {int(df['review_year'].max())}")

# ---------------------------------------------------------------------------
# 5. Report
# ---------------------------------------------------------------------------
print(f"Bars: {len(df)} | reviews {df['review_year'].min()}–{df['review_year'].max()} | source: {src.name}")
print(f"Bean countries: {df['bean_iso3'].nunique()} | maker countries: {df['maker_iso3'].nunique()}")
print(f"Australian makers: {df.loc[df['maker_iso3'].eq('AUS'), 'maker'].nunique()} "
      f"({df['maker_iso3'].eq('AUS').sum()} bars)")
if unmatched:
    print("WARNING: country names not matched (add them to OVERRIDES):", sorted(unmatched))
if no_point:
    print("WARNING: no map point for:", sorted(no_point))
for f in sorted(OUT.iterdir()):
    print(f"  {f.name:28s} {f.stat().st_size / 1024:7.1f} KB")
