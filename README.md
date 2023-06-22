# newer-app-cleaner

How to clean out your system completely of a given app, especially the iOS apps on Macs. No software to install to do this, and you are in complete control of the process.

It is great to be able to install, use and check out iOS apps on a Mac. But how do you make absolutely sure it is completely gone when you decide to trash it or reinstall?

# Version 2 - a Python script

> ***Update:*** I uploaded a [souped up Python script] version as well. It does it all in one script, handles native Mac as well as wrapped iOS app removal. Complete and utter removal. Because I could not just leave it well enough alone, I guess.

# Version 1 - shell script

There is already an excellent script by Sun Knudsen called [app-cleaner.sh]. Unfortunately, it fails completely for iOS apps and it still may leave some files behind (like crash logs).

I updated the script and published the [new app-cleaner.sh] with instructions for use.

## Installation (of script version 1)

Download the [new app-cleaner.sh].

Make it executable and place the file anywhere you find convenient. I recommend:

```
$ chmod +x app-cleaner.sh
    # Now the script is able to run
$ mv app-cleaner.sh /usr/local/bin/
    # Now the script is available to you from anywhere
```

## First, clean up with the new app-cleaner.sh version 1

Once you have the script ready to use, let it stop any running processes and trash the usual files. This updated version will be able to process the iOS apps and will let you know about it. Here is an example of uninstalling a Damus iOS (Nostr chat) app from a Mac.

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

As you can see, the script will move _most_ of the app files to Trash. If you're happy with it so far, empty Trash to avoid finding those files in the next and final step.

## Clean up the rest (after running script version 1)

Find the other files still remaining (example for iOS Damus.app, replace with any part of the iOS app name) by running the following script.

```
$ find-all.sh damus
```

This script was covered in the [Search blog post] previously.

## Resources:

- Updated version 2: [souped up Python script]
- Updated version 1: [new app-cleaner.sh]
- Starting point [app-cleaner.sh]
- [Search blog post]

[app-cleaner.sh]: https://github.com/sunknudsen/privacy-guides/tree/d6b7f836a0595efaf9716703b597138ce34e3b28/how-to-clean-uninstall-macos-apps-using-appcleaner-open-source-alternative
[new app-cleaner.sh]: https://github.com/verityj/newer-app-cleaner/blob/000524534e6a0befc6f8e4f48674c8164c4d9302/app-cleaner.sh
[Search blog post]: https://github.com/verityj/verityj.github.io/blob/b264f1af4cb9af93ecf8abf7c2e69054a65f8c5a/_posts/2023-06-16-search.md
[souped up Python script]: https://github.com/verityj/newer-app-cleaner/blob/32ef8e1b4a7acea9bbe6265c179af53986529e19/app-cleaner.py
