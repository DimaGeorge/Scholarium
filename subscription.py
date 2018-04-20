from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess
import requests

subscription = Blueprint('subscription', __name__)

@subscription.route(settings.version + '/offchain/subscription' , methods = ['GET'])
def sendSubscription():
    output = requests.delete('http://192.168.1.10:5000/v1.1/blockchain').content
    return Response(output)