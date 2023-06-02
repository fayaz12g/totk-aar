import os
from subprocess import run
import struct
import sys
import ctypes
from pathlib import Path
import subprocess
import tkinter as tk
import ratiotohex
import extract
import decompress
import patch
import shutil
from tkinter import filedialog
from tkinter import Tk, Button, Label, OptionMenu, StringVar, Entry, Frame, Checkbutton

from tkinter.filedialog import askdirectory
from shutil import copy2

centered_HUD = True

output_folder = None  # Declare the output_folder as a global variable
patch_folder = None  # Declare the output_folder as a global variable
blyt_folder = None  # Declare the blyt_folder as a global variable
blarc_file_path = None  # Declare the blarc_file_path as a global variable
zs_file_path = None  # Declare the zs_file_path as a global variable
scaling_factor = 0.0

def calculate_ratio():
    numerator_entry_value = numerator_entry.get()
    if not numerator_entry_value:
        print("Numerator value is empty. Please provide a valid number.")
        return

    try:
        numerator = float(numerator_entry_value)
    except ValueError:
        print("Invalid numerator value. Please provide a valid number.")
        return

    denominator = float(denominator_entry.get())

    if denominator == 0:
        print("Denominator value cannot be zero.")
        return

    scaling_component = numerator / denominator
    if scaling_component < 16 / 9:
        scaling_factor = scaling_component / (16/9)
    else:
        scaling_factor = (16/9) / scaling_component
    return scaling_factor

def create_ratio():
    numerator = float(numerator_entry.get())
    denominator = float(denominator_entry.get())
    ratio = numerator / denominator

    return str(ratio)

def select_zs_file():
    global zs_file_path
    zs_file_path = filedialog.askopenfilename(filetypes=[("ZSTD Files", "*.zs")])

def update_HUD_location():
    global centered_HUD
    centered_HUD = centered_HUD
    corner_checkbox.deselect()

def update_corner_location():
    global centered_HUD
    centered_HUD = not centered_HUD
    center_checkbox.deselect()

def select_output_folder():
    global output_folder
    global patch_folder
    output_folder = askdirectory()
    if output_folder:
        patch_folder = os.path.join(output_folder, "AAR MOD", "exefs")
        try:
            os.makedirs(output_folder, exist_ok=True)
            Path(patch_folder).mkdir(parents=True, exist_ok=True)  # Create the exefs folder
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
            return
        status_label.config(text=f"Output folder selected: {output_folder}")
    else:
        status_label.config(text="No output folder selected.")

def create_patch():
    global output_folder
    global zs_file_path
    global centered_HUD

    if not output_folder:
        print("Select an output folder.")
        return

    controller_type = controller_type_var.get()
    button_color = button_color_var.get()
    button_layout = button_layout_var.get()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    controller_id = f"{controller_type}-{button_color}-{button_layout}"
    download_script_path = os.path.join(script_dir, "download.py")
    subprocess.run(["python", download_script_path, controller_id, output_folder])

    patch_script_path = os.path.join(os.path.dirname(__file__), "patch.py")
    ratio_value = create_ratio()
    scaling_factor = calculate_ratio()
    blyt_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN", "blyt")
    patch_args = ["python", patch_script_path, patch_folder, ratio_value]
    run(patch_args, cwd=os.path.dirname(patch_script_path))
    global zs_file_path
    zs_file_path = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive", "Common.Product.110.Nin_NX_NVN.blarc.zs")

    if zs_file_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        decompress_script_path = os.path.join(script_dir, "decompress.py")
        subprocess.run(["python", decompress_script_path, zs_file_path, output_folder])
        blarc_script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_folder = os.path.join(output_folder, "AAR MOD", "temp")
        blarc_file_path = os.path.join(temp_folder, "Common.Product.110.Nin_NX_NVN.blarc")
        blarc_script_path = os.path.join(script_dir, "extract.py")
        subprocess.run(["python", blarc_script_path, blarc_file_path, output_folder])
        centered_HUD = str(centered_HUD)      # Convert centered_HUD to string
        if scaling_factor < 1:
            fruithapje21_script_path = os.path.join(script_dir, "scriptdeck.py")
        else:
            fruithapje21_script_path = os.path.join(script_dir, "script.py")
        scaling_factor = str(scaling_factor)  # Convert scaling_factor to string
        blarc_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN")
        subprocess.run(["python", fruithapje21_script_path, scaling_factor, centered_HUD, blyt_folder])
        repack_script_path = os.path.join(script_dir, "repack.py")
        os.remove(blarc_file_path)
        print("Deleted old blarc file.")
        print("Repacking new blarc file.")
        subprocess.run(["python", repack_script_path, blarc_folder, blarc_file_path])
        print("Repacked new blarc file.")
        print("Repacking new zs file.")
        compress_script_path = os.path.join(script_dir, "compress.py")
        subprocess.run(["python", compress_script_path, blarc_file_path])
        new_source_zs = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN.blarc.zs")
        destination_zs = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive", "Common.Product.110.Nin_NX_NVN.blarc.zs")
        print("Repacked new zs file.")
        os.remove(destination_zs)
        destination_directory = os.path.dirname(destination_zs)
        os.makedirs(destination_directory, exist_ok=True)
        shutil.copy2(new_source_zs, destination_zs)
        print("Copied new zs file to mod.")
        shutil.rmtree(temp_folder)
        print("Removed temp folder.")
        print("Complete! Enjoy the mod.")

    else:
        print("No .zs file selected.")



root = Tk()
root.geometry("500x400")
root.title("Any Aspect Ratio for Tears of the Kingdom")

ratio_label = Label(root, text="Enter Aspect Ratio or Screen Dimensions (ex: 21:9 or 3440x1440)")
ratio_label.pack()

frame = Frame(root)
frame.pack()

numerator_entry = Entry(frame)
numerator_entry.pack(side="left")
numerator_label = Label(frame, text=":")
numerator_label.pack(side="left")
denominator_entry = Entry(frame)
denominator_entry.pack(side="left")

controller_type_var = StringVar()
button_color_var = StringVar()
button_layout_var = StringVar()

controller_type_label = Label(root, text="Controller Type:")
controller_type_label.pack()

controller_type_dropdown = OptionMenu(root, controller_type_var, "Xbox", "Playstation")
controller_type_dropdown.pack()

button_color_label = Label(root, text="Button Color:")
button_color_label.pack()

button_color_dropdown = OptionMenu(root, button_color_var, "Colored", "White")
button_color_dropdown.pack()

button_layout_label = Label(root, text="Button Layout:")
button_layout_label.pack()

button_layout_dropdown = OptionMenu(root, button_layout_var, "Western", "Normal", "PE", "Elden Ring")
button_layout_dropdown.pack()

# Add the following later using the StavaasEVG mod
controller_color_var = StringVar()
controller_color_label = Label(root, text="Controller Color:")
controller_color_dropdown = OptionMenu(root, controller_color_var, "Black", "White", "Red", "Blue", "Pink", "Purple")

HUD_label = Label(root, text="HUD Location:")
HUD_label.pack()

center_checkbox_var = tk.BooleanVar()
center_checkbox = Checkbutton(root, text="Center", variable=center_checkbox_var, command=update_HUD_location)
center_checkbox.pack()

corner_checkbox_var = tk.BooleanVar()
corner_checkbox = Checkbutton(root, text="Corner", variable=corner_checkbox_var, command=update_corner_location)
corner_checkbox.pack()

output_folder_button = Button(root, text="Select Output Folder", command=select_output_folder)
output_folder_button.pack()

create_patch_button = Button(root, text="Create Patch", command=create_patch)
create_patch_button.pack()

root.mainloop()
