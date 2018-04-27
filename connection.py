from werkzeug.wrappers import Response
from flask import Blueprint, request
import settings
import subprocess
from Savoir import Savoir
import time
import json

connection = Blueprint('connection', __name__)

@connection.route(settings.version + '/blockchain/connection' , methods = ['OPTIONS'])
def uselessFunction():
    rsp = Response("")
    rsp.headers['Access-Control-Allow-Origin']='*'
    rsp.headers['Access-Control-Max-Age'] = 3628800
    rsp.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT'
    rsp.headers['Access-Control-Allow-Headers'] = 'content-type' 
    return rsp

@connection.route(settings.version + '/blockchain/connection', methods = ['POST'])
def connectToExistingChain():
    parameter = request.get_json()
    settings.nodeAddress = parameter
    settings.chainName = parameter.split("@")[0]
    return settings.corsResponse(parameter)

@connection.route(settings.version + '/blockchain/connection' , methods = ['GET'])
def getNodeAddress():
    settings.initMultichainNode()
    return settings.corsResponse(settings.multichainNode.getinfo()['nodeaddress'])

@connection.route(settings.version + '/blockchain/connection' , methods = ['PUT'])
def startChain():
    if settings.nodePid == 0:
        command = [settings.pathToMultichain + "/multichaind", "-daemon", settings.nodeAddress] 
        proc = subprocess.Popen(command)
        settings.nodePid = proc.pid
        if settings.nodePid == 0:
            return settings.corsResponse("Something went wrong when trying to start the chain!")
        else:
            return settings.corsResponse("Node running.")
    else:
        return settings.corsResponse(settings.killNode())

