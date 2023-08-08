8.6.1
- Fix an issue where text fields have white text in light mode making it unreadable
- Cleanup code in the compress script

8.6.0
- The main fix here is the save screen now shows the correct aspect ratio for the game preview image!
- Added default values for all dFPS elements
- Fixed issue with custom output folder
- Cleaned up download code to optimize it

8.5.1
- Autoupdates
- You can now customize the name of the generated mod
- Updated credits with acknowledgment of @InterClaw for their help in detailed issue reporting
- Credits is now clickable and leads to the GitHub repo page
- Unneeded visuals are now moved to legacy
- Disable Dynamic res now notes it’s incompatibility (thanks @SigonLegacy for figuring this one out)
- Tweaked save game page again (still a WIP)
- Errors will now halt the progress bar and make it red
- Now if Yuzu or Ryujinx is open, you will see an error message asking you to close it

8.5.0
- Fix shop menu stretching with 16:10 aspect ratio
- Text stretching fixes in save screen
- Camera stretching fixes

8.4.1
- The Print Redirector "flush" command now works to print error messages directly into the custom console
- The console now has a UI that matches the rest of the UI
- The console is now read only so you cannot accidentally type in it

8.4.0
- Visual Fixes SHOULD now work, thanks to an issue found by @InterClaw and @Fruithapje21! A new method loads them all in disabled, and enables them based on the checkboxes you select.
- Fix name of generated Anisotropic Filtering Fix
- Tweaked fixes for the way the save game pane displays the game preview

8.3.0
- This dev build is a WIP, but it contains the following fixes:
- Fixed photos in the compendium being squished when taken and when displayed
- Fixed the game preview in the save game screen
- Fixed the game preview in the load game screen
- Fix the picture preview before saving photos taken with the camera
- Replaced the expand scope feature with a feature to hide the scope circle entirely
- Added offline mode so the tool doesn't rely on the internet if you've ever downloaded the controller mod before
- Removed non critical warnings

dev8.3
- This dev build is a WIP, but it contains the following fixes:
- Fixed photos in the compendium being squished when taken and when displayed
- Fixed the game preview in the save game screen
- Fixed the game preview in the load game screen
- Fix the picture preview before saving photos taken with the camera
- Replaced the expand scope feature with a feature to hide the scope circle entirely
- Added offline mode so the tool doesn't rely on the internet if you've ever downloaded the controller mod before
- Removed non critical warnings

8.2.0
- Fix an issue causing the tool to not run multiple times in one session
- Incorporate the latest fixes and code optimization by Fruithapje21, including corner HUD on smaller than 16:10 aspect ratios

8.1.4
- Now generated properly with custom aspect ratio

8.1.3
- Fix the order the boxes jump to when pressing tab on the visuals screen

8.1.2
- Fix an issue with string to float causing it to not generate properly
- Renamed visuals 2 to legacy visuals, reordered where the visuals were

8.1.1
- Fix an issue with string to float causing it to not generate properly
- Renamed visuals 2 to legacy visuals, reordered where the visuals were

8.1.0
- Update all asm visuals to work on 1.2.0 (previously a few of them were not up to date)
- Add new Visuals 2 tab (temporary until I get better formatting for all the new features)
- Added back the options for static fps and shadow resolution to be exefs asm code not using dFPS. Only use one or the other.
- Added the Remove Lens Flare, Camera Speed, and LOD Improvement Visuals
- Appropriately named the Disable Quality Reduction visual fix

8.0.1
- Switch the order of resolution components (wdith x height)

8.0.0
- new dark mode custom tkinter library!!
- Fixed an issue where shadow resolution would not generate if -1
- Added an edge case for 16/9 that skips all the unpacking and repacking (will be much faster and now won't shift UI elements wrongly)
- Updated lingering GUI issues from refactoring
- Fixed issue causing controller selection to break
- Implemented fixes for circles on menu bars from Fruithapje21
- Implemented fix for purah pad icon
- Optimized code
- Resized console & controller image
- Fixed the issue where dFPS ini wasn't recognized (needs testing)
- Added Chris to the credits :)
- packed in customtkinter
- fixed credits tab
- New Tab layout using customtkinter Tabview instead of Notebook
- New experimental expand shutter option (has issues with the sides being shown)
- Experimental camera picture UI fixes
- New progress bar to show generation progress
- New radio buttons for emulator and Hud location

7.0.0
- Includes the newest fixes from Fruit. These issues have been resolved:
- Map no longer is duplicated in quest menu
- Header bar in the save UI is no longer too short
- Geogliphs are no longer stretched on map
- Pictures can now be viewed without being squished
- Map on loading screen is no longer stretched

dev721c
- Added an edge case for 16/9 that skips all the unpacking and repacking (will be much faster and now won't shift UI elements wrongly)

dev721b
- Fixed the issue where dFPS ini wasn't recognized (needs testing)
- Added Chris to the credits :)

dev721a
-Restore the unsupported controller options hiding
- Reduce file size by 30%

dev720f
- Updated lingering GUI issues from refactoring
- Fixed issue causing controller selection to break
- Implemented fixes for circles on menu bars from Fruithapje21

dev720e
- Optimized code
- Resized console & controller image

dev720d
-packed in customtkinter
-fixed credits tab

dev720c
- New Tab layout using customtkinter Tabview instead of Notebook

dev720b
- Tabs are more readable and larger
- camera checkbox is lower on the window (window is now larger)
- other minor fixes

dev720a
- New experimental expand shutter option (has issues with the sides being shown)
- Experimental camera picture UI fixes
- New custom Tkinter UI
- New progress bar to show generation progress
- New radio buttons for emulator and Hud location

6.1.3
- Includes Chuck's latest dFPS 1.5.5 beta 3 (released 2 hours ago!)

6.1.2
- Fixed the corner hud boolean in the 1610 script not being recognized as it was passed as a string

6.1.1
- Fixed a wrong name for Anisotropic Filtering Fix

6.1.0
- Thanks to the work by @Fruithapje21, 16:10 aspect ratios now support corner HUD

6.0.1
- Update credits
- Fix a bug causing dFPS not to copy over and freeze

6.0.0
- Now dynamically creates the dFPS mod by ChucksFeedAndSeed INI file with custom values!

5.6.0
- New controller frame layout, almost done, just polishing now.
- Options that don't work are no longer selectable (except for 2 layouts on Steam Deck, Elden Ring and PE)
- An image shows you what your controller scheme will look like
- Text shows you what to map your controller buttons to

5.5.1
- Packed in images correctly (was missing prior)

5.5.0
- As I revamp the controller section (as promised to be the current worked on feature) I have added a new image and controller button mapping explanation section. They are currently not aligned properly so you must stretch the window horizontally to see it. This is a beta because of the misalignment and it being half done, but I think I'll be going to bed for the night so wanted to release this.

5.4.1
- Updated latest version of all controller mods

5.4.0
- Versions 1.5.5 beta 2 of dFPS by ChucksFeedandSeed now copies into the mod folder when selected.
- New message showing the longest step of writing the blarc file to ensure you don't click away
- You can now open the generated mod folder automatically upon completion.
- The tool version is displayed evenly across all frames
- Lays the groundwork for a future version of this tool which will let you customize its settings in the ini to specify any internal resolution, any shadow resolution up to 8192, enter any FPS, and use his camera mod all built in.

5.3.1
- Enable use of new controller repo to support updates to controller mods externally

5.3.0
- Restructured the entire interface and tabs to be more easy to understand

5.2.2
- New error message if Yuzu is open stating to close it
- Now defaults to corner HUD

5.2.1
- New error message if Yuzu is open stating to close it
- Now defaults to corner HUD

5.2.0
- Fix a fatal issue that causes the game to crash on startup due to improperly generated exefs

5.1.1
- Update tool version
- Fix comments trying to be passed into the code

5.1.0
- Fixed Hestu Menu fix for 1.2.0 as provided by [keatonthewise]
- Made the generated pchtxt more human readable to ensure the correct settings were applied
- Cleaned up code in patch.py

5.0.0
- VISUAL FIXES NOW WORK Not guaranteed for 1.2.0 until a future update, but works on 1.0.0-1.1.2
- New tool version notice
- Now defaults to 16:9, meaning you can technically hit generate without any parameters now.
- 16:9 shows up greyed out and in the background of the aspect ratio box before you type anything
- New icon- its just the game's logo for now
- Controller mods have moved to a separate repo to make building and forking easier!
- DynamicFPS built in support will be introduced in the next version, hopefully this week!

4.2.2
- Support UI Text Fixes on aspect ratios below 16/9

4.2.1
- Fix an issue where the UI Text fixes would not generate properly.

4.2.0
- Support for 1.2.0 version of TOTK
- Latest fixes from fruithapje21 including text UI element fixes

4.1.1
- Fix an issue where pchtxt doesnt generate properly

4.1.0
- adds support for Colored Dualsense controllers (StavaasEVG)
- Adds preliminary options for more visual fixes. All the code is there, I just need to incorporate the logic for generating the patch file correctly!

4.0.2
- Fix Link stretching in Hestu menu and menu for 1.0.0 thanks to ActualMandM

4.0.1
- Below 16/9 script works again

4.0.0
- No longer relies on Python being installed. It should just work, regardless of what version you have or whether you have it or not (on Windows via the EXE) 
- Includes new tabs to make room for upcoming changes to HUD and Controller customization features, as well as visual mods to be added
- Includes fruithapje21's new script with the mini map fix. No more shifting the main map!!
- Fixes the stretched text in the action guide

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
