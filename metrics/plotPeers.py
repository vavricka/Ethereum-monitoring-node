import pandas as pd                     
import numpy as np  
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PEERS_CSV = "peers.csv"

peers = pd.read_csv(PEERS_CSV, usecols=['LocalTimeStamp', 'Peers'], parse_dates=['LocalTimeStamp'])
peers.rename(columns={'LocalTimeStamp': 'Time'}, inplace=True)
peers.set_index('Time',inplace=True)

# old peers.csv formating
#peers = pd.read_csv(PEERS_CSV, usecols=['LocalTimeStamp', 'TypeDependentParam2'], parse_dates=['LocalTimeStamp'])
#peers.rename(columns={'LocalTimeStamp': 'Time', 'TypeDependentParam2': 'Peers'}, inplace=True)
#peers.set_index('Time',inplace=True)

peers.plot()
plt.show()

