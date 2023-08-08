import os
import sys
import subprocess

def compress_zstd(input_file):
    import zstandard as zstd

    # Compress the input file using zstd
    output_file = f"{input_file}.zs"
    cctx = zstd.ZstdCompressor()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        compressed_data = cctx.compress(f_in.read())
        f_out.write(compressed_data)

    print(f"Compressed file: {output_file}")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide the input file path and the destination file path.")
        sys.exit(1)

    input_file = sys.argv[1]
    compress_zstd(input_file)
