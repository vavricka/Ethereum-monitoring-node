#!/usr/bin/python3
#this script filters out redundat receptions of the same blocks
#leaves the first reception only

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#check   -   need exactly one param
if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

BLOCKS_LOG = sys.argv[1]                      #input .log  (not .csv)

#check - that log-file exists
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

#create output file
UNIQUE_BLOCKS = "unique-" + BLOCKS_LOG          #output .log
Path(UNIQUE_BLOCKS).touch()

dtypes = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'         : 'object',
        }

blocks = pd.read_csv(BLOCKS_LOG, dtype=dtypes,
    names=['LocalTimeStamp','BlockHash'])

blocks.drop_duplicates('BlockHash', inplace=True)

blocks.to_csv(UNIQUE_BLOCKS, index=False, header=False)
