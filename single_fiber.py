# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:22:58 2024

@author: Nate
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({'font.size': 32})

# # https://plotly.com/python/contour-plots/ uses contour module from plotly, see link for more info

### setup #####################################################################

### read in .pkl files. change file path if in different path or PC.

position = pd.read_pickle(r"pickle_path")
values = pd.read_pickle(r"pickle_path")
time = pd.read_pickle(r"pickle_path")


values = values.fillna(0)
std = values.values.std(ddof=1)

### change dataframes to arrays

position = position.values.flatten()
time = time.values.flatten()
values = values.values.T

# update values for your fiber of interest

g1, g2 =  0, 0 ### gage range
t1, t2 = 0, 0 ### correponds to timestep

# make position at steel deck start zero

position = position - position[g1]

# strain values for each cable

strain = values[g1:g2,t1]

# range of gauges to plot

deck = position[g1:g2]

### plotting ##################################################################


fig = plt.figure(figsize=(24,12))
gs = gridspec.GridSpec(1, 2, width_ratios=[30, 1])  # 2 rows, 4 columns

### FLT1 ######################################################################

X, Y = np.meshgrid(time[t1:t2], position[g1:g2])

ax1 = plt.subplot(gs[0, 0])
color_plot = ax1.pcolormesh(X, Y, values[g1:g2, t1:t2], cmap='bwr', vmax = 2*std, vmin = -2*std)
ax1.set_xlabel('Time (sec)')
ax1.set_ylabel('Position along fiber (m)')
ax1.set_title("Strain in FLB1")

cax = plt.subplot(gs[0, 1])
cbar = plt.colorbar(color_plot, cax=cax, label=r'microstrain ($\mu\varepsilon$)')
cbar.set_ticks([-2*std, -600, -300, 0, 300, 600, 2*std])  # Set the positions of the ticks
cbar.set_ticklabels(['C(-)', '-600', '-300', '0', '300', '600', 'T(+)'])  # Set the labels corresponding to the ticks
# Set the position of the ticks and labels
cbar.ax.xaxis.set_ticks_position('top')

plt.tight_layout() 
plt.show()

