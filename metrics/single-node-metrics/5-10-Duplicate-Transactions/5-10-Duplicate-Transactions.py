#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

TXS_LOG = sys.argv[1] #"txs-stage-5.log"

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
        'CommitTime0'       : 'float',
        'CommitTime3'       : 'float',
        'CommitTime12'      : 'float',
        'CommitTime36'      : 'float',
        }


#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['InMainBlock','InUncleBlocks'],
            dtype=dtypes)

print( "num of txs total:")
TXS_TOTAL = len(txs)
print(TXS_TOTAL)

print( "num of txs THAT ARE  in some MAIN")
print(  len(  txs[  txs['InMainBlock'].notnull() ]    ))

print( "num of txs THAT are not in any MAIN")
print(len(txs[   pd.isnull( txs.InMainBlock )   ] )  )


print( "num of txs THAT are not in any UNCLE")
print(len(txs[   pd.isnull( txs.InUncleBlocks )   ] )  )


print( "num of txs THAT ARE  in some UNCLE")
print(  len(  txs[  txs['InUncleBlocks'].notnull() ]    ))



print("------ THE ACTUAL metric starts here:")



# not dup tx ---   inMain=True  InBlocks == 1  (= only in MAIN)
DUP_TXS = len(  txs[  (txs['InUncleBlocks'].notnull()) &   (txs['InMainBlock'].notnull())     ]    )
print( "Duplicate txs:")
print(DUP_TXS)


#last calculate proportions..
print("the proportion of duplicate txs to all txs in main-blocks is:", DUP_TXS/TXS_TOTAL, "  |",
    DUP_TXS, "/", TXS_TOTAL)

