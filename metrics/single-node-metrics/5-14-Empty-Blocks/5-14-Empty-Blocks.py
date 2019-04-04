#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import textdistance
from itertools import chain

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
        'ForkLength'        : 'object',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    dtype=dtypes_blocks)


# assign number of txs to every block
blocks = blocks.assign(NumTxs = 0)
for id_block, row in blocks.iterrows():
    try:
        txs = row['ListOfTxs'].split(";")
        #remove empty lines (there is always one empty line at the end of the list)
        txs = list(filter(None, txs))
        num_txs_in_uncle_block = len(txs)
    except AttributeError:
        num_txs_in_uncle_block = 0
    
    blocks.at[id_block, 'NumTxs'] = num_txs_in_uncle_block


#      num     MAIN BLOCKS
num_main_total = len(blocks[blocks.BlockType == "Main"])
#      num     MAIN BLOCKS   and zero txs
num_main_with_zero_txs = len(blocks[(blocks.BlockType == "Main") & (blocks.NumTxs == 0)])
#  calc proportion
main_proportion = num_main_with_zero_txs / num_main_total

#      num     UNCLE BLOCKS
num_uncle_total = len(blocks[blocks.BlockType != "Main"])  #  both Recognized and Uncles
#      num     UNCLE BLOCKS   and zero txs
num_uncle_with_zero_txs = len(blocks[(blocks.BlockType != "Main") & (blocks.NumTxs == 0)])
#  calc proportion
uncle_proportion = num_uncle_with_zero_txs / num_uncle_total

print("MAIN BLOCKS:", num_main_total, "EMPTY MAIN BLOCKS:", num_main_with_zero_txs,
    "proportion of empty main blocks:", main_proportion)

print("UNCLE BLOCKS:", num_uncle_total, "EMPTY UNCLE BLOCKS:", num_uncle_with_zero_txs,
    "proportion of empty uncle blocks:", uncle_proportion)