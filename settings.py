from Savoir import Savoir
from os.path  import expanduser
import signal
import subprocess
import json

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
global diplomaName
global actors
global identitySetted

rpcuser = 'default'
rpcpasswd = 'default'
rpchost = 'localhost'
rpcport = '5001'
chainName = 'unichain'
nodeAddress = 'unichain'
version = '/v1.1'
myAddress = 'none'
myPubKey = 'none'
diplomaName = 'ud'
actors = {}
identitySetted = True

defaultBlockchainParamsList = [
    '-anyone-can-connect=true',
    '-default-rpc-port=' + rpcport
]

homeDir = expanduser("~")
pathToMultichain = homeDir + '/multichain/src'
pathToHiddenMultichain = homeDir + '/.multichain'

nodePid = 0

multichainNode = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainName)


def exitGracefully(signum, frame):
    killNode()
    exit()

def killNode():
    global nodePid
    global rpcport
    if(nodePid):
        command = ["kill", "-9", str(nodePid)]
        subprocess.call(command)
        command = ["fuser", rpcport + "/tcp", "-k"]
        subprocess.call(command)
        nodePid = 0
        return "Node stopped.\n"

signal.signal(signal.SIGTERM, exitGracefully)
signal.signal(signal.SIGINT, exitGracefully)

def initMultichainNode():
    global multichainNode
    global myAddress
    global myPubKey
    global pathToHiddenMultichain
    global chainName
    global rpcuser
    global rpcpasswd
    global actors

    confFilePath = (pathToHiddenMultichain + "/" + chainName + "/multichain.conf")
    confFile = open(confFilePath, 'r')
    confFileContent = confFile.read()
    rows = confFileContent.split("\n")
    rpcuser = rows[0].split("=")[1]
    rpcpasswd = rows[1].split("=")[1]
    print "GOT " + rpcuser + "-" + rpcpasswd

    multichainNode = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainName)
    print "Multichain node initiated!"

    if(identitySetted):
        with open('./res/identity', 'r') as fin:
            identity = json.load(fin)
            myAddress = identity['address']
            myPubKey = identity['pubkey']
    else:
        addressesList = multichainNode.listaddresses()
        myAddress = addressesList[0]['address'] # not got to take the last address, when you import multisg addresses
        myPubKey = multichainNode.validateaddress(myAddress)['pubkey']
        permissions = multichainNode.listpermissions('*', myAddress)
        rank = 4
        for item in permissions:
            if item['type'] == 'admin':
                rank = 1
                break
            elif item['type'] == 'activate':
                rank = 2
            elif (item['type'] == 'send') and (rank > 2):
                rank = 3

        identity = {'address': myAddress, 'pubkey': myPubKey, 'rank':rank}
        with open('./res/identity', 'w') as fout:
            json.dump(identity, fout)

    with open('./res/actors', 'r') as fin:
        actors = json.load(fin)

def updateChainName(param):
    global chainName
    global nodeAddress
    chainName = param
    nodeAddress = param
            
