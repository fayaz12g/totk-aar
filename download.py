def download_extract_copy(controller_id, output_folder):
    import requests
    import zipfile
    import shutil

    # URL of the ZIP file
    zip_url = f"https://github.com/fayaz12g/totk-controllers/raw/main/{controller_id}.zip"

    # Download the ZIP file
    print("Downloading zip file. This may take up to 10 seconds.")
    response = requests.get(zip_url)
    print("Zip file downloaded.")
    zip_file_path = os.path.join(output_folder, f"{controller_id}.zip")
    with open(zip_file_path, "wb") as file:
        print("Writing contents to temp folder.")
        file.write(response.content)

    # Extract the ZIP file
    extract_folder = os.path.join(output_folder, "AAR MOD", "temp")
    print(f"Extracting zip to {extract_folder}. This can also take a few seconds.")
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

