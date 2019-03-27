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

TXS_LOG = sys.argv[1] #"txs-stage-5.log"

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
        'GasUsed'           : 'object',
        'InMainBlock'       : 'object',
        'InUncleBlocks'     : 'object',
        'InOrder'           : 'object',
        'NeverCommitting'    : 'object',
        'RemoteTimeStamp'   : 'object',
        'CommitTime0'       : 'float',
        'CommitTime3'       : 'float',
        'CommitTime12'      : 'float',
        'CommitTime36'      : 'float',
        }


#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting','RemoteTimeStamp',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['Hash','CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            dtype=dtypes)

# first just basic...
print("txs:", len(txs.index))
print("min CommitTime0:", txs['CommitTime0'].min())
print("max CommitTime0:", txs['CommitTime0'].max())

print("   CommitTime0 median:", txs['CommitTime0'].median())
print("   CommitTime0 mean:", txs['CommitTime0'].mean())
print(" this is becasue maybe need drop veird vals.")

print("min CommitTime3:", txs['CommitTime3'].min())
print("max CommitTime3:", txs['CommitTime3'].max())
print("min CommitTime12:", txs['CommitTime12'].min())
print("max CommitTime12:", txs['CommitTime12'].max())
print("min CommitTime36:", txs['CommitTime36'].min())
print("max CommitTime36:", txs['CommitTime36'].max())

# num of with val set (all 4 separately)
print("txs w/ CommitTime0 set:", len(txs[    txs['CommitTime0'].notnull()       ]))   # try
print("txs w/ CommitTime3 set:", len(txs[    txs['CommitTime3'].notnull()       ]))   # try
print("txs w/ CommitTime12 set:", len(txs[    txs['CommitTime12'].notnull()       ]))   # try
print("txs w/ CommitTime36 set:", len(txs[    txs['CommitTime36'].notnull()       ]))   # try
#
##num of with all 4 val set
print("txs w/ all 4 commTimes set:", len(
    txs[  
    (txs['CommitTime0'].notnull()) &  (txs['CommitTime0'].notnull()) &
    (txs['CommitTime0'].notnull()) & (txs['CommitTime0'].notnull()) 
    ]
    ))  


# TMP  drop comm < 0     ;...hopefully not needed later.
print("txs CommitTime0 < 0:", len(txs[txs.CommitTime0 <0]))
txs = txs[txs.CommitTime0 > 0]
print("txs CommitTime3 < 0:", len(txs[txs.CommitTime3 <0]))

print("txs CommitTime12 < 0:", len(txs[txs.CommitTime12 <0]))

print("txs CommitTime36 < 0:", len(txs[txs.CommitTime36 <0]))

#TMP maybe uncomment  ..   filter  time>1000....
#txs = txs[txs.CommitTime0 < 2900]

print("txs CommitTime0 > 1000:", len(txs[txs.CommitTime0 > 1000]))
print("txs CommitTime0 > 2000:", len(txs[txs.CommitTime0 > 2000]))
print("txs CommitTime0 > 3000:", len(txs[txs.CommitTime0 > 3000]))


print("txs:", len(txs.index))
print("min CommitTime0:", txs['CommitTime0'].min())
print("max CommitTime0:", txs['CommitTime0'].max())

print("   CommitTime0 median:", txs['CommitTime0'].median())
print("   CommitTime0 mean:", txs['CommitTime0'].mean())
print("txs w/ CommitTime0 set:", len(txs[    txs['CommitTime0'].notnull()       ]))   # try





s_c0 = txs[txs.CommitTime0.notnull()].CommitTime0   #check
s_c3 = txs[txs.CommitTime3.notnull()].CommitTime3   #check
s_c12 = txs[txs.CommitTime12.notnull()].CommitTime12   #check
s_c36 = txs[txs.CommitTime36.notnull()].CommitTime36   #check

bin_seq = list(range(0,1000,1))   #TODO CHANGE !!!  set to  max CommitTIme .. eg 1000
fig, ax = plt.subplots()


counts_c0, bin_edges_c0 = np.histogram (s_c0, bins=bin_seq)
cdf_c0 = np.cumsum (counts_c0)
linec0, = ax.plot (bin_edges_c0[1:], cdf_c0/cdf_c0[-1], label='transaction inclusion')

counts_c3, bin_edges_c3 = np.histogram (s_c3, bins=bin_seq)
cdf_c3 = np.cumsum (counts_c3)
linec3, = ax.plot (bin_edges_c3[1:], cdf_c3/cdf_c3[-1], label='3 confirmations')

counts_c12, bin_edges_c12 = np.histogram (s_c12, bins=bin_seq)
cdf_c12 = np.cumsum (counts_c12)
linec12, = ax.plot (bin_edges_c12[1:], cdf_c12/cdf_c12[-1], label='12 confirmations')

counts_c36, bin_edges_c36 = np.histogram (s_c36, bins=bin_seq)
cdf_c36 = np.cumsum (counts_c36)
linec36, = ax.plot (bin_edges_c36[1:], cdf_c36/cdf_c36[-1], label='36 confirmations')


plt.xlabel('seconds')
plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
#
#plt.xscale('symlog')
ax.set_xlim(left=0)
ax.set_xlim(right=1000)
#
nums = [0,100,200,300,400,500,600,700,800,900,1000]
labels = ['0','100','200','300','400','500','600','700','800','900','1000']

plt.xticks(nums, labels)
#
###  tmp
#for q in [50, 90, 95, 100]:
#    print ("reg tx  :{}%% percentile: {}".format (q, np.percentile(s_c0, q)))
###end tmp
#
ax.legend()
#
##LOCAL show
#plt.show()
##save to file
plt.savefig('5-3.pdf')


