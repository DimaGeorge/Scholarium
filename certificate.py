import settings
from flask import Blueprint, request
from werkzeug.wrappers import Response
import sys
import hashlib


certificate = Blueprint('certificate', __name__)

@certificate.route(settings.version + '/offchain/certificate', methods = ['GET'])
def integrateCertificate():
    settings.initMultichainNode()
    params = request.get_json()

    # creating the certificate
    if 'file' in params.keys():
        print params['file']
    else:
        return Response("The feature of Scholarium certificates was not yet implemented")

    # hashing the certificate
    sha256 = hashlib.sha256()

    fin = open(params['file'], 'rb')
    myData = fin.read()
    fin.close()

    sha256.update(myData)
    
    myHash = sha256.hexdigest()
    
    multisigAddress = settings.actors[params['code']]['multisig']
    print multisigAddress
    settings.multichainNode.issuefrom(settings.myAddress, multisigAddress, settings.diplomaName, 1)
    
    recipient = {settings.myAddress : 1}
    
    hexBloc = settings.multichainNode.createrawsendfrom(multisigAddress, recipient, [myData])
    print hexBloc
    return Response("done")

