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
fig_height = fig_width * 0.8 # 3:2 aspect ratio

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

# Some random gps data for testing
np.random.seed(19680801)
rng = np.random.default_rng()
x = [rng.random() for _ in range(6)]
y = [rng.random() for _ in range(6)]

class OdomPlot:
    """ Struct class to store everything we need for a single odom plot """
    def __init__(self, name: str, x, y, color, linestyle: str | None = None, lw: float | None = 1):
        self.name = name
        self.color = color
        self.linestyle = linestyle
        self.x = x
        self.y = y
        self.lw = lw

        # The future result of self.plot
        self.plt: Line2D | None = None

    def plot(self) -> Line2D:
        if self.plt is None:
            self.plt, = plt.plot(self.x, self.y, c=self.color, linestyle=self.linestyle, lw=self.lw)
        return self.plt

    def legend_name(self) -> str:
        return self.name + " Trajectory"


# Add new odom plots here!
# We plot them when we construct the legend
odom_plots: List[OdomPlot] = [
    OdomPlot("RTAB-Map", color="blue", linestyle="dashed",
             x=[x[0]] + [rng.random() for _ in range(5)],
             y=[y[0]] + [rng.random() for _ in range(5)]),
    OdomPlot("ORB-SLAM3", color="red", linestyle="dashed",
             x=[x[0]] + [rng.random() for _ in range(5)],
             y=[y[0]] + [rng.random() for _ in range(5)]),
]

# create figure and axes from above config
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Below is some example plotting from the article:
# ------------------------------------------------




# Plot RTK GPS
# ------------------------------------------------
# Try color the line differently over time
t = np.arange(len(x))  # time steps
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments, cmap=cmap_name, norm=plt.Normalize(t.min(), t.max()))
lc.set_array(t)
lc.set_linewidth(2)
lc.set_linestyle("solid")
lc.set_rasterized(False)
ax.add_collection(lc)
ax.autoscale()

# Create color bar on the side to show gradient
cmap = plt.get_cmap(cmap_name)
sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(t.min(), t.max()))
sm.set_array([])  # required, but array is empty

ticks = np.linspace(t.min(), t.max(), 11)
cbar = plt.colorbar(sm, ax=ax, ticks=ticks)
cbar.set_label("Time (s)", fontsize=9)
cbar.ax.minorticks_off()
cbar.ax.tick_params(labelsize=6)
cbar.solids.set_rasterized(False)

# Add the RTK GPS line to the legend with a proxy artist
colors = cmap(np.linspace(0, 1, 256))  # RGBA array
avg_color = colors[:, :3].mean(axis=0)  # average RGB (ignore alpha)
proxy = Line2D([0], [0], color=avg_color, linestyle="solid", lw=1.5)  # representative color

# ------------------------------------------------

# Layout:
# ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

start_point = plt.scatter([x[0]], [y[0]], c=colors[0], marker="o", )

ax.legend(
    [proxy, start_point] + [odom.plot() for odom in odom_plots],
    ["RTK GPS Trajectory", "GPS \& Odom Start"] + [odom.legend_name() for odom in odom_plots],
    fontsize=8,       # font size
    labelspacing=0.2, # vertical spacing between entries
    handlelength=1.5, # length of lines in legend
    handleheight=1,   # height of line box
    markerscale=0.5,  # scale of markers
    borderaxespad=0.2 # padding around legend
)
ax.set_xlabel('X Position (m)', fontsize=9)
ax.set_ylabel('Y Position (m)', fontsize=9)

# Smaller tick labels
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)

# plt.legend()

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

