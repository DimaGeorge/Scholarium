from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess
import requests
import json

subscription = Blueprint('subscription', __name__)

@subscription.route(settings.version + '/offchain/subscription' , methods = ['OPTIONS'])
def uselessFunction():
    rsp = Response("")
    rsp.headers['Access-Control-Allow-Origin']='*'
    rsp.headers['Access-Control-Max-Age'] = 3628800
    rsp.headers['Access-Control-Allow-Methods'] = 'POST'
    rsp.headers['Access-Control-Allow-Headers'] = 'content-type' 
    return rsp

@subscription.route(settings.version + '/offchain/subscription' , methods = ['POST'])
def createSubscripton():
    settings.initMultichainNode()
    subscriptionForm = request.get_json()

    subscriptionForm['address'] = settings.myAddress
    subscriptionForm['pubKey'] = settings.myPubKey
    url = 'http://' + subscriptionForm['ip'] + '/v1.1/actor'
    subscriptionResponse = requests.post(url, json = subscriptionForm).content
    if 'diploma' in subscriptionResponse.keys():
        settings.diplomaName = subscriptionResponse['diploma']

    multisigAddress = settings.multichainNode.addmultisigaddress(2,[subscriptionResponse['pubkey'],settings.myPubKey])
    settings.multichainNode.importaddress(multisigAddress,'false')
    settings.subscriptionMultisig = multisigAddress
    return settings.corsResponse('You were accepted. Your multisig: ' + multisigAddress)



