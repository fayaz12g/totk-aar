
def create_visualsnew(do_camera, res_multiplier, lod_improve, remove_flare, staticfps, shadow_quality, do_dynamicfps, do_disable_fxaa, do_disable_fsr, do_DOF, do_disable_reduction, do_disable_ansiotropic, do_cutscene_fix, do_disable_dynamicres, do_force_trilinear, do_chuck):

    qualityreduction = "disabled"
    lodimprove = "disabled"
    disablefxaa = "disabled"
    disableDOF = "disabled"
    disablefsr = "disabled"
    disableansiotropic = "disabled"
    disabledynamicres = "disabled"
    removelens = "disabled"
    forectri = "disabled"
    cutscene = "disabled"
    skyfix = "disabled"
    camspeed = "disabled"
    internalres = "disabled"
    staticfps20 = "disabled"
    staticfps30 = "disabled"
    staticfps60 = "disabled"
    setshadowres = "disabled"
    do_island = False
    
    visual_fixes = []
        
    if res_multiplier == "2" or res_multiplier == "3" or res_multiplier == "4" or res_multiplier == "5" or res_multiplier == "6" or res_multiplier == "7":
        res_multiplier = float(res_multiplier)
        do_island = True
    else:
        res_multiplier = 0
        res_multiplier = float(res_multiplier)
        island_replace = "1B10201E"
    if res_multiplier == 2:
        island_replace = "1B10201E"
    if res_multiplier == 3:
        island_replace = "1B10211E"
    if res_multiplier == 4:
        island_replace = "1B10221E"
    if res_multiplier == 5:
        island_replace = "1B90221E"
    if res_multiplier == 6:
        island_replace = "1B10231E"
    if res_multiplier == 7:
        island_replace = "1B90231E"
    if res_multiplier == 8:
        island_replace = "1B10241E"
        
    if staticfps == "20" or staticfps == "30" or staticfps == "60":
        staticfps = float(staticfps)
    else:
        staticfps = 0.0
        staticfps = float(staticfps)
    
    if shadow_quality == "":
        shadow_quality = 0
        shadow1_replace = "0B018052"
        shadow_quality = float(shadow_quality)
        
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
    

    if do_island:
        skyfix = "enabled"
    if do_disable_reduction:
        qualityreduction = "enabled"
    if lod_improve:
        lodimprove = "enabled"
    if do_camera:
        camspeed = "enabled"
    if do_disable_fxaa:
        disablefxaa = "enabled"
    if do_DOF:
        disableDOF = "enabled"
    if do_disable_fsr:
        disablefsr = "enabled"
    if do_disable_ansiotropic:
        disableansiotropic = "enabled"
    if do_disable_dynamicres:
        disabledynamicres = "enabled"
    if do_force_trilinear:
        forectri = "enabled"
    if remove_flare:
        removelens = "enabled"
    if do_cutscene_fix:
        cutscene = "enabled"
    if do_chuck:
        internalres = "enabled"
    if staticfps == 60:
        staticfps60 = "enabled"
    if staticfps == 30:
        staticfps30 = "enabled"
    if staticfps == 20:
        staticfps20 = "enabled"
    if shadow_quality > 0:
        setshadowres = "enabled"
        
    visuals1_0_0 = f'''// Disable Quality Reduction
    @{qualityreduction}
    00C40A8C C0000014
    @stop

    // Improve the LOD (Level of Detail)
    @{lodimprove}
    027D9448 24000014
    @stop

    // Disable FXAA
    @{disablefxaa}
    00C40A70 08008052
    @stop

    // Disable DOF Targeting
    @{disableDOF}
    00BD0F14 C0035FD6
    @stop

    //// Disable FSR
    @{disablefsr}
    00C40A70 08008052
    @stop

    // Disable Ansiiotropic Filtering
    @{disableansiotropic}
    00895558 28E0A0F2
    @stop

    // Disable Dynamic Resolution
    @{disabledynamicres}
    0103474C 15000014
    02760D24 000080D2
    @stop

    // Remove Lens Flare
    @{removelens}
    029ca250 1F2003D5
    @stop

    // Force Trilinear Scaling
    @{forectri}
    0070CD2C 4A008052
    @stop

    // Sync Cutscene FPS to Game FPS
    @{cutscene}
    008F6C78 C4280D94
    00C40F88 97CD0190
    00C40F8C F7DE46F9
    00C40F90 F7020391
    00C40F94 E9024039
    00C40F98 29050011
    00C40F9C F503092A
    00C40FA0 C0035FD6
    @stop

    e // Fix the Rendering of Sky Islands When Using a Multiplier of {int(res_multiplier)}x
    @{skyfix}
    029d1510 {island_replace}
    029d1518 BF000014
    029d1814 00083B1E
    029d1818 21083B1E
    @stop

    // Increase the Camera Speed
    @{camspeed}
    03775f6c 0000A03f
    00d0531c 09902E1E
    @stop

    // Set Internal Resolution to 1008p
    @{internalres}
    00CEA5BC F50300AA
    00CEA5C0 83F6FE97
    00CEA5C4 140040B9
    00CEA5C8 E00315AA
    00CEA5D4 F50700F9
    00CEA5D8 08E080D2
    00CEA5DC 097E80D2
    00CEA5E0 0001221E
    00CEA5E4 0001221E
    00CEA5EC 2101221E
    @stop

    // Set the Static FPS to 30
    @{staticfps30}
    00E9D8A0 41008052
    008F6D90 48008052
    008F6C74 EB031F2A
    0196591C 1F2003D5
    019707AC 1F2003D5
    008F6C78 55008052
    008F6CAC 41008052
    008F6D28 4C008052
    008F6D20 55008052
    @stop
    
    // Set the Static FPS to 20
    @{staticfps20}
    00E9D8A0 61008052
    008F6D90 75008052
    008F6C74 68008052
    0196591C 6C008052
    019707AC EB031F2A
    008F6C78 1F2003D5
    008F6CAC 1F2003D5
    008F6D28 75008052
    008F6D20 61008052
    @stop
    
    // Set the Static FPS to 60
    @{staticfps60}
    00E9D8A0 21008052
    008F6D20 35008052
    008F6D90 28008052
    008F6D28 2C008052
    008F6C74 EB031F2A
    0196591C 1F2003D5
    019707AC 1F2003D5
    @stop

    // Set the Shadow Resolution to {int(shadow_quality)}
    @{setshadowres}
    00B7214C {shadow1_replace}
    00B72150 17000014
    @stop
    '''

    visuals1_1_0= f'''e // Fix the Rendering of Sky Islands When Using a Multiplier of {int(res_multiplier)}x
    @{skyfix}
    02a498d0 {island_replace}
    02a498d8 BF000014
    02a49bd4 00083B1E
    02a49bd8 21083B1E
    @stop

    // Disable Quality Reduction
    @{qualityreduction}
    00CAD34C C0000014
    @stop

    // Improve the LOD (Level of Detail)
    @{lodimprove}
    027D9448 24000014
    @stop

    // Increase the Camera Speed
    @{camspeed}
    0381648C 0000A03f
    00D228DC 09902E1E
    @stop

    // Disable FXAA
    @{disablefxaa}
    00CAD330 08008052
    @stop

    // Disable DOF Targeting
    @{disableDOF}
    00C488B4 C0035FD6
    @stop

    //// Disable FSR
    @{disablefsr}
    00CAD340 08008052
    @stop

    // Disable Ansiiotropic Filtering
    @{disableansiotropic}
    00C7F700 28E0A0F2
    @stop

    // Disable Dynamic Resolution
    @{disabledynamicres}
    010622C4 15000014
    027CA074 000080D2
    @stop

    // Force Trilinear Scaling
    @{forectri}
    007639FC 4A008052
    @stop

    // Remove Lens Flare
    @{removelens}
    02A42490 1F2003D5
    @stop

    // Sync Cutscene FPS to Game FPS
    @{cutscene}
    0090E990 CD7B0E94
    00CAD8C4 F7D001F0
    00CAD8C8 F79E44F9
    00CAD8CC F7020391
    00CAD8D0 E9024039
    00CAD8D4 29050011
    00CAD8D8 F503092A
    00CAD8DC C0035FD6
    @stop

    // Set Internal Resolution to 1008p
    @{internalres}            
    00CEA5BC F50300AA
    00CEA5C0 83F6FE97
    00CEA5C4 140040B9
    00CEA5C8 E00315AA
    00CEA5D4 F50700F9
    00CEA5D8 08E080D2
    00CEA5DC 097E80D2
    00CEA5E0 0001221E
    00CEA5E4 0001221E
    00CEA5EC 2101221E
    @stop

    // Set the Static FPS to 30
    @{staticfps30}            
    00EBD158 41008052
    0090EA38 55008052
    0090EAA8 48008052
    0090EA40 4C008052
    0090E98C EB031F2A
    019BF104 1F2003D5
    019CA668 1F2003D5
    0090E990 55008052
    0090E9C4 41008052
    @stop

    // Set the Static FPS to 20
    @{staticfps20}
    00EBD158 61008052
    0090EA38 75008052
    0090EAA8 68008052
    0090EA40 6C008052
    0090E98C EB031F2A
    019BF104 1F2003D5
    019CA668 1F2003D5
    0090E990 75008052
    0090E9C4 61008052
    @stop
    
    // Set the Static FPS to 60
    @{staticfps60}
    00EBD158 21008052
    0090EA38 35008052
    0090EAA8 28008052
    0090EA40 2C008052
    0090E98C EB031F2A
    019BF104 1F2003D5
    019CA668 1F2003D5
    @stop
    
    // Set the Shadow Resolution to {int(shadow_quality)}
    @{setshadowres}
    00D075AC {shadow1_replace}
    00D075B0 17000014
    @stop
    '''

    visuals1_1_1 = f'''e // Fix the Rendering of Sky Islands When Using a Multiplier of {int(res_multiplier)}x
    @{skyfix}
    02a51630 {island_replace}
    02a51638 BF000014
    02a51934 00083B1E
    02a51938 21083B1E
    @stop

    // Disable Quality Reduction
    @{qualityreduction}
    00CC1C2C C0000014
    @stop

    // Improve the LOD (Level of Detail)
    @{lodimprove}
    027E07A8 24000014
    @stop

    // Increase the Camera Speed
    @{camspeed}
    0381f26c 0000A03f
    00d01e4c 09902E1E
    @stop

    // Disable FXAA
    @{disablefxaa}
    00CC1C10 08008052
    @stop

    // Disable DOF Targeting
    @{disableDOF}
    00C25898 C0035FD6
    @stop

    //// Disable FSR
    @{disablefsr}
    00CC1C20 08008052
    @stop

    // Disable Ansiiotropic Filtering
    @{disableansiotropic}
    008714D0 28E0A0F2
    @stop

    // Disable Dynamic Resolution
    @{disabledynamicres}
    01063774 15000014
    027D13D4 000080D2
    @stop

    // Force Trilinear Scaling
    @{forectri}
    0069B218 4A008052
    @stop

    // Remove Lens Flare
    @{removelens}
    02A4A1E0 1F2003D5
    @stop

    // Sync Cutscene FPS to Game FPS
    @{cutscene}
    0081FF10 A5881294
    00CC21A4 97D001D0
    00CC21A8 F73644F9
    00CC21AC F7020391
    00CC21B0 E9024039
    00CC21B4 29050011
    00CC21B8 F503092A
    00CC21BC C0035FD6
    @stop

    // Set Internal Resolution to 1008p
    @{internalres}
    00CECA44 F50300AA
    00CECA48 993FFF97
    00CECA4C 140040B9
    00CECA50 E00315AA
    00CECA5C F50700F9
    00CECA60 08E080D2
    00CECA64 097E80D2
    00CECA68 0001221E
    00CECA6C 0001221E
    00CECA74 2101221E
    @stop

    // Set the Static FPS to 30
    @{staticfps30}            
    00ECF81C 41008052
    0081FFB8 55008052
    00820028 48008052
    0081FFC0 4C008052
    0081FF0C EB031F2A
    019BCC40 1F2003D5
    019C84D8 1F2003D5
    0081FF10 55008052
    0081FF44 41008052
    @stop


    // Set the Static FPS to 20
    @{staticfps20}
    00ECF81C 61008052
    0081FFB8 75008052
    00820028 68008052
    0081FFC0 6C008052
    0081FF0C EB031F2A
    019BCC40 1F2003D5
    019C84D8 1F2003D5
    0081FF10 75008052
    0081FF44 61008052
    @stop
    
    // Set the Static FPS to 60
    @{staticfps60}
    00ECF81C 21008052
    0081FFB8 35008052
    00820028 28008052
    0081FFC0 2C008052
    0081FF0C EB031F2A
    019BCC40 1F2003D5
    019C84D8 1F2003D5
    @stop

    
    // Set the Shadow Resolution to {int(shadow_quality)}
    @{setshadowres}
    00BF002C {shadow1_replace}
    00BF0030 17000014
    @stop
    '''

    visuals1_1_2 = f'''e // Fix the Rendering of Sky Islands When Using a Multiplier of {int(res_multiplier)}x
    @{skyfix}
    02A40A40 {island_replace}
    02A40A48 BF000014
    02A40D44 00083B1E
    02A40D48 21083B1E
    @stop

    // Disable Quality Reduction
    @{qualityreduction}
    00C76FFC C0000014
    @stop

    // Improve the LOD (Level of Detail)
    @{lodimprove}
    027D04F8 24000014
    @stop

    // Increase the Camera Speed
    @{camspeed}
    0380ee6c 0000A03f
    00d1411c 09902E1E
    @stop

    // Disable FXAA
    @{disablefxaa}
    00C76FE0 08008052
    @stop

    // Disable DOF Targeting
    @{disableDOF}
    00C4B934 C0035FD6
    @stop

    //// Disable FSR
    @{disablefsr}
    00C76FF0 08008052
    @stop

    // Disable Ansiiotropic Filtering
    @{disableansiotropic}
    00BF21F0 28E0A0F2
    @stop

    // Disable Dynamic Resolution
    @{disabledynamicres}
    0104A704 15000014
    027C1124 000080D2
    @stop

    // Force Trilinear Scaling
    @{forectri}
    00753AA4 4A008052
    @stop

    // Remove Lens Flare
    @{removelens}
    02A395F0 1F2003D5
    @stop

    // Sync Cutscene FPS to Game FPS
    @{cutscene}            
    008F66FC 9E030E94
    00C77574 77D201F0
    00C77578 F77646F9
    00C7757C F7020391
    00C77580 E9024039
    00C77584 29050011
    00C77588 F503092A
    00C7758C C0035FD6
    @stop

    // Set Internal Resolution to 1008p
    @{internalres}
    00CDD3C4 F50300AA
    00CDD3C8 2D52FE97
    00CDD3CC 140040B9
    00CDD3D0 E00315AA
    00CDD3DC F50700F9
    00CDD3E0 08E080D2
    00CDD3E4 097E80D2
    00CDD3E8 0001221E
    00CDD3EC 0001221E
    00CDD3F4 2101221E
    @stop

    // Set the Static FPS to 30
    @{staticfps30}
    00EAC370 41008052
    008F67A4 55008052
    008F6814 48008052
    008F67AC 4C008052
    008F66F8 EB031F2A
    019B1F84 1F2003D5
    019BD9E8 1F2003D5
    008F66FC 55008052
    008F6730 41008052
    @stop

    // Set the Static FPS to 20
    @{staticfps20}
    00EAC370 61008052
    008F67A4 75008052
    008F6814 68008052
    008F67AC 6C008052
    008F66F8 EB031F2A
    019B1F84 1F2003D5
    019BD9E8 1F2003D5
    008F66FC 75008052
    008F6730 61008052
    @stop
    
    // Set the Static FPS to 60
    @{staticfps60}
    00EAC370 21008052
    008F67A4 35008052
    008F6814 28008052
    008F67AC 2C008052
    008F66F8 EB031F2A
    019B1F84 1F2003D5
    019BD9E8 1F2003D5
    @stop
    
    // Set the Shadow Resolution to {int(shadow_quality)}
    @{setshadowres}
    00BD2BFC {shadow1_replace}
    00BD2C00 17000014
    @stop
    '''

    visuals1_2_0 = f'''e // Fix the Rendering of Sky Islands When Using a Multiplier of {int(res_multiplier)}x
    @{skyfix}
    02A348A0 {island_replace}
    02A348A8 BF000014
    02A34BA4 00083B1E
    02A34BA8 21083B1E
    @stop

    // Disable Quality Reduction
    @{qualityreduction}
    00C4275c C0000014
    @stop

    // Improve the LOD (Level of Detail)
    @{lodimprove}
    027c3ea8 24000014
    @stop

    // Increase the Camera Speed
    @{camspeed}
    03802acc 0000A03f
    00ce3834 09902E1E
    @stop

    // Disable FXAA
    @{disablefxaa}
    00C42740 08008052
    @stop

    // Disable DOF Targeting
    @{disableDOF}
    00C07024 C0035FD6
    @stop

    //// Disable FSR
    @{disablefsr}
    00C42750 08008052
    @stop

    // Disable Ansiiotropic Filtering
    @{disableansiotropic}
    00B3BF24 28E0A0F2
    @stop

    // Disable Dynamic Resolution
    @{disabledynamicres}
    0104A704 15000014
    027C1124 000080D2
    @stop

    // Force Trilinear Scaling
    @{forectri}
    00723AE4 4A008052
    @stop

    // Remove Lens Flare
    @{removelens}
    02a2d460 1F2003D5
    @stop

    // Sync Cutscene FPS to Game FPS
    @{cutscene}            
    008F66FC 9E030E94
    00C77574 77D201F0
    00C77578 F77646F9
    00C7757C F7020391
    00C77580 E9024039
    00C77584 29050011
    00C77588 F503092A
    00C7758C C0035FD6
    @stop

    // Set Internal Resolution to 1008p
    @{internalres}
    00c34598 F50300AA
    00c3459c 2D52FE97
    00c345a0 140040B9
    00c345a4 E00315AA
    00c345b0 F50700F9
    00c345b4 08E080D2
    00c345b8 097E80D2
    00c345bc 0001221E
    00c345c0 0001221E
    00c345c8 2101221E
    @stop

    // Set the Static FPS to 30
    @{staticfps30}            
    00ea28dc 41008052
    008a9460 55008052
    008a94d0 48008052
    008a9468 4C008052
    008a93b4 EB031F2A
    019a2374 1F2003D5
    019adbe8 1F2003D5
    008a93b8 55008052
    008a93ec 41008052
    @stop

    // Set the Static FPS to 20
    @{staticfps20}
    00ea28dc 61008052
    008a9460 75008052
    008a94d0 68008052
    008a9468 6C008052
    008a93b4 EB031F2A
    019a2374 1F2003D5
    019adbe8 1F2003D5
    008a93b8 75008052
    008a93ec 61008052
    @stop
    
    // Set the Static FPS to 60
    @{staticfps60}
    00ea28dc 21008052
    008a9460 35008052
    008a94d0 28008052
    008a9468 2C008052
    008a93b4 EB031F2A
    019a2374 1F2003D5
    019adbe8 1F2003D5
    @stop
    
    // Set the Shadow Resolution to {int(shadow_quality)}
    @{setshadowres}
    00ccd368 {shadow1_replace}
    00ccd36c 17000014
    @stop
    '''

    visual_fixes.append(visuals1_0_0)
    visual_fixes.append(visuals1_1_0)
    visual_fixes.append(visuals1_1_1)
    visual_fixes.append(visuals1_1_2)
    visual_fixes.append(visuals1_2_0)
    
    return visual_fixes