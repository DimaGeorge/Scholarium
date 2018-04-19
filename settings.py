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

rpcuser = 'gg'
rpcpasswd = 'gg'
rpchost = 'localhost'
rpcport = '5001'
chainName = 'unichain'

defaultBlockchainParamsList = [
    '-anyone-can-connect=true',
    '-default-rpc-port=' + rpcport
]


pathToMultichain = '/home/dimi/multichain/src'
pathToHiddenMultichain = '/home/dimi/.multichain'
version = '/v1.1'
multichainNode = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainName)
nodePid = 0

def initMultichainNode():
    global multichainNode
    multichainNode = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainName)
    print "Multichain node initiated!"