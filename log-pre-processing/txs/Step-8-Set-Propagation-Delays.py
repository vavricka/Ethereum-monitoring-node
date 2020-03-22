#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#from sortedcontainers import SortedSet

if len(sys.argv) != 5:
    sys.exit(sys.argv[0], ": expecting 4 parameters.")

TXS_LOG = sys.argv[1] #"txs-stage-1.log.ANGAINOR"
if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

TXS_2_LOG = sys.argv[2] #"txs-stage-1.log.FALCON"
if not os.path.isfile(TXS_2_LOG):
    sys.exit(TXS_2_LOG, ": does not exists!")

TXS_3_LOG = sys.argv[3] #"txs-stage-1.log.S1-US"
if not os.path.isfile(TXS_3_LOG):
    sys.exit(TXS_3_LOG, ": does not exists!")

TXS_4_LOG = sys.argv[4] #"txs-stage-1.log.S2-CN"
if not os.path.isfile(TXS_4_LOG):
    sys.exit(TXS_4_LOG, ": does not exists!")

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

txs3 = pd.read_csv(TXS_3_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['LocalTimeStamp','Hash','ValidityErr','CapturedLocally'],
            dtype=dtypes)

txs4 = pd.read_csv(TXS_4_LOG,
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

txs3.sort_values(by=['Hash'], inplace=True)
txs3.reset_index(inplace=True, drop=True)

txs4.sort_values(by=['Hash'], inplace=True)
txs4.reset_index(inplace=True, drop=True)

#tmp print
print("txs total before drop:")
print(len(txs),len(txs2),len(txs3),len(txs4))

# drop where that or that is capturedlocally == false
condition = txs[ (txs['CapturedLocally'] == "False") | (txs2['CapturedLocally'] == "False") |\
    (txs3['CapturedLocally'] == "False") | (txs4['CapturedLocally'] == "False")].index
txs.drop(condition , inplace=True)
txs2.drop(condition , inplace=True)
txs3.drop(condition , inplace=True)
txs4.drop(condition , inplace=True)

#tmp print
print("txs total after drop:")
print(len(txs),len(txs2),len(txs3),len(txs4))


# NEW DATAFRAME  
all_txs = txs[['Hash','ValidityErr','LocalTimeStamp']].copy()
#append
all_txs = pd.concat([all_txs, txs2[['LocalTimeStamp']],
    txs3[['LocalTimeStamp']], txs4[['LocalTimeStamp']] ], axis='columns')

#rename cols
#Hash,ValidityErr,AngainorTimeStamp,FalconTimeStamp,S1USTimeStamp,S2CNTimeStamp,FirstObservation,AngainorDiff,FalconDiff,S1USDiff,S2CNDiff
all_txs.columns = ['Hash','ValidityErr','AngainorTimeStamp', 'FalconTimeStamp','S1USTimeStamp','S2CNTimeStamp']

#progress print
print("sorting done, starting for loop")
num_txs = len(all_txs)
print ("txs total:", num_txs)


all_txs = all_txs.assign(FirstObservation = np.nan, AngainorDiff = np.nan,
    FalconDiff = np.nan, S1USDiff = np.nan, S2CNDiff = np.nan)

for i in all_txs.index:
    all_txs.at[i, 'FirstObservation'] = min(pd.to_datetime(all_txs.at[i,'AngainorTimeStamp']),\
        pd.to_datetime(all_txs.at[i,'FalconTimeStamp']), pd.to_datetime(all_txs.at[i,'S1USTimeStamp']),\
        pd.to_datetime(all_txs.at[i,'S2CNTimeStamp']) )

    all_txs.at[i, 'AngainorDiff'] = (pd.to_datetime(all_txs.at[i,'AngainorTimeStamp']) - pd.to_datetime(all_txs.at[i,'FirstObservation'])).total_seconds()
    all_txs.at[i, 'FalconDiff'] = (pd.to_datetime(all_txs.at[i,'FalconTimeStamp']) - pd.to_datetime(all_txs.at[i,'FirstObservation'])).total_seconds()
    all_txs.at[i, 'S1USDiff'] = (pd.to_datetime(all_txs.at[i,'S1USTimeStamp']) - pd.to_datetime(all_txs.at[i,'FirstObservation'])).total_seconds()
    all_txs.at[i, 'S2CNDiff'] = (pd.to_datetime(all_txs.at[i,'S2CNTimeStamp']) - pd.to_datetime(all_txs.at[i,'FirstObservation'])).total_seconds()


all_txs.sort_values(by=['AngainorTimeStamp'], inplace=True)
all_txs.to_csv(TXS_OUT, index=False, header=False)
