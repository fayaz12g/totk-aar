import importlib.util
import subprocess
import sys

def install_keystone_engine():
    try:
        importlib.util.find_spec("keystone")
        print("Keystone Engine is already installed.")
    except ImportError:
        print("Keystone Engine not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "keystone-engine"])
            print("Keystone Engine installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing Keystone Engine: {str(e)}")
            sys.exit(1)

def convert_asm_to_arm64_hex(asm_code):
    try:
        import keystone
    except ImportError:
        print("Keystone Engine not found. Installing...")
        install_keystone_engine()
        try:
            import keystone
        except ImportError:
            print("Failed to install Keystone Engine. Please install it manually.")
            sys.exit(1)

    ks = keystone.Ks(keystone.KS_ARCH_ARM64, keystone.KS_MODE_LITTLE_ENDIAN)
    encoding, _ = ks.asm(asm_code)
    hex_value = "".join(f"{byte:02x}" for byte in encoding).upper()  # Convert to uppercase
    print(hex_value)
    return hex_value

def calculate_rounded_ratio(ratio_value):
    if ratio_value <= 2:
        rounded_ratio = round(ratio_value * 16) / 16
    elif ratio_value > 2 and ratio_value <= 4:
        rounded_ratio = round(ratio_value * 8) / 8
    else:
        rounded_ratio = round(ratio_value * 4) / 4
    return rounded_ratio

def generate_asm_code(rounded_ratio):
    asm_code = f"fmov s0, #{rounded_ratio}"
    return asm_code

if __name__ == "__main__":
    install_keystone_engine()

    ratio = 21 / 9
    rounded_ratio = calculate_rounded_ratio(ratio_value)
    print(f"Rounded Ratio: {rounded_ratio}")
    
    asm_code = generate_asm_code(rounded_ratio)
    print(f"Assembly Code: {asm_code}")
    
    arm64_hex = convert_asm_to_arm64_hex(asm_code)
    print(f"ARM64 Hex: {arm64_hex}")
