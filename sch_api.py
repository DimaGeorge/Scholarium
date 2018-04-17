from werkzeug.wrappers import Request, Response
from flask import Blueprint
import requests
import json
from settings import url, headers, chainName


api = Blueprint('api', __name__)

@api.route('/scholarium_api', methods = ['GET'])
def postHighAuthority():
    address = getNodeAddress()
    if isHighAuthority(address):
        return Response("You are the High Authority here!")
    else:
        return Response("You are pp")

def getNodeAddress():
    payload = {
        "method": "listaddresses",
        "params": [],
        "id":1,
        "chain_name": chainName
    }
    response = requests.get(url, data=json.dumps(payload), headers=headers).json()
    address = response['result'][0]['address']
    return address

def isHighAuthority(address):
    payload = {
        "method": "listpermissions",
        "params":["admin", address],
        "id":1,
        "chain_name":chainName}
    
    response = requests.get(url, data=json.dumps(payload), headers=headers).json()
    if not response['result']:
        return False
    else:
        return True