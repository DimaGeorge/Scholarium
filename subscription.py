from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess
import requests
import json

subscription = Blueprint('subscription', __name__)

@subscription.route(settings.version + '/offchain/subscription' , methods = ['POST'])
def createSubscripton(url,subscriotionForm):
    if sendSubscription(url,subscriotionForm) == 'Your subscription failed':
       return 'Subscription faild'
    else:
       multisigAddress = createMultisignatureAddress(sendSubscription(url,subscriotionForm))
       if multisigAddress:
           return 'You were accepted'
       else:
           return 'Subscription Failed' 

def createMultisignatureAddress(actorPubKey):
    return multichainNode.addmultisigaddress(2,[actorPubKey,setting.myPubKey])

def sendSubscription(url,subscriotionForm):
    
    url = 'http://192.168.1.7:5000/v1.1/acceptActor'
    subscriotionForm = {'pubkey': settings.myPubKey, 'address':settings.myAddress, 'name':'ATM'}
    print data
    output = requests.post(url, json=data).content
    return Response(output)

