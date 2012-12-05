
from snack import utils
from snack import client
from snack.handler import base
from snack.handler.base import require_login

class Auth(base.BaseHandler):
    
    def get(self):
        self.render("login.html")
    
    @utils.debug
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        snack_client = client.SnackClient.authenticate(username, password)
        user = dict(username=username, client=snack_client)
        self.session['user'] = user
        self.session.save()
        self.redirect('/')
        
class Logout(base.BaseHandler):
    
    def get(self):
        del self.session['user']
        self.redirect('/auth')