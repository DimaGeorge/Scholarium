from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess

blockchain = Blueprint('blockchain', __name__)

@blockchain.route(settings.version + '/blockchain' , methods = ['POST'])
def createChain():
    parameter = request.get_json()
    settings.chainName = parameter['chainName']
    # to verify if some of the params received are in the default params
    command = (
        [settings.pathToMultichain + "/multichain-util"]
        + [ "create" , settings.chainName] 
        + parameter['params'] 
        + settings.defaultBlockchainParamsList
        )
    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    return Response(output)

@blockchain.route(settings.version + '/blockchain' , methods = ['GET'])
def startChain():
    parameter = request.get_json()
    command = [settings.pathToMultichain + "/multichaind", "-daemon", settings.chainName] 
    settings.nodePid = subprocess.Popen(command).pid
    return Response("Node running.\n")

@blockchain.route(settings.version + '/blockchain' , methods = ['DELETE'])
def destroyChain():
    if settings.nodePid == 0:
        return Response("pid 0")
    else:
        command = ["kill", "-9", str(settings.nodePid)]
        subprocess.call(command)
    
    command = ["rm", "-r" , settings.pathToHiddenMultichain + "/" + settings.chainName] 
    subprocess.call(command)
    return Response("Node killed and chain deleted.\n")