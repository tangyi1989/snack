
from snack import utils
from snack import exception
from snack.handler import base

"""
NOTE : This file is just for test.

This project is organized based on instance not function.
So after test, this file should be refactored. 
"""

class Performance(base.BaseHandler):
    def get(self):
        self.render("instance/monitor.html");
    