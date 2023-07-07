import importlib.util
import subprocess
import sys
import struct
import math

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

def convert_asm_to_arm64_hex(x):
    p = math.floor(math.log(x, 2))
    a = round(16*(p-2) + x / 2**(p-4))
    if a<0: a += 128
    a = 2*a + 1
    h = hex(a).lstrip('0x').rjust(2,'0').upper()
    hex_value = '00' + h[1] + '02' + h[0] + '1E' 
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

def float2hex(f):
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()
    
if __name__ == "__main__":
    ratio = 21 / 9
    rounded_ratio = calculate_rounded_ratio(ratio_value)
    print(f"Rounded Ratio: {rounded_ratio}")
    
    asm_code = generate_asm_code(rounded_ratio)
    print(f"Assembly Code: {asm_code}")
    
    arm64_hex = convert_asm_to_arm64_hex(asm_code)
    print(f"ARM64 Hex: {arm64_hex}")
