(1) go to the folder with all the txs.log.xx files

(2) copy there concatLogs.sh, txs-dropDuplicates.py, txs-dropDuplicates.sh
     also make sure that you did not forget to do repairLogs.sh first!

(3) $bash txs-dropDuplicates.sh
(Result) it will create one final unique-unique-txs.log.FINAL

(4) $bash concatLogs.sh txgasused.log
    also make sure that you did not forget to do repairLogs.sh first!
(Result) txgasused.log.FINAL

(5) $python3 Step-0-Txs-Add-Columns.py unique-unique-txs.log.FINAL
(Result) txs-stage-0.log   (with many new params - GasUsed(notSet),CapturedLocally(set) and so on)

(6) copy (rsync) txs-stage-0.log from other machines
(7) copy (rsync) txgasused.log.FINAL.REMOTE from other machines

(8) $time python3 Step-1-Import-Missing-Txs.py txs-stage-0.log.LOCAL txs-stage-0.log.REMOTE <OUT>
     (quite fast)

(8a)first on angainor
$python3 Step-1-Import-Missing-Txs.py txs-stage-0.log.LOCAL txs-stage-0.log.falcon tmp-txs-A-F
$python3 Step-1-Import-Missing-Txs.py tmp-txs-A-F txs-stage-0.log.s1 tmp-txs-A-F-S1
$python3 Step-1-Import-Missing-Txs.py tmp-txs-A-F-S1 txs-stage-0.log.s2 tmp-txs-A-F-S1-S2
$mv tmp-txs-A-F-S1-S2 txs-stage-1.log

(8b) every machine (except angainor):
$python3 Step-1-Import-Missing-Txs.py txs-stage-0.log txs-stage-1.log.ANGAINOR txs-stage-1.log

---
now, txs-stage-1.logs are logs ready to perform Step-8  propagation delays
 steps 9+ do only on angainor...
---

(9) $time python3 Step-2-Set-Gas-Used.py txs-stage-1.log txgasused.log.FINAL
     (relat. fast - 11m (23m falc) on 4 day logs)
(Results) txs-stage-2.log (with GasUsed set)

(10)
$python3 Step-3-Set-Gas-Used-AFTER.py txs-stage-2.log txgasused.log.FINAL.falcon tmp-gas-A-F
$python3 Step-3-Set-Gas-Used-AFTER.py tmp-gas-A-F txgasused.log.FINAL.s1 tmp-gas-A-F-S1
$python3 Step-3-Set-Gas-Used-AFTER.py tmp-gas-A-F-S1 txgasused.log.FINAL.S2 tmp-gas-A-F-S1-S2
mv tmp-gas-A-F-S1-S2 txs-stage-3.log
(Result) txs-stage-3.log   (possibly) with more gasUsed set
     it can also yield err when it reaches a txs with different gasUsed..

(11) Make sure that blocks-stage-3.log already exists (or stage-4 is also fine)

(12) $time python3 Step-4-Assign-Blocks-To-Txs.py txs-stage-3.log blocks-stage-4.log    (or blocks-stage-3.log)
     11m (ANGAINOR)
(Result) txs-stage-4.log with two last params set:
     InMainBlock (Boolean) - if one of the blocks in which this tx is is Main-chain
     InUncleBlocks - semicolon separated list of uncle-blocks in which this txs is located..

(13) $time python3 Step-5-Commit-Times.py txs-stage-4.log blocks-stage-4.log  #(blocks-stage can be any 3+)
     82m (ANG)
(Result) txs-stage-5.log  with commit times set

(14)   $python3 Step-6-Never-Commiting.py txs-stage-5.log //NeverCommitting [ Committed | nil ]
     (super fast)
(Result) txs-stage-6.log   with  NeverCommitting set [ Committed | NeverCommitting | nil ]  

(15) $python3 Step-7-Set-In-Order.py txs-stage-6.log
     (cca 20 min ANG)
(Result) txs-stage-7.log   InOrder set True/False for every NeverCommitting==Commited..  nil otherwise (must be object, not bool!)  

! txs-stage-7.log is the final log-file to calculate single-node metrics

---
multiple-node metrics:

(16) $python3 Step-8-Set-Propagation-Delays.py txs-stage-7.log.ANGAINOR txs-stage-7.log.FALCON
          #(can be even smaller stage, e.g. 5... )
          26 m Angainor
(Results) txs-propagation-times.log with propagation delays set
 csv-template in metrics/multi../5-2../txs-propagation-times.csv
     (TODO?) if we decide for more geth peers, need to be extended a bit)