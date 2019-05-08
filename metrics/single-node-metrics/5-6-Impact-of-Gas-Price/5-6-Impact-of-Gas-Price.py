#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

import inspect


#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

TXS_LOG = sys.argv[1] #"txs-stage-5.log"

if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

dtypes = {
        'LocalTimeStamp'    : 'object',
        'Hash'              : 'object',
        'GasLimit'          : 'object',
        'GasPrice'          : 'float',
        'Value'             : 'object',
        'Nonce'             : 'object',
        'MsgType'           : 'object',
        'Cost'              : 'object',
        'Size'              : 'object',
        'To'                : 'object',
        'From'              : 'object',
        'ValidityErr'       : 'object',
        'CapturedLocally'   : 'object',
        'GasUsed'           : 'object',
        'InMainBlock'       : 'object',
        'InUncleBlocks'     : 'object',
        'InOrder'           : 'object',
        'NeverCommitting'    : 'object',
        'CommitTime0'       : 'float',
        'CommitTime3'       : 'float',
        'CommitTime12'      : 'float',
        'CommitTime36'      : 'float',
        }


#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            #usecols=['GasPrice','Hash','CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['GasPrice','CommitTime12','ValidityErr'],
            dtype=dtypes)



#In this metric, we analyze the correlation between the commit time and the gas
# price of a transaction which is defined by the sender. It is expected that
# high gas price will lead to a higher probability of low commit time. This
# happens because miners are incentivized to include those transactions to make
# more profit. This metric is in order to observe whether it is possible to
# speed up the commit time by offering a higher gas price.


#divide the transactions
#  into five disjoint sets according to their gas price as follows: [0, 0
# ], (0, 20), [20, 25), [25, 105), [105, +∞) in Gwei. Then, we will respectively assign the average
#  commit times between the elements of the just defined sets of transactions.

# VIA how they do it in paper ON AVAILABILITY IN BLOCKCHAIN SYSTEMS... !!   figure 6,  página 7



# drop all txs without CommitTime12  or invalid
#condition = txs[  (txs['ValidityErr'] != "nil") | (txs['CommitTime12'].isnull()) ].index
condition = txs[ txs['CommitTime12'].isnull() ].index
txs.drop(condition , inplace=True)



s_txs0        = txs[txs.GasPrice == 0].CommitTime12
s_txs0to20    = txs[(txs.GasPrice > 0) & (txs.GasPrice < 20000000000)].CommitTime12
s_txs20to25    = txs[(txs.GasPrice >= 20000000000) & (txs.GasPrice < 25000000000)].CommitTime12
s_txs25to105    = txs[(txs.GasPrice >= 25000000000) & (txs.GasPrice < 105000000000)].CommitTime12
s_txs105up    = txs[(txs.GasPrice >= 105000000000) ].CommitTime12


print("TXS all:",len(txs))

print("0:",len(s_txs0))
print("0 to 20:",   len(s_txs0to20))
print("20 to 25:",  len(s_txs20to25))
print("25 to 105:", len(s_txs25to105))
print("105Gwei+:",  len(s_txs105up))


max_delay = 200000

bin_seq = list(range(0,max_delay,10))   #TODO increase for 1 month last. logs (10000 good for 4-days)
fig, ax = plt.subplots()

counts_txs0, bin_edges_txs0 = np.histogram (s_txs0, bins=bin_seq)
cdf_txs0 = np.cumsum (counts_txs0)
linetxs0, = ax.plot (bin_edges_txs0[1:], cdf_txs0/cdf_txs0[-1], label='0 GWei')

counts_txs0to20, bin_edges_txs0to20 = np.histogram (s_txs0to20, bins=bin_seq)
cdf_txs0to20 = np.cumsum (counts_txs0to20)
linetxs0to20, = ax.plot (bin_edges_txs0to20[1:], cdf_txs0to20/cdf_txs0to20[-1], label='(0, 20) GWei')

counts_txs20to25, bin_edges_txs20to25 = np.histogram (s_txs20to25, bins=bin_seq)
cdf_txs20to25 = np.cumsum (counts_txs20to25)
linetxs20to25, = ax.plot (bin_edges_txs20to25[1:], cdf_txs20to25/cdf_txs20to25[-1], label='[20, 25) GWei')

counts_txs25to105, bin_edges_txs25to105 = np.histogram (s_txs25to105, bins=bin_seq)
cdf_txs25to105 = np.cumsum (counts_txs25to105)
linetxs25to105, = ax.plot (bin_edges_txs25to105[1:], cdf_txs25to105/cdf_txs25to105[-1], label='[25, 105) GWei')

counts_txs105up, bin_edges_txs105up = np.histogram (s_txs105up, bins=bin_seq)
cdf_txs105up = np.cumsum (counts_txs105up)
lines_txs105up, = ax.plot (bin_edges_txs105up[1:], cdf_txs105up/cdf_txs105up[-1], label='[105, Inf) GWei')


plt.xlabel('seconds')
plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
#
plt.xscale('symlog')
ax.set_xlim(left=80)
ax.set_xlim(right=max_delay)    #TODO increase for 1 month last. logs
#
nums = [80,100,1000,10000,100000,200000]  #TODO increase for 1 month last. logs
labels = ['','100','1 000','10 000','100 000',' 200 000']   #TODO increase for 1 month last. logs

plt.xticks(nums, labels)



def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

for txtype in [s_txs0, s_txs0to20, s_txs20to25, s_txs25to105, s_txs105up]:
    for q in [50, 90, 95, 98, 99, 99.5, 100]:
        print (retrieve_name(txtype)[0], ":{}%% percentile: {}".format (q, np.percentile(txtype, q)))


ax.legend()


#LOCAL show
#plt.show()
##save to file
plt.savefig('5-6-Impact-of-Gas-Price-on-Commit-Time.pdf')

