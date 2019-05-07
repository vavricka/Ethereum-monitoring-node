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


max_delay = 0.5
bin_seq = list(np.arange(0,max_delay,0.01))    # (0,  MAX PositiveDif,  step size) 
fig, ax = plt.subplots()

series_all = pd.concat([txs['AngainorDiff'], txs['FalconDiff'],
    txs['S1USDiff'],txs['S2CNDiff']], ignore_index=True)

#sort delays from the smallest
series_all = np.sort(series_all)

#delete first 1/4 of delays
#because they are zero, they are from the node that
#received the msg and thus must not be accounted
series_all = series_all[len(series_all)//4:]

counts, bin_edges = np.histogram (series_all, bins=bin_seq)
number_of_txs = len(txs)
number_of_txs_three_machines = number_of_txs * 3

plt.xlabel('Time since first transaction observation [s]')
ax.bar (bin_edges[:-1], counts, width=0.009)


## uncomment the prints below when you need to know the percentages on Y-axis:
#print("len counts:", len(counts))
#print("counts>")
#print(counts)
#print("bin_edges>")
#print(bin_edges)
#print("num of txs:", number_of_txs, "txs total (3 machines):", number_of_txs_three_machines)
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
# counts[14]/number_of_txs_three_machines 0.0025713399005559048
# counts[13]/number_of_txs_three_machines 0.0032606838063039606
# counts[12]/number_of_txs_three_machines 0.0046736858991096655
# counts[11]/number_of_txs_three_machines 0.010092034018455275
# counts[10]/number_of_txs_three_machines 0.033986083673951624
# counts[9]/number_of_txs_three_machines 0.08150636232745846
# counts[8]/number_of_txs_three_machines 0.14082890724305427
# counts[7]/number_of_txs_three_machines 0.0849845109681157
# counts[6]/number_of_txs_three_machines 0.059639778907545994
# counts[5]/number_of_txs_three_machines 0.08055968054635107
# counts[0]/number_of_txs_three_machines 0.041653690617323345
# counts[1]/number_of_txs_three_machines 0.04779508142092284
# counts[2]/number_of_txs_three_machines 0.05333131756165102
# counts[3]/number_of_txs_three_machines 0.10564317013565008
# counts[4]/number_of_txs_three_machines 0.16812968797950914
#median 0.06
#average 3966.669536208694
#:50%% percentile: 0.06
#:90%% percentile: 0.111
#:95%% percentile: 0.804
#:98%% percentile: 38.461
#:99%% percentile: 74121.027
#:100%% percentile: 2691922.76


plt.yticks([counts[0], counts[2], counts[3], counts[4], counts[5], counts[11]],
    ['4.1%','5.3%','10.6%','16.8%','8.1%','1%'])   

plt.xscale('linear')
ax.set_xlim(left=0)
ax.set_xlim(right=max_delay)

nums = [0,0.1,0.2,0.3,0.4,0.5]
labels = ['0','0.1','0.2','0.3','0.4','0.5']
plt.xticks(nums, labels)

#  median and average propag delay
print("median", np.median(series_all))
print("average", np.average(series_all))

# delays for first 50%/ 90%, 95%,.... of all blocks.
for q in [50, 90, 95, 98, 99, 100]:
    print (":{}%% percentile: {}".format (q, np.percentile(series_all, q)))

#LOCAL show
#plt.show()
#save to file
plt.savefig('5-2-tx-propagation-time.pdf')

