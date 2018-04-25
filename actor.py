from flask import Flask
import json
import requests
from Savoir import Savoir

from flask import Flask, render_template, request, url_for, jsonify
from flask import Blueprint, request
import settings
from werkzeug.wrappers import Request, Response


actor = Blueprint('actor', __name__)

def giveActorPermissions(actorAddress, multisigAddress, permissionsList):
    settings.initMultichainNode()
    actorPermissions = settings.multichainNode.grantfrom(settings.myAddress,actorAddress,permissionsList)
    multisigPermissions = settings.multichainNode.grantfrom(settings.myAddress,multisigAddress,"send,receive")
    return True    
            

def createMultisignatureAddress(claimerPubKey):
    settings.initMultichainNode()
    return  settings.multichainNode.addmultisigaddress(2,[settings.myPubKey,claimerPubKey])

    

def addActor(subscriptionForm,permissionsList):
    multisigAddress = createMultisignatureAddress(subscriptionForm['pubKey'])
    if giveActorPermissions(subscriptionForm['address'],multisigAddress,permissionsList):
        print subscriptionForm['name'] + 'was accepted'
        return jsonify(settings.myPubKey)
    else:
        return 'Your subscription faild'

def createLicence(certifyingEntityName):
    #issue
    return certifyingEntityName + 'cert'


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





@actor.route(settings.version + '/actor', methods = ['DELETE'])
def delActor():
    params = request.get_json()
    actorAddress = params['address']

    settings.multichainNode.revokefrom(settings.myAddress,actorAddress,'send,receive,mine,create,admin,activate,issue')
    return 'Address' + actorAddress + 'permissions were deleted' 


@actor.route(settings.version +'/actor', methods = ['POST'])
def accActorData():
    subscriptionForm = request.get_json()
    print subscriptionForm
    if validateActorData(subscriptionForm) == 'failed':
        return 'Your subscription failed'
    else:    
        a = addActor(subscriptionForm,validateActorData(subscriptionForm))
        print a
        return a

