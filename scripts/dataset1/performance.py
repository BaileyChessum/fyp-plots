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
import matplotlib.colors as mcol
import colorsys


# use this to preview the graph
INTERACTIVE = False
# INTERACTIVE = True

# The width of the plot, as a scalar to textwidth
# Check the value used after {R} in \begin{wrapfigure} for the plot is the same
width = 6/11

# Configure the size of the figure
fig_width = width * TEXTWIDTH
fig_height = TEXTWIDTH * 0.65 * 0.66666666  # 3:2 aspect ratio

# https://matplotlib.org/stable/users/explain/colors/colormaps.html
cmap_name = "plasma"

def plot(fig, ax):
    data = {
        "SLAM System": ["RTABMap-SLAM\n(LiDAR)", "ORB-SLAM\n(RGBD)", "DROID-SLAM\n(RGBD)", "ORB-SLAM3\n(Mono)", "DROID-SLAM\n(Mono)", "MASt3R-SLAM\n(Mono)", "AnyFeature-VSLAM\n(Mono)"],
        "Peak CPU (%)": [78, 66, 62, 32, 45, 32, 71],
        "Peak Memory (%)": [65, 45, 75, 72, 63, 52, 55],
        "Peak I/O (%)": [46, 27, 31, 60, 52, 57, 25],
        "Peak GPU Usage (%)": [6, 2, 5, 98, 97, 98, 4]
    }

    # create figure and axes from above config
    df = pd.DataFrame(data)
    x = np.arange(len(df["SLAM System"]))

    # Bar width and positions
    bar_width = 0.4/2

    # Plot the data with adjusted bar width and spacing
    # thing = df.plot(x="SLAM System", kind="bar", ax=ax)
    bars = [
        ax.bar(x + (0*bar_width) - 1.5*bar_width, df["Peak CPU (%)"], color="C0", width=bar_width, label="Peak CPU (%)"),
        ax.bar(x + (1*bar_width) - 1.5*bar_width, df["Peak Memory (%)"], color='C1', width=bar_width, label="Peak Current (A)"),
        ax.bar(x + (2*bar_width) - 1.5*bar_width, df["Peak I/O (%)"], color='C2', width=bar_width, label="Peak I/O (%)"),
        ax.bar(x + (3*bar_width) - 1.5*bar_width, df["Peak GPU Usage (%)"], color='C3', width=bar_width, label="Peak GPU Usage (%)")
    ]

    # plt.title("Peak Resource Usage by SLAM Systems", fontsize=16)
    ax.set_ylabel("Resource Utilisation (%)", fontsize=7.5)
    # plt.xlabel("SLAM Algorithm", fontsize=7.5) # Add xlabel for clarity
    ax.set_xticks(x)
    ax.set_xticklabels(df["SLAM System"], rotation=45, ha="right", fontsize=7)
    ax.tick_params(axis='y', labelsize=6)
    ax.legend(
        fontsize=6,       # font size
        labelspacing=0.125, # vertical spacing between entries
        handlelength=1, # length of lines in legend
        handleheight=1,   # height of line box
        markerscale=0.35,  # scale of markers
        borderaxespad=0.2 # padding around legend
    )

    # Move x tick labels right
    offset = mtransforms.ScaledTranslation(6/72, 4/72, fig.dpi_scale_trans)
    for label in ax.get_xticklabels():
        label.set_transform(label.get_transform() + offset)

    ax.xaxis.label.set_visible(False)
    ax.set_ylim(0, 110)

    def darken_cx(i, hs=0.05, ls=0.3, ss=0.2):
        c = plt.get_cmap("tab10")(i)
        r, g, b = mcol.to_rgb(c)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return colorsys.hls_to_rgb((h + hs * (1 if h > 0.2 and h < 0.95 else -1)) % 1.0, ls * l, 1 - (ss * (1 - s)))

    # Add data labels to the bars with adjusted padding
    for bar, i in zip(bars, range(len(bars))):
        c = darken_cx(i)

        labels = ax.bar_label(bar, fmt='%d%%', label_type='edge', padding=1, fontsize=7.5, color=c) # Reduced padding
        for label in labels:
            offset_coords = (2, 0)
            lx, ly = label.get_position()
            label.set_position((lx + offset_coords[0], ly + offset_coords[1]))

    ax.grid(axis='y', linestyle='--', alpha=0.7) # Add a horizontal grid

    fig.tight_layout()


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
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    plot(fig, ax)

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
