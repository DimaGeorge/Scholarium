import settings
from flask import Blueprint, request
from werkzeug.wrappers import Response
import sys
import hashlib
import json


request = Blueprint('request',__name__)


@request.route(settings.version +'/offchain/request', methods=['GET'])
def requestCertificate():
    requestForm = request.get_json()

    requestResponse = requests.get(requestForm['url'], json = subscriptionForm).content
    
    #extract the hash of the cetificate from transaction
    decodedTransaction =  settings.multichainnode.decoderawtransaction(requestResponse['transaction'])
    hashedCertificate = transactionaaa =decodedTransaction['vout'][1]['data'][0]

    #validate certificate
    plainCertificate = requestResponse['cert']
    sha256 = hashlib.sha256()
    sha256.update(plainCertificate)
    myHashedCertificate = sha256.hexdigest()

    if myHashedCertificate == hashedCertificate:
        print 'The certificate is valid'
    else: 
        print 'The hashes does not match'   


@request.route(settings.version + '/offchain/request', methods=['POST'])
def publishCertificate():
    publishForm = request.get_json()
    
    #signed transaction
    signedTransaction = settings.multichainNode.signrawtransaction(publishForm['transaction'])['hex']
    
    publishResponse = requests.get(publishForm['url'], json = publishForm).content

    return publishResponse
