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
    # to verify if I can do it
    params = request.get_json()
    # creating the certificate
    key = params['pass']
    if key not in settings.actors.keys():
        return "Wrong pass"

    fin = open('res/' + settings.actors[key]['file'], 'rb')
    myData = fin.read()
    fin.close()

    if 'txid' in settings.actors[key].keys():
        retval = {'cert': myData, 'txid': settings.actors[params['pass']]['txid']}
        return Response(json.dumps(retval))

    # hashing the certificate
    sha256 = hashlib.sha256()
    sha256.update(myData)
    myHash = sha256.hexdigest()
    
    multisigAddress = settings.actors[params['pass']]['multisig']
    settings.multichainNode.issuemorefrom(settings.myAddress, multisigAddress, settings.diplomaName, 1)
    recipient = {settings.subscriptionMultisig : {settings.diplomaName : 1}}
    hexBloc = settings.multichainNode.createrawsendfrom(multisigAddress, recipient, [myHash])

    retval = {'cert': myData, 'transaction': hexBloc}
    return Response(json.dumps(retval))

@certificate.route(settings.version + '/offchain/certificate', methods = ['POST'])
def publishTransaction():
    settings.initMultichainNode()
    params = request.get_json()
    hexBloc = settings.multichainNode.signrawtransaction(params['hex'])
    if hexBloc['complete']:
        txid = settings.multichainNode.sendrawtransaction(hexBloc['hex'])
        settings.actors[params['pass']]['txid'] = txid
        settings.saveActors()
        print settings.actors
        return Response(txid)
    else:
        print "Something went wrong"
        return Response("error")
    
