#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path


# Merges bloks from 
# another node to fill the missing blocks in the curent machi.
# also adds two new params: blocktype and capturedLocally
#  BlockType will be empty atm-will be set in next step, 
#  CapturedLocally - True - if the block was there; False -> if it was added in this
#  script and in this case, the LocalTimestamp does not count...
#  Input: blocks-stage-1.log.LOC blocks-stage-1.log.REM
#  Output blocks-stage-2.log  with two more params:  BlockType,CapturedLocally

if len(sys.argv) != 4:
    sys.exit(sys.argv[0], ": expecting 3 parameters.")

#INPUT FILES
LOCAL_BLOCKS = sys.argv[1] #"blocks-stage-1.log.LOC"
REMOTE_BLOCKS = sys.argv[2]

#output of this script
BLOCKS_FINAL_LOG = sys.argv[3]

if not os.path.isfile(LOCAL_BLOCKS):
    sys.exit(LOCAL_BLOCKS, ": does not exists!")

if not os.path.isfile(REMOTE_BLOCKS):
    sys.exit(REMOTE_BLOCKS, ": does not exists!")

if os.path.isfile(BLOCKS_FINAL_LOG):
    sys.exit(BLOCKS_FINAL_LOG, ": ALREADY EXISTS not exists!")

local_blocks = pd.read_csv(LOCAL_BLOCKS, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'])

remote_blocks = pd.read_csv(REMOTE_BLOCKS, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'])

# na -> to True,   False remains False...
local_blocks.CapturedLocally = local_blocks.CapturedLocally.fillna('True')

remote_blocks['CapturedLocally'] = 'False'

#loop through all remote blocks
for _, row in remote_blocks.iterrows():
    #search if RemoteHASH   is  in LOCAL-blocks
    loc_res = local_blocks.loc[local_blocks['BlockHash'] == row.BlockHash]
    if len(loc_res) == 0: # local-locs do not contain that has yet
        local_blocks = local_blocks.append(row) #put it there

# sort by timestamp
local_blocks = local_blocks.sort_values(by=['LocalTimeStamp'])

local_blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
