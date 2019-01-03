#!/usr/bin/python3

#this script filters out redundat receptions of the same txs
#leaves the first reception only

import pandas as pd
import numpy as np

TXS_CSV = "txs.csv"
UNIQUE_TXS_CSV = "txsNoDuplicates.csv"

txs = pd.read_csv(TXS_CSV, index_col=0)

txsNoDuplicates = txs.drop_duplicates('Hash')

#print(txsNoDuplicates)

txsNoDuplicates.to_csv(UNIQUE_TXS_CSV)
