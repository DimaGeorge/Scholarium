import settings
from flask import Blueprint, request, jsonify
from werkzeug.wrappers import Response
import sys
import hashlib
import json
import requests



verification = Blueprint('verification',__name__)

@verification.route(settings.version + '/verification' , methods = ['OPTIONS'])
def uselessFunction():
    rsp = Response("")
    rsp.headers['Access-Control-Allow-Origin']='*'
    rsp.headers['Access-Control-Max-Age'] = 3628800
    rsp.headers['Access-Control-Allow-Methods'] = 'POST, PUT'
    rsp.headers['Access-Control-Allow-Headers'] = 'content-type' 
    return rsp

@verification.route(settings.version + '/verification', methods=['POST'])
def verifyCertificate():
    verificationForm = request.get_json()

    transaction = verificationForm['txid']
    transactionOutput = settings.multichainNode.gettxout(transaction,0)

    plainCertificate = verificationForm['cert']
    sha256 = hashlib.sha256()
    sha256.update(plainCertificate)
    myHashedCertificate = 'dada'


    if transactionOutput:
        hashedCertificate = settings.multichainNode.gettxoutdata(transaction,1)
        if hashedCertificate == myHashedCertificate:
            transactionData = settings.multichainNode.getrawtransaction(transaction,1)
            
            transactionDetails = {}
            transactionDetails['Message'] = 'The certificate is valid'
            transactionDetails['Owner'] = transactionData['vout'][0]['scriptPubKey']['addresses']
            transactionDetails['Sender'] = transactionData['vout'][2]['scriptPubKey']['addresses'] 
            transactionDetails['HashedCertificate'] = hashedCertificate
            return settings.corsResponse(json.dumps(transactionDetails))
        else:
            return settings.corsResponse('The certiifcates do not match')    
    else:    
        return settings.corsResponse('The certificate was revoked')

 
