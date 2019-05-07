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

bin_seq = list(np.arange(0,5,0.01))
fig, ax = plt.subplots()

#concat all propag delays as in Decker's work
series_all = pd.concat([blocks['AngainorDiff'], blocks['FalconDiff'],
    blocks['S1USDiff'],blocks['S2CNDiff']], ignore_index=True)

# just one server (just testing) e.g. test separately each server to see similarity
#counts, bin_edges = np.histogram (blocks['AngainorDiff'], bins=bin_seq)
# all four servers (as in Decker's)
counts, bin_edges = np.histogram (series_all, bins=bin_seq)
plt.xlabel('Time since first block observation [s]')
ax.bar (bin_edges[:-1], counts, width=0.009)

number_of_blocks = len(blocks) # per machine
number_of_blocks_four_machines = number_of_blocks * 4

## uncomment the prints below when you need to know the percentages on Y-axis:
#print("len counts:", len(counts))
#print("counts>")
#print(counts)
#print("bin_edges>")
#print(bin_edges)
#print("num of blocks:", number_of_blocks, "blocks total (4 machines):", number_of_blocks_four_machines)
#
#print("CALCULATE PERCENTAGES FOR LABELING>")
#print("counts.max()", counts.max())
#print("percentages>")
#print("counts.max()/number_of_blocks_four_machines",   counts.max()/number_of_blocks_four_machines)
#print(" counts[4]/number_of_blocks_four_machines",    counts[4]/number_of_blocks_four_machines)
#print(" counts[9]/number_of_blocks_four_machines",    counts[9]/number_of_blocks_four_machines)
#print(" counts[16]/number_of_blocks_four_machines",    counts[16]/number_of_blocks_four_machines)

##E.g. in our measurements (1.4. - 2.5.) we have got:
#counts.max()/number_of_blocks_four_machines 0.29244668545824115
#counts[4]/number_of_blocks_four_machines 0.05448667557581951
#counts[9]/number_of_blocks_four_machines 0.04262776960481544
#counts[16]/number_of_blocks_four_machines 0.014722562242411311

# HERE - manually label y ticks according to the PERCENTAGES FOL LABELING OUTPUT
plt.yticks([counts[16], counts[9], counts[4], counts.max()],['1.5%','4.3%','5.4%','29.2%'])

plt.xscale('linear')
ax.set_xlim(left=0)
ax.set_xlim(right=0.5)

nums = [0,0.1,0.2,0.3,0.4,0.5]
labels = ['0','0.1','0.2','0.3','0.4','0.5']
plt.xticks(nums, labels)


#  median and average propag delay
np.sort(series_all)
print("median", np.median(series_all))
print("average", np.average(series_all))

# delays for first 50%/ 90%, 95%,.... of all blocks.
for q in [50, 90, 95, 98, 99, 100]:
    print (":{}%% percentile: {}".format (q, np.percentile(series_all, q)))


#LOCAL show
#plt.show()
#save to file
plt.savefig('5-1-block-propagation-time.pdf')




