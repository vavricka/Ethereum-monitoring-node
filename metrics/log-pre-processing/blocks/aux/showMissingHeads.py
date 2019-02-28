#!/usr/bin/python3
import pandas as pd
import numpy as np

BLOCKHEADS_LOG = "heads.log"
blocks = pd.read_csv(BLOCKHEADS_LOG, names=['LocalTimeStamp','BlockHash','Number'])

print("blocks: ", len(blocks.index))

#sort
sorted = blocks.sort_values('Number')

first_loop = True
last_val = -1

#loop and print  
for i, row in sorted.iterrows():

    if first_loop:
        first_loop = False
        last_val = row["Number"]
        print("FIRST Block's num: ", last_val)
        continue

    if (row["Number"] == last_val + 1): # smooth (as expected)
        pass
    elif (row["Number"] == last_val):  #fork
        print("FORK: ", row["Number"])
    else:  #a hole, very bad
        print("HOLE: last block number", last_val, " current number: ", row["Number"])
    
    last_val = row["Number"]
