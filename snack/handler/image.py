

from snack import utils
from snack.handler import base
from snack.handler.base import require_login

class List(base.BaseHandler):
    @require_login
    def get(self):
        client = self.session['user']['client']
        self.render('image/list.html' ,images = client.get_image_list())