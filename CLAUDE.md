# From Bean to Bar: project notes for Claude Code

This is Anushka's FIT3179 Data Visualisation 2 assignment (topic: Product Reviews).
It is a one-page data story about expert chocolate bar reviews, built with Vega-Lite and
hosted on GitHub Pages at https://anushka260506.github.io/bean-to-bar/

**Due:** Sunday 25 October 2026, 11:55 PM (Melbourne time).

## Ground rules

- Work one step at a time. Explain each change in plain words and wait for Anushka to say "yes" before moving on.
- Keep the page sounding like a person wrote it: short sentences, plain words, no em dashes, no repeated
  "Key insight:" style labels. Do not invent personal facts about Anushka (favourite chocolate, what she
  expected and so on). Ask her instead.
- Never make up or change data values. Every number in the text must come from `scripts/findings.py`.
- Keep the "Use of AI" acknowledgement in the footer.
- The page must have no horizontal scrolling on a 1280px-wide laptop screen.
- After a change is approved: commit with a clear message and push to `main` so the live page updates.

## How the project works

```
index.html                 the page (text, layout, where each chart goes)
css/style.css              colours, fonts, 12-column grid
js/theme.js                shared Vega-Lite settings (fonts, colours)
js/main.js                 embeds each spec in /specs and fills in numbers marked data-fact="..."
specs/*.json               one readable spec per chart (13 charts)
data/raw/                  original downloads
data/processed/            what the charts load (made by the scripts below)
scripts/prepare_data.py    data/raw -> data/processed (run after any data change)
scripts/findings.py        prints every number quoted in the page text
sketch/                    put the scanned hand-drawn sketch here as sketch.pdf
```

Preview locally: `python -m http.server 8000`, then open http://localhost:8000
(opening index.html directly does not load the charts).

## Design decisions (keep these)

- Palette: browns for ratings (light = low, dark = high), raspberry #B0304A for highlights and notes,
  teal #2E7D7A always means Australia.
- Fonts: Fraunces for headings, Source Sans 3 for body text.
- 13 charts, 9 advanced idioms: waffle, choropleth, slope chart, flow map, proportional symbol map,
  mosaic, heatmap, recipe matrix (UpSet-style), ridgeline. Basic: scatter, two lollipop charts, line.
- 3 map idioms: choropleth (02), flow map (05), proportional symbol map (06).
- The treemap was removed on tutor feedback and replaced by the maker map (06).
- Layout follows the unit's two-column grid template in places: text in a side column next to the chart (mosaic 07 and tasting words 11), alternating sides.

## What is done

- All 13 charts work, with tooltips, a year slider (02), a maker-country dropdown (05) and hover highlights.
- FAO 2024 cocoa production (via Our World in Data) is in `data/raw/fao_cocoa_production_owid_2024.csv`.
- Critique feedback has been applied (accent colour, zoomed-scale note, mosaic counts, ridgeline lines, layout gaps).

## What is left (do these in order)

1. **Newest chocolate data.** The ratings are still a 2021 copy (2,530 bars). The brief asks for the most
   recent data. The live database is at https://flavorsofcacao.com/chocolate_database.html (updated
   April 2026, about 2,700 bars). The table is filled in by JavaScript, so look at the page source or the
   network requests to find the file it loads, download it, and save it as
   `data/raw/chocolate_ratings.csv` with the same columns as the 2021 copy. If that is not possible,
   ask Anushka to copy the table into Google Sheets and download it as CSV.
2. Run `python scripts/prepare_data.py` and fix any country names it warns about.
3. Run `python scripts/findings.py` and update every sentence in `index.html` whose number has changed
   (section text, takeaway lines under charts, the Australia spotlight list, the four aisle-guide cards).
   Also update the flow map dropdown in `specs/05_flow_map.vl.json` if the top maker countries changed.
4. Check every chart renders with no errors, labels do not overlap, and there is no horizontal scrolling.
5. When Anushka provides the scanned sketch, save it as `sketch/sketch.pdf`.
6. Draft the written description for Moodle in `docs/description.md`, using Munzner's What/Why/How
   headings: domain, why and who; what (data sources, authors, how the data was made); how (why each
   idiom was chosen and what task it helps with). Keep it short and in plain words.
7. Write `docs/interview_notes.md`: for each chart, one line on what it shows, why that idiom, and one
   design choice to mention. Plain words, so Anushka can revise from it.
