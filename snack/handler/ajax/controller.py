
from snack import api
from snack import utils
from snack.handler.base import require_login

class AjaxHandleController(object):
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session = self.request_handler.session
        
        if self.request_handler.is_logged_in:
            self.client = self.session['user']['client']
        else:
            self.client = None

class InstanceController(AjaxHandleController):
    
    def get_performance(self, *args, **kargs):
        """ This method is test for wlee, don't mention about this."""
        instance_id = int(kargs.get("instance_id", [None])[0])
        return api.wlee.get_instance_performance(instance_id)
    
    @require_login
    def list(self):
        return self.client.get_instance_list()
    
class ImageController(AjaxHandleController):
    
    @require_login
    def list(self):
        return self.client.get_image_list()
