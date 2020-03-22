#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
import gc
from pathlib import Path

# Merges txs from 
# another node to fill the missing txs in the curent machine.
# also adds two new params: GasUsed,CapturedLocally
#  CapturedLocally - True - if the block was there; False -> if it was added in this
# GasUsed will be filled in the following Step 1
#  script and in this case, the LocalTimestamp does not count...
#  Input: unique-unique-txs.log.FINAL unique-unique-txs.log.FINAL.OTHERMACHINE
#  Output txs-stage-1.log

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

#INPUT FILES
TXS = sys.argv[1] #"unique-unique-txs.log.FINAL"
OUT = "txs-stage-0.log"

if not os.path.isfile(TXS):
    sys.exit(TXS, ": does not exists!")

if os.path.isfile(OUT):
    sys.exit(OUT, ": already exists!")

dtypes = {
        'LocalTimeStamp'    : 'object',
        'Hash'              : 'object',
        'GasLimit'          : 'object',
        'GasPrice'          : 'object',
        'Value'             : 'object',
        'Nonce'             : 'object',
        'MsgType'           : 'object',
        'Cost'              : 'object',
        'Size'              : 'object',
        'To'                : 'object',
        'From'              : 'object',
        'ValidityErr'       : 'object',
        }

txs = pd.read_csv(TXS, 
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr'], dtype=dtypes)

# add  columns to loc & all captLoc = True
txs = txs.assign(CapturedLocally = np.nan, GasUsed = np.nan, InMainBlock = np.nan,
    InUncleBlocks = np.nan, InOrder = np.nan, NeverCommitting = np.nan,
    CommitTime0 = np.nan, CommitTime3 = np.nan, CommitTime12 = np.nan, CommitTime36 = np.nan)

#out
#txs = txs.sort_values(by=['LocalTimeStamp'])
txs.to_csv(OUT, index=False, header=False)
