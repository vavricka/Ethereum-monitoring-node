#!/usr/bin/python3
import numpy as np

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd

import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter (txs-stage-2.log).")

TXS_LOG = sys.argv[1] #txs-stage-2.log

if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

#output of this script
TXS_OUT="txs-stage-2.log" #txs with gasUsed set

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
        }

txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed'],
            index_col=False, dtype=dtypes)


#tmp leave only first 300000
#txs.drop(txs.index[300000:], inplace=True)

#tmp  leave only last 300000
#txs.drop(txs.index[:-300000], inplace=True)


#drop first 300k
txs.drop(txs.index[:300000], inplace=True)
#drop last 300k
txs.drop(txs.index[-300000:], inplace=True)

#tmp print
#print(txs)


#num of ALL
numAllTxs = len(txs)
print("txs total:  ", numAllTxs)

numTxsGasUsedNotSet = sum(txs['GasUsed'].isnull())
numGasUsedSet = numAllTxs - numTxsGasUsedNotSet
# txs with gasUsed set
print("txs with gasUsed set: ", numGasUsedSet)
# num of w/o GASused
print("txs w/o GasUsed set: ", numTxsGasUsedNotSet)

# num of w/o GASused   and validity != nil (nejakej error, proto neni gasUSED)
#numTxsGasUsedNotSetAndValidityNill = sum(txs[(txs['GasUsed'].isnull()) & (txs['ValidityErr'] != "nil")])
#print("txs w/o GasUsed AND nejakej err: ", numTxsGasUsedNotSetAndValidityNill)
noGasUsedValidityNotNil = len((txs[(txs['GasUsed'].isnull()) & (txs['ValidityErr'] != "nil")]))
print("num of w/o GASused   and validity != nil: ", noGasUsedValidityNotNil)

# num of w/o GASused   and validity == nil  (bez erroru -> tzn gasUsed neni nastaven protoze)
noGasUsedValidityisNil = len((txs[(txs['GasUsed'].isnull()) & (txs['ValidityErr'] == "nil")]))
print("num of w/o GASused   and validity == nil: ", noGasUsedValidityisNil)

#PLOT PIE
df = pd.DataFrame({'num': [numGasUsedSet, noGasUsedValidityisNil , noGasUsedValidityNotNil]},
    index=['Valid TX with GasUsed set', 'Valid TX w/o GasUsed set', 'Invalid TX w/o GasUsed set'])

plot = df.plot.pie(y='num', figsize=(5, 5))

#LOCAL show
#plt.show()

#save to file
plt.savefig('5-5-AUX-Pie.pdf')
