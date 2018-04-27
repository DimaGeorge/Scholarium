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
    
    subscriptionResponse = requests.post(subscriptionForm['url'], json = subscriptionForm).content

    if subscriptionResponse:
        multisigAddress = settings.multichainNode.addmultisigaddress(2,[subscriptionResponse,settings.myPubKey])
        settings.multichainNode.importaddress(multisigAddress,'false')
        return settings.corsResponse('You were accepted. Your multisig: ' + multisigAddress)
    else:
        return settings.corsResponse('Subscription Failed')



