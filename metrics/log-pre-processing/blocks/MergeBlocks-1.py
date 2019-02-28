#!/usr/bin/python3

import pandas as pd
import numpy as np

NEWBLOCKS_LOG = "unique-unique-blocks.log.FINAL.TimestampsUpdated" #new blocks, w/o duplicates
BLOCKHEADS_LOG = "heads.log" #unique by def; careful, in the beginning not sorted. DELETE unsorted beginning first

#output of this script
BLOCKS_FINAL_LOG = "blocksMergedCheckManuallyNow.log"

blck1 = pd.read_csv(NEWBLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'])


# add BlockType column
blocks = blck1.assign(BlockType = np.nan)


# (2) from new blck head... update   the structure and mark main/uncle
heads = pd.read_csv(BLOCKHEADS_LOG, names=['LocalTimeStamp','BlockHash','Number'])

#add column  BlockType
heads = heads.assign(BlockType = np.nan)

last_index = (len(heads.index)-1)
block_hash=""
previous_num = 0
# loop -  go upward
for idx in reversed(heads.index):
    current_num = heads.loc[idx, 'Number']
    
    # first loop (last row)
    if idx == last_index:
        previous_num = current_num
        heads.loc[idx, 'BlockType'] = "Main"
        block_hash = heads.loc[idx, 'BlockHash']
        continue

    if current_num == (previous_num-1):
        heads.loc[idx, 'BlockType'] = "Main"     
    elif current_num == previous_num:
        if heads.loc[idx, 'BlockHash'] == block_hash:
            heads.loc[idx, 'BlockType'] = "Main"
        else:
            heads.loc[idx, 'BlockType'] = "Uncle"
    else:
        #raise Exception('Unexpected BlockNumber; idx=', idx, 'current_num=', current_num, 
        #'previous_num=', previous_num)
        #Unexpected behaviour... probably due to lost connection...
        heads.loc[idx, 'BlockType'] = "CheckManually"
        print('Unexpected BlockNumber; idx=', idx, 'current_num=', current_num, 
        'previous_num=', previous_num)
        

    block_hash = heads.loc[idx, 'BlockHash']
    previous_num = current_num



# TODO tady je problem ze  v heads muzou bejt blocky ktery v  newblocks. nebyli...

for row in heads.itertuples():
    hash = row[2]
    blockType = row[4]
    idx = blocks.index[blocks['BlockHash'] == hash]

    if not idx.empty:
       # print("Going to set", blockType)
        blocks.loc[idx, 'BlockType'] = blockType




blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
