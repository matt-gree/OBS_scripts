import obspython as S
import os
import json
import platform as plt

#def script_defaults(settings):

class rosterimages:
    def __init__(self):

        self.location = S.vec2()

        self.inning
        self.halfinning = 0

        self.away_team_captain = str()
        self.home_team_captain = str()

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

    #Used when reverting from the captains only layout
    def enable_roster_images(self):
        for i in range(0, len(self.roster_image_list)):
            source = S.obs_get_source_by_name(self.roster_image_list[i][0])
            S.obs_source_set_enabled(source, True)
            S.obs_source_release(source)

    #Used for auto-enableing the rosters after event 0a
    def set_visible(self):
        for i in range(0, len(self.roster_image_list)):
            S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.home_group), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.away_group), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.home_player_text_source), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, self.away_player_text_source), True)

    def add_image_source(self, image_name, OBS_name, scene):
        #will only add images in the images_directory
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, 'file', str(images_directory) + image_name + '.png')
        source = S.obs_source_create('image_source', OBS_name, settings, None)
        S.obs_scene_add(scene, source)
        S.obs_data_release(settings)
        S.obs_source_release(source)

    def add_captains(self):
        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        home_group = S.obs_scene_add_group(self.scene, self.home_group)
        away_group = S.obs_scene_add_group(self.scene, self.away_group)
        #Home and Away Player Names
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Home_Captain_Text = S.obs_source_create('text_ft2_source', self.home_player_text_source, settings, None)
        else:
            Home_Captain_Text = S.obs_source_create('text_gdiplus', self.home_player_text_source, settings, None)
        S.obs_scene_add(self.scene, Home_Captain_Text)
        S.obs_data_release(settings)
        S.obs_source_release(Home_Captain_Text)

        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Away_Captain_Text = S.obs_source_create('text_ft2_source', self.away_player_text_source, settings, None)
        else:
            Away_Captain_Text = S.obs_source_create('text_gdiplus', self.away_player_text_source, settings, None)
        S.obs_scene_add(self.scene, Away_Captain_Text)
        S.obs_data_release(settings)
        S.obs_source_release(Away_Captain_Text)

        text_postions = S.vec2()
        text_postions.x = 500
        text_postions.y = 500
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.home_player_text_source), text_postions)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.away_player_text_source), text_postions)

        #Batting and Fielding Icons
        self.add_image_source('bat', 'away_indicator', self.scene)
        S.obs_sceneitem_group_add_item(away_group, S.obs_scene_find_source(self.scene, 'away_indicator'))

        self.add_image_source('glove', 'home_indicator', self.scene)
        S.obs_sceneitem_group_add_item(home_group, S.obs_scene_find_source(self.scene, 'home_indicator'))

        #Team Roster
        for i in range(0,len(self.roster_image_list)):
            self.add_image_source(str(self.away_team_captain), self.roster_image_list[i][0], self.scene)
            if i < 9:
                S.obs_sceneitem_group_add_item(away_group,
                                               S.obs_scene_find_source(self.scene, self.roster_image_list[i][0]))
            else:
                S.obs_sceneitem_group_add_item(home_group,
                                               S.obs_scene_find_source(self.scene, self.roster_image_list[i][0]))

    def dir_scan(self):
        hud_file_path = S.obs_data_get_string(globalsettings, '_path')
        hud_file_path = hud_file_path.replace("\\", "/")

        if not os.path.isfile(hud_file_path):
            return ''

        with open(hud_file_path) as f:
            hud_data = json.load(f)

        # Return if the event hasn't changed
        if (self.current_event_num == hud_data['Event Num']):
            if (self.new_event != 1):
                return self.current_event_num

        if hud_data['Event Num'] == '0a':
            return self.current_event_num

        global visible_bool

        if visible_bool is True and ((hud_data['Event Num'] == '0b')
                                     or (self.current_event_num == '0b')
                                     or (int(str(hud_data['Event Num'])[:-1]) < int(str(self.current_event_num[:-1])))):
            self.set_visible()
            print("visible")

        self.current_event_num = hud_data['Event Num']

        print(hud_data['Event Num'])

        self.inning = hud_data['Inning']
        self.halfinning = hud_data['Half Inning']

        self.new_event = 1

        self.home_player = hud_data['Home Player']
        self.away_player = hud_data['Away Player']

def script_load(settings):

    S.timer_add(check_for_updates, 1000)

    global globalsettings
    globalsettings = settings

    global inning_source_display
    inning_source_display = rosterimages()

    global visible_bool
    visible_bool = S.obs_data_get_bool(settings, '_visible')

    inning_source_display.new_event = 1
    inning_source_display.dir_scan()

    print(inning_source_display.scene)

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, '_path')


def check_for_updates():
   if pause_bool == False:
       inning_source_display.dir_scan()
       inning_source_display.update_images()

def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    inning_source_display.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, '_pause')

    indicator_bool = S.obs_data_get_bool(settings, '_indicator')

    global visible_bool
    visible_bool = S.obs_data_get_bool(settings, '_visible')
    away_indicator_source = S.obs_get_source_by_name(inning_source_display.indicator_image_list[0][0])
    home_indicator_source = S.obs_get_source_by_name(inning_source_display.indicator_image_list[1][0])

    if indicator_bool == True:
        S.obs_source_set_enabled(away_indicator_source, False)
        S.obs_source_set_enabled(home_indicator_source, False)
    else:
        S.obs_source_set_enabled(away_indicator_source, True)
        S.obs_source_set_enabled(home_indicator_source, True)

    S.obs_source_release(away_indicator_source)
    S.obs_source_release(home_indicator_source)


def script_description():
    return 'Mario Baseball Team HUD Version 1.2 \nOBS interface by MattGree \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nDonations are welcomed!'

def add_pressed(props, prop):
    inning_source_display.add_captains()
    inning_source_display.new_event = 1
    inning_source_display.dir_scan()
    inning_source_display.update_images()
    print(inning_source_display.roster_image_list)

    settings = S.obs_data_create()
    layout_callback(props, prop, settings)
    S.obs_data_release(settings)

def refresh_pressed(props, prop):
    inning_source_display.new_event = 1
    inning_source_display.dir_scan()
    inning_source_display.update_images()

#def remove_pressed(props, prop):



def script_properties():
    props = S.obs_properties_create()
    #S.obs_properties_add_button(props, 'refreshbutton', 'Refresh HUD', refresh_pressed)
    S.obs_properties_add_bool(props, '_pause', 'Pause')
    S.obs_properties_add_button(props, '_add_button', 'Add', add_pressed)
    S.obs_properties_add_button(props, '_removebutton', 'Remove', remove_pressed)

    OS_list = S.obs_properties_add_list(props, '_OS_list', 'HUD File Path:', S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, 'Custom', 'custom')
    S.obs_property_list_add_string(OS_list, 'Windows Default Path', 'windows')
    S.obs_property_list_add_string(OS_list, 'MacOS Default Path', 'macOS')
    file_path_input = S.obs_properties_add_text(props, '_path', 'HUD File Path:', S.OBS_TEXT_DEFAULT)

    font_property = S.obs_properties_add_font(props, '_player_font', 'Player Font:')

    S.obs_properties_add_bool(props, '_indicator', 'Remove Indicators')

    S.obs_properties_add_bool(props, '_visible', 'Automatically make visible:')

    S.obs_property_set_modified_callback(OS_list, OS_callback)
    S.obs_property_set_modified_callback(font_property, font_callback)

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

def font_callback(props, prop, settings):
    S.obs_data_set_obj(settings, 'font', S.obs_data_get_obj(settings, '_player_font'))
    source = S.obs_get_source_by_name(inning_source_display.away_player_text_source)
    S.obs_data_set_bool(settings, 'outline', True)
    S.obs_source_update(source, settings)
    S.obs_source_release(source)

    source = S.obs_get_source_by_name(inning_source_display.home_player_text_source)
    S.obs_source_update(source, settings)
    S.obs_source_release(source)

    return True