#!/usr/bin/python3

import pandas as pd
import numpy as np



NEWBLOCK_CSV = "blocks.csv"
NEWBLOCKHASHES_CSV = "blocksAnnouncements.csv"
NEWBLOCKHEADS_CSV = "heads.csv"

BLOCKS_CSV = "blocksFinal.csv"

# NewBlockMsg -- remove rows with
blck1 = pd.read_csv(NEWBLOCK_CSV, index_col=0)
#drop_duplicates is by def (keep='first') -- leaves the oldes Timestamp ;)
blck1NoDuplicates = blck1.drop_duplicates('BlockHash')

# NewBlockHashesMsg -- remove rows with
blck2 = pd.read_csv(NEWBLOCKHASHES_CSV, index_col=0)
blck2NoDuplicates = blck2.drop_duplicates('BlockHash')



# 1 -------- DONE
# for each row in NewBlockMsg    check if some row from NewBlockHashesMsg with equal hash has lowertimestamp
#   update newblockmsg  accordingly
for i, row in blck1NoDuplicates.iterrows():
    tmp = blck2NoDuplicates.loc[blck2NoDuplicates['BlockHash'] == row['BlockHash']]['LocalTimestamp'].head()
    
    #it goes to this clausule only if blck2NoDuplicates contains a row with given BlockHash
    if not tmp.empty:
        # update NEWEST timestamps
        if pd.to_datetime(tmp.item(), utc=True) < pd.to_datetime(blck1NoDuplicates.at[i,'LocalTimestamp'], utc=True):
            blck1NoDuplicates.at[i,'LocalTimestamp'] = tmp.item()

# add BlockType column
blocks = blck1NoDuplicates.assign(BlockType = np.nan)


# 2  next ....    from new blck head... update   the structure and marck main/uncle

######### ASI DONE, j u s t  CHECK

#load newblockhead....   
heads = pd.read_csv(NEWBLOCKHEADS_CSV, index_col=0)
#add columnt     BlockType
heads = heads.assign(BlockType = np.nan)


last_index = (len(heads.index)-1)
block_hash=""
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
        block_hash = heads.loc[idx, 'BlockHash']
    elif current_num == previous_num:
        if heads.loc[idx, 'BlockHash'] == block_hash:
            heads.loc[idx, 'BlockType'] = "Main"
        else:
            heads.loc[idx, 'BlockType'] = "Uncle"
    else:
        raise Exception('Unexpected BlockNumber; idx=', idx, 'current_num=', current_num, 
        'previous_num=', previous_num)

    previous_num = current_num


#tmp
print("HEADS>")
print(heads)

# 3     uncles --  to  rec/unrec   uncle 
#   read heads; copy Main/Uncle from there to  blocks
for row in heads.itertuples():
    hash = row[2]
    blockType = row[4]
    idx = blocks.index[blocks['BlockHash'] == hash]

    if not idx.empty:
       # print("Going to set", blockType)
        blocks.loc[idx, 'BlockType'] = blockType

#   in blocks, where there is   BlockType== np.nan...  set Uncle......
for idx in blocks.index:
    if blocks.loc[idx, 'BlockType'] != "Main":
        blocks.loc[idx, 'BlockType'] = 'Uncle'

# each Uncle ->   RecUncle/UnRecUncle
# for each  Main check its ListOfUncles  ; findt these uncles and set them as recognized uncles "Recognized"
for row in blocks.itertuples():
    if row[14] == 'Main': # 14 # blockType
        if not pd.isnull(row[13]):   #row[13]  uncles..
            uncles = row[13].split(';')
            for uncle in uncles:
                if uncle: #to skip empty strings
                    blocks.loc[blocks['BlockHash'] == uncle, 'BlockType'] = "Recognized"


#  export to blocks.csv
blocks.to_csv(BLOCKS_CSV)
