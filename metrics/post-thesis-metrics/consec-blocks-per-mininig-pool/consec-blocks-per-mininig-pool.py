import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

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
    usecols=['BlockHash','Number', 'Coinbase','BlockType'],
    dtype=dtypes_blocks)


####### now just      num of all blcks
len_blocks = len(blocks)
print("blocks total:  ", len_blocks)

#######   num per each coinbase
#print(blocks["Coinbase"].value_counts())




####### ASSIGN
blocks = blocks.assign(MiningPool = "ALL-OTHER-MINERS-TOGETHER", probNext = np.nan, SameMinerSequences = np.nan)
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
blocks.loc[blocks['Coinbase'] == "0x00192Fb10dF37c9FB26829eb2CC623cd1BF599E8", 'MiningPool'] = "2miners"
blocks.loc[blocks['Coinbase'] == "0x52E44f279f4203Dcf680395379E5F9990A69f13c", 'MiningPool'] = "bw"
blocks.loc[blocks['Coinbase'] == "0x6a7a43BE33ba930fE58F34E07D0ad6bA7ADB9B1F", 'MiningPool'] = "Coinotron"
blocks.loc[blocks['Coinbase'] == "0x002e08000acbbaE2155Fab7AC01929564949070d", 'MiningPool'] = "2minerssolo"
# TODO ? consider add more or delete the smallest ?

#print(blocks["MiningPool"].value_counts())

#  take only  MAIN blocks from now
main_blocks = blocks[ blocks['BlockType'] == "Main" ]
rec_uncle_blocks = blocks[ blocks['BlockType'] == "Recognized" ]
unrec_forked_blocks = blocks[ blocks['BlockType'] == "Uncle" ]

len_man_blocks = len(main_blocks)
print("main blocks total:  ", len_man_blocks)
counts_of_blcks_per_pool = main_blocks["MiningPool"].value_counts()
#print(type(counts_of_blcks_per_pool))
#print(counts_of_blcks_per_pool)



#######   just to verify,..  for uncles   and dropped forks  ######
#len_rec_uncle_blocks = len(rec_uncle_blocks)
#print("rec uncle blocks total:  ", len_rec_uncle_blocks)
#print(rec_uncle_blocks["MiningPool"].value_counts())
#
#len_unrec_forked_blocks = len(unrec_forked_blocks)
#print("unrec forked blocks total:  ", 
#len_unrec_forked_blocks)
#print(unrec_forked_blocks["MiningPool"].value_counts())





#  crate a data framame   with  one min. pool  for each row
min_pools_list = main_blocks['MiningPool'].unique() 

min_pools = pd.DataFrame(min_pools_list, columns =['Pool'])
min_pools.set_index('Pool', inplace=True)

min_pools = min_pools.assign( count = counts_of_blcks_per_pool, proportionToTotal = np.nan, SameMinerSequences = 0,
    proportionOfSequences = np.nan, totalVsProporSequences = np.nan)

for i in min_pools.index:
    min_pools.at[i, 'proportionToTotal'] = min_pools.at[i, 'count'] / len_man_blocks

min_pools = min_pools.sort_values('count', ascending=False)



#  reset index, because we dropped some forks and uncles
main_blocks.reset_index(inplace=True, drop=True)


#loop all  main blocks   (SORTED BY   Num  (ascending))
#  set SameMinerSequences
for i in main_blocks.index:

    if i == 0:
        prevMiner = main_blocks.at[i, 'MiningPool']
        continue

    if main_blocks.at[i, 'MiningPool'] == prevMiner:
        min_pools.at[prevMiner, 'SameMinerSequences'] = min_pools.at[prevMiner, 'SameMinerSequences'] + 1
    
    prevMiner = main_blocks.at[i, 'MiningPool']


for i in min_pools.index:
    min_pools.at[i, 'proportionOfSequences'] = min_pools.at[i, 'SameMinerSequences'] / min_pools.at[i, 'count']
    min_pools.at[i, 'totalVsProporSequences'] = min_pools.at[i, 'proportionOfSequences'] - min_pools.at[i, 'proportionToTotal']



print ( min_pools )




