every log that had been divided into 2+ 500MB chunks
it is possible that rsyslog's log-rotation incorrectly cut some
leading and trailing rows of the files.

(1) verify that with this:  (example for txs.log of 20 chunks)
$for i in {0..20}; do echo $i; cat txs.log.$i | grep -v 2019; done

this checks if all leading rows start with "2019" which is desired.
if there are some leading lines starting with a different string

(2) it is needed to fix it using the following command
$bash repairLogs.sh <whatever.log> (txs.log / blocks.log / ... )

(3) diff the repaired logs with the original files that have the
~Backup-Original suffix

(4) if all ok, delete *~Backup-Original files


