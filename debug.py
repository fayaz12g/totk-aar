import os
from subprocess import run
import struct
import sys
import ctypes
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import Tk, Button, Label, OptionMenu, StringVar, Entry, Frame

from tkinter.filedialog import askdirectory
from shutil import copy2

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
    scaling_factor = (16/9) / scaling_component
    return scaling_factor

def create_ratio():
    numerator = float(numerator_entry.get())
    denominator = float(denominator_entry.get())
    ratio = numerator / denominator

    return str(ratio)

def float_to_hex(f):
    """
    Converts float values into hex, strips the 0x prefix and prepends zeroes to
    always have length 8
    """
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0')


def select_blyt_folder():
    global blyt_folder
    blyt_folder = askdirectory()
    if blyt_folder:
        status_label.config(text=f"BLYT folder selected: {blyt_folder}")
    else:
        status_label.config(text="No BLYT folder selected.")


def select_blarc_file():
    global blarc_file_path
    blarc_file_path = filedialog.askopenfilename(filetypes=[("BLARC Files", "*.blarc")])


def select_zs_file():
    global zs_file_path
    zs_file_path = filedialog.askopenfilename(filetypes=[("ZSTD Files", "*.zs")])


def select_output_folder():
    global output_folder
    global patch_folder
    output_folder = askdirectory()
    if output_folder:
        patch_folder = os.path.join(output_folder, "AAR MOD", "exefs")
        output_folder = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive")
        try:
            os.makedirs(output_folder, exist_ok=True)
            Path(patch_folder).mkdir(parents=True, exist_ok=True)  # Create the exefs folder
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
            return
        status_label.config(text=f"Output folder selected: {output_folder}")
    else:
        status_label.config(text="No output folder selected.")

def generate_mod():
    if not output_folder:
        status_label.config(text="Error: Please select the output folder.")
        return

    if blarc_file_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        extract_script_path = os.path.join(script_dir, "extract.py")

        try:
            subprocess.run(["python", extract_script_path, blarc_file_path, output_folder], check=True)
            print("Extraction completed successfully.")
        except subprocess.CalledProcessError as e:
            print("Extraction failed:", e)
    else:
        print("No BLARC file selected.")

    scaling_factor = calculate_ratio()  # Get the scaling factor from calculate_ratio()

    if not blyt_folder:
        status_label.config(text="Error: Please select the BLYT folder.")
        return

    ratio = calculate_ratio()

    if not os.path.isdir(blyt_folder):
        status_label.config(text="Error: Invalid BLYT folder.")
        return

    destination_blyt_folder = os.path.join(output_folder, "blyt")
    os.makedirs(destination_blyt_folder, exist_ok=True)

    for root, _, files in os.walk(blyt_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_blyt_folder, file)
            copy2(source_path, destination_path)

    status_label.config(text="Output created successfully.")


def convert_mod():
    scaling_factor = calculate_ratio()

    # Make sure scaling_factor is a float
    if not isinstance(scaling_factor, float):
        scaling_factor = float(scaling_factor)

    x = float_to_hex(scaling_factor)

    if not blyt_folder:
        status_label.config(text="Error: Please select the BLYT folder.")
        return

    if not numerator_entry:
        status_label.config(text="Error: Please enter the full aspect ratio.")
        return

    if not denominator_entry:
        status_label.config(text="Error: Please enter the full aspect ratio.")
        return

    if not output_folder:
        status_label.config(text="Error: Please select the output folder.")
        return

    # Use the scaling_factor variable here
    ratio = calculate_ratio()
    scaling_factor = calculate_ratio()
    x = float_to_hex(scaling_factor)

    if not os.path.isdir(blyt_folder):
        status_label.config(text="Error: Invalid BLYT folder.")
        return

    destination_blyt_folder = os.path.join(output_folder, "blyt")
    os.makedirs(destination_blyt_folder, exist_ok=True)

    file_names = os.listdir(blyt_folder)
    file_names = [name for name in file_names if name.startswith('blyt')]
    file_names = [name[4:] for name in file_names]  # Remove the "blyt" prefix

    for name in file_names:
        source_path = os.path.join(blyt_folder, f'blyt{name}')
        destination_path = os.path.join(destination_blyt_folder, name)
        copy2(source_path, destination_path)

    # Get the full path to script.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "script.py")

    # Pass the ratio value to script.py using subprocess
    subprocess.run(["python", script_path, str(ratio), destination_blyt_folder])


def decompress_zstd():
    if zs_file_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        decompress_script_path = os.path.join(script_dir, "decompress.py")
        subprocess.run(["python", decompress_script_path, zs_file_path])
    else:
        print("No .zs file selected.")

def create_patch():
    if not output_folder:
        status_label.config(text="Error: Please select the output folder.")
        return
    
    patch_script_path = os.path.join(os.path.dirname(__file__), "patch.py")
    ratio_value = create_ratio()  # Obtain the ratio value as a string
    print(ratio_value)
    patch_args = ["python", patch_script_path, patch_folder, ratio_value, version_variable.get()]
    run(patch_args, cwd=os.path.dirname(patch_script_path))


root = Tk()
root.geometry("500x350")
root.title("Any Aspect Ratio for Tears of the Kingdom")

blyt_folder_button = Button(root, text="Select blyt Folder", command=select_blyt_folder)
blyt_folder_button.pack()

# Create a button for selecting the BLARC file
select_blarc_button = tk.Button(root, text="Select BLARC File", command=select_blarc_file)
select_blarc_button.pack()

# Create a button for selecting the ZSTD file
select_zs_button = tk.Button(root, text="Select ZSTD File", command=select_zs_file)
select_zs_button.pack()

version_options = ['1.0.0', '1.1.0', '1.1.1', '1.1.2']
version_variable = StringVar(root)
version_variable.set('1.0.0')

version_label = Label(root, text="Select Game Version:")
version_label.pack()

version_menu = OptionMenu(root, version_variable, *version_options)
version_menu.pack()

ratio_label = Label(root, text="Enter Aspect Ratio:")
ratio_label.pack()

frame = Frame(root)
frame.pack()

numerator_entry = Entry(frame)
numerator_entry.pack(side="left")
numerator_label = Label(frame, text=":")
numerator_label.pack(side="left")
denominator_entry = Entry(frame)
denominator_entry.pack(side="left")

output_folder_button = Button(root, text="Select Output Folder", command=select_output_folder)
output_folder_button.pack()

generate_button = Button(root, text="Generate Mod", command=generate_mod)
generate_button.pack()

convert_button = Button(root, text="Convert Mod", command=convert_mod)
convert_button.pack()

create_patch_button = Button(root, text="Create Patch", command=create_patch)
create_patch_button.pack()

decompress_button = Button(root, text="Decompress ZSTD", command=decompress_zstd)
decompress_button.pack()

status_label = Label(root, text="Select BLYT and Output folders.")
status_label.pack()

root.mainloop()
