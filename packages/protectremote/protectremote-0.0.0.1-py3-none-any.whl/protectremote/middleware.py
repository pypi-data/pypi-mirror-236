from werkzeug.wrappers import Request, Response
from .main import has_ip_access, get_html
from functools import wraps
from flask import make_response, jsonify, render_template
from python_settings import settings 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent



class ProtechRemoteMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        
        if not has_ip_access():
            # TODO: response type ( html or json)
            if settings.RENDER_HTML_PAGE:
                res = Response(get_html(), mimetype='text/html', status=401)
            else:
                res = Response(settings.RESTRICTED_MESSAGE, mimetype='text/plain', status=401)
            return res(environ, start_response)
        return self.app(environ, start_response)
    

def pr_access():
    def _pr_access(f):
        @wraps(f)
        def __pr_access(*args, **kwargs):
            # just do here everything what you need
            if not has_ip_access():
                if settings.RENDER_HTML_PAGE:
                    return make_response(get_html(), 401)
                else:
                    return make_response(settings.RESTRICTED_MESSAGE, 401)
            result = f(*args, **kwargs)
            return result
        return __pr_access
    return _pr_access