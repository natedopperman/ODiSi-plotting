# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:38:03 2024

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

positionFLT1 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLT1position.pkl")
positionFLT2 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLT2position.pkl")
positionFLB1 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLB1position.pkl")
positionFLB2 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLB2position.pkl")
valuesFLT1 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLT1values.pkl")
valuesFLT2 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLT2values.pkl")
valuesFLB1 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLB1values.pkl")
valuesFLB2 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLB2values.pkl")
timeFLT1 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLT1time.pkl")
timeFLT2 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLT2time.pkl")
timeFLB1 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLB1time.pkl")
timeFLB2 = pd.read_pickle(r"C:/Users/natha/Documents/coding/deck/code/pickle/FLB2time.pkl")

valuesFLT1 = valuesFLT1.fillna(0)
valuesFLT2 = valuesFLT2.fillna(0)
valuesFLB1 = valuesFLB1.fillna(0)
valuesFLB2 = valuesFLB2.fillna(0)
stdFLT1 = valuesFLT1.values.std(ddof=1)
stdFLT2 = valuesFLT2.values.std(ddof=1)
stdFLB1 = valuesFLB1.values.std(ddof=1)
stdFLB2 = valuesFLB2.values.std(ddof=1)

### change dataframes to arrays

positionFLT1 = positionFLT1.values.flatten()
positionFLT2 = positionFLT2.values.flatten()
positionFLB1 = positionFLB1.values.flatten()
positionFLB2 = positionFLB2.values.flatten()
timeFLT1 = timeFLT1.values.flatten()
timeFLT2 = timeFLT2.values.flatten()
timeFLB1 = timeFLB1.values.flatten()
timeFLB2 = timeFLB2.values.flatten()
valuesFLT1 = valuesFLT1.values.T
valuesFLT2 = valuesFLT2.values.T
valuesFLB1 = valuesFLB1.values.T
valuesFLB2 = valuesFLB2.values.T

# setting ranges for gages and times of interest

gT11, gT12 =  445, 2189 ### flt1
gT21, gT22 =  397, 2145 ### flt2
gB11, gB12 =  410, 2164 ### flb1
gB21, gB22 =  775, 2524 ### flb2
t1, t2 = 1250, 10312 ### correponds to timestep

# make position at steel deck start zero

positionFLT1 = positionFLT1 - positionFLT1[gT11]
positionFLT2 = positionFLT2 - positionFLT2[gT21]  
positionFLB1 = positionFLB1 - positionFLB1[gB11]
positionFLB2 = positionFLB2 - positionFLB2[gB21]

# strain values for each cable

FLT1strain = valuesFLT1[gT11:gT12,t1]
FLT2strain = valuesFLT2[gT21:gT22,t1]
FLB1strain = valuesFLB1[gB11:gB12,t1]
FLB2strain = valuesFLB2[gB21:gB22,t1]

# range of gauges to plot

FLT1deck = positionFLT1[gT11:gT12]
FLT2deck = positionFLT2[gT21:gT22]
FLB1deck = positionFLB1[gB11:gB12]
FLB2deck = positionFLB2[gB21:gB22]

### plotting ##################################################################

# select which fiber to plot by commenting out the ones you don't want to plot

fig = plt.figure(figsize=(48,16))
gs = gridspec.GridSpec(2, 3, width_ratios=[10, 30, 1])  # 3 rows, 2 columns, colorbar column

### first timestamp

ax1 = plt.subplot(gs[0, 0])
# ax1.plot(FLT1deck, FLT1strain, linewidth = 2.0, color = 'r', label='FLT1')
ax1.plot(FLB1deck, FLB1strain, linewidth = 2.0, color = 'b', label='FLB1')
# ax1.plot(FLT2deck, FLT2strain, linewidth = 2.0, color = 'g', label='FLT2')
# ax1.plot(FLB2deck, FLB2strain, linewidth = 2.0, color = 'magenta', label='FLB2')
# ax1.set_xlabel('Position along fiber (m)')
ax1.set_xlabel('Position along fiber (m)')
ax1.set_ylabel('Strain ($\mu$$\epsilon$)')
ax1.set_title('Strain at t = 200 seconds')
ax1.set_ylim([-2000,1200])
plt.grid()
# plt.legend(loc='best', bbox_to_anchor=(1.12, 1))

### second timestamp

FLT1strain = valuesFLT1[gT11:gT12,t2]
FLT2strain = valuesFLT2[gT21:gT22,t2]
FLB1strain = valuesFLB1[gB11:gB12,t2]
FLB2strain = valuesFLB2[gB21:gB22,t2]

ax2 = plt.subplot(gs[1, 0],sharex=ax1)
# ax2.plot(FLT1deck, FLT1strain, linewidth = 2.0, color = 'r')
ax2.plot(FLB1deck, FLB1strain, linewidth = 2.0, color = 'b')
# ax2.plot(FLT2deck, FLT2strain, linewidth = 2.0, color = 'g')
# ax2.plot(FLB2deck, FLB2strain, linewidth = 2.0, color = 'magenta')
ax2.set_xlabel('Position along fiber (m)')
ax2.set_ylabel('Strain ($\mu$$\epsilon$)')
ax2.set_title('Strain at t = 1650 seconds')
ax2.set_ylim([-2000,1200])
plt.grid()

### Fiber Map

# X, Y = np.meshgrid(timeFLT1[0:10312], positionFLT1[gT11:gT12])
X, Y = np.meshgrid(timeFLB1[0:10312], positionFLB1[gB11:gB12])
# X, Y = np.meshgrid(timeFLT2[0:10312], positionFLT2[gT21:gT22])
# X, Y = np.meshgrid(timeFLB2[0:10312], positionFLB2[gB21:gB22])

ax3 = plt.subplot(gs[:, 1])
# color_plot = ax3.pcolormesh(X, Y, valuesFLT1[gT11:gT12, 0:10312], cmap='bwr', vmax = 1.5*stdFLT1, vmin = -1.5*stdFLB1)
color_plot = ax3.pcolormesh(X, Y, valuesFLB1[gB11:gB12, 0:10312], cmap='bwr', vmax = 1.5*stdFLB1, vmin = -1.5*stdFLB1)
# color_plot = ax3.pcolormesh(X, Y, valuesFLT2[gT21:gT22, 0:10312], cmap='bwr', vmax = 1.5*stdFLT2, vmin = -1.5*stdFLB1)
# color_plot = ax3.pcolormesh(X, Y, valuesFLB2[gB21:gB22, 0:10312], cmap='bwr', vmax = 1.5*stdFLB2, vmin = -1.5*stdFLB1)
ax3.set_xlabel('Time (sec)')
ax3.set_ylabel('Position along fiber (m)')
ax3.set_title("Strain in FLT1")

cax = plt.subplot(gs[:, 2])  # Spanning across both rows
cbar = plt.colorbar(color_plot, cax=cax, label=r'microstrain ($\mu\varepsilon$)')
# cbar.set_ticks([-1.5*stdFLT1, -800, -400, 0, 400, 800, 1.5*stdFLT1])  # Set the positions of the ticks
cbar.set_ticks([-1.5*stdFLB1, -800, -400, 0, 400, 800, 1.5*stdFLB1])  # Set the positions of the ticks
# cbar.set_ticks([-1.5*stdFLT2, -800, -400, 0, 400, 800, 1.5*stdFLT2])  # Set the positions of the ticks
# cbar.set_ticks([-1.5*stdFLB2, -800, -400, 0, 400, 800, 1.5*stdFLB2])  # Set the positions of the ticks
cbar.set_ticklabels(['C(-)', '-800', '-400', '0', '400', '800', 'T(+)'])  # Set the labels corresponding to the ticks
# Set the position of the ticks and labels
cbar.ax.xaxis.set_ticks_position('top')

plt.tight_layout() 
plt.show()

