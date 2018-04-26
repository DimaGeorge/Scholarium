import settings
from flask import Blueprint, request
from werkzeug.wrappers import Response
import sys
import hashlib
import json

certificate = Blueprint('certificate', __name__)

@certificate.route(settings.version + '/offchain/certificate', methods = ['GET'])
def integrateCertificate():
    settings.initMultichainNode()
    with open("./res/identity", 'r') as fin:
        identiy = json.load(fin)
        if identiy['rank'] == 1:
            print "You are a High Authority. You can issue certificates, but you shouldn't"
        elif identiy['rank'] == 2:
            print "You are a Certifying Entity. Happy certifying!"
        else:
            print "You don't have permissions to create certificates"
            return Response("")

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
    settings.multichainNode.issuemorefrom(settings.myAddress, multisigAddress, settings.diplomaName, 1)
    recipient = {settings.myAddress : {settings.diplomaName : 1}}
    hexBloc = settings.multichainNode.createrawsendfrom(multisigAddress, recipient, [myHash])

    ## semnez?
    hexBloc = settings.multichainNode.signrawtransaction(hexBloc)['hex']
    retval = {'cert': myData, 'transaction': hexBloc}

    return Response(json.dumps(retval))

