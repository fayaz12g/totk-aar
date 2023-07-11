import ast
import sys
import subprocess

def create_visuals(do_dynamicfps, do_disable_fxaa, do_disable_fsr, do_DOF, do_disable_reduction, do_disable_ansiotropic, do_cutscene_fix, do_disable_dynamicres, do_force_trilinear, do_chuck, staticfps, shadow_quality):
    DOF_replace = "C0035FD6"
    shadow2_replace = "17000014"
    reduction_replace = "C0000014"
    FSR_replace = "08008052"
    dynamic1_replace = "15000014"
    dynamic2_replace = "000080D2"
    trilinear_replace = "4A008052"
    ansiotropic_replace = "28E0A0F2"
    fxaa_replace = "08008052"
    if staticfps:
        staticfps = float(staticfps)
    if shadow_quality:
        shadow_quality = float(shadow_quality)
    visual_fixes = []
    
    version_variables = ["1.0.0", "1.1.0", "1.1.1", "1.1.2", "1.2.0"]
        
    for version_variable in version_variables:
            
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
        
        if version_variable == "1.0.0":
            DOF_value = "00BD0F14"
            shadow1_value = "00B7214C"
            shadow2_value = "00B72150"
            reduction_value = "00C40A8C"
            fsr_value = "00C40A70"
            fxaa_value = "00C40A70"
            dynamic1_value = "0103474C"
            dynamic2_value = "02760D24"
            trilinear_value = "0070CD2C"
            ansiotropic_value = "00895558"
            fps20_code = f'''
@stop
// Set the Static FPS to 20
@enabled
00E9D8A0 61008052
008F6D90 75008052
008F6C74 68008052
0196591C 6C008052
019707AC EB031F2A
008F6C78 1F2003D5
008F6CAC 1F2003D5
008F6D28 75008052
008F6D20 61008052'''
            fps30_code = f'''
@stop
// Set the Static FPS to 30
@enabled
00E9D8A0 41008052
008F6D90 48008052
008F6C74 EB031F2A
0196591C 1F2003D5
019707AC 1F2003D5
008F6C78 55008052
008F6CAC 41008052
008F6D28 4C008052
008F6D20 55008052'''
            fps60_code = f'''
@stop
// Set the Static FPS to 60
@enabled
00E9D8A0 21008052
008F6D20 35008052
008F6D90 28008052
008F6D28 2C008052
008F6C74 EB031F2A
0196591C 1F2003D5
019707AC 1F2003D5'''
            cutscene_code = f'''
@stop
// Sync Cutscene FPS to Game FPS
@enabled
008F6C78 C4280D94
00C40F88 97CD0190
00C40F8C F7DE46F9
00C40F90 F7020391
00C40F94 E9024039
00C40F98 29050011
00C40F9C F503092A
00C40FA0 C0035FD6'''
            chuck_1008 = f'''
@stop
// Set Internal Resolution to 1008
@enabled
00CEA5BC F50300AA
00CEA5C0 83F6FE97
00CEA5C4 140040B9
00CEA5C8 E00315AA
00CEA5D4 F50700F9
00CEA5D8 08E080D2
00CEA5DC 097E80D2
00CEA5E0 0001221E
00CEA5E4 0001221E
00CEA5EC 2101221E'''
            visual_fixese = ""
            if do_disable_fxaa:
                visual_fixese += f"@stop\n// Disable FXAA\n@enable\n{fxaa_value} {fxaa_replace}\n"
            if do_DOF:
                visual_fixese += f"@stop\n// Disable DOF Targeting\n@enable\n{DOF_value} {DOF_replace}\n"
            if do_disable_fsr:
                visual_fixese += f"@stop\n// Disable FSR\n@enable\n{fsr_value} {FSR_replace}\n"
            if do_disable_reduction:
                visual_fixese += f"@stop\n// Disable Quality Reduction\n@enable\n{reduction_value} {reduction_replace}\n"
            if do_disable_ansiotropic:
                visual_fixese += f"@stop\n// Disable Ansiotropic Filtering\n@enable\n{ansiotropic_value} {ansiotropic_replace}\n"
            if do_disable_dynamicres:
                visual_fixese += f"@stop\n// Disable Dynamic Resolution\n@enable\n{dynamic1_value} {dynamic1_replace}\n"
                visual_fixese += f"{dynamic2_value} {dynamic2_replace}\n"
            if do_force_trilinear:
                visual_fixese += f"@stop\n// Force Trilinear Scaling\n@enable\n{trilinear_value} {trilinear_replace}\n"
            if do_cutscene_fix:
                visual_fixese += f"{cutscene_code}\n"
            if do_chuck:
                visual_fixese += f"{chuck_1008}\n"
            if staticfps == 60:
                visual_fixese += f"{fps60_code}\n"
            if staticfps == 30:
                visual_fixese += f"{fps30_code}\n"
            if staticfps == 20:
                visual_fixese += f"{fps20_code}\n"
            if shadow_quality > 0:
                visual_fixese += f"@stop\n// Set the shaow resolution to {shadow_quality}\n@enable\n{shadow1_value} {shadow1_replace}\n"
                visual_fixese += f"{shadow2_value} {shadow2_replace}\n"
            visual_fixes.append(visual_fixese)
        elif version_variable == "1.1.0":
            chuck_1008 = f'''
@stop
// Set Internal Resolution to 1008
@enabled            
00CEA5BC F50300AA
00CEA5C0 83F6FE97
00CEA5C4 140040B9
00CEA5C8 E00315AA
00CEA5D4 F50700F9
00CEA5D8 08E080D2
00CEA5DC 097E80D2
00CEA5E0 0001221E
00CEA5E4 0001221E
00CEA5EC 2101221E'''
            fps30_code = f'''
@stop
// Set the Static FPS to 30
@enabled            
00EBD158 41008052
0090EA38 55008052
0090EAA8 48008052
0090EA40 4C008052
0090E98C EB031F2A
019BF104 1F2003D5
019CA668 1F2003D5
0090E990 55008052
0090E9C4 41008052'''
            fps60_code = f'''
@stop
// Set the Static FPS to 60
@enabled
00EBD158 21008052
0090EA38 35008052
0090EAA8 28008052
0090EA40 2C008052
0090E98C EB031F2A
019BF104 1F2003D5
019CA668 1F2003D5'''
            cutscene_code = f'''
@stop
// Sync Cutscene FPS to Game FPS
@enabled
0090E990 CD7B0E94
00CAD8C4 F7D001F0
00CAD8C8 F79E44F9
00CAD8CC F7020391
00CAD8D0 E9024039
00CAD8D4 29050011
00CAD8D8 F503092A
00CAD8DC C0035FD6'''
            fps20_code = f'''
@stop
// Set the Static FPS to 20
@enabled
00EBD158 61008052
0090EA38 75008052
0090EAA8 68008052
0090EA40 6C008052
0090E98C EB031F2A
019BF104 1F2003D5
019CA668 1F2003D5
0090E990 75008052
0090E9C4 61008052'''
            shadow1_value = "00D075AC"
            shadow2_value = "00D075B0"
            DOF_value = "00C488B4"
            reduction_value = "00CAD34C"
            trilinear_value = "007639FC"
            ansiotropic_value = "00C7F700"
            fxaa_value = "00CAD330"
            fsr_value = "00CAD340"
            dynamic1_value = "010622C4"
            dynamic2_value = "027CA074"
            visual_fixesa = ""
            if do_disable_fxaa:
                visual_fixesa += f"@stop\n// Disable FXAA\n@enable\n{fxaa_value} {fxaa_replace}\n"
            if do_DOF:
                visual_fixesa += f"@stop\n// Disable DOF Targeting\n@enable\n{DOF_value} {DOF_replace}\n"
            if do_disable_fsr:
                visual_fixesa += f"@stop\n// Disable FSR\n@enable\n{fsr_value} {FSR_replace}\n"
            if do_disable_reduction:
                visual_fixesa += f"@stop\n// Disable Quality Reduction\n@enable\n{reduction_value} {reduction_replace}\n"
            if do_disable_ansiotropic:
                visual_fixesa += f"@stop\n// Disable Ansiotropic Filtering\n@enable\n{ansiotropic_value} {ansiotropic_replace}\n"
            if do_disable_dynamicres:
                visual_fixesa += f"@stop\n// Disable Dynamic Resolution\n@enable\n{dynamic1_value} {dynamic1_replace}\n"
                visual_fixesa += f"{dynamic2_value} {dynamic2_replace}\n"
            if do_force_trilinear:
                visual_fixesa += f"@stop\n// Force Trilinear Scaling\n@enable\n{trilinear_value} {trilinear_replace}\n"
            if do_cutscene_fix:
                visual_fixesa += f"{cutscene_code}\n"
            if do_chuck:
                visual_fixesa += f"{chuck_1008}\n"
            if staticfps == 60:
                visual_fixesa += f"{fps60_code}\n"
            if staticfps == 30:
                visual_fixesa += f"{fps30_code}\n"
            if staticfps == 20:
                visual_fixesa += f"{fps20_code}\n"
            if shadow_quality > 0:
                visual_fixesa += f"@stop\n// Set the shaow resolution to {shadow_quality}\n@enable\n{shadow1_value} {shadow1_replace}\n"
                visual_fixesa += f"{shadow2_value} {shadow2_replace}\n"
            visual_fixes.append(visual_fixesa)
        elif version_variable == "1.1.1":
            DOF_value = "00C25898"
            shadow1_value = "00BF002C"
            shadow2_value = "00BF0030"
            reduction_value = "00CC1C2C"
            fxaa_value = "00CC1C10"
            fsr_value = "00CC1C20"
            trilinear_value = "0069B218"
            ansiotropic_value = "008714D0"
            dynamic1_value = "01063774"
            dynamic2_value = "027D13D4"
            chuck_1008 = f'''
@stop
// Set Internal Resolution to 1008
@enabled
00CECA44 F50300AA
00CECA48 993FFF97
00CECA4C 140040B9
00CECA50 E00315AA
00CECA5C F50700F9
00CECA60 08E080D2
00CECA64 097E80D2
00CECA68 0001221E
00CECA6C 0001221E
00CECA74 2101221E'''
            cutscene_code = f'''
@stop
// Sync Cutscene FPS to Game FPS
@enabled
0081FF10 A5881294
00CC21A4 97D001D0
00CC21A8 F73644F9
00CC21AC F7020391
00CC21B0 E9024039
00CC21B4 29050011
00CC21B8 F503092A
00CC21BC C0035FD6'''
            fps60_code = f'''
@stop
// Set the Static FPS to 60
@enabled            
00ECF81C 21008052
0081FFB8 35008052
00820028 28008052
0081FFC0 2C008052
0081FF0C EB031F2A
019BCC40 1F2003D5
019C84D8 1F2003D5'''
            fps30_code = f'''
@stop
// Set the Static FPS to 30
@enabled            
00ECF81C 41008052
0081FFB8 55008052
00820028 48008052
0081FFC0 4C008052
0081FF0C EB031F2A
019BCC40 1F2003D5
019C84D8 1F2003D5
0081FF10 55008052
0081FF44 41008052'''
            fps20_code = f'''
@stop
// Set the Static FPS to 20
@enabled            
00ECF81C 61008052
0081FFB8 75008052
00820028 68008052
0081FFC0 6C008052
0081FF0C EB031F2A
019BCC40 1F2003D5
019C84D8 1F2003D5
0081FF10 75008052
0081FF44 61008052'''
            visual_fixesb = ""
            if do_disable_fxaa:
                visual_fixesb += f"@stop\n// Disable FXAA\n@enable\n{fxaa_value} {fxaa_replace}\n"
            if do_DOF:
                visual_fixesb += f"@stop\n// Disable DOF Targeting\n@enable\n{DOF_value} {DOF_replace}\n"
            if do_disable_fsr:
                visual_fixesb += f"@stop\n// Disable FSR\n@enable\n{fsr_value} {FSR_replace}\n"
            if do_disable_reduction:
                visual_fixesb += f"@stop\n// Disable Quality Reduction\n@enable\n{reduction_value} {reduction_replace}\n"
            if do_disable_ansiotropic:
                visual_fixesb += f"@stop\n// Disable Ansiotropic Filtering\n@enable\n{ansiotropic_value} {ansiotropic_replace}\n"
            if do_disable_dynamicres:
                visual_fixesb += f"@stop\n// Disable Dynamic Resolution\n@enable\n{dynamic1_value} {dynamic1_replace}\n"
                visual_fixesb += f"{dynamic2_value} {dynamic2_replace}\n"
            if do_force_trilinear:
                visual_fixesb += f"@stop\n// Force Trilinear Scaling\n@enable\n{trilinear_value} {trilinear_replace}\n"
            if do_cutscene_fix:
                visual_fixesb += f"{cutscene_code}\n"
            if do_chuck:
                visual_fixesb += f"{chuck_1008}\n"
            if staticfps == 60:
                visual_fixesb += f"{fps60_code}\n"
            if staticfps == 30:
                visual_fixesb += f"{fps30_code}\n"
            if staticfps == 20:
                visual_fixesb += f"{fps20_code}\n"
            if shadow_quality > 0:
                visual_fixesb += f"@stop\n// Set the shaow resolution to {shadow_quality}\n@enable\n{shadow1_value} {shadow1_replace}\n"
                visual_fixesb += f"{shadow2_value} {shadow2_replace}\n"
            visual_fixes.append(visual_fixesb)
        elif version_variable == "1.1.2":
            shadow1_value = "00BD2BFC"
            shadow2_value = "00BD2C00"
            fxaa_value = "00C76FE0"
            reduction_value = "00C76FFC"
            DOF_value = "00C4B934"
            fsr_value = "00C76FF0"
            trilinear_value = "00753AA4"
            ansiotropic_value = "00BF21F0"
            dynamic1_value = "0104A704"
            dynamic2_value = "027C1124"
            fps60_code = f'''
@stop
// Set the Static FPS to 60
@enabled
00EAC370 21008052
008F67A4 35008052
008F6814 28008052
008F67AC 2C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5'''
            fps30_code = f'''
@stop
// Set the Static FPS to 30
@enabled
00EAC370 41008052
008F67A4 55008052
008F6814 48008052
008F67AC 4C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 55008052
008F6730 41008052'''
            fps20_code = f'''
@stop
// Set the Static FPS to 20
@enabled        
00EAC370 61008052
008F67A4 75008052
008F6814 68008052
008F67AC 6C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 75008052
008F6730 61008052'''
            chuck_1008 = f'''
@stop
// Set Internal Resolution to 1008
@enabled
00CDD3C4 F50300AA
00CDD3C8 2D52FE97
00CDD3CC 140040B9
00CDD3D0 E00315AA
00CDD3DC F50700F9
00CDD3E0 08E080D2
00CDD3E4 097E80D2
00CDD3E8 0001221E
00CDD3EC 0001221E
00CDD3F4 2101221E'''
            cutscene_code = f'''
@stop
// Sync Cutscene FPS to Game FPS
@enabled            
008F66FC 9E030E94
00C77574 77D201F0
00C77578 F77646F9
00C7757C F7020391
00C77580 E9024039
00C77584 29050011
00C77588 F503092A
00C7758C C0035FD6'''
            visual_fixesc = ""
            if do_disable_fxaa:
                visual_fixesc += f"@stop\n// Disable FXAA\n@enable\n{fxaa_value} {fxaa_replace}\n"
            if do_DOF:
                visual_fixesc += f"@stop\n// Disable DOF Targeting\n@enable\n{DOF_value} {DOF_replace}\n"
            if do_disable_fsr:
                visual_fixesc += f"@stop\n// Disable FSR\n@enable\n{fsr_value} {FSR_replace}\n"
            if do_disable_reduction:
                visual_fixesc += f"@stop\n// Disable Quality Reduction\n@enable\n{reduction_value} {reduction_replace}\n"
            if do_disable_ansiotropic:
                visual_fixesc += f"@stop\n// Disable Ansiotropic Filtering\n@enable\n{ansiotropic_value} {ansiotropic_replace}\n"
            if do_disable_dynamicres:
                visual_fixesc += f"@stop\n// Disable Dynamic Resolution\n@enable\n{dynamic1_value} {dynamic1_replace}\n"
                visual_fixesc += f"{dynamic2_value} {dynamic2_replace}\n"
            if do_force_trilinear:
                visual_fixesc += f"@stop\n// Force Trilinear Scaling\n@enable\n{trilinear_value} {trilinear_replace}\n"
            if do_cutscene_fix:
                visual_fixesc += f"{cutscene_code}\n"
            if do_chuck:
                visual_fixesc += f"{chuck_1008}\n"
            if staticfps == 60:
                visual_fixesc += f"{fps60_code}\n"
            if staticfps == 30:
                visual_fixesc += f"{fps30_code}\n"
            if staticfps == 20:
                visual_fixesc += f"{fps20_code}\n"
            if shadow_quality > 0:
                visual_fixesc += f"@stop\n// Set the shaow resolution to {shadow_quality}\n@enable\n{shadow1_value} {shadow1_replace}\n"
                visual_fixesc += f"{shadow2_value} {shadow2_replace}\n"
            visual_fixes.append(visual_fixesc)
        elif version_variable == "1.2.0":
            shadow1_value = "00BD2BFC"
            shadow2_value = "00BD2C00"
            fxaa_value = "00C76FE0"
            reduction_value = "00C76FFC"
            DOF_value = "00C4B934"
            fsr_value = "00C76FF0"
            trilinear_value = "00753AA4"
            ansiotropic_value = "00BF21F0"
            dynamic1_value = "0104A704"
            dynamic2_value = "027C1124"
            fps60_code = f'''
@stop
// Set the Static FPS to 60
@enabled
00EAC370 21008052
008F67A4 35008052
008F6814 28008052
008F67AC 2C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5'''
            fps30_code = f'''
@stop
// Set the Static FPS to 30
@enabled            
00EAC370 41008052
008F67A4 55008052
008F6814 48008052
008F67AC 4C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 55008052
008F6730 41008052'''
            fps20_code = f'''
@stop
// Set the Static FPS to 20
@enabled         
00EAC370 61008052
008F67A4 75008052
008F6814 68008052
008F67AC 6C008052
008F66F8 EB031F2A
019B1F84 1F2003D5
019BD9E8 1F2003D5
008F66FC 75008052
008F6730 61008052'''
            chuck_1008 = f'''
@stop
// Set Internal Resolution to 1008
@enabled
00CDD3C4 F50300AA
00CDD3C8 2D52FE97
00CDD3CC 140040B9
00CDD3D0 E00315AA
00CDD3DC F50700F9
00CDD3E0 08E080D2
00CDD3E4 097E80D2
00CDD3E8 0001221E
00CDD3EC 0001221E
00CDD3F4 2101221E'''
            cutscene_code = f'''
@stop
// Sync Cutscene FPS to Game FPS
@enabled            
008F66FC 9E030E94
00C77574 77D201F0
00C77578 F77646F9
00C7757C F7020391
00C77580 E9024039
00C77584 29050011
00C77588 F503092A
00C7758C C0035FD6'''
            visual_fixesd = ""
            if do_disable_fxaa:
                visual_fixesd += f"@stop\n// Disable FXAA\n@enable\n{fxaa_value} {fxaa_replace}\n"
            if do_DOF:
                visual_fixesd += f"@stop\n// Disable DOF Targeting\n@enable\n{DOF_value} {DOF_replace}\n"
            if do_disable_fsr:
                visual_fixesd += f"@stop\n// Disable FSR\n@enable\n{fsr_value} {FSR_replace}\n"
            if do_disable_reduction:
                visual_fixesd += f"@stop\n// Disable Quality Reduction\n@enable\n{reduction_value} {reduction_replace}\n"
            if do_disable_ansiotropic:
                visual_fixesd += f"@stop\n// Disable Ansiotropic Filtering\n@enable\n{ansiotropic_value} {ansiotropic_replace}\n"
            if do_disable_dynamicres:
                visual_fixesd += f"@stop\n// Disable Dynamic Resolution\n@enable\n{dynamic1_value} {dynamic1_replace}\n"
                visual_fixesd += f"{dynamic2_value} {dynamic2_replace}\n"
            if do_force_trilinear:
                visual_fixesd += f"@stop\n// Force Trilinear Scaling\n@enable\n{trilinear_value} {trilinear_replace}\n"
            if do_cutscene_fix:
                visual_fixesd += f"{cutscene_code}\n"
            if do_chuck:
                visual_fixesd += f"{chuck_1008}\n"
            if staticfps == 60:
                visual_fixesd += f"{fps60_code}\n"
            if staticfps == 30:
                visual_fixesd += f"{fps30_code}\n"
            if staticfps == 20:
                visual_fixesd += f"{fps20_code}\n"
            if shadow_quality > 0:
                visual_fixesd += f"@stop\n// Set the shaow resolution to {shadow_quality}\n@enable\n{shadow1_value} {shadow1_replace}\n"
                visual_fixesd += f"{shadow2_value} {shadow2_replace}\n"
            visual_fixes.append(visual_fixesd)
        if do_dynamicfps:
            print("A future version will copy the dynamic fps file!")
        
    return visual_fixes