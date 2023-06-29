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
# Line 23 change errorCheck to False to simplify output

from sys import argv
from os import popen
from os import remove
from os.path import exists
from os.path import splitext
from pathlib import Path
import time # for pausing

errorCheck = True

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
def bundle_id(infoplist):
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

def search_function(directory, pattern, maxdepth):
  result = ''
  result = popen("find {} -iname '*{}*' -maxdepth {} -print 2>/dev/null | grep -v 'No such file or directory' | grep -v 'Operation not permitted' | grep -v 'Permission denied'".format(directory, pattern, maxdepth)).read().rstrip().splitlines()
  return result

#################
# Make a choice #
#################

def choose_to_delete(list):
  class color:
    blue = "\033[34m"
    green = "\033[32m"
    bold = "\033[1m"
    reset_all = "\033[0m"
  
  choice = input(f"\n - {color.bold}{color.blue}Delete the above [y/n]? ")
  print(f"{color.reset_all}", end='')
  if choice == 'y':
    # Mac OS user Trash folder location:
    trash = home_path + "/.Trash/"
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

app_name = argv[1].split('/')[2]
app_name = app_name.split('.app')[0]

# If application name is identified:
if app_name:
  # Check if the app is completely closed, no running processes
  if not popen(f"pgrep -afil '{app_name}' | grep -v 'app-cleaner' | grep -v 'pgrep'").read():
    if errorCheck:
      print(f" - '{app_name}' is not running. Proceeding")
  else:
    print(f"\n - {app_name} is running, quit and retry. Exiting\n")
    print("Running process(es):")
    print(popen(f"pgrep -afil '{app_name}' | grep -v 'app-cleaner' | grep -v 'pgrep'").read())
    exit(0)
  # For Mac applications, need to go 2 levels deep to find Info.plist
  infoplist_found = search_function(argv[1],'Info.plist', 2)
  if not infoplist_found:
    if errorCheck:
      print(" - This is not a regular Mac app, will search Containers")
    # For iOS containers, need to go 3 levels deep to find Info.plist
    infoplist_found = search_function(argv[1],'Info.plist', 3)
    if infoplist_found:
      infoplist_ios = infoplist_found[0]
      if errorCheck:
        print(f" - Found preference list {infoplist_ios}")
      identifier = bundle_id(infoplist_ios)
  elif infoplist_found:
    # This is a regular Mac app
    infoplist_mac = infoplist_found[0]
    if errorCheck:
      print(f" - Found preference list {infoplist_mac}")
    identifier = bundle_id(infoplist_mac)
  else:
    "'Info.plist' could not be found. Exiting"
    exit(0)
else:
  print(" - {} not found in /Applications/. Exiting".format(argv[1]))
  exit(0)

# Set search locations
from os.path import expanduser
home_path = expanduser('~')
locations = [
  "/private/var/db/receipts",
  "{}/Library".format(home_path),
  "{}/Library/Application Scripts".format(home_path),
  "{}/Library/Application Support".format(home_path),
  "{}/Library/Application Support/CrashReporter".format(home_path),
  "{}/Library/Containers".format(home_path),
  "{}/Library/Caches".format(home_path),
  "{}/Library/HTTPStorages".format(home_path),
  "{}/Library/Group Containers".format(home_path),
  "{}/Library/Internet Plug-Ins".format(home_path),
  "{}/Library/LaunchAgents".format(home_path),
  "{}/Library/Logs".format(home_path),
  "{}/Library/Preferences".format(home_path),
  "{}/Library/Preferences/ByHost".format(home_path),
  "{}/Library/Saved Application State".format(home_path),
  "{}/Library/WebKit".format(home_path),
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
  results += search_function(location, identifier, 1)
  results += search_function(location, app_name, 1)
# search through additional special locations
results += search_function('/private/var/tmp', identifier, 6)
results += search_function('/private/var/folders', identifier, 4)

try:
  infoplist_ios
  containers = []
  if errorCheck:
    print(f" - Looking for {app_name} containers")
  container_files = search_function("{}/Library/Containers".format(home_path), identifier, 6)
  # if containers are found
  if container_files:
    if errorCheck:
      print(" - Found container files:")
    for container_file in container_files:
      if errorCheck:
        print(container_file)
      container_folder = container_file.split('/')[5]
      if container_folder not in containers:
        containers.append(container_folder)
    for i in range (0, len(containers)):
      results += f'{home_path}/Library/Containers/{containers[i]}'.splitlines()
  else:
    if errorCheck:
      print(" - No containers found. Proceeding")
except:
  # this is not an iOS app with containers. Done
  # exit(0)
  pass

print(f"\n - All {app_name} locations:\n")
for file in results:
  print(file)

choose_to_delete(results)
