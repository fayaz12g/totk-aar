import os
import sys
import subprocess
import ratiotohex

from ratiotohex import calculate_rounded_ratio, convert_asm_to_arm64_hex


def create_patch_files(patch_folder, ratio_value):
    version_variables = ["1.0.0", "1.1.0", "1.1.1", "1.1.2"]

    for version_variable in version_variables:
        # Create the file path for the patch file
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        # Determine the replacement value based on the version
        if version_variable == "1.0.0":
            replacement_value = "00C7D8F4"
        elif version_variable == "1.1.0":
            replacement_value = "00CDB304"
        elif version_variable == "1.1.1":
            replacement_value = "00CE3410"
        else:
            replacement_value = "00CCB094"  # Default value if version_variable is not recognized

        # Calculate the rounded ratio
        rounded_ratio = ratiotohex.calculate_rounded_ratio(ratio_value)

        # Generate the assembly code and ARM64 hex
        asm_code = ratiotohex.generate_asm_code(rounded_ratio)
        hex_value = ratiotohex.convert_asm_to_arm64_hex(asm_code)
        print(hex_value)

        # Create the contents of the patch file with the replacement value and hex code
        patch_content = f'''@nsobid-9A10ED9435C06733DA597D8094D9000AB5D3EE60

@flag print_values
@flag offset_shift 0x100

@enabled
{replacement_value} {hex_value}
@stop

// by youtube.com/fayaz'''

        # Create the directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the patch content to the file
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)

        print(f"Patch file created: {file_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide the output folder and ratio.")
        sys.exit(1)

    patch_folder = sys.argv[1]
    ratio_value = float(sys.argv[2])  # Parse the ratio as a float

    create_patch_files(patch_folder, ratio_value)