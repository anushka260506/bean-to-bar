# From Bean to Bar: description

**Live page:** https://anushka260506.github.io/bean-to-bar/
**Code and data:** https://github.com/anushka260506/bean-to-bar
**Sketch:** https://anushka260506.github.io/bean-to-bar/sketch/sketch.pdf

## Why

**Domain.** Product reviews: expert ratings of plain dark chocolate bars, plus where their cocoa is grown.

**Purpose.** The page asks what makes a great chocolate bar. Its sections cover how good most bars are, where the best beans grow, who makes the bars (with an Australia spotlight), whether cocoa percentage and recipe matter, which words describe great bars, and change over time. It ends with a four-tip "aisle guide".

**Audience.** Everyday chocolate buyers in Australia who wonder if an expensive craft bar is worth it. They need no data background, so the text is plain and each chart has a one-line takeaway.

**Tasks (Munzner's action and target).** Present and discover the *distribution* of ratings; *compare* countries, regions, makers, cocoa bands and recipes; *identify* the best and worst values; look for a *correlation* between how much cocoa a country grows and its ratings; and follow the *trend* over time.

**Why this topic.** Nearly everyone buys chocolate, and the price gap between a supermarket bar and a craft bar made me want to know what the extra money actually buys. Thousands of reviews by one expert seemed a fair way to find out.

## What

**Flavors of Cacao ratings** by Brady Brelinski (flavorsofcacao.com, database updated 19 April 2026). One taster rates each plain dark bar from 1 to 5 in 0.25 steps, judging flavour, texture, aftermelt and overall opinion, and notes a few memorable words and the ingredients. 2,841 bars from 667 makers in 69 countries, reviewed 2006 to 2026, with beans from 58 countries. **Dataset type:** a table, one item per bar. **Attribute types:** categorical (maker, maker country, bean country, ingredients, tasting words), ordinal (rating band, cocoa band, review year) and quantitative (rating, cocoa percentage).

**Cocoa bean production, 2024** from FAOSTAT (Food and Agriculture Organization of the United Nations) via Our World in Data: tonnes grown in 57 countries, collected from national governments with FAO estimates filling gaps. It is relevant because it lets the page compare how much cocoa a country grows with how often craft makers choose its beans.

**Country shapes** from Natural Earth via world-atlas: geometry (a spatial dataset) that the country tables are joined to by ISO code.

A Python script only does light cleaning: standard country names, the five official rating bands, cocoa bands, recipe flags, single tasting words, and joining production to bean countries. No rating or production figure is changed.

## How

Nine of the thirteen idioms are advanced, because none of them is in the brief's list of basic idioms: waffle, choropleth, slope chart, flow map, proportional symbol map, mosaic, heatmap, recipe matrix and ridgeline. The waffle is a unit chart, not a pie: each square is one percent of the bars. The slope chart is not a time series: it joins two different measures for the same country.

| # | Idiom | Why (action and target) | Marks and channels |
|---|---|---|---|
| 1 | Waffle chart | Present a part of a whole: how many bars reach each rating band | Square marks; colour lightness for band; count of squares for share |
| 2 | Choropleth map | Compare and identify ratings by place | Area marks (countries); colour lightness for average rating |
| 3 | Slope chart | Compare two measures per country: share of world cocoa vs share of bars | Point and line marks; vertical position for each share; slope and hue for direction |
| 4 | Scatterplot (log scale) | Look for a correlation between tonnes grown and rating | Point marks; horizontal position (log) for tonnes; vertical position for rating |
| 5 | Flow map | Discover connections between bean countries and a maker country | Line marks with width for bars; point marks with area for bars |
| 6 | Proportional symbol map | Compare amounts and quality by maker country | Point marks; area for bars made; colour lightness for rating |
| 7 | Mosaic chart | Compare rating mixes across regions of very different size | Rectangle marks; width for region size; height for band share; lightness for band |
| 8 | Lollipop chart | Compare each Australian maker with the average | Line and point marks; horizontal position for rating, from the average line |
| 9 | Heatmap | Compare the rating mix of each cocoa band | Rectangle marks in a grid; colour lightness for share |
| 10 | Recipe matrix (UpSet style) | Compare sets of ingredients and identify the best recipe | Point marks filled or empty for each ingredient; position for average rating |
| 11 | Word lollipop chart | Identify words linked to good and bad bars | Point marks; horizontal position for rating; area for how often a word is used |
| 12 | Ridgeline plot | Compare distributions over time | Area marks; height for density; vertical position for period; lightness for average |
| 13 | Line chart | Show the trend in reviews per year | Line and point marks; vertical position for number of bars |

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
