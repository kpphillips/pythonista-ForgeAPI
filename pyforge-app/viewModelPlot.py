import model
from datetime import datetime
import viewbarplot as vbp
import viewpieplot as vpp
import time
import viewTreePlot as vtp
import viewGraphPlot as vgp
import re
from anytree import Node, find_by_attr
	
#model['versions'][1].attr['createTime']
		
def presentPlotData(dataDict,state):
	if state == 'Versions':
		#print(state)
		plotVersionData(dataDict)
	if state == 'MetaGuidObject':
		plotObjectData(dataDict)
	if state == 'MetaProperties':
		print(state)
	pass

panels={}
#topNode = Node('Top')

def getFirstFloatValue(str):
	res = re.findall(r"[-+]?\d*\.\d+|\d+", str)
	try:
		float(res[0])
		return float(res[0])
	except ValueError:
		return False
		
def getFloatValueFromElecData(s):
	#string '120 V/1-180 VA'
	res = re.search('-(.+?) VA', s)
	if res:
		load = res.group(1)
		try:
			float(load)
			return float(load)
		except ValueError:
			return False
	
def readPropertyValues(po,cat,m):
	ps=po.properties	
	if cat.startswith('Electrical Equipment'):
		print('Get elec Equipment')
		name=ps['General']['Panel Name']
		parent=ps['Electrical - Circuiting']['Supply From']
		panels[name]={}
		panels[name]['parent']=parent
		panels[name]['children']={}
		print('create node')		
		print(len(parent))
		#if len(parent) != 0:
		print('added to graph')
	elif cat.startswith('Lighting Fixtures'):
		name=po.name
		panel=ps['Electrical - Loads']['Panel']
		circuitS=ps['Electrical - Loads']['Circuit Number']
		circuit=circuitS.replace(",", "_")
		#load=ps['Electrical - Loads']['Apparent Load']
		s=ps['Electrical - Circuiting']['Electrical Data']
		load=getFloatValueFromElecData(s)
		#get number 		
		if panel in panels:					
			circuits=panels[panel]['children']
			if circuit in circuits:
				#res=getFirstFloatValue(load)
				circuits[circuit][cat]+=load
			else:
				circuits[circuit]={}
				#res=getFirstFloatValue(load)
				circuits[circuit][cat]=load
	elif cat.startswith('Electrical Fixtures'):
		name=po.name
		panel=ps['Electrical - Loads']['Panel']
		circuitS=ps['Electrical - Loads']['Circuit Number']
		circuit=circuitS.replace(",", "_")
		#load=ps['Electrical']['Load']
		s=ps['Electrical - Circuiting']['Electrical Data']
		load=getFloatValueFromElecData(s)
		#get number 		
		if panel in panels:					
			circuits=panels[panel]['children']
			if circuit in circuits:
				#res=getFirstFloatValue(load)
				circuits[circuit][cat]+=load
			else:
				circuits[circuit]={}
				#res=getFirstFloatValue(load)
				circuits[circuit][cat]=load
		
def itterateObjects(objects,mps,cat,m):
	if isinstance(objects,list):
		for o in objects:
			if 'objects' in o:
				itterateObjects(o['objects'], mps, cat, m)
			else:			
				id=o['objectid']
				#print(f'Get Properties for {id}')
				mpsd=m['metapropertiesdict']
				#create object 
				objectid=o['objectid']										
				if objectid in mpsd:
					po=mpsd[objectid]
					readPropertyValues(po,cat,m)			
	else:
		print('no objects, last node get proberties')
	#print('exiting recursive func')

def organizeParentPanels(panels,m):
	print('todo: organizing parent panels')
	root=Node('root')
	print('created root node')
	for key in panels:				
		n=Node(key)	
		print(n)
		parent=panels[key]['parent']
		print(f'node:{key}, parent:={parent}')
		print(f'{type(parent)}, {parent}')
		if not parent:
			print('not parent check')
			n.parent=root
		else:
			pn=find_by_attr(root, parent)
			n.parent=pn	
	m['nodes']=root
	pass

def presentGraphData(list, objectState, mps,m):
	print('Presenting graph data')
	if objectState == 'Model Objects':
		for o in list:			
			cat=o.name
			if cat.startswith('Electrical Equipment'):
				print('Itterate Electrical Equipment')
				itterateObjects(o.objects,mps,cat,m)
				print('Done Itterating Panels')
				print(panels)
			elif cat.startswith('Lighting Fixtures'):
				print('Itterate Lighting Fixtures')
				itterateObjects(o.objects,mps,cat,m)
				print(f'Panel Count {len(panels)}')
				m['electricalgraph']=panels
			elif cat.startswith('Electrical Fixtures'):
				print('Itterate Electrical Fixtures')
				itterateObjects(o.objects,mps,cat,m)
				print(f'Panel Count {len(panels)}')
				m['electricalgraph']=panels
			else:	
				print(f'Skip {cat}')
			#TODO: organize parent and subpanels
		parentPanels = organizeParentPanels(panels,m)
		print('panels organized')
		n=m['nodes']
		vgp.createAndWriteGraph(n)

def convert(s):
	dt=datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f0Z')
	return dt

def plotVersionData(dataDict):
	objects=[]
	data=[]
	filename='displayName'
	for i in dataDict:
		if isinstance(i, model.Version):
			filename=i.attr['displayName']
			vn=i.attr['versionNumber']
			#tjis is in bytes 1,000,000 b = 1mb
			t=i.attr['createTime']
			dt=convert(t)
			md=f'{dt.month}/{dt.day}'
			mbdiv=1024*1024
			st=1
			if 'storageSize' in i.attr.keys():
				st=i.attr['storageSize']/mbdiv
			else:
				st=0				
			print(f'v{vn}, {md}, {st}Mb,')
			objects.append(f'v{vn}, {md}')
			data.append(st)
		if isinstance(i, model.Metadata):
			print(i.name)	
	objectsr=list(reversed(objects))
	datar=list(reversed(data))
	vbp.plotBar(objectsr, datar, filename)
		
def plotObjectData(list):
	labels=[]
	sizes=[]
	for i in list:
		if isinstance(i, model.MetaGuidObject):
			objectId = i.objectId
			name = i.name
			objectCount = len(i.objects)
			labels.append(name)
			sizes.append(objectCount)
			print(f'{objectId}, {name}, {objectCount}')
	vpp.piePlot(labels,sizes)
	
	
	
