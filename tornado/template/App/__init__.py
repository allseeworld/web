from tornado.web import Application

from App.urls import patterns
from App.settings import app_settings


def make_app():
    return Application(
        handlers=patterns,
        **app_settings,
    )
