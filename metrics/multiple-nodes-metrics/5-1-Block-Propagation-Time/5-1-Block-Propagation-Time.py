import pandas as pd
import numpy as np
import sys
import os
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
    #usecols=['PositiveDif','AngainorMinusFalcon','FalconMinusAngainor'],
    dtype=dtypes_blocks)

#basic info
print(len(blocks))

print("delay AngainorDiff max/min:", blocks['AngainorDiff'].max(), blocks['AngainorDiff'].min())
print("delay FalconDiff max/min:", blocks['FalconDiff'].max(), blocks['FalconDiff'].min())
print("delay S1USDiff max/min:", blocks['S1USDiff'].max(), blocks['S1USDiff'].min())
print("delay S2CNDiff max/min:", blocks['S2CNDiff'].max(), blocks['S2CNDiff'].min())


#novy srandy
#all_blocks = all_blocks.assign(AngainorMinusFalcon = np.nan)
#for i in all_blocks.index:
#    all_blocks.at[i, 'AngainorMinusFalcon'] = (pd.to_datetime(all_blocks.at[i,'AngainorTimeStamp']) - pd.to_datetime(all_blocks.at[i,'FalconTimeStamp'])).total_seconds()



## DROP blocks here

# Drop  blocks received after network outage  BASED on   TIME range ..
#blocks = all_blocks.assign(NeedDrop = np.nan)

## loop through all blocks
#for i in blocks.index:
#    #CapturedLocally is False?
#    if blocks.at[i,'PositiveDif'] >= 20:
#        print(blocks.at[i,'Number'],blocks.at[i,'AngainorTimeStamp'], blocks.at[i,'PositiveDif'])
    
#NO dropping needed, so few missed blocks..


bin_seq = list(np.arange(0,5,0.01))    # (0,  MAX PositiveDif,  step size) 

fig, ax = plt.subplots()

series_all = pd.concat([blocks['AngainorDiff'], blocks['FalconDiff'],
    blocks['S1USDiff'],blocks['S2CNDiff']], ignore_index=True)

# just one server
#counts, bin_edges = np.histogram (blocks['AngainorDiff'], bins=bin_seq)
# all together
counts, bin_edges = np.histogram (series_all, bins=bin_seq)

plt.xlabel('Time since first block observation [s]')

ax.bar (bin_edges[:-1], counts, width=0.01)

number_of_blocks = len(blocks)
#y_range = 20  # 5 means 1/5 -> 20%   , 20 means 100/20 -> 5%  of y line
num_of_y_dots = 5 #  range 20 -> total = 0.05..   num_dots = 5 ...    0.05 /5 = 0.0§  one dot

print("counts",len(counts), type(counts), "max", counts.max(),counts.sum(),number_of_blocks )
plt.yticks(np.arange(0, counts.max() + counts.max()/num_of_y_dots, counts.max()/num_of_y_dots ),['0','1%','2%','3%','12.92%','16.16%'])    #max tick

#TODO y-ticks do better..


plt.xscale('symlog')
ax.set_xlim(left=0)
ax.set_xlim(right=1)

nums = [0,0.2,0.5,1]
labels = ['0','0.2','0.5','1']

plt.xticks(nums, labels)


#LOCAL show
#plt.show()
#save to file
plt.savefig('5-1-block-propagation-time.pdf')




