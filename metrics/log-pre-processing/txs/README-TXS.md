(1) go to the folder with all the txs.log.xx files

(2) copy there concatLogs.sh, txs-dropDuplicates.py, txs-dropDuplicates.sh
     also make sure that you did not forget to do repairLogs.sh first!

(3) $bash txs-dropDuplicates.sh
(Result) it will create one final unique-unique-txs.log.FINAL

(4) bash concatLogs.sh txgasused.log
    also make sure that you did not forget to do repairLogs.sh first!
(Result) txgasused.log.FINAL

(5) copy (rsync) unique-unique-txs.log.FINAL from another machine

#(opt)TODO  copy gas-used.log.FINAL  from another machine

(6) python3 Step-0-Import-Missing-Txs.py unique-unique-txs.log.FINAL.LOCAL \
     unique-unique-txs.log.FINAL.REMOTE
(Result) txs-stage-1.log   (with two new params - GasUsed(notSet),CapturedLocally(set))

#(opt)TODO  missingGasUsed also ....

(7) python3 Step-1-Set-Gas-Used.py txs-stage-1.log txgasused.log
(Results) txs-stage-2.log (with GasUsed set at those txs which were in txgasused.log)


(...) txs-stage.2.log is the final log-file with uniqe txs with all values set.
     Next step is to run individiual metrics.
