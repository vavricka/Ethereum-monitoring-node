#!/usr/bin/python3

import pandas as pd

PROJ_ROOT = "/Users/deus/Projects/Ethereum-monitoring-node/"
LOGS_PATH = PROJ_ROOT + "raw-logs/csv/"

INVALID_MESSAGES_CSV = LOGS_PATH + "InvalidMessages.csv"

#read file into a DataFrame
invMsgs = pd.read_csv(INVALID_MESSAGES_CSV, usecols=['MessageType','Cause'])   #skipping timestamp - no usage..

#PRINT total number of invalid messages per message type ,  
print(invMsgs["MessageType"].value_counts())
# get indexes
#print(invMsgs["MessageType"].value_counts().index.tolist())
# get values of occurrences
#print(invMsgs["MessageType"].value_counts().values.tolist())

#Per message type and cause.
print(invMsgs["Cause"].value_counts())
