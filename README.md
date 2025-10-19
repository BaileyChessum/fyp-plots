# FYP Plots

Every `.py` file in [./scripts](scripts/scripts) will generate a `.pgf` plot in [./plots](./plots).

### Setting up your LSP

1. Run `nix-build`
2. Point your IDE to use `./result/bin/python3` as the python interpreter. It should get access to matplotlib, numpy.

### Developing a new plot

1. Copy [./scripts/histogram.py](scripts/scripts/histogram.py) as a template. Put your new scirpt in [./scripts](scripts/scripts)

Make sure your script is executable with `chmod +x ...`

If you put your script in a subdirectory, remember to fix any relative imports.

### Rebuilding all scripts

1. Run [./build.py](./build.py) after running nix-shell on [shell.nix](./shell.nix).

```shell
./build.py
```

2. delete all the plots on [overleaf](https://www.overleaf.com/project/683813102d4472a9b9234233)
3. drag and drop [./plots](./plots) into [overleaf](https://www.overleaf.com/project/683813102d4472a9b9234233)
4. recompile in overleaf
