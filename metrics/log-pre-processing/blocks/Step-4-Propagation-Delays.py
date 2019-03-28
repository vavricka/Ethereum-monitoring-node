
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameter.")

BLOCKS_LOG = sys.argv[1] #"blocks-stage-4.log.ANGAINOR"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

BLOCKS_2_LOG = sys.argv[2] #"blocks-stage-4.log.FALCON"
if not os.path.isfile(BLOCKS_2_LOG):
    sys.exit(BLOCKS_2_LOG, ": does not exists!")

BLOCKS_FINAL_LOG = "blocks-propagation-times.log"

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
        'CapturedLocally'   : 'bool',
        'BlockType'         : 'object',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    usecols=['LocalTimeStamp','BlockHash','Number','CapturedLocally','BlockType'],
    dtype=dtypes_blocks)

blocks2 = pd.read_csv(BLOCKS_2_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    usecols=['LocalTimeStamp','BlockHash','Number','CapturedLocally','BlockType'],
    dtype=dtypes_blocks)

# they both have the same number of rows ....    should sort  by hash   so indexes point to the same block
blocks.sort_values(by=['BlockHash'], inplace=True)
blocks.reset_index(inplace=True, drop=True)

blocks2.sort_values(by=['BlockHash'], inplace=True)
blocks2.reset_index(inplace=True, drop=True)

# drop where that or that is capturedlocally == false
condition = blocks[ (blocks['CapturedLocally'] == False) | (blocks2['CapturedLocally'] == False) ].index
blocks.drop(condition , inplace=True)
blocks2.drop(condition , inplace=True)

# NEW DATAFRAME  
all_blocks = blocks[['BlockHash','Number','BlockType','LocalTimeStamp']].copy()
#append
all_blocks = pd.concat([all_blocks, blocks2[['LocalTimeStamp']] ], axis='columns')

#rename cols
all_blocks.columns = ['BlockHash','Number','BlockType','AngainorTimeStamp', 'FalconTimeStamp']

#   add columns   (IN FOR LOOP..)
all_blocks = all_blocks.assign(PositiveDif = np.nan, AngainorMinusFalcon = np.nan,
    FalconMinusAngainor = np.nan)
for i in all_blocks.index:
    all_blocks.at[i, 'AngainorMinusFalcon'] = (pd.to_datetime(all_blocks.at[i,'AngainorTimeStamp']) - pd.to_datetime(all_blocks.at[i,'FalconTimeStamp'])).total_seconds()
    all_blocks.at[i, 'FalconMinusAngainor'] = all_blocks.at[i, 'AngainorMinusFalcon'] * (-1)
    all_blocks.at[i, 'PositiveDif']         = abs(all_blocks.at[i, 'AngainorMinusFalcon'])


# would be better like this but   .total_seconds() makes trouble here
#all_blocks = all_blocks.assign(AngainorMinusFalcon =     pd.to_datetime(all_blocks['AngainorTimeStamp']) - pd.to_datetime(all_blocks['FalconTimeStamp'])    )
#all_blocks = all_blocks.assign(AngainorMinusFalcon = lambda x: pd.to_datetime(x.AngainorTimeStamp) - pd.to_datetime(x.FalconTimeStamp)    ) #.total_seconds()   



all_blocks.sort_values(by=['Number'], inplace=True)
all_blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
