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
    'CapturedLocally','BlockType'])#, dtype={'CapturedLocally': np.bool})

print()
print("Total Blocks: ", len(blocks), "(Local:",
    len(blocks[blocks.CapturedLocally == True]),
    "Imported:", str(len(blocks[blocks.CapturedLocally == False])) + ")")

print("---")

num_main = len(blocks[blocks.BlockType == "Main"])
num_main_local = len(blocks[(blocks.BlockType == "Main") & (blocks.CapturedLocally == True)] )
num_main_impor = len(blocks[(blocks.BlockType == "Main") & (blocks.CapturedLocally == False)] )
#prints number of Main   (check with num of Main in heads)
print("Main:", num_main, "(Local:", num_main_local , "Imported:", str(num_main_impor) + ")")

num_uncle = len(blocks[blocks.BlockType == "Uncle"])
num_uncle_local = len(blocks[(blocks.BlockType == "Uncle") & (blocks.CapturedLocally == True)] )
num_uncle_impor = len(blocks[(blocks.BlockType == "Uncle") & (blocks.CapturedLocally == False)] )
#print num of uncles
print("Uncle:", num_uncle, "(Local:", num_uncle_local , "Imported:", str(num_uncle_impor) + ")")

num_rec_uncle = len(blocks[blocks.BlockType == "Recognized"])
num_rec_uncle_local = len(blocks[(blocks.BlockType == "Recognized") & (blocks.CapturedLocally == True)] )
num_rec_uncle_impor = len(blocks[(blocks.BlockType == "Recognized") & (blocks.CapturedLocally == False)] )
#print num of uncles
print("Recognized:", num_rec_uncle, "(Local:", num_rec_uncle_local , "Imported:", str(num_rec_uncle_impor) + ")")

#uncomment to show imported blocks
#for i, row in blocks.iterrows():
#    if row['CapturedLocally'] == False:
#        print(row['LocalTimeStamp'], row['Number'], row['BlockHash'], row['BlockType'])
#        
