from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess
import requests
import json

subscription = Blueprint('subscription', __name__)

@subscription.route(settings.version + '/offchain/subscription' , methods = ['POST'])
def createSubscripton():
    subscriptionForm = request.get_json()
    subscriptionForm['address'] = settings.myAddress
    subscriptionForm['pubKey'] = settings.myPubKey
    subscriptionResponse = requests.post(subscriptionForm['url'], json = subscriptionForm).content
    
    if subscriptionResponse:
        if subscriptionForm['code'] != 1:
            multisigAddress = settings.multichainNode.addmultisigaddress(2,[actorPubKey,settings.myPubKey])
            settings.multichainNode.importaddress(multisigAddress,'false')
        return 'You were accepted'
    else:
        return 'Subscription Failed' 



