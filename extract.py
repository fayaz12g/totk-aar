import os
import sys
import time
import subprocess

def install_library(library):
    try:
        import importlib
        importlib.import_module(library)
    except ImportError:
        print(f"{library} is not installed!")
        ans = input(f"Do you want to install {library} now? (y/n)\t")
        if ans.lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
        else:
            print(f"Cannot proceed without {library}. Exiting...")
            exit(1)

# Install required libraries
install_library("SarcLib==0.3")
install_library("libyaz0==0.5")

try:
    import SarcLib
except ImportError:
    print("Failed to import SarcLib. Make sure it is installed correctly.")
    sys.exit(1)

try:
    import libyaz0
except ImportError:
    print("Failed to import libyaz0. Make sure it is installed correctly.")
    sys.exit(1)


def extract(file):
    """
    Extract the given archive
    """
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(file)[0]
    ext = SarcLib.guessFileExt(inb)

    if ext != ".sarc":
        with open(''.join([name, ext]), "wb") as out:
            out.write(inb)
    else:
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        root = os.path.join(os.path.dirname(file), name)
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


def main():
    print("SARC Tool v0.5")
    print("(C) 2017-2019 MasterVermilli0n / AboodXD\n")

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python your_script.py <path_to_blarc_file>")
        sys.exit(1)

    root = os.path.abspath(sys.argv[1])
    if os.path.isfile(root):
        extract(root)
    else:
        print("Blarc file doesn't exist!")
        sys.exit(1)


if __name__ == '__main__':
    main()
