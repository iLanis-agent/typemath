# Type Math

Type scale, line height and measure arithmetic. A 17 font at 150% line height is a 25.5 line, which is 3.19 units of an 8 grid, not a whole number of units.

## What it computes

All sizes are in one unit of your choice.

- **The scale truth** - a base size times a ratio (two whole numbers, like 3/2), from 2 steps down to up to 10 steps up, each rounded to hundredths.
- **The rhythm truth** - a line height given as a percent of the font size, how many baseline units it spans, and the next whole-unit line height with its percent of the font size.
- **The measure truth** - characters per line for a column width and an average character width (up to 2 decimals), and how many lines a text of a given length takes, with the last line's length.

## Boundary

Arithmetic only. It works out sizes, line heights and line lengths from the owner's own numbers. It does not know any screen, printer, font or reader and gives no verdict on whether a size, line height or line length is readable or good.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (BigInt fractions, half-up rounding to hundredths).
- `oracle.py` - the Python mirror (Fractions and Decimal, lines filled one at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (176 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/typemath/
Repo: https://github.com/iLanis-agent/typemath
