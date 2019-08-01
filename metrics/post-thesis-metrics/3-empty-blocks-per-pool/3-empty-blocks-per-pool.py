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
num_with_zero_txs = len(blocks[blocks.NumTxs == 0])

num_main_total = len(blocks[blocks.BlockType == "Main"])
num_main_with_zero_txs = len(blocks[(blocks.BlockType == "Main") & (blocks.NumTxs == 0)])

proportion = num_with_zero_txs / num_total
print("BLOCKS:", num_total, "EMPTY BLOCKS:", num_with_zero_txs,
    "proportion of empty blocks:", proportion)


####### ASSIGN
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
blocks.loc[blocks['Coinbase'] == "0x84A0d77c693aDAbE0ebc48F88b3fFFF010577051", 'MiningPool'] = "(0x84A0d7..)"
blocks.loc[blocks['Coinbase'] == "0xAA5c4244F05c92781C4F259913319d8ba1aCF05E", 'MiningPool'] = "(0xAA5c42..)"
blocks.loc[blocks['Coinbase'] == "0x00192Fb10dF37c9FB26829eb2CC623cd1BF599E8", 'MiningPool'] = "2miners"
blocks.loc[blocks['Coinbase'] == "0x52E44f279f4203Dcf680395379E5F9990A69f13c", 'MiningPool'] = "bw"
blocks.loc[blocks['Coinbase'] == "0x6a7a43BE33ba930fE58F34E07D0ad6bA7ADB9B1F", 'MiningPool'] = "Coinotron"
blocks.loc[blocks['Coinbase'] == "0x858fDEC2da9fA3CD3d97B8Bd1af98E9249D33613", 'MiningPool'] = "(0x858fDE..)"
blocks.loc[blocks['Coinbase'] == "0x002e08000acbbaE2155Fab7AC01929564949070d", 'MiningPool'] = "2minerssolo"



#  crate a data framame   with  one min. pool  for each row
min_pools_list = blocks['MiningPool'].unique() 

min_pools = pd.DataFrame(min_pools_list, columns =['Pool'])
min_pools.set_index('Pool', inplace=True)

counts_of_blcks_per_pool = blocks['MiningPool'].value_counts(dropna=False)

empty_blocks = blocks[ blocks['NumTxs'] == 0 ]
not_empty_blocks = blocks[ blocks['NumTxs'] != 0 ]


min_pools = min_pools.assign(blocks = np.nan, empty_blocks = np.nan,
    emptyVStotBlocks = np.nan)

for i in min_pools.index:
    num_empty = len(empty_blocks[empty_blocks['MiningPool'] == i])
    min_pools.at[i, 'empty_blocks'] = num_empty
    num_blocks = len(blocks[blocks['MiningPool'] == i])
    min_pools.at[i, 'blocks'] = num_blocks
    min_pools.at[i, 'emptyVStotBlocks'] = num_empty / num_blocks

min_pools = min_pools.sort_values('blocks', ascending=False)

min_pools['blocks'] = min_pools['blocks'].apply(np.int64)
min_pools['empty_blocks'] = min_pools['empty_blocks'].apply(np.int64)



### select 15 biggest  (blck 1650+   except ALL-OTHER)
pools_selection = min_pools[   (min_pools.index != "ALL-OTHER-MINERS")  & 
   (min_pools['blocks'] >= 1650)     ]
# or  just fifteen
#pools_selection = min_pools[:15]




x = ['Hiveon', 'MiningExpress', 'Zhizhu', 'Firepool', 'Minerall', 'Uupool', 'Xnpool', 'DwarfPool1', 'Pandapool'
    , 'HuoBi.pro', 'Miningpoolhub1', 'Nanopool', 'F2pool2', 'Sparkpool', 'Ethermine']
s_pools = pools_selection.emptyVStotBlocks

s_pools = np.flip(s_pools)  #, axis=None)[source]¶

x_pos = [i for i, _ in enumerate(x)]

plt.barh(x_pos, s_pools, color='blue')
plt.ylabel("Miners")
plt.xlabel("Percentage of empty blocks")
#plt.title("Empty blocks of the 15 biggest mining entities")

plt.yticks(x_pos, x)

nums = [0,0.05,0.10,0.15,0.20,0.25,0.30]
labels = ['0 %','5 %','10 %','15 %','20 %','25 %','30 %']

plt.xticks(nums, labels)

#plt.show()
#save to file
plt.savefig('ptm-3-empty-blcks-per-miner.pdf', bbox_inches="tight")




#print
min_pools['emptyVStotBlocks'] = pd.Series(["{0:.2f}%".format(val * 100) for val in min_pools['emptyVStotBlocks']], index = min_pools.index)
print (min_pools)

