#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

NEWBLOCKS_LOG = sys.argv[1] #"blocks-stage-2.log"
if not os.path.isfile(NEWBLOCKS_LOG):
    sys.exit(NEWBLOCKS_LOG, ": does not exists!")

#output of this script
BLOCKS_FINAL_LOG = "blocks-stage-3.log"

blocks = pd.read_csv(NEWBLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'], index_col='BlockHash')

# search by blockHash because we will be looking for blocks based on this propery
blocks = blocks.sort_values(by=['BlockHash'])

#ID = hash of block with highest Block-Number
ID=blocks['Number'].idxmax()
#ID of the blocks with lowest Block-Number
ID_MIN = blocks['Number'].idxmin()

while ID != ID_MIN: 
    blocks.loc[ID, 'BlockType'] = "Main"
    ID = blocks.loc[ID, 'ParentHash']

#last one
blocks.loc[ID, 'BlockType'] = "Main"

#sort it back by timestamp...
blocks = blocks.sort_values(by=['LocalTimeStamp'])

blocks.reset_index(level=0, inplace=True)

#need to reindex because now BlockHash is before Timestamp...
blocks = blocks.reindex (
    columns=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'])

blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
