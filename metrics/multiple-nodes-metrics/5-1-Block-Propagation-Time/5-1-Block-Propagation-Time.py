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
        'BlockType'            : 'object',
        'AngainorTimeStamp' : 'object',
        'FalconTimeStamp'   : 'object',
        'PositiveDif'       : 'float',
        'AngainorMinusFalcon'   : 'float',
        'FalconMinusAngainor'   : 'float',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp',
        'PositiveDif','AngainorMinusFalcon','FalconMinusAngainor'],
    #usecols=['PositiveDif','AngainorMinusFalcon','FalconMinusAngainor'],
    dtype=dtypes_blocks)

#basic info
print(len(blocks))

print("delay AngainorMinusFalcon max:", blocks['AngainorMinusFalcon'].max())
print("delay FalconMinusAngainor max:", blocks['FalconMinusAngainor'].max())

print("delay AngainorMinusFalcon min:", blocks['AngainorMinusFalcon'].min())
print("delay FalconMinusAngainor min:", blocks['FalconMinusAngainor'].min())



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
counts, bin_edges = np.histogram (blocks['PositiveDif'], bins=bin_seq)

plt.xlabel('Time since first block observation [s]')

ax.bar (bin_edges[:-1], counts, width=0.01)

number_of_blocks = len(blocks)
y_range = 20  # 5 means 1/5 -> 20%   , 20 means 100/20 -> 5%  of y line
num_of_y_dots = 5 #  range 20 -> total = 0.05..   num_dots = 5 ...    0.05 /5 = 0.0§  one dot

print("counts",len(counts), type(counts), "max", counts.max(),counts.sum(),number_of_blocks )
plt.yticks(np.arange(0, counts.max() + counts.max()/num_of_y_dots, counts.max()/num_of_y_dots ),['0','1%','2%','3%','4%','5%'])   

plt.xscale('symlog')
ax.set_xlim(left=0)
ax.set_xlim(right=1)

nums = [0,0.2,0.5,1]
labels = ['0','0.2','0.5','1']

plt.xticks(nums, labels)


#LOCAL show
plt.show()
#save to file
plt.savefig('5-1-block-propagation-time.pdf')




