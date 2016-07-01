
# def installapk(appId):
#     command = ["adb"]
#     if deviceId  <> "":
#         command.extend(["-s", deviceId])
#     command.extend(["install", "-r", "-d", path + appId + "/" + appId + ".apk"])
#     result = os.system(" ".join(command))

import pdfkit

pdfkit.from_url("https://play.google.com/store/apps/details?id=com.whatsapp","1.pdf")