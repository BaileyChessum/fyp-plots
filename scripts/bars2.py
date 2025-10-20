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

# use this to preview the graph
INTERACTIVE = False
# INTERACTIVE = True

# The width of the plot, as a scalar to textwidth
# Check the value used after {R} in \begin{wrapfigure} for the plot is the same
width = 1.0

# https://matplotlib.org/stable/users/explain/colors/colormaps.html
cmap_name = "plasma"

# Configure the size of the figure
fig_width = width * TEXTWIDTH
fig_height = fig_width * 0.66666666 # 3:2 aspect ratio

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

data = {
    "SLAM System": ["RTABMap-SLAM (LiDAR)", "ORB-SLAM3 (RGBD)", "DROID-SLAM (RGBD)", "ORB-SLAM3 (Mono)", "DROID-SLAM (Mono)", "MASt3R-SLAM", "Any-Feature-VSLAM"],
    "Peak CPU (%)": [78, 66, 62, 32, 45, 32, 71],
    "Peak Memory (%)": [65, 45, 75, 72, 63, 52, 55],
    "Peak I/O (%)": [46, 27, 31, 60, 52, 57, 25],
    "Peak GPU Usage (%)": [6, 2, 5, 98, 97, 98, 4]
}

df = pd.DataFrame(data)

# Plot the data with adjusted bar width and spacing
thing = df.plot(x="SLAM System", kind="bar", ax=ax)

# plt.title("Peak Resource Usage by SLAM Systems", fontsize=16)
plt.ylabel("Percentage (%)", fontsize=9)
plt.xlabel("SLAM Algorithm", fontsize=9) # Add xlabel for clarity
plt.xticks(rotation=45, ha="right", fontsize=9)
plt.yticks(fontsize=6)
plt.legend(
    fontsize=6,       # font size
    labelspacing=0.125, # vertical spacing between entries
    handlelength=1.5, # length of lines in legend
    handleheight=1,   # height of line box
    markerscale=0.5,  # scale of markers
    borderaxespad=0.2 # padding around legend
)


# Add data labels to the bars with adjusted padding
for container in ax.containers:
    if isinstance(container, BarContainer):
        ax.bar_label(container, fmt='%d%%', label_type='edge', padding=1, fontsize=9) # Reduced padding

plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a horizontal grid

fig.tight_layout()
# Originally from the article: Tweak spacing to prevent clipping of ylabel
# fig.set_size_inches(w=0.5 * TEXTWIDTH, h=0.5 * TEXTWIDTH * 2/3)

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
