import os
import sys
import subprocess
import ratiotohex

from ratiotohex import calculate_rounded_ratio, convert_asm_to_arm64_hex, float2hex


def create_patch_files(patch_folder, ratio_value, shadow_quality, scaling_factor):
    DOF_replace = "C0035FD6"
    shadow2_replace = "17000014"
    reducation_replace = "C0000014"
    FSR_replace = "08008052"
    dynamic1_replace = "15000014"
    dynamic2_replace = "000080D2"
    trilinear_replace = "4A008052"
    anisotropic_replace = "28E0A0F2"
    fxaa_replace = "08008052"
    scaling_factor=float(scaling_factor)
    hex_factor = ratiotohex.float2hex(scaling_factor)
    rounded_ratio = ratiotohex.calculate_rounded_ratio(float(ratio_value))
    asm_code = ratiotohex.generate_asm_code(rounded_ratio)
    ratio_value = float(ratio_value)
    hex_value = ratiotohex.convert_asm_to_arm64_hex(ratio_value)
    print(hex_value)
        
    if shadow_quality == "8":
        shadow1_replace = "0B018052"
    elif shadow_quality == "16":
        shadow1_replace = "0B028052"
    elif shadow_quality == "32":
        shadow1_replace = "0B048052"
    elif shadow_quality == "64":
        shadow1_replace = "0B088052"
    elif shadow_quality == "128":
        shadow1_replace = "0B108052"
    elif shadow_quality == "256":
        shadow1_replace = "0B208052"
    elif shadow_quality == "512":
        shadow1_replace = "0B408052"
    elif shadow_quality == "1024":
        shadow1_replace = "0B808052"
    elif shadow_quality == "2048":
        shadow1_replace = "0B008152"
        shadow_message = "Notice: Shadow resolution 2048 may cause freezing. We reccommend 1024."
    else:
        shadow1_replace = "0B808052"
    version_variables = ["1.0.0", "1.1.0", "1.1.1", "1.1.2", "1.2.0"]

    for version_variable in version_variables:
        # Create the file path for the patch file
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        # Determine the replacement value based on the version
        if version_variable == "1.0.0":
            text_fix = f'''
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
            replacement_value = "0377AC54"
            inventory_value = "01968C2C"
            hestu_value = "01E5EAE8"
            DOF_value = "00BD0F14"
            shadow1_value = "00B7214C"
            shadow2_value = "00B72150"
            reduction_value = "00C40A8C"
            fsr_value = "00C40A70"
            fxaa_value = "00C40A70"
            dynamic1_value = "0103474C"
            dynamic2_value = "02760D24"
            trilinear_value = "0070CD2C"
            anisotropic_value = "00895558"
            nsobidid = "082CE09B06E33A123CB1E2770F5F9147709033DB"
            fps20_code = f'''00E9D8A0 61008052
008F6D90 75008052
008F6C74 68008052
0196591C 6C008052
019707AC EB031F2A
008F6C78 1F2003D5
008F6CAC 1F2003D5
008F6D28 75008052
008F6D20 61008052'''
            fps30_code = f'''00E9D8A0 41008052
008F6D90 48008052
008F6C74 EB031F2A
0196591C 1F2003D5
019707AC 1F2003D5
008F6C78 55008052
008F6CAC 41008052
008F6D28 4C008052
008F6D20 55008052'''
            fps60_code = f'''00E9D8A0 21008052
008F6D20 35008052
008F6D90 28008052
008F6D28 2C008052
008F6C74 EB031F2A
0196591C 1F2003D5
019707AC 1F2003D5'''
            cutscene_code = f'''008F6C78 C4280D94
00C40F88 97CD0190
00C40F8C F7DE46F9
00C40F90 F7020391
00C40F94 E9024039
00C40F98 29050011
00C40F9C F503092A
00C40FA0 C0035FD6'''
            chuck_1008 = f'''00CEA5BC F50300AA
00CEA5C0 83F6FE97
00CEA5C4 140040B9
00CEA5C8 E00315AA
00CEA5D4 F50700F9
00CEA5D8 08E080D2
00CEA5DC 097E80D2
00CEA5E0 0001221E
00CEA5E4 0001221E
00CEA5EC 2101221E'''
        elif version_variable == "1.1.0":
            text_fix = f'''
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
            replacement_value = "0381B344"
            chuck_1008 = f'''00CEA5BC F50300AA
00CEA5C0 83F6FE97
00CEA5C4 140040B9
00CEA5C8 E00315AA
00CEA5D4 F50700F9
00CEA5D8 08E080D2
00CEA5DC 097E80D2
00CEA5E0 0001221E
00CEA5E4 0001221E
00CEA5EC 2101221E'''
            fps30_code = f'''00EBD158 41008052
0090EA38 55008052
0090EAA8 48008052
0090EA40 4C008052
0090E98C EB031F2A
019BF104 1F2003D5
019CA668 1F2003D5
0090E990 55008052
0090E9C4 41008052'''
            fps60_code = f'''00EBD158 21008052
0090EA38 35008052
0090EAA8 28008052
0090EA40 2C008052
0090E98C EB031F2A
019BF104 1F2003D5
019CA668 1F2003D5'''
            cutscene_code = f'''0090E990 CD7B0E94
00CAD8C4 F7D001F0
00CAD8C8 F79E44F9
00CAD8CC F7020391
00CAD8D0 E9024039
00CAD8D4 29050011
00CAD8D8 F503092A
00CAD8DC C0035FD6'''
            fps20_code = f'''00EBD158 61008052
0090EA38 75008052
0090EAA8 68008052
0090EA40 6C008052
0090E98C EB031F2A
019BF104 1F2003D5
019CA668 1F2003D5
0090E990 75008052
0090E9C4 61008052'''
            inventory_value = "019C2260"
            hestu_value = "01ED8FA4"
            shadow1_value = "00D075AC"
            shadow2_value = "00D075B0"
            DOF_value = "00C488B4"
            reduction_value = "00CAD34C"
            trilinear_value = "007639FC"
            anisotropic_value = "00C7F700"
            fxaa_value = "00CAD330"
            fsr_value = "00CAD340"
            nsobidid = "D5AD6AC71EF53E3E52417C1B81DBC9B4142AA3B3"
            dynamic1_value = "010622C4"
            dynamic2_value = "027CA074"
        elif version_variable == "1.1.1":
            text_fix = f'''
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
            replacement_value = "0382413C"
            inventory_value = "019C013C"
            hestu_value = "01ED6710"
            DOF_value = "00C25898"
            shadow1_value = "00BF002C"
            shadow2_value = "00BF0030"
            reduction_value = "00CC1C2C"
            fxaa_value = "00CC1C10"
            fsr_value = "00CC1C20"
            nsobidid = "168DD518D925C7A327677286E72FEDA833314919"
            trilinear_value = "0069B218"
            anisotropic_value = "008714D0"
            dynamic1_value = "01063774"
            dynamic2_value = "027D13D4"
            chuck_1008 = f'''00CECA44 F50300AA
00CECA48 993FFF97
00CECA4C 140040B9
00CECA50 E00315AA
00CECA5C F50700F9
00CECA60 08E080D2
00CECA64 097E80D2
00CECA68 0001221E
00CECA6C 0001221E
00CECA74 2101221E'''
            cutscene_code = f'''0081FF10 A5881294
00CC21A4 97D001D0
00CC21A8 F73644F9
00CC21AC F7020391
00CC21B0 E9024039
00CC21B4 29050011
00CC21B8 F503092A
00CC21BC C0035FD6'''
            fps60_code = f'''00ECF81C 21008052
0081FFB8 35008052
00820028 28008052
0081FFC0 2C008052
0081FF0C EB031F2A
019BCC40 1F2003D5
019C84D8 1F2003D5'''
            fps30_code = f'''00ECF81C 41008052
0081FFB8 55008052
00820028 48008052
0081FFC0 4C008052
0081FF0C EB031F2A
019BCC40 1F2003D5
019C84D8 1F2003D5
0081FF10 55008052
0081FF44 41008052'''
            fps20_code = f'''00ECF81C 61008052
0081FFB8 75008052
00820028 68008052
0081FFC0 6C008052
0081FF0C EB031F2A
019BCC40 1F2003D5
019C84D8 1F2003D5
0081FF10 75008052
0081FF44 61008052'''
        elif version_variable == "1.1.2":
            text_fix = f'''
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
            replacement_value = "03813D0C"
            inventory_value = "019B5480"
            hestu_value = "01ECE314"
            shadow1_value = "00BD2BFC"
            shadow2_value = "00BD2C00"
            fxaa_value = "00C76FE0"
            reduction_value = "00C76FFC"
            DOF_value = "00C4B934"
            fsr_value = "00C76FF0"
            nsobidid = "9A10ED9435C06733DA597D8094D9000AB5D3EE60"
            trilinear_value = "00753AA4"
            anisotropic_value = "00BF21F0"
            dynamic1_value = "0104A704"
            dynamic2_value = "027C1124"
            fps60_code = f'''00EAC370 21008052
008F67A4 35008052
008F6814 28008052
008F67AC 2C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5'''
            fps30_code = f'''00EAC370 41008052
008F67A4 55008052
008F6814 48008052
008F67AC 4C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 55008052
008F6730 41008052'''
            fps20_code = f'''00EAC370 61008052
008F67A4 75008052
008F6814 68008052
008F67AC 6C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 75008052
008F6730 61008052'''
            chuck_1008 = f'''00CDD3C4 F50300AA
00CDD3C8 2D52FE97
00CDD3CC 140040B9
00CDD3D0 E00315AA
00CDD3DC F50700F9
00CDD3E0 08E080D2
00CDD3E4 097E80D2
00CDD3E8 0001221E
00CDD3EC 0001221E
00CDD3F4 2101221E'''
            cutscene_code = f'''008F66FC 9E030E94
00C77574 77D201F0
00C77578 F77646F9
00C7757C F7020391
00C77580 E9024039
00C77584 29050011
00C77588 F503092A
00C7758C C0035FD6'''
        elif version_variable == "1.2.0":
            text_fix = f'''
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
            replacement_value = "0380794c"
            inventory_value = "019a5870"
            hestu_value = "01ECE314"
            shadow1_value = "00BD2BFC"
            shadow2_value = "00BD2C00"
            fxaa_value = "00C76FE0"
            reduction_value = "00C76FFC"
            DOF_value = "00C4B934"
            fsr_value = "00C76FF0"
            nsobidid = "6F32C68DD3BC7D77AA714B80E92A096A737CDA77"
            trilinear_value = "00753AA4"
            anisotropic_value = "00BF21F0"
            dynamic1_value = "0104A704"
            dynamic2_value = "027C1124"
            fps60_code = f'''00EAC370 21008052
008F67A4 35008052
008F6814 28008052
008F67AC 2C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5'''
            fps30_code = f'''00EAC370 41008052
008F67A4 55008052
008F6814 48008052
008F67AC 4C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 55008052
008F6730 41008052'''
            fps20_code = f'''00EAC370 61008052
008F67A4 75008052
008F6814 68008052
008F67AC 6C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 75008052
008F6730 61008052'''
            chuck_1008 = f'''00CDD3C4 F50300AA
00CDD3C8 2D52FE97
00CDD3CC 140040B9
00CDD3D0 E00315AA
00CDD3DC F50700F9
00CDD3E0 08E080D2
00CDD3E4 097E80D2
00CDD3E8 0001221E
00CDD3EC 0001221E
00CDD3F4 2101221E'''
            cutscene_code = f'''008F66FC 9E030E94
00C77574 77D201F0
00C77578 F77646F9
00C7757C F7020391
00C77580 E9024039
00C77584 29050011
00C77588 F503092A
00C7758C C0035FD6'''
        else:
            replacement_value = "00CCB094" 
            inventory_value = "019B5480"
            hestu_value = "01ECE314"
            nsobidid = "9A10ED9435C06733DA597D8094D9000AB5D3EE60"
            trilinear_value = "4A008052"
            anisotropic_value = "28E0A0F2"
            fxaa1_value = "027D149C"
            fxaa2_value = "0188CC50"
            DOF_value = "00BD0F14"
            shadow1_value = "00BD2BFC"
            fsr_value = "00CC1C20"
            reduction_value = "00C40A8C"
            shadow2_value = "00BD2C00"
            dynamic1_value = "0103474C"
            dynamic2_value = "02760D24"
        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{replacement_value} {ratiotohex.float2hex(ratio_value)}
{inventory_value} {hex_value}
{hestu_value} {hex_value}
{text_fix}
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
