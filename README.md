# news-image-20261121-bot-v6

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261121-green.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page for **Saturday 21 November 2026**: 40 stories,
7 regions, every one dated that Saturday. v1 restored and sharpened — the
winner's editorial backbone (Riyadh lead, BepiColombo at 18:24 UTC, COP31
overtime) with exact verified numbers and a punchy, honest DATE CHECK.

## Run

```sh
python3 draw.py   # renders entry.png (1024x1024, deterministic)
python3 main.py   # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

`draw.py` needs Pillow (local rendering only). `main.py` is stdlib-only.
