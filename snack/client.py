
from snack import utils
from snack import api
from snack import settings
from snack import exception

def get_public_urls(catalogs):
    """
    Assume we just have only one region here and all server in a single server.
    Cause NAT reason, we replace local address for debug.
    It's just debug environment.
    """
    public_urls = dict((catalog['name'], catalog['endpoints'][0]['publicURL']) \
                       for catalog in catalogs)
    for k in public_urls.iterkeys():
        public_urls[k] = public_urls[k].replace('127.0.0.1', settings.KEYSTONE_API_CONF['host'])
        public_urls[k] = public_urls[k].replace('localhost', settings.KEYSTONE_API_CONF['host'])
        
    return public_urls

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
        self.tenants = None
        self.current_tenant = None
        self.service_catalog = None
        self.current_public_urls = None
    
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
        client.current_public_urls = get_public_urls(service_catalog)
        
        return client
    
    def get_image_list(self):
        image_list = api.glance.get_image_list(self)
        return image_list
    