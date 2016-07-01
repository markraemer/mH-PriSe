# separator used by search.py, categories.py, ...
import ConfigParser

# load configuration
config = ConfigParser.RawConfigParser()
config.read('config.prop')

SEPARATOR = ";"

LANG            = config.get('googleplay','gp.language')
ANDROID_ID      = config.get('googleplay','gp.android_ID')
GOOGLE_LOGIN    = config.get('googleplay','gp.mail_address')
GOOGLE_PASSWORD = config.get('googleplay','gp.mail_password')
AUTH_TOKEN      = None # "yyyyyyyyy"

# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

