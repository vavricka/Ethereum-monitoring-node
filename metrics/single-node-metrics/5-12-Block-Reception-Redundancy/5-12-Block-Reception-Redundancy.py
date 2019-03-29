#!/usr/bin/python3
import pandas as pd
import numpy as np

BLOCKS_LOG =  "blocks.log.FINAL"
ANNOUN_LOG = "blocksAnnouncements.log"

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
        }

dtypes_announ = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'         : 'object',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'],
    dtype=dtypes_blocks,  usecols=['BlockHash'])

announ = pd.read_csv(ANNOUN_LOG, 
    names=['LocalTimeStamp','BlockHash'],
    dtype=dtypes_announ,  usecols=['BlockHash'])

blck_total = blocks.append(announ)

#computes how many times the same blockHash was received per msgType
#msgType -- block received via NewBlockMsg or NewBlockHashesMsg or combined
def print_info(msgType):
    #occurencies = pd.value_counts(msgType.value_counts().values)
    #for i, row in occurencies.iteritems():
    #    print("In total", row, "blocks were received", i, "times")
    print("Avg number of block reception", msgType['BlockHash'].value_counts().values.mean())
    print("Median number of block reception", np.median(msgType['BlockHash'].value_counts().values)  )


print("BLOCKS are propagated using 2 different message types",
"NewBlockMsg and NewBlockHashesMsg.")

print("####### blocks.log:")
print_info(blocks)

print("####### block announ:")
print_info(announ)

print("####### blocks and block announ together:")
print_info(blck_total)
