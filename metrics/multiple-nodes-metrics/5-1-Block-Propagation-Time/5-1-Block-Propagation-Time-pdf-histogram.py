import pandas as pd
import numpy as np
import sys
import os
import gc
from pathlib import Path

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter - blocks-propagation-times.log.")

BLOCKS_LOG = sys.argv[1] #"blocks-propagation-times.log"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

dtypes_blocks = {
        'BlockHash'         : 'object',
        'Number'            : 'object',
        'BlockType'         : 'object',
        'AngainorTimeStamp' : 'object',
        'FalconTimeStamp'   : 'object',
        'S1USTimeStamp'     : 'object',
        'S2CNTimeStamp'     : 'object',
        'FirstObservation'  : 'object',
        'AngainorDiff'      : 'float',
        'FalconDiff'        : 'float',
        'S1USDiff'          : 'float',
        'S2CNDiff'          : 'float',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp',
        'S1USTimeStamp','S2CNTimeStamp','FirstObservation',
        'AngainorDiff','FalconDiff','S1USDiff','S2CNDiff'],
    usecols=['AngainorDiff','FalconDiff','S1USDiff','S2CNDiff'],
    dtype=dtypes_blocks)

#concat all propag delays as in Decker's work
series_all_4 = pd.concat([blocks['AngainorDiff'], blocks['FalconDiff'],
    blocks['S1USDiff'],blocks['S2CNDiff']], ignore_index=True)

#del blocks  dataframe
del blocks
gc.collect()

# !!!!!!!   fixing fu***  pandas BUG omfg
series_all_4 = np.around(series_all_4, decimals=3)

#sort delays from the smallest
series_all_4 = np.sort(series_all_4)

#delete first 1/4 of delays
#because they are zero, they are from the node that
#received the msg and thus must not be accounted
#series_all = series_all_4[len(series_all_4)//4:].copy()
series_all = series_all_4[len(series_all_4)//4:]

#  print  numbs... dbg only
###unique, counts = np.unique(series_all, return_counts=True)
###myDict = dict(zip(unique, counts))
###for k in myDict:
###    print(myDict[k], k)

#exit(0)
# end dbg

#del series_all
#del series_all_4
#gc.collect()

fig, ax = plt.subplots()

plt.hist(series_all, density=True, bins='auto')   #bins='auto'   bins='fd'  ...the same

ax.set_xlim(left=0)
ax.set_xlim(right=0.5)
nums = [0,0.1,0.2,0.3,0.4,0.5]
labels = ['0','0.1','0.2','0.3','0.4','0.5']
plt.xticks(nums, labels)

ynums = [0,1,2,3,4,5,6,7]
ylabels = ['0','0.01','0.02','0.03','0.04','0.05','0.06','0.07']
plt.yticks(ynums, ylabels)

plt.ylabel("PDF")
plt.xlabel('Time since first block observation [s]')

#LOCAL show
#plt.show()
#save to file
plt.savefig('5-1-block-propagation-time-with-aprox-curve.pdf')




