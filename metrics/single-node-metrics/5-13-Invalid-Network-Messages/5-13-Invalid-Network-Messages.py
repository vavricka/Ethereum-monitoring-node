#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

LOG_FILE = sys.argv[1]      # "invalidmsgs.log"

if not os.path.isfile(LOG_FILE):
    sys.exit(LOG_FILE, ": does not exists!")

dtypes = {
    'LocalTimeStamp': 'object',
    'MessageType'   : 'object',
    'Cause'         : 'int',
    }

invMsgs = pd.read_csv(LOG_FILE, 
    names=['LocalTimeStamp','MessageType','Cause'], 
    usecols=['MessageType','Cause'], dtype=dtypes)

#Per message type and cause.
print(invMsgs["Cause"].value_counts())
