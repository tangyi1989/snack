
from snack.api.http import HTTPClient

def authenticate(keystone_url, username, password, tenant_name=None):
    auth_url = "%s/tokens" % keystone_url
    
    body = {"auth": {"passwordCredentials": 
                        {"username": username,
                        "password": password}}}
    if tenant_name == None:
        tenant_name = ""
        
    body['auth']['tenantName'] = tenant_name
        
    #Ignore head info here
    return HTTPClient().request(auth_url, method="POST", body=body)[1]

def get_service_catalog(client):
    """ Get current tenants' endpoints, It's ugly here """
    access = authenticate(client.keystone_url, client.username, client.password, 
                          client.current_tenant['name'])['access']
    
    #update token
    client.token = access['token']
    
    return access['serviceCatalog']

def get_tenants(client):
    tenants_url = "%s/tenants" % client.keystone_url
    
    headers = {"X-Auth-Token" : client.token['id']}
    return HTTPClient().request(tenants_url, method="GET", 
                                headers=headers)[1]['tenants']
