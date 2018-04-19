from werkzeug.wrappers import Response
from flask import Blueprint, request
import settings
import subprocess

connection = Blueprint('connection', __name__)

@connection.route(settings.version + '/blockchain/connection' , methods = ['POST'])
def connectToChain():
    return Response("")

@connection.route(settings.version + '/blockchain/connection' , methods = ['PUT'])
def startChain():
    if settings.nodePid == 0:
        command = [settings.pathToMultichain + "/multichaind", "-daemon", settings.chainName] 
        settings.nodePid = subprocess.Popen(command).pid
        if settings.nodePid == 0:
            return Response("Something went wrong when trying to start the chain!")
        else:
            return Response("Node running.\n")
    else:
        command = ["kill", "-9", str(settings.nodePid)]
        subprocess.call(command)
        settings.nodePid = 0
        return Response("Node stopped.\n")