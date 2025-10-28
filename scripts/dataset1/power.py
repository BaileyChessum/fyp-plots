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

# use this to preview the graph
# INTERACTIVE = False
INTERACTIVE = True

# The width of the plot, as a scalar to textwidth
# Check the value used after {R} in \begin{wrapfigure} for the plot is the same
width = 0.5

# https://matplotlib.org/stable/users/explain/colors/colormaps.html
cmap_name = "plasma"

def plot(fig, ax1):
    data = {
        "SLAM System": ["RTABMap-SLAM\n(LiDAR)", "ORB-SLAM3\n(RGBD)", "DROID-SLAM\n(RGBD)", "ORB-SLAM3\n(Mono)", "DROID-SLAM\n(Mono)", "MASt3R-SLAM\n(Mono)", "AnyFeature-VSLAM\n(Mono)"],
        "Total Power Consumption (mW h)": [0.277778 * x for x in [10.5, 8.3, 9.5, 16.8, 17.5, 16.5, 9.0]],
        "Peak Current": [2.1, 1.7, 1.9, 3.4, 3.5, 3.3, 1.8],
    }

    df = pd.DataFrame(data)

    # Bar width and positions
    bar_width = 0.35
    x = np.arange(len(df["SLAM System"]))

    # Bar width and positions
    # Plot Total Power Consumption (primary y-axis)
    bars1 = ax1.bar(x - bar_width/2, df["Total Power Consumption (mW h)"], color="C0", width=bar_width, label="Total Power Consumption (mW h)")

    # ax1.set_xlabel("SLAM Algorithm", fontsize=9)
    ax1.set_ylabel("Total Power Consumption (mW h)", color='C0', fontsize=7.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df["SLAM System"], rotation=45, ha="right", fontsize=7)
    ax1.tick_params(axis='y', labelsize=6, labelcolor='C0')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Secondary y-axis for Peak Current
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + bar_width/2, df["Peak Current"], width=bar_width, color='C3', label="Peak Current (A)")

    ax2.set_ylabel("Peak Current (A)", color='C3', fontsize=7.5)
    ax2.tick_params(axis='y', labelcolor='C3', labelsize=6)

    # Legends
    lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    # ax1.legend(lines, labels, fontsize=6, labelspacing=0.125, handlelength=1.2, handleheight=1, markerscale=0.5, borderaxespad=0.2)

    plt.legend(
    lines, labels,
        fontsize=5.25,       # font size
        labelspacing=0.1, # vertical spacing between entries
        handlelength=1, # length of lines in legend
        handleheight=1,   # height of line box
        markerscale=0.35,  # scale of markers
        borderaxespad=0.2,
    )

    # Add data labels
    for container, fmt in zip([bars1, bars2], ['%.1fmW h', '%.1fA']):
        ax = ax1 if container == bars1 else ax2
        labels = ax.bar_label(container, fmt=fmt, label_type='edge', padding=1, fontsize=7.5, rotation=35)

        # Create a small translation transform (e.g. 5 points right, 3 points up)
        offset_coords = (-7, 1) if container == bars1 else (-5.5, -1.75)
        # offset = mtransforms.ScaledTranslation(offset_coords[0], offset_coords[1], ax.figure.dpi_scale_trans)
        for label in labels:
            label.set_horizontalalignment('left')
            lx, ly = label.get_position()
            label.set_position((lx + offset_coords[0], ly + offset_coords[1]))
            label.set_color("C0" if container == bars1 else "C3")
            #label.set_transform(label.get_transform() + offset)

    Y_AXIS_SCALE = 1.2
    ax1.set_ylim(0, max(df["Total Power Consumption (mW h)"]) * Y_AXIS_SCALE)
    ax2.set_ylim(0, max(df["Peak Current"]) * Y_AXIS_SCALE)

    # Move x tick labels right
    offset = mtransforms.ScaledTranslation(6/72, 4/72, fig.dpi_scale_trans)
    for label in ax1.get_xticklabels():
        label.set_transform(label.get_transform() + offset)
    ax1.xaxis.label.set_visible(False)

    fig.tight_layout()


if __name__ == "__main__":
    # Configure the size of the figure
    fig_width = width * TEXTWIDTH
    fig_height = TEXTWIDTH * 0.65 * 0.66666  # 3:2 aspect ratio

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
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
    plot(fig, ax1)

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
