import os
import sys
import subprocess
import functions
import struct
import math

from functions import *

def create_patch_files(patch_folder, ratio_value, visual_fixes):
    if float(ratio_value) > (16/9):
        scaling_factor = float(ratio_value) / (16/9)
        scaling_factor = float(scaling_factor)
        stretch = "horizontal"
        do_text_fix = "enabled"
    if float(ratio_value) < (16/9):
        scaling_factor = (16/9) / float(ratio_value)
        scaling_factor = float(scaling_factor)
        stretch = "vertical"
        do_text_fix = "enabled"
    if float(ratio_value) == (16/9):
        scaling_factor = (16/9) / float(ratio_value)
        scaling_factor = float(scaling_factor)
        stretch = "vertical"
        do_text_fix = "disabled"
        
    print(f"Ratio value is set to {ratio_value} and the scaling factor is {scaling_factor}.")
    hex_factor = functions.float2hex(scaling_factor)
    rounded_ratio = functions.calculate_rounded_ratio(float(ratio_value))
    asm_code = functions.generate_asm_code(rounded_ratio)
    ratio_value = float(ratio_value)
    reduction_replace = "C0000014"
    lod_replace = "24000014"
    hex_value = functions.convert_asm_to_arm64_hex(ratio_value)
    print(hex_value)
    visual_fixese = visual_fixes[0]
    visual_fixesa = visual_fixes[1]
    visual_fixesb = visual_fixes[2]
    visual_fixesc = visual_fixes[3]
    visual_fixesd = visual_fixes[4]
    visual_fixesf = visual_fixes[5]
    version_variables = ["1.0.0", "1.1.0", "1.1.1", "1.1.2", "1.2.0", "1.2.1"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "082CE09B06E33A123CB1E2770F5F9147709033DB"
            visual_fix = visual_fixese
            reduction_value = "00C40A8C"
            lod_value = "027D9448"
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
@enabled
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
@disabled'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
@{do_text_fix}
037745a0 {hex_factor}
@disabled

// NPC Marker Fix
@{do_text_fix}
01a8f18c DD947394
03774500 A11F40BD
03774504 E0C31FF8
03774508 00000090
0377450c 00A045BD
03774510 E0C35FF8 
03774514 2108201E
03774518 A01B40BD
0377451c C0035FD6
@disabled

// NPC Text Balloon Fix
@{do_text_fix}
01a93954 F3827394
03774520 812640BD
03774524 E0C31FF8
03774528 00000090
0377452c 00A045BD
03774530 E0C35FF8
03774534 2108201E
03774538 802240BD
0377453c C0035FD6
@disabled

// Item Description Fix
@{do_text_fix}
01a8e69c A9977394
03774540 E10F40BD
03774544 E0C31FF8
03774548 00000090
0377454c 00A045BD
03774550 E0C35FF8
03774554 2108201E
03774558 E00B40BD
0377455c C0035FD6
@disabled

// Enemy Info Fix
@{do_text_fix}
012ade68 BE199394
03774560 010540BD
03774564 E0C31FF8
03774568 00000090
0377456c 00A045BD
03774570 E0C35FF8
03774574 2108201E
03774578 000140BD
0377457c C0035FD6
@disabled

// Enemy Notice Fix
@{do_text_fix}
012ae24c CD189394
03774580 010540BD
03774584 E0C31FF8
03774588 00000090
0377458c 00A045BD
03774590 E0C35FF8
03774594 2108201E
03774598 000140BD
0377459c C0035FD6
@disabled'''
            replacement_value = "0377AC54"
            inventory_value = "01968C2C"
            hestu_value = "01E5EAE8"
        elif version_variable == "1.1.0":
            nsobidid = "D5AD6AC71EF53E3E52417C1B81DBC9B4142AA3B3"
            visual_fix = visual_fixesa
            reduction_value = "00CAD34C"
            lod_value = "027D9448"
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
@enabled
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
@disabled'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
@{do_text_fix}
036d1120 {hex_factor}
@disabled

// NPC Marker Fix
@{do_text_fix}
01aec24c 8D936F94
036d1080 A11F40BD
036d1084 E0C31FF8
036d1088 00000090
036d108c 002041BD
036d1090 E0C35FF8
036d1094 2108201E
036d1098 A01B40BD
036d109c C0035FD6
@disabled

// NPC Text Balloon Fix
@{do_text_fix}
01af0a2c 9D816F94
036d10a0 812640BD
036d10a4 E0C31FF8
036d10a8 00000090
036d10ac 002041BD
036d10b0 E0C35FF8
036d10b4 2108201E
036d10b8 802240BD
036d10bc C0035FD6
@disabled

// Item Description Fix
@{do_text_fix}
01aeb644 9F966F94
036d10c0 E00F40BD
036d10c4 E0C31FF8
036d10c8 00000090
036d10cc 012041BD
036d10d0 E0C35FF8
036d10d4 0008211E
036d10d8 E10B40BD
036d10dc C0035FD6
@disabled

// Enemy Info Fix
@{do_text_fix}
012e5a18 B2AD8F94
036d10e0 010540BD
036d10e4 E0C31FF8
036d10e8 00000090
036d10ec 002041BD
036d10f0 E0C35FF8
036d10f4 2108201E
036d10f8 000140BD
036d10fc C0035FD6
@disabled

// Enemy Notice Fix
@{do_text_fix}
012e5e68 A6AC8F94
036d1100 010540BD
036d1104 E0C31FF8
036d1108 00000090
036d110c 002041BD
036d1110 E0C35FF8
036d1114 2108201E
036d1118 000140BD
036d111c C0035FD6
@disabled'''  
            replacement_value = "0381B344"
            inventory_value = "019C2260"
            hestu_value = "01ED8FA4"
        elif version_variable == "1.1.1":
            nsobidid = "168DD518D925C7A327677286E72FEDA833314919"
            visual_fix = visual_fixesb
            reduction_value = "00CC1C2C"
            lod_value = "027E07A8"
            replacement_value = "0382413C"
            inventory_value = "019C013C"
            hestu_value = "01ED6710"
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
@enabled
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
@disabled'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
@{do_text_fix}
036d9f80 {hex_factor}
@disabled

// NPC Marker Fix
@{do_text_fix}
01ae9b14 F3C06F94
036d9ee0 A11F40BD
036d9ee4 E0C31FF8
036d9ee8 00000090
036d9eec 00804FBD
036d9ef0 E0C35FF8
036d9ef4 2108201E
036d9ef8 A01B40BD
036d9efc C0035FD6
@disabled

// NPC Text Balloon Fix
@{do_text_fix}
01aee304 FFAE6F94
036d9f00 812640BD
036d9f04 E0C31FF8
036d9f08 00000090
036d9f0c 00804FBD
036d9f10 E0C35FF8
036d9f14 2108201E
036d9f18 802240BD
036d9f1c C0035FD6
@disabled

// Item Description Fix
@{do_text_fix}
01ae8f0c 05C46F94
036d9f20 E00F40BD
036d9f24 E0C31FF8
036d9f28 00000090
036d9f2c 01804FBD
036d9f30 E0C35FF8
036d9f34 0008211E
036d9f38 E10B40BD
036d9f3c C0035FD6
@disabled

// Enemy Info Fix
@{do_text_fix}
012e3614 4BDA8F94
036d9f40 010540BD
036d9f44 E0C31FF8
036d9f48 00000090
036d9f4c 00804FBD
036d9f50 E0C35FF8
036d9f54 2108201E
036d9f58 000140BD
036d9f5c C0035FD6
@disabled

// Enemy Notice Fix
@{do_text_fix}
012e39fc 59D98F94
036d9f60 010540BD
036d9f64 E0C31FF8
036d9f68 00000090
036d9f6c 00804FBD
036d9f70 E0C35FF8
036d9f74 2108201E
036d9f78 000140BD
036d9f7c C0035FD6
@disabled'''  
        elif version_variable == "1.1.2":
            nsobidid = "9A10ED9435C06733DA597D8094D9000AB5D3EE60"
            visual_fix = visual_fixesc
            reduction_value = "00C76FFC"
            lod_value = "027D04F8"
            replacement_value = "03813D0C"
            inventory_value = "019B5480"
            hestu_value = "01ECE314"
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
@enabled
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
@disabled'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
@{do_text_fix}
036c9b20 {hex_factor}
@disabled

// NPC Marker Fix
@{do_text_fix}
01ae0440 90A56F94
036c9a80 A11F40BD
036c9a84 E0C31FF8
036c9a88 00000090
036c9a8c 00204BBD
036c9a90 E0C35FF8
036c9a94 2108201E
036c9a98 A01B40BD
036c9a9c C0035FD6
@disabled

// NPC Text Balloon Fix
@{do_text_fix}
01ae4c24 9F936F94
036c9aa0 812640BD
036c9aa4 E0C31FF8
036c9aa8 00000090
036c9aac 00204BBD
036c9ab0 E0C35FF8
036c9ab4 2108201E
036c9ab8 802240BD
036c9abc C0035FD6
@disabled

// Item Description Fix
@{do_text_fix}
01adf838 A2A86F94
036c9ac0 E00F40BD
036c9ac4 E0C31FF8
036c9ac8 00000090
036c9acc 01204BBD
036c9ad0 E0C35FF8
036c9ad4 0008211E
036c9ad8 E10B40BD
036c9adc C0035FD6
@disabled

// Enemy Info Fix
@{do_text_fix}
012c2418 B21D9094
036c9ae0 010540BD
036c9ae4 E0C31FF8
036c9ae8 00000090
036c9aec 00204BBD
036c9af0 E0C35FF8
036c9af4 2108201E
036c9af8 000140BD
036c9afc C0035FD6
@disabled

// Enemy Notice Fix
@{do_text_fix}
012C2828 B61C9094
036c9b00 010540BD
036c9b04 E0C31FF8
036c9b08 00000090
036c9b0c 00204BBD
036c9b10 E0C35FF8
036c9b14 2108201E
036c9b18 000140BD
036c9b1c C0035FD6
@disabled'''   
        elif version_variable == "1.2.0":
            nsobidid = "6F32C68DD3BC7D77AA714B80E92A096A737CDA77"
            replacement_value = "0380794c"
            inventory_value = "019a5870"
            lod_value = "027c3ea8"
            reduction_value = "00C4275c"
            hestu_value = "01EC1918"
            visual_fix = visual_fixesd
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
@enabled
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
@disabled'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
@{do_text_fix}
036bd770 {hex_factor}
@disabled

// NPC Marker Fix
@{do_text_fix}
01ad2174 ABAC6F94
036bd420 A11F40BD
036bd424 E0C31FF8
036bd428 00000090
036bd42c 007047BD
036bd430 E0C35FF8
036bd434 2108201E
036bd438 A01B40BD
036bd43c C0035FD6
@disabled

// NPC Text Balloon Fix
@{do_text_fix}
01ad6964 B79A6F94
036bd440 812640BD
036bd444 E0C31FF8
036bd448 00000090
036bd44c 007047BD
036bd450 E0C35FF8
036bd454 2108201E
036bd458 802240BD
036bd45c C0035FD6
@disabled

// Item Description Fix
@{do_text_fix}
01ad156c 31AF6F94
036bd230 E00F40BD
036bd234 E0C31FF8
036bd238 00000090
036bd23c 017047BD
036bd240 E0C35FF8
036bd244 0008211E
036bd248 E10B40BD
036bd24c C0035FD6
@disabled

// Enemy Info Fix
@{do_text_fix}
012d5ae0 0C9F8F94
036bd710 010540BD
036bd714 E0C31FF8
036bd718 00000090
036bd71c 007047BD
036bd720 E0C35FF8
036bd724 2108201E
036bd728 000140BD
036bd72c C0035FD6
@disabled

// Enemy Notice Fix
@{do_text_fix}
012d5ea8 829D8F94
036bd4b0 010540BD
036bd4b4 E0C31FF8
036bd4b8 00000090
036bd4bc 007047BD
036bd4c0 E0C35FF8
036bd4c4 2108201E
036bd4c8 000140BD
036bd4cc C0035FD6
@disabled'''
                
        elif version_variable == "1.2.1":
            nsobidid = "9B4E43650501A4D4489B4BBFDB740F26AF3CF850"
            replacement_value = "00e66148"
            inventory_value = "019b36f0"
            hestu_value = "01ECdf68"
            visual_fix = visual_fixesf
            if stretch == "horizontal":
                text_fix = f'''// Text UI Fixes
@{do_text_fix}
036cc5a0 {hex_factor}
@disabled

// NPC Marker Fix
@{do_text_fix}
01add300 80BC6F94
036cc500 A01B40BD
036cc504 E0C31FF8
036cc508 00000090
036cc50c 01A045BD
036cc510 E0C35FF8
036cc514 0008211E
036cc518 A11F40BD
036cc51c C0035FD6
@disabled

// NPC Text Balloon Fix
@{do_text_fix}
01ae1ae4 8FAA6F94
036cc520 802240BD
036cc524 E0C31FF8
036cc528 00000090
036cc52c 01A045BD
036cc530 E0C35FF8
036cc534 0008211E
036cc538 812640BD
036cc53c C0035FD6
@disabled

// Item Description Fix
@{do_text_fix}
01adc6f8 92BF6F94
036cc540 E10B40BD
036cc544 E0C31FF8
036cc548 00000090
036cc54c 00A045BD
036cc550 E0C35FF8
036cc554 2108201E
036cc558 E00F40BD
036cc55c C0035FD6
@disabled

// Enemy Info Fix
@{do_text_fix}
012c7bd4 63129094
036cc560 000140BD
036cc564 E0C31FF8
036cc568 00000090
036cc56c 01A045BD
036cc570 E0C35FF8
036cc574 0008211E
036cc578 010540BD
036cc57c C0035FD6
@disabled

// Enemy Notice Fix
@{do_text_fix}
012c7fbc 71119094
036cc580 000140BD
036cc584 E0C31FF8
036cc588 00000090
036cc58c 01A045BD
036cc590 E0C35FF8
036cc594 0008211E
036cc598 010540BD
036cc59c C0035FD6
@disabled'''
            if stretch == "vertical":
                text_fix = f'''// Text UI Fixes
@{do_text_fix}
036cc5a0 {hex_factor}

// NPC Marker Fix
@{do_text_fix}
01add300 80BC6F94 // bl #0x1BEF200
036cc500 A11F40BD // ldr s1, [x29, #0x1c]
036cc504 E0C31FF8 // stur x0, [sp, #-4]
036cc508 00000090 // adrp x0, #0
036cc50c 00A045BD // ldr s0, [x0, #0x5a0]
036cc510 E0C35FF8 // ldur x0, [sp, #-4]
036cc514 2108201E // fmul s1, s1, s0
036cc518 A01B40BD // ldr s0, [x29,#0x18]
036cc51c C0035FD6 // ret
@disabled

// NPC Text Balloon Fix
@{do_text_fix}
01ae1ae4 8FAA6F94 // bl #0x1BEAA3C
036cc520 812640BD // ldr s1, [x20, #0x24]
036cc524 E0C31FF8 // stur x0, [sp, #-4]
036cc528 00000090 // adrp x0, #0
036cc52c 00A045BD // ldr s0, [x0, #0x5a0]
036cc530 E0C35FF8 // ldur x0, [sp, #-4]
036cc534 2108201E // fmul s1, s1, s0
036cc538 802240BD // ldr s0, [x20, #0x20]
036cc53c C0035FD6 // ret
@disabled

// Item Description Fix
@{do_text_fix}
01adc6f8 92BF6F94 // bl #0x1BEFE48
036cc540 E00F40BD // ldr s0, [sp, #0xc]
036cc544 E0C31FF8 // stur x0, [sp, #-4]
036cc548 00000090 // adrp x0, #0
036cc54c 01A045BD // ldr s1, [x0, #0x5a0]
036cc550 E0C35FF8 // ldur x0, [sp, #-4]
036cc554 0008211E // fmul s0, s0, s1
036cc558 E10B40BD // ldr s1, [sp, #0x8]
036cc55c C0035FD6 // ret
@disabled

// Enemy Info Fix
@{do_text_fix}
012c7bd4 63129094 // bl #0x240498C
036cc560 010540BD // ldr s1, [x8, #0x4]
036cc564 E0C31FF8 // stur x0, [sp, #-4]
036cc568 00000090 // adrp x0, #0
036cc56c 00A045BD // ldr s0, [x0, #0x5a0]
036cc570 E0C35FF8 // ldur x0, [sp, #-4]
036cc574 2108201E // fmul s1, s1, s0
036cc578 000140BD // ldr s0, [x8]
036cc57c C0035FD6 // ret
@disabled

// Enemy Notice Fix
@{do_text_fix}
012c7fbc 71119094 // bl #0x24045C4
036cc580 010540BD // ldr s1, [x8, #0x4]
036cc584 E0C31FF8 // stur x0, [sp, #-4]
036cc588 00000090 // adrp x0, #0
036cc58c 00A045BD // ldr s0, [x0, #0x5a0]
036cc590 E0C35FF8 // ldur x0, [sp, #-4]
036cc594 2108201E // fmul s1, s1, s0
036cc598 000140BD // ldr s0, [x8]
036cc59c C0035FD6 // ret
@disabled'''

        if version_variable == "1.2.1":
            patch_patches = f'''
@enabled
{replacement_value} {hex_value}
@disabled
'''
        else:
            patch_patches = f'''
@enabled
{replacement_value} {functions.float2hex(ratio_value)}
{inventory_value} {hex_value}
{hestu_value} {hex_value}
@disabled

{text_fix}
'''  
        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

{patch_patches}

{visual_fix}

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
