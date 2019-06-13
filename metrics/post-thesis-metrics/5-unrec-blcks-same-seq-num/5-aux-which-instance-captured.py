import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter - blocks-propagation-times.log.")

BLOCKS_LOG = sys.argv[1] #"blocks-propagation-times.log"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

dtypes_blocks = {
        'BlockHash'         : 'object',
        'Number'            : 'int',
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

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp',
        'S1USTimeStamp','S2CNTimeStamp','FirstObservation',
        'AngainorDiff','FalconDiff','S1USDiff','S2CNDiff'],
    dtype=dtypes_blocks)


#concat all propag delays as in Decker's work
#series_all = pd.concat([blocks['AngainorDiff'], blocks['FalconDiff'],
#    blocks['S1USDiff'],blocks['S2CNDiff']], ignore_index=True)



block_numbers = [7502124,7539271,7578014,7590000,7597411,7631234]

blocks = blocks[  (blocks['Number'] == 7502124 ) | (blocks['Number'] == 7539271 ) |
    (blocks['Number'] == 7578014 ) | (blocks['Number'] == 7590000 ) |
    (blocks['Number'] == 7597411 ) | (blocks['Number'] == 7631234 ) ]

print(blocks)



#for block_num in block_numbers:

