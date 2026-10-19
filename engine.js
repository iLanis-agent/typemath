// Type Math engine: type scales, line-height rhythm and line measure as exact fractions on BigInt. Sizes are in one unit you choose.
var BASE_ERR = "the base size must be a whole number from 1 to 1000";
var RATIO_ERR = "enter the ratio as two whole numbers with a slash, like 3/2, the top at least the bottom, each from 1 to 200";
var STEPS_ERR = "the steps up must be a whole number from 1 to 10";
var FONT_ERR = "the font size must be a whole number from 1 to 1000";
var PCT_ERR = "the line height percent must be a whole number from 1 to 1000";
var UNIT_ERR = "the baseline unit must be a whole number from 1 to 1000";
var WIDTH_ERR = "the column width must be a whole number from 1 to 10000";
var CW_ERR = "the character width must be a number above 0 and up to 999.99, with at most 2 decimals";
var LEN_ERR = "the text length must be a whole number from 1 to 1000000";

function _int(t, re, lo, hi, err) {
  t = typeof t === "string" ? t.trim() : "";
  if (!re.test(t)) throw new Error(err);
  var n = parseInt(t, 10);
  if (n < lo || n > hi) throw new Error(err);
  return n;
}
function _plural(n, one, many) { return n + " " + (String(n) === "1" ? one : many); }
// num/den rounded half up to hundredths, shown with trailing zeros dropped
function _fmt(num, den) {
  var v = (2n * num * 100n + den) / (2n * den);
  var s = (v / 100n).toString(), f = (v % 100n).toString();
  if (f.length < 2) f = "0" + f;
  f = f.replace(/0+$/, "");
  return f ? s + "." + f : s;
}

function scaleTruth(base, ratio, up) {
  var b = BigInt(_int(base, /^[0-9]{1,4}$/, 1, 1000, BASE_ERR));
  var r = typeof ratio === "string" ? ratio.trim() : "";
  var m = /^([0-9]{1,3})\s*\/\s*([0-9]{1,3})$/.exec(r);
  if (!m) throw new Error(RATIO_ERR);
  var p = parseInt(m[1], 10), q = parseInt(m[2], 10);
  if (p < 1 || q < 1 || p > 200 || q > 200 || p < q) throw new Error(RATIO_ERR);
  var u = _int(up, /^[0-9]{1,2}$/, 1, 10, STEPS_ERR);
  var P = BigInt(p), Q = BigInt(q), out = [];
  for (var k = -2; k <= u; k++) {
    var num = b, den = 1n;
    for (var i = 0; i < Math.abs(k); i++) { if (k > 0) num *= P; else num *= Q; }
    for (var j = 0; j < Math.abs(k); j++) { if (k > 0) den *= Q; else den *= P; }
    out.push(_fmt(num, den));
  }
  return "Sizes from 2 steps down to " + _plural(u, "step", "steps") + " up at ratio " + p + "/" + q + " on a base of " + b + ": " + out.join(", ") + ".";
}
function rhythmTruth(font, pct, unit) {
  var f = BigInt(_int(font, /^[0-9]{1,4}$/, 1, 1000, FONT_ERR));
  var c = BigInt(_int(pct, /^[0-9]{1,4}$/, 1, 1000, PCT_ERR));
  var g = BigInt(_int(unit, /^[0-9]{1,4}$/, 1, 1000, UNIT_ERR));
  var lineNum = f * c, lineDen = 100n; // line = f*c/100
  var out = "A " + f + " font at " + c + "% line height has a " + _fmt(lineNum, lineDen) + " line on a baseline unit of " + g + ": ";
  var unitsNum = f * c, unitsDen = 100n * g;
  if (unitsNum % unitsDen === 0n) {
    var n = unitsNum / unitsDen;
    return out + "that is exactly " + _plural(n, "unit", "units") + ".";
  }
  var shown = _fmt(unitsNum, unitsDen);
  var up = ((unitsNum + unitsDen - 1n) / unitsDen) * g;
  return out + "that is " + shown + (shown === "1" ? " unit" : " units") + ". The next whole-unit line height is " + up + ", which is " + _fmt(up * 100n, f) + "% of the font size.";
}
function measureTruth(width, charWidth, length) {
  var w = BigInt(_int(width, /^[0-9]{1,5}$/, 1, 10000, WIDTH_ERR));
  var t = typeof charWidth === "string" ? charWidth.trim() : "";
  var m = /^([0-9]{1,3})(?:\.([0-9]{1,2}))?$/.exec(t);
  if (!m) throw new Error(CW_ERR);
  var frac = (m[2] || "").padEnd(2, "0");
  var cw = BigInt(m[1]) * 100n + BigInt(frac);
  if (cw <= 0n) throw new Error(CW_ERR);
  var n = BigInt(_int(length, /^[0-9]{1,7}$/, 1, 1000000, LEN_ERR));
  var cpl = (w * 100n) / cw;
  var cwShow = _fmt(cw, 100n);
  if (cpl === 0n) return "A column " + w + " wide at " + cwShow + " per character holds 0 characters per line, so no text fits.";
  var lines = (n + cpl - 1n) / cpl;
  var last = n - (lines - 1n) * cpl;
  return "A column " + w + " wide at " + cwShow + " per character holds " + _plural(cpl, "character", "characters") + " per line. A text of " + _plural(n, "character", "characters") + " takes " + _plural(lines, "line", "lines") + ", and the last line holds " + last + ".";
}
