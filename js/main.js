// Embeds every chart spec into its place on the page.
// To add a chart: save its spec in /specs and add a line to CHARTS below.

const CHARTS = [
  ["#vis01", "specs/01_waffle.vl.json"],
  ["#vis02", "specs/02_choropleth.vl.json"],
  ["#vis03", "specs/03_growers_slope.vl.json"],
  ["#vis04", "specs/04_scatter.vl.json"],
  ["#vis05", "specs/05_flow_map.vl.json"],
  ["#vis06", "specs/06_maker_map.vl.json"],
  ["#vis07", "specs/07_mosaic.vl.json"],
  ["#vis08", "specs/08_australia_makers.vl.json"],
  ["#vis09", "specs/09_heatmap.vl.json"],
  ["#vis10", "specs/10_recipe_matrix.vl.json"],
  ["#vis11", "specs/11_word_scale.vl.json"],
  ["#vis12", "specs/12_ridgeline.vl.json"],
  ["#vis13", "specs/13_reviews_per_year.vl.json"],
];

const EMBED_OPTIONS = { actions: false, renderer: "svg", config: CHOC_THEME };

// Wait for the web fonts, so Vega measures label widths with the same font it draws with.
document.fonts.ready.then(() => {
  CHARTS.forEach(([el, spec]) => {
    vegaEmbed(el, spec, EMBED_OPTIONS).catch(err => {
      console.error(spec, err);
      document.querySelector(el).innerHTML = `<div class="pending">Could not load ${spec}</div>`;
    });
  });
});

// Fill the headline numbers from the data, so they stay correct when the data is updated.
vega.loader().load("data/processed/chocolate.csv").then(text => {
  const rows = vega.read(text, { type: "csv", parse: "auto" });
  const nf = new Intl.NumberFormat("en-AU");
  const beanCountries = new Set(rows.map(r => r.bean_iso3).filter(Boolean)).size;
  const years = rows.map(r => r.review_year).filter(Boolean);
  const au = rows.filter(r => r.maker_iso3 === "AUS");
  const mean = list => list.reduce((a, r) => a + r.rating, 0) / list.length;
  const facts = {
    "au-makers": new Set(au.map(r => r.maker)).size,
    "au-bars": au.length,
    "au-avg": mean(au).toFixed(2),
    "all-avg": mean(rows).toFixed(2),
    "bars": nf.format(rows.length),
    "bars-rounded": nf.format(Math.floor(rows.length / 100) * 100),
    "bean-countries": beanCountries,
    "data-note": `${nf.format(rows.length)} bars reviewed ${Math.min(...years)}–${Math.max(...years)}`
  };
  document.querySelectorAll("[data-fact]").forEach(node => {
    const v = facts[node.dataset.fact];
    if (v !== undefined) node.textContent = v;
  });
});
