import obspython as S
import os
import json
import platform as plt
import TeamNameAlgo
import requests
import time
import RioHudLib
import threading
import RioStatsConverter

test_data =  {'away_captain': 1, 'away_player': 'Away Player', 'away_roster_0_char': 1, 'away_roster_1_char': 1, 'away_roster_2_char': 1, 'away_roster_3_char': 1, 'away_roster_4_char': 1, 'away_roster_5_char': 1, 'away_roster_6_char': 1, 'away_roster_7_char': 1, 'away_roster_8_char': 1, 'away_score': 0, 'away_stars': 5, 'batter': 7, 'half_inning': 0, 'home_captain': 0, 'home_player': 'Home Player', 'home_roster_0_char': 0, 'home_roster_1_char': 0, 'home_roster_2_char': 0, 'home_roster_3_char': 0, 'home_roster_4_char': 0, 'home_roster_5_char': 0, 'home_roster_6_char': 0, 'home_roster_7_char': 0, 'home_roster_8_char': 0, 'home_score': 0, 'home_stars': 5, 'inning': 4, 'outs': 1, 'pitcher': 1, 'runner_on_first': True, 'runner_on_second': True, 'runner_on_third': True, 'stadium_id': 4, 'start_time': 1717140581, 'tag_set': 74}

def script_description():
    return 'Mario Baseball Team HUD Version 1.5 \nOBS interface by MattGree, \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nSupport me on YouTube.com/MattGree'


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
            'Away Logo': {'Image': '', 'Location': S.vec2(), 'Scale Vector': S.vec2(), 'Relative Position': 0,
                               'Small Scale': 0, 'Large Scale': 0, 'Group': self.away_group},
            'Home Logo': {'Image': '', 'Location': S.vec2(), 'Relative Position': 0,
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

        self.recent_live_games = {}

    def refesh_games_list(self):
        url_liveGames = 'https://api.projectrio.app//populate_db/ongoing_game/'
    
        liveGames_json = requests.get(url_liveGames).json()['ongoing_games']
        
        self.recent_live_games = {}
        self.recent_live_games["Select Game"] = test_data
        for game in liveGames_json:
            if int(game['start_time']) > (time.time() - 60*60*0.5): # 30 Minutes
                self.recent_live_games[f"{game['away_player']} @ {game['home_player']}"] = game

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

    def get_team_rosters_from_RW(self, game_key):
        selected_game = self.recent_live_games[game_key]
        self.away_player = selected_game['away_player']
        self.home_player = selected_game['home_player']
            
        for i in range(9):
            char_string = f'away_roster_{i}_char'
            self.roster_image_list[i][2] = RioStatsConverter.char_id(selected_game[char_string]).replace(' (', '()')
            self.roster_image_list[i][1] = 0
            if i == selected_game['away_captain']:
                self.roster_image_list[i][1] = 1

        for i in range(9):
            char_string = f'home_roster_{i}_char'
            self.roster_image_list[i+9][2] = RioStatsConverter.char_id(selected_game[char_string]).replace(' (', '()')
            self.roster_image_list[i+9][1] = 0
            if i == selected_game['home_captain']:
                self.roster_image_list[i+9][1] = 1

        self.away_roster = [element[2] for element in self.roster_image_list[:9]]
        self.home_roster = [element[2] for element in self.roster_image_list[9:]]

        print(self.away_roster)
        print(self.roster_image_list[selected_game['away_captain']][2])
        print(self.home_roster)
        print(self.roster_image_list[selected_game['home_captain']][2])

        self.addons_image_dict['Away Logo']['Image'] = TeamNameAlgo.Team_Name(self.away_roster, self.roster_image_list[selected_game['away_captain']][2])
        self.addons_image_dict['Home Logo']['Image'] = TeamNameAlgo.Team_Name(self.home_roster, self.roster_image_list[selected_game['home_captain']+9][2])

    def update_images(self):
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

    def alignment(self, source_name, align_int):
        # align_int = 4 for center top, 8 for center bottom, = 9 for bottom left
        source = S.obs_get_source_by_name(source_name)
        scene_item = S.obs_scene_find_source(getimage.scene, source_name)
        info = S.obs_transform_info()
        S.obs_sceneitem_get_info(scene_item, info)
        info.alignment = align_int
        S.obs_sceneitem_set_info(scene_item, info)
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
    global globalsettings
    globalsettings = settings

    global getimage
    getimage = rosterimages()

    global visible_bool
    visible_bool = S.obs_data_get_bool(settings, '_visible')

    getimage.new_event = 1
    getimage.refesh_games_list()

    print(getimage.scene)

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, '_path')


def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    getimage.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)


def add_pressed(props, prop):
    getimage.add_rosters()
    getimage.new_event = 1
    getimage.update_images()
    print(getimage.roster_image_list)
    settings = S.obs_data_create()
    layout_callback(props, prop, settings)
    S.obs_data_release(settings)

def refresh_pressed(props, prop):
    # Define a function to run the refresh_games_list method in a separate thread
    def refresh_in_thread():
        getimage.refesh_games_list()
        getimage.update_images()
        update_games_list()
        print('Updated')
        return True
    
    # Start a new thread
    refresh_thread = threading.Thread(target=refresh_in_thread)
    refresh_thread.start()

def update_games_list():
    global props
    live_games = S.obs_properties_get(props, '_live_games')
    S.obs_property_list_clear(live_games)

    S.obs_property_list_add_string(live_games, 'Select Team', 'selectteam')
    for game in getimage.recent_live_games.keys():
        S.obs_property_list_add_string(live_games, str(game), str(game))

    settings = S.obs_data_create()
    S.obs_properties_apply_settings(props, settings)
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

def center_text_allignment(props, prop):
    getimage.alignment(getimage.away_player_text_source, 4)
    getimage.alignment(getimage.home_player_text_source, 4)

def left_text_allignment(props, prop):
    getimage.alignment(getimage.away_player_text_source, 9)
    getimage.alignment(getimage.home_player_text_source, 9)

def script_properties():

    global props
    props = S.obs_properties_create()
    # S.obs_properties_add_button(props, 'refreshgames', 'Refresh Games', refresh_pressed)
    live_games = S.obs_properties_add_list(props, '_live_games', 'Live Games:', S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    
    for game in getimage.recent_live_games.keys():
        S.obs_property_list_add_string(live_games, str(game), str(game))

    S.obs_properties_add_button(props, '_add_button', 'Add', add_pressed)
    S.obs_properties_add_button(props, '_removebutton', 'Remove', remove_pressed)

    roster_layout = S.obs_properties_add_list(props, '_roster_layout', 'Roster Layout:', S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(roster_layout, 'Horizontal', 'horizontal')
    S.obs_property_list_add_string(roster_layout, 'Veritcal', 'vertical')
    S.obs_property_list_add_string(roster_layout, '2 x 4', '2x4')
    S.obs_property_list_add_string(roster_layout, '2 x 4 Vertical', '2x4vertical')
    S.obs_property_list_add_string(roster_layout, 'Captains', 'captainshorizontal')
    S.obs_property_list_add_string(roster_layout, 'Captains Vertical', 'captainsvertical')

    S.obs_properties_add_button(props, '_flipteams', 'Flip Team Locations', flip_teams)

    S.obs_properties_add_button(props, '_centerallignment', 'Text Allignment Center', center_text_allignment)
    S.obs_properties_add_button(props, '_leftallignment', 'Text Allignment Left', left_text_allignment)

    font_property = S.obs_properties_add_font(props, '_player_font', 'Player Font:')

    S.obs_property_set_modified_callback(live_games, game_select_callback)
    S.obs_property_set_modified_callback(roster_layout, layout_callback)
    S.obs_property_set_modified_callback(font_property, font_callback)

    return props

def game_select_callback(props, prop, settings):
    if S.obs_data_get_string(settings, '_live_games') in ['Select Team', 'selectteam', '']:
        return True
    getimage.get_team_rosters_from_RW(S.obs_data_get_string(settings, '_live_games'))
    getimage.update_images()

def layout_callback(props, prop, settings):
    if S.obs_data_get_string(settings, '_roster_layout') == 'horizontal':
        left_text_allignment(props, prop)
        getimage.set_position_straight('Horizontal')
    if S.obs_data_get_string(settings, '_roster_layout') == 'vertical':
        center_text_allignment(props, prop)
        getimage.set_position_straight('Vertical')
    if S.obs_data_get_string(settings, '_roster_layout') == '2x4':
        left_text_allignment(props, prop)
        getimage.set_position_2x4('Horizontal')
    if S.obs_data_get_string(settings, '_roster_layout') == '2x4vertical':
        center_text_allignment(props, prop)
        getimage.set_position_2x4('Vertical')
    if S.obs_data_get_string(settings, '_roster_layout') == 'captainshorizontal':
        left_text_allignment(props, prop)
        getimage.set_position_captains('Horizontal')
    if S.obs_data_get_string(settings, '_roster_layout') == 'captainsvertical':
        center_text_allignment(props, prop)
        getimage.set_position_captains('Vertical')
    return True

def font_callback(props, prop, settings):
    S.obs_data_set_obj(settings, 'font', S.obs_data_get_obj(settings, '_player_font'))
    source = S.obs_get_source_by_name(getimage.away_player_text_source)
    S.obs_data_set_bool(settings, 'outline', False)
    S.obs_source_update(source, settings)
    S.obs_source_release(source)

    source = S.obs_get_source_by_name(getimage.home_player_text_source)
    S.obs_source_update(source, settings)
    S.obs_source_release(source)

    return True
