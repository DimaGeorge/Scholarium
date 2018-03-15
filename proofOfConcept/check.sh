#!/bin/bash
#colors
RED='\033[0;31m'
LGREEN='\033[1;32m'
CYAN='\033[0;36m'
NC='\033[0m'
stream='unistream'
chain='unichain2'
theme=$RED
#
txid="$(<transaction.txid)"
diplomaHash=11223344556677889900abcdef
#
if [ -z "$txid" ]; then
echo -e "${theme}Transaction id not found!${NC}"
exit 1
fi


echo -e "${theme}Proving that the student has the certificate...${NC}"
echo -e "${theme}Verifying that the transaction output was unspent...${NC}"
valid="$(~/multichain/src/multichain-cli $chain gettxout $txid 0)"
if [ -z "$valid" ]; then
echo -e "${theme}The certificate was revoked or is invalid.${NC}"
else
echo $valid
echo -e "${theme}Knowing the txid we get the raw transaction...${NC}"
rawT="$(~/multichain/src/multichain-cli $chain getrawtransaction $txid)"
echo -e "${theme}Decoding the raw transaction in order to see the hash of the diploma...${NC}"
~/multichain/src/multichain-cli $chain decoderawtransaction $rawT | grep $diplomaHash
fi
