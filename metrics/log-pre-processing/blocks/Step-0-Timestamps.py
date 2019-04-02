#!/usr/bin/python3
import pandas as pd
import numpy as np

NEWBLOCKS_LOG = "blocks-stage-0.log" #new blocks, w/o duplicates
ANNOUNCEMENTS_LOG = "unique-unique-blocksAnnouncements.log.FINAL"
BLOCKS_FINAL_LOG = "blocks-stage-1.log"

blocks = pd.read_csv(NEWBLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'])
    #parse_dates=['LocalTimeStamp'])

announcements = pd.read_csv(ANNOUNCEMENTS_LOG, 
    names=['LocalTimeStamp','BlockHash'])

#sort announcements by BlockHash
announcements = announcements.sort_values(by=['BlockHash'])

# (1) set LOWEST Timestamp from both blocks.log and blocksAnnouncements.log
 #for each row in NewBlockMsg    check if some row from blocksAnnouncements with equal hash has lowertimestamp
 #update newblockmsg  accordingly
for i, row in blocks.iterrows():

    # searchsorted uses Binary search so it's fast.
    try:
        line = announcements['BlockHash'].searchsorted(row['BlockHash']) 

        if row['BlockHash'] == announcements.iloc[line][1]:
            if pd.to_datetime(announcements.iloc[line][0]) < pd.to_datetime(row['LocalTimeStamp']):
               blocks.iat[i,0] = announcements.iloc[line][0]
    except (IndexError, KeyError):
        continue

#add three params
blocks = blocks.assign(CapturedLocally = np.nan, BlockType = np.nan, ForkLength = 0)

# Gen out file
blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
