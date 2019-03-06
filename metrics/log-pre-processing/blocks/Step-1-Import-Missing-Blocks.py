#!/usr/bin/python3
import pandas as pd
import numpy as np

# Merges bloks from 
# another node to fill the missing blocks in the curent machi.
# also adds two new params: blocktype and capturedLocally
#  BlockType will be empty atm-will be set in next step, 
#  CapturedLocally - True - if the block was there; False -> if it was added in this
#  script and in this case, the LocalTimestamp does not count...
#  Input: blocks-stage-1.log from various machines
#  Output blocks-stage-2.log  with two more params:  BlockType,CapturedLocally

#INPUT FILES
LOCAL_BLOCKS = "blocks-stage-1.log" #new blocks, w/o duplicates
REMOTE_BLOCKS = "blocks-stage-1.log.MACHINE-2" #new blocks, w/o duplicates

#output of this script
BLOCKS_FINAL_LOG = "blocks-stage-2.log"

local_blocks = pd.read_csv(LOCAL_BLOCKS, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'])

remote_blocks = pd.read_csv(REMOTE_BLOCKS, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'])

# add  two columns to loc & all captLoc = True
local_blocks = local_blocks.assign(CapturedLocally = 'True', BlockType = np.nan)

#loop through all remote blocks
for _, row in remote_blocks.iterrows():
    #search if RemoteHASH   is  in LOCAL-blocks
    loc_res = local_blocks.loc[local_blocks['BlockHash'] == row.BlockHash]
    if len(loc_res) == 0: # local-locs do not contain that has yet
        local_blocks = local_blocks.append(row) #put it there

# sort by timestamp
local_blocks = local_blocks.sort_values(by=['LocalTimeStamp'])

local_blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
