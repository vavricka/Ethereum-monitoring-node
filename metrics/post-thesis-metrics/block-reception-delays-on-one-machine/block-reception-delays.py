import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#check   -   need exactly one param
if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

BLOCKS_LOG = sys.argv[1]                      #input .log  (not .csv)

#check - that log-file exists
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

dtypes = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'         : 'object',
        'Number'            : 'object',
        'GasLimit'          : 'object',
        'GasUsed'           : 'object',
        'Difficulty'        : 'object',
        'Time'              : 'object',
        'Coinbase'          : 'object',
        'ParentHash'        : 'object',
        'UncleHash'         : 'object',
        'BlockSize'         : 'object',
        'ListOfTxs'         : 'object',
        'ListOfUncles'      : 'object',
        }
#nacist   new blck msgs (FOR NOW, then both also.. announc.)
blocks = pd.read_csv(BLOCKS_LOG, dtype=dtypes,
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'])












#setridit podle    BlockHash   a pak podle   LocalTimeStamp
blocks.sort_values(['BlockHash', 'LocalTimeStamp'], ascending=[True, True], inplace=True)
blocks.reset_index(inplace=True, drop=True)

#add delta column
blocks = blocks.assign(ReceptionDelta = np.nan)


lastBlockHash = ""
firstReceptionDate = pd.to_datetime("1993-04-04T07:00:00.737+0000")
receptionsDeltas = []

# for each unique block has, print delays:
for i, row in blocks.iterrows():




    # compute delta
    if lastBlockHash == row.BlockHash:
        tmpDelta = (pd.to_datetime(row.LocalTimeStamp) - firstReceptionDate)
        row.ReceptionDelta = tmpDelta.total_seconds()
        #print
        print(row.ReceptionDelta, end=' ')

    # new block
    else:
        lastBlockHash = row.BlockHash
        firstReceptionDate = pd.to_datetime(row.LocalTimeStamp)
        #print
        print("\n", row.BlockHash, ": ", end=' ')





##List unique values in the df['name'] column
#print(blocks.BlockHash.unique())

