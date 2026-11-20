# makefun-19nov-news-image

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/rawacana2024-del/makefun-19nov-news-image/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/rawacana2024-del/makefun-19nov-news-image/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun bounty **"Sum up 19 November's world news in one image"** ($250).

`main.py` renders a newspaper front page — **"THE WORLD — Thursday,
19 November 2026"** — summarising 11 verified world news stories from 19 November
2026 in a single square image: the Trump–Xi–Putin summit in Shenzhen as the lead story,
a "Where it happened" world map with 11 numbered dots, and 10 further story panels
(Crimea Bridge, Iran–Gulf strikes, the ICJ Rohingya ruling, Bangladesh, COP31,
Anthropic's IPO, the record Van Gogh sale, North Korea, Cyclone Akvan, and the IEA
warning on Hormuz), with sources in the footer.

## Run it

```bash
pip install Pillow
python3 main.py              # writes /output/entry.png
python3 main.py out.png      # or any path you choose
```

Pure Pillow, no network access, no bundled fonts — it uses the system DejaVu
fonts. Output is a 1024x1024 RGB PNG, 124,885 bytes (under the 1 MiB limit),
deterministic: two runs produce byte-identical output (sha256
`56ea5bc0a7fdcf2ead7365d8accd5a832bd6106147fa80be4b796d6fbf972952`).

## Pre-submit checklist (verified 20 Nov 2026)

- [x] Output is exactly 1024x1024 px (max allowed) — verified with PIL
- [x] File is 124,885 bytes, under the 1 MiB limit
- [x] Program is named `main.py` at the repo root (the grader runs
      `python3 -P -s /bot/main.py`) — verified with that exact command
- [x] Two runs give identical sha256
- [x] No network access; no bundled fonts; only Pillow + stdlib
- [x] Visual check of the render: no overlapping or clipped text, all 11
      map dots separated and readable (see `entry-preview.png`)
- [x] Repo created on GitHub (public) — https://github.com/rawacana2024-del/makefun-19nov-news-image
- [x] Entry submitted via make.fun — 20 Nov 2026

## Notes

- All 11 stories were verified against public reporting on 19 November 2026.
- Built with an AI agent (Muse) for Irpan. This repo is the entry itself;
  nothing here was submitted anywhere by the script.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
