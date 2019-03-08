#!/usr/bin/python3

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

BLOCKS_LOG = sys.argv[1]                      #input .log  (not .csv)

#check - that log-file exists
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

#takes preprocessed blocksMerged
blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'])

print("Total: ", len(blocks))

#prints number of Main   (check with num of Main in heads)
print("Main: ", len(blocks[blocks.BlockType == "Main"]))

#print num of uncles
print("Uncle: ", len(blocks[blocks.BlockType == "Uncle"]))

#print num of rec uncles
print("Recognized: ", len(blocks[blocks.BlockType == "Recognized"]))


#nan
# doesn't work for some reason
#print("NaN: ", len(blocks[blocks.BlockType == np.nan]))


someNan = False



for i, row in blocks.iterrows():
    if (row['BlockType'] != "Main" and
        row['BlockType'] != "Uncle" and
        row['BlockType'] != "Recognized"):

        #print(int(row['Number']), row['BlockHash'], row['BlockType'] )
        if not someNan:
            someNan = True



if not someNan:
    print("there are NO blocks with blockType==NaN so nothing to do here")
else:
    print("there ARE some blocks with blockType==NaN so fix it")