# news-image-22

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/kitulaja7/news-image-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/kitulaja7/news-image-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page that sums up Sunday 22 November 2026 in a single
1024×1024 image: 35 stories — three features (the COP31 collapse in Antalya, the
Kyiv apartment strike, tankers ablaze in the Strait of Hormuz), ten illustrated
tiles, a world map with 13 pins, a DATE CHECK grid and an ALSO TODAY list. Every
illustration carries a source chip showing its status (REPORTED / OFFICIAL /
CONFIRMED) and the news agency it came from, so the verification is visible on
the page itself instead of hidden in small print.

The image is drawn at build time by `render.py` (Pillow, development only) and
committed as `entry.png`. The shipped entrypoint `main.py` uses only the Python
standard library and copies `entry.png` byte-for-byte to `/output/entry.png`,
so the grader's two runs produce identical bytes with no network and no
third-party imports.

## Run it

    python3 render.py        # draw entry.png (development, needs Pillow)
    python3 main.py          # copy entry.png to /output/entry.png

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122

## Verify

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    python3 -c "import hashlib; print(hashlib.sha256(open('out/entry.png','rb').read()).hexdigest())"

Run `main.py` twice and compare the hashes: they must match. The image is
1024×1024 and under 1 MiB.
