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

rpcuser = 'default'
rpcpasswd = 'default'
rpchost = 'localhost'
rpcport = '5001'
chainName = 'unichain'
nodeAddress = 'unichain'
version = '/v1.1'
myAddress = 'none'
myPubKey = 'none'
diplomaName = 'defaultDiploma'
actors = {}

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

    addressesList = multichainNode.listaddresses()
    for item in addressesList:
        if item['ismine'] == True:
            myAddress = item['address']

    myPubKey = multichainNode.validateaddress(myAddress)['pubkey']

    with open('./res/actors', 'r') as fin:
        actors = json.load(fin)

def updateChainName(param):
    global chainName
    global nodeAddress
    chainName = param
    nodeAddress = param
            
