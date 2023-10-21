import obspython as S
import os
import json
import platform as plt
import RioHudLib

#def script_defaults(settings):

def script_description():
    return 'Mario Baseball Inning End Source Enabler Version 0.2.0'

class SourceDisplay:
    def __init__(self):

        self.inning_float = 0.0

        self.current_event_num = -1

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        self.new_event = 0

        self.home_player = ''
        self.away_player = ''

        if str(plt.platform()).lower()[0] == 'm':
            self.platform = 'MacOS'
            current_path = str(os.path.realpath(__file__))
            '''self.HUD_path = '/' + current_path.split('/', 3)[1] + '/' + current_path.split('/', 3)[
                2] + '/' + 'Library/Application Support/ProjectRio/HudFiles/decoded.hud.json' '''
        elif str(plt.platform()).lower()[0] == 'w':
            self.platform = 'Windows'
            current_path = str(os.path.realpath(__file__))
            '''self.HUD_path = current_path.split('\\')[0] + '/' + current_path.split('\\')[1] + '/' + current_path.split('\\')[
                2] + '/Documents/Project Rio/HudFiles/decoded.hud.json' '''
        else:
            self.platform = 'Unknown'

    def set_visible(self):
        for i in range(0, len(self.roster_image_list)):
            S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.home_group), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.away_group), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.home_player_text_source), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.away_player_text_source), True)

    def dir_scan(self):
        hud_file_path = S.obs_data_get_string(globalsettings, '_path')
        hud_file_path = hud_file_path.replace("\\", "/")

        if not os.path.isfile(hud_file_path):
            return ''

        with open(hud_file_path) as f:
            hud_data = json.load(f)

        hud_data = RioHudLib.hudObj(hud_data)

        # Return if the event hasn't changed
        if (self.current_event_num == hud_data.event_number):
            if (self.new_event != 1):
                return self.current_event_num

        if hud_data.event_number == '0a':
            return self.current_event_num

        self.current_event_num = hud_data.event_number

        self.inning_float = hud_data.inning_float()

        if (hud_data.inning_end() == True) & (self.inning_float < 10):
            previous_source_str = S.obs_data_get_string(globalsettings, f'_{self.inning_float-0.5}_source_selector')
            if previous_source_str != 'None':
                S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, previous_source_str), False)
            source_str = S.obs_data_get_string(globalsettings, f'_{self.inning_float}_source_selector')
            if source_str == 'None':
                return
            print(f'{source_str} Activated')
            S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, source_str), True)
            

def script_load(settings):

    S.timer_add(check_for_updates, 1000)

    global globalsettings
    globalsettings = settings

    global inning_source_display
    inning_source_display = SourceDisplay()

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, '_path')


def check_for_updates():
   if pause_bool == False:
        inning_source_display.dir_scan()

def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    inning_source_display.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, '_pause')

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_bool(props, '_pause', 'Pause')

    OS_list = S.obs_properties_add_list(props, '_OS_list', 'HUD File Path:', S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, 'Custom', 'custom')
    S.obs_property_list_add_string(OS_list, 'Windows Default Path', 'windows')
    S.obs_property_list_add_string(OS_list, 'MacOS Default Path', 'macOS')
    file_path_input = S.obs_properties_add_text(props, '_path', 'HUD File Path:', S.OBS_TEXT_DEFAULT)

    current_scene = S.obs_frontend_get_current_scene()
    scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global halfinning_source_dict

    halfinning_source_dict = {1.5: None,
                              2.0: None,
                              2.5: None,
                              3.0: None,
                              3.5: None,
                              4.0: None,
                              4.5: None,
                              5.0: None,
                              5.5: None,
                              6.0: None,
                              6.5: None,
                              7.0: None,
                              7.5: None,
                              8.0: None,
                              8.5: None,
                              9.0: None,
                              9.5: None}
    
    source_str_list = ['None']
    if scene is not None:
        source_list = S.obs_scene_enum_items(scene)

        # Loop through the scene items and get the source names
        for scene_item in source_list:
            source = S.obs_sceneitem_get_source(scene_item)
            source_name = S.obs_source_get_name(source)
            source_str_list.append(source_name)

        # Release the scene items
        S.sceneitem_list_release(source_list)

    for key in halfinning_source_dict.keys():
        halfinning_source_dict[key] = S.obs_properties_add_list(props, f'_{key}_source_selector', f'Select Inning {key} Source:', S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
        for source in source_str_list:
            S.obs_property_list_add_string(halfinning_source_dict[key], source, source)

    S.obs_property_set_modified_callback(OS_list, OS_callback)

    return props

def OS_callback(props, prop, settings):
    if S.obs_data_get_string(settings, '_OS_list') == 'windows':
        current_path = str(os.path.realpath(__file__))
        HUD_Path = current_path.split('\\')[0] + '/' + current_path.split('\\')[1] + '/' + current_path.split('\\')[2] + '/Documents/Project Rio/HudFiles/decoded.hud.json'
        S.obs_data_set_string(settings, '_path', HUD_Path)
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), False)
    elif S.obs_data_get_string(settings, '_OS_list') == 'macOS':
        current_path = str(os.path.realpath(__file__))
        HUD_Path = '/'+current_path.split('/', 3)[1] + '/' + current_path.split('/', 3)[2] + '/' + 'Library/Application Support/ProjectRio/HudFiles/decoded.hud.json'
        S.obs_data_set_string(settings, '_path', HUD_Path)
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), False)
    else:
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), True)

    return True