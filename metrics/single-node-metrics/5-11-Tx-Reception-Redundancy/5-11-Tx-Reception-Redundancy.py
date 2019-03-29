#!/usr/bin/python3
import pandas as pd
import numpy as np

#TXS_LOG = "txs.log.FINAL"
TXS_LOG = "txs.log.FINAL.28T00"


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
        }

txs = pd.read_csv(TXS_LOG, 
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr'], 
   usecols=['Hash'], dtype=dtypes)

# FIRST  make sure you dropped first x    txs when there were <20 peers !
# check it via peers.log ....

#txs.sort_values(by=['Hash'], inplace=True)
#txs.reset_index(inplace=True, drop=True)


vals = txs["Hash"].value_counts().values

print("Average number of tx reception",  vals.mean()  )

#print("occurenciesn",  pd.value_counts(vals)  )

print("Median number of tx reception", np.median(vals)  )

