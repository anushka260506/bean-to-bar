# From Bean to Bar: What Makes a Great Chocolate Bar?

A scrollable data story about expert chocolate bar reviews and where cocoa comes from,
built with Vega-Lite and Vega for FIT3179 Data Visualisation 2 (Monash University).

**Author:** Anushka Khunteta · **Created:** October 2026

## Folder structure

```
index.html                 the web page
css/style.css              colours, fonts and the 12-column grid
js/theme.js                shared chart settings (fonts, colours) passed to every chart
js/main.js                 puts each chart spec into its place on the page
specs/                     one readable JSON spec per chart (01_waffle.vl.json, ...)
data/processed/            the small files the charts load (under 1 MB in total)
data/raw/                  original downloads, kept for transparency
scripts/prepare_data.py    turns data/raw into data/processed
sketch/sketch.pdf          the hand-drawn sketch
```

## Preview the page on your computer

The charts load data files, so the page needs a small local web server. Opening
`index.html` by double-clicking will not show the charts.

Option 1, VS Code: install the **Live Server** extension, right-click `index.html`, then choose **Open with Live Server**.

Option 2, Terminal:

```
cd path/to/bean-to-bar
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Updating the data

1. Save the newest chocolate ratings as `data/raw/chocolate_ratings.csv`.
2. Save the FAOSTAT cocoa bean production download as `data/raw/fao_cocoa_production.csv`.
3. Run `python scripts/prepare_data.py`. It needs `pandas`, `pycountry` and `pycountry-convert`.
4. The script prints a short report and warns about any country names it could not match.

## Data sources

- **Chocolate bar ratings:** Brady Brelinski, Flavors of Cacao chocolate database, https://flavorsofcacao.com/chocolate_database.html
- **Cocoa bean production:** FAOSTAT, Crops and livestock products, Food and Agriculture Organization of the United Nations, https://www.fao.org/faostat/en/#data/QCL
- **Country shapes:** Natural Earth, via world-atlas 2.0.2 (https://github.com/topojson/world-atlas)

## Use of AI

Claude (Anthropic) was used to help plan the story, write and debug chart code, prepare the
data files and check the grammar of the text. All design choices and final text were
reviewed by the author.
