
from snack import utils
from snack import exception
from snack.handler import base
from snack.handler.base import require_login

class List(base.BaseHandler):
    @require_login
    def get(self):
        client = self.session['user']['client']
        instances = client.get_instance_list()
        self.render('instance/list.html' ,instances=instances)
        
class Create(base.BaseHandler):
    @require_login
    def get(self):
        client = self.session['user']['client']
        images = client.get_image_list()
        flavors = client.get_flavor_list()
        
        self.render('instance/create.html', images=images, 
                    flavors=flavors)
        
    @require_login
    def post(self):
        name = self.get_argument("name", None)
        image_id = self.get_argument("image", None)
        flavor_id = self.get_argument("flavor", None)
        
        client = self.session['user']['client']
        result = client.create_instance(name, image_id, flavor_id)
        prompt = _("Creating instance, please wait ..." )
        
        self.prompt_and_redirect(prompt, "/instance/list")

class Action(base.BaseHandler):
    @require_login
    def get(self):
        instance_id = self.get_argument('instance_id', None)
        action = self.get_argument('action', None)
        
        if instance_id == None:
            raise exception.InvalidRequestArgument()
        
        if action == "delete":
            self.delete_instance(instance_id)
        elif action == "get_vnc_console":
            self.get_vnc_console(instance_id)
        #More actions add here!
        else:
            self.prompt_and_redirect(_("Unsupported instance action : %s") % action)
            
    def delete_instance(self, instance_id):
        client = self.session['user']['client']
        result = client.delete_instance(instance_id)
        prompt = _("Deleting instance, please wait ...")
        self.prompt_and_redirect(prompt)
    
    def get_vnc_console(self, instance_id):
        client = self.session['user']['client']
        console_url = client.get_vnc_console_url(instance_id)
        prompt = _("Getting VNC console ...")
        self.prompt_and_redirect(prompt, console_url)
        