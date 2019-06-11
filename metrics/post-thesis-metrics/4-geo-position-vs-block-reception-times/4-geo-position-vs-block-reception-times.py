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
    dtype=dtypes_blocks)



first_receptions_per_instance = []
num_blocks = len(blocks)

first_receptions_sum = 0


for i in ['AngainorDiff', 'FalconDiff', 'S1USDiff', 'S2CNDiff']:
    first_receptions = len(blocks[(blocks[i] == 0 )])
    print("first receptions:", first_receptions, round(first_receptions/num_blocks*100,2), " %", i)
    first_receptions_per_instance.append(len( blocks[  (blocks[i] == 0 ) ] ))
    first_receptions_sum = first_receptions_sum + first_receptions
    
print("blocks:", len(blocks))
print("first receptions:", first_receptions_sum,
    "--- (", first_receptions_sum-len(blocks), "times a new block was received on more machines at the same time)")

x = ['Portugal', 'Czechia', 'USA - East', 'Taiwan']

x_pos = [i for i, _ in enumerate(x)]
bar1 = plt.barh(x_pos, first_receptions_per_instance, color='blue')

plt.ylabel("Instances")
plt.xlabel("First receptions of blocks per Ethereum instance")
plt.title("Influence of geographical position on faster new block observation")

plt.yticks(x_pos, x)

nums = [0,num_blocks/10,num_blocks/5,num_blocks*0.3,num_blocks*0.4]
labels = ['0 %','10 %','20 %','30 %','40 %']

plt.xticks(nums, labels)

#plt.show()
#save to file
plt.savefig('ptm-4-geo-position-vs-block-observ-time.pdf', bbox_inches="tight")






