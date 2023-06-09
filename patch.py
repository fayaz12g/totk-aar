import os
import sys
import subprocess
import ratiotohex
import struct
import math

from ratiotohex import calculate_rounded_ratio, convert_asm_to_arm64_hex, float2hex

def create_patch_files(patch_folder, ratio_value, visual_fixes):
    if float(ratio_value) > (16/9):
        scaling_factor = float(ratio_value) / (16/9)
        scaling_factor = float(scaling_factor)
        stretch = "horizontal"
    else:
        scaling_factor = (16/9) / float(ratio_value)
        scaling_factor = float(scaling_factor)
        stretch = "vertical"
        
    print(f"Ratio value is set to {ratio_value} and the scaling factor is {scaling_factor}.")
    hex_factor = ratiotohex.float2hex(scaling_factor)
    rounded_ratio = ratiotohex.calculate_rounded_ratio(float(ratio_value))
    asm_code = ratiotohex.generate_asm_code(rounded_ratio)
    ratio_value = float(ratio_value)
    hex_value = ratiotohex.convert_asm_to_arm64_hex(ratio_value)
    print(hex_value)
    visual_fixese = visual_fixes[0]
    visual_fixesa = visual_fixes[1]
    visual_fixesb = visual_fixes[2]
    visual_fixesc = visual_fixes[3]
    visual_fixesd = visual_fixes[4]
    version_variables = ["1.0.0", "1.1.0", "1.1.1", "1.1.2", "1.2.0"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "082CE09B06E33A123CB1E2770F5F9147709033DB"
            visual_fix = visual_fixese
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
037745a0 {hex_factor}
01a8f18c DD947394 
03774500 A01B40BD 
03774504 E0C31FF8 
03774508 00000090 
0377450c 01A045BD
03774510 E0C35FF8 
03774514 0008211E 
03774518 A11F40BD
0377451c C0035FD6
01a93954 F3827394
03774520 802240BD
03774524 E0C31FF8
03774528 00000090 
0377452c 01A045BD
03774530 E0C35FF8
03774534 0008211E
03774538 812640BD
0377453c C0035FD6
01a8e69c A9977394
03774540 E00B40BD
03774544 E0C31FF8
03774548 00000090
0377454c 01A045BD 
03774550 E0C35FF8
03774554 0008211E
03774558 E10F40BD
0377455c C0035FD6
012ade68 BE199394
03774560 000140BD
03774564 E0C31FF8
03774568 00000090
0377456c 01A045BD
03774570 E0C35FF8
03774574 0008211E
03774578 010540BD
0377457c C0035FD6
012ae24c CD189394
03774580 000140BD
03774584 E0C31FF8
03774588 00000090
0377458c 01A045BD
03774590 E0C35FF8
03774594 0008211E
03774598 010540BD
0377459c C0035FD6
'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
037745a0 {hex_factor}

// NPC Marker Fix
01a8f18c DD947394
03774500 A11F40BD
03774504 E0C31FF8
03774508 00000090
0377450c 00A045BD
03774510 E0C35FF8 
03774514 2108201E
03774518 A01B40BD
0377451c C0035FD6

// NPC Text Balloon Fix
01a93954 F3827394
03774520 812640BD
03774524 E0C31FF8
03774528 00000090
0377452c 00A045BD
03774530 E0C35FF8
03774534 2108201E
03774538 802240BD
0377453c C0035FD6

// Item Description Fix
01a8e69c A9977394
03774540 E10F40BD
03774544 E0C31FF8
03774548 00000090
0377454c 00A045BD
03774550 E0C35FF8
03774554 2108201E
03774558 E00B40BD
0377455c C0035FD6

// Enemy Info Fix
012ade68 BE199394
03774560 010540BD
03774564 E0C31FF8
03774568 00000090
0377456c 00A045BD
03774570 E0C35FF8
03774574 2108201E
03774578 000140BD
0377457c C0035FD6

// Enemy Notice Fix
012ae24c CD189394
03774580 010540BD
03774584 E0C31FF8
03774588 00000090
0377458c 00A045BD
03774590 E0C35FF8
03774594 2108201E
03774598 000140BD
0377459c C0035FD6
@stop
'''
            replacement_value = "0377AC54"
            inventory_value = "01968C2C"
            hestu_value = "01E5EAE8"
        elif version_variable == "1.1.0":
            nsobidid = "D5AD6AC71EF53E3E52417C1B81DBC9B4142AA3B3"
            visual_fix = visual_fixesa
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
036d1120 {hex_factor}
01aec24c 8D936F94
036d1080 A01B40BD
036d1084 E0C31FF8
036d1088 00000090
036d108c 012041BD
036d1090 E0C35FF8
036d1094 0008211E
036d1098 A11F40BD
036d109c C0035FD6
01af0a2c 9D816F94
036d10a0 802240BD
036d10a4 E0C31FF8
036d10a8 00000090
036d10ac 012041BD
036d10b0 E0C35FF8
036d10b4 0008211E
036d10b8 812640BD
036d10bc C0035FD6
01aeb644 9F966F94
036d10c0 E10B40BD
036d10c4 E0C31FF8
036d10c8 00000090
036d10cc 002041BD
036d10d0 E0C35FF8
036d10d4 2108201E
036d10d8 E00F40BD
036d10dc C0035FD6
012e5a18 B2AD8F94
036d10e0 000140BD
036d10e4 E0C31FF8
036d10e8 00000090
036d10ec 012041BD
036d10f0 E0C35FF8
036d10f4 0008211E
036d10f8 010540BD
036d10fc C0035FD6
012e5e68 A6AC8F94
036d1100 000140BD
036d1104 E0C31FF8
036d1108 00000090
036d110c 012041BD
036d1110 E0C35FF8
036d1114 0008211E
036d1118 010540BD
036d111c C0035FD6
'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
036d1120 {hex_factor}

// NPC Marker Fix
01aec24c 8D936F94
036d1080 A11F40BD
036d1084 E0C31FF8
036d1088 00000090
036d108c 002041BD
036d1090 E0C35FF8
036d1094 2108201E
036d1098 A01B40BD
036d109c C0035FD6

// NPC Text Balloon Fix
01af0a2c 9D816F94
036d10a0 812640BD
036d10a4 E0C31FF8
036d10a8 00000090
036d10ac 002041BD
036d10b0 E0C35FF8
036d10b4 2108201E
036d10b8 802240BD
036d10bc C0035FD6

// Item Description Fix
01aeb644 9F966F94
036d10c0 E00F40BD
036d10c4 E0C31FF8
036d10c8 00000090
036d10cc 012041BD
036d10d0 E0C35FF8
036d10d4 0008211E
036d10d8 E10B40BD
036d10dc C0035FD6

// Enemy Info Fix
012e5a18 B2AD8F94
036d10e0 010540BD
036d10e4 E0C31FF8
036d10e8 00000090
036d10ec 002041BD
036d10f0 E0C35FF8
036d10f4 2108201E
036d10f8 000140BD
036d10fc C0035FD6

// Enemy Notice Fix
012e5e68 A6AC8F94
036d1100 010540BD
036d1104 E0C31FF8
036d1108 00000090
036d110c 002041BD
036d1110 E0C35FF8
036d1114 2108201E
036d1118 000140BD
036d111c C0035FD6
'''  
            replacement_value = "0381B344"
            inventory_value = "019C2260"
            hestu_value = "01ED8FA4"
        elif version_variable == "1.1.1":
            nsobidid = "168DD518D925C7A327677286E72FEDA833314919"
            visual_fix = visual_fixesb
            replacement_value = "0382413C"
            inventory_value = "019C013C"
            hestu_value = "01ED6710"
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
036d9f80 {hex_factor}
01ae9b14 F3C06F94
036d9ee0 A01B40BD
036d9ee4 E0C31FF8
036d9ee8 00000090
036d9eec 01804FBD
036d9ef0 E0C35FF8
036d9ef4 0008211E
036d9ef8 A11F40BD
036d9efc C0035FD6
01aee304 FFAE6F94
036d9f00 802240BD
036d9f04 E0C31FF8
036d9f08 00000090
036d9f0c 01804FBD
036d9f10 E0C35FF8
036d9f14 0008211E
036d9f18 812640BD
036d9f1c C0035FD6
01ae8f0c 05C46F94
036d9f20 E10B40BD
036d9f24 E0C31FF8
036d9f28 00000090
036d9f2c 00804FBD
036d9f30 E0C35FF8
036d9f34 2108201E
036d9f38 E00F40BD
036d9f3c C0035FD6
012e3614 4BDA8F94
036d9f40 000140BD
036d9f44 E0C31FF8
036d9f48 00000090
036d9f4c 01804FBD
036d9f50 E0C35FF8
036d9f54 0008211E
036d9f58 010540BD
036d9f5c C0035FD6
012e39fc 59D98F94
036d9f60 000140BD
036d9f64 E0C31FF8
036d9f68 00000090
036d9f6c 01804FBD
036d9f70 E0C35FF8
036d9f74 0008211E
036d9f78 010540BD
036d9f7c C0035FD6
'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
036d9f80 {hex_factor}

// NPC Marker Fix
01ae9b14 F3C06F94
036d9ee0 A11F40BD
036d9ee4 E0C31FF8
036d9ee8 00000090
036d9eec 00804FBD
036d9ef0 E0C35FF8
036d9ef4 2108201E
036d9ef8 A01B40BD
036d9efc C0035FD6

// NPC Text Balloon Fix
01aee304 FFAE6F94
036d9f00 812640BD
036d9f04 E0C31FF8
036d9f08 00000090
036d9f0c 00804FBD
036d9f10 E0C35FF8
036d9f14 2108201E
036d9f18 802240BD
036d9f1c C0035FD6

// Item Description Fix
01ae8f0c 05C46F94
036d9f20 E00F40BD
036d9f24 E0C31FF8
036d9f28 00000090
036d9f2c 01804FBD
036d9f30 E0C35FF8
036d9f34 0008211E
036d9f38 E10B40BD
036d9f3c C0035FD6

// Enemy Info Fix
012e3614 4BDA8F94
036d9f40 010540BD
036d9f44 E0C31FF8
036d9f48 00000090
036d9f4c 00804FBD
036d9f50 E0C35FF8
036d9f54 2108201E
036d9f58 000140BD
036d9f5c C0035FD6

// Enemy Notice Fix
012e39fc 59D98F94
036d9f60 010540BD
036d9f64 E0C31FF8
036d9f68 00000090
036d9f6c 00804FBD
036d9f70 E0C35FF8
036d9f74 2108201E
036d9f78 000140BD
036d9f7c C0035FD6
'''  
        elif version_variable == "1.1.2":
            nsobidid = "9A10ED9435C06733DA597D8094D9000AB5D3EE60"
            visual_fix = visual_fixesc
            replacement_value = "03813D0C"
            inventory_value = "019B5480"
            hestu_value = "01ECE314"
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
036c9b20 {hex_factor}
01ae0440 90A56F94
036c9a80 A01B40BD
036c9a84 E0C31FF8
036c9a88 00000090
036c9a8c 01204BBD
036c9a90 E0C35FF8
036c9a94 0008211E
036c9a98 A11F40BD
036c9a9c C0035FD6
01ae4c24 9F936F94
036c9aa0 802240BD
036c9aa4 E0C31FF8
036c9aa8 00000090
036c9aac 01204BBD
036c9ab0 E0C35FF8
036c9ab4 0008211E
036c9ab8 812640BD
036c9abc C0035FD6
01adf838 A2A86F94
036c9ac0 E10B40BD
036c9ac4 E0C31FF8
036c9ac8 00000090
036c9acc 00204BBD
036c9ad0 E0C35FF8
036c9ad4 2108201E
036c9ad8 E00F40BD
036c9adc C0035FD6
012c2418 B21D9094
036c9ae0 000140BD
036c9ae4 E0C31FF8
036c9ae8 00000090
036c9aec 01204BBD
036c9af0 E0C35FF8
036c9af4 0008211E
036c9af8 010540BD
036c9afc C0035FD6
012C2828 B61C9094
036c9b00 000140BD
036c9b04 E0C31FF8
036c9b08 00000090
036c9b0c 01204BBD
036c9b10 E0C35FF8
036c9b14 0008211E
036c9b18 010540BD
036c9b1c C0035FD6
'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
036c9b20 {hex_factor}

// NPC Marker Fix
01ae0440 90A56F94
036c9a80 A11F40BD
036c9a84 E0C31FF8
036c9a88 00000090
036c9a8c 00204BBD
036c9a90 E0C35FF8
036c9a94 2108201E
036c9a98 A01B40BD
036c9a9c C0035FD6

// NPC Text Balloon Fix
01ae4c24 9F936F94
036c9aa0 812640BD
036c9aa4 E0C31FF8
036c9aa8 00000090
036c9aac 00204BBD
036c9ab0 E0C35FF8
036c9ab4 2108201E
036c9ab8 802240BD
036c9abc C0035FD6

// Item Description Fix
01adf838 A2A86F94
036c9ac0 E00F40BD
036c9ac4 E0C31FF8
036c9ac8 00000090
036c9acc 01204BBD
036c9ad0 E0C35FF8
036c9ad4 0008211E
036c9ad8 E10B40BD
036c9adc C0035FD6

// Enemy Info Fix
012c2418 B21D9094
036c9ae0 010540BD
036c9ae4 E0C31FF8
036c9ae8 00000090
036c9aec 00204BBD
036c9af0 E0C35FF8
036c9af4 2108201E
036c9af8 000140BD
036c9afc C0035FD6

// Enemy Notice Fix
012C2828 B61C9094
036c9b00 010540BD
036c9b04 E0C31FF8
036c9b08 00000090
036c9b0c 00204BBD
036c9b10 E0C35FF8
036c9b14 2108201E
036c9b18 000140BD
036c9b1c C0035FD6 
'''   
        elif version_variable == "1.2.0":
            nsobidid = "6F32C68DD3BC7D77AA714B80E92A096A737CDA77"
            replacement_value = "0380794c"
            inventory_value = "019a5870"
            hestu_value = "01EC1918"
            visual_fix = visual_fixesd
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
036bd770 {hex_factor}
01ad2174 ABAC6F94
036bd420 A01B40BD
036bd424 E0C31FF8
036bd428 00000090
036bd42c 017047BD
036bd430 E0C35FF8
036bd434 0008211E
036bd438 A11F40BD
036bd43c C0035FD6
01ad6964 B79A6F94
036bd440 802240BD
036bd444 E0C31FF8
036bd448 00000090
036bd44c 017047BD
036bd450 E0C35FF8
036bd454 0008211E
036bd458 812640BD
036bd45c C0035FD6
01ad156c 31AF6F94
036bd230 E10B40BD
036bd234 E0C31FF8
036bd238 00000090
036bd23c 007047BD
036bd240 E0C35FF8
036bd244 2108201E
036bd248 E00F40BD
036bd24c C0035FD6
012d5ae0 0C9F8F94
036bd710 000140BD
036bd714 E0C31FF8
036bd718 00000090
036bd71c 017047BD
036bd720 E0C35FF8
036bd724 0008211E
036bd728 010540BD
036bd72c C0035FD6
012d5ea8 829D8F94
036bd4b0 000140BD
036bd4b4 E0C31FF8
036bd4b8 00000090
036bd4bc 017047BD
036bd4c0 E0C35FF8
036bd4c4 0008211E
036bd4c8 010540BD
036bd4cc C0035FD6
'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
036bd770 {hex_factor}

// NPC Marker Fix
01ad2174 ABAC6F94
036bd420 A11F40BD
036bd424 E0C31FF8
036bd428 00000090
036bd42c 007047BD
036bd430 E0C35FF8
036bd434 2108201E
036bd438 A01B40BD
036bd43c C0035FD6

// NPC Text Balloon Fix
01ad6964 B79A6F94
036bd440 812640BD
036bd444 E0C31FF8
036bd448 00000090
036bd44c 007047BD
036bd450 E0C35FF8
036bd454 2108201E
036bd458 802240BD
036bd45c C0035FD6

// Item Description Fix
01ad156c 31AF6F94
036bd230 E00F40BD
036bd234 E0C31FF8
036bd238 00000090
036bd23c 017047BD
036bd240 E0C35FF8
036bd244 0008211E
036bd248 E10B40BD
036bd24c C0035FD6

// Enemy Info Fix
012d5ae0 0C9F8F94
036bd710 010540BD
036bd714 E0C31FF8
036bd718 00000090
036bd71c 007047BD
036bd720 E0C35FF8
036bd724 2108201E
036bd728 000140BD
036bd72c C0035FD6

// Enemy Notice Fix
012d5ea8 829D8F94
036bd4b0 010540BD
036bd4b4 E0C31FF8
036bd4b8 00000090
036bd4bc 007047BD
036bd4c0 E0C35FF8
036bd4c4 2108201E
036bd4c8 000140BD
036bd4cc C0035FD6
'''
        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{replacement_value} {ratiotohex.float2hex(ratio_value)}
{inventory_value} {hex_value}
{hestu_value} {hex_value}

{text_fix}
{visual_fix}
@stop

// Generated using TOTK-AAR by Fayaz (github.com/fayaz12g/totk-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide the output folder and ratio.")
        sys.exit(1)
    patch_folder = sys.argv[1]
    ratio_value = float(sys.argv[2])
    create_patch_files(patch_folder, ratio_value)
