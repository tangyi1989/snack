import os
import redis
import tornado.options

from tornado import ioloop
from tornado import web
from tornado import httpserver
from tornado.options import define, options

from snack import handler
from snack import settings
from snack.session import RedisSessionStore
from snack import greentornado

define("port", default=8888, help="run on the given port", type=int)

class Application(web.Application):
    def __init__(self):
        
        handlers = [(r"/", handler.common.Index),
                    (r"/auth", handler.user.Auth),
                    (r"/logout", handler.user.Logout),
                    (r"/user/switch_to_tenant", handler.user.SwitchTenant),
                    (r"/instance/list", handler.instance.List),
                    (r"/instance/create", handler.instance.Create),
                    (r"/instance/action", handler.instance.Action),
                    #Handle all ajax request
                    (r"/~ajax/(.*)", handler.ajax.AjaxHandler),]
        
        #Greenify all handlers, so the request would be nonblock.
        for app_handler in handlers:
            hanlder_cls = app_handler[1]
            greentornado.greenify(hanlder_cls)
        
        redis_connection = redis.Redis(host='localhost', port=6379, db=0)
        self.session_store = RedisSessionStore(redis_connection)
        
        application_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            
            #These three parameters are used for session settings.
            permanent_session_lifetime = 1,
            redis_server = True,
            cookie_secret = 'You would never know this.',
            
            debug=settings.DEBUG)
        
        web.Application.__init__(self, handlers, **application_settings)

def main():
    tornado.options.parse_command_line()
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    #ioloop.IOLoop.instance().start()
    greentornado.Hub.start()

if __name__ == "__main__":
    main()
