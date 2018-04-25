from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess
import requests
import json

subscription = Blueprint('subscription', __name__)

@subscription.route(settings.version + '/offchain/subscription' , methods = ['POST'])
def createSubscripton():
    subscriotionForm = request.get_json()

    if sendSubscription(subscriotionForm) == 'Your subscription failed':
       return 'Subscription faild'
    else:
       multisigAddress = createMultisignatureAddress(sendSubscription(subscriotionForm))
       if multisigAddress:
           return 'You were accepted'
       else:
           return 'Subscription Failed' 

def createMultisignatureAddress(actorPubKey):
    return multichainNode.addmultisigaddress(2,[actorPubKey,setting.myPubKey])

def sendSubscription(subscriotionForm):
    subscriotionForm['address'] = settings.myAddress
    subscriotionForm['pubKey'] = settings.myPubKey
    
    output = requests.post(subscriptionForm['url'], json = subscriotionForm).content
    return Response(output)

