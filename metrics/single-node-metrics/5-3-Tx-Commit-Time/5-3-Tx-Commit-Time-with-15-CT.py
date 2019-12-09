#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
from matplotlib.pyplot import figure


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
        'CommitTime0'       : 'float',
        'CommitTime3'       : 'float',
        'CommitTime12'      : 'float',
        'CommitTime36'      : 'float',
        'CommitTime15'      : 'float',
        }


#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36','CommitTime15'],
            usecols=['Hash','CommitTime0','CommitTime3','CommitTime12','CommitTime36',
                'CommitTime15','CapturedLocally'],
            dtype=dtypes)


print("bef drop txs:", len(txs.index))
# drop txs that were not capture locally  
# leave only those that have all commitTimes set (i.e. drop the latest txs for which
# we do not have blocks)
# drop the txs from the beginning of measurement, for which we captured blocks before them
# this drop is only cosmetical as it drops so few txs that the medians and even means change by 0.01s.
condition = txs[   (txs['CapturedLocally'] != "True") | 
    (txs['CommitTime0'].isnull()) | (txs['CommitTime36'].isnull()) |
    (txs['CommitTime3'].isnull()) | (txs['CommitTime12'].isnull()) |
    (txs['CommitTime0'] < 0) ].index


txs.drop(condition , inplace=True)

# first just basic...
print("txs:", len(txs.index))



print("min CommitTime0:", txs['CommitTime0'].min())
print("max CommitTime0:", txs['CommitTime0'].max())

print("   CommitTime0 median:", txs['CommitTime0'].median())
print("   CommitTime0 mean:", txs['CommitTime0'].mean())

print("   CommitTime3 median:", txs['CommitTime3'].median())
print("   CommitTime3 mean:", txs['CommitTime3'].mean())

print("   CommitTime12 median:", txs['CommitTime12'].median())
print("   CommitTime12 mean:", txs['CommitTime12'].mean())

print("   CommitTime15 median:", txs['CommitTime15'].median())
print("   CommitTime15 mean:", txs['CommitTime15'].mean())

print("   CommitTime36 median:", txs['CommitTime36'].median())
print("   CommitTime36 mean:", txs['CommitTime36'].mean())



s_c0 = txs[txs.CommitTime0.notnull()].CommitTime0   #check
s_c3 = txs[txs.CommitTime3.notnull()].CommitTime3   #check
s_c12 = txs[txs.CommitTime12.notnull()].CommitTime12   #check
s_c15 = txs[txs.CommitTime15.notnull()].CommitTime15   #check
s_c36 = txs[txs.CommitTime36.notnull()].CommitTime36   #check

bin_seq = list(range(0,1000,1))   #TODO CHANGE !!!  set to  max CommitTIme .. eg 1000
fig, ax = plt.subplots()

#set figure size
#figure(num=None, figsize=(6, 2), dpi=600, facecolor='w', edgecolor='k')
fig.set_size_inches(6,3, forward=True)


counts_c0, bin_edges_c0 = np.histogram (s_c0, bins=bin_seq)
cdf_c0 = np.cumsum (counts_c0)
linec0, = ax.plot (bin_edges_c0[1:], cdf_c0/cdf_c0[-1], label='transaction inclusion', linestyle=':')

counts_c3, bin_edges_c3 = np.histogram (s_c3, bins=bin_seq)
cdf_c3 = np.cumsum (counts_c3)
linec3, = ax.plot (bin_edges_c3[1:], cdf_c3/cdf_c3[-1], label='3 confirmations', linestyle='--')

counts_c12, bin_edges_c12 = np.histogram (s_c12, bins=bin_seq)
cdf_c12 = np.cumsum (counts_c12)
linec12, = ax.plot (bin_edges_c12[1:], cdf_c12/cdf_c12[-1], label='12 confirmations', linestyle='-.')

counts_c15, bin_edges_c15 = np.histogram (s_c15, bins=bin_seq)
cdf_c15 = np.cumsum (counts_c15)
linec15, = ax.plot (bin_edges_c15[1:], cdf_c15/cdf_c15[-1], label='15 confirmations', linestyle='-')

counts_c36, bin_edges_c36 = np.histogram (s_c36, bins=bin_seq)
cdf_c36 = np.cumsum (counts_c36)
linec36, = ax.plot (bin_edges_c36[1:], cdf_c36/cdf_c36[-1], label='36 confirmations', linestyle=':')



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
for q in [50, 90, 95, 100]:
    print ("c0  :{}%% percentile: {}".format (q, np.percentile(s_c0, q)))

for q in [50, 90, 95, 100]:
    print ("3  :{}%% percentile: {}".format (q, np.percentile(s_c3, q)))

for q in [50, 90, 95, 100]:
    print ("12  :{}%% percentile: {}".format (q, np.percentile(s_c12, q)))

for q in [50, 90, 95, 100]:
    print ("15  :{}%% percentile: {}".format (q, np.percentile(s_c15, q)))

for q in [50, 90, 95, 100]:
    print ("c36  :{}%% percentile: {}".format (q, np.percentile(s_c36, q)))
#
ax.legend()
#
##LOCAL show
#plt.show()
##save to file

plt.tight_layout()
plt.savefig('5-3-with-15-CT-AS-WELL.pdf')


