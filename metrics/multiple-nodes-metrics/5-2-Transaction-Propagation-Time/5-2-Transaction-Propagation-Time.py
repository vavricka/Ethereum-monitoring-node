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


max_delay = 0.5 #txs['PositiveDif'].max()   .. mozna s 0.5. to vypadalo hezceji.
bin_seq = list(np.arange(0,max_delay,0.01))    # (0,  MAX PositiveDif,  step size) 
fig, ax = plt.subplots()

series_all = pd.concat([txs['AngainorDiff'], txs['FalconDiff'],
    txs['S1USDiff'],txs['S2CNDiff']], ignore_index=True)

counts, bin_edges = np.histogram (series_all, bins=bin_seq)
number_of_txs = len(txs)
number_of_txs_three_machines = number_of_txs * 3

# remove one whole machine from the bucket with zero delay
# this is because this is the machine that captured the
# message and so it does not count
print("counts0", counts[0])
counts[0] = counts[0] - number_of_txs
print("counts0", counts[0])

plt.xlabel('Time since first transaction observation [s]')
ax.bar (bin_edges[:-1], counts, width=0.009)


## uncomment the prints below when you need to know the percentages on Y-axis:
#print("len counts:", len(counts))
#print("counts>")
#print(counts)
#print("bin_edges>")
#print(bin_edges)
#print("num of txs:", number_of_txs, "txs total (4 machines):", number_of_txs_three_machines)
#
#print("CALCULATE PERCENTAGES FOR LABELING>")
#print("counts.max()", counts.max())
#print("percentages>")
#print(" counts[14]/number_of_txs_three_machines",    counts[14]/number_of_txs_three_machines)
#print(" counts[13]/number_of_txs_three_machines",    counts[13]/number_of_txs_three_machines)
#print(" counts[12]/number_of_txs_three_machines",    counts[12]/number_of_txs_three_machines)
#print(" counts[11]/number_of_txs_three_machines",    counts[11]/number_of_txs_three_machines)
#print(" counts[10]/number_of_txs_three_machines",    counts[10]/number_of_txs_three_machines)
#print(" counts[9]/number_of_txs_three_machines",    counts[9]/number_of_txs_three_machines)
#print(" counts[8]/number_of_txs_three_machines",    counts[8]/number_of_txs_three_machines)
#print(" counts[7]/number_of_txs_three_machines",    counts[7]/number_of_txs_three_machines)
#print(" counts[6]/number_of_txs_three_machines",    counts[6]/number_of_txs_three_machines)
#print(" counts[5]/number_of_txs_three_machines",    counts[5]/number_of_txs_three_machines)
#print(" counts[0]/number_of_txs_three_machines",    counts[0]/number_of_txs_three_machines)
#print(" counts[1]/number_of_txs_three_machines",    counts[1]/number_of_txs_three_machines)
#print(" counts[2]/number_of_txs_three_machines",    counts[2]/number_of_txs_three_machines)
#print(" counts[3]/number_of_txs_three_machines",    counts[3]/number_of_txs_three_machines)
#print(" counts[4]/number_of_txs_three_machines",    counts[4]/number_of_txs_three_machines)

## E.G. results for measurement 1.4.- 2.5. is:
#counts.max() 7299951
#percentages>
# counts[14]/number_of_txs_three_machines 0.0033688584240646976
# counts[13]/number_of_txs_three_machines 0.005119694618283915
# counts[12]/number_of_txs_three_machines 0.011888513592465785
# counts[11]/number_of_txs_three_machines 0.0356846213643139
# counts[10]/number_of_txs_three_machines 0.07594977612528098
# counts[9]/number_of_txs_three_machines 0.1282668797075746
# counts[8]/number_of_txs_three_machines 0.08479653256495502
# counts[7]/number_of_txs_three_machines 0.05390654340068954
# counts[6]/number_of_txs_three_machines 0.058616159275968666
# counts[5]/number_of_txs_three_machines 0.12042683580683713
# counts[0]/number_of_txs_three_machines 0.03674434408222425
# counts[1]/number_of_txs_three_machines 0.04399387074614231
# counts[2]/number_of_txs_three_machines 0.04237513684117999
# counts[3]/number_of_txs_three_machines 0.07302888833557751
# counts[4]/number_of_txs_three_machines 0.14041063461897443
#median 0.044000000000000004
#average 2975.002152156524
#:50%% percentile: 0.044000000000000004
#:90%% percentile: 0.1
#:95%% percentile: 0.282
#:98%% percentile: 9.032
#:99%% percentile: 13127.443630006732
#:100%% percentile: 2691922.76


plt.yticks([counts[0], counts[1], counts[3], counts[4], counts[5], counts[12]],
    ['3.7%','4.4%','7.3%','14%','12%','1.2%'])   

plt.xscale('linear')
ax.set_xlim(left=0)
ax.set_xlim(right=max_delay)

nums = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
labels = ['0','0.05','0.1','0.15','0.2','0.25','0.3','0.35','0.4','0.45','0.5']
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

