#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#from sortedcontainers import SortedSet

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

TXS_LOG = sys.argv[1] #"txs-stage-6.log"

TXS_OUT = "txs-stage-7.log"

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

#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting','RemoteTimeStamp',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            dtype=dtypes)

#  only commited txs
committed_txs = txs.loc[txs['NeverCommitting'] == "Committed", ['From','Nonce']]  

#  sort by   From  ,  Nonce
committed_txs.sort_values(['From', 'Nonce'], ascending=[True, True], inplace=True)  # nonce   vzestup, time
# DO NOT RESET INDEX.

highest_timestamp = pd.to_datetime("1993-04-04T07:00:00.737+0000")
prev_from = ""

# indexes shared for both txs and committed_txs ...
for i in committed_txs.index:

    #NEW From
    if prev_from != txs.at[i,'From']:
        prev_from = txs.at[i,'From']
        highest_timestamp = pd.to_datetime(txs.at[i,'LocalTimeStamp'])
        txs.at[i,'InOrder'] = "True"
        continue

    if pd.to_datetime(txs.at[i, 'LocalTimeStamp']) >= highest_timestamp:
        highest_timestamp = pd.to_datetime(txs.at[i, 'LocalTimeStamp'])
        txs.at[i,'InOrder'] = "True"
    else:
        txs.at[i,'InOrder'] = "False"

#for i in txs.index:
#    print (txs.at[i,'LocalTimeStamp'],txs.at[i,'From'], txs.at[i,'Nonce'], txs.at[i,'InOrder'])

#OUT
txs.to_csv(TXS_OUT, index=False, header=False)
