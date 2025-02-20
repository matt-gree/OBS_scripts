import obspython as S
import os
import json
import platform as plt
from pyRio.team_name_algo import team_name
from pyRio.stat_file_parser import HudObj

def script_description():
    return 'Mario Baseball Team HUD Version 2.1.1 \nOBS interface by MattGree, \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nSupport me on YouTube.com/MattGree'


images_directory = str(os.path.dirname(__file__)) + '/Images/'

class rosterimages:
    def __init__(self):

        self.location = S.vec2()

        self.away_team_roster = []
        self.home_team_roster = []

        self.halfinning = 0

        self.away_captain_index = -1
        self.home_captain_index = -1

        self.current_event_num = '-1a'

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        self.roster_image_list = [
            ['AwayRoster0', 0, '', S.vec2()],
            ['AwayRoster1', 0, '', S.vec2()],
            ['AwayRoster2', 0, '', S.vec2()],
            ['AwayRoster3', 0, '', S.vec2()],
            ['AwayRoster4', 0, '', S.vec2()],
            ['AwayRoster5', 0, '', S.vec2()],
            ['AwayRoster6', 0, '', S.vec2()],
            ['AwayRoster7', 0, '', S.vec2()],
            ['AwayRoster8', 0, '', S.vec2()],
            ['HomeRoster0', 0, '', S.vec2()],
            ['HomeRoster1', 0, '', S.vec2()],
            ['HomeRoster2', 0, '', S.vec2()],
            ['HomeRoster3', 0, '', S.vec2()],
            ['HomeRoster4', 0, '', S.vec2()],
            ['HomeRoster5', 0, '', S.vec2()],
            ['HomeRoster6', 0, '', S.vec2()],
            ['HomeRoster7', 0, '', S.vec2()],
            ['HomeRoster8', 0, '', S.vec2()],
        ]

        self.home_group = 'Home Roster'
        self.away_group = 'Away Roster'
        self.home_player_text_source = 'Home Player'
        self.away_player_text_source = 'Away Player'

        self.away_roster = ''
        self.home_roster = ''

        self.away_team_name = ''
        self.home_team_name = ''

        self.home_player = ''
        self.away_player = ''

        self.addons_image_dict = {
            'Away Indicator': {'Image': 'bat', 'Location': S.vec2(), 'Relative Position': 0,
                               'Small Scale': 0, 'Large Scale': 0, 'Scale Vector': S.vec2(), 'Group': self.away_group},
            'Home Indicator': {'Image': 'glove', 'Location': S.vec2(), 'Relative Position': 0,
                               'Small Scale': 0, 'Large Scale': 0, 'Scale Vector': S.vec2(), 'Group': self.home_group},
            'Away Logo': {'Image': '', 'Location': S.vec2(), 'Scale Vector': S.vec2(), 'Relative Position': 1,
                               'Small Scale': 0, 'Large Scale': 0, 'Group': self.away_group},
            'Home Logo': {'Image': '', 'Location': S.vec2(), 'Relative Position': 1,
                               'Small Scale': 0, 'Large Scale': 0, 'Scale Vector': S.vec2(), 'Group': self.home_group}
        }

        self.new_event = 0

        self.inning_end = False

        self.home_roster_loc = S.vec2()
        self.away_roster_loc = S.vec2()

        self.home_player_loc = S.vec2()
        self.away_player_loc = S.vec2()

        self.image_width = 60
        self.captain_size_multiplier = 1.6

        if str(plt.platform()).lower()[0] == 'm':
            self.platform = 'MacOS'
            current_path = str(os.path.realpath(__file__))
            '''self.HUD_path = '/' + current_path.split('/', 3)[1] + '/' + current_path.split('/', 3)[
                2] + '/' + 'Library/Application Support/Project Rio/HudFiles/decoded.hud.json' '''
        elif str(plt.platform()).lower()[0] == 'w':
            self.platform = 'Windows'
            current_path = str(os.path.realpath(__file__))
            '''self.HUD_path = current_path.split('\\')[0] + '/' + current_path.split('\\')[1] + '/' + current_path.split('\\')[
                2] + '/Documents/Project Rio/HudFiles/decoded.hud.json' '''
        else:
            self.platform = 'Unknown'

        self.indicator_images_exist = True

    #Used when reverting from the captains only layout
    def enable_roster_images(self):
        for i in range(0, len(self.roster_image_list)):
            source = S.obs_get_source_by_name(self.roster_image_list[i][0])
            if source:
                S.obs_source_set_enabled(source, True)
                S.obs_source_release(source)
            else:
                S.script_log(S.LOG_WARNING, "Source not found: SourceName")

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

    def add_rosters(self):
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

        text_positions = S.vec2()
        text_positions.x = 500
        text_positions.y = 500
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.home_player_text_source), text_positions)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.away_player_text_source), text_positions)

        #Indicators and Logos
        for key, item in self.addons_image_dict.items():
            self.add_image_source(item['Image'], key, self.scene)
            group = S.obs_scene_get_group(self.scene, item['Group'])
            S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(self.scene, key))

        #Team Roster
        for i in range(0,len(self.roster_image_list)):
            self.add_image_source('', self.roster_image_list[i][0], self.scene)
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
            return False

        with open(hud_file_path) as f:
            hud_data = json.load(f)

        hud_data = HudObj(hud_data)
        self.inning_end = hud_data.inning_end()

        # Return if the event hasn't changed
        if (self.current_event_num == hud_data.event_number):
            if (self.new_event != 1):
                return False

        if hud_data.event_number == '0a':
            return False

        global visible_bool

        if visible_bool is True and ((hud_data.event_number == '0b')
                                     or (self.current_event_num == '0b')
                                     or (hud_data.event_integer() < int(str(self.current_event_num)[:-1]))):
            
            if (self.away_player == hud_data.player(1)) and (self.home_player == hud_data.player(0)):
                flip_teams('', '')

            self.set_visible()
            print("visible")

        self.current_event_num = hud_data.event_number
        print(hud_data.event_number)
        self.halfinning = hud_data.half_inning()
        self.new_event = 1

        self.away_player = hud_data.player(0)
        self.home_player = hud_data.player(1)

        away_roster = hud_data.roster(0)
        home_roster = hud_data.roster(1)

        for player in away_roster:
            self.roster_image_list[player][1] = away_roster[player]['captain']
            self.roster_image_list[player][2] = away_roster[player]['char_id']

        for player in home_roster:
            self.roster_image_list[player+9][1] = home_roster[player]['captain']
            self.roster_image_list[player+9][2] = home_roster[player]['char_id']

        self.away_captain_index = hud_data.captain_index(0)
        self.home_captain_index = hud_data.captain_index(1) + 9
        
        self.roster_image_list[self.away_captain_index][1] = 0
        self.roster_image_list[self.home_captain_index-9][1] = 1
        self.roster_image_list[self.home_captain_index][1] = 0
        self.roster_image_list[self.away_captain_index+9][1] = 1

        self.away_roster = [element[2] for element in self.roster_image_list[:9]]
        self.home_roster = [element[2] for element in self.roster_image_list[9:]]

        self.addons_image_dict['Away Logo']['Image'] = team_name(self.away_roster, self.roster_image_list[self.home_captain_index-9][2])
        self.addons_image_dict['Home Logo']['Image'] = team_name(self.home_roster, self.roster_image_list[self.away_captain_index+9][2])

        return True

    def update_images(self):
        if (self.new_event == 0):
            return self.current_event_num

        for image in self.roster_image_list:
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + str(image[2]) + '.png')
            source = S.obs_get_source_by_name(image[0])
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

        for key, item in self.addons_image_dict.items():
            if key not in ['Away Logo', 'Home Logo']:
                continue
            source = S.obs_get_source_by_name(key)
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + item['Image'] + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

        source = S.obs_get_source_by_name(self.home_player_text_source)
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, 'text', str(self.home_player))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        source = S.obs_get_source_by_name(self.away_player_text_source)
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, 'text', str(self.away_player))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        self.new_event = 0

        if S.obs_data_get_string(globalsettings, '_roster_layout') == 'horizontal':
            self.set_position_straight('Horizontal')
        if S.obs_data_get_string(globalsettings, '_roster_layout') == 'vertical':
            self.set_position_straight('Vertical')
        if S.obs_data_get_string(globalsettings, '_roster_layout') == '2x4':
            self.set_position_2x4('Horizontal')
        if S.obs_data_get_string(globalsettings, '_roster_layout') == '2x4vertical':
            self.set_position_2x4('Vertical')
        if S.obs_data_get_string(globalsettings, '_roster_layout') == 'captainshorizontal':
            self.set_position_captains('Horizontal')
        if S.obs_data_get_string(globalsettings, '_roster_layout') == 'captainsvertical':
            self.set_position_captains('Vertical')
        
        def update_indicators(source_name, image):
            source = S.obs_get_source_by_name(source_name)
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + image + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

        if self.halfinning == 0:
            update_indicators('Home Indicator', 'glove')
            update_indicators('Away Indicator', 'bat')
        else:
            update_indicators('Home Indicator', 'bat')
            update_indicators('Away Indicator', 'glove')

        if self.inning_end:
            print(self.inning_end)
            if self.halfinning == 0:
                update_indicators('Home Indicator', 'bat')
                update_indicators('Away Indicator', 'glove')
            else:
                update_indicators('Home Indicator', 'glove')
                update_indicators('Away Indicator', 'bat')

    def indicator_scale(self, size):
        for key, item in self.addons_image_dict.items():
            item['Scale Vector'].x = item[f'{size} Scale']
            item['Scale Vector'].y = item[f'{size} Scale']
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, key), item['Scale Vector'])

    def pre_position_update(self):
        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        home_roster_8 = S.obs_get_source_by_name('HomeRoster8')

        if home_roster_8:
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.home_player_text_source), self.home_player_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.away_player_text_source), self.away_player_loc)
            for item in self.roster_image_list:
                S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, item[0]), item[3])
        else:
            self.home_roster_loc = S.vec2()
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
            self.away_roster_loc = S.vec2()
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)

        S.obs_source_release(home_roster_8)

        for key, item in self.addons_image_dict.items():
            source = S.obs_get_source_by_name(key)
            if S.obs_source_get_width(source) == 0:
                item['Small Scale'] = 0
                item['Large Scale'] = 0
            else:
                item['Small Scale'] = (self.image_width)/S.obs_source_get_width(source)
                item['Large Scale'] = item['Small Scale'] * self.captain_size_multiplier
            S.obs_source_release(source)

    def set_position_straight(self, direction):
        self.enable_roster_images()
        self.pre_position_update()

        for i in range(0, len(self.roster_image_list)):
            scale = S.vec2()
            scale.x = 1
            scale.y = 1
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), scale)
            S.vec2_zero(self.roster_image_list[i][3])
            if direction == 'Horizontal':
                self.roster_image_list[i][3].x = i * self.image_width
                if i > 8:
                    self.roster_image_list[i][3].x = (i-9) * self.image_width
            elif direction == 'Vertical':
                self.roster_image_list[i][3].y = i * self.image_width
                if i > 8:
                    self.roster_image_list[i][3].y = (i-9) * self.image_width
            
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), self.roster_image_list[i][3])
        
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)

        # Set indicator location and scale
        for key, item in self.addons_image_dict.items():
            S.vec2_zero(item['Location'])
            if direction == 'Horizontal':
                item['Location'].x = (9+item['Relative Position']) * self.image_width
            if direction == 'Vertical':
                item['Location'].y = (9+item['Relative Position']) * self.image_width

            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, key), item['Location'])

        self.indicator_scale('Small')

    def set_position_2x4(self, direction):
        self.enable_roster_images()
        self.pre_position_update()
        counter = 0

        for i in range(0,len(self.roster_image_list)):
            S.vec2_zero(self.roster_image_list[i][3])
            if self.roster_image_list[i][1] == 1:
                scale = S.vec2()
                scale.x = self.captain_size_multiplier
                scale.y = self.captain_size_multiplier
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), scale)
                if direction == 'Horizontal':
                    if i < 8:
                        self.roster_image_list[i][3].y = 0.2 * self.image_width
                    else:
                        self.roster_image_list[i][3].y = 0.2 * self.image_width

                elif direction == 'Vertical':
                    if i < 8:
                        self.roster_image_list[i][3].x = 0.2 * self.image_width
                    else:
                        self.roster_image_list[i][3].x = 0.2 * self.image_width
            else:
                scale = S.vec2()
                scale.x = 1
                scale.y = 1
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), scale)
                if direction == 'Horizontal':
                    if counter%8 < 4:
                        self.roster_image_list[i][3].x = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                    else:
                        self.roster_image_list[i][3].x = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                        self.roster_image_list[i][3].y = self.image_width
                elif direction == 'Vertical':
                    if counter%8 < 4:
                        self.roster_image_list[i][3].y = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                    else:
                        self.roster_image_list[i][3].y = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                        self.roster_image_list[i][3].x = self.image_width
                counter += 1

            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                    self.roster_image_list[i][3])

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)

        # Set indicator location and scale
        for key, item in self.addons_image_dict.items():
            S.vec2_zero(item['Location'])
            source = S.obs_get_source_by_name(key)
            if direction == 'Horizontal':
                item['Location'].x = 4 * self.image_width + (self.captain_size_multiplier * self.image_width)*(1+item['Relative Position'])
                item['Location'].y = (2 * self.image_width - (S.obs_source_get_width(source)) * item['Large Scale'])/2
            elif direction == 'Vertical':
                item['Location'].y = 4 * self.image_width + (self.captain_size_multiplier * self.image_width)*(1+item['Relative Position'])
                item['Location'].x = (2 * self.image_width - (S.obs_source_get_width(source)) * item['Large Scale'])/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, key), item['Location'])
            S.obs_source_release(source)
        self.indicator_scale('Large')

    def set_position_captains(self, direction):
        self.pre_position_update()
        self.set_position_2x4(direction)
        for i in range(0, len(self.roster_image_list)):
            S.vec2_zero(self.roster_image_list[i][3])
            if self.roster_image_list[i][1] == 1:
                scale = S.vec2()
                scale.x = self.captain_size_multiplier
                scale.y = self.captain_size_multiplier
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                          scale)
                if direction == 'Horizontal':
                    if i < 8:
                        self.roster_image_list[i][3].y = 0.2 * self.image_width
                    else:
                        self.roster_image_list[i][3].y = 0.2 * self.image_width
                elif direction == 'Vertical':
                    if i < 8:
                        self.roster_image_list[i][3].y = 0.2 * self.image_width
                    else:
                        self.roster_image_list[i][3].y = 0.2 * self.image_width
            else:
                source = S.obs_get_source_by_name(self.roster_image_list[i][0])
                S.obs_source_set_enabled(source, False)
                S.obs_source_release(source)

        # Set indicator location and scale
        for key, item in self.addons_image_dict.items():
            S.vec2_zero(item['Location'])
            source = S.obs_get_source_by_name(key)
            if direction == 'Horizontal':
                item['Location'].x = (self.captain_size_multiplier * self.image_width)*(1 + item['Relative Position'])
                item['Location'].y = (2 * self.image_width - (S.obs_source_get_width(source) * item['Large Scale']))/2
            elif direction == 'Vertical':
                item['Location'].y = (self.captain_size_multiplier * self.image_width)*(1 + item['Relative Position'])
                item['Location'].x = (2 * self.image_width - (S.obs_source_get_width(source) * item['Large Scale']))/2
            
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, key), item['Location'])
            S.obs_source_release(source)

        self.indicator_scale('Large')

def script_load(settings):

    S.timer_add(check_for_updates, 1000)

    global globalsettings
    globalsettings = settings

    global getimage
    getimage = rosterimages()

    global visible_bool
    visible_bool = S.obs_data_get_bool(settings, '_visible')

    getimage.new_event = 1
    getimage.dir_scan()

    print(getimage.scene)

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, '_path')


def check_for_updates():
   if pause_bool == False:
        update = getimage.dir_scan()
        if update:
            getimage.update_images()

def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    getimage.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, '_pause')

    indicator_bool = S.obs_data_get_bool(settings, '_indicator')

    global visible_bool
    visible_bool = S.obs_data_get_bool(settings, '_visible')
    away_indicator_source = S.obs_get_source_by_name('Away Indicator')
    home_indicator_source = S.obs_get_source_by_name('Home Indicator')

    if indicator_bool == True:
        S.obs_source_set_enabled(away_indicator_source, False)
        S.obs_source_set_enabled(home_indicator_source, False)
    else:
        S.obs_source_set_enabled(away_indicator_source, True)
        S.obs_source_set_enabled(home_indicator_source, True)

    S.obs_source_release(away_indicator_source)
    S.obs_source_release(home_indicator_source)

def add_pressed(props, prop):
    getimage.add_rosters()
    getimage.new_event = 1
    getimage.dir_scan()
    getimage.update_images()
    print(getimage.roster_image_list)

    settings = S.obs_data_create()
    layout_callback(props, prop, settings)
    S.obs_data_release(settings)

def remove_pressed(props, prop):
    source = S.obs_get_source_by_name(getimage.home_group)
    S.obs_source_remove(source)
    S.obs_source_release(source)

    source = S.obs_get_source_by_name(getimage.away_group)
    S.obs_source_remove(source)
    S.obs_source_release(source)

    source = S.obs_get_source_by_name(getimage.away_player_text_source)
    S.obs_source_remove(source)
    S.obs_source_release(source)

    source = S.obs_get_source_by_name(getimage.home_player_text_source)
    S.obs_source_remove(source)
    S.obs_source_release(source)

def flip_teams(props, prop):
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.home_group), getimage.home_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.away_group), getimage.away_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.home_player_text_source), getimage.home_player_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.away_player_text_source), getimage.away_player_loc)

    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.home_group), getimage.away_roster_loc)
    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.away_group), getimage.home_roster_loc)
    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.home_player_text_source), getimage.away_player_loc)
    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.away_player_text_source), getimage.home_player_loc)

    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.home_group), getimage.home_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.away_group), getimage.away_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.home_player_text_source), getimage.home_player_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, getimage.away_player_text_source), getimage.away_player_loc)

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_bool(props, '_pause', 'Pause')
    S.obs_properties_add_button(props, '_add_button', 'Add', add_pressed)
    S.obs_properties_add_button(props, '_removebutton', 'Remove', remove_pressed)

    OS_list = S.obs_properties_add_list(props, '_OS_list', 'HUD File Path:', S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, 'Custom', 'custom')
    S.obs_property_list_add_string(OS_list, 'Windows Default Path', 'windows')
    S.obs_property_list_add_string(OS_list, 'MacOS Default Path', 'macOS')
    file_path_input = S.obs_properties_add_text(props, '_path', 'HUD File Path:', S.OBS_TEXT_DEFAULT)

    roster_layout = S.obs_properties_add_list(props, '_roster_layout', 'Roster Layout:', S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(roster_layout, 'Horizontal', 'horizontal')
    S.obs_property_list_add_string(roster_layout, 'Veritcal', 'vertical')
    S.obs_property_list_add_string(roster_layout, '2 x 4', '2x4')
    S.obs_property_list_add_string(roster_layout, '2 x 4 Vertical', '2x4vertical')
    S.obs_property_list_add_string(roster_layout, 'Captains', 'captainshorizontal')
    S.obs_property_list_add_string(roster_layout, 'Captains Vertical', 'captainsvertical')

    S.obs_properties_add_button(props, '_flipteams', 'Flip Team Locations', flip_teams)

    S.obs_properties_add_bool(props, '_visible', 'Automatically make visible:')

    S.obs_property_set_modified_callback(OS_list, OS_callback)
    S.obs_property_set_modified_callback(roster_layout, layout_callback)

    return props

def OS_callback(props, prop, settings):
    if S.obs_data_get_string(settings, '_OS_list') == 'windows':
        current_path = str(os.path.realpath(__file__))
        HUD_Path = current_path.split('\\')[0] + '/' + current_path.split('\\')[1] + '/' + current_path.split('\\')[2] + '/Documents/Project Rio/HudFiles/decoded.hud.json'
        S.obs_data_set_string(settings, '_path', HUD_Path)
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), False)
    elif S.obs_data_get_string(settings, '_OS_list') == 'macOS':
        current_path = str(os.path.realpath(__file__))
        HUD_Path = '/'+current_path.split('/', 3)[1] + '/' + current_path.split('/', 3)[2] + '/' + 'Library/Application Support/Project Rio/HudFiles/decoded.hud.json'
        S.obs_data_set_string(settings, '_path', HUD_Path)
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), False)
    else:
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), True)

    return True

def layout_callback(props, prop, settings):
    if S.obs_data_get_string(settings, '_roster_layout') == 'horizontal':
        getimage.set_position_straight('Horizontal')
    if S.obs_data_get_string(settings, '_roster_layout') == 'vertical':
        getimage.set_position_straight('Vertical')
    if S.obs_data_get_string(settings, '_roster_layout') == '2x4':
        getimage.set_position_2x4('Horizontal')
    if S.obs_data_get_string(settings, '_roster_layout') == '2x4vertical':
        getimage.set_position_2x4('Vertical')
    if S.obs_data_get_string(settings, '_roster_layout') == 'captainshorizontal':
        getimage.set_position_captains('Horizontal')
    if S.obs_data_get_string(settings, '_roster_layout') == 'captainsvertical':
        getimage.set_position_captains('Vertical')
    return True