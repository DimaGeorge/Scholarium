from werkzeug.wrappers import Response
from flask import Blueprint, request
import settings
import subprocess
from Savoir import Savoir

connection = Blueprint('connection', __name__)

@connection.route(settings.version + '/blockchain/connection', methods = ['POST'])
def connectToExistingChain():
    parameter = request.get_json()
    settings.nodeAddress = parameter
    settings.chainName = parameter.split("@")[0]
    return Response(parameter + "\n")

@connection.route(settings.version + '/blockchain/connection' , methods = ['GET'])
def getNodeAddress():
    return Response(settings.multichainNode.getinfo()['nodeaddress'] + "\n")

@connection.route(settings.version + '/blockchain/connection' , methods = ['PUT'])
def startChain():
    if settings.nodePid == 0:
        command = [settings.pathToMultichain + "/multichaind", "-daemon", settings.nodeAddress] 
        proc = subprocess.Popen(command)
        settings.nodePid = proc.pid
        if settings.nodePid == 0:
            return Response("Something went wrong when trying to start the chain!")
        else:
            readConfFile()
            settings.initMultichainNode()
            return Response("Node running.\n")
    else:
        command = ["kill", "-9", str(settings.nodePid)]
        subprocess.call(command)
        command = ["fuser", settings.rpcport + "/tcp", "-k"]
        subprocess.call(command)
        settings.nodePid = 0
        return Response("Node stopped.\n")


def readConfFile():
    # reading rpcuser and rpcpassword
    confFilePath = (settings.pathToHiddenMultichain 
        + "/" + settings.chainName + "/multichain.conf"
        )
    confFile = open(confFilePath, 'r')
    confFileContent = confFile.read()
    rows = confFileContent.split("\n")
    settings.rpcuser = rows[0].split("=")[1]
    settings.rpcpasswd = rows[1].split("=")[1]
    print "GOT " + settings.rpcuser + "-" + settings.rpcpasswd