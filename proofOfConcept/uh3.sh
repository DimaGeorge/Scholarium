#!/bin/bash

#colors
RED='\033[0;31m'
LGREEN='\033[1;32m'
CYAN='\033[0;36m'
NC='\033[0m'
stream='unistream'
chain='unichain2'
#
theme=$CYAN

## context
haAddr="$(<highAuthority.txt)"
uAddr="$(<university.txt)"
uPub="$(<university.pub)"
burnaddress="$(<burnaddress.txt)"
sAddr="$(<student.txt)"
diplomaHash=11223344556677889900abcdef


echo -e "${theme}The university receives student's pubkey... ${NC}"
sPub="$(<student.pub)"
if [ -z "$sPub" ]; then
echo -e "${theme}Public key not found!${NC}"
exit 1
fi

echo -e "${theme}The university creates SUmultisig address:${NC}"
suAddr="$(~/multichain/src/multichain-cli $chain addmultisigaddress 2 [\"$uPub\",\"$sPub\"])"
echo -e "${theme}SUmultisig - $suAddr ${NC}"

echo -e "${theme}The university grants send,receive to SUmultisig...${NC}"cd 
~/multichain/src/multichain-cli $chain grantfrom $uAddr $suAddr send,receive

echo -e "${theme}The university issues 1BA to SUmultisig...${NC}"
~/multichain/src/multichain-cli $chain issuemorefrom $uAddr $suAddr BA 1 0 '{"occasion":"graduation"}'

echo -e "${theme}The university creates SUHmultisig address:${NC}"
suhAddr="$(~/multichain/src/multichain-cli $chain addmultisigaddress 2 [\"$sPub\",\"$uAddr\",\"$haAddr\"])"
echo -e "${theme}SUHmultisig - $suhAddr ${NC}"
echo $suhAddr > suh.txt  #save the suhAddr for eventual revocation


echo -e "${theme}The university grants send,receive to SUHmultisig...${NC}"
~/multichain/src/multichain-cli $chain grantfrom $uAddr $suhAddr send,receive

echo -e "${theme}The university creates a raw transaction from SU to SUH...${NC}"
rawT="$(~/multichain/src/multichain-cli $chain createrawsendfrom $suAddr {\"$suhAddr\":{\"BA\"\:1\}} [\"$diplomaHash\"])" 
echo -e "${theme}Unsigned raw transaction:${NC} $rawT "

echo -e "${theme}The raw transaction is being signed... ${NC}"
rawT="$(~/multichain/src/multichain-cli $chain signrawtransaction $rawT | grep  -oP '(?<=\")[0-9a-f]*(?=\")')"
echo -e "${theme}Signed raw transaction:${NC} $rawT "

echo -e "${theme}The university publishes transaction in stream${NC} $rawT "
~/multichain/src/multichain-cli $chain publishfrom $uAddr $stream $sAddr $rawT

