#!/usr/bin/python3

import pandas as pd

PEERS_LOG = "peers.log"
PEERSNEW_CSV = "peersnew.csv"

peers = pd.read_csv(PEERS_LOG,
        names=['LocalTimeStamp','Type','ID','TypeDependentParam1',
        'TypeDependentParam2','Peers','InboundPeers'])

# loop rows, print rows where inboundPeers changes
inboundPeers = 0
peers_new = pd.DataFrame(data=None, columns=peers.columns)

for index, row in peers.iterrows():
    if row['InboundPeers'] != inboundPeers:
        inboundPeers = row['InboundPeers']
        peers_new = peers_new.append(row)
        #print(row)
    
peers_new.to_csv(PEERSNEW_CSV)
