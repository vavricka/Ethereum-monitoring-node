#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#from sortedcontainers import SortedSet

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameters.")

TXS_LOG = sys.argv[1] #"txs-stage-6.log.ANGAINOR"
if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

TXS_2_LOG = sys.argv[2] #"txs-stage-6.log.FALCON"
if not os.path.isfile(TXS_2_LOG):
    sys.exit(TXS_2_LOG, ": does not exists!")

TXS_OUT = "txs-propagation-times.log"

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
        'CommitTime0'       : 'object',
        'CommitTime3'       : 'object',
        'CommitTime12'      : 'object',
        'CommitTime36'      : 'object',
        }

txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['LocalTimeStamp','Hash','ValidityErr','CapturedLocally'],
            dtype=dtypes)

txs2 = pd.read_csv(TXS_2_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['LocalTimeStamp','Hash','ValidityErr','CapturedLocally'],
            dtype=dtypes)


# they both have the same number of txs ....    should sort  by hash   so indexes point to the same block
txs.sort_values(by=['Hash'], inplace=True)
txs.reset_index(inplace=True, drop=True)

txs2.sort_values(by=['Hash'], inplace=True)
txs2.reset_index(inplace=True, drop=True)

# drop where that or that is capturedlocally == false
condition = txs[ (txs['CapturedLocally'] == False) | (txs2['CapturedLocally'] == False) ].index
txs.drop(condition , inplace=True)
txs2.drop(condition , inplace=True)


# NEW DATAFRAME  
all_txs = txs[['Hash','ValidityErr','LocalTimeStamp']].copy()
#append
all_txs = pd.concat([all_txs, txs2[['LocalTimeStamp']] ], axis='columns')

#rename cols
all_txs.columns = ['Hash','ValidityErr','AngainorTimeStamp', 'FalconTimeStamp']


#   add columns   (IN FOR LOOP..)
all_txs = all_txs.assign(PositiveDif = np.nan, AngainorMinusFalcon = np.nan)
for i in all_txs.index:
    all_txs.at[i, 'AngainorMinusFalcon'] = (pd.to_datetime(all_txs.at[i,'AngainorTimeStamp']) - pd.to_datetime(all_txs.at[i,'FalconTimeStamp'])).total_seconds()
    all_txs.at[i, 'PositiveDif']         = abs(all_txs.at[i, 'AngainorMinusFalcon'])


# would be better like this but   .total_seconds() makes trouble here
#all_txs = all_txs.assign(AngainorMinusFalcon =     pd.to_datetime(all_txs['AngainorTimeStamp']) - pd.to_datetime(all_txs['FalconTimeStamp'])    )
#all_txs = all_txs.assign(AngainorMinusFalcon = lambda x: pd.to_datetime(x.AngainorTimeStamp) - pd.to_datetime(x.FalconTimeStamp)    ) #.total_seconds()   



all_txs.sort_values(by=['AngainorTimeStamp'], inplace=True)
all_txs.to_csv(TXS_OUT, index=False, header=False)
