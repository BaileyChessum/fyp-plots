#!/usr/bin/env python

# Example histogram plot
# This is based on this article: https://blog.timodenk.com/exporting-matplotlib-plots-to-latex/

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.collections import LineCollection

from scripts.reusable_code.constants import TEXTWIDTH
from matplotlib.lines import Line2D
from typing import List
from matplotlib.container import BarContainer
import pandas as pd
import matplotlib.transforms as mtransforms

from scripts.dataset1 import performance
from scripts.dataset1 import power

# use this to preview the graph
INTERACTIVE = False
# INTERACTIVE = True

# The width of the plot, as a scalar to textwidth
# Check the value used after {R} in \begin{wrapfigure} for the plot is the same
width = 1.0

# Configure the size of the figure
fig_width = width * TEXTWIDTH
fig_height = fig_width * 0.65 * 0.66666666  # 3:2 aspect ratio

# https://matplotlib.org/stable/users/explain/colors/colormaps.html
cmap_name = "plasma"

if __name__ == "__main__":
    # Make the graph export to .pgf, to be used by LaTeX
    if not INTERACTIVE:
        matplotlib.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
            "savefig.transparent": True,
            "savefig.dpi": 300,
            # prevent rasterization
        })
        matplotlib.use("pgf")
    else:
        matplotlib.use("TkAgg")

    # create figure and axes from above config
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(fig_width, fig_height), gridspec_kw={'width_ratios': [60, 50]})

    performance.plot(fig, ax1)
    power.plot(fig, ax2)

    # Generate the name of the plot based on the name of this python file
    # Absolute path of the current file
    current_script_file = os.path.abspath(__file__)
    # Relative path from the current working directory
    relative_path = os.path.relpath(current_script_file, start=os.getcwd())
    filename = relative_path.removesuffix('.py').removeprefix('scripts/').replace('/', '.')

    # Interactive preview
    if INTERACTIVE:
        plt.plot()
        plt.show()
    else:
        # Save PGF for LaTeX
        plt.savefig(f'plots/{filename}.pgf')
