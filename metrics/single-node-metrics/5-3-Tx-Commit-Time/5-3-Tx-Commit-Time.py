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
        'NeverCommiting'    : 'object',
        'RemoteTimeStamp'   : 'object',
        'CommitTime0'       : 'object',
        'CommitTime3'       : 'object',
        'CommitTime12'      : 'object',
        'CommitTime36'      : 'object',
        }


#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommiting','RemoteTimeStamp',
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

#num of with all 4 val set
print("txs w/ all 4 commTimes set:", len(
    txs[  
    (txs['CommitTime0'].notnull()) &  (txs['CommitTime0'].notnull()) &
    (txs['CommitTime0'].notnull()) & (txs['CommitTime0'].notnull()) 
    ]
    ))  








#PLOTS   First draft TODO !


s_c0 = txs[txs.CommitTime0.notnull()].CommitTime0   #check
s_c3 = txs[txs.CommitTime3.notnull()].CommitTime3   #check
s_c12 = txs[txs.CommitTime12.notnull()].CommitTime12   #check
s_c36 = txs[txs.CommitTime36.notnull()].CommitTime36   #check

bin_seq = list(range(0,8000000,20))   #dif nums !!!!!! TODO
fig, ax = plt.subplots()


counts_c0, bin_edges_c0 = np.histogram (s_c0, bins=bin_seq)
cdf_c0 = np.cumsum (counts_c0)
linec0, = ax.plot (bin_edges_c0[1:], cdf_c0/cdf_c0[-1], label='commit time 0')

counts_c3, bin_edges_c3 = np.histogram (s_c3, bins=bin_seq)
cdf_c3 = np.cumsum (counts_c3)
linec3, = ax.plot (bin_edges_c3[1:], cdf_c3/cdf_c3[-1], label='commit time 3')

counts_c12, bin_edges_c12 = np.histogram (s_c12, bins=bin_seq)
cdf_c12 = np.cumsum (counts_c12)
linec12, = ax.plot (bin_edges_c12[1:], cdf_c12/cdf_c12[-1], label='commit time 12')

counts_c36, bin_edges_c36 = np.histogram (s_c36, bins=bin_seq)
cdf_c36 = np.cumsum (counts_c36)
linec36, = ax.plot (bin_edges_c36[1:], cdf_c36/cdf_c36[-1], label='commit time 36')


plt.xlabel('xlabel')
plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])

plt.xscale('symlog')
ax.set_xlim(left=20000)
ax.set_xlim(right=8000000)

nums = [21000,80000,160000,500000,1000000,2000000,4000000,8000000]
labels = ['21', '80', '160', '500', '1000', '2000', '4000', '8000']

plt.xticks(nums, labels)

##  tmp
for q in [50, 90, 95, 100]:
    print ("reg tx  :{}%% percentile: {}".format (q, np.percentile(s_c0, q)))
##end tmp

ax.legend()

#LOCAL show
#plt.show()
#save to file
plt.savefig('5-5-txs-gasUsed.pdf')


