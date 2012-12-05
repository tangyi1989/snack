
from snack import utils
from snack.handler import base
from snack.handler.base import require_login

class Index(base.BaseHandler):
    
    @require_login
    @utils.debug
    def get(self):
        client = self.session['user']['client']
        print client.public_urls
        self.write("")