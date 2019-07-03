#geth dir  
#TODO   To be changed! 
GETH_DIR=/Users/deus/Desktop/testnet-now/clients-data/

START_BLOCK=$1
echo "start block: $START_BLOCK"

END_BLOCK=$2
echo "end block: $END_BLOCK"

OUT_FILE=$3
echo "out file: $OUT_FILE"


ethereumetl export_blocks_and_transactions \
--start-block $START_BLOCK \
--end-block $END_BLOCK \
--provider-uri file://$GETH_DIR/geth.ipc \
--batch-size 100 \
--max-workers 4 \
--blocks-output $OUT_FILE \
--transactions-output /dev/null
