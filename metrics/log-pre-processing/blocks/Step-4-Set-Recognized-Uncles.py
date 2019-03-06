#!/usr/bin/python3
# the purpose of this script is to check all Uncles and set them to either recognized or 
# not recognized
import pandas as pd
import numpy as np

MERGED_CHECKED_BLOCKS_LOG = "blocksMergedChecked.log" #new blocks, w/o duplicates

#output of this script
BLOCKS_FINAL_LOG = "blocksFinal.log"

blocks = pd.read_csv(MERGED_CHECKED_BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles','BlockType'])

# each Uncle ->  RecUncle/UnRecUncle
# for each  Main check its ListOfUncles  ; find these uncles and set them as recognized uncles "Recognized"
for row in blocks.itertuples():
    if row[14] == 'Main': # 14 # blockType
        if not pd.isnull(row[13]):   #row[13]  uncles..
            uncles = row[13].split(';')
            for uncle in uncles:
                if uncle: #to skip empty strings
                    blocks.loc[blocks['BlockHash'] == uncle, 'BlockType'] = "Recognized"

blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
