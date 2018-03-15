#!/bin/bash
#colors
RED='\033[0;31m'
LGREEN='\033[1;32m'
CYAN='\033[0;36m'
NC='\033[0m'
stream='unistream'
#
theme=$LGREEN

#### Create and start chain unichain2

if [ -f ~/.multichain/unichain2/params.dat ]; then
	echo unichain2 already exists!
else
	~/multichain/src/multichain-util create unichain2 
fi

~/multichain/src/multichaind unichain2 -daemon

### Establish the environment

haAddr="$(~/multichain/src/multichain-cli unichain2 listpermissions admin | grep  -oP '(?<=\")1.*(?=\")' | head -n 1)"
echo -e ${theme}High Authority - $haAddr ${NC}

echo -e ${theme}The high authority initialize a burn address ${NC}
burnaddress="$(~/multichain/src/multichain-cli unichain2 getinfo | grep -oP '(?<=\")1X*.*(?=\")')"
~/multichain/src/multichain-cli unichain2 grant $burnaddress receive

echo -e ${theme}The high authority activates a university ${NC}
uAddr="$(~/multichain/src/multichain-cli unichain2 getnewaddress | grep  1.*)"

~/multichain/src/multichain-cli unichain2 grantfrom $haAddr $uAddr activate,create
echo -e ${theme}University - $uAddr ${NC}

echo -e ${theme}The university creates a stream $uAddr ${NC}
~/multichain/src/multichain-cli unichain2 createfrom $uAddr stream $stream true
~/multichain/src/multichain-cli unichain2 subscribe $stream

uPub="$(~/multichain/src/multichain-cli unichain2 validateaddress $uAddr | grep -oP '0[0-9a-f]*' | head -n 1)"
echo -e ${theme}The university save its pubkey : $uPub ${NC}
### Save context

echo $uPub > university.pub
echo $haAddr > highAuthority.txt
echo $uAddr > university.txt
echo $burnaddress >burnaddress.txt


