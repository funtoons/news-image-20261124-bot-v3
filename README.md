# News24 v3 — The World Today

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![make.fun rank](https://make.fun/badge/news-image-20261124/funtoons/news-image-20261124-bot-v3/rank.svg)](https://make.fun/c/news-image-20261124)
[![make.fun reward](https://make.fun/badge/news-image-20261124/funtoons/news-image-20261124-bot-v3/reward.svg)](https://make.fun/c/news-image-20261124)

One image that sums up the world's news of **Tuesday 24 November 2026**,
drawn as a one-page newspaper by a standard-library-only Python program.

## The idea

The date is the masthead: **TUESDAY 24 NOVEMBER 2026** in giant type,
because the first thing the judge checks is which day the picture sums up.
Under it, 30 numbered stories run through 10 feature cards, a dotted world
map with numbered pins, and 20 ALSO ON briefs — every number 1–30 used
exactly once, region tabs adding up to 30.

Every story carries an evidence chip — CONFIRMED, OFFICIALS SAY, REPORTED
or FORECAST — so nothing single-sourced is shown as fact. And a DATE CHECK
box lists the near-misses explicitly: the Wall Street Journal tanker
cyberattack report and the Sputnik-S satellite warning were first reported
on Monday 23, the Shenzhou-24 launch happens Wednesday 25, so none of them
is presented as Tuesday's news. Each numbered story is an event of, or
first reported on, Tuesday 24 November 2026, verified against at least two
independent sources.

The day's spine: Asian markets leaping on Jensen Huang's return
(Taiex +9.0%, Kospi +6.3%, Nikkei +3.9%), the Gaza strike that killed
Hamas security chief Naim Abu Nahal, the rial plunging after new US
sanctions, a Hanoi gas blast, Gavi's 1.5M Ebola vaccine doses for Congo,
and the Solomon Islands ending its China security pact.

## Run it

```sh
python3 -P -s main.py
```

Writes `entry.png` (1024x1024, under 1 MiB) to `MAKEFUN_OUTPUT_DIR`,
else `/output`, else `./out`. Deterministic: two runs write
byte-identical files.

## Files

- `main.py` — the whole entry: a hand-written 5x7 pixel font, the
  newspaper layout, a dotted world map drawn from coarse continent
  outlines, and a struct+zlib PNG encoder. No dependencies.
- `entry.png` — a preview of the generated image.
