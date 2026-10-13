// Shared Vega / Vega-Lite settings so every chart uses the same fonts and colours.
// Passed to vegaEmbed as `config`, so the chart specs in /specs stay short and readable.
const CHOC_THEME = {
  background: null,                       // let the white card show through
  font: "Source Sans 3, Segoe UI, Arial, sans-serif",
  view: { stroke: null },                 // no box around the plot area (better data-ink ratio)
  title: { font: "Fraunces, Georgia, serif", fontSize: 16, fontWeight: 600, color: "#2B1D14", anchor: "start" },
  axis: {
    labelColor: "#6E5A4B", titleColor: "#6E5A4B", labelFontSize: 12, titleFontSize: 12,
    titleFontWeight: 600, domainColor: "#C9B8A6", tickColor: "#C9B8A6", gridColor: "#EFE5D8"
  },
  legend: {
    labelColor: "#6E5A4B", titleColor: "#2B1D14", labelFontSize: 12, titleFontSize: 12,
    titleFontWeight: 600, symbolStrokeWidth: 0
  },
  text: { font: "Source Sans 3, Segoe UI, Arial, sans-serif", color: "#2B1D14" },
  range: {
    // Ratings, light (low) to dark (high)
    ramp: ["#EFD5B2", "#E0B98A", "#C48A57", "#8E5531", "#4E2A16"],
    heatmap: ["#EFD5B2", "#E0B98A", "#C48A57", "#8E5531", "#4E2A16"]
  }
};

// Colours with a fixed meaning across the whole page
const CHOC_COLOURS = {
  bands: ["Outstanding", "Highly recommended", "Recommended", "Disappointing", "Unpleasant"],
  bandColours: ["#4E2A16", "#8E5531", "#C48A57", "#E0B98A", "#EFD5B2"],
  accent: "#B0304A",
  australia: "#2E7D7A"
};
