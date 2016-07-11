#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

BANNER = """
Google Play Unofficial API Interactive Shell
Successfully logged in using your Google account. The variable 'api' holds the API object.
Feel free to use help(api).
"""

import code

from googleplay import GooglePlayAPI

api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
code.interact(BANNER, local=locals())
