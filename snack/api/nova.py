
from snack.api.http import HTTPClient

def get_instance_list(client):
    nova_url = client.current_public_urls['nova']
    nova_list_url = "%s/servers/detail" % nova_url
    
    headers = {"X-Auth-Token" : client.token['id']}
    return HTTPClient().request(nova_list_url, method="GET", 
                                headers=headers)[1]['servers']

def get_flavor_list(client):
    nova_url = client.current_public_urls['nova']
    flavor_list_url = "%s/flavors/detail" % nova_url
    
    headers = {"X-Auth-Token" : client.token['id']}
    return HTTPClient().request(flavor_list_url, method="GET", 
                                headers=headers)[1]['flavors']
                                
def create_instance(client, name, image_ref, flavor_ref):
    nova_url = client.current_public_urls['nova']
    create_instance_url = "%s/servers" % nova_url
    body = {"server" : {"name" : name, 
                        "imageRef" : image_ref,
                        "flavorRef" : flavor_ref}}
    
    headers = {"X-Auth-Token" : client.token['id']}
    return HTTPClient().request(create_instance_url, method="POST", 
                                body = body, headers=headers)[1]
    
def delete_instance(client, instance_id):
    nova_url = client.current_public_urls['nova']
    delete_instance_url = "%s/servers/%s" % (nova_url, instance_id)
    
    headers = {"X-Auth-Token" : client.token['id']}
    return HTTPClient().request(delete_instance_url, method="DELETE", 
                                headers=headers)[1]