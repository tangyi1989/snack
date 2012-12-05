
from snack import api
from snack import settings
from snack import exception

def get_public_urls(catalogs):
    """
    Assume we just have only one region here!
    """
    return dict((catalog['name'], catalog['endpoints'][0]['publicURL']) \
                for catalog in catalogs)
        

class SnackClient():
    """
    A client wrapper to request all openstack API.
    """
    
    def __init__(self, token, keystone_url=None, management_url = None, 
                 username=None, password=None):
        
        self.token = token
        self.username = username
        self.password = password
        self.keystone_url = keystone_url
        self.management_url = management_url
        self.public_urls = None
        self.tenants = None
        self.current_tenant = None
        self.service_catalog = None
    
    @classmethod
    def authenticate(cls, username, password):
        keystone_url = "%(protocol)s://%(host)s:%(port)d/%(version)s" % \
                        settings.KEYSTONE_API_CONF
                        
        management_url = "%(protocol)s://%(host)s:%(admin_port)d/%(version)s" % \
                            settings.KEYSTONE_API_CONF
                        
        access = api.keystone.authenticate(keystone_url, username, password)
        token = access["access"]["token"]
        client = cls(token, keystone_url=keystone_url, 
                     management_url=management_url,
                     username=username, password=password)
        
        tenants = api.keystone.get_tenants(client)
        
        #Get tenants, always use the first tenant as current tenant
        if len(tenants) > 0:
            client.tenants = tenants
            client.current_tenant = tenants[0]
        
        #Get service_catalog
        service_catalog = api.keystone.get_service_catalog(client)
        client.service_catalog = service_catalog
        client.public_urls = get_public_urls(service_catalog)
        
        return client
    