import os
import sys
import shutil
import requests
from zipfile import ZipFile
import getpass
import webbrowser
from tkinter import *
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory
import customtkinter
from customtkinter import *
from PIL import Image, ImageTk
import os
from threading import Thread
import getpass
from pathlib import Path
import sys
import shutil
import requests
import psutil

# Define the directory path

username = getpass.getuser()
aar_dir = f'C:\\Users\\{username}\\AppData\\Roaming\\totk-aar'
gui_dir = f'C:\\Users\\{username}\\AppData\\Roaming\\totk-aar\\totk-aar-main'

# Check if the directory exists
if not os.path.exists(aar_dir):
    print(f"Directory '{aar_dir}' does not exist. Creating the directory...")
    os.makedirs(aar_dir)

    # Download the contents of the GitHub repository
    print("Downloading the contents of the GitHub repository...")
    url = 'https://github.com/fayaz12g/totk-aar/archive/main.zip'
    response = requests.get(url)
    
    # Save the downloaded content as a zip file
    zip_file_path = os.path.join(aar_dir, 'totk-aar-main.zip')
    with open(zip_file_path, 'wb') as zip_file:
        zip_file.write(response.content)
    
    # Extract the zip file
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(aar_dir)
    
    # Remove the downloaded zip file
    os.remove(zip_file_path)

# Add the directory to sys.path
sys.path.append(gui_dir)

# Now, you can import GUI
import GUI