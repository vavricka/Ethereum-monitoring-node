#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

from sortedcontainers import SortedSet

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

TXS_LOG = sys.argv[1] #"txs-stage-5.log"

TXS_OUT = "txs-stage-6.log"

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

committed_txs = txs.loc[txs['NeverCommitting'] == "Committed", ['From','Nonce']]   
uncommitted_txs = txs.loc[txs['NeverCommitting'] != "Committed", ['From','Nonce']]  

ss = SortedSet()
# create sorted series_commited_txs    of tuples  (From, Nonce)  
for i in committed_txs.index:
    tmp_tuple = (committed_txs.at[i,'From'], committed_txs.at[i,'Nonce'])
    ss.add(tmp_tuple)
#                                                                    = may-comm.
#   BEFORE       NeverCommitting  [ Committed   | nil              |   nil      ]
#   AFTER        NeverCommitting  [ Committed   | NeverCommitting  |   nil      ]

for i in uncommitted_txs.index:
    tmp_tuple = (uncommitted_txs.at[i,'From'], uncommitted_txs.at[i,'Nonce'])
    
    if tmp_tuple in ss:
        txs.at[i,'NeverCommitting'] = "NeverCommitting"

#OUT
txs.to_csv(TXS_OUT, index=False, header=False)
