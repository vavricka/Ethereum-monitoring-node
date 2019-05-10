#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import inspect

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

BLOCKS_LOG = sys.argv[1]   # "5-9-uncles-jaro.log"

#check - that log-file exists
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

dtypes_blocks = {
        'LocalTimeStamp' : 'object',
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
        'ForkLength'        : 'int',
        'NumTxs'            : 'int',
        'NumTxsInCorrespondingMain' : 'int',
        'NumCommonTxs'      : 'int',
        'JaroCommonTxsOnly' : 'float',
        'JaroAllTxs'        : 'float',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength',
    'NumTxs', 'NumTxsInCorrespondingMain', 'NumCommonTxs', 'JaroCommonTxsOnly', 'JaroAllTxs'],
    dtype=dtypes_blocks)



print( "forks total:", len(blocks))
print( "forks with exactly the same tx ordering as main blocks:",
    len(blocks[  blocks.JaroCommonTxsOnly == 1   ]  )   )


#NumTxsMinFromBoth: MIN number of txs from both NUMBER-OF-TXS-IN-UNCLE  and  NUMBER-OF-TXS-IN-CORRESPONDING-MAIN
#ProportionOfTxsInBoth:   NumCommonTxs/NumTxsMinFromBoth
blocks = blocks.assign(NumTxsMinFromBoth = 0, ProportionOfTxsInBoth = 0.0, ProportionToMain = 0.0, ProportionToUncle = 0.0)
for i in blocks.index:
    blocks.at[i, 'NumTxsMinFromBoth'] = min (blocks.at[i, 'NumTxs'], blocks.at[i, 'NumTxsInCorrespondingMain'])
    
    #proportion of txs in both (PROPORTION to MIN from both)
    if blocks.at[i, 'NumTxsMinFromBoth'] == 0 & blocks.at[i, 'NumCommonTxs'] == 0:
        blocks.at[i, 'ProportionOfTxsInBoth'] = 1
    elif blocks.at[i, 'NumTxsMinFromBoth'] == 0:
        blocks.at[i, 'ProportionOfTxsInBoth'] = 0
    else:
        blocks.at[i, 'ProportionOfTxsInBoth'] =  blocks.at[i, 'NumCommonTxs']/blocks.at[i, 'NumTxsMinFromBoth'] 



    if blocks.at[i, 'NumTxsInCorrespondingMain'] == 0 & blocks.at[i, 'NumCommonTxs'] == 0:
        blocks.at[i, 'ProportionToMain'] = 1
    elif blocks.at[i, 'NumTxsInCorrespondingMain'] == 0:
        blocks.at[i, 'ProportionToMain'] = 0
    else:
        blocks.at[i, 'ProportionToMain'] =  blocks.at[i, 'NumCommonTxs']/blocks.at[i, 'NumTxsInCorrespondingMain'] 

    if blocks.at[i, 'NumTxs'] == 0 & blocks.at[i, 'NumCommonTxs'] == 0:
        blocks.at[i, 'ProportionToUncle'] = 1
    elif blocks.at[i, 'NumTxs'] == 0:
        blocks.at[i, 'ProportionToUncle'] = 0
    else:
        blocks.at[i, 'ProportionToUncle'] =  blocks.at[i, 'NumCommonTxs']/blocks.at[i, 'NumTxs'] 



#print stats
num_uncles_all = len(blocks)
print("number of all uncles:", num_uncles_all)

median_jaro = np.median(blocks['JaroAllTxs'].values) 
print("median jaro: {0:.4f}".format(median_jaro) )

median_jaro_common_txs_only = np.median(blocks['JaroCommonTxsOnly'].values) 
print("median jaro (of common txs only): {0:.4f}".format(median_jaro_common_txs_only) )

median_proportion_of_common_txs = np.median(blocks['ProportionOfTxsInBoth'].values) 
print("median proportion of common txs: {0:.4f}".format(median_proportion_of_common_txs) )

median_proportion_of_common_txs_to_MAIN = np.median(blocks['ProportionToMain'].values) 
print("median proportion of common txs to main: {0:.4f}".format(median_proportion_of_common_txs_to_MAIN) )

median_proportion_of_common_txs_to_UNCLE = np.median(blocks['ProportionToUncle'].values) 
print("median proportion of common txs to uncle: {0:.4f}".format(median_proportion_of_common_txs_to_UNCLE) )


#PLOT graph
s_jaro     =  blocks.JaroAllTxs
s_jaro_common_txs = blocks.JaroCommonTxsOnly

bin_seq = list(np.arange(0,1,0.001))    #np.arange(0, 1.1, step=0.1)
fig, ax = plt.subplots()

counts_jaro, bin_edges_jaro = np.histogram (s_jaro, bins=bin_seq)
cdf_jaro = np.cumsum (counts_jaro)
linetxs0, = ax.plot (bin_edges_jaro[1:], cdf_jaro/cdf_jaro[-1], label='All transactions from both blocks')

counts_jaro_common_txs, bin_edges_jaro_common_txs = np.histogram (s_jaro_common_txs, bins=bin_seq)
cdf_jaro_common_txs = np.cumsum (counts_jaro_common_txs)
linetxs0to20, = ax.plot (bin_edges_jaro_common_txs[1:], cdf_jaro_common_txs/cdf_jaro_common_txs[-1], label='Common transactions only')

plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
#
plt.xlabel('Jaro metric')
plt.xscale('linear')
ax.set_xlim(left=0)
ax.set_xlim(right=1)
nums = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
labels = ['0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1']

plt.xticks(nums, labels)
ax.legend()

#LOCAL show
#plt.show()
##save to file
plt.savefig('5-9-JARO-Tx-reordering-in-forked-blocks.pdf')
