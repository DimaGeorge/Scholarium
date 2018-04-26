from flask import Flask
import json
import requests
from Savoir import Savoir

from flask import Flask, render_template, request, url_for, jsonify
from flask import Blueprint, request
import settings
from werkzeug.wrappers import Request, Response


actor = Blueprint('actor', __name__)

@actor.route(settings.version + '/actor', methods = ['DELETE'])
def delActor():
    settings.initMultichainNode()
    parameter = request.get_json()
    actorAddress = parameter['address']
    settings.multichainNode.revokefrom(settings.myAddress,actorAddress,'send,receive,mine,create,admin,activate,issue')
    return 'Address ' + actorAddress + ' permissions were deleted' 


@actor.route(settings.version +'/actor', methods = ['POST'])
def addActor():
    subscriptionForm = request.get_json()
    settings.initMultichainNode()

    #create the permision list based on actor's role
    permissionsList = validateActorData(subscriptionForm)
    
    #grant actor permissions 
    if permissionsList: 
        multisigAddress = settings.multichainNode.addmultisigaddress(2,[settings.myPubKey,subscriptionForm['pubKey']])
        settings.multichainNode.importaddress(multisigAddress,'false')
        settings.multichainNode.grantfrom(settings.myAddress,multisigAddress,'send,receive')
        
        settings.multichainNode.grantfrom(settings.myAddress,subscriptionForm['address'],permissionsList)
        print subscriptionForm['name'] + ' was accepted'
        print settings.myPubKey
        return Response(settings.myPubKey)
    else:
        return ''


def validateActorData(subscriptionForm):
    if subscriptionForm['code'] == 1: # for high autorities
        return 'send,receive,mine,create,admin,activate,issue'
    else:
        if subscriptionForm['code'] == 2: # for certifying entity
            return 'send,receive,activate,issue.' + createLicence(subscriptionForm['name']) 
        else:
            if subscriptionForm['code'] == 3: # for claimer
                return 'send,receive' 
            else:
                return''    

            
def createLicence(certifyingEntityName):
    #create the unique asset for Certifying Entities
    licence = certifyingEntityName + 'cert' 
    settings.multichainNode.issue(settings.myAddress, {'name':licence, 'open':True}, 0)
    return licence




