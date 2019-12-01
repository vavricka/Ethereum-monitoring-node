# Ethereum Monitoring Client (EMC)
EMC is a platform for measuring the Ethereum network behavior. The two main components are the Ethereum client (go-ethereum) and a logger (rsyslog).

##### go-ethereum
Contains the measurement peer implementation based on [Geth 1.8.23](https://github.com/ethereum/go-ethereum/tree/release/1.8). We made no changes to the program’s logic; the only modifications represent the addition of several syslog calls that capture all received transactions, blocks, etc.

##### rsyslog
A Rsyslog configuration to capture logs from EMC.

### Data processing

##### metrics
The folder 'metrics' contains a set of Shell and Python scripts to process the captured logs.

##### Simplified diagram of log processing
![Log processing](images/flow-diagram.png)






