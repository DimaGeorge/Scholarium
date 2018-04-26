from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess
import requests
import json

subscription = Blueprint('subscription', __name__)

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
        return 'You were accepted\n'
    else:
        return 'Subscription Failed\n' 



