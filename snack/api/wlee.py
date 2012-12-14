from snack import settings
from snack.api.http import HTTPClient

conf = settings.WLEE_API_CONF
WLEE_URL = "%s://%s:%d/%s" % (conf['protocol'], conf['host'], 
                              conf['port'], conf['version'])

def get_instance_performance(instance_id):
    url = "%s/instance/%d/performance" % (WLEE_URL, instance_id)
    return HTTPClient().request(url, method="GET")[1]