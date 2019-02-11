#!/usr/bin/python3
#this script filters out redundat receptions of the same txs
#leaves the first reception only

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path


#check   -   need exactly one param
if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

TXS_LOG = sys.argv[1]                      #input .log  (not .csv)

#check - that log-file exists
if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

#create output file
UNIQUE_TXS = "unique-" + TXS_LOG          #output .log
Path(UNIQUE_TXS).touch()

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

txs = pd.read_csv(TXS_LOG, dtype=dtypes,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
    'Cost','Size','To','From','ValidityErr'])

txs.drop_duplicates('Hash', inplace=True)

txs.to_csv(UNIQUE_TXS, index=False, header=False)
