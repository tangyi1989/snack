
from snack import exception

from tornado.web import RequestHandler
from snack.session import RedisSession, Session

def require_login(request_method):
    """
    A decorator to check the if the user is logged in.
    """
    def wrapper(self, *args, **kwargs):
        if not self.is_logged_in():
            raise exception.NotLoggedInException()
        else:
            return request_method(self, *args, **kwargs)
        
    return wrapper

class BaseHandler(RequestHandler):
    """
    Base of all handlers in snack, process all common things.
    """ 
    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            self.require_setting('permanent_session_lifetime', 'session')
            expires = self.settings['permanent_session_lifetime'] or None
            if 'redis_server' in self.settings and self.settings['redis_server']:
                sessionid = self.get_secure_cookie('sid')
                self._session = RedisSession(self.application.session_store, sessionid, expires_days=expires)
                if not sessionid: 
                    self.set_secure_cookie('sid', self._session.id, expires_days=expires)
            else:
                self._session = Session(self.get_secure_cookie, self.set_secure_cookie, expires_days=expires)
            return self._session
        
    def _handle_request_exception(self, e):
        """
        Handle uncaught exception in base class.
        """
        if isinstance(e, exception.SnackException):
            self.write(e.message)
        else:
            self.write(e.message)
            
        self.finish()
        
    def is_logged_in(self):
        return 'user' in self.session
    