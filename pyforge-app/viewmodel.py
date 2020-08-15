'''
Recieves parsed JSON already converted to dictionaries. these functions extract the relevant data that will be displayed to the user in a UI 
'''

import model

def presentNoneData():
	nd=model.make_noneDatum('Aquiring Data...')	
	nd2=model.make_noneDatum('...')
	return [nd,nd2]
	
def presentResponse(code, text):
	nd=model.make_response(code)	
	nd2=model.make_response(text)	
	return [nd,nd2]

def presentUser(js):
	model.api_response_data['user']=js
	first=js['firstName']
	last=js['lastName']
	email=js['emailId']
	imageUrl=js['profileImages']['sizeX240']
	user=model.make_user(f'{first} {last}', email, imageUrl)	
	return user
	
def presentHubs(js):	
	model.api_response_data['hubs']=js
	data=js['data']
	list=[]
	for i in data:
		id=i['id']
		name=i['attributes']['name']
		hub=model.make_hub(name,id)
		list.append(hub)	
	return list

def presentProjects(js):
	model.api_response_data['projects']=js
	data=js['data']
	list=[]
	for i in data:
		id=i['id']
		name=i['attributes']['name']
		project=model.make_project(name,id)
		list.append(project)
	return list

def presentTopFolders(js):
	model.api_response_data['topfolders']=js
	data=js['data']
	list=[]
	for i in data:
		id=i['id']
		name=i['attributes']['displayName']
		type=i['type']
		version=''
		folder=model.make_item(name,type,id,version)
		list.append(folder)
	return list
	
def presentFolderContents(js):
	model.api_response_data['foldercontents']=js
	data=js['data']
	list=[]
	for i in data:
		id=i['id']
		name=i['attributes']['displayName']
		type=i['type']
		version=''
		item=model.make_item(name,type,id,version)
		list.append(item)
	return list

def presentItemVersions(js):
	model.api_response_data['versions']=js
	data=js['data']
	list=[]
	for i in data:
		type=i['type']
		id=i['id']
		attr=i['attributes']
		vsnum=str(attr['versionNumber'])
		name=attr['name'] + '_v' + vsnum
		attrExt=attr['extension']
		vs=model.make_version(type,id,name,attr,attrExt)
		list.append(vs)
	return list
	
#Model DerivitiveAPI
def presentMetadata(js,urn):
	model.api_response_data['metadata']=js
	data=js['data']['metadata']
	list=[]
	for i in data:
		name=i['name']
		role=i['role']
		guid=i['guid']
		md=model.make_metadata(name,role,guid,urn)
		list.append(md)
	return list

def presentMetaGuidObjects(js,mos):
	model.api_response_data['metaguidobjects']=js
	data=js['data']['objects']	
	list=[]
	objType = mos	
	#objType = model['objectstate']
	for i in data:
		objectid=i['objectid']
		name=i['name']
		objects = []
		if 'objects' in i.keys():
			objects = i['objects']
			c=len(objects)
			name += f' ({str(c)} {objType})'
		mp=model.make_metaguidobject(objectid, name, objects)
		list.append(mp)
	return list

def presentNestedObjects(obj,mos):
	print(mos)
	data=obj.objects
	list=[]
	objType = mos
	for i in data:
		objectid=i['objectid']
		name=i['name']
		objects = []
		if 'objects' in i.keys():
			objects = i['objects']
			c=len(objects)
			name += f' ({str(c)} {objType})'
		mp=model.make_metaguidobject(objectid, name, objects)
		list.append(mp)
	return list

def presentMetaProperties(js):
	#TODO: need to get response from DB here
	#count=len(model.api_response_data['response']['data']['collection'])
	
	model.api_response_data['metaproperties']=js
		
	#if none then skip NoneType
	if not js:
		list=[]
		name='Getting Data...'
		md=model.make_noneDatum(name)
		list.append(md)
		return list
	
	data=js['data']['collection']
	
	list=[]
	dict={}
	for i in data:
		objectId=i['objectid']
		name=i['name']
		externalId=i['externalId']
		properties = []
		if 'properties' in i.keys():
			properties = i['properties']
			c=len(properties)
			name += f' ({str(c)} Property Groups)'
		mp=model.make_metaproperty(objectId, name, externalId, properties)
		list.append(mp)
		dict[objectId]=mp
	return list,dict
	
def presentNestedProperties(propDict):
	list=[]
	print(type(propDict))
	for cat in propDict:
		value=propDict[cat]	
		catStr=f'--{cat}--'
		c=model.make_categorypropert(catStr)
		list.append(c)
		for prop in value:
			propValue=value[prop]
			propStr=f'	{prop}: {propValue}'
			p=model.make_categorypropert(propStr)
			list.append(p)
	return list
