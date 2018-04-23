from flask import Flask
import json
import requests
from Savoir import Savoir
from function import function
from flask_cors import CORS
from flask import Flask, render_template, request, url_for, jsonify
from flask import Blueprint, request


acceptActor = Blueprint('acceptActor', __name__)


rpcuser = 'gg'
rpcpasswd = 'gg'
rpchost = 'localhost'
rpcport = '7416'
chainName = 'chainf'

multichainNode = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainName)

def validateData(actorData):
    #in functie de datele pe care o sa le contina formularul de subscribe o sa verificam datele
    return True

def giveActorPermissions(actorAddress, nodeAddres, multisigAddress):
    #ceva nu cred ca merge bine :))
    actorPermissions = multichainNode.grantfrom(nodeAddres,actorAddress,'send,receive')
    multisigPermissions = multichainNode.grantfrom(nodeAddres,multisigAddress,'send,receive')
    
    if actorPermissions and multisigPermissions:
        return True
    else:    
        return False    

def getNodeAddress():
    addressesList = multichainNode.listaddresses()

    for item in addressesList:
        if item['ismine'] == True:
            return item['address']
            

def getNodePublicKey():
    if getNodeAddress():
        return multichainNode.validateaddress(getNodeAddress())['pubkey']
    else: 
        return 'Something is wrong!'


def createMultisignatureAddress(claimerPubKey):
    if getNodePublicKey():
        multisigAddress = multichainNode.addmultisigaddress(2,[getNodePublicKey(),claimerPubKey])
        return multisigAddress


@acceptActor.route(setings.entityName +'/acceptActor', methods = ['POST'])
def addClaimer():
    subscriptionForm = request.get_json(force=True)

    if validateData(subscriptionForm):
        multisigAddress = createMultisignatureAddress(subscriptionForm['pubkey'])
        nodeAddress = getNodeAddress()

        if giveActorPermissions(subscriptionForm['address'],nodeAddress,multisigAddress):
           print subscriptionForm['name'] + 'was accepted'
           return jsonify(getNodePublicKey())
        else:
            return 'Your subscription faild because ....'
    else:
        return 'Your subscription failed because your data is wrong'           