import os
import struct
import sys
import ast
import subprocess


def float_to_hex(f):
    """
    Converts float values into hex, strips the 0x prefix and prepends zeroes to
    always have length 8
    """
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0')

def perform_patching(scaling_factor, centered_HUD, unpacked_folder):
    blyt_folder = unpacked_folder + "\\blyt"
    anim_folder = unpacked_folder + "\\anim"
    shift_numerator = (1 - float(scaling_factor))
    shift_denominataor = (float(scaling_factor))
    shift_factor = (shift_numerator / shift_denominataor)
    print("Shift value", shift_factor)
    centered_HUD = ast.literal_eval(centered_HUD)
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

    for name in file_names:
        file_loc = blyt_folder + '\\' + name
        
        with open(file_loc, 'rb') as f:
            content = f.read().hex()
            
            
        if name == 'AppMenuOverlay_00.bflyt':
            # Scale N_FadeInOut_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F46616465496E4F75745F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F46616465496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_FadeInOut_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F46616465496E4F75745F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F46616465496E4F75745F3031000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
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
        
        # Scale BG_00 by inverse scaling_factor
        x = float_to_hex(1/scaling_factor)
        source_str = '42475F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
        replace_str = '42475F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
        content = content.replace(source_str.lower(), replace_str.lower())
        
        
        if  name == 'LoadingFade_00.bflyt':
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
            # Scale N_InOutScope_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F496E4F757453636F70655F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F496E4F757453636F70655F30300000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale W_shadow_01
            x = float_to_hex(1/scaling_factor)
            source_str = '575F536861646F775F30310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '575F536861646F775F3031000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
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
            
            
        if name == 'CameraSystemWindow_00.bflyt':
            # Scale N_InOut_00
            x = float_to_hex(1/scaling_factor)
            source_str = '4E5F496E4F75745F3030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000803F'
            replace_str = '4E5F496E4F75745F303000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
            
            # Scale N_FirstOut_00
            x = float_to_hex(scaling_factor)
            source_str = '4E5F46697273744F75745F3030000000000000000000000000000000000000000000000000000041000000000000000000000000000000000000803F'
            replace_str = '4E5F46697273744F75745F303000000000000000000000000000000000000000000000000000004100000000000000000000000000000000' + x
            content = content.replace(source_str.lower(), replace_str.lower())
                
            
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
        
    
        if centered_HUD == False:
            if name == 'EnvironmentInfo_00.bflyt':
                print("Shifting environment info to corner HUD")
                # Shift RootPane
                x = float_to_hex(603 * shift_factor * scaling_factor / 0.744)
                source_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000'
                replace_str = '526F6F7450616E65000000000000000000000000000000000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                
                
            if name == 'PlayerStatus_00.bflyt':
                print("Shifting PlayerStatus to corner HUD")
                # Shift RootPane
                x = float_to_hex(-645 * shift_factor * scaling_factor / 0.744)
                source_str = '526F6F7450616E6500000000000000000000000000000000000000000000000000000000'
                replace_str = '526F6F7450616E65000000000000000000000000000000000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                    
                
            if name == 'PlayerStatus3D_00.bflyt':
                print("Shifting Extra Stamina to corner HUD")
                # Shift N_ExtraStaminaTarget_01
                x = float_to_hex(-760 * (1 + shift_factor) * scaling_factor**(-1/11))
                source_str = '45787472615374616D696E615461726765745F303100000000000000000000403AC4'
                replace_str = '45787472615374616D696E615461726765745F3031000000000000000000' + x
                content = content.replace(source_str.lower(), replace_str.lower())
                    
                
        with open(file_loc, 'wb') as f:
            f.write(bytes.fromhex(content))


    file_names = os.listdir(anim_folder)

    for name in file_names:
        file_loc = anim_folder + '\\' + name
        
        with open(file_loc, 'rb') as f:
            content = f.read().hex()
            
        if centered_HUD == False:
            if name == 'AppMap_00_MiniMap.bflan':
                print("Shifting mini map to corner HUD")
                # Shift N_Cut_XX
                x = float_to_hex(780 * (1 + shift_factor) * (0.744 / scaling_factor)**(1/22))
                source_str = '00403F44'
                replace_str = x
                content = content.replace(source_str.lower(), replace_str.lower())
            
        with open(file_loc, 'wb') as f:
            print(f"Writing patched file {f}")
            f.write(bytes.fromhex(content))
        


