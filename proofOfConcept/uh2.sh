#!/bin/bash

#colors
RED='\033[0;31m'
LGREEN='\033[1;32m'
CYAN='\033[0;36m'
NC='\033[0m'
stream='unistream'
chain='unichain2'
#
theme=$LGREEN

## context
haAddr="$(<highAuthority.txt)"
uAddr="$(<university.txt)"
burnaddress="$(<burnaddress.txt)"

###
echo -e ${theme}The university accepts a student ${NC}
sAddr="$(<student.txt)"
if [ -z "$sAddr" ]; then
echo -e "${theme}No student found!${NC}"
fi

~/multichain/src/multichain-cli $chain grantfrom $uAddr $sAddr connect,send,receive
echo -e ${theme}Student - $sAddr ${NC}

echo -e ${theme}The high authority creates a new type of degree... ${NC} 
~/multichain/src/multichain-cli $chain issuefrom $haAddr $haAddr '{"name":"BA", "open":true}' 0 1 0 '{"meaning":"Bachelor of Arts"}'

echo -e ${theme}The high authority gives the university issue permission... ${NC}
~/multichain/src/multichain-cli $chain grantfrom $haAddr $uAddr BA.issue

