# Any Aspect Ratio for Tears of the Kingdom!
Any Aspect Ratio for Tears of the Kingdom! With HUD fix and controller merge and blackscreenfix

Download Link: https://github.com/fayaz12g/totk-aar/releases/download/3.3.0/AAR.3.3.0.zip

If you want to donate to support this utility, you can here: https://ko-fi.com/fayaz12

This utility lets you select the following:

Aspect Ratio (type in ANY two numbers, like the resolution of your display)

Controller Type, Button Color, and Button Layout

Centered or Corner HUD

It will then create a mod given all those parameters, including a HUD fix, a fix for link in the menu, and the aspect ratio mod itself, and black screen fix. If you use this utility, disable BlackscreenFIX, Controller Mods, and my Any Aspect Ratio mod. This one file will do all that for you and more!

You need Python 3.11 to use this. If you don't have it, open PowerShell and enter "python". Then download what it opens.

Known Issues
- Elden Ring only uses Colored button. Selecting White buttons uses colored buttons
- Character names are stretched
- Aspect ratios below 16:9 dont support corner HUD, only center
- The Elden Ring layout yields Colored regardless of white being entered
- Item pickup text is stretched
- Some HUD elements aren't cornered (item pickup, location name)


Stretch Goals
- Colored Dualsense Controller Options
- DualShock Controller Option
- Stadia Controller Option
- python 3.11 is required but if I call the functions using subprocesses i could avoid this 
- include a feature to specify a FOV
- include a "launch game" button

Running Changelog:

3.3.0
- New credits tab indicating appropriate credits (will be updated based on what they prefer later)
- New console tab if you want to see the steps that are running
- New Emulator selector to automatically output the mod in the yuzu or ryujinx folder
- Customize Output button to select where you want the mod to generate if not in the yuzu or ryujinx folders (if you are transferring it to a different device like a Steam Deck)
- Now removes older versions of the mod detected in yuzu or ryujinx

3.2.0
- Includes early support for steam controller
- Early support for steam deck controller

3.1.1
- Fixed v3.1 Download issue with new console

3.1.0
- New output console created with simpler to understand text

3.0.0
- File size reduced from 1.3GB to 14MB

2.1.2
- Fixed an issue where charset was needed to be installed

2.1.1
- Fixes the issue where urllib3 was not found, causing the entire thing to fail
- No longer requires a "pip install requests" from powershell
- Smaller file size utilizing 7z archiving

2.1.0
- Fixes an issue where the nsobid does not update for different versions of the pchtxt
- Adds option for switch controller
- Adds all the PlayStation Controllers

2.0.2
- Fixed an issue that used an old status label config outputting an error (albeit, it did not interrupt the script, but people complained)

2.0.1
- Fixes critical issue where the HUD would be expanded vertically even if the aspect ratio was bigger than 16/9. This is to support aspect ratios such as 4:3. 3:2. and 16:10.

2.0.0
- Introduced support to automatically download and pack in selected controller layouts, no more external files required

1.0.0
-allows you to simply select a .zs file, it unpacks it, modifies the contents, then repacks it where it needs to go.

0.0.3
- Fixed an issue where zstandard files would not decompress. 

0.0.2
- Went to the open folder format to show the source code to virus scanning programs
- Packed in dependencies

0.0.1
- Now you can create whatever aspect ratio you want! This is an early version. the debug file contains everything I've been working on, but I literally started this program yesterday so its in EARLY STAGES! Right now, the only guaranteed thing to work is the main file with patch creating for any aspect ratio, not the hud fix, yet.
