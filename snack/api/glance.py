
from snack.api.http import HTTPClient

def get_image_list(client):
    glance_url = client.current_public_urls['glance']
    image_list_url = "%s/v2/images" % glance_url
    
    headers = {"X-Auth-Token" : client.token['id']}
    return HTTPClient().request(image_list_url, method="GET", 
                                headers=headers)[1]['images']
    
