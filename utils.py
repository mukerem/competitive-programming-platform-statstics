import os

from dotenv import load_dotenv

load_dotenv()

def get_env(var_name):
    value = os.environ.get(var_name)
    if value is None:
        msg = "Set the %s environment variable" % var_name
        raise ValueError(msg)
    return value