#!/usr/bin/env python3
# Type Math oracle - mirrors engine.js with Fractions and Decimal rounding, and fills lines one character at a time.
import json, re, random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

BASE_ERR = "the base size must be a whole number from 1 to 1000"
RATIO_ERR = "enter the ratio as two whole numbers with a slash, like 3/2, the top at least the bottom, each from 1 to 200"
STEPS_ERR = "the steps up must be a whole number from 1 to 10"
FONT_ERR = "the font size must be a whole number from 1 to 1000"
PCT_ERR = "the line height percent must be a whole number from 1 to 1000"
UNIT_ERR = "the baseline unit must be a whole number from 1 to 1000"
WIDTH_ERR = "the column width must be a whole number from 1 to 10000"
CW_ERR = "the character width must be a number above 0 and up to 999.99, with at most 2 decimals"
LEN_ERR = "the text length must be a whole number from 1 to 1000000"

def pint(t, pat, lo, hi, err):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(pat, t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def plural(n, one, many): return f"{n} {one if str(n) == '1' else many}"
def fmt(fr):
    d = (Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    s = format(d, "f")
    if "." in s: s = s.rstrip("0").rstrip(".")
    return s

def scale(base, ratio, up):
    b = pint(base, r"[0-9]{1,4}", 1, 1000, BASE_ERR)
    r = ratio.strip() if isinstance(ratio, str) else ""
    m = re.fullmatch(r"([0-9]{1,3})\s*/\s*([0-9]{1,3})", r)
    if not m: raise ValueError(RATIO_ERR)
    p, q = int(m.group(1)), int(m.group(2))
    if p < 1 or q < 1 or p > 200 or q > 200 or p < q: raise ValueError(RATIO_ERR)
    u = pint(up, r"[0-9]{1,2}", 1, 10, STEPS_ERR)
    rr = Fraction(p, q)
    vals = [fmt(b * rr ** k) for k in range(-2, u + 1)]
    return f"Sizes from 2 steps down to {plural(u,'step','steps')} up at ratio {p}/{q} on a base of {b}: " + ", ".join(vals) + "."

def rhythm(font, pct, unit):
    f = pint(font, r"[0-9]{1,4}", 1, 1000, FONT_ERR)
    c = pint(pct, r"[0-9]{1,4}", 1, 1000, PCT_ERR)
    g = pint(unit, r"[0-9]{1,4}", 1, 1000, UNIT_ERR)
    line = Fraction(f * c, 100)
    out = f"A {f} font at {c}% line height has a {fmt(line)} line on a baseline unit of {g}: "
    units = line / g
    if units.denominator == 1:
        return out + f"that is exactly {plural(units.numerator,'unit','units')}."
    shown = fmt(units)
    k = 1
    while k * g < line: k += 1   # smallest whole number of units that reaches the line
    up = k * g
    return out + f"that is {shown} {'unit' if shown == '1' else 'units'}. The next whole-unit line height is {up}, which is {fmt(Fraction(up * 100, f))}% of the font size."

def measure(width, cwt, length):
    w = pint(width, r"[0-9]{1,5}", 1, 10000, WIDTH_ERR)
    t = cwt.strip() if isinstance(cwt, str) else ""
    m = re.fullmatch(r"([0-9]{1,3})(?:\.([0-9]{1,2}))?", t)
    if not m: raise ValueError(CW_ERR)
    cw = Fraction(m.group(1)) + (Fraction(int((m.group(2) or "0").ljust(2, "0")), 100))
    if cw <= 0: raise ValueError(CW_ERR)
    n = pint(length, r"[0-9]{1,7}", 1, 1000000, LEN_ERR)
    cpl = 0
    while (cpl + 1) * cw <= w: cpl += 1
    show = fmt(cw)
    if cpl == 0: return f"A column {w} wide at {show} per character holds 0 characters per line, so no text fits."
    lines = 0; left = n; last = 0
    while left > 0:
        take = min(cpl, left); left -= take; lines += 1; last = take
    return f"A column {w} wide at {show} per character holds {plural(cpl,'character','characters')} per line. A text of {plural(n,'character','characters')} takes {plural(lines,'line','lines')}, and the last line holds {last}."

FNS = {"scaleTruth": scale, "rhythmTruth": rhythm, "measureTruth": measure}

def cases():
    c = []
    rnd = random.Random(695)
    for a in [["16","3/2","5"],["16","5/4","3"],["1","200/1","10"],["1000","1/1","1"],["16","1/1","2"],["10","200/199","10"],["16"," 3 / 2 ","1"],["0","3/2","5"],["1001","3/2","5"],["16","2/3","5"],["16","3/0","5"],["16","201/1","5"],
              ["16","3/2","0"],["16","3/2","11"],["16","3-2","5"],["16","","5"],["abc","3/2","5"],["16","1.5","5"],["7","7/5","4"],["12","18/11","6"],["16","3/2","1"]]:
        c.append(("scaleTruth", a))
    for _ in range(30):
        q = rnd.randint(1, 200); p = rnd.randint(q, 200)
        c.append(("scaleTruth", [str(rnd.randint(1, 1000)), f"{p}/{q}", str(rnd.randint(1, 10))]))
    for a in [["17","150","8"],["16","150","8"],["16","150","24"],["16","100","16"],["1","1","1000"],["1000","1000","1"],["1000","1000","1000"],["10","99","1"],["10","100","10"],["3","333","1"],
              ["0","150","8"],["16","0","8"],["16","150","0"],["1001","150","8"],["16","1001","8"],["16","150","1001"],["x","150","8"],[" 17 "," 150 "," 8 "],["16","","8"],["20","125","4"],["7","143","3"]]:
        c.append(("rhythmTruth", a))
    for _ in range(40):
        c.append(("rhythmTruth", [str(rnd.randint(1, 100)), str(rnd.randint(50, 300)), str(rnd.randint(1, 40))]))
    for a in [["640","8.4","1200"],["640","8","1280"],["640","8","1281"],["640","8","1"],["5","8.4","100"],["8","8","8"],["7","8","8"],["10000","0.01","1000000"],["10000","999.99","5"],["640","8.40","1200"],["640","08.4","1200"],
              ["0","8.4","1200"],["10001","8.4","1200"],["640","0","1200"],["640","0.00","1200"],["640","1000","1200"],["640","8.456","1200"],["640","-8","1200"],["640","8.","1200"],["640",".5","1200"],["640","8.4","0"],["640","8.4","1000001"],[" 640 "," 8.4 "," 1200 "],["x","8.4","1200"]]:
        c.append(("measureTruth", a))
    for _ in range(40):
        c.append(("measureTruth", [str(rnd.randint(1, 2000)), f"{rnd.randint(1, 30)}.{rnd.randint(0, 99):02d}", str(rnd.randint(1, 5000))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
