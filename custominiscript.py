import sys
import subprocess
import ast
import os

def create_custom_ini(customwidth, customheight, customshadow, customfps, cameramod, customini_output):
    # Convert values to floats or 0 if empty
    customwidth = float(customwidth) if customwidth else 0
    customheight = float(customheight) if customheight else 0
    customshadow = float(customshadow) if customshadow else 0
    customfps = float(customfps) if customfps else 0
    cameramod = str(cameramod)

    # Create the content of the default.ini file
    content = "[dFPS]\n"
    if customfps > 0:
        content += f"MaxFramerate = {int(customfps)}\n"

    content += "\n[Graphics]\n"
    if customwidth > 0 and customheight > 0:
        content += f"ResolutionWidth = {int(customwidth)}\n"
        content += f"ResolutionHeight = {int(customheight)}\n"
    if customshadow > 0 or customshadow == -1:
        content += f"ResolutionShadows = {int(customshadow)}\n"

    content += "\n[Features]\n"
    content += f"EnableCameraQualityImprovement = {cameramod.lower()}\n"
    
    # Create the directories if they don't exist
    dfps_dir = os.path.join(customini_output, "romfs", "dfps")
    os.makedirs(dfps_dir, exist_ok=True)

    # Write the content to the default.ini file
    ini_file_path = os.path.join(customini_output, "romfs", "dfps", "60.ini")
    with open(ini_file_path, "w") as ini_file:
        ini_file.write(content)


