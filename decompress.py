import os
import sys
import subprocess

def install_zstandard():
    try:
        import zstandard
    except ImportError:
        print("Installing zstandard library...")
        try:
            import pip
            pip.main(['install', 'zstandard'])
        except:
            print("Failed to install zstandard library. Please install it manually.")
            sys.exit(1)

def decompress_zstd(input_file):
    # Check if zstandard library is installed
    try:
        import zstandard as zstd
    except ImportError:
        print("zstandard library not found.")
        install_zstandard()
        try:
            import zstandard as zstd
        except ImportError:
            print("Failed to import zstandard library. Please make sure it is installed.")
            sys.exit(1)

    # Check if the input file exists
    if not os.path.isfile(input_file):
        print("Input file not found.")
        sys.exit(1)

    # Decompress the zstd file
    output_file = os.path.splitext(input_file)[0]  # Remove .zs extension
    dctx = zstd.ZstdDecompressor()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        decompressed_data = dctx.decompress(f_in.read())
        f_out.write(decompressed_data)

    print(f"Decompressed file: {output_file}")

if __name__ == "__main__":
    # Install zstandard if not already installed
    install_zstandard()

    if len(sys.argv) < 2:
        print("Please provide the input file path.")
        sys.exit(1)

    input_file = sys.argv[1]
    decompress_zstd(input_file)
