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


#  crate a data framame   with  one min. pool  for each row
#sequences_list = block_propag_times['SameMinerSeqLen'].unique() 
sequences_list = list(range(0,10))  #  0  means overall
sequences = pd.DataFrame(sequences_list, columns =['SeqLen'])
sequences.set_index('SeqLen', inplace=True)

sequences = sequences.assign(mean = np.nan, median = np.nan, std = np.nan,
    based_on_num_of_blocks = np.nan)



for i in range(0,10):

    if i == 0:
        block_propag_times_tmp = block_propag_times
    else:
        block_propag_times_tmp = block_propag_times[block_propag_times.SameMinerSeqLen == i]
        
    vals = block_propag_times_tmp["InterblockTimePerPool"]#.value_counts().values

    sequences.at[i, 'mean']   = np.nanmean(vals)
    sequences.at[i, 'median'] = np.nanmedian(vals)
    sequences.at[i, 'std']    = np.std(vals)
    sequences.at[i, 'based_on_num_of_blocks'] = sum(~np.isnan(vals))
    

#float to int
sequences['based_on_num_of_blocks'] = sequences['based_on_num_of_blocks'].astype('Int32')


#PRINT
print("0 means ALL sequences together.")
print(sequences)










#  crate a data framame   with  one min. pool  for each row
#sequences_list = block_propag_times['SameMinerSeqLen'].unique() 
sequences_list = list(range(0,10))  #  0  means overall
sequences = pd.DataFrame(sequences_list, columns =['SeqLen'])
sequences.set_index('SeqLen', inplace=True)

sequences = sequences.assign(mean = np.nan, median = np.nan, std = np.nan,
    based_on_num_of_seqences = np.nan)


for i in range(0,10):

    if i == 0:
        block_propag_times_tmp = block_propag_times[block_propag_times.PositionInsideSeq == 1]
    else:
        block_propag_times_tmp = block_propag_times[(block_propag_times.SameMinerSeqLen == i) &
        (block_propag_times.PositionInsideSeq == 1)]
        
    vals = block_propag_times_tmp["InterblockTime"]#.value_counts().values

    sequences.at[i, 'mean']   = np.nanmean(vals)
    sequences.at[i, 'median'] = np.nanmedian(vals)
    sequences.at[i, 'std']    = np.std(vals)
    sequences.at[i, 'based_on_num_of_seqences'] = sum(~np.isnan(vals))
    

#float to int
sequences['based_on_num_of_seqences'] = sequences['based_on_num_of_seqences'].astype('Int32')


#PRINT
print("0 means ALL sequences together.")
print(sequences)


# print("block whitdrawing?")
# #  for each  seq_len 1-10  check the delay between the first
# #  blck from the sequence and the main block before ...  to see if they withdrawed or not.
# for i in range(1,10):
#     block_propag_times_tmp = block_propag_times[(block_propag_times.SameMinerSeqLen == i) &
#         (block_propag_times.PositionInsideSeq == 1)]
#     vals = block_propag_times_tmp["InterblockTime"]#.value_counts().values
#     print("seq. length:",i, "(based on data from", sum(~np.isnan(vals)), "blocks)")
#     print("                 Average interblock time per pool",  np.nanmean(vals)  )
#     print("                 Median interblock time per pool ", np.nanmedian(vals)  )
#     print("---------")



