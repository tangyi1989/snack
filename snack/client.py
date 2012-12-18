
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
        #TODO : haven't process zero tenant here
        client.tenants = tenants
        if len(tenants) > 0:    
            client.switch_to_tenant(tenants[0]['name'])
        
        return client
    
    def switch_to_tenant(self, tenant_name):
        for tenant in self.tenants:
            if tenant['name'] == tenant_name:
                self.current_tenant = tenant
                break
            
        if tenant_name != self.current_tenant['name']:
            raise exception.WleeException(_("You have not the special tenant."))
        
        #Get service_catalog
        self.service_catalog = api.keystone.get_service_catalog(self)
        self.current_public_urls = get_public_urls(self.service_catalog)
    
    def get_image_list(self):
        image_list = api.glance.get_image_list(self)
        return image_list
    
    def get_instance_list(self):
        instance_list = api.nova.get_instance_list(self)
        return instance_list
    
    def get_flavor_list(self):
        instance_list = api.nova.get_flavor_list(self)
        return instance_list
    
    def create_instance(self, name, image_id, flavor_id):
        result = api.nova.create_instance(self, name, image_id, flavor_id)
        return result
    
    def delete_instance(self, instance_id):
        result = api.nova.delete_instance(self, instance_id)
        return result