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







## calculate  avg   and   median
vals = block_propag_times["InterblockTime"]
print("seq. lengths: (all)", "(based on data from", sum(~np.isnan(vals)), "blocks)")
print("                 Average interblock time",  np.nanmean(vals)  )
print("                 Median interblock      ", np.nanmedian(vals)  )
print("---------")

vals = block_propag_times["InterblockTimePerPool"]
print("seq. lengths: (all)", "(based on data from", sum(~np.isnan(vals)), "blocks)")
print("                 Average interblock time per pool",  np.nanmean(vals)  )
print("                 Median interblock time per pool ", np.nanmedian(vals)  )
print("---------")


for i in range(1,10):
    block_propag_times_tmp = block_propag_times[block_propag_times.SameMinerSeqLen == i]
    vals = block_propag_times_tmp["InterblockTimePerPool"]#.value_counts().values
    print("seq. length:",i, "(based on data from", sum(~np.isnan(vals)), "blocks)")
    print("                 Average interblock time per pool",  np.nanmean(vals)  )
    print("                 Median interblock time per pool ", np.nanmedian(vals)  )
    print("---------")



print("block whitdrawing?")
#  for each  seq_len 1-10  check the delay between the first
#  blck from the sequence and the main block before ...  to see if they withdrawed or not.
for i in range(1,10):
    block_propag_times_tmp = block_propag_times[(block_propag_times.SameMinerSeqLen == i) &
        (block_propag_times.PositionInsideSeq == 1)]
    vals = block_propag_times_tmp["InterblockTime"]#.value_counts().values
    print("seq. length:",i, "(based on data from", sum(~np.isnan(vals)), "blocks)")
    print("                 Average interblock time per pool",  np.nanmean(vals)  )
    print("                 Median interblock time per pool ", np.nanmedian(vals)  )
    print("---------")



