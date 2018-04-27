import settings
from flask import Blueprint, request
from werkzeug.wrappers import Response
import sys
import hashlib
import json
import requests


claim = Blueprint('claim',__name__)

@claim.route(settings.version + '/offchain/certificate/claim' , methods = ['OPTIONS'])
def uselessFunction():
    rsp = Response("")
    rsp.headers['Access-Control-Allow-Origin']='*'
    rsp.headers['Access-Control-Max-Age'] = 3628800
    rsp.headers['Access-Control-Allow-Methods'] = 'POST, PUT'
    rsp.headers['Access-Control-Allow-Headers'] = 'content-type' 
    return rsp

@claim.route(settings.version +'/offchain/certificate/claim', methods=['POST']) #to be continued
def requestCertificate():
    settings.initMultichainNode()
    requestForm = request.get_json()
    url = 'http://' + requestForm['ip'] + '/v1.1/offchain/certificate'
    requestResponse = requests.get(url, json = requestForm).content
    requestResponse = json.loads(requestResponse)
    
    #extract the hash of the cetificate from transaction
    if 'txid' in requestResponse.keys():
        return settings.corsResponse(json.dumps(requestResponse))

    decodedTransaction = settings.multichainNode.decoderawtransaction(requestResponse['transaction'])
    hashedCertificate =decodedTransaction['vout'][1]['data'][0]
    
    #validate certificate
    plainCertificate = requestResponse['cert']
    sha256 = hashlib.sha256()
    sha256.update(plainCertificate)
    myHashedCertificate = sha256.hexdigest()

    if myHashedCertificate == hashedCertificate:
        return settings.corsResponse(json.dumps(requestResponse))
    else: 
        return settings.corsResponse("The certificates do not match")   


@claim.route(settings.version +'/offchain/certificate/claim', methods=['PUT'])
def publishCertificate():
    settings.initMultichainNode()
    publishForm = request.get_json()
    signedTransaction = settings.multichainNode.signrawtransaction(publishForm['transaction'])['hex']
    
    url = 'http://' + publishForm['ip'] + '/v1.1/offchain/certificate'
    publishResponse = requests.post(url, json = {'hex': signedTransaction, 'pass':publishForm['pass']}).content
    return settings.corsResponse(publishResponse)
