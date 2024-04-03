# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:57:23 2024

Plots a time series of pressure beneath a fiber strain plot on shared axis

@author: Nate
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({'font.size': 32})

# # https://plotly.com/python/contour-plots/ uses contour module from plotly, see link for more info

### Setup Fiber ###############################################################

### read in .pkl files. change file path if in different path or PC.

position = pd.read_pickle(r"file_path")
values = pd.read_pickle(r"file_path")
time = pd.read_pickle(r"file_path")
values = values.fillna(0)
std = values.values.std(ddof=1)
position = position.values.flatten()
time = time.values.flatten()
values = values.values.T

### gages and times of interest

g1, g2 =  1553, 4749 ### gage range
t1, t2 = 0, 6460 ### correponds to timestep
position = position - position[g1]
strain = values[g1:g2,t1]
deck = position[g1:g2]

### Setup Pressure ############################################################

# Replace 'file_path.csv' with the path to your .csv file
file_path = r'file_path'
df = pd.read_csv(file_path)

# replace 'column_name' with the name of the column in your .csv
p_time = df['column_name'].values
pressure = df['column_name'].values

### plotting ##################################################################


fig = plt.figure(figsize=(24,12))
gs = gridspec.GridSpec(2, 2, width_ratios=[30, 1], height_ratios=[2,1])

### Fiber #####################################################################

X, Y = np.meshgrid(time[t1:t2], position[g1:g2])

ax = plt.subplot(gs[0, 0])
color_plot = ax.pcolormesh(X, Y, values[g1:g2, t1:t2], cmap='bwr', vmax = 2*std, vmin = -2*std)
ax.set_ylabel('Position along fiber (m)')
ax.set_title("Strain in FIBER_NAME")

cax = plt.subplot(gs[0, 1])
cbar = plt.colorbar(color_plot, cax=cax, label=r'microstrain ($\mu\varepsilon$)')
cbar.set_ticks([-2*std, -600, -300, 0, 300, 600, 2*std])  # Set the positions of the ticks
cbar.set_ticklabels(['C(-)', '-600', '-300', '0', '300', '600', 'T(+)'])  # Set the labels corresponding to the ticks
# Set the position of the ticks and labels
cbar.ax.xaxis.set_ticks_position('top')

### Pressure ##################################################################

ax1 = plt.subplot(gs[1,0],sharex=ax)
ax1.plot(p_time,-pressure,color='black')
ax1.set_xlabel('Time Elapsed (sec)')
ax1.set_ylabel('Pressure')
plt.grid()

plt.tight_layout() 
plt.show()