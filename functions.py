import struct
import math
import os

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
