#!/usr/bin/env python

# Example histogram plot
# This is based on this article: https://blog.timodenk.com/exporting-matplotlib-plots-to-latex/

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.collections import LineCollection
from scripts.reusable_code.constants import TEXTWIDTH

# The width of the plot, as a scalar to textwidth
# Check the value used after {R} in \begin{wrapfigure} for the plot is the same
width = 0.5

# Configure the size of the figure
fig_width = width * TEXTWIDTH
fig_height = fig_width * 0.6  # 3:2 aspect ratio

# Make the graph export to .pgf, to be used by LaTeX
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

# create figure and axes from above config
fig, ax = plt.subplots(figsize=(fig_width, fig_height))


# Below is some example plotting from the article:
# ------------------------------------------------
np.random.seed(19680801)

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution

rng = np.random.default_rng()

x = [rng.random() for _ in range(100)]
y = [rng.random() for _ in range(100)]
t = np.arange(len(x))  # time steps

# Try color the line differently over time
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

from matplotlib.collections import LineCollection
lc = LineCollection(segments, cmap='viridis', norm=plt.Normalize(t.min(), t.max()))
lc.set_array(t)
lc.set_linewidth(2)

ax.add_collection(lc)
ax.autoscale()

# plt.plot(x, y, color='red', linestyle='-', linewidth=1, label='RTK GPS (measured)')

plt.colorbar(lc, label='Time')

# ------------------------------------------------

# Layout:
# ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

ax.set_xlabel('X position', fontsize=9)
ax.set_ylabel('Y position', fontsize=9)

# Smaller tick labels
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)

plt.legend()

fig.tight_layout()
# Originally from the article: Tweak spacing to prevent clipping of ylabel
# fig.set_size_inches(w=0.5 * TEXTWIDTH, h=0.5 * TEXTWIDTH * 2/3)

# Generate the name of the plot based on the name of this python file
# Absolute path of the current file
current_script_file = os.path.abspath(__file__)
# Relative path from the current working directory
relative_path = os.path.relpath(current_script_file, start=os.getcwd())
filename = relative_path.removesuffix('.py').removeprefix('scripts/').replace('/', '.')

plt.savefig(f'plots/{filename}.pgf')
