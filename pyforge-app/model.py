'''
Objects that are created and used in the app

helper function that keeps track of the state of the data to display

this model is updated as the user navigates the UI and past lists of data are saved into a dictionary for access at any time. 
'''
import forgeapi
import base64
import pprint
import json
import urllib
import webbrowser
import viewmodel

api_response_data={}

def viewJayson():
	parsed_dict = api_response_data['response']
	print(type(parsed_dict))
	parsed_json = json.dumps(parsed_dict)
	urlencoded=urllib.parse.quote(parsed_json)
	print('showing Jayson bro')
	model=forgeapi._model
	print("—————————")
	print(model['state'])
	#print(model['objectstate'])
	print("—————————")
	webbrowser.open_new(f'jayson:///view?text={urlencoded}')

#User Class
class User(object):	
	def __init__(self, name, email, imgUrl):
		self.name = name
		self.email = email
		self.imgUrl = imgUrl
				
def make_user(name, email, imgUrl):
	user = User(name, email, imgUrl)
	return user
	
#Hub Class
class Hub(object):
	def __init__(self, name, id, monitor="checked"):
		self.name = name
		self.id = id
		self.monitor = monitor
		
def make_hub(name, id):
	hub = Hub(name, id)
	return hub
		
#Project Class
class Project(object): 
	def __init__(self, name, id):
		self.name = name
		self.id = id
		
def make_project(name, id):
	project = Project(name, id)
	return project
	
#Item Class
class Item(object):
	def __init__(self, name, type, id, version):
		self.name = name + f'{version}'
		self.type = type
		self.id = id
		
def make_item(name, type, id, version):
	type = Item(name, type, id, version)
	return type

#Version Class
class Version(object):
	def __init__(self, type, id, name, attr, attrExt):
		self.type = type
		self.id = id
		self.name = name
		self.attr = attr
		self.attrExt = attrExt
				
def make_version(type, id, name, attr, attrExt):
	vs = Version(type, id, name, attr, attrExt)
	return vs

#Version Datum Class
class VersionDatum(object):
	def __init__(self, name):
		self.name = name
				
def make_versionDatum(name):
	vs = VersionDatum(name)
	return vs

#Metadata Class
class Metadata(object):
	def __init__(self, name, role, guid, urn):
		self.name = name
		self.role = role
		self.guid = guid
		self.urn = urn
		
def make_metadata(name, role, guid, urn):
	md = Metadata(name, role, guid, urn)
	return md

#MetadataProperties Class
#objects can be optional or None
class MetaGuidObject(object):
	def __init__(self, objectId, name, objects):
		self.objectId = objectId
		self.name = name
		self.objects = objects
		
def make_metaguidobject(objectId, name, objects):
	mgo = MetaGuidObject(objectId, name, objects)
	return mgo

#MetadataProperties Class
class MetaProperty(object):
	def __init__(self, objectId, name, externalId, properties):
		self.objectId = objectId
		self.name = name
		self.externalId = externalId
		self.properties = properties
		
def make_metaproperty(objectId, name, externalId, properties):
	mp = MetaProperty(objectId, name, externalId, properties)
	return mp

#Category or Property
class CategoryProperty (object):
	def __init__(self, name):
		self.name = name
			
def make_categorypropert(name):
	mcp = CategoryProperty(name)
	return mcp

#None Type Class to show when no data returned
class NoneDatum(object):
	def __init__(self, name):
		self.name = name
				
def make_noneDatum(name):
	nd = NoneDatum(name)
	return nd	
	
#respomse Type Class to show when no data returned
class Response(object):
	def __init__(self, name):
		self.name = name
				
def make_response(name):
	rd = Response(name)
	return rd
			
def updateModel2(toUpdate, js, model):
	model['state']=toUpdate
	if toUpdate == 'User':
		user = viewmodel.presentUser(js)
		model['user']=user
		return model
	if toUpdate == 'Hubs':
		hubs = viewmodel.presentHubs(js)
		model['hubs']=hubs
		return model
	if toUpdate == 'Projects':
		projects = viewmodel.presentProjects(js)
		model['projects']=projects
		return model
	if toUpdate == 'Topfolders':
		topfolders = viewmodel.presentTopFolders(js)
		model['topfolders']=topfolders
		return model
	if toUpdate == 'Folder':
		items = viewmodel.presentFolderContents(js)
		model['items']=items
		return model
	if toUpdate == 'Versions':
		versions = viewmodel.presentItemVersions(js)
		model['versions']=versions
		return model
	if toUpdate == 'Metadata':
		urn=model['metadataurn']
		metadata = viewmodel.presentMetadata(js,urn)
		model['metadata']=metadata
		return model
	if toUpdate == 'MetaGuidObjects':
		model['objectstate']='Model Objects'
		mos=model['objectstate']
		mgos = viewmodel.presentMetaGuidObjects(js,mos)
		print('update metaguidobjects')
		model['metaguidobjects']=mgos		
		#TODO: if 202 response update ui 
		return model
	if toUpdate == 'MetaProperties':
		mps,mpsd = viewmodel.presentMetaProperties(js)
		model['metaproperties']=mps
		model['metapropertiesdict']=mpsd
		print('update metaproperties')
		#TODO: if 202 response update ui 
		#model['metaguidobjects']=mps
		return model
	pass

def dataFromState(model):
	state=model['state']
	if state == 'Hubs':
		return model['hubs']
	if state == 'Projects':
		return model['projects']
	if state == 'Contents':
		return model['contents']
	if state == 'Topfolders':
		return model['topfolders']
	if state == 'Folder':
		return model['items']
	if state == 'Item':
		return model['item']
	if state == 'Versions':
		return model['versions']
	if state == 'Version':
		return model['version']
	if state == 'Metadata':
		return model['metadata']
	if state == 'MetaGuidObjects':
		return model['metaguidobjects']
	if state == 'MetaGuidObject':
		return model['objects']
	if state == 'MetaProperties':
		return model['metaproperties']
	if state == 'MetaProperty':
		return model['properties']
	if state == 'NoneData':
		return model['nonedata']
	if state == 'Response':
		return model['response']
	return None
	
def selected(model,selected):
	data=dataFromState(model)	
	itemSelected=data[selected]
	model['itemSelected']=itemSelected.name
	#check for what was selected
	if isinstance(itemSelected, Hub):
		model['hub']=itemSelected		
		forgeapi.getProjects(itemSelected.id)
		pass
	if isinstance(itemSelected, Project):
		model['project']=itemSelected
		hubid=model['hub'].id
		projectid=itemSelected.id
		forgeapi.getTopFolders(hubid,projectid)
		pass
	if isinstance(itemSelected, Item):
		if itemSelected.type == 'folders':
			projid=model['project'].id
			folderid=itemSelected.id
			forgeapi.getFolderContents(projid,folderid)
			pass
		if itemSelected.type == 'items':
			model['item']=itemSelected
			projid=model['project'].id
			itemid=itemSelected.id
			forgeapi.getItemVersions(projid,itemid)
			pass
	if isinstance(itemSelected, Version):
		model['version']=itemSelected
		model['state']='Metadata'
		id=itemSelected.id
		data64=id.encode("utf-8")
		base64Urn=base64.urlsafe_b64encode(data64)
		base64UrnSt=base64Urn.decode("utf-8")
		model['metadataurn']=base64UrnSt
		forgeapi.getMetadata(base64UrnSt)
		pass
	if isinstance(itemSelected, Metadata):
		model['metadatum']=itemSelected
		model['state']='MetaGuidObjects'
		guid=itemSelected.guid
		urn=itemSelected.urn	
		print('Get Meta Objects')
		forgeapi.getMetaGuidObjects(urn,guid)		
		print('Get Meta Properties')
		forgeapi.getMetaProperties(urn,guid)
		pass
	if isinstance(itemSelected, MetaProperty):
		print('Meta Prop Selected')
		model['metaproperty']=itemSelected
		model['state']='MetaProperty'	
		pdict=itemSelected.properties
		model['properties']=pdict	
		propPresent = viewmodel.presentNestedProperties(pdict)
		model['properties']=propPresent
		forgeapi.updateUi(model)
		pass
	if isinstance(itemSelected, MetaGuidObject):
		print(itemSelected.name)
		mos=model['objectstate']
		ms=model['state']
		print(f'Update Object State {mos}')
		model['metaguidobject']=itemSelected
		model['state']='MetaGuidObject'
		if mos == 'Model Objects':
			if itemSelected.name=='Model':
				mos = 'Categories'	
		elif mos == 'Categories':
			mos = 'Loaded Families'
		elif mos == 'Loaded Families':
			mos = 'Family Types'
		elif mos == 'Family Types':
			mos = 'Instances'
		elif mos == 'Instances':
			mos = 'Properties'
			ms = 'MetaProperties'
			print(itemSelected.objectId)			
		#show properties of element
		if mos == 'Properties':
			model['objectstate'] = mos
			model['state'] = ms
			mp=model['metaproperties']
			for i, p in enumerate(mp):
				if p.objectId == itemSelected.objectId:
					updateModel(model,i)
		else:		
			model['objectstate'] = mos
			objsPresent = viewmodel.presentNestedObjects(itemSelected,mos)
			model['objects']=objsPresent
			forgeapi.updateUi(model)	
			#return model	
	if isinstance(itemSelected, NoneDatum):
		model['nonedata']=itemSelected
		model['state']='NoneData'
		return model
	return None
	
	
	
