# Ethereum Monitoring Client (EMC)
EMC is an Ethereum network behavior monitoring client based on the official Go-lang implementation.

- **This project is at a very early stage of development.**

- List of functionalities will be continuously extended.

- Temporarily - for development purposes - we provide two subsidiary scripts: __deploy_net.sh__ and __run_instance.sh__. Below, one can find instructions how to run them.

### Private Network Deployment Script
- To deploy a private network with \<n\> clients run:
```sh
sh deploy_net.sh <n>
```
- e.g.
```sh
sh deploy_net.sh 3
```
- This script expects exactly one integer parameter (1 - 10) which represents the number of Geth instances to be deployed.
- It initializes for each Geth instance a separate data directory to store the network state and loads a (configured) genesis block.

### Running a Geth Instance
If you have deployed a private network of 3 nodes and want to run them all; first, open 3 terminals.
- In each terminal, run:
```sh
$sh run_client.sh <m>
```
- For m: <1,3>



## Geth Console Use-Cases
The *run_client.sh* command should open a Geth console. In the following text, we refer to n-th Console as (C\<n\>).

#### Peers Interconnection
In the official public Ethereum network, there are boot-strap nodes that help find other peers to connect to. In a private network, it is needed to do this manually.

- Get the "enode" identifier of Client 1:
```
(C1) > admin.nodeInfo.enode
"enode://0e409a08482fcd8390797422438a0e3f909ba93cc925675e6fce6221be49b7666f0b2f6106e1b5936aa96c0ca59c8d9b1d7f642657dfa842eb88c8a66c70655b@[::]:30301?discport=0"
```

- Connect Client 2 to Client 1:
```
(C2) > admin.addPeer("enode://0e409a08482fcd8390797422438a0e3f909ba93cc925675e6fce6221be49b7666f0b2f6106e1b5936aa96c0ca59c8d9b1d7f642657dfa842eb88c8a66c70655b@[::]:30302?discport=0")
```
- Check that connecting was successful.
```
(C2) > admin.peers
```
- (Similarly connect other peers)



#### Account Creation and Mining

- Create a new account on Client two with password "testing".
```
(C2) > personal.newAccount("testing")
```

- Make the just created account as the destination for mining rewards.
```
(C2) > miner.setEtherbase(personal.listAccounts[0])
```

- Start mining on Client Two.
```
(C2) > miner.start(1)
```

#### Check Balance
- Check the account balance of the accounts[0] on the Client Two.
```
(C2) > primary = eth.accounts[0]
(C2) > balance = web3.fromWei(eth.getBalance(primary), "ether");
```

#### Sending Transactions

Send 6.23 Ethers from an account that exists on the current session (if you followed the previous steps, it should work).
```
(C2) > var tx = {from: "0x391694e7e0b0cce554cb130d723a9d27458f9298", to: "0xafa3f8684e54059998bc3a7b0d2b0da075154d66", value: web3.toWei(6.23, "ether")}
undefined
(C2) > personal.sendTransaction(tx, "passphrase")
0x8474441674cdd47b35b875fd1a530b800b51a5264b9975fb21129eeb8c18582f
```
