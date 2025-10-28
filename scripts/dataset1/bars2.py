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
width = 0.65

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
    "SLAM System": ["RTABMap-SLAM\n(LiDAR)", "ORB-SLAM\n(RGBD)", "DROID-SLAM\n(RGBD)", "ORB-SLAM3\n(Mono)", "DROID-SLAM\n(Mono)", "MASt3R-SLAM\n(Mono)", "AnyFeature-VSLAM\n(Mono)"],
    "Peak CPU (%)": [78, 66, 62, 32, 45, 32, 71],
    "Peak Memory (%)": [65, 45, 75, 72, 63, 52, 55],
    "Peak I/O (%)": [46, 27, 31, 60, 52, 57, 25],
    "Peak GPU Usage (%)": [6, 2, 5, 98, 97, 98, 4]
}

# create figure and axes from above config
df = pd.DataFrame(data)

# Plot the data with adjusted bar width and spacing
thing = df.plot(x="SLAM System", kind="bar", ax=ax)

# plt.title("Peak Resource Usage by SLAM Systems", fontsize=16)
plt.ylabel("Resource Utilisation (%)", fontsize=7.5)
# plt.xlabel("SLAM Algorithm", fontsize=7.5) # Add xlabel for clarity
plt.xticks(rotation=40, ha="right", fontsize=7.5)
plt.yticks(fontsize=6)
plt.legend(
    fontsize=5.75,       # font size
    labelspacing=0.1, # vertical spacing between entries
    handlelength=1, # length of lines in legend
    handleheight=0.95,   # height of line box
    markerscale=0.35,  # scale of markers
    borderaxespad=0.2 # padding around legend
)

# Move x tick labels right
offset = mtransforms.ScaledTranslation(6/72, 4/72, fig.dpi_scale_trans)
for label in ax.get_xticklabels():
    label.set_transform(label.get_transform() + offset)

ax.xaxis.label.set_visible(False)
plt.ylim(0, 110)

# Add data labels to the bars with adjusted padding
for container in ax.containers:
    if isinstance(container, BarContainer):
        ax.bar_label(container, fmt='%d%%', label_type='edge', padding=1, fontsize=9) # Reduced padding

plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a horizontal grid

fig.tight_layout()

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
