import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Just some I don't know."