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


#sort delays from the smallest
series_all = np.sort(series_all)

#tmp out:
print ( "len series", len(series_all))

#delete first 1/4 of delays
#because they are zero, they are from the node that
#received the msg and thus must not be accounted
series_all = series_all[len(series_all)//4:]
#tmp pit
print ( "len series", len(series_all))


# just one server (just testing) e.g. test separately each server to see similarity
#counts, bin_edges = np.histogram (blocks['AngainorDiff'], bins=bin_seq)
# all four servers (as in Decker's)
counts, bin_edges = np.histogram (series_all, bins=bin_seq)
number_of_blocks = len(blocks) # per machine
number_of_blocks_three_machines = number_of_blocks * 3

#plt.title("Block propagation")
plt.ylabel("PDF")

plt.xlabel('Time since first block observation [ms]')
ax.bar (bin_edges[:-1], counts, width=0.009)


## uncomment the prints below when you need to know the percentages on Y-axis:
#print("len counts:", len(counts))
#print("counts>")
#print(counts)
#print("bin_edges>")
#print(bin_edges)
#print("num of blocks:", number_of_blocks, "blocks total (3 machines):", number_of_blocks_three_machines)
#
#print("CALCULATE PERCENTAGES FOR LABELING>")
#print("counts.max()", counts.max())
#print("percentages>")
#print("counts.max()/number_of_blocks_three_machines",   counts.max()/number_of_blocks_three_machines)
#print(" counts[4]/number_of_blocks_three_machines",    counts[4]/number_of_blocks_three_machines)
#print(" counts[2]/number_of_blocks_three_machines",    counts[2]/number_of_blocks_three_machines)
#print(" counts[0]/number_of_blocks_three_machines",    counts[0]/number_of_blocks_three_machines)
#print(" counts[14]/number_of_blocks_three_machines",    counts[14]/number_of_blocks_three_machines)
#print(" counts[18]/number_of_blocks_three_machines",    counts[18]/number_of_blocks_three_machines)
#print(" counts[22]/number_of_blocks_three_machines",    counts[22]/number_of_blocks_three_machines)
#print(" counts[21]/number_of_blocks_three_machines",    counts[21]/number_of_blocks_three_machines)
#print(" counts[20]/number_of_blocks_three_machines",    counts[20]/number_of_blocks_three_machines)
#print(" counts[17]/number_of_blocks_three_machines",    counts[17]/number_of_blocks_three_machines)

#E.g. in our measurements (1.4. - 2.5.) we have got:
#counts.max()/number_of_blocks_three_machines 0.07264890076775934
# counts[4]/number_of_blocks_three_machines 0.07264890076775934
# counts[2]/number_of_blocks_three_machines 0.0661785349309915
# counts[0]/number_of_blocks_three_machines 0.056595580610988204
# counts[14]/number_of_blocks_three_machines 0.02856543922497857
# counts[18]/number_of_blocks_three_machines 0.013814801921082873
# counts[22]/number_of_blocks_three_machines 0.006595767778064767
# counts[21]/number_of_blocks_three_machines 0.008102462744393411
# counts[20]/number_of_blocks_three_machines 0.009698997907472084
# counts[17]/number_of_blocks_three_machines 0.016173107085771184
#median 0.07400000000000001
#average 0.10902917934723612
#:50%% percentile: 0.07400000000000001
#:90%% percentile: 0.171
#:95%% percentile: 0.21100000000000002
#:98%% percentile: 0.267
#:99%% percentile: 0.317
#:100%% percentile: 673.7230000000001

# HERE - manually label y ticks according to the PERCENTAGES FOL LABELING OUTPUT
plt.yticks([counts[22],counts[18],counts[14], counts[0], counts[2] ,counts[4]],
    ['0.7%','1.4%','2.9%','5.6%','6.6%','7.3%'])

plt.xscale('linear')
ax.set_xlim(left=0)
ax.set_xlim(right=0.5)

nums = [0,0.1,0.2,0.3,0.4,0.5]
labels = ['0','100','200','300','400','500']
plt.xticks(nums, labels)

print("median", np.median(series_all))
print("average", np.average(series_all))

# delays for first 50%/ 90%, 95%,.... of all blocks.
for q in [50, 90, 95, 98, 99, 100]:
    print (":{}%% percentile: {}".format (q, np.percentile(series_all, q)))


#LOCAL show
#plt.show()
#save to file
plt.savefig('5-1-block-propagation-time.pdf')




