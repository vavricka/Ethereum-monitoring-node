(1) go to the folder with all the txs.log.xx files

(2) copy there concatLogs.sh, txs-dropDuplicates.py, txs-dropDuplicates.sh
     also make sure that you did not forget to do repairLogs.sh first!

(3) $bash txs-dropDuplicates.sh
(Result) it will create one final unique-unique-txs.log.FINAL

(4) bash concatLogs.sh txgasused.log
    also make sure that you did not forget to do repairLogs.sh first!
(Result) txgasused.log.FINAL

(5) copy (rsync) unique-unique-txs.log.FINAL from another machine
(6) copy (rsync) txgasused.log.FINAL.REMOTE from another machine

(7) python3 Step-0-Import-Missing-Txs.py unique-unique-txs.log.FINAL.LOCAL \
     unique-unique-txs.log.FINAL.REMOTE
(Result) txs-stage-1.log   (with many new params - GasUsed(notSet),CapturedLocally(set) and so on)

(8) python3 Step-1-Set-Gas-Used.py txs-stage-1.log txgasused.log.FINAL
(Results) txs-stage-2.log (with GasUsed set)

(9) python3 Step-2-Set-Gas-Used-AFTER.py txs-stage-2.log txgasused.log.FINAL.REMOTE
(Result) txs-stage-3.log   (possibly) with more gasUsed set
     it can also yell err when it reaches a txs with different gasUsed..
     do diff txs-stage-3.log and txs-stage-2.log to check some gasUsed were added..

(10) Make sure that blocks-stage-3.log already exists (or stage-4 is also fine)

(11) python3 Step-3-Assign-Blocks-To-Txs.py txs-stage-3.log blocks-stage-3.log
(Result) txs-stage-4.log with two last params set:
     InMainBlock (Boolean) - if one of the blocks in which this tx is is Main-chain
     InUncleBlocks - semicolon separated list of uncle-blocks in which this txs is located..

(12) python3 Step-4-Commit-Times.py txs-stage-4.log blocks-stage-4.log  #(blocks-stage can be any 3+)
(Result) txs-stage-5.log  with commit times set
