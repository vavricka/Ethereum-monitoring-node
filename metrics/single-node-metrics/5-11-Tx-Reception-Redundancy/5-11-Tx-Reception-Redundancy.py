#!/usr/bin/python3

import pandas as pd

TX_CSV = "txs.csv"

#read file into DataFrame
txs = pd.read_csv(TX_CSV, usecols=["Hash"])

#print for each unique txHash it's number of occurencies
#print(txs["Hash"].value_counts())

occurencies = pd.value_counts(txs["Hash"].value_counts().values)
for i, row in occurencies.iteritems():
    print("In total", row, "txs were received", i, "times")

print("Avg number of tx reception", txs["Hash"].value_counts().values.mean())
