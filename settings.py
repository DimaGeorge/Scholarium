from Savoir import Savoir

global chainName
global defaultBlockchainParamsList
global rpcuser
global rpcpasswd
global rpchost
global rpcport
global chainName
global pathToMultichain
global version
global multichainNode
global nodePid

defaultBlockchainParamsList = [
    '-anyone-can-connect=true'
]

rpcuser = 'gg'
rpcpasswd = 'gg'
rpchost = 'localhost'
rpcport = '4786'
chainName = 'defaultName'
pathToMultichain = '/home/dimi/multichain/src'
pathToHiddenMultichain = '/home/dimi/.multichain'
version = '/v1.1'
multichainNode = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainName)
nodePid = 0