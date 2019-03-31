
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 5:
    sys.exit(sys.argv[0], ": expecting 4 parameter.")

BLOCKS_ANGAINOR = sys.argv[1] #"blocks-stage-4.log.ANGAINOR"   or 2 or 3 ...
if not os.path.isfile(BLOCKS_ANGAINOR):
    sys.exit(BLOCKS_ANGAINOR, ": does not exists!")

BLOCKS_FALCON = sys.argv[2] #"blocks-stage-2.log.FALCON" or 3,4..
if not os.path.isfile(BLOCKS_FALCON):
    sys.exit(BLOCKS_FALCON, ": does not exists!")

BLOCKS_S1_US = sys.argv[3] #"blocks-stage-2.log.S1"
if not os.path.isfile(BLOCKS_S1_US):
    sys.exit(BLOCKS_S1_US, ": does not exists!")

BLOCKS_S2_CN = sys.argv[4] #"blocks-stage-2.log.S2"
if not os.path.isfile(BLOCKS_S2_CN):
    sys.exit(BLOCKS_S2_CN, ": does not exists!")

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

blocks_angainor = pd.read_csv(BLOCKS_ANGAINOR, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    usecols=['LocalTimeStamp','BlockHash','Number','CapturedLocally','BlockType'],
    dtype=dtypes_blocks)

blocks_falcon = pd.read_csv(BLOCKS_FALCON, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    usecols=['LocalTimeStamp','BlockHash','Number','CapturedLocally','BlockType'],
    dtype=dtypes_blocks)

blocks_s1_us = pd.read_csv(BLOCKS_S1_US, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    usecols=['LocalTimeStamp','BlockHash','Number','CapturedLocally','BlockType'],
    dtype=dtypes_blocks)

blocks_s2_cn = pd.read_csv(BLOCKS_S2_CN, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType'],
    usecols=['LocalTimeStamp','BlockHash','Number','CapturedLocally','BlockType'],
    dtype=dtypes_blocks)

# they all have the same number of rows ....    should sort  by hash   so indexes point to the same block
blocks_angainor.sort_values(by=['BlockHash'], inplace=True)
blocks_angainor.reset_index(inplace=True, drop=True)

blocks_falcon.sort_values(by=['BlockHash'], inplace=True)
blocks_falcon.reset_index(inplace=True, drop=True)

blocks_s1_us.sort_values(by=['BlockHash'], inplace=True)
blocks_s1_us.reset_index(inplace=True, drop=True)

blocks_s2_cn.sort_values(by=['BlockHash'], inplace=True)
blocks_s2_cn.reset_index(inplace=True, drop=True)





# drop where any ofthem has capturedlocally == false
condition = blocks_angainor[ (blocks_angainor['CapturedLocally'] == False) | \
    (blocks_falcon['CapturedLocally'] == False) | (blocks_s1_us['CapturedLocally'] == False) | \
    (blocks_s2_cn['CapturedLocally'] == False) ].index

blocks_angainor.drop(condition , inplace=True)
blocks_falcon.drop(condition , inplace=True)
blocks_s1_us.drop(condition , inplace=True)
blocks_s2_cn.drop(condition , inplace=True)

# NEW DATAFRAME  
all_blocks = blocks_angainor[['BlockHash','Number','BlockType','LocalTimeStamp']].copy()
#append
all_blocks = pd.concat([all_blocks, blocks_falcon[['LocalTimeStamp']] ], axis='columns')
all_blocks = pd.concat([all_blocks, blocks_s1_us[['LocalTimeStamp']] ], axis='columns')
all_blocks = pd.concat([all_blocks, blocks_s2_cn[['LocalTimeStamp']] ], axis='columns')



#rename cols
all_blocks.columns = ['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp','S1USTimeStamp','S2CNTimeStamp']


#   add columns   (IN FOR LOOP..)
all_blocks = all_blocks.assign(FirstObservation = np.nan, AngainorDiff = np.nan, \
    FalconDiff = np.nan, S1USDiff = np.nan, S2CNDiff = np.nan)


for i in all_blocks.index:
    all_blocks.at[i, 'FirstObservation'] = min(pd.to_datetime(all_blocks.at[i,'AngainorTimeStamp']),\
        pd.to_datetime(all_blocks.at[i,'FalconTimeStamp']), pd.to_datetime(all_blocks.at[i,'S1USTimeStamp']),\
        pd.to_datetime(all_blocks.at[i,'S2CNTimeStamp']) )
    all_blocks.at[i, 'AngainorDiff'] = (pd.to_datetime(all_blocks.at[i,'AngainorTimeStamp']) - pd.to_datetime(all_blocks.at[i,'FirstObservation'])).total_seconds()
    all_blocks.at[i, 'FalconDiff'] = (pd.to_datetime(all_blocks.at[i,'FalconTimeStamp']) - pd.to_datetime(all_blocks.at[i,'FirstObservation'])).total_seconds()
    all_blocks.at[i, 'S1USDiff'] = (pd.to_datetime(all_blocks.at[i,'S1USTimeStamp']) - pd.to_datetime(all_blocks.at[i,'FirstObservation'])).total_seconds()
    all_blocks.at[i, 'S2CNDiff'] = (pd.to_datetime(all_blocks.at[i,'S2CNTimeStamp']) - pd.to_datetime(all_blocks.at[i,'FirstObservation'])).total_seconds()

# would be better like this but   .total_seconds() makes trouble here
#all_blocks = all_blocks.assign(AngainorMinusFalcon =     pd.to_datetime(all_blocks['AngainorTimeStamp']) - pd.to_datetime(all_blocks['FalconTimeStamp'])    )
#all_blocks = all_blocks.assign(AngainorMinusFalcon = lambda x: pd.to_datetime(x.AngainorTimeStamp) - pd.to_datetime(x.FalconTimeStamp)    ) #.total_seconds()   



all_blocks.sort_values(by=['Number'], inplace=True)
all_blocks.to_csv(BLOCKS_FINAL_LOG, index=False, header=False)
