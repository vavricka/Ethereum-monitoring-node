import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

#print all columns (not to cut the tail)
pd.set_option('display.expand_frame_repr', False)

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

BLOCKS = sys.argv[1] #"blocks-stage-4.log"
if not os.path.isfile(BLOCKS):
    sys.exit(BLOCKS, ": does not exists!")

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
blocks = pd.read_csv(BLOCKS, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    usecols=['BlockHash','Number', 'Coinbase','BlockType', 'ListOfTxs'],
    dtype=dtypes_blocks)



# assign number of txs to every block
blocks = blocks.assign(NumTxs = 0)
for id_block, row in blocks.iterrows():
    try:
        txs = row['ListOfTxs'].split(";")
        #remove empty lines (there is always one empty line at the end of the list)
        txs = list(filter(None, txs))
        num_txs_in_uncle_block = len(txs)
    except AttributeError:
        num_txs_in_uncle_block = 0
    
    blocks.at[id_block, 'NumTxs'] = num_txs_in_uncle_block

num_total = len(blocks)
print("BLOCKS:", num_total)

####### ASSIGN     15 biggest   AND    all the rest in one
blocks = blocks.assign(MiningPool = "ALL-OTHER-MINERS")
blocks.loc[blocks['Coinbase'] == "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8", 'MiningPool'] = "Ethermine"
blocks.loc[blocks['Coinbase'] == "0x5A0b54D5dc17e0AadC383d2db43B0a0D3E029c4c", 'MiningPool'] = "Sparkpool"
blocks.loc[blocks['Coinbase'] == "0x829BD824B016326A401d083B33D092293333A830", 'MiningPool'] = "f2pool2"
blocks.loc[blocks['Coinbase'] == "0x52bc44d5378309EE2abF1539BF71dE1b7d7bE3b5", 'MiningPool'] = "Nanopool"
blocks.loc[blocks['Coinbase'] == "0xb2930B35844a230f00E51431aCAe96Fe543a0347", 'MiningPool'] = "miningpoolhub1"
blocks.loc[blocks['Coinbase'] == "0x1B5B5906306c96b842dc03105E3b38636A4EDa0b", 'MiningPool'] = "HuoBi.pro"
blocks.loc[blocks['Coinbase'] == "0x2a5994b501E6A560e727b6C2DE5D856396aaDd38", 'MiningPool'] = "pandapool"
blocks.loc[blocks['Coinbase'] == "0x2a65Aca4D5fC5B5C859090a6c34d164135398226", 'MiningPool'] = "DwarfPool1"
blocks.loc[blocks['Coinbase'] == "0x005e288D713a5fB3d7c9cf1B43810A98688C7223", 'MiningPool'] = "xnpool"
blocks.loc[blocks['Coinbase'] == "0xD224cA0c819e8E97ba0136B3b95ceFf503B79f53", 'MiningPool'] = "uupool"
blocks.loc[blocks['Coinbase'] == "0x09ab1303d3CcAF5f018CD511146b07A240c70294", 'MiningPool'] = "Minerall"
blocks.loc[blocks['Coinbase'] == "0x35F61DFB08ada13eBA64Bf156B80Df3D5B3a738d", 'MiningPool'] = "firepool"
blocks.loc[blocks['Coinbase'] == "0x04668Ec2f57cC15c381b461B9fEDaB5D451c8F7F", 'MiningPool'] = "zhizhu"
blocks.loc[blocks['Coinbase'] == "0x06B8C5883Ec71bC3f4B332081519f23834c8706E", 'MiningPool'] = "MiningExpress"
blocks.loc[blocks['Coinbase'] == "0x4C549990A7eF3FEA8784406c1EECc98bF4211fA5", 'MiningPool'] = "Hiveon"

#  crate a data framame   with  one min. pool  for each row
min_pools_list = blocks['MiningPool'].unique() 

min_pools = pd.DataFrame(min_pools_list, columns =['Pool'])
min_pools.set_index('Pool', inplace=True)

counts_of_blcks_per_pool = blocks['MiningPool'].value_counts(dropna=False)

min_pools = min_pools.assign(blocks = np.nan, power = np.nan)

for i in min_pools.index:
    num_blocks = len(blocks[blocks['MiningPool'] == i])
    min_pools.at[i, 'blocks'] = num_blocks
    min_pools.at[i, 'power'] = num_blocks / num_total

min_pools = min_pools.sort_values('power', ascending=False)

min_pools['blocks'] = min_pools['blocks'].apply(np.int64)

#print
min_pools['power'] = pd.Series(["{0:.2f}%".format(val * 100) for val in min_pools['power']], index = min_pools.index)
print (min_pools)
