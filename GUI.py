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
from extract import extract_blarc
import decompress
from decompress import decompress_zstd
import download
from download import download_extract_copy
import patch
import requests
from tkinter import scrolledtext
import shutil
from tkinter import filedialog
from tkinter import Tk, Button, Label, OptionMenu, StringVar, Entry, Frame, Checkbutton
import ratiotohex
import visuals
from visuals import create_visuals
import extract
import decompress
import patch
from threading import Thread
from tkinter import ttk
import time
import ast
from script import perform_patching
from scriptdeck import perform_deck_patching
import SarcLib
import libyaz0
import ratiotohex
from ratiotohex import calculate_rounded_ratio, convert_asm_to_arm64_hex
from patch import create_patch_files
from tkinter.filedialog import askdirectory
from shutil import copy2
from repack import pack
from repack import pack_folder_to_blarc
from compress import compress_zstd

centered_HUD = False
output_folder = None  
tool_version = "5.4.0"
patch_folder = None 
blyt_folder = None  
open_when_done = False
blarc_file_path = None  
zs_file_path = None  
scaling_factor = 0.0
shadow_quality = "0"
do_disable_fxaa = False
do_disable_fsr = False
do_disable_reduction = False
do_disable_ansiotropic = False
do_disable_dynamicres = False
do_force_trilinear = False
do_cutscene_fix = False
do_staticfps = False
do_DOF = False
do_chuck = False
do_shadowres = False
do_dynamicfps = False
staticfps = "0"

controller_id = "Switch"

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
icon_path = os.path.join(script_directory, 'icon.ico')
dfps_folder = os.path.join(script_directory, "dFPS")

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
    numerator = numerator_entry.get()
    denominator = denominator_entry.get()

    if numerator and denominator:
        numerator = float(numerator)
        denominator = float(denominator)
        ratio = numerator / denominator
    else:
        ratio = 16/9

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
    centered_HUD = False
    center_checkbox.deselect()
    
def disable_fxaa():
    global do_disable_fxaa
    do_disable_fxaa = True
    
def disable_fsr():
    global do_disable_fsr
    do_disable_fsr = True
    
def disable_ansiotropic():
    global do_disable_ansiotropic
    do_disable_ansiotropic = True
    
def open_output():
    global open_when_done
    open_when_done = True

def disable_reduction():
    global do_disable_reduction
    do_disable_reduction = True
    
def apply_chuck():
    global do_chuck
    do_chuck = True
    
def force_trilinear():
    global do_force_trilinear
    do_force_trilinear = True
    
def disable_dynamicres():
    global do_disable_dynamicres
    do_disable_dynamicres = True
    
def apply_dynamicfps():
    global do_dynamicfps
    do_dynamicfps = True
    
def apply_cutscenefix():
    global do_cutscene_fix
    do_cutscene_fix = True
    
def apply_DOF():
    global do_DOF
    do_DOF = True
    
def apply_shadowres():
    global do_shadowres
    shadow_quality = shadow_res_var
    do_shadowres = True
    print("Shadow Resolution is set to " + shadow_quality)

def apply_staticfps():
    global do_staticfps
    do_staticfps = True
    print("Static FPS is set to " + staticfps_var)
    
def update_HUD_location():
    global centered_HUD
    centered_HUD = True
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
    global output_folder
    global zs_file_path
    global centered_HUD
    global zs_file_path
    global shadow_quality
    sys.stdout = PrintRedirector(scrolled_text)
    t = Thread(target=create_full)
    t.start()

def create_full():
    global output_folder
    global zs_file_path
    global centered_HUD
    global shadow_quality
    global staticfps
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
        print("If you are stuck hanging here, be sure to close the emulator first and then hit generate again.")
        shutil.rmtree(folder_to_delete)
        print("Old mod deleted.")
  
    controller_type = controller_type_var.get()
    button_color = button_color_var.get()
    button_layout = button_layout_var.get()
    controller_color = controller_color_var.get()
    staticfpsnew = staticfps_var.get()
    shadow_qualitynew = shadow_res_var.get()
    if staticfpsnew:
        staticfps = staticfps_var.get()
    if shadow_qualitynew:
        shadow_quality = shadow_res_var.get()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if button_layout == "Elden Ring":
        button_layout = "Elden"
    if controller_type == "Switch":
        controller_id = "Switch"
    elif controller_type == "Steam Deck":
        controller_id = f"deck-White-{button_layout}"
    elif controller_type == "Steam":
        controller_id = "steam"
    elif controller_type == "":
        controller_id = "Switch"
    elif controller_type == "Colored Dualsense":
        controller_id = f"dual-{controller_color}"
    else:
        controller_id = f"{controller_type}-{button_color}-{button_layout}"
    download_script_path = os.path.join(script_dir, "download.py")
    download_extract_copy(controller_id, output_folder)
    print("Extracting zip.")
    ratio_value = create_ratio()
    scaling_factor = calculate_ratio()
    blyt_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN", "blyt")
    unpacked_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN")
    visual_fixes = create_visuals(do_dynamicfps, do_disable_fxaa, do_disable_fsr, do_DOF, do_disable_reduction, do_disable_ansiotropic, do_cutscene_fix, do_disable_dynamicres, do_force_trilinear, do_chuck, staticfps, shadow_quality)
    create_patch_files(patch_folder, ratio_value, visual_fixes)
    global dfps_folder
    dfps_output = os.path.join(output_folder, "dFPS")
    if do_dynamicfps:
        if os.path.exists(dfps_output):
            shutil.rmtree(dfps_output)
        print("Copying dynamicFPS mod.")
        shutil.copytree(dfps_folder, dfps_output)
        print("Copied dynamicFPS mod.")
    global zs_file_path
    zs_file_path = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive", "Common.Product.110.Nin_NX_NVN.blarc.zs")
    print("Extracting ZS.")

    if zs_file_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        decompress_script_path = os.path.join(script_dir, "decompress.py")
        decompress_zstd(zs_file_path, output_folder)
        blarc_script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_folder = os.path.join(output_folder, "AAR MOD", "temp")
        print("Extracting BLARC.")
        file = os.path.join(temp_folder, "Common.Product.110.Nin_NX_NVN.blarc")
        blarc_file_path = os.path.join(temp_folder, "Common.Product.110.Nin_NX_NVN.blarc")
        blarc_script_path = os.path.join(script_dir, "extract.py")
        extract_blarc(file, output_folder)
        centered_HUD = str(centered_HUD)  
        scaling_factor = str(scaling_factor)  
        print("Patching BLYT.")
        blarc_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN")
        if float(ratio_value) < 1.7777778:
            print("Using vertical stretch script")
            perform_deck_patching(scaling_factor, centered_HUD, blyt_folder)
        else:
            print("Using horizontal stretch script")
            perform_patching(scaling_factor, centered_HUD, unpacked_folder)
        repack_script_path = os.path.join(script_dir, "repack.py")
        os.remove(file)
        print("Deleted old blarc file.")
        print("Repacking new blarc file. This step may take about 10 seconds")
        pack_folder_to_blarc(blarc_folder, blarc_file_path)
        print("Repacked new blarc file.")
        print("Repacking new zs file.")
        compress_zstd(blarc_file_path)
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
        global open_when_done
        if open_when_done == True:
            print ("Complete! Opening output folder.")
            os.startfile(output_folder)
        else:
            print("Complete! Enjoy the mod.")
    else:
        print("No .zs file selected.")

def handle_focus_in(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.configure(fg='black')

def handle_focus_out(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.configure(fg='gray')

root = Tk()
root.geometry("500x550")
root.title(f"Any Aspect Ratio for Tears of the Kingdom {tool_version}")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

visuals_frame = ttk.Frame(root)
visuals_frame.pack(fill="both", expand=True)
console_label3 = ttk.Label(visuals_frame, text='Enter Aspect Ratio or Screen Dimensions (ex: 21:9 or 3440x1440):')
console_label3.pack(padx=10, pady=10)

visuals_version_label = ttk.Label(visuals_frame, text=f"Tool Version: {tool_version}")

def update_label_position2(event):
    visuals_version_label.place(x=visuals_frame.winfo_width()-10, y=visuals_frame.winfo_height()-10, anchor="se")

visuals_frame.bind("<Configure>", update_label_position2)

frame = Frame(visuals_frame)
frame.pack()

numerator_entry = Entry(frame)
numerator_entry.insert(0, "16")
numerator_entry.configure(fg='gray')
numerator_entry.bind("<FocusIn>", lambda event: handle_focus_in(numerator_entry, "16"))
numerator_entry.bind("<FocusOut>", lambda event: handle_focus_out(numerator_entry, "16"))
numerator_entry.pack(side="left")
numerator_label = Label(frame, text=":")
numerator_label.pack(side="left")
denominator_entry = Entry(frame)
denominator_entry.insert(0, "9")
denominator_entry.configure(fg='gray')
denominator_entry.bind("<FocusIn>", lambda event: handle_focus_in(denominator_entry, "9"))
denominator_entry.bind("<FocusOut>", lambda event: handle_focus_out(denominator_entry, "9"))
denominator_entry.pack(side="left")

cutscene_checkbox_var = tk.BooleanVar()
cutscene_checkbox = Checkbutton(visuals_frame, text="Cutscene Fix", variable=cutscene_checkbox_var, command=apply_cutscenefix)
cutscene_checkbox.pack()

fsr_checkbox_var = tk.BooleanVar()
fsr_checkbox = Checkbutton(visuals_frame, text="Disable FSR", variable=fsr_checkbox_var, command=disable_fsr)
fsr_checkbox.pack()

DOF_checkbox_var = tk.BooleanVar()
DOF_checkbox = Checkbutton(visuals_frame, text="Disable targeting DOF", variable=DOF_checkbox_var, command=apply_DOF)
DOF_checkbox.pack()

chuck_checkbox_var = tk.BooleanVar()
chuck_checkbox = Checkbutton(visuals_frame, text="Use Chuck's 1008p", variable=chuck_checkbox_var, command=apply_chuck)
chuck_checkbox.pack()

fxaa_checkbox_var = tk.BooleanVar()
fxaa_checkbox = Checkbutton(visuals_frame, text="Disable FXAA", variable=fxaa_checkbox_var, command=disable_fxaa)
fxaa_checkbox.pack()

reduction_checkbox_var = tk.BooleanVar()
reduction_checkbox = Checkbutton(visuals_frame, text="Disable LOD Reduction", variable=reduction_checkbox_var, command=disable_reduction)
reduction_checkbox.pack()

ansiotropic_checkbox_var = tk.BooleanVar()
ansiotropic_checkbox = Checkbutton(visuals_frame, text="Disable Ansiotropic", variable=ansiotropic_checkbox_var, command=disable_ansiotropic)
ansiotropic_checkbox.pack()

trilinear_checkbox_var = tk.BooleanVar()
trilinear_checkbox = Checkbutton(visuals_frame, text="Force Trilinear Over Bilinear", variable=trilinear_checkbox_var, command=force_trilinear)
trilinear_checkbox.pack()

dynamicres_checkbox_var = tk.BooleanVar()
dynamicres_checkbox = Checkbutton(visuals_frame, text="Disable Dynamic Resolution", variable=dynamicres_checkbox_var, command=disable_dynamicres)
dynamicres_checkbox.pack()

dynamicfps_checkbox_var = tk.BooleanVar()
dynamicfps_checkbox = Checkbutton(visuals_frame, text="Use Dynamic FPS", variable=dynamicfps_checkbox_var, command=apply_dynamicfps)
dynamicfps_checkbox.pack()

staticfps_label = Label(visuals_frame, text="Static FPS:")
staticfps_label.pack()

staticfps_var = StringVar()

staticfps_label_dropdown = OptionMenu(visuals_frame, staticfps_var, "20", "30", "60")
staticfps_label_dropdown.pack()

shadow_res_label = Label(visuals_frame, text="Shadow Resolution:")
shadow_res_label.pack()

shadow_res_var = StringVar()

shadow_res_dropdown = OptionMenu(visuals_frame, shadow_res_var, "8", "16", "32", "64", "128", "256", "512", "1024", "2048")
shadow_res_dropdown.pack()

notebook.add(visuals_frame, text="Visuals")

controllers_frame = ttk.Frame(root)
controllers_frame.pack(fill="both", expand=True)
content2_frame = ttk.Frame(controllers_frame)
content2_frame.pack(padx=10, pady=10)

controller_type_var = StringVar()
button_color_var = StringVar()
controller_color_var = StringVar()
button_layout_var = StringVar()

controller_frame = Frame(controllers_frame)
controller_frame.pack()

button_frame = Frame(controllers_frame)
button_frame.pack()

controller_version_label = ttk.Label(controllers_frame, text=f"Tool Version: {tool_version}")

def update_label_position3(event):
    controller_version_label.place(x=controllers_frame.winfo_width()-10, y=controllers_frame.winfo_height()-10, anchor="se")

controller_frame.bind("<Configure>", update_label_position3)

controller_type_label = Label(controller_frame, text="Controller Type:")
controller_type_label.pack(side="left")

controller_type_dropdown = OptionMenu(controller_frame, controller_type_var, "Xbox", "Playstation", "Colored Dualsense", "Switch", "Steam", "Steam Deck")
controller_type_dropdown.pack(side="left")

controller_color_label = Label(button_frame, text="Controller Color:")
controller_color_label.pack(side="left")

controller_color_dropdown = OptionMenu(button_frame, controller_color_var, "Red", "White", "Blue", "Pink", "Purple", "Black")
controller_color_dropdown.pack(side="left")

button_color_label = Label(button_frame, text="Button Color:")
button_color_label.pack(side="left")

button_color_dropdown = OptionMenu(button_frame, button_color_var, "Colored", "White")
button_color_dropdown.pack(side="left")

button_layout_label = Label(button_frame, text="Button Layout:")
button_layout_label.pack(side="left")

button_layout_dropdown = OptionMenu(button_frame, button_layout_var, "Western", "Normal", "PE", "Elden Ring")
button_layout_dropdown.pack(side="left")

notebook.add(controllers_frame, text="Controller")

hud_frame = ttk.Frame(root)
hud_frame.pack(fill="both", expand=True)
content_frame = ttk.Frame(hud_frame)
content_frame.pack(padx=10, pady=10)

hud_label = ttk.Label(content_frame, text='Hud Location:')
hud_label.pack()

hud_version_label = ttk.Label(hud_frame, text=f"Tool Version: {tool_version}")

def update_label_position4(event):
    hud_version_label.place(x=hud_frame.winfo_width()-10, y=hud_frame.winfo_height()-10, anchor="se")

hud_frame.bind("<Configure>", update_label_position4)

center_checkbox_var = tk.BooleanVar()
center_checkbox = Checkbutton(hud_frame, text="Center", variable=center_checkbox_var, command=update_HUD_location)
center_checkbox.pack()

corner_checkbox_var = tk.BooleanVar()
corner_checkbox = Checkbutton(hud_frame, text="Corner", variable=corner_checkbox_var, command=update_corner_location)
corner_checkbox.pack()

notebook.add(hud_frame, text="HUD")

console_frame = ttk.Frame(root)
console_frame.pack(fill="both", expand=True)
console_label = ttk.Label(console_frame, text='Console:')
console_label.pack(padx=10, pady=10)

notebook.add(console_frame, text="Generate")

scrolled_text = scrolledtext.ScrolledText(console_frame, width=55, height=15)
scrolled_text.pack()

emulator_label = Label(console_frame, text="Select your Emulator OR choose a custom output folder, then click Generate.")
emulator_label.pack()

yuzu_checkbox_var = tk.BooleanVar()
yuzu_checkbox = Checkbutton(console_frame, text="Yuzu", variable=yuzu_checkbox_var, command=update_yuzu_location)
yuzu_checkbox.pack(side="top")

ryujinx_checkbox_var = tk.BooleanVar()
ryujinx_checkbox = Checkbutton(console_frame, text="Ryujinx", variable=ryujinx_checkbox_var, command=update_ryujinx_location)
ryujinx_checkbox.pack(side="top")

output_folder_button = Button(console_frame, text="Custom Output Folder", command=select_output_folder)
output_folder_button.pack()
output_folder_button.pack(pady=10)

open_checkbox_var = tk.BooleanVar()
open_checkbox = Checkbutton(console_frame, text="Open Output Folder When Done", variable=open_checkbox_var, command=open_output)
open_checkbox.pack(side="top")

create_patch_button = Button(console_frame, text="Generate", command=create_patch)
create_patch_button.pack()
create_patch_button.pack(pady=5)

console_version_label = ttk.Label(console_frame, text=f"Tool Version: {tool_version}")

def update_label_position4(event):
    console_version_label.place(x=console_frame.winfo_width()-10, y=console_frame.winfo_height()-10, anchor="se")

console_frame.bind("<Configure>", update_label_position4)

credits_frame = ttk.Frame(root)
credits_frame.pack(fill="both", expand=True)
credits_label = ttk.Label(credits_frame, text='Utility created by fayaz\nhttps://ko-fi.com/fayaz12\nyoutube.com/fayaz\n\nBased on\nHUD Fix script by u/fruithapje21 on Reddit\n\nController Mods:\nAlerion921 on Gamebanana')
credits_label.pack(padx=10, pady=10)

notebook.add(credits_frame, text="Credits")

credits_version_label = ttk.Label(credits_frame, text=f"Tool Version: {tool_version}")

def update_label_position4(event):
    credits_version_label.place(x=credits_frame.winfo_width()-10, y=credits_frame.winfo_height()-10, anchor="se")

credits_frame.bind("<Configure>", update_label_position4)

root.iconbitmap(icon_path)
root.mainloop()
