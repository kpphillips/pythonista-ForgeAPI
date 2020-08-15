'''
Calls to api endpoints formatted lists of data to display in a UI

Currently this script uses the viewmodel script to extract only relevant info to display to a list UI, in this case a tableview for iOS 
'''

import forge_endpoints as c
import requests
import json
import model
import time
import viewmodel
import threading
import datetime
import forgeui

_model={}

_model['state']='NoneData'
_model['nonedata']=viewmodel.presentNoneData()
_model['response']=[]
start = datetime.datetime.now()
#print(f'Start time: {start}')
view=forgeui.showViewWithData(_model)

class UIthread(threading.Thread):
	def __init__(self, url, callback, state):
		threading.Thread.__init__(self)
		self.url = url
		self.callback = callback
		self.state = state
		self.start()
	
	def run(self):
		headers = c.GETheaders
		r = requests.request("GET", self.url,
		headers=headers)		
		now=datetime.datetime.now()-start
		#print(f'State: {self.state}, {now}')
		#print(f'Status Code: {r.status_code}\n')
		#print(f'Size of {self.state}: {len(r.content)} bytes\n')
			
		#if async sucsess
		if (r.status_code == 202):
			timenow=datetime.datetime.now()-start
			rc=str(r.status_code)
			rt=f'{r.text}: {timenow}'
			list=viewmodel.presentResponse(rc, rt)
			_model['metaproperties']=list
			_model['metaguidobjects']=list
			#_model['metaguidobjects']=list
			#print(list)
			updateUi(_model)
			
			time.sleep(5)
			msg=f'01_Status code 202_{timenow}'
			#print(msg)
			
			js=commonGetRequest(self.url, self.state)			
			
			if js:
				return js
						
		elif (r.status_code == requests.codes.ok):			
			dict = json.loads(r.content)
			model.api_response_data['response']=dict
			_model['response']=dict
			
			#if dict['data']['type']=='objects':
			#	_model['responseObjs']=dict
			
			#print(f'State {self.state} Callback')
			return self.callback(self.state, dict)		
		
		elif (r.status_code == requests.codes.request_entity_too_large):
			if self.state == 'MetaProperties':
				rc=str(r.status_code)
				rt=r.text
				list=viewmodel.presentResponse(rc, rt)
				_model['metaproperties']=list
				_model['metaguidobjects']=list
				updateUi(_model)
				return
						
		else:
			rc=str(r.status_code)
			rt=r.text
			list=viewmodel.presentResponse(rc, rt)
			_model['state']='Response'
			_model['response'] = list
			return self.callback(_model['state'], {rc,rt})

def callback(*args, **kwargs):
	st=_model['state']
	model.updateModel2(args[0], args[1],_model)
	updateUi(_model)
	if _model['state'] != 'MetaProperties':
		print('TODO: remove if: state != MetaProperties')
		
def updateUi(model):
	forgeui.updateView(model, view)

def commonGetRequest(endpoint, state):
	start = datetime.datetime.now()
	r=UIthread(endpoint, callback, state)

#OAUTH				
def getUser():
	commonGetRequest(c.userEndpoint, 'User')
	#TODO: need to wait on a response here
	pass

#Data Managment API
def getHubs():
	url=(c.hubEndpoint)
	commonGetRequest(url, 'Hubs')
	pass

def getProjects(hub_id):
	url=c.projectsEndpoint(hub_id)
	js=commonGetRequest(url, 'Projects')
	pass

def getTopFolders(hub_id, project_id):
	url=c.topFoldersEndpoint(hub_id, project_id)
	commonGetRequest(url, 'Topfolders')
	pass
	
def getFolderContents(project_id, folder_id):
	url=c.contentsEndpoint(project_id,folder_id)
	commonGetRequest(url, 'Folder')

def getItemVersions(project_id, item_id):
	url=c.versionsEndpoint(project_id,item_id)
	commonGetRequest(url, 'Versions')
	pass
	
#Model DerivitiveAPI
def getMetadata(urn):
	url=c.metadataEndpoint(urn)
	commonGetRequest(url, 'Metadata')
	pass
	
def getMetaGuidObjects(urn, guid):
	url=c.metaGuidObjectsEndpoint(urn, guid)
	commonGetRequest(url, 'MetaGuidObjects')
	pass

def getMetaProperties(urn, guid):
	url=c.metaPropertiesEndpoint(urn, guid)
	commonGetRequest(url, 'MetaProperties')
	pass

user=getUser()
hubs=getHubs()
_model['user']=user
_model['hubs']=hubs
#_model={'user' : user, 'hubs' : hubs, 'state':'Hubs'}



