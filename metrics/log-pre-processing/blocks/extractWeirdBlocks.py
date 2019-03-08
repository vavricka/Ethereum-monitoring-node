#!/usr/bin/python3

#first param LOG-file ... *should be: unique-unique-blocks.log.FINAL*
#following two input params MIN and MAX (inclusive) block numbers
#that mark the inclusive range of blocks that go to <LOG>.withoutWeirdBlocks
#the block numbers outside this range will go to <LOG>.weirdBlocks

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 4:
    sys.exit(sys.argv[0], ": expecting 3 parameters.")

BLOCKS_LOG = sys.argv[1] #"unique-unique-blocks.log.FINAL"
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

MIN_NUMBER = int(sys.argv[2])
MAX_NUMBER = int(sys.argv[3])

#OUT
BLOCKS_WITHOUT_WEIRD_BLOCKS = BLOCKS_LOG + ".withoutWeirdBlocks"
WEIRD_BLOCKS = BLOCKS_LOG + ".weirdBlocks"

blocks = pd.read_csv(BLOCKS_LOG,
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles'])


#apply conditions
blocks_out = blocks[(blocks.Number >= MIN_NUMBER) & (blocks.Number <= MAX_NUMBER)]
weird_blocks_out = blocks[(blocks.Number < MIN_NUMBER) | (blocks.Number > MAX_NUMBER)]

# Gen out file
blocks_out.to_csv(BLOCKS_WITHOUT_WEIRD_BLOCKS, index=False, header=False)
weird_blocks_out.to_csv(WEIRD_BLOCKS, index=False, header=False)
