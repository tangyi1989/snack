
from snack import exception

from tornado.web import RequestHandler
from snack.session import RedisSession, Session

def require_login(request_method):
    """
    A decorator to check the if the user is logged in.
    """
    def wrapper(self, *args, **kwargs):
        if not self.is_logged_in():
            raise exception.NotLoggedInError()
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
                self._session = RedisSession(self.application.session_store, 
                                             sessionid, expires_days=expires)
                if not sessionid: 
                    self.set_secure_cookie('sid', self._session.id, 
                                           expires_days=expires)
            else:
                self._session = Session(self.get_secure_cookie, 
                                        self.set_secure_cookie, 
                                        expires_days=expires)
                
            return self._session
    
    def _handle_request_exception(self, e):
        """
        Handle uncaught exception in base class.
        """
        #Snack's own exception
        if isinstance(e, exception.SnackException):
            self.handle_snack_exception(e)
        #Other exception
        else:
            self.write(e.message)
            self.flush()
    
    def handle_snack_exception(self, e):
        #Specify exception that we want handle
        exception_handlers = {exception.NotLoggedInError : self.handle_not_logged_in}
        if exception_handlers.has_key(type(e)):
            return exception_handlers[type(e)](e)
        
        #Common exception, just display it, and return to previous page
        referer = self.request.headers.get('Referer', "/")
        self.render("common/exception.html", exception=e, 
                    referer=referer)
        
    def handle_not_logged_in(self, e):
        referer = self.request.headers.get('Referer', "/auth")
        self.render("common/exception.html", exception=e, 
                    referer=referer)
    
    def is_logged_in(self):
        return 'user' in self.session
    