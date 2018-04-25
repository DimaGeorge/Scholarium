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
    partnerPubKey = sendSubscription(subscriptionForm)
    if partnerPubKey == 'Your subscription failed':
       return 'Subscription faild'
    else:
       multisigAddress = createMultisignatureAddress(partnerPubKey)
       if multisigAddress:
           return 'You were accepted'
       else:
           return 'Subscription Failed' 

def createMultisignatureAddress(actorPubKey):
    return settings.multichainNode.addmultisigaddress(2,[actorPubKey,settings.myPubKey])

def sendSubscription(subscriptionForm):
    subscriptionForm['address'] = settings.myAddress
    subscriptionForm['pubKey'] = settings.myPubKey
    output = requests.post(subscriptionForm['url'], json = subscriptionForm).content
    return output

