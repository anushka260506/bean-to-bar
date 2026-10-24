# From Bean to Bar: description

**Live page:** https://anushka260506.github.io/bean-to-bar/
**Code and data:** https://github.com/anushka260506/bean-to-bar

## Why

**Domain.** Product reviews: expert ratings of plain dark chocolate bars, plus where their cocoa is grown.

**Purpose.** The page asks what makes a great chocolate bar. Its sections cover how good most bars are, where the best beans grow, who makes the bars (with an Australia spotlight), whether cocoa percentage and recipe matter, which words describe great bars, and change over time. It ends with a four-tip "aisle guide".

**Audience.** Everyday chocolate buyers in Australia who wonder if an expensive craft bar is worth it. They need no data background, so the text is plain and each chart has a one-line takeaway.

**Tasks.** See how ratings spread, compare countries, regions, makers and recipes, test whether bigger growers get better ratings, and track change over time.

**Why this topic.** Nearly everyone buys chocolate, and the price gap between a supermarket bar and a craft bar made me want to know what the extra money actually buys. Thousands of reviews by one expert seemed a fair way to find out.

## What

**Flavors of Cacao ratings** by Brady Brelinski (flavorsofcacao.com, database updated 19 April 2026). One taster rates each plain dark bar from 1 to 5 in 0.25 steps, judging flavour, texture, aftermelt and overall opinion, and notes a few memorable words and the ingredients. 2,841 bars from 667 makers in 69 countries, reviewed 2006 to 2026, with beans from 58 countries. Attributes: maker, maker country, review year, bean country, cocoa percentage, ingredients, words and rating.

**Cocoa bean production, 2024** from FAOSTAT (Food and Agriculture Organization of the United Nations) via Our World in Data: tonnes grown in 57 countries, collected from national governments with FAO estimates filling gaps. It is relevant because it lets the page compare how much cocoa a country grows with how often craft makers choose its beans.

**Country shapes** from Natural Earth via world-atlas.

A Python script only does light cleaning: standard country names, the five official rating bands, cocoa bands, recipe flags, single tasting words, and joining production to bean countries. No rating or production figure is changed.

## How

Nine of the thirteen idioms are advanced: waffle, choropleth, slope chart, flow map, proportional symbol map, mosaic, heatmap, recipe matrix and ridgeline. The slope chart is not a time series: it joins two different measures for the same country, so the reader can see which way each country moves.

| # | Idiom | Task, and why this idiom fits |
|---|---|---|
| 1 | Waffle chart | Part of a whole. 100 squares coloured by rating band make "4 in 100 bars are outstanding" easy to count. |
| 2 | Choropleth map | Compare places. There is one average per country, so it fills the country shape, with lightness for rating. |
| 3 | Slope chart | Compare two measures. Position on the left is share of world cocoa, on the right share of bars; the slope shows the gap. |
| 4 | Scatterplot (log scale) | Find a relationship between size and quality. A log scale fits growers from about 10 to 2 million tonnes on one axis. |
| 5 | Flow map | Follow connections. Line width shows how many bars link a bean country to the chosen maker country. |
| 6 | Proportional symbol map | Compare amounts by place. Circle area shows bars made, colour shows average rating. |
| 7 | Mosaic chart | Compare mixes across groups of very different size. Column width shows each region's bars, stacked height its rating mix. |
| 8 | Lollipop chart | Compare each Australian maker to the average. Position along one scale, starting from the average line. |
| 9 | Heatmap | Compare two categories at once. Cocoa band against rating band, with lightness showing each band's share. |
| 10 | Recipe matrix (UpSet style) | Compare sets. Filled dots show which ingredients a recipe uses, next to its average rating. |
| 11 | Word lollipop chart | Rank words by rating. Position shows the average, dot size how often the word is used. |
| 12 | Ridgeline plot | Compare distributions over time. One smoothed hill per three-year group, stacked so the shifts line up. |
| 13 | Line chart | Show a trend. Reviews per year, so readers know which years in chart 12 rest on few bars. |

**Special features**

- **Year slider (chart 2).** Limits the map to reviews from a chosen year onwards (2006 to 2021, so every setting keeps enough bars), and the "Top rated" label updates with it.
- **Maker dropdown (chart 5).** Picks the maker country; the map turns so that country sits in the middle.
- **Hand-built recipe matrix (chart 10).** Vega-Lite has no UpSet chart, so it is built from layered dots and lines next to a panel of average ratings with a shared sort. Hovering a recipe's dot highlights that row in both panels.
- **Ridgeline average lines (chart 12).** Each hill has a white line and number for its period's average, plus a baseline to its year label. Year groups come from the data.
- **Waffle and mosaic.** Built by hand from squares and stacked rectangles, as Vega-Lite has neither.
- **Numbers from the data.** Headline numbers in the text are filled in from the data, so they stay correct when it changes.

**Colour and layout.** Browns show rating, light for low and dark for high. Raspberry marks notes and the all-bars average line. Teal always means Australia. Tooltips give exact numbers on every chart. All three maps use the Equal Earth projection, which keeps each country's size true to its real area, so big and small countries are compared fairly. The map's colour scale covers only 2.8 to 3.5, and the page says so.

## Use of AI

Claude (Anthropic) was used to help plan the story, write and debug chart code, prepare the data files, draft and edit the page text, and draw the chocolate bar in the header. All design choices and final text were reviewed by the author.
