#!/usr/bin/python3

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

BLOCKS_LOG = sys.argv[1]   # blocks-stage-4.log

#check - that log-file exists
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

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
        'CapturedLocally'   : 'bool',
        'BlockType'         : 'object',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    dtype=dtypes_blocks)

# 5.8 preval. of forks
# 2 things, A and B:
# A) number of: blocks  TOTAL BLOCKS,    Main /  Uncle (unrec) / Uncle (recognized)
# B) distinguish between forks of various lengths.

total_blocks = len(blocks)
print("Total Blocks: ", total_blocks)

num_main = len(blocks[blocks.BlockType == "Main"])
print("Main:", num_main, "rate:", num_main / total_blocks)

num_unrec_uncle = len(blocks[blocks.BlockType == "Uncle"])
print("Unrec Uncle:", num_unrec_uncle, "rate:", num_unrec_uncle / total_blocks)

num_rec_uncle = len(blocks[blocks.BlockType == "Recognized"])
print("Recognized Uncle:", num_rec_uncle, "rate:", num_rec_uncle / total_blocks)

num_uncle = num_unrec_uncle + num_rec_uncle
print("Uncle:", num_uncle, "rate:", num_uncle / total_blocks)


print("Verifying Uncle+Main", num_main + num_uncle,
    "=?", len(blocks), "blocks")





#B   forks and their lengths..
uncles = blocks[(blocks.BlockType == "Uncle") | (blocks.BlockType == "Recognized")]

uncles = uncles.assign(ForkLength = 0)  #0 means  NOT SET because the smallest fork-size is 1

current_fork_length = 1

#for each UNCLE
for i, row in uncles.iterrows():

    current_fork_length = 1

    parentHash = row.ParentHash
    
    while True:

        if blocks[blocks.BlockHash == parentHash].empty:
            print("this uncle's parent isn't in our blocks")
            print("thus we can't determine the length of this fork")
            break
        else:
            curr_block = blocks[blocks.BlockHash == parentHash]
            #Main?
            if curr_block.BlockType.values[0] == "Main":
                #reaching main... here the forks ends
                #print("FORK LENGTH:", current_fork_length) #, "index:", i)

                uncles.loc[i, 'ForkLength'] = current_fork_length
                #print(uncles.loc[i])

                break
            else:
                current_fork_length = current_fork_length + 1
                parentHash = curr_block.ParentHash.values[0]


print("fork not set:", len(uncles[uncles.ForkLength == 0]))
print("fork len 1:", len(uncles[uncles.ForkLength == 1]))
print("fork len 2:", len(uncles[uncles.ForkLength == 2]))
print("fork len 3:", len(uncles[uncles.ForkLength == 3]))
print("fork len >3:", len(uncles[uncles.ForkLength > 3]))

