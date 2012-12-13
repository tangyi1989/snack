
from snack import api
from snack import utils
from snack import exception
from snack.handler import base

from snack.handler.ajax.controller import InstanceController, ImageController

class AjaxHandler(base.BaseHandler):
    """
    FIXME: There's a lot of things need process here.
    """
    def initialize(self):
        self.controller_mapper = {"instance" : InstanceController,
                                  "image" : ImageController}
    
    def _handle_request_exception(self, e):
        self.set_status(500)
        response_body = {"reason" : str(e)}
        self.finish_result(response_body)
    
    def finish_result(self, data):
        self.set_header("Content-Type", "application/json")
        body = utils.json_dumps(data)
        self.finish(body)
    
    def get(self, *args, **kargs):
        self.handle_ajax_request(*args, **kargs)
    
    def post(self, *args, **kargs):
        self.handle_ajax_request(*args, **kargs)
    
    @utils.debug
    def handle_ajax_request(self, path, **karg):
        url_param_list = path.split('/')
        
        if len(url_param_list) != 2:
            raise exception.AjaxRequestError(reason = "Invalid request .")
        
        controller_name, method_name = url_param_list
        controller = self.controller_mapper.get(controller_name)
        if controller == None:
            raise exception.AjaxRequestError(reason = "Invalid controller parameter.")
        
        controller_instance = controller(self)
        
        try:
            #FIXME : It's not safe here, should check if method is exposed.
            #Some function should not exposed. NOTE: THIS MUST BE FIXED LATER.
            method = getattr(controller_instance, method_name)
        except:
            raise exception.AjaxRequestError(reason = "Invaid method parameter.")
        
        params = self.request.arguments
        result = method(**params)
        
        self.finish_result(result)
