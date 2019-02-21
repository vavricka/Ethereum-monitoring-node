#!/usr/bin/python3
import pandas as pd
import numpy as np

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
