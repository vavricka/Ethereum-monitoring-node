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

TXS_LOG = sys.argv[1] #txs-stage-4.log  !!

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
        'CommitTime0'       : 'object',
        'CommitTime3'       : 'object',
        'CommitTime12'      : 'object',
        'CommitTime36'      : 'object',
        }

txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting','RemoteTimeStamp',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            index_col=False, dtype=dtypes)


#tmp leave only first 300000
#txs.drop(txs.index[300000:], inplace=True)

#tmp  leave only last 300000
#txs.drop(txs.index[:-300000], inplace=True)

#drop first 300k
#txs.drop(txs.index[:300000], inplace=True)
#drop last 300k
#txs.drop(txs.index[-300000:], inplace=True)


#num of ALL
numAllTxs = len(txs)
print("txs total:  ", numAllTxs)

print("---")

numTxsGasUsedNotSet = sum(txs['GasUsed'].isnull())
numGasUsedSet = numAllTxs - numTxsGasUsedNotSet
# txs with gasUsed set
print("txs with gasUsed set: ", numGasUsedSet, numGasUsedSet/numAllTxs)


#Executed (GasUsed set) ; NotValid(ValidityErr != nil) ; Included in some block from MAINCHAIN
ExecutedNotValidMAINCHAIN = txs[(txs['GasUsed'].notnull()) & (txs['ValidityErr'] != "nil") & (txs['InMainBlock'].notnull())]
LenExecutedNotValidMAINCHAIN = len(ExecutedNotValidMAINCHAIN)
print("num of w/ GASused   and validity != nil MAIN-CHAIN!: ", LenExecutedNotValidMAINCHAIN, LenExecutedNotValidMAINCHAIN/numAllTxs)

ExecutedNotValidMAINCHAIN.to_csv("Aux-step4-A-ExecutedNotValidMAINCHAIN.csv", index=False, header=True)


ExecutedNotValidNotMAINCHAIN = txs[(txs['GasUsed'].notnull()) & (txs['ValidityErr'] != "nil") & (txs['InMainBlock'].isnull())]
LenExecutedNotValidNotMAINCHAIN = len(ExecutedNotValidNotMAINCHAIN)
print("num of w/ GASused   and validity != nil not-MAIN-CHAIN jen pro kontr: ", LenExecutedNotValidNotMAINCHAIN, LenExecutedNotValidNotMAINCHAIN/numAllTxs)

ExecutedNotValidNotMAINCHAIN.to_csv("Aux-step4-B-ExecutedNotValidNotMAINCHAIN.csv", index=False, header=True)


# num of w/o GASused   and validity == nil  (bez erroru -> tzn gasUsed neni nastaven protoze)
GasUsedValidityisNil = len((txs[(txs['GasUsed'].notnull()) & (txs['ValidityErr'] == "nil")]))
print("num of w/ GASused   and validity == nil: ", GasUsedValidityisNil, GasUsedValidityisNil/numAllTxs)



print("---")

# num of w/o GASused
print("txs w/o GasUsed set: ", numTxsGasUsedNotSet, numTxsGasUsedNotSet/numAllTxs)
# num of w/o GASused   and validity != nil (nejakej error, proto neni gasUSED)
#numTxsGasUsedNotSetAndValidityNill = sum(txs[(txs['GasUsed'].isnull()) & (txs['ValidityErr'] != "nil")])
#print("txs w/o GasUsed AND nejakej err: ", numTxsGasUsedNotSetAndValidityNill)
noGasUsedValidityNotNil = len((txs[(txs['GasUsed'].isnull()) & (txs['ValidityErr'] != "nil")]))
print("num of w/o GASused   and validity != nil: ", noGasUsedValidityNotNil, noGasUsedValidityNotNil/numAllTxs)

# num of w/o GASused   and validity == nil  (bez erroru -> tzn gasUsed neni nastaven protoze)
noGasUsedValidityisNil = len((txs[(txs['GasUsed'].isnull()) & (txs['ValidityErr'] == "nil")]))
print("num of w/o GASused   and validity == nil: ", noGasUsedValidityisNil, noGasUsedValidityisNil/numAllTxs)





#PLOT PIE
#df = pd.DataFrame({'num': [numGasUsedSet, noGasUsedValidityisNil , noGasUsedValidityNotNil]},
#    index=['Valid TX with GasUsed set', 'Valid TX w/o GasUsed set', 'Invalid TX w/o GasUsed set'])
#
#plot = df.plot.pie(y='num', figsize=(5, 5))



#LOCAL show
#plt.show()

#save to file
#plt.savefig('5-5-AUX-Pie.pdf')
