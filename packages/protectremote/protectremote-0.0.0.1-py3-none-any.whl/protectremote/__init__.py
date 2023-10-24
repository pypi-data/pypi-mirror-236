import os
os.environ["SETTINGS_MODULE"] = 'protectremote.settings'

from protectremote.middleware import ProtechRemoteMiddleware, pr_access
from python_settings import settings
from apscheduler.schedulers.background import BackgroundScheduler
from protectremote.job import update_request_data
import copy



def set_token(token: str):
    settings.TOKEN = token
    print("new token",   settings.TOKEN)
    
def set_debug(ip_address: str):
    settings.DEBUG_MODE = True
    settings.DEBUG_MODE_IP_ADDRESS = ip_address

def set_request_interval(seconds: int):
    settings.REQUEST_INTERVAL_IN_SECONDS = seconds

def set_render_html_page(active: bool):
    settings.RENDER_HTML_PAGE = active


scheduler = BackgroundScheduler()
job = scheduler.add_job(update_request_data, 'interval', seconds=15)

scheduler.start()


__all__ = [
    "pr_access",
    "set_token",
    "set_debug",
    "set_render_html_page",
    "ProtechRemoteMiddleware"
]