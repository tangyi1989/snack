
from snack import utils
from snack.handler import base
from snack.handler.base import require_login

class Index(base.BaseHandler):
    
    @utils.debug
    @require_login
    def get(self):
        self.render('common/index.html')