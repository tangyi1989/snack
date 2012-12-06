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

define("port", default=80, help="run on the given port", type=int)
#this line is for test
class Application(web.Application):
    def __init__(self):
        
        handlers = [(r"/", handler.common.Index),
                    (r"/auth", handler.user.Auth),
                    (r"/logout", handler.user.Logout),
                    (r"/image/list", handler.image.List),]
        
        redis_connection = redis.Redis(host='localhost', port=6379, db=0)
        self.session_store = RedisSessionStore(redis_connection)
        
        application_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            permanent_session_lifetime = 1, #These 3 parameter is just for session
            redis_server = True,
            cookie_secret = 'You would never know this.',
            debug=settings.DEBUG)
        
        web.Application.__init__(self, handlers, **application_settings)

def main():
    tornado.options.parse_command_line()
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
