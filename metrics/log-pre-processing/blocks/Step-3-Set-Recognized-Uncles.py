#not implemented (and not needed in fact)

##!/usr/bin/python3
## the purpose of this script is to set BlockType to Uncle or Recognized Uncle..
## not recognized
#import pandas as pd
#import numpy as np
#import sys
#import os
#from pathlib import Path
#
#if len(sys.argv) != 2:
#    sys.exit(sys.argv[0], ": expecting 1 parameter.")
#
#BLOCKS_LOG = sys.argv[1] #"blocks-stage-3.log"
#if not os.path.isfile(BLOCKS_LOG):
#    sys.exit(BLOCKS_LOG, ": does not exists!")
#
##output of this script
#BLOCKS_FINAL_LOG = "blocks-stage-4.log"
#
#blocks = pd.read_csv(BLOCKS_LOG, 
#    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
#    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
#    'CapturedLocally','BlockType'])
#
## each Uncle ->  RecUncle/UnRecUncle
## for each  Main check its ListOfUncles  ; find these uncles and set them as recognized uncles "Recognized"
#for row in blocks.itertuples():
#    if row[14] == 'Main': # 14 # blockType
#        if not pd.isnull(row[13]):   #row[13]  uncles..
#            uncles = row[13].split(';')
#            for uncle in uncles:
#                if uncle: #to skip empty strings
#                    blocks.loc[blocks['BlockHash'] == uncle, 'BlockType'] = "Recognized"
#
#blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)



#tmp   -   ## another stuff maybe needed later
#for i, row in blocks.iterrows():
#    if row['BlockType'] == 'Main':
#
#        print(row['Number'], row['ListOfUncles'])
#    else:
#        print("UNCLIK", row['Number'])
#unclesNotSet = len(blocks[blocks.ListOfUncles.isnull()])
#print("num of blocks w/o unclesSet", unclesNotSet)
#unclesSet = len(blocks[blocks.ListOfUncles.notnull()])
#print("num of blocks w/ unclesSet", unclesSet)
#
#blocksWithListOfUnclesSet = blocks[blocks.ListOfUncles.notnull()]
