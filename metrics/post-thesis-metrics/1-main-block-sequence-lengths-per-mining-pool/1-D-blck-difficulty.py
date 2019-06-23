import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#print all columns (not to cut the tail)
pd.set_option('display.expand_frame_repr', False)

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter - blck-st-4 ")

BLOCKS_LOG = sys.argv[1] 
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

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
        'ForkLength'    : 'int',
        }

# load  blck-st-4   ;  load only needed   things (surely not txs)
blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    usecols=['LocalTimeStamp','Number','BlockHash', 'Difficulty','BlockType'],
    dtype=dtypes_blocks)


main_blocks = blocks[blocks.BlockType == "Main"].copy()
main_blocks.sort_values(by='Number', inplace=True)
main_blocks.set_index('Number', inplace=True, drop=True)


forks = blocks[blocks.BlockType != "Main"].copy()
#forks.sort_values(by='Number', inplace=True)
#forks.set_index('Number', inplace=True, drop=True)



num_fork_higher_dif = 0
num_main_higher_dif = 0
num_same = 0


fork_rec_first1 = 0
main_rec_first1 = 0
fork_rec_first2 = 0
main_rec_first2 = 0

fork_rec_first = 0
main_rec_first = 0

for i in forks.index:
    fork_dif = forks.at[i, 'Difficulty']
    fork_time = forks.at[i, 'LocalTimeStamp']


    block_num = forks.at[i, 'Number']
    main_dif = main_blocks.at[block_num, 'Difficulty']
    main_time = main_blocks.at[block_num, 'LocalTimeStamp']

    if fork_dif > main_dif:
        num_fork_higher_dif = num_fork_higher_dif + 1
        #print("fork", fork_dif, ">", "main", main_dif)

        if pd.to_datetime(fork_time) < pd.to_datetime(main_time):
            fork_rec_first1 = fork_rec_first1 + 1
        else:
            main_rec_first1 = main_rec_first1 + 1

    elif main_dif > fork_dif:
        #print("fork", fork_dif, "<", "main", main_dif)
        num_main_higher_dif = num_main_higher_dif + 1

        if pd.to_datetime(fork_time) < pd.to_datetime(main_time):
            fork_rec_first2 = fork_rec_first2 + 1
        else:
            main_rec_first2 = main_rec_first2 + 1

    else:
        #print("fork", fork_dif, "=", "main", main_dif)
        num_same = num_same + 1

        if pd.to_datetime(fork_time) < pd.to_datetime(main_time):
            fork_rec_first = fork_rec_first + 1
        else:
            main_rec_first = main_rec_first + 1



print('num_fork_higher_dif', num_fork_higher_dif, '(fork_rec_first:', fork_rec_first1, 'main_rec_first:', main_rec_first1, ")")
print('num_main_higher_dif', num_main_higher_dif, '(fork_rec_first:', fork_rec_first2, 'main_rec_first:', main_rec_first2, ")")
print('num_same', num_same, '(fork_rec_first:', fork_rec_first, 'main_rec_first:', main_rec_first, ")")




