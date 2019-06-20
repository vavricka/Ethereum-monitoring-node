import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter -blocks-propagation-times-v2.log")

BLOCKS_LOG = sys.argv[1] #"blocks-propagation-times-v2.log"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")


BLOCKS_PROPAG_V3_OUT = "blocks-propagation-times-v3.log"

dtypes_blocks_propag_times_v2 = {
        'BlockHash'         : 'object',
        'Number'            : 'Int64',
        'BlockType'         : 'object',
        'AngainorTimeStamp' : 'object',
        'FalconTimeStamp'   : 'object',
        'S1USTimeStamp'     : 'object',
        'S2CNTimeStamp'     : 'object',
        'FirstObservation'  : 'object',
        'AngainorDiff'      : 'float',
        'FalconDiff'        : 'float',
        'S1USDiff'          : 'float',
        'S2CNDiff'          : 'float',
        'MiningPool'        : 'object',
        'NumTransactions'   : 'Int64',
        'SameMinerSeqLen'   : 'Int64',
        'PositionInsideSeq' : 'Int64',
        'Difficulty'        : 'Int64',   
        'BlockSize'         : 'Int64',
        }

#load blocks
block_propag_times = pd.read_csv(BLOCKS_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp',
        'S1USTimeStamp','S2CNTimeStamp','FirstObservation',
        'AngainorDiff','FalconDiff','S1USDiff','S2CNDiff',
        'MiningPool','NumTransactions','SameMinerSeqLen','PositionInsideSeq',
        'Difficulty','BlockSize'],
    dtype=dtypes_blocks_propag_times_v2)

##   add column   interblockTime
block_propag_times = block_propag_times.assign(InterblockTime = np.nan,
    InterblockTimePerPool = np.nan)

main_blocks = block_propag_times[block_propag_times.BlockType == "Main"].copy()
main_blocks.sort_values(by='Number', inplace=True)
main_blocks.set_index('Number', inplace=True, drop=True)


#prevReceptionDate  is the recep. data of the MAIN block  with blockNum = i-1
prevReceptionDate = pd.to_datetime("1993-04-04T07:00:00.737+0000")
#block_propag_times = block_propag_times.sort_values(by=['Number'])

for i in block_propag_times.index:
    blockNum = block_propag_times.at[i, 'Number']
    receptionDate = pd.to_datetime(block_propag_times.at[i,'FirstObservation'])

    try:
        prevReceptionDateString = main_blocks.at[blockNum-1, 'FirstObservation']
        prevReceptionDate = pd.to_datetime(prevReceptionDateString)
    except (KeyError):
        #print('block num', blockNum-1, "not in main blocks")
        continue

    block_propag_times.at[i, 'InterblockTime'] = (receptionDate - prevReceptionDate).total_seconds()

def setInterBlckDelaysPerPool(block_propag_times, poolName):
    prevReceptionDate = pd.to_datetime("1993-04-04T07:00:00.737+0000")
    prevBlockNumber = -1
    # block_propag_times  is already ordered by BlockNumber so chill..
    for i in block_propag_times.index:

        if block_propag_times.at[i, 'MiningPool'] != poolName:
            continue

        #first run: set prev and continue
        if prevBlockNumber == -1:
            prevReceptionDate = pd.to_datetime(block_propag_times.at[i, 'FirstObservation'])
            prevBlockNumber = block_propag_times.at[i, 'Number']
            continue

        BlockNumber = block_propag_times.at[i, 'Number']
        receptionDate = pd.to_datetime(block_propag_times.at[i,'FirstObservation'])
        
        if BlockNumber == (prevBlockNumber +1):
            block_propag_times.at[i, 'InterblockTimePerPool'] = (receptionDate - prevReceptionDate).total_seconds()

        prevBlockNumber = BlockNumber
        prevReceptionDate = receptionDate
            



for pool in ['Ethermine', 'Sparkpool', 'f2pool2', 'Nanopool', 'miningpoolhub1',
    'HuoBi.pro', 'pandapool', 'DwarfPool1', 'xnpool', 'uupool', 'Minerall',
    'firepool', 'zhizhu', 'MiningExpress', 'Hiveon', '(0x84A0d7..)', '(0xAA5c42..)',
    '2miners', 'bw', 'Coinotron', '(0x858fDE..)', '2minerssolo']:
    setInterBlckDelaysPerPool(block_propag_times, pool)


# sort by timestamp
#block_propag_times.sort_values(by=['Number'], inplace=True)
block_propag_times.to_csv(BLOCKS_PROPAG_V3_OUT, index=False, header=False)

