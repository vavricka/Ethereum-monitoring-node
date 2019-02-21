#!/usr/bin/python3
import numpy as np

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd

TXS_WITHOUT_GAS="unique-unique-txs-with-gasused.log"

short = pd.read_csv(
TXS_WITHOUT_GAS,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr','GasUsed'])

#num of ALL
numAllTxs = len(short)
print("txs total:  ", numAllTxs)

numTxsGasUsedNotSet = sum(short['GasUsed'].isnull())
numGasUsedSet = numAllTxs - numTxsGasUsedNotSet
# txs with gasUsed set
print("txs with gasUsed set: ", numGasUsedSet)

# num of w/o GASused
print("txs w/o GasUsed set: ", numTxsGasUsedNotSet)

# num of w/o GASused   and validity != nil (nejakej error, proto neni gasUSED)
#numTxsGasUsedNotSetAndValidityNill = sum(short[(short['GasUsed'].isnull()) & (short['ValidityErr'] != "nil")])
#print("txs w/o GasUsed AND nejakej err: ", numTxsGasUsedNotSetAndValidityNill)
noGasUsedValidityNotNil= len((short[(short['GasUsed'].isnull()) & (short['ValidityErr'] != "nil")]))
print("num of w/o GASused   and validity != nil: ",noGasUsedValidityNotNil)

# num of w/o GASused   and validity == nil  (bez erroru -> tzn gasUsed neni nastaven protoze)
noGasUsedValidityisNil= len((short[(short['GasUsed'].isnull()) & (short['ValidityErr'] == "nil")]))
print("num of w/o GASused   and validity == nil: ", noGasUsedValidityisNil)

#PLOT PIE
df = pd.DataFrame({'num': [numGasUsedSet, noGasUsedValidityisNil , noGasUsedValidityNotNil]},
    index=['Valid TX with GasUsed set', 'Valid TX w/o GasUsed set', 'Invalid TX w/o GasUsed set'])

plot = df.plot.pie(y='num', figsize=(5, 5))

#LOCAL show
#plt.show()
#save to file
plt.savefig('5-5-AUX-Pie.pdf')
