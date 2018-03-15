#colors
RED='\033[0;31m'
LGREEN='\033[1;32m'
CYAN='\033[0;36m'
NC='\033[0m'
stream='unistream'
chain='unichain2'
#

theme=$LGREEN
suhAddr="$(<suh.txt)"
burnaddress="$(<burnaddress.txt)"
echo -e "${theme}Revoking the certificate...${NC}"
rawT="$(~/multichain/src/multichain-cli unichain2 createrawsendfrom $suhAddr {\"$burnaddress\":{\"BA\"\:1\}} '[]' sign | grep  -oP '(?<=\")[0-9a-f]*(?=\")' )"
~/multichain/src/multichain-cli unichain2 sendrawtransaction $rawT
