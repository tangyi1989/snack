
from snack import utils
from snack import client
from snack.handler import base
from snack.handler.base import require_login

class Auth(base.BaseHandler):
    def get(self):
        self.render("common/login.html")
    
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        snack_client = client.SnackClient.authenticate(username, password)
        user = dict(username=username, client=snack_client)
        self.session['user'] = user
        self.session.save()
        self.redirect('/')
        
class SwitchTenant(base.BaseHandler):
    @require_login
    def get(self):
        tenant_name = self.get_argument('tenant_name', None)
        if tenant_name == None:
            raise exception.InvalidRequestArgument()
        client = self.session['user']['client']
        client.switch_to_tenant(tenant_name)
        self.session['user']['client'] = client
        self.session.save()
        self.prompt_and_redirect(_('Switching tenant'), '/')
        
class Logout(base.BaseHandler):
    def get(self):
        del self.session['user']
        self.session.save()
        self.redirect('/auth')