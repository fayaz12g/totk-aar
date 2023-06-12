import os
import getpass
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
import download
import patch
from tkinter import scrolledtext
import shutil
from tkinter import filedialog
from tkinter import Tk, Button, Label, OptionMenu, StringVar, Entry, Frame, Checkbutton
import ratiotohex
import extract
import decompress
import patch
from threading import Thread
from tkinter import ttk

from tkinter.filedialog import askdirectory
from shutil import copy2

centered_HUD = True

output_folder = None  
patch_folder = None 
blyt_folder = None  
blarc_file_path = None  
zs_file_path = None  
scaling_factor = 0.0


class PrintRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert("end", text)
        self.text_widget.see("end")  


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
        scaling_factor = scaling_component / (16 / 9)
    else:
        scaling_factor = (16 / 9) / scaling_component
    return scaling_factor


def create_ratio():
    numerator = float(numerator_entry.get())
    denominator = float(denominator_entry.get())
    ratio = numerator / denominator

    return str(ratio)


def select_zs_file():
    global zs_file_path
    zs_file_path = filedialog.askopenfilename(filetypes=[("ZSTD Files", "*.zs")])


def update_yuzu_location():
    global output_folder
    username = getpass.getuser()
    output_folder = f"C:/Users/{username}/AppData/Roaming/yuzu/load/0100F2C0115B6000"
    ryujinx_checkbox.deselect()


def update_corner_location():
    global centered_HUD
    centered_HUD = not centered_HUD
    center_checkbox.deselect()

def update_HUD_location():
    global centered_HUD
    centered_HUD = centered_HUD
    corner_checkbox.deselect()


def update_ryujinx_location():
    global output_folder
    username = getpass.getuser()
    output_folder = f"C:/Users/{username}/AppData/Roaming/Ryujinx/mods/contents/0100f2c0115b6000"
    yuzu_checkbox.deselect()


def select_output_folder():
    global output_folder
    global patch_folder
    output_folder = askdirectory()
    if output_folder:
        patch_folder = os.path.join(output_folder, "AAR MOD", "exefs")
        try:
            os.makedirs(output_folder, exist_ok=True)
            Path(patch_folder).mkdir(parents=True, exist_ok=True) 
        except Exception as e:
            return
    else:
        return


def create_patch():
    t = Thread(target=create_full)
    t.start()


def create_full():
    global output_folder
    global zs_file_path
    global centered_HUD
    sys.stdout = PrintRedirector(scrolled_text)
    if output_folder:
        patch_folder = os.path.join(output_folder, "AAR MOD", "exefs")
        try:
            os.makedirs(output_folder, exist_ok=True)
            Path(patch_folder).mkdir(parents=True, exist_ok=True) 
        except Exception as e:
            return
    if not output_folder:
        print("Select an emulator or output folder.")
        return
    folder_to_delete = os.path.join(output_folder, "AAR MOD")

    if os.path.exists(folder_to_delete):
        print("Old mod found, deleting.")
        shutil.rmtree(folder_to_delete)
        print("Old mod deleted.")
    print("Downloading zip file. This may take up to 10 seconds.")
  
    controller_type = controller_type_var.get()
    button_color = button_color_var.get()
    button_layout = button_layout_var.get()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if button_layout == "Elden Ring":
        button_layout = "Elden"
    if controller_type == "Switch":
        controller_id = "Switch"
    elif controller_type == "Steam Deck":
        controller_id = f"deck-White-{button_layout}"
    elif controller_type == "Steam":
        controller_id = "steam"
    else:
        controller_id = f"{controller_type}-{button_color}-{button_layout}"
    download_script_path = os.path.join(script_dir, "download.py")
    subprocess.run(["python", download_script_path, controller_id, output_folder])
    print("Controller type is", controller_id)
    print("Extracting zip.")

    patch_script_path = os.path.join(os.path.dirname(__file__), "patch.py")
    ratio_value = create_ratio()
    scaling_factor = calculate_ratio()
    blyt_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN", "blyt")
    patch_args = ["python", patch_script_path, patch_folder, ratio_value]
    run(patch_args, cwd=os.path.dirname(patch_script_path))
    global zs_file_path
    zs_file_path = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive",
                               "Common.Product.110.Nin_NX_NVN.blarc.zs")
    print("Extracting ZS.")

    if zs_file_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        decompress_script_path = os.path.join(script_dir, "decompress.py")
        subprocess.run(["python", decompress_script_path, zs_file_path, output_folder])
        blarc_script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_folder = os.path.join(output_folder, "AAR MOD", "temp")
        print("Extracting BLARC.")
        blarc_file_path = os.path.join(temp_folder, "Common.Product.110.Nin_NX_NVN.blarc")
        blarc_script_path = os.path.join(script_dir, "extract.py")
        subprocess.run(["python", blarc_script_path, blarc_file_path, output_folder])
        centered_HUD = str(centered_HUD)  
        if float(ratio_value) < 16 / 9:
            fruithapje21_script_path = os.path.join(script_dir, "scriptdeck.py")
        else:
            fruithapje21_script_path = os.path.join(script_dir, "script.py")
        scaling_factor = str(scaling_factor)  
        print("Patching BLYT.")
        blarc_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN")
        subprocess.run(["python", fruithapje21_script_path, scaling_factor, centered_HUD, blyt_folder])
        repack_script_path = os.path.join(script_dir, "repack.py")
        os.remove(blarc_file_path)
        print("Deleted old blarc file.")
        print("Repacking new blarc file. This step may take about 10 seconds")
        subprocess.run(["python", repack_script_path, blarc_folder, blarc_file_path])
        print("Repacked new blarc file.")
        print("Repacking new zs file.")
        compress_script_path = os.path.join(script_dir, "compress.py")
        subprocess.run(["python", compress_script_path, blarc_file_path])
        new_source_zs = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN.blarc.zs")
        destination_zs = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive",
                                      "Common.Product.110.Nin_NX_NVN.blarc.zs")
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
root.geometry("600x400")
root.title("Any Aspect Ratio for Tears of the Kingdom")


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

settings_frame = ttk.Frame(root)
settings_frame.pack(fill="both", expand=True)

ratio_label = Label(settings_frame, text="Enter Aspect Ratio or Screen Dimensions (ex: 21:9 or 3440x1440)")
ratio_label.pack()

frame = Frame(settings_frame)
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

controller_frame = Frame(settings_frame)
controller_frame.pack()

button_frame = Frame(settings_frame)
button_frame.pack()

controller_type_label = Label(controller_frame, text="Controller Type:")
controller_type_label.pack(side="left")

controller_type_dropdown = OptionMenu(controller_frame, controller_type_var, "Xbox", "Playstation", "Switch", "Steam", "Steam Deck")
controller_type_dropdown.pack(side="left")

button_color_label = Label(button_frame, text="Button Color:")
button_color_label.pack(side="left")

button_color_dropdown = OptionMenu(button_frame, button_color_var, "Colored", "White")
button_color_dropdown.pack(side="left")

button_layout_label = Label(button_frame, text="Button Layout:")
button_layout_label.pack(side="left")

button_layout_dropdown = OptionMenu(button_frame, button_layout_var, "Western", "Normal", "PE", "Elden Ring")
button_layout_dropdown.pack(side="left")

HUD_label = Label(settings_frame, text="HUD Location:")
HUD_label.pack()

center_checkbox_var = tk.BooleanVar()
center_checkbox = Checkbutton(settings_frame, text="Center", variable=center_checkbox_var, command=update_HUD_location)
center_checkbox.pack()

corner_checkbox_var = tk.BooleanVar()
corner_checkbox = Checkbutton(settings_frame, text="Corner", variable=corner_checkbox_var, command=update_corner_location)
corner_checkbox.pack()

emulator_label = Label(settings_frame, text="Emulator")
emulator_label.pack()

yuzu_checkbox_var = tk.BooleanVar()
yuzu_checkbox = Checkbutton(settings_frame, text="Yuzu", variable=yuzu_checkbox_var, command=update_yuzu_location)
yuzu_checkbox.pack()

ryujinx_checkbox_var = tk.BooleanVar()
ryujinx_checkbox = Checkbutton(settings_frame, text="Ryujinx", variable=ryujinx_checkbox_var, command=update_ryujinx_location)
ryujinx_checkbox.pack()

output_folder_button = Button(settings_frame, text="Custom Output Folder", command=select_output_folder)
output_folder_button.pack()
output_folder_button.pack(pady=3)

create_patch_button = Button(settings_frame, text="Create Patch", command=create_patch)
create_patch_button.pack()
create_patch_button.pack(pady=20)

notebook.add(settings_frame, text="Settings")

credits_frame = ttk.Frame(root)
credits_frame.pack(fill="both", expand=True)
credits_label = ttk.Label(credits_frame, text='Utility created by fayaz\nhttps://ko-fi.com/fayaz12\nyoutube.com/fayaz\n\nBased on\nHUD Fix script by u/fruithapje21 on Reddit\n\nController Mods:\nAlerion921 on Gamebanana')
credits_label.pack(padx=10, pady=10)

notebook.add(credits_frame, text="Credits")

console_frame = ttk.Frame(root)
console_frame.pack(fill="both", expand=True)
console_label = ttk.Label(console_frame, text='Console:')
console_label.pack(padx=10, pady=10)

notebook.add(console_frame, text="Console")

scrolled_text = scrolledtext.ScrolledText(console_frame, width=60, height=20)
scrolled_text.pack()


root.mainloop()
