#!/usr/bin/python3

import pandas as pd

PEERS_CSV = "peers.csv"
PEERSNEW_CSV = "peersnew.csv"

peers = pd.read_csv(PEERS_CSV)

# loop rows, print rows where inboundPeers changes
inboundPeers = 0
peers_new = pd.DataFrame(data=None, columns=peers.columns)
peers_new.set_index('LocalTimeStamp',inplace=True)

for index, row in peers.iterrows():
    if row['InboundPeers'] != inboundPeers:
        inboundPeers = row['InboundPeers']
        peers_new = peers_new.append(row)
        #print(row)
    
peers_new.to_csv(PEERSNEW_CSV)
