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
        'Number'            : 'object',
        'BlockType'            : 'object',
        'AngainorTimeStamp' : 'object',
        'FalconTimeStamp'   : 'object',
        'PositiveDif'       : 'float',
        'AngainorMinusFalcon'   : 'float',
        'FalconMinusAngainor'   : 'float',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp',
        'PositiveDif','AngainorMinusFalcon','FalconMinusAngainor'],
    #usecols=['PositiveDif','AngainorMinusFalcon','FalconMinusAngainor'],
    dtype=dtypes_blocks)



    
# TODO !! plots histohrams

print(len(blocks))

