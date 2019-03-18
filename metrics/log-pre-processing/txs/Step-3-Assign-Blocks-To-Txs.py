#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameters.")

TXS_LOG = sys.argv[1] #txs-stage-3.log
BLOCKS_LOG = sys.argv[2] #blocks-stage-3.log

if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

#output of this script
TXS_OUT="txs-stage-4.log"

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
        'InBlocks'          : 'object',
        'InOrder'           : 'object',
        'CommitTime'        : 'object',
        'NeverCommiting'    : 'object',
        'RemoteTimeStamp'   : 'object',
        }

dtypes_blocks = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'     : 'object',
        'Number'        : 'object',
        'GasLimit'      : 'object',
        'GasUsed'       : 'object',
        'Difficulty'    : 'object',
        'Time'          : 'object',
        'Coinbase'      : 'object',
        'ParentHash'    : 'object',
        'UncleHash'     : 'object',
        'BlockSize'     : 'object',
        'ListOfTxs'     : 'object',
        'ListOfUncles'  : 'object',
        'CapturedLocally'   : 'object',
        'BlockType'         : 'object',
        }

txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InBlocks','InOrder','CommitTime','NeverCommiting',
            'RemoteTimeStamp'],
            index_col=False, dtype=dtypes)

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    usecols=['BlockHash','ListOfTxs','BlockType'],
    index_col='BlockHash', dtype=dtypes_blocks)

#(11) python3 Step-3-Assign-Blocks-To-Txs.py txs-stage-3.log blocks-stage-3.log
#(Result) txs-stage-4.log with two last params set:
#     InMainBlock ..hash of the main blocks, if the txs isn't in any, pd.nan
#     InBlocks - semicolon separated list in which this txs is located..
#  +  NeverCommiting - False in all txs with InMainBlock set..

#sort txs by Hash..
txs = txs.sort_values(by=['Hash'])
txs.reset_index(inplace=True, drop=True)

# loop in blocks (maybe entire rows!)
for i, row in blocks.iterrows():

    #SKIP BLOCKS WITH NO TXS
    if pd.isnull(row['ListOfTxs']):
        #tmp print
        print(i, "zero txs")
        continue

    txs_in_block = row['ListOfTxs'].split(";")

    #LOOP each txs in the block (skip last position since it's empty)
    for tmp_tx in txs_in_block[:-1]:        
        #is tmp_tx in txs?
        line = txs['Hash'].searchsorted(tmp_tx)

        try:
            #TXS from blocks  IS   in txs.log
            if tmp_tx == txs.at[line,'Hash']:
                
                #SET InMainBlock 
                if row['BlockType'] == "Main":
                        txs.at[line,'InMainBlock'] = i
                        txs.at[line,'NeverCommiting'] = "False"

                ## append i (hash of curr block)   to inBlocks
                tmp_inblocks = txs.at[line,'InBlocks']
                
                if pd.isnull(tmp_inblocks):
                    tmp_inblocks = i + ";"
                else:
                    tmp_inblocks = tmp_inblocks + i + ";"

                txs.at[line,'InBlocks'] = tmp_inblocks

            #it is not there -> nothing to do here
            else:
                continue
        #it is not there -> nothing to do here
        except (IndexError, KeyError) as e:
            continue

#sort txs back 
txs = txs.sort_values(by=['LocalTimeStamp'])
#txs.sort_index(inplace=True)

##out
txs.to_csv(TXS_OUT, index=False, header=False)
