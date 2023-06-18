import os
import sys
import subprocess
import requests
import sys



def install_required_packages():
    required_packages = ["requests", "zipfile"]

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} package not found. Installing...")
            subprocess.run(["pip", "install", package])

def download_extract_copy(controller_id, output_folder):
    import requests
    import zipfile
    import shutil

    # URL of the ZIP file
    zip_url = f"https://github.com/fayaz12g/totk-aar/raw/main/controllers/{controller_id}.zip"

    # Download the ZIP file
    print("Controller type is", controller_id)
    print("Downloading zip file. This may take up to 10 seconds.")
    response = requests.get(zip_url)
    zip_file_path = os.path.join(output_folder, f"{controller_id}.zip")
    with open(zip_file_path, "wb") as file:
        file.write(response.content)

    # Extract the ZIP file
    print("Extracting zip file")
    extract_folder = os.path.join(output_folder, "AAR MOD", "temp")
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    # Copy the extracted file
    print("Copying extracted files")
    romfs_folder = os.path.join(output_folder, "AAR MOD", "romfs")
    extracted_folder = os.path.join(extract_folder)
    src_file_path = os.path.join(extracted_folder, "UI", "LayoutArchive", "Common.Product.110.Nin_NX_NVN.blarc.zs")
    dst_file_path = os.path.join(romfs_folder, "UI", "LayoutArchive", "Common.Product.110.Nin_NX_NVN.blarc.zs")
    os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
    shutil.copy2(src_file_path, dst_file_path)
    src_folder_path = os.path.join(extracted_folder, "Font")
    dst_folder_path = os.path.join(romfs_folder, "Font")
    os.makedirs(os.path.dirname(dst_folder_path), exist_ok=True)
    shutil.copytree(src_folder_path, dst_folder_path)

    # Clean up
    print("Cleaning up old files")
    os.remove(zip_file_path)
    shutil.rmtree(extract_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <controller_id> <output_folder>")
        sys.exit(1)

    controller_id = sys.argv[1]
    output_folder = sys.argv[2]

    install_required_packages()
    download_extract_copy(controller_id, output_folder)
