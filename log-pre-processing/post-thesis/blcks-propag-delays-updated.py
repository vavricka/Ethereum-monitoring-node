import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameters - block-stage-4.log blocks-propagation-times.log")

BLOCKS_LOG = sys.argv[1] #"blocks-propagation-times.log"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

BLOCK_PROPAG_TIMES_LOG = sys.argv[2] #"blocks-propagation-times.log"
if not os.path.isfile(BLOCK_PROPAG_TIMES_LOG):
    sys.exit(BLOCK_PROPAG_TIMES_LOG, ": does not exists!")

BLOCKS_PROPAG_V2_OUT = "blocks-propagation-times-v2.log"

OUT = "blocks-propagation-times-v2.log"#sys.argv[3] #out
if  os.path.isfile(OUT):
    if input(" blocks-propagation-times-v2.log already exists! rewrite? [y] or exit? [n]: ") == "y":
        pass
    else:
        sys.exit("exiting")

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

dtypes_blocks_propag_times = {
        'BlockHash'         : 'object',
        'Number'            : 'object',
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
        }

# load  blck-st-4   ;  load only needed   things (surely not txs)
blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    dtype=dtypes_blocks)

#load blocks
block_propag_times = pd.read_csv(BLOCK_PROPAG_TIMES_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp', #BLOCKTYPE not set..
        'S1USTimeStamp','S2CNTimeStamp','FirstObservation',
        'AngainorDiff','FalconDiff','S1USDiff','S2CNDiff'],
    dtype=dtypes_blocks_propag_times)

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

block_propag_times = block_propag_times.assign(MiningPool = "",
    NumTransactions = 0, SameMinerSeqLen = np.nan, PositionInsideSeq = np.nan, Difficulty = "",BlockSize = np.nan)

main_blocks = blocks[ blocks['BlockType'] == "Main" ]

#    SameMinerSeqLen (1-9) and PositionInsideSeq  eg for seq 3,.. first 1, second2, last 3
# for non-main blocks  keep  np.nan for those two. 
main_blocks = main_blocks.sort_values(by=['Number'])
main_blocks.reset_index(inplace=True, drop=True)
main_blocks = main_blocks.assign(SameMinerSeqLen = np.nan, PositionInsideSeq = np.nan)

cur_seq = 1
for i in main_blocks.index:
    if i == 0:
        prevMiner = main_blocks.at[i, 'MiningPool']
        continue
    
    #cur miner the same as the previous one
    if (main_blocks.at[i, 'MiningPool'] == prevMiner):
        cur_seq = cur_seq + 1
    #cur miner changed.. -> it's needed to compute len seq and set prev  and all prev miners from the seq
    else:
        l = 1
        for k in range(i-cur_seq, i):
            main_blocks.at[k, 'SameMinerSeqLen'] = cur_seq
            main_blocks.at[k, 'PositionInsideSeq'] = l
            l = l + 1

        # reset cur seq to 1
        cur_seq = 1

    prevMiner = main_blocks.at[i, 'MiningPool']

    #last block... must set len
    if (i == main_blocks.index[-1]):
        l = 1
        for k in range(i-cur_seq+1, i+1):
            main_blocks.at[k, 'SameMinerSeqLen'] = cur_seq
            main_blocks.at[k, 'PositionInsideSeq'] = l
            l = l + 1
            #tmp
            #print(main_blocks.at[k, 'Number'], prevMiner,cur_seq, l-1)

# sort mainblocks by hash
main_blocks = main_blocks.sort_values(by=['BlockHash'])
blocks = blocks.sort_values(by=['BlockHash'])

for i in block_propag_times.index:
    blockHash = block_propag_times.at[i, 'BlockHash'] 

    #find mainblocks with given hash and fill all data to  block_propag_times_BLOCK
        # searchsorted uses Binary search so it's fast.
    try:
        line = blocks['BlockHash'].searchsorted(blockHash) 

        if blockHash == blocks.iloc[line]['BlockHash']:
            #print('found', blockHash)
            pass
    except (IndexError, KeyError):
        #tmp
        print('not found in main_blcks', blockHash)
        continue

    #BlockType
    block_propag_times.at[i, 'BlockType'] = blocks.iloc[line]['BlockType']
    #mining pool
    block_propag_times.at[i, 'MiningPool'] = blocks.iloc[line]['MiningPool']
    #blck size
    block_propag_times.at[i, 'BlockSize'] = blocks.iloc[line]['BlockSize']

    try:
        txs = blocks.iloc[line]['ListOfTxs'].split(";")
        #remove empty lines (there is always one empty line at the end of the list)
        txs = list(filter(None, txs))
        numTxs = len(txs)
    except AttributeError:
        numTxs = 0
    
    #num txs
    block_propag_times.at[i, 'NumTransactions'] = numTxs

    #difficulty of blck   DONE
    block_propag_times.at[i, 'Difficulty'] = blocks.iloc[line]['Difficulty']


    #
    if blocks.iloc[line]['BlockType'] != "Main":
        continue

    #find mainblocks with given hash and fill all data to  block_propag_times_BLOCK
    # searchsorted uses Binary search so it's fast.
    try:
        line = main_blocks['BlockHash'].searchsorted(blockHash) 

        if blockHash == main_blocks.iloc[line]['BlockHash']:
            #print('found', blockHash)
            pass
    except (IndexError, KeyError):
        #tmp
        print('not found in main_blcks', blockHash)
        continue

    block_propag_times.at[i, 'SameMinerSeqLen'] = main_blocks.iloc[line]['SameMinerSeqLen']
    block_propag_times.at[i, 'PositionInsideSeq'] = main_blocks.iloc[line]['PositionInsideSeq']


#float to int
block_propag_times['SameMinerSeqLen'] = block_propag_times['SameMinerSeqLen'].astype('Int32')
block_propag_times['PositionInsideSeq'] = block_propag_times['PositionInsideSeq'].astype('Int32')
block_propag_times['NumTransactions'] = block_propag_times['NumTransactions'].astype('Int32')#.apply(np.int64)
block_propag_times['BlockSize'] = block_propag_times['BlockSize'].astype('Int32')

# sort by timestamp
block_propag_times.sort_values(by=['Number'], inplace=True)
block_propag_times.to_csv(OUT, index=False, header=False)
