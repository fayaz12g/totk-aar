import os
import struct
import sys
import ast
import subprocess


def float_to_hex(f):
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0')

def perform_deck_patching(scaling_factor, centered_HUD, unpacked_folder):
    blyt_folder = unpacked_folder + "\\blyt"
    anim_folder = unpacked_folder + "\\anim"
    scaling_factor = float(scaling_factor)
    shift_factor = (1 - float(scaling_factor) / float(scaling_factor))
    centered_HUD = ast.literal_eval(centered_HUD)
    print("Centered HUD value is set to ", centered_HUD)
    print("The scaling factor is ", scaling_factor)
    file_names = os.listdir(blyt_folder)
    file_names = os.listdir(blyt_folder)
    file_names.remove('AppMenuBG_00.bflyt')
    file_names.remove('PauseMenuBG_00.bflyt')
    file_names.remove('ShopMenuParasailBG_00.bflyt')
    file_names.remove('ShortCutBG_00.bflyt')
    file_names.remove('TitleMenuBG_00.bflyt')
    file_names.remove('PaMap_00.bflyt')
    file_names.remove('EventFade_00.bflyt')
    file_names.remove('EventFadeWipe_00.bflyt')
    file_names.remove('CameraShutter_00.bflyt')

    for name in file_names:
        file_loc = blyt_folder + "\\" + name
        print("Modyfying " + name)
        
        with open(file_loc, 'rb') as f:
            content = f.read().hex()
                
        if name == 'AppMenuOverlay_00.bflyt':
            # Scale N_FadeInOut_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F46616465496E4F75745F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F46616465496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_FadeInOut_01
            x = float_to_hex(scaling_factor)
            source_str = '4E5F46616465496E4F75745F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F46616465496E4F75745F3031000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            with open(file_loc, 'wb') as f:
                f.write(bytes.fromhex(content))            
                continue
                
        # Scale RootPane by scaling_factor
        x = float_to_hex(scaling_factor)
        source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
        replace_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
        content = content.replace(source_str.lower(), replace_str.lower())
        
        # Scale BG_00 by inverse scaling_factor
        x = float_to_hex(1/scaling_factor)
        source_str = '42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
        replace_str = '42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
        content = content.replace(source_str.lower(), replace_str.lower()) 
        
        # Scale BG_00 by inverse scaling_factor
        x = float_to_hex(1/scaling_factor)
        source_str = '42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
        replace_str = '42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
        content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'ShopMenu_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
            # Shift A_AlignGuide_00
            x = float_to_hex(-625)
            source_str = '415F416C69676E47756964655F30300000000000000000000000000000000000000000000080EEC3'
            replace_str = '415F416C69676E47756964655F3030000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Type_00
            x = float_to_hex(-66)
            source_str = '4E5F547970655F303000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F547970655F3030000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'PickUpWin_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'TreasureFullShortCut_00.bflyt':
            # Shift RootPane
            x = float_to_hex(-310)
            source_str = '4E5F47756964655F30300000000000000000000000000000000000000000000000000000000048C3'
            replace_str = '4E5F47756964655F30300000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'AppAlbum_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'AppPictureBook_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'ChallengeLog_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'NumDisplay_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'NumDisplaySecond_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'MiniGameTimer_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
    
        if name == 'InstantTips_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'InstantTipsWithPict_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'DoCommand_00.bflyt':
            # Shift RootPane
            x = float_to_hex(-45)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'Challenge_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'HorseGauge_00.bflyt':
            # Shift RootPane
            x = float_to_hex(-60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'CharaDirectory_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'MessageLog_01.bflyt':
            # Scale P_Capture_00
            x = float_to_hex(1/scaling_factor)
            source_str = '505F436170747572655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '505F436170747572655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift RootPane
            x = float_to_hex(-60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift P_Capture_00
            x = float_to_hex(60)
            source_str = '505F436170747572655F303000000000000000000000000000000000000000000000000000000000'
            replace_str = '505F436170747572655F3030000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'CtrlGuide_00.bflyt':
            # Shift RootPane
            x = float_to_hex(-50)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'SaveLoadIcon_00.bflyt':
            # Shift RootPane
            x = float_to_hex(-65)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'Location_00.bflyt':
            # Shift N_Small_00
            x = float_to_hex(-445)
            source_str = '4E5F536D616C6C5F3030000000000000000000000000000000000000000000000000C2C30080C5C3'
            replace_str = '4E5F536D616C6C5F3030000000000000000000000000000000000000000000000000C2C3' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Large_00
            x = float_to_hex(330)
            source_str = '4E5F4C617267655F3030000000000000000000000000000000000000000000000000000000008743'
            replace_str = '4E5F4C617267655F30300000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'Pouch_00.bflyt':
            # Shift RootPane
            x = float_to_hex(54)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Info_00
            x = float_to_hex(-116)
            source_str = '4E5F496E666F5F303000000000000000000000000000000000000000000000000000304200000000'
            replace_str = '4E5F496E666F5F3030000000000000000000000000000000000000000000000000003042' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'MessageDialog_00.bflyt':
            # Shift RootPane
            x = float_to_hex(-60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'SystemSaveLoad_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'SystemLoadList_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Guide_01
            x = float_to_hex(-150)
            source_str = '4E5F47756964655F3031000000000000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F47756964655F30310000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'SystemOption_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift A_Guide_00
            x = float_to_hex(-474 - 150)
            source_str = '415F47756964655F303000000000000000000000000000000000000000000000004021440000EDC3'
            replace_str = '415F47756964655F30300000000000000000000000000000000000000000000000402144' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'SystemActionGuide_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if name == 'SystemWindow_00.bflyt':
            # Shift RootPane
            x = float_to_hex(60)
            source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if  name == 'LoadingFade_00.bflyt':
            # Scale N_Base
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426173655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F426173655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Logo
            x = float_to_hex(-70)
            source_str = '4E5F4C6F676F5F303000000000000000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F4C6F676F5F3030000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # # Shift N_Tips
            # x = float_to_hex(-400)
            # source_str = '4E5F546970735F303000000000000000000000000000000000000000000000000000000000000000'
            # replace_str = '4E5F546970735F3030000000000000000000000000000000000000000000000000000000' + x
            # content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Status
            x = float_to_hex(70)
            source_str = '4E5F5374617475735F30300000000000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F5374617475735F303000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
    
        if name == 'PauseMenuOverlay_00.bflyt':
            # Scale P_FooterBase
            x = float_to_hex(1/scaling_factor)
            source_str = '505F466F6F746572426173655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '505F466F6F746572426173655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale S_DecoScissor
            x = float_to_hex(1/scaling_factor)
            source_str = '535F4465636F53636973736F725F303000000000000000000000000000000000000000000000F841000000000000000000000000000000000000803F0000803F'
            replace_str = '535F4465636F53636973736F725F303000000000000000000000000000000000000000000000F841000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift P_FooterBase
            x = float_to_hex(-66)
            source_str = '505F466F6F746572426173655F303000000000000000000000000000000000000000000000000000'
            replace_str = '505F466F6F746572426173655F3030000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift S_DecoScissor
            x = float_to_hex(-29)
            source_str = '535F4465636F53636973736F725F303000000000000000000000000000000000000000000000F841'
            replace_str = '535F4465636F53636973736F725F30300000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift Pa_GuideL
            x = float_to_hex(-25)
            source_str = '50615F47756964654C5F30300000000000000000000000000000000000000000008046C400000C42'
            replace_str = '50615F47756964654C5F30300000000000000000000000000000000000000000008046C4' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift A_Align
            x = float_to_hex(-25)
            source_str = '415F416C69676E5F3030000000000000000000000000000000000000000000000000024300000C42'
            replace_str = '415F416C69676E5F30300000000000000000000000000000000000000000000000000243' + x
            content = content.replace(source_str.lower(), replace_str.lower())
           
            
        if name == 'CameraPointer_00.bflyt':
            # Scale N_InOutScop
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F496E4F757453636F70655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F496E4F757453636F70655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale W_shadow_01
            x = float_to_hex(1/scaling_factor)
            source_str = '575F536861646F775F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '575F536861646F775F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale S_Scissor_00
            x = float_to_hex(1/scaling_factor)
            source_str = '535F53636973736F725F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '535F53636973736F725F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_Type_01
            x = float_to_hex(scaling_factor)
            source_str = '4E5F547970655F303100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F547970655F303100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
    
        if name == 'CameraSystemWindow_00.bflyt':
            # Scale N_InOut_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_FirstOut_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F46697273744F75745F3030000000000000000000000000000000000000000000000000000041000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F46697273744F75745F3030000000000000000000000000000000000000000000000000000041000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'AppMap_00.bflyt':
            # Scale N_BlurInOut_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F426C7572496E4F75745F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_BlurInOut_01
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F426C7572496E4F75745F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_BlurInOut_02
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30320000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F426C7572496E4F75745F30320000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_BlurInOut_03
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F0000803F'
            replace_str = '4E5F426C7572496E4F75745F30330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_AllMapTime
            x = float_to_hex(-60)
            source_str = '4E5F416C6C4D617054696D655F303000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F416C6C4D617054696D655F3031000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        if centered_HUD == False:
            if name == 'EnvironmentInfo_00.bflyt':
                # Shift RootPane
                print(f"Shifting {name}")
                x = float_to_hex(-67)
                source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
                replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                
            if name == 'PlayerStatus_00.bflyt':
                # Shift RootPane
                print(f"Shifting {name}")
                x = float_to_hex(55)
                source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000'
                replace_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                    
            if name == 'PlayerStatus3D_00.bflyt':
                print(f"Shifting {name}")
                # Shift N_ExtraStaminaTarget_01
                x = float_to_hex(400)
                source_str = '45787472615374616D696E615461726765745F303100000000000000000000403AC400009843'
                replace_str = '45787472615374616D696E615461726765745F303100000000000000000000403AC4' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                
        
        with open(file_loc, 'wb') as f:
            f.write(bytes.fromhex(content))
            

    file_names = os.listdir(anim_folder)
    
    for name in file_names:
        file_loc = os.path.join(anim_folder, name)
        
        with open(file_loc, 'rb') as f:
            content = f.read().hex()
        if centered_HUD == False:
            if name == 'AppMap_00_MiniMap.bflan':
                # Shift N_Cut_XX
                print(f"Shifting {name}")
                x = float_to_hex(-440)
                source_str = '0000b4c3'
                replace_str = x
                content = content.replace(source_str.lower(), replace_str.lower())
                
            if name == 'Location_00_IsDiscovery.bflan':
                # Shift N_Lange
                print(f"Shifting {name}")
                x = float_to_hex(285+60)
                source_str = '00808e43'
                replace_str = x
                content = content.replace(source_str.lower(), replace_str.lower())
        
                x = float_to_hex(260+60)
                source_str = '00008243'
                replace_str = x
                content = content.replace(source_str.lower(), replace_str.lower())
            
        with open(file_loc, 'wb') as f:
            f.write(bytes.fromhex(content))
    