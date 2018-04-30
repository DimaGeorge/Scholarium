import settings
from flask import Blueprint, request
from werkzeug.wrappers import Response
import sys
import hashlib
import json
import requests



verification = Blueprint('verification',__name__)


@verification.route(settings.version + '/verification', methods=['GET'])
def verifyCertificate():
    verificationForm = request.get_json()

    transaction = verificationForm['txid']
    transactionOutput = settings.multichainNode.gettxout(transaction,0)

    plainCertificate = verificationForm['cert']
    sha256 = hashlib.sha256()
    sha256.update(plainCertificate)
    myHashedCertificate = sha256.hexdigest()

    if transactionOutput:
        hashedCertificate = settings.multichainNode.gettxoutdata(transaction,1)
        if hashedCertificate == myHashedCertificate:
            return 'The certificate is valid'
        else:
            return 'The certificates do not match'    
    else:    
        return 'The certificate was revoked'


 
