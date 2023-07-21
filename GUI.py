import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory
import customtkinter
from PIL import Image, ImageTk
import os
from threading import Thread
import getpass
from pathlib import Path
import sys
import shutil
from download import download_extract_copy
from visuals import create_visuals
from patch import create_patch_files
from custominiscript import create_custom_ini
from decompress import decompress_zstd
from compress import compress_zstd
from extract import extract_blarc
from scriptdeck import perform_deck_patching
from script import perform_patching
from repack import pack_folder_to_blarc

###############################################
###########    GLOBAL SETTINGS      ###########
###############################################
tool_version = "dev"

root = customtkinter.CTk()
root.title(f"Any Aspect Ratio {tool_version} Settings")
root.geometry("500x780")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")  

notebook = customtkinter.CTkTabview(root, width=10, height=10)

# Visuals
ar_numerator = StringVar(value="16")
ar_denominator = StringVar(value="9")
do_cutscene_fix = BooleanVar()
do_disable_fsr = BooleanVar()
do_DOF = BooleanVar()
do_chuck = BooleanVar()
do_disable_fxaa = BooleanVar()
do_disable_reduction = BooleanVar()
do_disable_ansiotropic = BooleanVar()
do_force_trilinear = BooleanVar()
do_disable_dynamicres = BooleanVar()
do_dynamicfps = BooleanVar(value=True)
custom_fps = StringVar()
custom_shadow = StringVar()
custom_height = StringVar(value="1080")
custom_width = StringVar(value="1920")
camera_mod = BooleanVar()

# Controller
controller_types = ["Xbox", "Playstation", "Colored Dualsense", "Switch", "Steam", "Steam Deck"]

full_button_layouts = ["Western", "Normal", "PE", "Elden Ring"]
default_button_layouts = ["Normal"]

dualsense_colors = ["Red", "White", "Blue", "Pink", "Purple", "Black"]
default_colors = ["Black"]

colored_button_colors = ["Colored", "Monochrome"]
default_button_colors = ["Monochrome"]

controller_type = StringVar(value="Switch")
button_color = StringVar()
controller_color = StringVar()
button_layout = StringVar()

# HUD
centered_HUD = BooleanVar()
corner_HUD = BooleanVar(value=True)
expand_shutter = BooleanVar()

# Generation
output_yuzu = BooleanVar()
output_ryujinx = BooleanVar()
open_when_done = BooleanVar()

output_folder = None

do_custom_ini = False
zs_file_path = None

image_name = "switch_normal.jpeg"
controller_layout_label = ""
normal__xbox_layout = "Normal Layout:  A > B, B > A , X > Y, Y > X"
PE__xbox_layout = "PE Layout: A > A, B > B, X > X, Y > Y"
western_xbox_layout = "Western Layout: B > A,  A > B, X > X, Y > Y"
elden_xbox_layout = "Elden Ring Layout: A > Y, B > B, Y > A,  X > X"
normal__dual_layout = "Normal Layout:  A > Circle, B > Cross, X > Triangle, Y > Square"
PE__dual_layout = "PE Layout: B > Circle, A > Cross, Y > Triangle, X > Square"
western_dual_layout = "Western Layout: B  > Circle,  A > Cross, X > Triangle, Y > Square"
elden_dual_layout = "Elden Ring Layout: A > Triangle,  B > Square, X > Circle, Y > Cross"

patch_folder = None
blyt_folder = None

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
icon_path = os.path.join(script_directory, 'icon.ico')
dfps_folder = os.path.join(script_directory, "dFPS")
dfps_ini_folder = os.path.join(script_directory, "customini", "dfps")

root.iconbitmap(icon_path)

################################################
###########    HELPER FUNCTIONS      ###########
################################################

class PrintRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert("end", text)
        self.text_widget.see("end")  

def handle_focus_in(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.configure(text_color='white')

def handle_focus_out(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.configure(text_color='gray')

def update_values(*args):
    global do_custom_ini
    do_custom_ini = True
    print (f"New values:{custom_width.get()} {custom_height.get()} {custom_fps.get()} {custom_shadow.get()}")

# def change_menu(list, option_menu, option_var):
#     option_menu['menu'].delete(0, 'end')
#     for option in list:
#         option_menu['menu'].add_command(label=option, command=tk._setit(option_var, option))
#     option_var.set(list[0])

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

def create_ratio():
    numerator = ar_numerator.get()
    denominator = ar_denominator.get()

    if numerator and denominator:
        numerator = float(numerator)
        denominator = float(denominator)
        ratio = numerator / denominator
    else:
        ratio = 16/9

    return str(ratio)

def calculate_ratio():
    numerator_entry_value = ar_numerator.get()
    if not numerator_entry_value:
        print("Numerator value is empty. Please provide a valid number.")
        return

    try:
        numerator = float(numerator_entry_value)
    except ValueError:
        print("Invalid numerator value. Please provide a valid number.")
        return

    denominator = float(ar_denominator.get())

    if denominator == 0:
        print("Denominator value cannot be zero.")
        return

    scaling_component = numerator / denominator
    if scaling_component < 16 / 9:
        scaling_factor = scaling_component / (16 / 9)
    else:
        scaling_factor = (16 / 9) / scaling_component
    return scaling_factor

def create_patch():
    global output_folder
    global zs_file_path
    global zs_file_path
    sys.stdout = PrintRedirector(scrolled_text)
    t = Thread(target=create_full)
    t.start()

def create_full():
    global output_folder
    global zs_file_path

    progressbar.start()

    username = getpass.getuser()
    if output_yuzu.get() is True:
        output_folder = f"C:/Users/{username}/AppData/Roaming/yuzu/load/0100F2C0115B6000"
    if output_ryujinx.get() is True:
        output_folder = f"C:/Users/{username}/AppData/Roaming/Ryujinx/mods/contents/0100f2c0115b6000"

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

    progressbar.set(.05)

    if os.path.exists(folder_to_delete):
        print("Old mod found, deleting.")
        print("If you are stuck hanging here, be sure to close the emulator first and then hit generate again.")
        shutil.rmtree(folder_to_delete)
        print("Old mod deleted.")
  
    progressbar.set(.1)

    global controller_type
    global button_color
    global button_layout
    global controller_color
    controller_type = controller_type.get()
    button_color = button_color.get()
    button_layout = button_layout.get()
    controller_color = controller_color.get()
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
    progressbar.set(.15)
    download_extract_copy(controller_id, output_folder)
    progressbar.set(.25)
    print("Extracting zip.")
    ratio_value = create_ratio()
    scaling_factor = calculate_ratio()
    unpacked_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN")
    visual_fixes = create_visuals(do_dynamicfps.get(), do_disable_fxaa.get(), do_disable_fsr.get(), do_DOF.get(), do_disable_reduction.get(), do_disable_ansiotropic.get(), do_cutscene_fix.get(), do_disable_dynamicres.get(), do_force_trilinear.get(), do_chuck.get())
    create_patch_files(patch_folder, ratio_value, visual_fixes)
    global dfps_folder
    global do_custom_ini
    global dfps_ini_folder
    dfps_default_ini = os.path.join(dfps_ini_folder, "default.ini")
    dfps_output = os.path.join(output_folder, "dFPS")
    dfps_ini_output = os.path.join(output_folder, "AAR MOD", "romfs")
    dfps_default_output = os.path.join(dfps_ini_output, "dfps")
    if do_dynamicfps.get():
        if os.path.exists(dfps_output):
            shutil.rmtree(dfps_output)
        print("Copying dynamicFPS mod.")
        shutil.copytree(dfps_folder, dfps_output)
        print("Copied dynamicFPS mod.")
        if os.path.exists(dfps_default_output):
            shutil.rmtree(dfps_default_output)
        shutil.copy2(dfps_default_ini, dfps_default_output)
        if do_custom_ini == True:
            print("Creating custom ini")
            create_custom_ini(custom_width.get(), custom_height.get(), custom_shadow.get(), custom_fps.get(), str(camera_mod.get()), dfps_ini_output)
    progressbar.set(.3)
    global zs_file_path
    zs_file_path = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive", "Common.Product.110.Nin_NX_NVN.blarc.zs")
    print("Extracting ZS.")

    if zs_file_path:
        decompress_zstd(zs_file_path, output_folder)
        progressbar.set(.35)
        temp_folder = os.path.join(output_folder, "AAR MOD", "temp")
        print("Extracting BLARC.")
        file = os.path.join(temp_folder, "Common.Product.110.Nin_NX_NVN.blarc")
        blarc_file_path = os.path.join(temp_folder, "Common.Product.110.Nin_NX_NVN.blarc")
        extract_blarc(file, output_folder)
        progressbar.set(.5)
        scaling_factor = str(scaling_factor)  
        print("Patching BLYT.")
        blarc_folder = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN")
        if float(ratio_value) < 1.7777778:
            print("Using vertical stretch script")
            perform_deck_patching(scaling_factor, str(centered_HUD.get()), unpacked_folder)
        else:
            print("Using horizontal stretch script")
            perform_patching(scaling_factor, str(centered_HUD.get()), unpacked_folder, str(expand_shutter.get()))
        os.remove(file)
        print("Deleted old blarc file.")
        print("Repacking new blarc file. This step may take about 10 seconds")
        progressbar.set(.75)
        pack_folder_to_blarc(blarc_folder, blarc_file_path)
        progressbar.set(.9)
        print("Repacked new blarc file.")
        print("Repacking new zs file.")
        compress_zstd(blarc_file_path)
        progressbar.set(.95)
        new_source_zs = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN.blarc.zs")
        destination_zs = os.path.join(output_folder, "AAR MOD", "romfs", "UI", "LayoutArchive", "Common.Product.110.Nin_NX_NVN.blarc.zs")
        print("Repacked new zs file.")
        os.remove(destination_zs)
        destination_directory = os.path.dirname(destination_zs)
        os.makedirs(destination_directory, exist_ok=True)
        shutil.copy2(new_source_zs, destination_zs)
        print("Copied new zs file to mod.")
        shutil.rmtree(temp_folder)
        progressbar.stop()
        progressbar.set(1)
        print("Removed temp folder.")
        if open_when_done.get() == True:
            print ("Complete! Opening output folder.")
            os.startfile(output_folder)
        else:
            print("Complete! Enjoy the mod.")
    else:
        print("No .zs file selected.")


################################
####### Layout Mangement #######
################################

def pack_widgets():
    notebook.pack(padx=10, pady=10)

    console_label3.pack(padx=10, pady=10)

    frame.pack()

    numerator_entry.pack(side="left")
    aspect_ratio_divider.pack(side="left")
    denominator_entry.pack(side="left")
    
    cutscene_checkbox.pack(padx=5, pady=5)
    fsr_checkbox.pack(padx=5, pady=5)
    DOF_checkbox.pack(padx=5, pady=5)
    chuck_checkbox.pack(padx=5, pady=5)
    fxaa_checkbox.pack(padx=5, pady=5)
    reduction_checkbox.pack(padx=5, pady=5)
    ansiotropic_checkbox.pack(padx=5, pady=5)
    trilinear_checkbox.pack(padx=5, pady=5)
    dynamicres_checkbox.pack(padx=5, pady=5)
    dynamicfps_label.pack(pady=(20, 0))
    dynamicfps_checkbox.pack()

    frame2.pack()

    if do_dynamicfps.get() is True:
        resolution_label.pack(pady=(10, 0))
        res_numerator_entry.pack(side="left")
        res_numerator_label.pack(side="left")
        res_denominator_entry.pack(side="left")
        shadow_label.pack()
        shadow_entry.pack()
        FPS_label.pack()
        FPS_entry.pack()
        camera_checkbox.pack(pady=10)

    image_label.pack()

    image_layout_label.pack(padx=5, pady=5)
    
    controller_type_label.pack()
    controller_type_dropdown.pack()

    controller_color_label.pack()
    controller_color_dropdown.pack()
    
    button_color_label.pack()
    button_color_dropdown.pack()

    button_layout_label.pack()
    button_layout_dropdown.pack()

    content_frame.pack(padx=10, pady=10)

    hud_label.pack()
    center_checkbox.pack()
    corner_checkbox.pack(padx=10, pady=10) 
    shutter_checkbox.pack(padx=20, pady=20)

    emulator_label.pack(pady=10)
    yuzu_checkbox.pack(side="top")
    ryujinx_checkbox.pack(side="top")

    output_folder_button.pack()
    output_folder_button.pack(pady=10)

    open_checkbox.pack(pady=10, side="top")

    create_patch_button.pack(pady=15)

    console_label.pack(padx=10, pady=5)
    scrolled_text.pack()

    progressbar.pack(pady=5)

    credits_label.pack(padx=20, pady=50)


def forget_packing():
    notebook.pack_forget()

    console_label3.pack_forget()

    frame.pack_forget()

    numerator_entry.pack_forget()
    aspect_ratio_divider.pack_forget()
    denominator_entry.pack_forget()
    
    cutscene_checkbox.pack_forget()
    fsr_checkbox.pack_forget()
    DOF_checkbox.pack_forget()
    chuck_checkbox.pack_forget()
    fxaa_checkbox.pack_forget()
    reduction_checkbox.pack_forget()
    ansiotropic_checkbox.pack_forget()
    trilinear_checkbox.pack_forget()
    dynamicres_checkbox.pack_forget()
    dynamicfps_label.pack_forget()
    dynamicfps_checkbox.pack_forget()

    frame2.pack_forget()

    resolution_label.pack_forget()
    res_numerator_entry.pack_forget()
    res_numerator_label.pack_forget()
    res_denominator_entry.pack_forget()
    shadow_label.pack_forget()
    shadow_entry.pack_forget()
    FPS_label.pack_forget()
    FPS_entry.pack_forget()
    camera_checkbox.pack_forget()

    master=notebook.tab("Controller").pack_forget()
    image_label.pack_forget()
    image_layout_label.pack_forget()
    
    controller_type_label.pack_forget()
    controller_type_dropdown.pack_forget()
    
    controller_color_label.pack_forget()
    controller_color_dropdown.pack_forget()
    
    button_color_label.pack_forget()
    button_color_dropdown.pack_forget()

    button_layout_label.pack_forget()
    button_layout_dropdown.pack_forget()

    master=notebook.tab("HUD").pack_forget()

    content_frame.pack_forget()

    hud_label.pack_forget()
    center_checkbox.pack_forget()
    corner_checkbox.pack_forget()
    shutter_checkbox.pack_forget()

    master=notebook.tab("Generate").pack_forget()

    emulator_label.pack_forget()
    yuzu_checkbox.pack_forget()
    ryujinx_checkbox.pack_forget()

    output_folder_button.pack_forget()
    output_folder_button.pack_forget()

    open_checkbox.pack_forget()

    create_patch_button.pack_forget()
    create_patch_button.pack_forget()

    console_label.pack_forget()
    scrolled_text.pack_forget()

    progressbar.pack_forget()

    credits_label.pack_forget()

def repack_widgets(*args):
    forget_packing()
    pack_widgets()


notebook.add("Visuals")
notebook.add("Controller")
notebook.add("HUD")
notebook.add("Generate")
notebook.add("Credits")

#######################
####### Visuals #######
#######################

console_label3= customtkinter.CTkLabel(master=notebook.tab("Visuals"), text='Enter Aspect Ratio or Screen Dimensions (ex: 21:9 or 3440x1440):')

frame = customtkinter.CTkFrame(master=notebook.tab("Visuals"))

numerator_entry = customtkinter.CTkEntry(frame, textvariable=ar_numerator)
numerator_entry.configure(text_color='gray')
numerator_entry.bind("<FocusIn>", lambda event: handle_focus_in(numerator_entry, "16"))
numerator_entry.bind("<FocusOut>", lambda event: handle_focus_out(numerator_entry, "16"))
aspect_ratio_divider= customtkinter.CTkLabel(frame, text=":")
denominator_entry = customtkinter.CTkEntry(frame, textvariable=ar_denominator)
denominator_entry.configure(text_color='gray')
denominator_entry.bind("<FocusIn>", lambda event: handle_focus_in(denominator_entry, "9"))
denominator_entry.bind("<FocusOut>", lambda event: handle_focus_out(denominator_entry, "9"))

cutscene_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Cutscene FPS Fix", variable=do_cutscene_fix)
fsr_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Disable FSR", variable=do_disable_fsr)
DOF_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Disable Targeting DOF", variable=do_DOF)
chuck_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Use Chuck's 1008p", variable=do_chuck)
fxaa_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Disable FXAA", variable=do_disable_fxaa)
reduction_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Disable LOD Reduction", variable=do_disable_reduction)
ansiotropic_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Anisotropic Filtering Fix", variable=do_disable_ansiotropic)
trilinear_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Force Trilinear Over Bilinear", variable=do_force_trilinear)
dynamicres_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Disable Dynamic Resolution", variable=do_disable_dynamicres)

dynamicfps_label= customtkinter.CTkLabel(master=notebook.tab("Visuals"), text="DynamicFPS Settings:")
dynamicfps_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Use Dynamic FPS", variable=do_dynamicfps, command=repack_widgets)

frame2 = customtkinter.CTkFrame(master=notebook.tab("Visuals"))

resolution_label= customtkinter.CTkLabel(frame2, text="Custom Resolution:")

res_numerator_entry = customtkinter.CTkEntry(frame2, textvariable=custom_height)
res_numerator_entry.configure(text_color='gray')
res_numerator_entry.bind("<FocusIn>", lambda event: handle_focus_in(res_numerator_entry, "1080"))
res_numerator_entry.bind("<FocusOut>", lambda event: handle_focus_out(res_numerator_entry, "1080"))

res_numerator_label= customtkinter.CTkLabel(frame2, text="x")

res_denominator_entry = customtkinter.CTkEntry(frame2, textvariable=custom_width)
res_denominator_entry.configure(text_color='gray')
res_denominator_entry.bind("<FocusIn>", lambda event: handle_focus_in(res_denominator_entry, "1920"))
res_denominator_entry.bind("<FocusOut>", lambda event: handle_focus_out(res_denominator_entry, "1920"))

shadow_label= customtkinter.CTkLabel(master=notebook.tab("Visuals"), text="Custom Shadow Resolution (Set to -1 to scale to resolution):")
shadow_entry = customtkinter.CTkEntry(master=notebook.tab("Visuals"), textvariable=custom_shadow)

FPS_label= customtkinter.CTkLabel(master=notebook.tab("Visuals"), text="Custom FPS:")
FPS_entry = customtkinter.CTkEntry(master=notebook.tab("Visuals"), textvariable=custom_fps)

camera_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Increase Camera Quality", variable=camera_mod)

custom_fps.trace("w", update_values)
custom_shadow.trace("w", update_values)
custom_width.trace("w", update_values)
custom_height.trace("w", update_values)  

##########################
####### Controller #######
##########################

def select_controller(event):
    selected_controller_type = controller_type.get().lower()
    selected_controller_color = controller_color.get().lower()
    selected_button_color = button_color.get().lower()
    selected_button_layout = button_layout.get().lower()

    global image_name
    if selected_controller_type == "colored dualsense":
        if selected_controller_color:
            image_name = f"dual_{selected_controller_color}.jpeg"
        else:
            image_name = f"dual_black.jpeg"
    elif selected_controller_type == "xbox":
        if selected_button_layout:
            image_name = f"xbox_{selected_button_layout}.jpeg"
        else:
            image_name = f"xbox_normal.jpeg"
    elif selected_controller_type == "playstation":
        if selected_button_layout:
            image_name = f"dual_{selected_button_layout}.jpeg"
        else:
            image_name = f"dual_normal.jpeg"
    elif selected_controller_type == "switch":
        image_name = "switch_normal.jpeg"
    elif selected_controller_type == "steam deck":
        if selected_button_layout == "normal":
            image_name = "deck_normal.jpeg"
        else:
            image_name = "deck_western.jpeg"
    elif selected_controller_type == "steam":
        image_name = "steam_pe.jpeg"
    else:
        image_name = "switch_normal.jpeg"

    if selected_button_layout == "elden ring":
        image_name = image_name.replace("elden ring", "elden")
        if selected_controller_type == "playstation":
            controller_layout_label = elden_dual_layout
        else:
            controller_layout_label = elden_xbox_layout
    if selected_button_layout == "western":
        if selected_controller_type == "playstation":
            controller_layout_label = western_dual_layout
        else:
            controller_layout_label = western_xbox_layout
    if selected_button_layout == "PE":
        if selected_controller_type == "playstation":
            controller_layout_label = PE__dual_layout
        else:
            controller_layout_label = PE__xbox_layout
    if selected_button_layout == "normal":
        if selected_controller_type == "playstation":
            controller_layout_label = normal__dual_layout
        else:
            controller_layout_label = normal__xbox_layout

    image_path = os.path.join(script_directory, "images", image_name)
    
    # Load and display the image
    image = Image.open(image_path)
    image = image.resize((500, 300))  # Adjust the size as needed
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo  # Keep a reference to the photo to prevent garbage collection
    print(f"Controller image set to {image_name}")
    image_label.update()

    # controller = controller_type.get()

    # if controller == "Xbox" or controller == "Playstation" or controller == "Steam Deck":
    #     change_menu(full_button_layouts, button_layout_dropdown, button_layout)
        
    # else:
    #     change_menu(default_button_layouts, button_layout_dropdown, button_layout)

    # if controller == "Colored Dualsense":
    #     change_menu(dualsense_colors, controller_color_dropdown, controller_color)
    # else:
    #     change_menu(default_colors, controller_color_dropdown, controller_color)

    # if controller == "Xbox" or controller == "Playstation":
    #     change_menu(colored_button_colors, button_color_dropdown, button_color)
    # else:
    #     change_menu(default_button_colors, button_color_dropdown, button_color)

image_label= customtkinter.CTkLabel(master=notebook.tab("Controller"))

image_layout_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text=f"{controller_layout_label}", font=("Roboto", 11, "bold"))

controller_type_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Controller Type:")
controller_type_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=controller_type, values=controller_types, command=select_controller)

controller_color_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Controller Color:")
controller_color_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=controller_color, values=default_colors)

button_color_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Button Color:")
button_color_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=button_color, values=colored_button_colors)

button_layout_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Button Layout:")
button_layout_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=button_layout, values=full_button_layouts)

select_controller("initialize")

###################
####### HUD #######
###################

content_frame = customtkinter.CTkFrame(master=notebook.tab("HUD"))

hud_label= customtkinter.CTkLabel(content_frame, text='Hud Location:')
center_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("HUD"), text="Center", variable=centered_HUD, value=1, command=lambda: [corner_HUD.set(False), repack_widgets])
corner_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("HUD"), text="Corner", variable=corner_HUD, value=2, command=lambda: [centered_HUD.set(False), repack_widgets])
shutter_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("HUD"), text="Expand Shutter Size", variable=expand_shutter)

########################
####### GENERATE #######
########################

emulator_label= customtkinter.CTkLabel(master=notebook.tab("Generate"), text="Select your Emulator OR choose a custom output folder, then click Generate.")
yuzu_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("Generate"), text="Yuzu", value=1, variable=output_yuzu, command=lambda: [output_ryujinx.set(False), repack_widgets])
ryujinx_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("Generate"), text="Ryujinx", value=2, variable=output_ryujinx, command=lambda: [output_yuzu.set(False), repack_widgets])   

output_folder_button = customtkinter.CTkButton(master=notebook.tab("Generate"), text="Custom Output Folder", fg_color="gray", hover_color="black", command=select_output_folder)

open_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Generate"), text="Open Output Folder When Done", variable=open_when_done)

create_patch_button = customtkinter.CTkButton(master=notebook.tab("Generate"), text="Generate", command=create_patch)

console_label= customtkinter.CTkLabel(master=notebook.tab("Generate"), text='Console:')
scrolled_text = scrolledtext.ScrolledText(master=notebook.tab("Generate"), width=50, height=22, font=("Helvetica", 10))

progressbar = customtkinter.CTkProgressBar(master=notebook.tab("Generate"), orientation="horizontal")
progressbar.configure(mode="determinate", determinate_speed=.01, progress_color="green", fg_color="lightgreen", height=6, width=400)
progressbar.set(0)

#######################
####### CREDITS #######
#######################

credits_label = customtkinter.CTkLabel(master=notebook.tab("Credits"), text='Utility created by fayaz\nhttps://ko-fi.com/fayaz12\nyoutube.com/fayaz\n\nBased on\nHUD Fix script by u/fruithapje21 on Reddit\n\nController Mods:\nAlerion921 on Gamebanana\nStavaasEVG on Gamebanana\n\nVisual Fixes by\nChuckFeedAndSeed, patchanon, somerandompeople, SweetMini, \ntheboy181, Wollnashorn, and Zeikken on GBAtemp\n\ndFPS Mod by\nu/ChucksFeedAndSeed on reddit')

pack_widgets()

root.mainloop()