import os
import sys
import subprocess
import shutil

def install_dependencies():
    """
    Install the required dependencies.
    """
    dependencies = ["sarc", "libyaz0"]
    try:
        subprocess.run(["pip", "install"] + dependencies, check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Dependency installation failed:", e)

def compress(folder_path, output_file):
    """
    Compress the given folder into a BLARC archive.
    """
    try:
        subprocess.run(["sarc", "-c", folder_path, output_file], check=True)
        print("Compression completed successfully.")
    except FileNotFoundError:
        print("sarc-tool is not installed. Please install it manually.")
    except subprocess.CalledProcessError as e:
        print("Compression failed:", e)

def main(blarc_file_path, folder_path):
    if not os.path.isfile(blarc_file_path):
        print("Invalid BLARC file path.")
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    output_file = os.path.join(folder_path, "output.blarc")
    compress(folder_path, output_file)

    # Delete the compressed folder
    shutil.rmtree(folder_path)
    print("Compressed folder deleted.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python compress.py <blarc_file_path> <folder_path>")
        sys.exit(1)

    blarc_file_path = sys.argv[1]
    folder_path = sys.argv[2]

    install_dependencies()
    main(blarc_file_path, folder_path)
