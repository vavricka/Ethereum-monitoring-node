#!/usr/bin/python3
# the purpose of this script is to set BlockType to Uncle or Recognized Uncle..
# and to set the lenghts of forks
# not recognized
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

BLOCKS_LOG = sys.argv[1] #"blocks-stage-3.log"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

BLOCKS_FINAL_LOG = "blocks-stage-4.log"

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
        'BlockType'     : 'object',
        'ForkLength'    : 'int',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    dtype=dtypes_blocks)

#sort by hash
blocks.sort_values(by=['BlockHash'], inplace=True)
blocks.reset_index(inplace=True, drop=True)

current_fork_length = 1

# for each Main check its ListOfUncles  
for i, row in blocks.iterrows():

    
    if row['BlockType'] != 'Main':  # each FORK
    ######set length of fork
        current_fork_length = 1
        parentHash = row.ParentHash
        while True:
            if blocks[blocks.BlockHash == parentHash].empty:
                print("!!! set fork-len of block:", row.BlockHash, "with parent:", parentHash,
                "manually, please. IT can't be done in this script because",
                "the parent is not in our blocks!!!!")
                break
            else:
                curr_block = blocks[blocks.BlockHash == parentHash]
                #Main?
                if curr_block.BlockType.values[0] == "Main":
                    blocks.loc[i, 'ForkLength'] = current_fork_length
                    break
                else:
                    current_fork_length = current_fork_length + 1
                    parentHash = curr_block.ParentHash.values[0]
    else:   # each MAIN
        ######set recognized/unrecognized
        #skip main blocks that have no uncles
        if pd.isnull(row['ListOfUncles']):
            #print("skipping",row["BlockType"], i, "ListOfUncles is null")
            continue

        #loop over the uncles, if they are present, set them as Recognized.
        uncles_in_block = row['ListOfUncles'].split(";")
        for tmp_uncle in uncles_in_block[:-1]:
            #print(tmp_uncle)
            try:
                line = blocks['BlockHash'].searchsorted(tmp_uncle)

                if blocks.at[line,'BlockHash'] == tmp_uncle:
                    #print("setting block", tmp_uncle, "as Recognized")
                    blocks.at[line,'BlockType'] = "Recognized"
                else:
                    print("!! MainBlock:", row['BlockHash'], "contains uncle:",
                    tmp_uncle, "that is not in our blocks.log..")

            #uncle is not present
            except (IndexError, KeyError) as e:
                print("! MainBlock:", row['BlockHash'], "contains uncle:",
                    tmp_uncle, "that is not in our blocks.log..")
                continue

print("don't forget check manually the last uncles num=N, they might be recognized in")
print("a main-blocks N+1, N+2... that we don't have...")

blocks.sort_values(by=['LocalTimeStamp'], inplace=True)
blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
