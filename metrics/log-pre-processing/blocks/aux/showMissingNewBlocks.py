#!/usr/bin/python3
import pandas as pd
import numpy as np

BLOCKS_LOG = "unique-unique-blocks.log.FINAL"

blocks = pd.read_csv(BLOCKS_LOG,
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'])

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
        missing=row["Number"] - last_val - 1
        print("HOLE: last block number", last_val, "current number: ", row["Number"],
        "missing: ", f"{missing:7}", "TIME: ", row["LocalTimeStamp"])
    
    last_val = row["Number"]
