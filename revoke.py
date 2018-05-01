import settings
from flask import Blueprint, request
from werkzeug.wrappers import Response
import sys
import hashlib
import json
import requests


revoke = Blueprint('revoke',__name__)

@revoke.route(settings.version + '/certificate/revoke' , methods = ['OPTIONS'])
def uselessFunction():
    rsp = Response("")
    rsp.headers['Access-Control-Allow-Origin']='*'
    rsp.headers['Access-Control-Max-Age'] = 3628800
    rsp.headers['Access-Control-Allow-Methods'] = 'POST, PUT'
    rsp.headers['Access-Control-Allow-Headers'] = 'content-type' 
    return rsp

@revoke.route(settings.version+ '/certificate/revoke', methods=['DELETE'])
def revokeCertificate():
    revocationForm = request.get_json()

    if revocationForm['txid'] != '':  
        revocationTransaction = settings.multichainNode.createrawtransaction(
        [{"txid":revocationForm['txid'],"vout":0}],
        {settings.burnAddress:{settings.diplomaName:1}},
        [],
        'sign'
        )
        print revocationTransaction
        revocationForm['hex'] = revocationTransaction['hex']
        revocationForm['txid'] = ''
        
        revocationResponse = requests.delete(revocationForm['url'],json=revocationForm).content
        
        return settings.corsResponse(json.dumps(revocationResponse))

    if revocationForm['hex']:
        signedRevocationTransaction = settings.multichainNode.signrawtransaction(revocationForm['hex'])

        if signedRevocationTransaction['complete'] == True:
            publish = settings.multichainNode.sendrawtransaction(signedRevocationTransaction['hex'])
            return settings.corsResponse('Certificate succesfuly revoked')
        else:
            return settings.corsResponse('Error')    
    
    return settings.corsResponse('Error')