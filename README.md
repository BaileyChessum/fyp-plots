# FYP Plots

Every `.py` file in [./scripts](./scripts) will generate a `.pgf` plot in [./plots](./plots).

### Developing a new plot

1. Copy [./scripts/histogram.py](./scripts/histogram.py) as a template. Put your new scirpt in [./scripts](./scripts)

### Rebuilding all scripts

1. Run [./build.py](./build.py) after running nix-shell on [shell.nix](./shell.nix).

```shell
./build.py
```

2. Delete all the plots on [overleaf](https://www.overleaf.com/project/683813102d4472a9b9234233)
3. Drag and drop [./plots](./plots) into [overleaf](https://www.overleaf.com/project/683813102d4472a9b9234233)
4. Recompile in overleaf

