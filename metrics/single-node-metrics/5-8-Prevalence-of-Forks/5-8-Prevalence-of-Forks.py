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
        'ForkLength'         : 'int',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    dtype=dtypes_blocks)

# 5.8 preval. of forks
# 2 things, A and B:
# A) number of: blocks  TOTAL BLOCKS,    Main /  Uncle (unrec) / Uncle (recognized)
# B) forks of various lengths.

total_blocks = len(blocks)
print("Total Blocks: ", total_blocks)

print("--")
print("min block-num:", blocks['Number'].min())
print("max block-num:", blocks['Number'].max())
print("num of unique block numbers:", int(blocks['Number'].max()) - int(blocks['Number'].min()) +1)
print("--")

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


for x in range(1, 4):
    print("fork len", x, ":", len(uncles[uncles.ForkLength == x]))
    print("fork len", x, "& Unrecognized:", len(uncles[(uncles.ForkLength == x) & (uncles.BlockType == "Uncle")]))
    print("fork len", x, "& RECOGNIZED:", len(uncles[(uncles.ForkLength == x) & (uncles.BlockType == "Recognized")]))
    print("--")
    #print(uncles[uncles.ForkLength == x])

print("fork len >= 4:", len(uncles[uncles.ForkLength >= 4]))
