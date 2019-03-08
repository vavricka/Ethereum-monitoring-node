#!/usr/bin/python3

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

BLOCKS_LOG = sys.argv[1] #"blocks-stage-2.log"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

blocks = pd.read_csv(BLOCKS_LOG,
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'])

#sort
blocks = blocks.sort_values('Number')

first_loop = True
last_val = -1
num_holes = 0

#loop and print  
for i, row in blocks.iterrows():

    if first_loop:
        first_loop = False
        last_val = row["Number"]
        continue

    if (row["Number"] == last_val + 1): # smooth (as expected)
        pass
    elif (row["Number"] == last_val):  #fork
        #print("FORK: ", row["Number"])
        pass
    else:  #a hole, very bad
        missing=row["Number"] - last_val - 1
        print("HOLE: last block number", last_val, "current number: ", row["Number"],
        "missing: ", f"{missing:7}", "TIME: ", row["LocalTimeStamp"])
        num_holes += 1
    
    last_val = row["Number"]

print("blocks:", len(blocks.index))
print("min block-num:", blocks['Number'].min())
print("max block-num:", blocks['Number'].max())
print("num holes:", num_holes)

#tmp !!!
#blocks.to_csv("TMP.csv", index=False, header=True)
