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


class GpsData:
    """ Struct class to hold GPS x, y """
    def __init__(self, x, y):
        # x and y should by numpy arrays
        self.x = x
        self.y = y


class RmsePlot:
    """ Struct class to store everything we need for a single RMS error plot """
    def __init__(self, gps: GpsData, name: str, x, y, color, linestyle1: str | None = "solid", linestyle2: str | None = "dashed", lw: float | None = 1):
        self.name = name
        self.color = color
        self.linestyle1 = linestyle1
        self.linestyle2 = linestyle2
        self.lw = lw

        # x and y should by numpy arrays
        self.sqdist = (x - gps.x)**2 + (y - gps.y)**2
        self.dist = self.sqdist ** 0.5

        # overall RMSE
        self.rmse = np.sqrt(self.sqdist.mean())

        # cumulative RMSE over time
        self.cumulative_rmse = np.sqrt(np.cumsum(self.sqdist) / np.arange(1, len(self.sqdist)+1))

        # The future result of self.plot
        self.plt1: Line2D | None = None
        self.plt2: Line2D | None = None

    def plot_cumulative_rmse(self) -> Line2D:
        if self.plt1 is None:
            self.plt1, = plt.plot(range(len(self.cumulative_rmse)), self.cumulative_rmse, c=self.color, linestyle=self.linestyle1, lw=self.lw)
        return self.plt1

    def plot_distance(self) -> Line2D:
        if self.plt2 is None:
            self.plt2, = plt.plot(range(len(self.dist)), self.dist, c=self.color, linestyle=self.linestyle2, lw=self.lw)
        return self.plt2

    def legend_name_distance(self) -> str:
        return self.name + " Distance to GPS"

    def legend_name_error(self) -> str:
        return self.name + " Cumulative RMS error"


gps = GpsData(x, y)

# Add new odom plots here!
# We plot them when we construct the legend
odom_plots: List[RmsePlot] = [
    RmsePlot(gps, "RTAB-Map", color="blue",
             x=np.array([x[0]] + [rng.random() for _ in range(5)]),
             y=np.array([y[0]] + [rng.random() for _ in range(5)])),
    RmsePlot(gps, "ORB-SLAM3", color="red",
             x=np.array([x[0]] + [rng.random() for _ in range(5)]),
             y=np.array([y[0]] + [rng.random() for _ in range(5)])),
]

# create figure and axes from above config
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Below is some example plotting from the article:
# ------------------------------------------------




# Plot RTK GPS
# ------------------------------------------------
# Try color the line differently over time
# t = np.arange(len(x))  # time steps
# points = np.array([x, y]).T.reshape(-1, 1, 2)
# segments = np.concatenate([points[:-1], points[1:]], axis=1)
# lc = LineCollection(segments, cmap=cmap_name, norm=plt.Normalize(t.min(), t.max()))
# lc.set_array(t)
# lc.set_linewidth(2)
# lc.set_linestyle("solid")
# lc.set_rasterized(False)
# ax.add_collection(lc)
# ax.autoscale()
#
# # Create color bar on the side to show gradient
# cmap = plt.get_cmap(cmap_name)
# sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(t.min(), t.max()))
# sm.set_array([])  # required, but array is empty
#
# ticks = np.linspace(t.min(), t.max(), 11)
# cbar = plt.colorbar(sm, ax=ax, ticks=ticks)
# cbar.set_label("Time (s)", fontsize=9)
# cbar.ax.minorticks_off()
# cbar.ax.tick_params(labelsize=6)
# cbar.solids.set_rasterized(False)
#
# # Add the RTK GPS line to the legend with a proxy artist
# colors = cmap(np.linspace(0, 1, 256))  # RGBA array
# avg_color = colors[:, :3].mean(axis=0)  # average RGB (ignore alpha)
# proxy = Line2D([0], [0], color=avg_color, linestyle="solid", lw=1.5)  # representative color

# ------------------------------------------------

# Layout:
# ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# start_point = plt.scatter([x[0]], [y[0]], c=colors[0], marker="o", )

ax.legend(
    [odom.plot_distance() for odom in odom_plots] + [odom.plot_cumulative_rmse() for odom in odom_plots],
    [odom.legend_name_distance() for odom in odom_plots] + [odom.legend_name_error() for odom in odom_plots],
    fontsize=6,       # font size
    labelspacing=0.125, # vertical spacing between entries
    handlelength=1.5, # length of lines in legend
    handleheight=1,   # height of line box
    markerscale=0.5,  # scale of markers
    borderaxespad=0.2 # padding around legend
)
ax.set_xlabel('Time', fontsize=9)
ax.set_ylabel('Distance to GPS (m)', fontsize=9)

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

