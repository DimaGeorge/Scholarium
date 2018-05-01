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
    settings.initMultichainNode()
    subscriptionForm = request.get_json()
    
    #create the permision list based on actor's role
    print subscriptionForm
    print "-----------------------------------"
    key = subscriptionForm['pass']
    if key not in settings.actors.keys():
        return ''

    permissionsList = validateActorData(settings.actors[key]['rank'])
  
    #grant actor permissions 
    if permissionsList: 
        rsp = {'pubkey' : settings.myPubKey}

        #creating multisig
        multisigAddress = settings.multichainNode.addmultisigaddress(2,[settings.myPubKey,subscriptionForm['pubKey']])
        settings.multichainNode.importaddress(multisigAddress,'false')
        settings.multichainNode.grantfrom(settings.myAddress,multisigAddress,'send,receive')
        
        #granting permissions
        if settings.actors[key]['rank'] == 2:
            titleName = createLicence(subscriptionForm['name'])
            settings.multichainNode.grantfrom(settings.myAddress,subscriptionForm['address'], titleName + '.issue')
            rsp['diploma'] = titleName            
        settings.multichainNode.grantfrom(settings.myAddress,subscriptionForm['address'],permissionsList)
        
        #saving actor
        settings.actors[key]['multisig'] = multisigAddress
        settings.actors[key]['identity'] = subscriptionForm['name']
        settings.saveActors()

        print subscriptionForm['name'] + ' was accepted'
        print rsp
        return Response(json.dumps(rsp))
    else:
        return ''


def validateActorData(rank):
    if rank == 1: # for high autorities
        return 'send,receive,mine,create,admin,activate,issue'
    elif rank == 2: # for certifying entity
        return 'send,receive,activate'
    elif rank == 3: # for claimer
        return 'send,receive' 
    else:
        return''    

            
def createLicence(certifyingEntityName):
    #create the unique asset for Certifying Entities
    licence = certifyingEntityName + 'cert'
    settings.multichainNode.issue(settings.myAddress, {'name':licence, 'open':True}, 0)
    return licence




