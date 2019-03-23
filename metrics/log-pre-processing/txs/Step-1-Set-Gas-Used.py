#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameters.")

TXS_LOG = sys.argv[1] #txs-stage-1.log
GAS_LOG = sys.argv[2] #txgasused.log.FINAL

if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

if not os.path.isfile(GAS_LOG):
    sys.exit(GAS_LOG, ": does not exists!")

#output of this script
TXS_OUT="txs-stage-2.log" #txs with gasUsed set

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
        'NeverCommiting'    : 'object',
        'RemoteTimeStamp'   : 'object',
        'CommitTime0'       : 'object',
        'CommitTime3'       : 'object',
        'CommitTime12'      : 'object',
        'CommitTime36'      : 'object',
        }

dtypes_gas = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'         : 'object',
        'TxHash'            : 'object',
        'GasUsed'           : 'object',
        }

#load txs
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommiting','RemoteTimeStamp',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            index_col=False, dtype=dtypes)

# load txgasused
txsgas = pd.read_csv(GAS_LOG,
    names=['LocalTimeStamp','BlockHash','TxHash','GasUsed'],
    usecols=['LocalTimeStamp','TxHash','GasUsed'],
    dtype=dtypes_gas)

#sort by txhash
txsgas = txsgas.sort_values(by=['TxHash'])
txsgas.reset_index(inplace=True, drop=True)

#loop all txs in TXS_LOG
for i in txs.index:
        txHash = txs.at[i,'Hash']
        
        # search sorted if txs is in GAS_LOG
        line = txsgas['TxHash'].searchsorted(txHash)

        try:
            #is it there? -> set GasUsed to TXS_LOG !
            if txHash == txsgas.at[line,'TxHash']:
                #print(line, txHash, "in both")
                txs.at[i,'GasUsed'] = txsgas.at[line,'GasUsed']
            #it is not there -> nothing to do here
            else:  
                #print(line, txHash, "not in txgas->", txsgas.at[line,'TxHash'])
                pass
        #it is not there -> nothing to do here
        except IndexError as e:
            #print(line, txHash, "not in txgas + err", e)
            pass

# export to new csv..
txs.to_csv(TXS_OUT, index=False, header=False)
