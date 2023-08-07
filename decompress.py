import os
import sys
import subprocess

def decompress_zstd(input_file, output_folder, mod_name):
    import zstandard as zstd

    # Create the output folder path
    aar_mod_folder = os.path.join(output_folder, mod_name)
    temp_folder = os.path.join(aar_mod_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    # Decompress the zstd file
    output_file = os.path.join(temp_folder, os.path.splitext(os.path.basename(input_file))[0])
    dctx = zstd.ZstdDecompressor()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        decompressed_data = dctx.decompress(f_in.read())
        f_out.write(decompressed_data)

    print(f"Decompressed file: {output_file}")

if __name__ == "__main__":
    # Install zstandard if not already installed
    import zstandard as zstd

    if len(sys.argv) < 3:
        print("Please provide the input file path and output folder path.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    dctx = zstd.ZstdDecompressor()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        decompressed_data = dctx.decompress(f_in.read())
        f_out.write(decompressed_data)
