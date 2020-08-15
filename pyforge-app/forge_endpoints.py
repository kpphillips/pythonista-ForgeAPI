'''
Common constants and url endpoints for the forge api used in this app
'''

import client_keys as ck
import forgeauth_response_keys as rk

baseUrl='https://developer.api.autodesk.com'
GETheaders = {'Authorization': 'Bearer ' + rk.access_token }

#OAuth2
client_id=ck.client_id
client_secret=ck.client_secret
endpointuri='https://developer.api.autodesk.com/authentication/v1/authorize'
endpointtoken='https://developer.api.autodesk.com/authentication/v1/gettoken'
granttype='response_type=code'
scope='data:read data:create'
redirect_uri='https://www.kpphillips.com'

#User
userEndpoint=f'{baseUrl}/userprofile/v1/users/@me'

#Data Managment API
hubEndpoint=f'{baseUrl}/project/v1/hubs'

def projectsEndpoint(hub_id):
	projectsEndpoint=f'{baseUrl}/project/v1/hubs/{hub_id}/projects'
	return projectsEndpoint	

def topFoldersEndpoint(hub_id, project_id):
	topFolderEndpoint=f'{baseUrl}/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders'
	return topFolderEndpoint

def contentsEndpoint(project_id, folder_id):	
	contentsEndpoint=f'{baseUrl}/data/v1/projects/{project_id}/folders/{folder_id}/contents'
	return contentsEndpoint
	
def versionsEndpoint(project_id, item_id):
	versionsEndpoint=f'{baseUrl}/data/v1/projects/{project_id}/items/{item_id}/versions'
	return versionsEndpoint

#Model Derivitive API
#GET	https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata
def metadataEndpoint(urn):
	metaEndpoint=f'{baseUrl}/modelderivative/v2/designdata/{urn}/metadata'
	return metaEndpoint

#GET	https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata/:guid
def metaGuidObjectsEndpoint(urn, guid):
	metaGuidObjectsEndpoint=f'{baseUrl}/modelderivative/v2/designdata/{urn}/metadata/{guid}'
	return metaGuidObjectsEndpoint

#GET	https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata/:guid/properties
def metaPropertiesEndpoint(urn, guid):
	metaPropEndPoint=f'{baseUrl}/modelderivative/v2/designdata/{urn}/metadata/{guid}/properties'
	return metaPropEndPoint
	
#Beta
#GET	https://developer.api.autodesk.com/issues/v1/containers/:container_id/markups
#https://forge.autodesk.com/en/docs/issues/v1/reference/http/markups-GET/

