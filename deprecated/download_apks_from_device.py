    #!/usr/bin/python
    # KK, October 2014
    # Update: Dec, download selected apps

    # The script loads all android apk files from a connected smart phone
    # to the current directory and creates a file with the package name
    # and title of the app
    # Output will be written in file and directory with device id
    # Prerequisutes: adb + aapt + access to apks over debugging bridge

    # TBD Check if files are already existing prior to download

    import os
    import commands
    import re

    # Settings
    GSA = 1 # Get only selected apks, must give apk names in file
    app_list = "/home/labits/svn/kk/medical/google-apps.txt"
    GAA = 0 # Get all apks from device
    NGP = 1 # set = 1 for no download of appe with google or system in path
    NGA = 1 # set = 1 for no download of google apps

    # Get device number
    command = "adb devices"
    status, output = commands.getstatusoutput(command)
if status: # TBD add offline
    print "Something wrong. Is a device attached?"
    exit()
else:
    devid = output[26:42] # get device ID
    devid.strip("\n")
    print "Device " + devid + " is attached. Staring processing."
    


f_packages = "packages-" + devid
f_path = "paths-" + devid
f_out =  "out-" + devid
os.system("mkdir " + devid)
os.system("rm " + f_packages)
os.system("rm " + f_path)

counter = 1

# OPTION 1: GET all APKS from device
if GAA == 1:
    os.system("touch " + f_packages)
    os.system("adb shell pm list packages > " + f_packages)

    f = open(f_packages, 'r')
    print "Extracting package path for "
    
    for line in f:
        line = line.strip()
        line = line.replace("package:", "")
        if NGA and (line.find("com.google.")>-1 or line.find("com.android.")>-1):
            print "Excluding ", line, "(NGA flag set)"
        else:
            print "Inlcuding " + line
            command = "adb shell pm path " + line + " >> " + f_path
            os.system(command)
            counter += 1
    f. close()

# OPTION 2: GET only selected apps
if GSA == 1:
    f = open(app_list, 'r')
    print "Extracting package path for "
    counter = 1
    for line in f:
        if len(line)<4: continue
        line = line.strip()
        # line = line.replace("https://play.google.com/store/apps/details?id=", "")
                
        if NGA and (line.find("com.google.")>-1 or line.find("com.android.")>-1):
            print "Excluding ", line, "(NGA flag set)"
        else:
            print "Inlcuding " + line
            command = "adb shell pm path " + line + " >> " + f_path
            os.system(command)
            counter += 1
    f. close()


print "Will try do download ",counter, " APK files."

print "Downloading apk for "
f = open(f_path, 'r')
g = open(f_out, 'w')
for line in f:
    line = line.strip()
    line = line.replace("package:", "")
    print "Treating: " + line
    s = line.split("/")
    print "Path information: " + str(s)
    if NGP and ("android" in s or "system" in s): # no download for android or system apks
        print "No download for android or system apks"
    else:
        print "Pulling " + line
        command = "adb pull " + line + " " + devid
        os.system(command)      
        command = "aapt dump badging " + s[-1] + " | grep application-label:"
        out = commands.getstatusoutput(command)
        # print "Result: "+ line + "\t" + s[-1] + "\t" + out[1] 
        g.write(line + "\t" + s[-1] + "\t" + out[1] + "\n")
g.close()
f.close()


