# MK Jul 2016
# runner application file

from playstore import apps_companion
from apk import extractBaseInfo, runMallodroid


apps_companion.do()
extractBaseInfo.apkInfo()
runMallodroid.do()