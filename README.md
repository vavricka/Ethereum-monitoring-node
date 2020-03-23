# Ethereum Monitoring Client (EMC)
EMC is a platform for measuring the Ethereum network. The two main components are the modified Ethereum client (go-ethereum) and a logger (rsyslog).

##### go-ethereum
Contains the measurement Ethereum client based on [Geth 1.8.23](https://github.com/ethereum/go-ethereum/tree/release/1.8).

##### rsyslog
A Rsyslog configuration to capture logs from go-ethereum.

##### run_client.sh
Executes the measuring instance.

##### log-pre-processing
Contains Shell and Python scripts that process the raw logs.

![Log processing](images/flow-diagram.png)

##### metrics
A set of scripts that plot metrics.







## License

The content of this repository outside of the `go-ethereum` directory is licensed under the
[GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html).

The license specification of the `go-ethereum` directory is defined in the `go-ethereum/README.md` file.
