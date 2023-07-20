import os
import struct
import sys
import ast
import subprocess


def float_to_hex(f):
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0')

def perform_patching(scaling_factor, centered_HUD, unpacked_folder, expand_shutter):
    blyt_folder = unpacked_folder + "\\blyt"
    anim_folder = unpacked_folder + "\\anim"
    shift_numerator = (1 - float(scaling_factor))
    shift_denominataor = (float(scaling_factor))
    shift_factor = (shift_numerator / shift_denominataor)
    print("Shift value", shift_factor)
    centered_HUD = ast.literal_eval(centered_HUD)
    expand_shutter = ast.literal_eval(expand_shutter)
    print("Centered HUD value is set to ", centered_HUD)
    scaling_factor = float(scaling_factor)
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
    file_names.remove('PaAppPictureBookDetail_00.bflyt')

    for name in file_names:
        file_loc = os.path.join(blyt_folder, name)
        print("Modifying " + name)
        
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
        
        if name == 'ChallengeLog_00.bflyt':
            # Scale N_RContents_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F52436F6E74656E74735F303000000000000000000000000000000000000000000000000028C2000000000000000000000000000000000000803F'
            replace_str = '4E5F52436F6E74656E74735F303000000000000000000000000000000000000000000000000028C200000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale C_CaptureUp_00
            x = float_to_hex(scaling_factor)
            source_str = '435F4361707475726555705F30300000000000000000000000000000000000000000BAC300009A43000000000000000000000000000000000000803F'
            replace_str = '435F4361707475726555705F30300000000000000000000000000000000000000000BAC300009A4300000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale C_CaptureUp_01
            x = float_to_hex(scaling_factor)
            source_str = '435F4361707475726555705F30310000000000000000000000000000000000000000BAC30000BE43000000000000000000000000000000000000803F'
            replace_str = '435F4361707475726555705F30310000000000000000000000000000000000000000BAC30000BE4300000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_SlideList_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F536C6964654C6973745F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F536C6964654C6973745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_ListTitleAll_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F4C6973745469746C65416C6C5F30300000000000000000000000000000000000BAC30000D743000000000000000000000000000000000000803F'
            replace_str = '4E5F4C6973745469746C65416C6C5F30300000000000000000000000000000000000BAC30000D74300000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
                        
            # Scale Pa_ActionWindow_00
            x = float_to_hex(scaling_factor)
            source_str = '50615F416374696F6E57696E646F775F303000000000000000000000000000000000BAC3000048C2000000000000000000000000000000000000803F'
            replace_str = '50615F416374696F6E57696E646F775F303000000000000000000000000000000000BAC3000048C200000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_Tab_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F5461625F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F5461625F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_SlideListAll_00
            x = float_to_hex(80 * scaling_factor)
            source_str = '4E5F536C6964654C697374416C6C5F30300000000000000000000000000000000000A042'
            replace_str = '4E5F536C6964654C697374416C6C5F3030000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_ListTitleAll_00
            x = float_to_hex(-372 * scaling_factor)
            source_str = '4E5F4C6973745469746C65416C6C5F30300000000000000000000000000000000000BAC3'
            replace_str = '4E5F4C6973745469746C65416C6C5F3030000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            with open(file_loc, 'wb') as f:
                f.write(bytes.fromhex(content))  
            continue
 
        # Scale RootPane by scaling_factor
        x = float_to_hex(scaling_factor)
        source_str = '526F6F7450616E650000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
        replace_str = '526F6F7450616E65000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
        content = content.replace(source_str.lower(), replace_str.lower())
        
        # Scale BG_00 by inverse scaling_factor
        x = float_to_hex(1/scaling_factor)
        source_str = '42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
        replace_str = '42475F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
        content = content.replace(source_str.lower(), replace_str.lower()) 
                        
        if  name == 'SystemSaveLoad_00.bflyt':
            # Scale N_Header_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F4865616465725F30300000000000000000000000000000000000000000000000000000C00344000000000000000000000000000000000000803F'
            replace_str = '4E5F4865616465725F30300000000000000000000000000000000000000000000000000000C0034400000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale A_Title_00
            x = float_to_hex(scaling_factor)
            source_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C1000000000000000000000000000000000000803F'
            replace_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C100000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())       
            
            # Scale N_SystemBG_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F53797374656D42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F53797374656D42475F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
                
        if  name == 'SystemLoadList_00.bflyt':
            # Scale N_Header_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F4865616465725F30300000000000000000000000000000000000000000000000000000C00344000000000000000000000000000000000000803F'
            replace_str = '4E5F4865616465725F30300000000000000000000000000000000000000000000000000000C0034400000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale A_Title_00
            x = float_to_hex(scaling_factor)
            source_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C1000000000000000000000000000000000000803F'
            replace_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C100000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_SystemBG_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F53797374656D42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F53797374656D42475F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if  name == 'SystemOption_00.bflyt':
            # Scale N_Header_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F4865616465725F30300000000000000000000000000000000000000000000000000000000744000000000000000000000000000000000000803F'
            replace_str = '4E5F4865616465725F3030000000000000000000000000000000000000000000000000000000074400000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale A_Title_00
            x = float_to_hex(scaling_factor)
            source_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C1000000000000000000000000000000000000803F'
            replace_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C100000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_SystemBG_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F53797374656D42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F53797374656D42475F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if  name == 'SystemActionGuide_00.bflyt':
            # Scale N_Header_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F4865616465725F30300000000000000000000000000000000000000000000000000000C00344000000000000000000000000000000000000803F'
            replace_str = '4E5F4865616465725F30300000000000000000000000000000000000000000000000000000C0034400000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale A_Title_00
            x = float_to_hex(scaling_factor)
            source_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C1000000000000000000000000000000000000803F'
            replace_str = '415F5469746C655F30300000000000000000000000000000000000000000000000000000000040C100000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_SystemBG_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F53797374656D42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F53797374656D42475F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())

        if  name == 'AppAlbum_00.bflyt':
            # Scale N_Open_01
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F4F70656E5F303100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F4F70656E5F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_Open_02
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F4F70656E5F303200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F4F70656E5F30320000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_FadeInOut_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F46616465496E4F75745F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F46616465496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())  
        
        if  name == 'LoadingFade_00.bflyt':
            # Scale Pa_Map_00
            x = float_to_hex(scaling_factor)
            source_str = '50615F4D61705F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '50615F4D61705F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale Pa_LargeDungeonMap_00
            x = float_to_hex(scaling_factor)
            source_str = '50615F4C6172676544756E67656F6E4D61705F303000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '50615F4C6172676544756E67656F6E4D61705F30300000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale Pa_Map_01
            x = float_to_hex(scaling_factor)
            source_str = '50615F4D61705F303100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '50615F4D61705F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale Pa_LargeDungeonMap_01
            x = float_to_hex(scaling_factor)
            source_str = '50615F4C6172676544756E67656F6E4D61705F303100000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '50615F4C6172676544756E67656F6E4D61705F30310000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
                        
            # Scale Pa_IconPlayer_00
            x = float_to_hex(scaling_factor)
            source_str = '50615F49636F6E506C617965725F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '50615F49636F6E506C617965725F303000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale P_SideBGDeco_00
            x = float_to_hex(scaling_factor)
            source_str = '505F5369646542474465636F5F303000000000000000000000000000000000000000704400001A43000000000000000000000000000000000000803F'
            replace_str = '505F5369646542474465636F5F303000000000000000000000000000000000000000704400001A4300000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_Base
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426173655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F426173655F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Logo
            x = float_to_hex(610 * shift_factor)
            source_str = '4E5F4C6F676F5F3030000000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F4C6F676F5F30300000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Tips
            x = float_to_hex(-879 * shift_factor)
            source_str = '4E5F546970735F3030000000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F546970735F30300000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Status
            x = float_to_hex(897 * shift_factor)
            source_str = '4E5F5374617475735F303000000000000000000000000000000000000000000000000000'
            replace_str = '4E5F5374617475735F3030000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
    
        if name == 'PauseMenuOverlay_00.bflyt':
            # Scale P_FooterBase
            x = float_to_hex(1/scaling_factor)
            source_str = '505F466F6F746572426173655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '505F466F6F746572426173655F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale S_DecoScissor
            x = float_to_hex(1/scaling_factor)
            source_str = '535F4465636F53636973736F725F303000000000000000000000000000000000000000000000F841000000000000000000000000000000000000803F'
            replace_str = '535F4465636F53636973736F725F303000000000000000000000000000000000000000000000F84100000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())  
            
        if name == 'CameraPointer_00.bflyt':
            if expand_shutter == True:
                print("Expanding Shutter")
                # Scale N_InOutScope_00
                x = float_to_hex(1/scaling_factor)
                source_str = '4E5F496E4F757453636F70655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
                replace_str = '4E5F496E4F757453636F70655F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale S_Scissor_00
            x = float_to_hex(1/scaling_factor)
            source_str = '535F53636973736F725F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '535F53636973736F725F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_Type_01
            x = float_to_hex(scaling_factor)
            source_str = '4E5F547970655F303100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F547970655F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())

            # Scale W_shadow_01
            x = float_to_hex(1/scaling_factor)
            source_str = '575F536861646F775F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '575F536861646F775F3031000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())

            # Scale Pa_CameraFocus_00
            x = float_to_hex(1/scaling_factor)
            source_str = '50615F43616D657261466F6375735F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '50615F43616D657261466F6375735F3030000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
               
        if name == 'CameraSystemWindow_00.bflyt':
            # Scale N_InOut_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F496E4F75745F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # # Scale N_FirstOut_00
            # x = float_to_hex(scaling_factor)
            # source_str = '4E5F46697273744F75745F3030000000000000000000000000000000000000000000000000000041000000000000000000000000000000000000803F'
            # replace_str = '4E5F46697273744F75745F303000000000000000000000000000000000000000000000000000004100000000000000000000000000000000' + x
            # content = content.replace(source_str.lower(), replace_str.lower())  
            
        if name == 'AppMap_00.bflyt':
            # Scale N_BlurInOut_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F426C7572496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_BlurInOut_01
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F426C7572496E4F75745F3031000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_BlurInOut_02
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30320000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F426C7572496E4F75745F3032000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_BlurInOut_03
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F426C7572496E4F75745F30330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F426C7572496E4F75745F3033000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_MiniMap
            x = float_to_hex(-200 * shift_factor * scaling_factor / 0.744) 
            source_str = '4E5F4D696E694D61705F3030000000000000000000000000000000000000000000000000'
            replace_str = '4E5F4D696E694D61705F30300000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
               
        if name == 'PaMessageBtn_00.bflyt':
            # Shift B_Hit_00
            x = float_to_hex(10000)
            source_str = '425F4869745F303000000000000000000000000000000000000000000000000000403F44'
            replace_str = '425F4869745F3030000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
                  
        if name == 'PaCommonBtnTitle_00.bflyt':
            # Shift B_Hit_00
            x = float_to_hex(10000)
            source_str = '425F4869745F303000000000000000000000000000000000000000000000000000007A44'
            replace_str = '425F4869745F3030000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Shift N_Cursor_00
            x = float_to_hex(10000)
            source_str = '4E5F437572736F725F303000000000000000000000000000000000000000000000007A44'
            replace_str = '4E5F437572736F725F3030000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
              
        if name == 'MessageLog_01.bflyt':
            # Shift P_Capture_00
            x = float_to_hex(1/scaling_factor)
            source_str = '505F436170747572655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '505F436170747572655F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if name == 'SaveLoadIcon_00.bflyt':
            # Shift RootPane
            x = float_to_hex(-728 * (1-scaling_factor))
            source_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000'
            replace_str = '526F6F7450616E65000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
        
        
        if centered_HUD == False:
        
            if name == 'EnvironmentInfo_00.bflyt':
                print(f"Shifting {name}")
                # Shift RootPane
                x = float_to_hex(765 * (1-scaling_factor))
                source_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000'
                replace_str = '526F6F7450616E65000000000000000000000000000000000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                
            if name == 'PlayerStatus_00.bflyt':
                print(f"Shifting {name}")
                # Shift RootPane
                x = float_to_hex(-831 * (1-scaling_factor))
                source_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000'
                replace_str = '526F6F7450616E65000000000000000000000000000000000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                
            if name == 'PlayerStatus3D_00.bflyt':
                print(f"Shifting {name}")
                # Shift N_ExtraStaminaTarget_01
                x = float_to_hex(-745/scaling_factor - (831-745)*shift_factor)
                source_str = '45787472615374616D696E615461726765745F303100000000000000000000403AC4'
                replace_str = '45787472615374616D696E615461726765745F3031000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                
        with open(file_loc, 'wb') as f:
            f.write(bytes.fromhex(content))
    
    file_names = os.listdir(anim_folder)
    
    for name in file_names:
        file_loc = os.path.join(anim_folder, name)
        
        with open(file_loc, 'rb') as f:
            content = f.read().hex()
            
        if name == 'PaMapIconDragonTears_00_Zoom.bflan':
            # Scale P_Geoglyph_00
            print(f"Shifting {name}")
            x = float_to_hex(1.28 / scaling_factor)
            source_str = '464C545302000000100000003400000000030200020000000C00000000000040713D8A3F00000000000040400AD7A33F'
            replace_str = '464C545302000000100000003400000000030200020000000C00000000000040713D8A3F0000000000004040' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            x = float_to_hex(1.08 / scaling_factor)
            source_str = '464C545302000000100000003400000000030200020000000C00000000000040713D8A3F'
            replace_str = '464C545302000000100000003400000000030200020000000C00000000000040' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
        if centered_HUD == False:   
            if name == 'AppMap_00_MiniMap.bflan':
                # Shift N_Cut_XX
                print(f"Shifting {name}")
                x = float_to_hex(765 / scaling_factor)
                source_str = '00403F44'
                replace_str = x
                content = content.replace(source_str.lower(), replace_str.lower())
                
        with open(file_loc, 'wb') as f:
            f.write(bytes.fromhex(content))
