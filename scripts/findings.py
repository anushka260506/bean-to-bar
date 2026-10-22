"""
findings.py: prints every number that is quoted in the page text (index.html).

Run it after prepare_data.py whenever the data changes, then update any sentence in
index.html whose number no longer matches. Usage:
    python scripts/findings.py
"""
from pathlib import Path
import pandas as pd

P = Path(__file__).resolve().parent.parent / "data" / "processed"
d = pd.read_csv(P / "chocolate.csv")
avg = d["rating"].mean()

def pct(x):
    return f"{x * 100:.1f}%"

print("== Section 1 ==")
print("bars:", len(d), "| years:", d.review_year.min(), "-", d.review_year.max(), "| average rating:", round(avg, 2))
print("makers:", d.maker.nunique(), "| maker countries:", d.maker_country.nunique())
print("share by band:", (d.rating_band.value_counts(normalize=True) * 100).round(1).to_dict())

print("\n== Section 2 ==")
g = d.dropna(subset=["bean_iso3"]).groupby("bean_country").rating.agg(["mean", "count"])
print("top bean countries (20+ bars):\n", g[g["count"] >= 20].sort_values("mean", ascending=False).head(5).round(2))
print("West Africa:", g.reindex(["Côte d'Ivoire", "Ghana", "Nigeria", "Cameroon"]).round(2).to_dict("index"))
gc = P / "grower_compare.csv"
if gc.exists():
    c = pd.read_csv(gc)
    print("growers (world share vs bar share):\n", c[["country", "world_share", "bar_share"]].round(3).to_string(index=False))

print("\n== Section 3 ==")
au = d[d.maker_iso3 == "AUS"]
single = au.dropna(subset=["bean_iso3"])
print("Australia: makers", au.maker.nunique(), "| bars", len(au), "| average", round(au.rating.mean(), 2))
print("AU bean origins:", single.bean_country.value_counts().head(6).to_dict())
pacific = {"PNG", "VUT", "SLB", "FJI", "WSM"}
print("AU single-origin bars from Pacific neighbours:", single.bean_iso3.isin(pacific).sum(), "of", len(single))
m = d.groupby("maker_country").size().sort_values(ascending=False)
print("top maker country:", m.index[0], m.iloc[0], pct(m.iloc[0] / len(d)))
print("outstanding share by maker region:", (d.groupby("maker_region").apply(lambda x: (x.rating >= 4).mean()) * 100).round(1).to_dict())
mk = au.groupby("maker").rating.agg(["mean", "count"])
print("AU makers above average:", (mk["mean"] > avg).sum(), "of", len(mk), "| most bars:", mk["count"].idxmax(), mk["count"].max())

print("\n== Section 4 ==")
cb = d.groupby("cocoa_band").apply(lambda x: pd.Series({"outstanding": (x.rating >= 4).mean(), "disappointing": (x.rating < 3).mean()}))
print((cb * 100).round(1))
r = d[d.recipe != "Not listed"].groupby("recipe").rating.agg(["mean", "count"])
print(r[r["count"] >= 20].sort_values("mean", ascending=False).round(3))

print("\n== Section 5 ==")
w = pd.read_csv(P / "tasting_words.csv").groupby("word").rating.agg(["mean", "count"])
top = w.sort_values("count", ascending=False).head(25).sort_values("mean")
print("lowest:", top.head(3).round(2).to_dict("index"))
print("highest:", top.tail(3).round(2).to_dict("index"))

print("\n== Section 6 ==")
d["period"] = 2006 + ((d.review_year - 2006) // 3) * 3
print("average by period:", d.groupby("period").rating.mean().round(2).to_dict())
y = d.groupby("review_year").size()
print("busiest year:", y.idxmax(), y.max())

print("\n== Section 7 ==")
print("blends:", round(d[d.bean_origin_raw == "Blend"].rating.mean(), 2), "| single origin:", round(d[d.bean_origin_raw != "Blend"].rating.mean(), 2))
