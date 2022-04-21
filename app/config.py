from os import getenv
from dotenv import load_dotenv

def get_config(key):
    """ Returns the value of the key on a .env file or from an environment variable"""
    load_dotenv()
    value = getenv(key, None)
    #print("{}:{}".format(key, value))
    return value