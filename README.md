# newer-app-cleaner

Updated [app-cleaner.sh](https://github.com/sunknudsen/privacy-guides/tree/master/how-to-clean-uninstall-macos-apps-using-appcleaner-open-source-alternative) from Sun Knudsen for iOS apps on Macs

## Usage

Example: Damus iOS app removal.

```
$ app-cleaner.sh /Applications/Damus.app
Cannot find /Applications/Damus.app/Contents/Info.plist
(Found /Applications/Damus.app/Wrapper/Damus.app/Info.plist)
(Assigned /Applications/Damus.app/Wrapper/Damus.app/Info.Plist)

  ************* IMPORTANT *************
  * This is an iOS app with Containers!
  * Next, run $ find-all.sh Damus (case-insensitive)
  * find-all.sh available at https://verityj.github.io
  * Remove all identified folders from ~/Library/Containers/<long-string>

Checking for running processes…
Finding app data…
/Applications/Damus.app
/var/folders/qp/fvwj41093d7c1ht9k_kmml100000gn/C/com.jb55.damus2
Move app data to trash (y or n)?
```

This will quit any running processes and find the usual files for the application.
Allow this script to move the found files to Trash, as usual.

Then find the other files still remaining (example for iOS Damus.app, replace with any part of the iOS app name):

```
$ find-all.sh damus
```

`find-all.sh` is [my script](https://gist.github.com/verityj/1baf59b95a7da5f03a44ce0620a4253d) that I use to find everything that might be hiding in the system:

There will be other files found! There will be app logs, for example. Those are safe to remove.

The most important are the container folders, such as

```
/Users/<your-user>/Library/Containers/B39DA0EE-A036-4E9F-BA8D-75C674F70F91/Data/Library/Saved Application State/com.jb55.damus2~iosmac.savedState
/Users/<your-user>/Library/Containers/B39DA0EE-A036-4E9F-BA8D-75C674F70F91/Data/Library/Preferences/com.jb55.damus2.plist
/Users/<your-user>/Library/Containers/B39DA0EE-A036-4E9F-BA8D-75C674F70F91/Data/Library/Application Scripts/com.jb55.damus2
/Users/<your-user>/Library/Containers/B39DA0EE-A036-4E9F-BA8D-75C674F70F91/Data/Library/HTTPStorages/com.jb55.damus2
/Users/<your-user>/Library/Containers/B39DA0EE-A036-4E9F-BA8D-75C674F70F91/Data/Library/Caches/com.jb55.damus2
```

Delete all those containers (there may be more than 1). Just copy the paths from the list of results above:
```
$ rm -rf /Users/<your-user>/Library/Containers/B39DA0EE-A036-4E9F-BA8D-75C674F70F91
```

Cleaning done! No more app.
