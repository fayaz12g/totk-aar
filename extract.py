import os
import sys
import time
import SarcLib
import libyaz0

def extract_blarc(file, output_folder):
    """
    Extract the given archive.
    """
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(os.path.basename(file))[0]  # Extract the base name of the file without extension
    ext = SarcLib.guessFileExt(inb)

    if ext != ".sarc":
        with open(os.path.join(output_folder, ''.join([name, ext])), "wb") as out:
            out.write(inb)
    else:
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        root = os.path.join(output_folder, "AAR MOD", "temp", name)  # Update the construction of the output path
        if not os.path.isdir(root):
            os.mkdir(root)

        files = []

        def getAbsPath(folder, path):
            nonlocal root
            nonlocal files

            for checkObj in folder.contents:
                if isinstance(checkObj, SarcLib.File):
                    files.append(["/".join([path, checkObj.name]), checkObj.data])
                else:
                    path_ = os.path.join(root, "/".join([path, checkObj.name]))
                    if not os.path.isdir(path_):
                        os.mkdir(path_)
                    getAbsPath(checkObj, "/".join([path, checkObj.name]))

        for checkObj in arc.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append([checkObj.name, checkObj.data])
            else:
                path = os.path.join(root, checkObj.name)
                if not os.path.isdir(path):
                    os.mkdir(path)
                getAbsPath(checkObj, checkObj.name)

        for file, fileData in files:
            print(file)
            with open(os.path.join(root, file), "wb") as out:
                out.write(fileData)

def main(blarc_file_path, output_folder):
    if not os.path.isfile(blarc_file_path):
        print("Invalid BLARC file path.")
        sys.exit(1)

    if not os.path.isdir(output_folder):
        print("Invalid output folder path.")
        sys.exit(1)

    extracted_file_path = os.path.join(output_folder, "AAR MOD", "temp", "Common.Product.110.Nin_NX_NVN.blarc")
    extract(extracted_file_path, output_folder)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python extract.py <blarc_file_path> <output_folder>")
        sys.exit(1)

    blarc_file_path = sys.argv[1]
    output_folder = sys.argv[2]

    main(blarc_file_path, output_folder)
