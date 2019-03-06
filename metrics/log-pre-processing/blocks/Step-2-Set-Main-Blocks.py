#!/usr/bin/python3
import pandas as pd
import numpy as np

NEWBLOCKS_LOG = "blocks-stage-2.log" #new blocks, w/o duplicates
#NEWBLOCKS_LOG = "unique-unique-blocks.log.FINAL.TimestampsUpdated-SHORT"

#output of this script
BLOCKS_FINAL_LOG = "blocks-stage-3.log"
#BLOCKS_FINAL_LOG = "blocksMergedCheckManuallyNow.log-SHORT"

blocks = pd.read_csv(NEWBLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'], index_col='BlockHash')

# add BlockType column
blocks = blocks.assign(BlockType = np.nan)

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

blocks.to_csv(BLOCKS_FINAL_LOG, index=True, header=False)