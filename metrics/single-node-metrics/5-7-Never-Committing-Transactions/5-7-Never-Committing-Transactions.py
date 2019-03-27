#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#save to file
#import matplotlib as mpl
#mpl.use('Agg')
#
#import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

TXS_LOG = sys.argv[1] #"txs-stage-5.log"

if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

dtypes = {
        'LocalTimeStamp'    : 'object',
        'Hash'              : 'object',
        'GasLimit'          : 'object',
        'GasPrice'          : 'float',
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
        'CommitTime0'       : 'float',
        'CommitTime3'       : 'float',
        'CommitTime12'      : 'float',
        'CommitTime36'      : 'float',
        }

#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting','RemoteTimeStamp',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['NeverCommitting','ValidityErr'],
            dtype=dtypes)



def printMetric(txs):
    txs_all = len(txs)
    print("tot", txs_all)

    may_commit = sum(txs['NeverCommitting'].isnull())
    print("still may commit ", may_commit, "| {0:.4f}%".format(may_commit/txs_all * 100)  )

    never_commit = len(txs[(txs['NeverCommitting'] == "NeverCommitting")])
    print("will never commit ", never_commit, "| {0:.4f}%".format(never_commit/txs_all * 100)  )

    committed_txs =  len(txs[(txs['NeverCommitting'] == "Committed")])
    print("committed ", committed_txs ,   "| {0:.4f}%".format(committed_txs/txs_all * 100)  )



printMetric(txs)

print ("only valid txs:")
txs.drop(txs[(txs['ValidityErr'] != "nil")].index, inplace=True)

printMetric(txs)
