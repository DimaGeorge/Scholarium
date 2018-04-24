from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess
import requests
import json

subscription = Blueprint('subscription', __name__)

@subscription.route(settings.version + '/offchain/subscription' , methods = ['POST'])
def sendSubscription():
    url = 'http://192.168.1.7:5000/v1.1/acceptActor'
    data = {'pubkey': settings.myPubKey, 'address':settings.myAddress, 'name':'ATM'}
    print data
    output = requests.post(url, json=data).content
    return Response(output)

