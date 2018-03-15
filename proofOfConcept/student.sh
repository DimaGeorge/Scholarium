 #!/bin/bash

#colors
RED='\033[0;31m'
LGREEN='\033[1;32m'
CYAN='\033[0;36m'
NC='\033[0m'
stream='unistream'
#
theme=$LGREEN

chain=$1
chainName=$2

echo -e "${theme}Get student address...${NC}"
sAddr="$(~/Desktop/multichain-master/src/multichaind unichain2@192.168.1.12:6813 -daemon | grep -oP '1[^ \n\.]*(?= )' | tail -n 1)"

echo -- $sAddr
if [ ! -z "$sAddr" ]; then
echo  $sAddr > student.txt
else
sAddr=$(<student.txt)

fi

echo -e "${theme}Get student pubkey...${NC}"
pubKey="$(~/Desktop/multichain-master/src/multichain-cli unichain2 getaddresses true | grep -oP '0[0-9a-f]*' | head -n 1)"
echo --$pubKey

if [ ! -z $pubKey ]; then
echo $pubKey >student.pub
fi

echo -e "${theme}Get university pubkey...${NC}"
uPubKey="$(<university.pub)"

if [ -z $uPubKey ]; then
echo --university pubkey missing
fi
echo --$uPubKey

echo -e "${theme}Genereate multisig address(multis(U,St)...${NC}"
mAddr="$(~/Desktop/multichain-master/src/multichain-cli unichain2 addmultisigaddress 2 [\"$uPubKey\",\"$pubKey\"])"
echo --$mAddr

echo -e "${theme}Import multisig address(multis(U,//St)...${NC}"
~/Desktop/multichain-master/src/multichain-cli unichain2 importaddress $mAddr

echo -e "${theme}Subscribe university stream...${NC}"
~/Desktop/multichain-master/src/multichain-cli unichain2 subscribe unistream

echo -e "${theme}Get the last item publish with the student address...${NC}"
rawT="$(~/Desktop/multichain-master/src/multichain-cli unichain2 liststreamkeyitems unistream $sAddr true 1 | grep  -oP '(?<=\")[0-9a-f]*(?=\")' | head -n 1)"
echo --$rawT

echo -e "${theme}The raw transaction is being signed... ${NC}"
rawT="$(~/Desktop/multichain-master/src/multichain-cli unichain2 signrawtransaction $rawT  | grep  -oP '(?<=\")[0-9a-f]*(?=\")')"

echo -e "${theme}Signed raw transaction:${NC} $rawT "

echo -e "${theme}The complete transaction is being sent...${NC}"
txid="$(~/Desktop/multichain-master/src/multichain-cli unichain2 sendrawtransaction $rawT)"


echo  $txid >transaction.txid




