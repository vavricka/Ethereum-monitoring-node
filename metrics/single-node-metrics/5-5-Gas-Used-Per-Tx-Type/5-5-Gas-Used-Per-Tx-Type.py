#!/usr/bin/python3
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
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

TXS_LOG = sys.argv[1] #txs-stage-5.log     ...or 4 also..

if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

dtypes = {
        'LocalTimeStamp'    : 'object',
        'Hash'              : 'object',
        'GasLimit'          : 'object',
        'GasPrice'          : 'object',
        'Value'             : 'object',
        'Nonce'             : 'object',
        'MsgType'           : 'object',
        'Cost'              : 'object',
        'Size'              : 'object',
        'To'                : 'object',
        'From'              : 'object',
        'ValidityErr'       : 'object',
        'CapturedLocally'   : 'object',
        'GasUsed'           : 'float',
        'InMainBlock'       : 'object',
        'InUncleBlocks'     : 'object',
        'InOrder'           : 'object',
        'NeverCommitting'    : 'object',
        'CommitTime0'       : 'float',
        'CommitTime3'       : 'float',
        'CommitTime12'      : 'float',
        'CommitTime36'      : 'float',
        }

txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['Hash', 'MsgType', 'ValidityErr', 'GasUsed'],
            dtype=dtypes)

# print  txs before drop
print("Txs TOTAL: ", len(txs.index))

#print("txs['GasUsed'].isnull():", sum(txs['GasUsed'].isnull()))
#print("txs['ValidityErr'] != nil:", sum(txs['ValidityErr'] != "nil"))
#print( "gasused NULL  and valid != nil ",   len(  txs[  (txs['GasUsed'].isnull()) & (txs['ValidityErr'] != "nil") ]   )  )

# drop txs w/ GasUsed nil, validityErr != nil
condition = txs[  (txs['GasUsed'].isnull()) | (txs['ValidityErr'] != "nil") ].index
txs.drop(condition , inplace=True)

# print  txs after drop
print("Txs TOTAL (after drop): ", len(txs.index))

tx_only = txs[txs.MsgType == "TX"]
mc_only = txs[txs.MsgType == "MC"]
cc_only = txs[txs.MsgType == "CC"]

#print ("TX:", len(tx_only), tx_only.GasUsed.min(),tx_only.GasUsed.max(),tx_only.GasUsed.median(),tx_only.GasUsed.mean() )   #min max median mean
#print ("MC:", len(mc_only), mc_only.GasUsed.min(),mc_only.GasUsed.max(),mc_only.GasUsed.median(),mc_only.GasUsed.mean() )
#print ("CC:", len(cc_only), cc_only.GasUsed.min(),cc_only.GasUsed.max(),cc_only.GasUsed.median(),cc_only.GasUsed.mean() )
#
#filtered_txs = tx_only[  tx_only['GasUsed'] >  21000 ]
#print("TX and gasUsed > 21 000:", len(filtered_txs) ) 

s_tx = txs[txs.MsgType == "TX"].GasUsed
s_mc = txs[txs.MsgType == "MC"].GasUsed
s_cc = txs[txs.MsgType == "CC"].GasUsed

bin_seq = list(range(0,8000000,20)) 

fig, ax = plt.subplots()

counts_tx, bin_edges_tx = np.histogram (s_tx, bins=bin_seq)
cdf_tx = np.cumsum (counts_tx)
lineTx, = ax.plot (bin_edges_tx[1:], cdf_tx/cdf_tx[-1], label='regular transfers')

counts_mc, bin_edges_mc = np.histogram (s_mc, bins=bin_seq)
cdf_mc = np.cumsum (counts_mc)
lineMc, = ax.plot (bin_edges_mc[1:], cdf_mc/cdf_mc[-1], label='function calls')

counts_cc, bin_edges_cc = np.histogram (s_cc, bins=bin_seq)
cdf_cc = np.cumsum (counts_cc)
lineCc, = ax.plot (bin_edges_cc[1:], cdf_cc/cdf_cc[-1], label='contract creations')

plt.xlabel('Gas used (x1000)')
plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])

plt.xscale('symlog')
ax.set_xlim(left=20000)
ax.set_xlim(right=8000000)

nums = [21000,80000,160000,500000,1000000,2000000,4000000,8000000]
labels = ['21', '80', '160', '500', '1000', '2000', '4000', '8000']

plt.xticks(nums, labels)

##  tmp
for q in [50, 90, 95, 100]:
    print ("reg tx  :{}%% percentile: {}".format (q, np.percentile(s_tx, q)))
    print ("Msg call:{}%% percentile: {}".format (q, np.percentile(s_mc, q)))
    print ("con crea:{}%% percentile: {}".format (q, np.percentile(s_cc, q)))
##end tmp

ax.legend()

#LOCAL show
#plt.show()
#save to file
plt.savefig('5-5-txs-gasUsed.pdf')
