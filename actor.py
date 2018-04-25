from flask import Flask
import json
import requests
from Savoir import Savoir
from function import function
from flask_cors import CORS
from flask import Flask, render_template, request, url_for, jsonify
from flask import Blueprint, request
import settings

acceptActor = Blueprint('acceptActor', __name__)

def giveActorPermissions(actorAddress, myAddres, multisigAddress, permissionsList):
    actorPermissions = multichainNode.grantfrom(myAddres,actorAddress,permissionsList)
    multisigPermissions = multichainNode.grantfrom(myAddres,multisigAddress,permissionsList)
    
    if actorPermissions['error code'] or multisigPermissions['error code']:
        return False
    else:    
        return True    
            

def createMultisignatureAddress(claimerPubKey):
    return multichainNode.addmultisigaddress(2,[setting.myPubKey,claimerPubKey])
    

def addActor(subscriptionForm,permissionsList):
    multisigAddress = createMultisignatureAddress(subscriptionForm['pubkey'])

    if giveActorPermissions(subscriptionForm['address'],settings.myAddress,multisigAddress,permissionsList):
        print subscriptionForm['name'] + 'was accepted'
        return jsonify(settings.myPubKey)
    else:
        return 'Your subscription faild'
     
def validateActorData(subscriptionForm):
    if subscriptionForm['code'] == 1: # for high autorities
        return 'admin'
    else:
        if subscriptionForm['code'] == 2: # for certifying entity
            return 'send,receive,activate,issue.' + createLicence(subscriptionForm['name']) 
        else:
            if subscriptionForm['code'] == 3: # for claimer
                return 'send,receive' 
            else:
                return 'failed'    


def createLicence(certifyingEntityName):
    return certifyingEntityName + 'cert'


@deleteActor.route(settings.version + '/deleteActor', methods = ['DELETE'])
def delActor(actorAddress):
    settings.multichainNode.revokefrom(myAddress,actorAddress,'send,receive,mine,create,admin,activate,issue')
    return 'Address' + actorAddress + 'permissions were deleted' 


@acceptActor.route(settings.version +'/acceptActor', methods = ['POST'])
def accActorData():
    subscriptionForm = request.get_json()
    if validateActorData() = 'failed':
        return 'Your subscription failed'
    else:    
        return addActor(subscriptionForm,validateActorData)
