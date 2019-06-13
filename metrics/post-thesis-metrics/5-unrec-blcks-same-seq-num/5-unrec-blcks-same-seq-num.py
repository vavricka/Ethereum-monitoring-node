#!/usr/bin/python3

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

BLOCKS_LOG = sys.argv[1]  # blocks-stage-4.log

#check - that log-file exists
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
        'BlockType'     : 'object',
        'ForkLength'    : 'int',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    dtype=dtypes_blocks)


#DO ONLY ONCE   NOT TO LOAD whole block-stage4 all the tim
#drop all blocks except unrecognized forks
#blocks = blocks[blocks.BlockType == "Uncle"]
#blocks.to_csv("blocks-stage-4-unrec-forks-only.log", index=False, header=False)
#



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




blocks = blocks[blocks.duplicated(['Number', 'Coinbase'], keep=False)]

print("Recognized Uncles:", len(blocks))

for i, row in blocks.iterrows():
    print(row['Number'], row['LocalTimeStamp'], row['BlockHash'],
    row['MiningPool'])#,row['CapturedLocally'])
        



