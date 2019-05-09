#!/usr/bin/python3
import pandas as pd
import numpy as np



import sys
import os
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameter.")

BLOCKS_LOG = sys.argv[1] #"blocks.log.FINAL"
ANNOUN_LOG = sys.argv[2] #"blocksAnnouncements.log"

if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")
if not os.path.isfile(ANNOUN_LOG):
    sys.exit(ANNOUN_LOG, ": does not exists!")

dtypes_blocks = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'     : 'object',
        'Number'        : 'object',
        'GasLimit'      : 'object',
        'GasUsed'       : 'object',
        'Difficulty'    : 'object',
        'Time'          : 'object',
        'Coinbase'      : 'object',
        'ParentHash'    : 'object',
        'UncleHash'     : 'object',
        'BlockSize'     : 'object',
        'ListOfTxs'     : 'object',
        'ListOfUncles'  : 'object',
        }

dtypes_announ = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'         : 'object',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'],
    dtype=dtypes_blocks,  usecols=['BlockHash'])

announ = pd.read_csv(ANNOUN_LOG, 
    names=['LocalTimeStamp','BlockHash'],
    dtype=dtypes_announ,  usecols=['BlockHash'])

blck_total = blocks.append(announ)




print("BLOCKS are propagated using 2 different message types",
"NewBlockMsg and NewBlockHashesMsg.")


series_blocks = blocks['BlockHash'].value_counts().values
series_announ = announ['BlockHash'].value_counts().values
series_blck_total = blck_total['BlockHash'].value_counts().values

print("Avg number of block reception", blocks['BlockHash'].value_counts().values.mean())
for q in [50, 90, 95, 98, 99, 100]:
    print ("new block msgs:{}%% percentile: {}".format (q, np.percentile(series_blocks, q)))

print("Avg number of announcements reception", announ['BlockHash'].value_counts().values.mean())
for q in [50, 90, 95, 98, 99, 100]:
    print ("announcements:{}%% percentile: {}".format (q, np.percentile(series_announ, q)))

print("Avg number of blck_total reception", blck_total['BlockHash'].value_counts().values.mean())
for q in [50, 90, 95, 98, 99, 100]:
    print ("blocks and block announ together:{}%% percentile: {}"
        .format (q, np.percentile(series_blck_total, q)))
