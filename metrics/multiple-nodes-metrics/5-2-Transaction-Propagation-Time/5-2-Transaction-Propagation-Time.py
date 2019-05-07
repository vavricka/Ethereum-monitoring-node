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
    sys.exit(sys.argv[0], ": expecting 1 parameter - txs-propagation-times.log.")

TXS_LOG = sys.argv[1] #"txs-propagation-times.log"
if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

##Hash,ValidityErr,AngainorTimeStamp,FalconTimeStamp,S1USTimeStamp,S2CNTimeStamp,
##FirstObservation,AngainorDiff,FalconDiff,S1USDiff,S2CNDiff
dtypes = {
        'Hash'              : 'object',
        'ValidityErr'       : 'object',
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

txs = pd.read_csv(TXS_LOG, 
    names=['Hash','ValidityErr','AngainorTimeStamp','FalconTimeStamp',
        'S1USTimeStamp','S2CNTimeStamp','FirstObservation','AngainorDiff',
        'FalconDiff','S1USDiff','S2CNDiff'],
    dtype=dtypes)


max_delay = 0.2 #txs['PositiveDif'].max()   .. mozna s 0.5. to vypadalo hezceji.
bin_seq = list(np.arange(0,max_delay,0.004))    # (0,  MAX PositiveDif,  step size) 
fig, ax = plt.subplots()

series_all = pd.concat([txs['AngainorDiff'], txs['FalconDiff'],
    txs['S1USDiff'],txs['S2CNDiff']], ignore_index=True)

counts, bin_edges = np.histogram (series_all, bins=bin_seq)
plt.xlabel('Time since first transaction observation [s]')
ax.bar (bin_edges[:-1], counts, width=0.0036)

number_of_txs = len(txs)
number_of_txs_four_machines = number_of_txs * 4

## uncomment the prints below when you need to know the percentages on Y-axis:
#print("len counts:", len(counts))
#print("counts>")
#print(counts)
#print("bin_edges>")
#print(bin_edges)
#print("num of txs:", number_of_txs, "txs total (4 machines):", number_of_txs_four_machines)
#
#print("CALCULATE PERCENTAGES FOR LABELING>")
#print("counts.max()", counts.max())
#print("percentages>")
#print("counts.max()/number_of_txs_four_machines",   counts.max()/number_of_txs_four_machines)
#print(" counts[9]/number_of_txs_four_machines",    counts[9]/number_of_txs_four_machines)
#print(" counts[10]/number_of_txs_four_machines",    counts[10]/number_of_txs_four_machines)
#print(" counts[11]/number_of_txs_four_machines",    counts[11]/number_of_txs_four_machines)
#print(" counts[0]/number_of_txs_four_machines",    counts[0]/number_of_txs_four_machines)
#print(" counts[1]/number_of_txs_four_machines",    counts[1]/number_of_txs_four_machines)
#print(" counts[2]/number_of_txs_four_machines",    counts[2]/number_of_txs_four_machines)

## E.G. results for measurement 1.4.- 2.5. is:
#counts.max() 18064760
#percentages>
#counts.max()/number_of_txs_four_machines 0.2605994631853828
# counts[9]/number_of_txs_four_machines 0.039210764797817425
# counts[10]/number_of_txs_four_machines 0.052385183962728225
# counts[11]/number_of_txs_four_machines 0.052443320125989575
# counts[0]/number_of_txs_four_machines 0.2605994631853828
# counts[1]/number_of_txs_four_machines 0.013393302540882128
# counts[2]/number_of_txs_four_machines 0.014805924753051139
#median 0.044000000000000004
#average 2975.002152156524 ---- this is very skewed and should not be accounted
#:50%% percentile: 0.044000000000000004
#:90%% percentile: 0.1
#:95%% percentile: 0.282
#:98%% percentile: 9.032
#:99%% percentile: 13127.443630006732
#:100%% percentile: 2691922.76

plt.yticks([counts[2], counts[10], counts.max()],
    ['1.5%','5.2%','26%'])   

plt.xscale('linear')
ax.set_xlim(left=0)
ax.set_xlim(right=max_delay)

nums = [0,0.05,0.1,0.15,0.2]
labels = ['0','0.05','0.1','0.15','0.2']
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
plt.savefig('5-2-tx-propagation-time.pdf')

