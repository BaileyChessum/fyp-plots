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
width = 1

# https://matplotlib.org/stable/users/explain/colors/colormaps.html
cmap_name = "plasma"

# Configure the size of the figure
fig_width = width * TEXTWIDTH
fig_height = fig_width * 0.5 # 3:2 aspect ratio

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
gps_raw_data=np.load("raw_data/" + "gps_ground_truth.npz")["data"]
x = gps_raw_data[:,0]
y = gps_raw_data[:,1]

class GpsData:
    """ Struct class to hold GPS x, y """
    def __init__(self, x, y):
        # x and y should by numpy arrays
        self.x = x
        self.y = y

class RmsePlot:
    """ Struct class to store everything we need for a single RMS error plot """
    def __init__(self, gps: GpsData, name: str, raw_data, color, linestyle1: str | None = "solid", linestyle2: str | None = "dashed", lw: float | None = 1):
        self.name = name
        self.color = color
        self.linestyle1 = linestyle1
        self.linestyle2 = linestyle2
        self.lw = lw

        x = raw_data[:,0]
        y = raw_data[:,1]

        # x and y should by numpy arrays
        self.sqdist = ((x - gps.x)**2) + ((y - gps.y)**2)
        self.dist = np.sqrt(self.sqdist)

        # overall RMSE
        self.rmse = np.sqrt(self.sqdist.mean())

        # cumulative RMSE over time
        self.cumulative_rmse = np.sqrt(np.cumsum(self.sqdist) / np.arange(1, len(self.sqdist)+1))

        # The future result of self.plot
        self.plt1: Line2D | None = None
        self.plt2: Line2D | None = None

    def plot_cumulative_rmse(self, ax) -> Line2D:
        if self.plt1 is None:
            self.plt1, = ax.plot(range(len(self.cumulative_rmse)), self.cumulative_rmse, c=self.color, linestyle=self.linestyle1, lw=1.5)
        return self.plt1

    def plot_distance(self, ax) -> Line2D:
        if self.plt2 is None:
            self.plt2, = ax.plot(range(len(self.dist)), self.dist, c=self.color, linestyle=self.linestyle2, alpha=0.5, lw=0.8)
        return self.plt2

    def legend_name_distance(self) -> str:
        return self.name + " Distance to GPS"

    def legend_name_error(self) -> str:
        return self.name + " Cumulative RMS error"

class OdomPlot:
    """ Struct class to store everything we need for a single odom plot """
    def __init__(self, name: str, raw_data, color, linestyle: str | None = "solid", lw: float | None = 0.5):
        self.name = name
        self.color = color
        self.linestyle = linestyle
        self.x = raw_data[:,0]
        self.y = raw_data[:,1]
        self.lw = lw

        # The future result of self.plot
        self.plt: Line2D | None = None

    def plot(self, ax) -> Line2D:
        if self.plt is None:
            self.plt, = ax.plot(self.x, self.y, c=self.color, linestyle=self.linestyle, lw=self.lw)
        return self.plt

    def legend_name(self) -> str:
        return self.name + " Trajectory"


# Add new odom plots here!
# We plot them when we construct the legend
odom_plots: List[OdomPlot] = [
    OdomPlot("RTAB-Map",
             color="C0",
             raw_data=np.load("raw_data/" + "rtabmap_slam_traj.npz")["data"]),
    OdomPlot("ORB-SLAM3 (RGBD)",
             color="C1",
             raw_data=np.load("raw_data/" + "orb_slam3_traj.npz")["data"]),
    OdomPlot("DROID-SLAM (RGBD)",
             color="C2",
             raw_data=np.load("raw_data/" + "droid_slam_traj.npz")["data"]),
    OdomPlot("ORB-SLAM3 (Mono)",
             color="C3",
             raw_data=np.load("raw_data/" + "orb_slam3_mono_traj.npz")["data"]),
    OdomPlot("DROID-SLAM (Mono)",
             color="C4",
             raw_data=np.load("raw_data/" + "droid_slam_mono_traj.npz")["data"]),
    OdomPlot("MAST3R-SLAM",
             color="C5",
             raw_data=np.load("raw_data/" + "mast3r_slam_traj.npz")["data"]),
    OdomPlot("AnyFeature-VSLAM",
             color="C6",
             raw_data=np.load("raw_data/" + "anyfeature_slam_traj.npz")["data"]),
]

gps = GpsData(x, y)
# Add new odom plots here!
# We plot them when we construct the legend
rmse_plots: List[RmsePlot] = [
    RmsePlot(gps, "RTAB-Map",
             color="C0",
             raw_data=np.load("raw_data/" + "rtabmap_slam_traj.npz")["data"]),
    RmsePlot(gps, "ORB-SLAM3 (RGBD)",
             color="C1",
             raw_data=np.load("raw_data/" + "orb_slam3_traj.npz")["data"]),
    RmsePlot(gps, "DROID-SLAM (RGBD)",
             color="C2",
             raw_data=np.load("raw_data/" + "droid_slam_traj.npz")["data"]),
    RmsePlot(gps, "ORB-SLAM3 (Mono)",
             color="C3",
             raw_data=np.load("raw_data/" + "orb_slam3_mono_traj.npz")["data"]),
    RmsePlot(gps, "DROID-SLAM (Mono)",
             color="C4",
             raw_data=np.load("raw_data/" + "droid_slam_mono_traj.npz")["data"]),
    RmsePlot(gps, "MAST3R-SLAM",
             color="C5",
             raw_data=np.load("raw_data/" + "mast3r_slam_traj.npz")["data"]),
    RmsePlot(gps, "AnyFeature-VSLAM",
             color="C6",
             raw_data=np.load("raw_data/" + "anyfeature_slam_traj.npz")["data"]),
]

# create figure and axes from above config
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(fig_width, fig_height))

# Below is some example plotting from the article:
# ------------------------------------------------

for odom in odom_plots:
    odom.plot(ax1)

# Plot RTK GPS
# ------------------------------------------------
# Try color the line differently over time
t = np.arange(len(x))  # time steps
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments, cmap=cmap_name, norm=plt.Normalize(t.min(), t.max()))
lc.set_array(t)
lc.set_linewidth(1.5)
lc.set_linestyle("solid")
lc.set_rasterized(False)
ax1.add_collection(lc)
ax1.autoscale()

# Create color bar on the side to show gradient
cmap = plt.get_cmap(cmap_name)
sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(t.min(), t.max()))
sm.set_array([])  # required, but array is empty

ticks = np.linspace(t.min(), t.max(), 11)

# Add the RTK GPS line to the legend with a proxy artist
colors = cmap(np.linspace(0, 1, 256))  # RGBA array
avg_color = colors[:, :3].mean(axis=0)  # average RGB (ignore alpha)
proxy = Line2D([0], [0], color=avg_color, linestyle="solid", lw=1.5)  # representative color

# ------------------------------------------------

# Layout:
# ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

start_point = ax1.scatter([x[0]], [y[0]], c=colors[0], marker="o", )

ax1.legend(
    [proxy, start_point] + [odom.plot(ax1) for odom in odom_plots],
    ["RTK GPS Trajectory", "GPS \& Odom Start"] + [odom.legend_name() for odom in odom_plots],
    fontsize=6,       # font size
    labelspacing=0.125, # vertical spacing between entries
    handlelength=1.5, # length of lines in legend
    handleheight=1,   # height of line box
    markerscale=0.5,  # scale of markers
    borderaxespad=0.2 # padding around legend
)
ax1.set_xlabel('X Position (m)', fontsize=9)
ax1.set_ylabel('Y Position (m)', fontsize=9)

# ----------------------------------------------------
[odom.plot_distance(ax2) for odom in rmse_plots]
ax2.legend(
    [odom.plot_cumulative_rmse(ax2) for odom in rmse_plots],
    [odom.name for odom in rmse_plots],
    fontsize=6,       # font size
    labelspacing=0.125, # vertical spacing between entries
    handlelength=1.2, # length of lines in legend
    handleheight=1,   # height of line box
    markerscale=0.5,  # scale of markers
    borderaxespad=0.2 # padding around legend
)
# ax2.set_xlabel('Time', fontsize=9)
ax2.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False)
ax2.autoscale()

ax2.set_ylabel('Cumulative RMSE (solid) (m)\nAbsolute Trajectory Error (dashed) (m)', fontsize=7.5)
ax2.set_xlim(0, len(x)-1)

# Smaller tick labels
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax1.tick_params(axis='x', labelsize=6)  # x-axis tick labels
ax1.tick_params(axis='y', labelsize=6)  # y-axis tick labels
ax2.tick_params(axis='x', labelsize=6)  # x-axis tick labels
ax2.tick_params(axis='y', labelsize=6)  # y-axis tick labels

# plt.legend()

fig.tight_layout()

# Get the position of the main axes in figure coordinates
pos = ax2.get_position()
# Create a new Axes for the colorbar directly below it
cax_height = 0.036   # height of colorbar as fraction of figure
cax_pad = -cax_height      # gap between plot and colorbar
cax = fig.add_axes([
    pos.x0,                      # left aligned with ax
    pos.y0 - cax_height - cax_pad,  # directly below ax
    pos.width,                   # same width as ax
    cax_height                   # defined height
])

cbar = plt.colorbar(sm, ax=ax2, cax=cax, orientation="horizontal", ticks=ticks)

cbar.set_label("Time", fontsize=9)
cbar.ax.minorticks_off()
cbar.ax.tick_params(labelsize=6)
cbar.set_ticks([])            # no ticks
cbar.set_ticklabels([])       # no labels (optional, usually redundant)
cbar.ax.tick_params(size=0, labelsize=0)  # hides ticks and labels
cbar.solids.set_rasterized(False)

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

