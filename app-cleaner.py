#!/usr/bin/env python3
# Created using python 3.9.6 on Mac OS 13
#
# This script removes directories and files specific to a given application
#
# Created by VerityJ
# https://verityj.github.io
# Created 2023.06
#
# Usage: python3 app-cleaner.py /Applications/<app-name>.app
# Example: python3 app-cleaner.py /Applications/Damus.app
#
# Line 15 change errorCheck to False to simplify output

errorCheck = True

from sys import argv
from os import popen
from os import remove
from os.path import exists
from os.path import splitext
from pathlib import Path
import time # for pausing

##############
# How to use #
##############

if len(argv) != 2:
  print("\nUsage:")
  print("python3 {} /Applications/<app-name>.app".format(argv[0]))
  print("\nExample:")
  print("python3 {} /Applications/Damus.app\n".format(argv[0]))
  exit(0)

#########################
# Get bundle identifier #
#########################
# Command:
# /usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "/Applications/<app-name>.app/Contents/Info.plist" 2> /dev/null
def bundleID(infoplist):
  identifier = ''
  identifier = popen(f"/usr/libexec/PlistBuddy -c \"Print CFBundleIdentifier\" \"{infoplist}\" 2> /dev/null").read().rstrip()
  if identifier != '':
    if errorCheck:
     print(" - Found bundle identifier", identifier)
    return identifier
  else:
    print("Bundle identifier not found. Exiting")
    exit(0)

########
# Find #
########

def searchFunction(directory, pattern, maxdepth):
  result = ''
  result = popen("find {} -iname '*{}*' -maxdepth {} -print 2>/dev/null | grep -v 'No such file or directory' | grep -v 'Operation not permitted' | grep -v 'Permission denied'".format(directory, pattern, maxdepth)).read().rstrip().splitlines()
  return result

#################
# Make a choice #
#################

def chooseToDelete(list):
  class color:
    blue = "\033[34m"
    green = "\033[32m"
    bold = "\033[1m"
    reset_all = "\033[0m"
  
  choice = input(f"\n - {color.bold}{color.blue}Delete the above [y/n]? ")
  print(f"{color.reset_all}", end='')
  if choice == 'y':
    # Mac OS user Trash folder location:
    trash = homePath + "/.Trash/"
    if Path(trash).exists():
      for file in list:
        # popen(f"mv -f {file} {trash}")
        try:
          popen(f"osascript -e 'tell application \"Finder\"' -e 'try' -e 'set source_file to POSIX file (\"{file}\")' -e 'delete source_file with replacing' -e 'end try' -e 'end tell' ")
          time.sleep(2)
        finally:
          print(f"{color.blue}Moving to trash:{color.reset_all} {file}")
    else:
      # Trash folder not found, remove:
      popen(f"rm -rf {file} {trash}/")
    time.sleep(2)
  else:
    print(f" - {color.green}No changes made{color.reset_all}")

########
# Main #
########

appName = argv[1].split('/')[2]
appName = appName.split('.app')[0]

# If application name is identified:
if appName:
  # Check if the app is completely closed, no running processes
  if not popen(f"pgrep -afil '{appName}' | grep -v 'app-cleaner' | grep -v 'pgrep'").read():
    if errorCheck:
      print(f" - '{appName}' is not running. Proceeding")
  else:
    print(f"\n - {appName} is running, quit and retry. Exiting\n")
    print("Running process(es):")
    print(popen(f"pgrep -afil '{appName}' | grep -v 'app-cleaner' | grep -v 'pgrep'").read())
    exit(0)
  # For Mac applications, need to go 2 levels deep to find Info.plist
  infoplistFound = searchFunction(argv[1],'Info.plist', 2)
  if not infoplistFound:
    if errorCheck:
      print(" - This is not a regular Mac app, will search Containers")
    # For iOS containers, need to go 3 levels deep to find Info.plist
    infoplistFound = searchFunction(argv[1],'Info.plist', 3)
    if infoplistFound:
      infoplist_ios = infoplistFound[0]
      if errorCheck:
        print(f" - Found preference list {infoplist_ios}")
      identifier = bundleID(infoplist_ios)
  elif infoplistFound:
    # This is a regular Mac app
    infoplist_mac = infoplistFound[0]
    if errorCheck:
      print(f" - Found preference list {infoplist_mac}")
    identifier = bundleID(infoplist_mac)
  else:
    "'Info.plist' could not be found. Exiting"
    exit(0)
else:
  print(" - {} could not be processed as an app. Exiting".format(argv[1]))
  exit(0)

# Set search locations
from os.path import expanduser
homePath = expanduser('~')
locations = [
  "/private/var/db/receipts",
  "{}/Library".format(homePath),
  "{}/Library/Application Scripts".format(homePath),
  "{}/Library/Application Support".format(homePath),
  "{}/Library/Application Support/CrashReporter".format(homePath),
  "{}/Library/Containers".format(homePath),
  "{}/Library/Caches".format(homePath),
  "{}/Library/HTTPStorages".format(homePath),
  "{}/Library/Group Containers".format(homePath),
  "{}/Library/Internet Plug-Ins".format(homePath),
  "{}/Library/LaunchAgents".format(homePath),
  "{}/Library/Logs".format(homePath),
  "{}/Library/Preferences".format(homePath),
  "{}/Library/Preferences/ByHost".format(homePath),
  "{}/Library/Saved Application State".format(homePath),
  "{}/Library/WebKit".format(homePath),
  "/Library",
  "/Library/Logs/DiagnosticReports",
  "/Library/Application Support",
  "/Library/Application Support/CrashReporter",
  "/Library/Caches",
  "/Library/Extensions",
  "/Library/Internet Plug-Ins",
  "/Library/LaunchAgents",
  "/Library/LaunchDaemons",
  "/Library/Logs",
  "/Library/Preferences",
  "/Library/PrivilegedHelperTools",
  "/usr/local/bin",
  "/usr/local/etc",
  "/usr/local/opt",
  "/usr/local/sbin",
  "/usr/local/share",
  "/usr/local/var"
]
# user cache directry is /var/folders/qp/<>/C
locations.append(popen("getconf DARWIN_USER_CACHE_DIR | sed 's/.$//' ").read().rstrip())
# user temp directry is /var/folders/qp/<>/T
locations.append(popen("getconf DARWIN_USER_TEMP_DIR | sed 's/.$//' ").read().rstrip())

# first, include the app itself
results = ["{}".format(argv[1])]

# perform app content search
for location in locations:
  results += searchFunction(location, identifier, 1)
  results += searchFunction(location, appName, 1)
# search through additional special locations
results += searchFunction('/private/var/tmp', identifier, 6)
results += searchFunction('/private/var/folders', identifier, 4)

try:
  infoplist_ios
  containers = []
  if errorCheck:
    print(f" - Looking for {appName} containers")
  containerFiles = searchFunction("{}/Library/Containers".format(homePath), identifier, 6)
  # if containers are found
  if containerFiles:
    if errorCheck:
      print(" - Found container files:")
    for containerFile in containerFiles:
      if errorCheck:
        print(containerFile)
      container_folder = containerFile.split('/')[5]
      if container_folder not in containers:
        containers.append(container_folder)
    for i in range (0, len(containers)):
      results += f'{homePath}/Library/Containers/{containers[i]}'.splitlines()
  else:
    if errorCheck:
      print(" - No containers found. Proceeding")
except:
  # this is not an iOS app with containers. Done
  # exit(0)
  pass

print(f"\n - All {appName} locations:\n")
for file in results:
  print(file)

chooseToDelete(results)
