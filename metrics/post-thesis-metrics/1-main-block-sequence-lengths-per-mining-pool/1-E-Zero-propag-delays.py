import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter -blocks-propagation-times-v3.log")

BLOCKS_LOG = sys.argv[1] #"blocks-propagation-times-v2.log"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

dtypes_blocks_propag_times_v3 = {
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
        'InterblockTime'    : 'float',   
        'InterblockTimePerPool' : 'float',
        }

#load blocks
block_propag_times = pd.read_csv(BLOCKS_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp',
        'S1USTimeStamp','S2CNTimeStamp','FirstObservation',
        'AngainorDiff','FalconDiff','S1USDiff','S2CNDiff',
        'MiningPool','NumTransactions','SameMinerSeqLen','PositionInsideSeq',
        'Difficulty','BlockSize','InterblockTime','InterblockTimePerPool'],
    dtype=dtypes_blocks_propag_times_v3)




#  ZERO  or around  zero   interblocktimes      (not per pool)
vals = block_propag_times["InterblockTime"]
num_delays_not_nan = sum(~np.isnan(vals))

print("delays total (not nan):", num_delays_not_nan)

prev_i = -100000
for i in [0, 0.01, 0.1, 0.5, 1]:
    block_propag_times_tmp = block_propag_times[(block_propag_times.InterblockTime > prev_i) &
        (block_propag_times.InterblockTime <= i)]
    #block_propag_times_tmp = block_propag_times[ (block_propag_times.InterblockTime <= i)]


    print("<=", i)

    #tmp
    if i == 0:
        print(block_propag_times_tmp[['Number','BlockType','FirstObservation','MiningPool',
        'SameMinerSeqLen','PositionInsideSeq','InterblockTime','InterblockTimePerPool']])

    vals = block_propag_times_tmp["InterblockTime"]#.value_counts().values
    print("num of blcks with delay <=",i, ":", sum(~np.isnan(vals)), sum(~np.isnan(vals))/num_delays_not_nan
        *100, "%")
    print("                 Average delay",  np.nanmean(vals)  )
    print("                 Median delay", np.nanmedian(vals)  )
    print("---------")
    print(block_propag_times_tmp[['Number','BlockType','FirstObservation','MiningPool',
        'SameMinerSeqLen','PositionInsideSeq','InterblockTime','InterblockTimePerPool']])

    prev_i = i







#TMP
exit(0)
#Zero or Negative inter-block times in sequences mined by one pool
vals = block_propag_times["InterblockTimePerPool"]
num_delays_not_nan = sum(~np.isnan(vals))

print("delays total:", num_delays_not_nan)

prev_i = -100000
for i in [0, 0.01, 0.1]:
    #block_propag_times_tmp = block_propag_times[(block_propag_times.InterblockTimePerPool > prev_i) &
    #    (block_propag_times.InterblockTimePerPool <= i)]
    block_propag_times_tmp = block_propag_times[ (block_propag_times.InterblockTimePerPool <= i)]

    #tmp
    if i == 0:
        print(block_propag_times_tmp[['Number','BlockType','FirstObservation','MiningPool',
        'SameMinerSeqLen','PositionInsideSeq','InterblockTime','InterblockTimePerPool']])

    vals = block_propag_times_tmp["InterblockTimePerPool"]#.value_counts().values
    print("num of blcks with delay <=",i, ":", sum(~np.isnan(vals)), sum(~np.isnan(vals))/num_delays_not_nan
        *100, "%")
    print("                 Average delay",  np.nanmean(vals)  )
    print("                 Median delay", np.nanmedian(vals)  )
    print("---------")

    prev_i = i












