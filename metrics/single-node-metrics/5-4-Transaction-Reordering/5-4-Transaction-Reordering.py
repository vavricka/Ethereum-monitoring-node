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

TXS_LOG = sys.argv[1] #"txs-stage-7.log"

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
            #usecols=['GasPrice','Hash','CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['NeverCommitting','From','Nonce','InOrder','CommitTime12'],
            dtype=dtypes)




def printMetric(txs):
    txs_all = len(txs)
    print("tot", txs_all)

    not_committed = sum(txs['InOrder'].isnull())
    print("not_committed ",not_committed, "| {0:.4f}%".format(not_committed/txs_all * 100)  )

    committed = txs_all - not_committed
    print("committed ",committed, "| {0:.4f}%".format(committed/txs_all * 100)  )

    print ("(proportion to committed just)")

    in_order = len(txs[(txs['InOrder'] == "True")])
    print("in_order ", in_order, "| {0:.4f}%".format(in_order/committed * 100)  )

    out_of_order =  len(txs[(txs['InOrder'] == "False")])
    print(" out_of_order ",  out_of_order ,   "| {0:.4f}%".format( out_of_order/committed * 100)  )

printMetric(txs)




# drop all txs without InOrder (those not Committed)  and  without commitTime12 set
condition = txs[  (txs['InOrder'].isnull()) | (txs['CommitTime12'].isnull()) ].index

txs.drop(condition , inplace=True)

s_in_order     = txs[txs.InOrder == "True"].CommitTime12
s_out_of_order = txs[txs.InOrder == "False"].CommitTime12

print("committed txs with 12 confirm:",len(txs))
print("in order txs:",len(s_in_order))
print("out of order txs:",   len(s_out_of_order))





bin_seq = list(range(0,1000,5))   #TODO increase for 1 month last. logs (10000 good for 4-days) .. 1 000 000 ?
fig, ax = plt.subplots()

counts_in, bin_edges_in = np.histogram (s_in_order, bins=bin_seq)
cdf_in = np.cumsum (counts_in)
linetxs0, = ax.plot (bin_edges_in[1:], cdf_in/cdf_in[-1], label='in-order')

counts_out, bin_edges_out = np.histogram (s_out_of_order, bins=bin_seq)
cdf_out = np.cumsum (counts_out)
linetxs0to20, = ax.plot (bin_edges_out[1:], cdf_out/cdf_out[-1], label='out-of-order')


plt.xlabel('seconds')
plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
#
plt.xscale('symlog')
ax.set_xlim(left=80)
ax.set_xlim(right=1000)    #TODO increase for 1 month last. logs
#
nums = [80,100,200,500,1000]  #TODO increase for 1 month last. logs
labels = ['','100','200','500','1 000']   #TODO increase for 1 month last. logs

plt.xticks(nums, labels)


def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

for txtype in [s_in_order, s_out_of_order]:
    for q in [50, 90, 95, 100]:
        print (retrieve_name(txtype)[0], ":{}%% percentile: {}".format (q, np.percentile(txtype, q)))

ax.legend()

#LOCAL show
#plt.show()
##save to file
plt.savefig('5-4-Impact-of-Ordering-on-Commit-Time.pdf')

