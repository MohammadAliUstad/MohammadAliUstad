# Profile README generators

Python scripts that build the animated SVGs in `../assets/`. Run from this folder:

```
pip install pillow
python build_banner.py   # banner-vN.svg (artwork, lightning, Outfit font)
python build_stats.py    # stats.svg
python build_stack.py    # tech-stack-vN.svg (icons from Simple Icons, in si/)
```

When the banner changes, bump its file name (and the README reference): GitHub caches README images by name.
`font/` holds Outfit (SIL OFL) subsets with only the letters in use; re-subset with `pyftsubset` if the text changes.
