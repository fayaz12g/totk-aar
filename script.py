import os
import struct
import math
import ast

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder, expand_shutter2):
    from functions import float2hex
    
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)
    # expand_shutter2 = ast.literal_eval(expand_shutter2)
    expand_shutter2 = str(expand_shutter2)
    print(f"Expand shutter is set to {expand_shutter2}")
     
    def patch_blyt(filename, pane, operation, value):
        print(f"Performng {operation} by {value} on the {pane} pane in {filename}")
        offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78} 
        full_path = os.path.join(unpacked_folder, 'blyt', f'{filename}.bflyt')
        with open(full_path, 'rb') as f:
            content = f.read().hex()
        start_rootpane = content.index(b'RootPane'.hex())
        pane_hex = str(pane).encode('utf-8').hex()
        start_pane = content.index(pane_hex, start_rootpane)
        idx = start_pane + offset_dict[operation]
        content_new = content[:idx] + float2hex(value) + content[idx+8:]
        with open(full_path, 'wb') as f:
            f.write(bytes.fromhex(content_new))  

    def patch_anim(filename, offset, value):
        full_path = os.path.join(unpacked_folder, 'anim', f'{filename}.bflan')
        with open(full_path, 'rb') as f:
            content = f.read().hex()
        idx = offset
        content_new = content[:idx] + float2hex(value) + content[idx+8:]
        with open(full_path, 'wb') as f:
            f.write(bytes.fromhex(content_new))  
            
    blyt_folder = os.path.join(unpacked_folder, 'blyt')
    file_names = os.listdir(blyt_folder)
    file_names_stripped = [s.strip('.bflyt') for s in file_names]
    do_not_scale_rootpane = ['AppMenuBG_00', 'PauseMenuBG_00',
                             'ShopMenuParasailBG_00', 'ShortCutBG_00',
                             'TitleMenuBG_00', 'EventFade_00',
                             'EventFadeWipe_00', 'CameraShutter_00',
                             'PaAppPictureBookDetail_00', 'AppMenuOverlay_00', 'Pa_Map_00']
    
    if aspect_ratio >= 16/9:
        s1 = (16/9) / aspect_ratio
        print(f"Scaling factor is set to {s1}")
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                print(f"Skipping root pane scaling of {name}")
            if name not in do_not_scale_rootpane:
                print(f"Scaling root pane horizontally for {name}")
                patch_blyt(name, 'RootPane', 'scale_x', s1)
                
        patch_anim('PaMapIconDragonTears_00_Zoom', 576, 1.08/s1)
        patch_anim('PaMapIconDragonTears_00_Zoom', 600, 1.28/s1)
        patch_blyt('AppAlbum_00', 'N_FadeInOut_00', 'scale_x', s1)
        patch_blyt('AppAlbum_00', 'N_Open_01', 'scale_x', 1/s1)
        patch_blyt('AppMap_00', 'N_BlurInOut_00', 'scale_x', 1/s1) 
        patch_blyt('AppMap_00', 'N_BlurInOut_01', 'scale_x', 1/s1) 
        patch_blyt('AppMap_00', 'N_BlurInOut_02', 'scale_x', 1/s1) 
        patch_blyt('AppMap_00', 'N_BlurInOut_03', 'scale_x', 1/s1)
        patch_blyt('AppMap_00', 'S_Sunaarashi_00', 'scale_x', 1/s1) # new
        patch_blyt('AppMap_00', 'N_Capture_00', 'scale_x', 1/s1) # new
        patch_blyt('AppMap_00', 'N_Capture_00', 'scale_y', 1/s1) # new
        patch_blyt('AppMap_00', 'N_MiniMap_00', 'shift_x', -270*s2) 
        patch_blyt('AppMenuOverlay_00', 'N_FadeInOut_00', 'scale_x', s1)
        patch_blyt('AppMenuOverlay_00', 'N_FadeInOut_01', 'scale_x', s1)
        patch_blyt('AppMenuOverlay_00', 'N_Icon_00', 'scale_x', s1)
        patch_blyt('AppMenuOverlay_00', 'N_TitleOne_01', 'scale_x', s1)
        patch_blyt('AppOpenDemoWindow_00', 'P_BG_00', 'scale_x', 1/s1)
        patch_blyt('AutoBuilder_00', 'N_BG_00', 'scale_x', 1/s1)
        if expand_shutter2 == "True":
            patch_blyt('CameraPointer_00', 'N_InOutScope_00', 'scale_x', 500)
            patch_blyt('CameraPointer_00', 'N_InOutScope_00', 'scale_y', 500)
            patch_blyt('CameraPointer_00', 'S_Scissor_00', 'scale_x', 500)
            patch_blyt('CameraPointer_00', 'N_Type_01', 'scale_x', 1/500)  
            patch_blyt('CameraPointer_00', 'Pa_CameraFocus_00', 'scale_x', 1/s1)
            patch_blyt('CameraPointer_00', 'W_Shadow_01', 'scale_x', 1/s1)          
        if expand_shutter2 == "False":
            patch_blyt('CameraPointer_00', 'N_InOutScope_00', 'scale_x', 1/s1)
            patch_blyt('CameraPointer_00', 'N_InOutScope_00', 'scale_y', 1/s1)
            patch_blyt('CameraPointer_00', 'S_Scissor_00', 'scale_x', 1/s1)
            patch_blyt('CameraPointer_00', 'N_Type_01', 'scale_x', s1)  
            patch_blyt('CameraPointer_00', 'Pa_CameraFocus_00', 'scale_x', 1/s1)
            patch_blyt('CameraPointer_00', 'W_Shadow_01', 'scale_x', 1/s1)   
        patch_blyt('CameraSystemWindow_00', 'N_InOut_00', 'scale_x', 1/s1) # new
        patch_blyt('CameraSystemWindow_00', 'T_Text_00', 'scale_x', s1) # new
        patch_blyt('CameraSystemWindow_00', 'Pa_BtnR_00', 'scale_x', s1) # new
        patch_blyt('CameraSystemWindow_00', 'Pa_BtnL_00', 'scale_x', s1) # new
        patch_blyt('CameraSystemWindow_00', 'N_Now_00', 'scale_x', 1/s1) # new
        patch_blyt('CameraSystemWindow_00', 'N_New_00', 'scale_x', 1/s1) # new
        patch_blyt('CameraSystemWindow_00', 'N_AlbumCon_00', 'scale_x', s1)  # new
        #code to make robbie photos fit aspect ratio
        patch_blyt('ChallengeLog_00', 'C_CaptureUp_00', 'shift_x', 10000)
        patch_blyt('ChallengeLog_00', 'C_CaptureUp_01', 'shift_x', 10000)
        patch_blyt('GameOver_00', 'P_BG_00', 'scale_x', 1/s1)
        patch_blyt('LoadingFade_00', 'N_Base', 'scale_x', 1/s1)
        patch_blyt('LoadingFade_00', 'P_BG_00', 'scale_x', 1/s1)
        patch_blyt('LoadingFade_00', 'P_SideBGDeco_00', 'scale_x', s1)
        patch_blyt('LoadingFade_00', 'Pa_IconPlayer_00', 'scale_x', s1)
        patch_blyt('LoadingFade_00', 'Pa_LargeDungeonMap_00', 'scale_x', s1)
        patch_blyt('LoadingFade_00', 'Pa_LargeDungeonMap_01', 'scale_x', s1)
        patch_blyt('LoadingFade_00', 'Pa_Map_00', 'scale_x', s1)
        patch_blyt('LoadingFade_00', 'Pa_Map_01', 'scale_x', s1)
        patch_blyt('MessageLog_01', 'P_Capture_00', 'scale_x', 1/s1) 
        patch_blyt('OwnedHorseList_00', 'N_BG_00', 'scale_x', 1/s1)
        patch_blyt('PaCommonBtnTitle_00', 'B_Hit_00', 'shift_x', 10000)
        patch_blyt('PaCommonBtnTitle_00', 'N_Cursor_00', 'shift_x', 10000) 
        patch_blyt('PaLargeDungeonMap_00', 'P_BG_00', 'scale_x', 1/s1)
        patch_blyt('PaMessageBtn_00', 'B_Hit_00', 'shift_x', 10000) 
        patch_blyt('PaRecipeCardList_00', 'P_BG_00', 'scale_x', 1/s1)
        patch_blyt('PauseMenuOverlay_00', 'P_DecoL_00', 'scale_x', s1)
        patch_blyt('PauseMenuOverlay_00', 'P_DecoL_00', 'shift_x', -(675 + 960*s3)*s1)
        patch_blyt('PauseMenuOverlay_00', 'P_DecoR_00', 'scale_x', s1)
        patch_blyt('PauseMenuOverlay_00', 'P_DecoR_00', 'shift_x', (737 + 960*s3)*s1)
        patch_blyt('PauseMenuOverlay_00', 'P_FooterBase', 'scale_x', 1/s1)
        patch_blyt('PauseMenuOverlay_00', 'S_DecoScissor', 'scale_x', 1/s1)
        patch_blyt('ShopMenu_00', 'N_BG_00', 'scale_x', 1/s1)
        patch_blyt('StaffRoll_00', 'N_BG_00', 'scale_x', 1/s1)
        patch_blyt('SystemActionGuide_00', 'A_Title_00', 'scale_x', s1)
        patch_blyt('SystemActionGuide_00', 'N_Header_00', 'scale_x', 1/s1)
        patch_blyt('SystemActionGuide_00', 'N_SystemBG_00', 'scale_x', 1/s1)
        patch_blyt('SystemActionGuide_00', 'P_DecoL_01', 'scale_x', s1)
        patch_blyt('SystemActionGuide_00', 'P_DecoL_01', 'shift_x', -(675 + 960*s3)*s1)
        patch_blyt('SystemActionGuide_00', 'P_DecoL_02', 'scale_x', s1)
        patch_blyt('SystemActionGuide_00', 'P_DecoL_02', 'shift_x', (675 + 960*s3)*s1)
        patch_blyt('SystemLoadList_00', 'A_Title_00', 'scale_x', s1)
        patch_blyt('SystemLoadList_00', 'N_Slide_00', 'scale_x', 1/s1) # new
        patch_blyt('SystemLoadList_00', 'C_CaptureUp_00', 'scale_x', s1) # new 
        patch_blyt('SystemLoadList_00', 'N_Header_00', 'scale_x', 1/s1)
        patch_blyt('SystemLoadList_00', 'N_SystemBG_00', 'scale_x', 1/s1)
        patch_blyt('SystemLoadList_00', 'P_DecoL_00', 'scale_x', s1)
        patch_blyt('SystemLoadList_00', 'P_DecoL_00', 'shift_x', -(675 + 960*s3)*s1)
        patch_blyt('SystemLoadList_00', 'P_DecoR_00', 'scale_x', s1)
        patch_blyt('SystemLoadList_00', 'P_DecoR_00', 'shift_x', (737 + 960*s3)*s1)
        patch_blyt('SystemOption_00', 'A_Title_00', 'scale_x', s1)
        patch_blyt('SystemOption_00', 'N_Header_00', 'scale_x', 1/s1)
        patch_blyt('SystemOption_00', 'N_SystemBG_00', 'scale_x', 1/s1)
        patch_blyt('SystemOption_00', 'P_DecoL_00', 'scale_x', s1)
        patch_blyt('SystemOption_00', 'P_DecoL_00', 'shift_x', -(675 + 960*s3)*s1)
        patch_blyt('SystemOption_00', 'P_DecoR_00', 'scale_x', s1)
        patch_blyt('SystemOption_00', 'P_DecoR_00', 'shift_x', (737 + 960*s3)*s1)
        patch_blyt('SystemSaveLoad_00', 'A_Title_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'N_Header_00', 'scale_x', 1/s1)
        patch_blyt('SystemSaveLoad_00', 'N_SystemBG_00', 'scale_x', 1/s1)
        patch_blyt('SystemSaveLoad_00', 'P_DecoL_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'P_DecoL_00', 'shift_x', -(675 + 960*s3)*s1)
        patch_blyt('SystemSaveLoad_00', 'P_DecoR_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'P_DecoR_00', 'shift_x', (737 + 960*s3)*s1)
        patch_blyt('SystemSaveLoad_00', 'N_InOut_00', 'scale_x', 1/s1)
        patch_blyt('SystemSaveLoad_00', 'N_Save_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'Pa_CheckButton_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'Pa_CheckButton_01', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'T_CheckText_00', 'scale_x', s1)
        # patch_blyt('SystemSaveLoad_00', 'W_CheckCover_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'A_DayAndClear_00', 'shift_x', 135*s1)
        patch_blyt('SystemSaveLoad_00', 'A_DayAndClear_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'T_Place_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'N_AutoSaveIcon_00', 'scale_x', s1)
        patch_blyt('SystemSaveLoad_00', 'N_PopupBase_00', 'scale_x', (s1*1.35))
        
        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_anim('AppMap_00_MiniMap', 1744, 765 + 960*s3)
            patch_anim('AppMap_00_MiniMap', 1760, 765 + 960*s3)
            patch_anim('AppMap_00_MiniMap', 3256, 765 + 960*s3)
            patch_anim('AppMap_00_MiniMap', 3272, 765 + 960*s3)
            patch_anim('AppMap_00_MiniMap', 6528, 765 + 960*s3)
            patch_anim('AppMap_00_MiniMap', 6544, 765 + 960*s3)
            patch_anim('AppMap_00_MiniMap', 6936, 765 + 960*s3)
            patch_anim('AppMap_00_MiniMap', 6952, 765 + 960*s3)
            patch_blyt('EnvironmentInfo_00', 'RootPane', 'shift_x', 960*s2) 
            patch_blyt('EventSkip_00', 'RootPane', 'shift_x', 960*s2)
            patch_blyt('InstantTipsAppMenu_00', 'RootPane', 'shift_x', 960*s2)
            patch_blyt('InstantTipsWithPict_00', 'RootPane', 'shift_x', 960*s2)
            patch_blyt('InstantTips_00', 'RootPane', 'shift_x', 960*s2)
            patch_blyt('Location_00', 'N_Small_00', 'shift_x', -(388 + 960*s3))
            patch_blyt('NumDisplaySecond_00', 'RootPane', 'shift_x', 960*s2)
            patch_blyt('NumDisplay_00', 'RootPane', 'shift_x', 960*s2)
            patch_blyt('PickUpWin_00', 'RootPane', 'shift_x', 960*s2)
            patch_blyt('PlayerStatus3D_00', 'N_ExtraStaminaTarget_01', 'shift_x', -(745 + 960*s3))
            patch_blyt('PlayerStatus_00', 'N_DevilDemoTargetC_00', 'shift_x', -(284 + 960*s3)) 
            patch_blyt('PlayerStatus_00', 'N_DevilDemoTargetLT_00', 'shift_x', -(576 + 960*s3)) 
            patch_blyt('PlayerStatus_00', 'N_HeartGaugeTargetLT_00', 'shift_x', -(576 + 960*s3))
            patch_blyt('PlayerStatus_00', 'N_HeartPos_00', 'shift_x', -960*s3) 
            patch_blyt('PlayerStatus_00', 'Pa_CompanionLife_00', 'shift_x', -(840 + 960*s3))
            patch_blyt('LoadingFade_00', 'N_Logo', 'shift_x', 960*s3)
            patch_blyt('LoadingFade_00', 'N_Status', 'shift_x', 960*s3)
            patch_blyt('LoadingFade_00', 'N_Tips', 'shift_x', -960*s3)
            patch_blyt('SaveLoadIcon_00', 'RootPane', 'shift_x', -960*s2) 
            
    else:
        s1 = aspect_ratio / (16/9)
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                print(f"Skipping root pane scaling of {name}")
            if name not in do_not_scale_rootpane:
                print(f"Scaling root pane vertically for {name}")
                patch_blyt(name, 'RootPane', 'scale_y', s1)
             
        patch_anim('Location_00_IsDiscovery', 416, 285 + 540*s3)
        patch_anim('Location_00_IsDiscovery', 440, 285 + 540*s3)
        patch_anim('Location_00_IsDiscovery', 464, 260 + 540*s3)
        patch_anim('PaMapIconDragonTears_00_Zoom', 648, 1.08/s1)
        patch_anim('PaMapIconDragonTears_00_Zoom', 672, 1.28/s1)
        patch_blyt('AppAlbum_00', 'N_FadeInOut_00', 'scale_y', s1)
        patch_blyt('AppAlbum_00', 'N_Open_01', 'scale_y', 1/s1)
        patch_blyt('AppMap_00', 'N_BlurInOut_00', 'scale_y', 1/s1)
        patch_blyt('AppMap_00', 'N_BlurInOut_01', 'scale_y', 1/s1)
        patch_blyt('AppMap_00', 'N_BlurInOut_02', 'scale_y', 1/s1)
        patch_blyt('AppMap_00', 'N_BlurInOut_03', 'scale_y', 1/s1)
        patch_blyt('AppMenuOverlay_00', 'A_Align_00', 'shift_y', -(505+540*s3))
        patch_blyt('AppMenuOverlay_00', 'N_FadeInOut_00', 'scale_y', s1)
        patch_blyt('AppMenuOverlay_00', 'N_FadeInOut_01', 'scale_y', s1)
        patch_blyt('AppMenuOverlay_00', 'N_Icon_00', 'scale_y', s1)
        patch_blyt('AppMenuOverlay_00', 'N_TitleOne_01', 'scale_y', s1)
        patch_blyt('AppMenuOverlay_00', 'N_TitleTab_00', 'shift_y', 491+540*s3)
        patch_blyt('AppMenuOverlay_00', 'Pa_GuideLeft_00', 'shift_y', -(505+540*s3))
        patch_blyt('AppOpenDemoWindow_00', 'P_BG_00', 'scale_y', 1/s1)
        patch_blyt('AutoBuilder_00', 'N_BG_00', 'scale_y', 1/s1)
        patch_blyt('CameraPointer_00', 'N_InOutScop', 'scale_y', 1/s1)
        patch_blyt('CameraPointer_00', 'N_Type_01', 'scale_y', s1)
        patch_blyt('CameraPointer_00', 'Pa_CameraFocus_00', 'scale_y', 1/s1)
        patch_blyt('CameraPointer_00', 'S_Scissor_00', 'scale_y', 1/s1)
        patch_blyt('CameraPointer_00', 'W_Shadow_01', 'scale_y', 1/s1)
        patch_blyt('CameraSystemWindow_00', 'N_FirstOut_00', 'scale_y', s1)
        patch_blyt('CameraSystemWindow_00', 'N_InOut_00', 'scale_y', 1/s1)
        patch_blyt('GameOver_00', 'P_BG_00', 'scale_y', 1/s1)
        patch_blyt('LoadingFade_00', 'N_Base_00', 'scale_y', 1/s1)
        patch_blyt('LoadingFade_00', 'P_BG_00', 'scale_y', 1/s1)
        patch_blyt('LoadingFade_00', 'Pa_IconPlayer_00', 'scale_y', s1)
        patch_blyt('LoadingFade_00', 'Pa_LargeDungeonMap_00', 'scale_y', s1)
        patch_blyt('LoadingFade_00', 'Pa_LargeDungeonMap_01', 'scale_y', s1)
        patch_blyt('LoadingFade_00', 'Pa_Map_00', 'scale_y', s1)
        patch_blyt('LoadingFade_00', 'Pa_Map_01', 'scale_y', s1)
        patch_blyt('MessageLog_01', 'P_Capture_00', 'scale_y', 1/s1)
        patch_blyt('OwnedHorseList_00', 'N_BG_00', 'scale_y', 1/s1)
        patch_blyt('PaLargeDungeonMap_00', 'P_BG_00', 'scale_y', 1/s1)
        patch_blyt('PaRecipeCardList_00', 'P_BG_00', 'scale_y', 1/s1)
        patch_blyt('ShopMenu_00', 'N_BG_00', 'scale_y', 1/s1)
        patch_blyt('StaffRoll_00', 'N_BG_00', 'scale_y', 1/s1)
        patch_blyt('SystemActionGuide_00', 'N_SystemBG_00', 'scale_y', 1/s1)
        patch_blyt('SystemActionGuide_00', 'RootPane', 'shift_y', 540*s2)
        patch_blyt('SystemLoadList_00', 'N_SystemBG_00', 'scale_y', 1/s1)
        patch_blyt('SystemOption_00', 'N_SystemBG_00', 'scale_y', 1/s1)
        patch_blyt('SystemSaveLoad_00', 'N_SystemBG_00', 'scale_y', 1/s1)
        patch_blyt('PickUpWin_00', 'RootPane', 'shift_y', 540*s2)

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_anim('AppMap_00_MiniMap', 1816, -(360 + 540*s3))
            patch_anim('AppMap_00_MiniMap', 1832, -(360 + 540*s3))
            patch_anim('AppMap_00_MiniMap', 3328, -(360 + 540*s3))
            patch_anim('AppMap_00_MiniMap', 3344, -(360 + 540*s3))
            patch_anim('AppMap_00_MiniMap', 6600, -(360 + 540*s3))
            patch_anim('AppMap_00_MiniMap', 6616, -(360 + 540*s3))
            patch_anim('AppMap_00_MiniMap', 7008, -(360 + 540*s3))
            patch_anim('AppMap_00_MiniMap', 7024, -(360 + 540*s3))
            patch_blyt('ChallengeLog_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('Challenge_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('CtrlGuide_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('DoCommand_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('EnvironmentInfo_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('SystemSaveLoad_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('TreasureFullShortCut_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('PlayerStatus3D_00', 'N_ExtraStaminaTarget_01', 'shift_y', 304+540*s3)
            patch_blyt('PlayerStatus_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('HorseGauge_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('InstantTipsWithPict_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('LoadingFade_00', 'N_Logo_00', 'shift_y', -540*s3)
            patch_blyt('LoadingFade_00', 'N_Sage_00', 'shift_y', -477 - 2*540*s3)
            patch_blyt('LoadingFade_00', 'N_Status_00', 'shift_y', 540*s3)
            patch_blyt('LoadingFade_00', 'N_Tips_00', 'shift_y', -(360+540*s3))
            patch_blyt('SystemSaveLoad_00', 'N_SystemBG_00', 'shift_y', -540*s3)
            patch_blyt('SystemOption_00', 'N_SystemBG_00', 'shift_y', -540*s3)
            patch_blyt('SystemOption_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('MessageLog_01', 'P_Capture_00', 'shift_y', 540*s3)
            patch_blyt('MessageLog_01', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('MiniGameTimer_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('NumDisplaySecond_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('NumDisplay_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('PauseMenuOverlay_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('Pouch_00', 'N_Info_00', 'shift_y', -540*s3)
            patch_blyt('Pouch_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('SaveLoadIcon_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('ShopMenu_00', 'A_AlignGuide_00', 'shift_y', -(477+540*s3))
            patch_blyt('ShopMenu_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('SystemActionGuide_00', 'N_SystemBG_00', 'shift_y', -540*s3)
            patch_blyt('SystemLoadList_00', 'N_SystemBG_00', 'shift_y',-540*s3)
            patch_blyt('SystemLoadList_00', 'Pa_Guide_00', 'shift_y', -(474+540*s3))
            patch_blyt('SystemLoadList_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('SystemOption_00', 'A_Guide_00', 'shift_y', -(474+540*s3))
            patch_blyt('AppAlbum_00', 'N_PicLoad_01', 'shift_y', -540*s2)
            patch_blyt('InstantTips_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('Location_00', 'N_Large_00', 'shift_y', 270+540*s3)
            patch_blyt('Location_00', 'N_Small_00', 'shift_y', -(395+540*s3))
            patch_blyt('MessageDialog_00', 'RootPane', 'shift_y', -540*s2)
            patch_blyt('AppAlbum_00', 'RootPane', 'shift_y', 540*s2)
            patch_blyt('AppMap_00', 'N_AllMapTime_00', 'shift_y', -540*s3)
            patch_blyt('AppPictureBook_00', 'RootPane', 'shift_y', 540*s2)