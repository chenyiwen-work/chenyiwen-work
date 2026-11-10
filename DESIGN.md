# Profile artwork

The ASCII header and navigation are custom artwork inspired by [ignaciochiappero's profile](https://github.com/ignaciochiappero). The portrait is derived from this account's public avatar; underlying image rights belong to their respective holders.

## Header

Edit `scripts/render.py` and run `python scripts/render.py` to regenerate the header and navigation. They use transparent backgrounds and support reduced motion.

## Pac-Man contribution calendar

`scripts/build_pacman.py` is adapted directly from [ignaciochiappero's calendar renderer](https://github.com/ignaciochiappero/ignaciochiappero/blob/main/tools/build_pacman.py) at the user's request. Credit for the calendar design, sprites, animation timing and renderer belongs to its original author. Changes are limited to supplying the original theme constants locally and writing the SVGs to this repository's assets directory. The original animation behavior is retained.

Data belongs to `chenyiwen-work` and is read from the GitHub contribution calendar API. Only dates, aggregate daily counts and contribution levels are stored; no private repository names or commit contents are included. Visibility and counts depend on the token used to fetch the calendar.

Use **Actions → Refresh contribution calendar → Run workflow** to refresh the graph with GitHub's repository token. No scheduled refresh is configured.

Or run locally with `GH_TOKEN` set:

```sh
python scripts/fetch_calendar.py
python scripts/build_pacman.py
```

The generator validates SMIL keyframe counts, order and ranges before publishing both themes. The contribution calendar keeps the reference's original orange/coral sprites and rounded background.
