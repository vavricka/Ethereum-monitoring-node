#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameter.")

TXS_LOG = sys.argv[1] #txs-stage-4.log
BLOCKS_LOG = sys.argv[2] #blocks-stage-4.log
TXS_OUT = "txs-stage-5.log"

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
        'NeverCommiting'    : 'object',
        'RemoteTimeStamp'   : 'object',
        'CommitTime0'       : 'object',
        'CommitTime3'       : 'object',
        'CommitTime12'      : 'object',
        'CommitTime36'      : 'object',
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
        'CapturedLocally'   : 'object',# obj == str;  not bool! intentional
        'BlockType'         : 'object',
        }

#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommiting','RemoteTimeStamp',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'], dtype=dtypes)

#load blocks
blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    dtype=dtypes_blocks,
    usecols=['LocalTimeStamp','BlockHash','Number','CapturedLocally','BlockType']
    )
#blocks:  #  drop  not MAIN blocks..
blocks = blocks[blocks.BlockType == "Main"]   # DROP Uncles; (= leave Main blocks only)

print("Main blocks before drop:", len(blocks))

#first sort blocks (temporarily by Number)
blocks = blocks.sort_values(by=['Number'])
blocks.reset_index(inplace=True, drop=True)

# loop through all blocks
for i in blocks.index:
    #CapturedLocally is False?
    if blocks.at[i,'CapturedLocally'] == "False":
        #mark 20 blocks around it as "Drop"
        for x in range(i - 10, i + 11):
            try:
                if blocks.at[x,'CapturedLocally'] != "False":
                    blocks.at[x,'CapturedLocally'] = "Drop"
            except KeyError:
                pass

# drop both  "False" and "Drop"  blocks
blocks = blocks[blocks.CapturedLocally == "True"]

print("Main blocks after dropping not Locally capt and their neighbours:", len(blocks))


# blocks2 = copy of blocks sorted by Num..
blocks2 = blocks.copy()

#  # blocks sort by HASH..
blocks = blocks.sort_values(by=['BlockHash'])
blocks.reset_index(inplace=True, drop=True)

#  blocks2  sort by num..
blocks2 = blocks2.sort_values(by=['Number'])
blocks2.reset_index(inplace=True, drop=True)

print("sorting done, starting for loop")
num_txs = len(txs)
print ("txs total:", num_txs)

# for every TX   in MAINblock
for i in txs.index:

    #progress bar
    if i % 500000 == 0:
        print (i)

    blockHash = txs.at[i,'InMainBlock']
    try:
        if pd.isnull(blockHash): # SKIP if tx is not in any MAIN-BLOCK
            continue
        
        #tx.InMainBlock  is in blocks? still block could be dropped
        line = blocks['BlockHash'].searchsorted(blockHash)

        #is it there? 
        if blockHash == blocks.at[line,'BlockHash']:
            #print(txs.at[i, 'LocalTimeStamp'], blocks.at[line, 'LocalTimeStamp'],
            #pd.to_datetime(blocks.at[line, 'LocalTimeStamp']) - pd.to_datetime(txs.at[i, 'LocalTimeStamp']) )
           
            for commitT in 0,3,12,36:
                block_num = int(blocks.at[line,'Number'])
                block_num2 = block_num + commitT
                block_num2 = str(block_num2)

                # is the a block with commit_block_num in blocks2?
                line2 = blocks2['Number'].searchsorted(block_num2)

                #is  block with num+(12/36/..) there?
                try:
                    if block_num2 == blocks2.at[line2,'Number']:
                        tmp_delta = pd.to_datetime(blocks2.at[line2, 'LocalTimeStamp']) - pd.to_datetime(txs.at[i, 'LocalTimeStamp'])
                        # set commit time
                        str_commitTime = "CommitTime" + str(commitT)
                        txs.at[i,str_commitTime] = tmp_delta.total_seconds()
                except (IndexError, KeyError):
                    #print("block not there err")  
                    pass
      
    #it is not there -> nothing to do here
    except (IndexError, KeyError):
        #print("block not there err")  
        pass

##out
txs.to_csv(TXS_OUT, index=False, header=False)

