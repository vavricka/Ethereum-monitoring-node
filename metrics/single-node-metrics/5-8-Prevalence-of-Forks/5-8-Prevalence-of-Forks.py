#!/usr/bin/python3

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

BLOCKS_LOG = sys.argv[1]                      #input .log  (not .csv)

#check - that log-file exists
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

#takes preprocessed blocksMerged
blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'])#, dtype={'CapturedLocally': np.bool})



# 5.8 preval. of forks
# 2 things, A and B:
# A) number of: blocks  TOTAL BLOCKS,    Main/Fork     (Later Main/Fork-rec/Fork-unRecognized)
# B) distinguish between forks of various lengths.

#A:
print("Warning --atm it distinguishes only Main and Uncles")
print("Uncles encompass both Recognized and Unrecognized ones.")
print("------")

total_blocks = len(blocks)
print("Total Blocks: ", total_blocks)

num_main = len(blocks[blocks.BlockType == "Main"])
print("Main:", num_main, "rate:", num_main / total_blocks)

num_uncle = len(blocks[blocks.BlockType == "Uncle"])
print("Uncle:", num_uncle, "rate:", num_uncle / total_blocks)

print("Verifying Uncle+Main", num_main + num_uncle, "=?", len(blocks), "blocks")

#not implemented yet
#num_rec_uncle = len(blocks[blocks.BlockType == "Recognized"])
#print("Recognized:", num_rec_uncle)




#B   forks and their lengths..
uncles = blocks[blocks.BlockType == "Uncle"]
current_fork_length = 1

#for each UNCLE
for _, row in uncles.iterrows():

    current_fork_length = 1
    print("uncle num:",row.Number, "hash:", row.BlockHash)

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
                print("FORK LENGTH:", current_fork_length)
                break
            else:
                current_fork_length = current_fork_length + 1
                parentHash = curr_block.ParentHash.values[0]






    





