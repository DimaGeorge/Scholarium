import settings
from flask import Blueprint, request
from werkzeug.wrappers import Response
import sys
import hashlib
import json
import requests


revoke = Blueprint('revoke',__name__)


@revoke.route(settings.version+ '/certificate/revoke', methods=['DELETE'])
def revokeCertificate():
    revocationForm = request.get_json()

    if revocationForm['txid'] != '':  
        revocationTransaction = settings.multichainNode.createrawtransaction(
        [{"txid":revocationForm['txid'],"vout":0}],
        {"1XXXXXXXCuXXXXXXdqXXXXXXV5XXXXXXZFb4eK":{settings.diplomaName:1}},
        [],
        'sign'
        )
        print revocationTransaction
        revocationForm['hex'] = revocationTransaction['hex']
        revocationForm['txid'] = ''
        
        revocationResponse = requests.delete(revocationForm['url'],json=revocationForm).content
        
        return revocationResponse

    if revocationForm['hex']:
        signedRevocationTransaction = settings.multichainNode.signrawtransaction(revocationForm['hex'])

        if signedRevocationTransaction['complete'] == True:
            publish = settings.multichainNode.sendrawtransaction(signedRevocationTransaction['hex'])
            return 'Certificate deleted'
        else:
            return 'Error'    
    
    return 'Error'