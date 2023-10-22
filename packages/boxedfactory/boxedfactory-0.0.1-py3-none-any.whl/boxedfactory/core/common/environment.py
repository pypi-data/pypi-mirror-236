import os

def getenv(name:str, default_value:None):
    os.environ.get(name, default_value)