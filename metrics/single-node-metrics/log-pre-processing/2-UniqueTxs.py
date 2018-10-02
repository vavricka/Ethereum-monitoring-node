#!/usr/bin/python3

#this script filters out redundat receptions of the same txs
#leaves the first reception only

import pandas as pd
import numpy as np

PROJ_ROOT = "/Users/deus/Projects/Ethereum-monitoring-node/"
LOGS_PATH = PROJ_ROOT + "raw-logs/csv/"
FINAL_PATH = PROJ_ROOT + "raw-logs/csv-final/"

TXS_CSV = LOGS_PATH + "TxMsg.csv"
UNIQUE_TXS_CSV = FINAL_PATH + "UniqueTxMsg.csv"

txs = pd.read_csv(TXS_CSV)


txsNoDuplicates = txs.drop_duplicates('Hash')


#print(txsNoDuplicates)

txsNoDuplicates.to_csv(UNIQUE_TXS_CSV)
