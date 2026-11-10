# Profile artwork

This repository displays the public GitHub profile for `chenyiwen-work`.

The layout takes inspiration from [ignaciochiappero's terminal-style profile](https://github.com/ignaciochiappero). The SVG composition, palette, typography, navigation cards and portrait conversion were made for this profile; no artwork or source code was copied from that repository.

## Update

Edit the profile copy and colors in `scripts/render.py`, then run:

```sh
python scripts/render.py
```

Only Python's standard library is needed. The committed character portrait in `assets/portrait.txt` comes from this account's existing public avatar; its underlying image belongs to its respective rights holders. The generator does not require the original image, network access, fonts, API tokens or a scheduled workflow.

GitHub chooses the dark or light SVG through the README's `<picture>` elements. All SVG assets are self-contained. The cursor honors `prefers-reduced-motion`.
