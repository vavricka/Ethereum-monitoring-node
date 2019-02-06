#!/usr/bin/python3
import pandas as pd
import numpy as np

TXS_IN="unique-unique-txs-with-gasused.log"

txs = pd.read_csv(TXS_IN,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr', 'GasUsed'])


condition = txs[ (txs['GasUsed'] == -1) | (txs['GasUsed'].isnull()) | (txs['ValidityErr'] != "nil") ].index

txs.drop(condition , inplace=True)




print("Txs TOTAL: ", len(txs.index))
print("txs err : ", len(txs[txs.ValidityErr != "nil"]))
print("txs gaslim err (-1) : ", len(txs[txs.GasUsed == -1]))
print("txs  GasUsed not null ", len(txs[txs['GasUsed'].notnull()]))
