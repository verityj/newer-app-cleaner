#!/bin/zsh

# Written by: VerityJ
# Published on: https://gist.github.com/verityj
#
# Usage: ./app-cleaner.sh /Applications/<app-name>.app
#
# Modified from:
# https://github.com/sunknudsen/privacy-guides/tree/d6b7f836a0595efaf9716703b597138ce34e3b28/how-to-clean-uninstall-macos-apps-using-appcleaner-open-source-alternative

if [ -z "$1" ] || [ "$1" = "--help" ]; then
  printf "%s\n" "Usage: app-cleaner.sh /path/to/app.app"
  exit 0
fi

IFS=$'\n'

red=$(tput setaf 1)
normal=$(tput sgr0)

app_name=$(basename $1 .app)

if [ ! -e "$1/Contents/Info.plist" ]; then
  printf "%s\n" "Cannot find "$1"/Contents/Info.plist"
  if [ ! -e "$1/Wrapper/$app_name.app/Info.plist" ];
  then
    printf "%s\n" "Cannot find "$1"/Wrapper/"$app_name".app/Info.plist"
    exit 1
  else
    printf "%s\n" "(Found "$1"/Wrapper/"$app_name".app/Info.plist)"
    info_plist=$1/Wrapper/$app_name.app/Info.Plist
    printf "%s\n" "(Assigned "$info_plist")"
    printf "\n"
    printf "%s\n" "  ************* IMPORTANT *************"
    printf "%s\n" "  * This is an iOS app with Containers!"
    printf "  * Next, run \$ find-all.sh "$app_name
    printf "%s\n" " (case-insensitive)"
    printf "%s\n" "  * find-all.sh available at https://verityj.github.io"
    printf "%s\n" "  * Remove all identified folders from ~/Library/Containers/<long-string>"
    printf "\n"
  fi
  else
    info_plist=$1/Contents/Info.Plist
    printf "%s\n" "Assigned "$info_plist
fi

bundle_identifier=$(/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$info_plist" 2> /dev/null)

if [ "$bundle_identifier" = "" ]; then
  printf "%s\n" "Cannot find app bundle identifier"
  exit 1
fi

printf "%s\n" "Checking for running processes…"
sleep 1

processes=($(pgrep -afil "$app_name" | grep -v "app-cleaner.sh"))

if [ ${#processes[@]} -gt 0 ]; then
  printf "%s\n" "${processes[@]}"
  printf "$red%s$normal" "Kill running processes (y or n)? "
  read -r answer
  if [ "$answer" = "y" ]; then
    printf "%s\n" "Killing running processes…"
    sleep 1
    for process in "${processes[@]}"; do
      echo $process | awk '{print $1}' | xargs sudo kill 2>&1 | grep -v "No such process"
    done
  fi
fi

paths=()

paths+=($(find /private/var/db/receipts -iname "*$app_name*.bom" -maxdepth 1 -prune 2>&1 | grep -v "Permission denied"))
paths+=($(find /private/var/db/receipts -iname "*$bundle_identifier*.bom" -maxdepth 1 -prune 2>&1 | grep -v "Permission denied"))

if [ ${#paths[@]} -gt 0 ]; then
  printf "%s\n" "Saving bill of material logs to desktop…"
  sleep 1
  for path in "${paths[@]}"; do
    mkdir -p "$HOME/Desktop/$app_name"
    lsbom -f -l -s -p f $path > "$HOME/Desktop/$app_name/$(basename $path).log"
  done
fi

printf "%s\n" "Finding app data…"
sleep 1

locations=(
  "$HOME/Library"
  "$HOME/Library/Application Scripts"
  "$HOME/Library/Application Support"
  "$HOME/Library/Application Support/CrashReporter"
  "$HOME/Library/Containers"
  "$HOME/Library/Caches"
  "$HOME/Library/HTTPStorages"
  "$HOME/Library/Group Containers"
  "$HOME/Library/Internet Plug-Ins"
  "$HOME/Library/LaunchAgents"
  "$HOME/Library/Logs"
  "$HOME/Library/Preferences"
  "$HOME/Library/Preferences/ByHost"
  "$HOME/Library/Saved Application State"
  "$HOME/Library/WebKit"
  "/Library"
  "/Library/Application Support"
  "/Library/Application Support/CrashReporter"
  "/Library/Caches"
  "/Library/Extensions"
  "/Library/Internet Plug-Ins"
  "/Library/LaunchAgents"
  "/Library/LaunchDaemons"
  "/Library/Logs"
  "/Library/Preferences"
  "/Library/PrivilegedHelperTools"
  "/private/var/db/receipts"
  "/usr/local/bin"
  "/usr/local/etc"
  "/usr/local/opt"
  "/usr/local/sbin"
  "/usr/local/share"
  "/usr/local/var"
  $(getconf DARWIN_USER_CACHE_DIR | sed "s/\/$//")
  $(getconf DARWIN_USER_TEMP_DIR | sed "s/\/$//")
)

paths=($1)

for location in "${locations[@]}"; do
  paths+=($(find "$location" -iname "*$app_name*" -maxdepth 1 -prune 2>&1 | grep -v "No such file or directory" | grep -v "Operation not permitted" | grep -v "Permission denied"))
done

for location in "${locations[@]}"; do
  paths+=($(find "$location" -iname "*$bundle_identifier*" -maxdepth 1 -prune 2>&1 | grep -v "No such file or directory" | grep -v "Operation not permitted" | grep -v "Permission denied"))
done

paths=($(printf "%s\n" "${paths[@]}" | sort -u));

printf "%s\n" "${paths[@]}"

printf "$red%s$normal" "Move app data to trash (y or n)? "
read -r answer
if [ "$answer" = "y" ]; then
  printf "%s\n" "Moving app data to trash…"
  sleep 1
  posixFiles=$(printf ", POSIX file \"%s\"" "${paths[@]}" | awk '{print substr($0,3)}')
  osascript -e "tell application \"Finder\" to delete { $posixFiles }" > /dev/null
  printf "%s\n" "Done"
fi
