import obspython as S
import os
import json
import platform as plt
import TeamNameAlgo

def script_description():
    return 'Mario Baseball Team HUD Version 1.3.11 \nOBS interface by MattGree \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nDonations are welcomed!'


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

        self.indicator_image_list = [
            ['away_indicator', S.vec2()],
            ['home_indicator', S.vec2()]
        ]

        self.logo_image_list = [
            ['Away Logo', '', S.vec2()],
            ['Home Logo', '', S.vec2()]
        ]

        self.new_event = 0

        self.home_roster_loc = S.vec2()
        self.away_roster_loc = S.vec2()

        self.home_player_loc = S.vec2()
        self.away_player_loc = S.vec2()

        self.image_width = 60
        self.captain_size_multiplier = 1.6

        self.away_indicator_scale = S.vec2()
        self.home_indicator_scale = S.vec2()

        self.away_indicator_scale_multiplier_small = 0
        self.home_indicator_scale_multiplier_small = 0

        self.away_indicator_scale_multiplier_large = 0
        self.home_indicator_scale_multiplier_large = 0

        self.home_player = ''
        self.away_player = ''

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

        #Team Logos
        self.add_image_source(self.logo_image_list[0][1], 'Away Logo', self.scene)
        S.obs_sceneitem_group_add_item(away_group, S.obs_scene_find_source(self.scene, 'Away Logo'))

        self.add_image_source(self.logo_image_list[1][1], 'Home Logo', self.scene)
        S.obs_sceneitem_group_add_item(home_group, S.obs_scene_find_source(self.scene, 'Home Logo'))

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
                                     or (int(str(hud_data['Event Num'])[:-1]) < int(str(self.current_event_num)[:-1]))):
            
            if (self.away_player == hud_data['Home Player']) and (self.home_player == hud_data['Away Player']):
                print('flipped')
                flip_teams('', '')

            self.set_visible()
            print("visible")


        self.current_event_num = hud_data['Event Num']

        print(hud_data['Event Num'])

        self.halfinning = hud_data['Half Inning']

        self.new_event = 1

        self.home_player = hud_data['Home Player']
        self.away_player = hud_data['Away Player']

        # Roster Data
        for team in range(2):
            team_string = "Away" if team == 0 else "Home"
            for roster in range(9):
                team_roster_str = f'{team_string} Roster {roster}'
                captain = hud_data[team_roster_str]['Captain']
                #print(team_roster_str, hud_data[team_roster_str])
                #print(roster, captain)
                char_id = hud_data[team_roster_str]['CharID']
                index = roster + (team * 9)
                print(index)
                self.roster_image_list[index][2] = str(char_id)
                self.roster_image_list[index][1] = 1 if captain == 1 else 0

        for i in range(0,18):
            if self.roster_image_list[i][1] == 1:
                if i < 9:
                    self.away_captain_index = i
                else:
                    self.home_captain_index = i


        if self.away_captain_index == -1:
            raise ValueError("Away captain not found:")

        if self.home_captain_index == -1:
            raise ValueError("Home captain not found:")
        
        self.roster_image_list[self.away_captain_index][1] = 0
        self.roster_image_list[self.home_captain_index-9][1] = 1
        self.roster_image_list[self.home_captain_index][1] = 0
        self.roster_image_list[self.away_captain_index+9][1] = 1

        self.away_roster = [element[2] for element in self.roster_image_list[:9]]
        self.home_roster = [element[2] for element in self.roster_image_list[9:]]

        print(self.away_roster)
        print(self.home_roster)

        self.logo_image_list[0][1] = TeamNameAlgo.Team_Name(self.away_roster, self.roster_image_list[self.home_captain_index-9][2])
        self.logo_image_list[1][1] = TeamNameAlgo.Team_Name(self.home_roster, self.roster_image_list[self.away_captain_index+9][2])

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

        for logo in self.logo_image_list:
            source = S.obs_get_source_by_name(logo[0])
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + logo[1] + '.png')
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
            self.set_position_horizontal()
        if S.obs_data_get_string(globalsettings, '_roster_layout') == 'vertical':
            self.set_position_vertical()
        if S.obs_data_get_string(globalsettings, '_roster_layout') == '2x4':
            self.set_position_2x4()
        if S.obs_data_get_string(globalsettings, '_roster_layout') == '2x4vertical':
            self.set_position_2x4_vertical()
        if S.obs_data_get_string(globalsettings, '_roster_layout') == 'captainshorizontal':
            self.set_position_captainshorizontal()
        if S.obs_data_get_string(globalsettings, '_roster_layout') == 'captainsvertical':
            self.set_position_captainsvertical()

        if self.halfinning == 0:
            source = S.obs_get_source_by_name('home_indicator')
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + str('glove') + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

            source = S.obs_get_source_by_name('away_indicator')
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + str('bat') + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

        elif self.halfinning == 1:
            source = S.obs_get_source_by_name('home_indicator')
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + str('bat') + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

            source = S.obs_get_source_by_name('away_indicator')
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, 'file', str(images_directory) + str('glove') + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

    def indicator_scale(self, size):
        if size == 'small':
            self.away_indicator_scale.x = self.away_indicator_scale_multiplier_small
            self.away_indicator_scale.y = self.away_indicator_scale_multiplier_small
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, 'away_indicator'), self.away_indicator_scale)

            self.home_indicator_scale.x = self.home_indicator_scale_multiplier_small
            self.home_indicator_scale.y = self.home_indicator_scale_multiplier_small
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, 'home_indicator'), self.home_indicator_scale)

        elif size == 'large':
            self.away_indicator_scale.x = self.away_indicator_scale_multiplier_large
            self.away_indicator_scale.y = self.away_indicator_scale_multiplier_large
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, 'away_indicator'), self.away_indicator_scale)

            self.home_indicator_scale.x = self.home_indicator_scale_multiplier_large
            self.home_indicator_scale.y = self.home_indicator_scale_multiplier_large
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, 'home_indicator'), self.home_indicator_scale)

    def pre_postion_update(self):
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


        away_indicator = S.obs_get_source_by_name('away_indicator')
        home_indicator = S.obs_get_source_by_name('home_indicator')

        if away_indicator:
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.away_player_text_source), self.indicator_image_list[0][1])
        if home_indicator:
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.home_player_text_source), self.indicator_image_list[1][1])

        #Batting and Fielding Icon Scale
        if S.obs_source_get_width(away_indicator) == 0:
            self.away_indicator_scale_multiplier_small = 0
            self.away_indicator_scale_multiplier_large = 0
        else:
            self.away_indicator_scale_multiplier_small = (self.image_width)/S.obs_source_get_width(away_indicator)
            self.away_indicator_scale_multiplier_large = self.away_indicator_scale_multiplier_small * self.captain_size_multiplier

        if S.obs_source_get_width(home_indicator) == 0:
            self.home_indicator_scale_multiplier_small = 0
            self.home_indicator_scale_multiplier_large = 0
        else:
            self.home_indicator_scale_multiplier_small = (self.image_width) / S.obs_source_get_width(home_indicator)
            self.home_indicator_scale_multiplier_large = self.home_indicator_scale_multiplier_small * self.captain_size_multiplier

        S.obs_source_release(away_indicator)
        S.obs_source_release(home_indicator)

    def alignment(self, source_name, align_int):
        # align_int = 4 for center top, 8 for center bottom, = 9 for bottom left
        source = S.obs_get_source_by_name(source_name)
        scene_item = S.obs_scene_find_source(getimage.scene, source_name)
        info = S.obs_transform_info()
        S.obs_sceneitem_get_info(scene_item, info)
        info.alignment = align_int
        S.obs_sceneitem_set_info(scene_item, info)
        S.obs_source_release(source)

    def set_position_horizontal(self):
        self.enable_roster_images()
        self.pre_postion_update()

        for i in range(0, len(self.roster_image_list)):
            scale = S.vec2()
            scale.x = 1
            scale.y = 1
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                      scale)
            S.vec2_zero(self.roster_image_list[i][3])
            self.roster_image_list[i][3].x = i * self.image_width
            if i > 8:
                self.roster_image_list[i][3].x = (i-9) * self.image_width
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), self.roster_image_list[i][3])
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].x = 9 * self.image_width
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale('small')

    def set_position_vertical(self):
        self.enable_roster_images()
        self.pre_postion_update()

        for i in range(0, len(self.roster_image_list)):
            scale = S.vec2()
            scale.x = 1
            scale.y = 1
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), scale)
            S.vec2_zero(self.roster_image_list[i][3])
            self.roster_image_list[i][3].y = i * self.image_width
            if i > 8:
                self.roster_image_list[i][3].y = (i-9) * self.image_width
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), self.roster_image_list[i][3])
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].y = 9 * self.image_width
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale('small')

    def set_position_2x4(self):
        self.enable_roster_images()
        self.pre_postion_update()
        counter = 0
        for i in range(0,len(self.roster_image_list)):
            S.vec2_zero(self.roster_image_list[i][3])
            if self.roster_image_list[i][1] == 1:
                scale = S.vec2()
                scale.x = self.captain_size_multiplier
                scale.y = self.captain_size_multiplier
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), scale)
                if i < 8:
                    self.roster_image_list[i][3].y = 0.2 * self.image_width
                else:
                    self.roster_image_list[i][3].y = 0.2 * self.image_width
            else:
                scale = S.vec2()
                scale.x = 1
                scale.y = 1
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                          scale)
                if counter%8 < 4:
                    self.roster_image_list[i][3].x = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                    counter +=1
                else:
                    self.roster_image_list[i][3].x = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                    self.roster_image_list[i][3].y = self.image_width
                    counter += 1
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                    self.roster_image_list[i][3])

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].x = 4 * self.image_width + self.captain_size_multiplier * self.image_width
            source = S.obs_get_source_by_name(self.indicator_image_list[i][0])
            self.indicator_image_list[i][1].y = (2 * self.image_width - (S.obs_source_get_width(source))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])
            S.obs_source_release(source)
        self.indicator_scale('large')

    def set_position_2x4_vertical(self):
        self.enable_roster_images()
        self.pre_postion_update()
        counter = 0
        for i in range(0,len(self.roster_image_list)):
            S.vec2_zero(self.roster_image_list[i][3])
            if self.roster_image_list[i][1] == 1:
                print(self.roster_image_list[i][2])
                scale = S.vec2()
                scale.x = self.captain_size_multiplier
                scale.y = self.captain_size_multiplier
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), scale)
                if i < 8:
                    self.roster_image_list[i][3].x = 0.2 * self.image_width
                else:
                    self.roster_image_list[i][3].x = 0.2 * self.image_width
            else:
                scale = S.vec2()
                scale.x = 1
                scale.y = 1
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                          scale)
                if counter%8 < 4:
                    self.roster_image_list[i][3].y = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                    counter +=1
                else:
                    self.roster_image_list[i][3].y = counter%4 * self.image_width + self.captain_size_multiplier *self.image_width
                    self.roster_image_list[i][3].x = self.image_width
                    counter += 1
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                    self.roster_image_list[i][3])

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.home_group), self.home_roster_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, self.away_group), self.away_roster_loc)

        #Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].y = 4 * self.image_width + self.captain_size_multiplier * self.image_width
            source = S.obs_get_source_by_name(self.indicator_image_list[i][0])
            self.indicator_image_list[i][1].x = (2 * self.image_width - (S.obs_source_get_width(source))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])
            S.obs_source_release(source)

        self.indicator_scale('large')

    def set_position_captainshorizontal(self):
        self.pre_postion_update()
        self.set_position_2x4()
        for i in range(0, len(self.roster_image_list)):
            S.vec2_zero(self.roster_image_list[i][3])
            if self.roster_image_list[i][1] == 1:
                scale = S.vec2()
                scale.x = self.captain_size_multiplier
                scale.y = self.captain_size_multiplier
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                          scale)
                if i < 8:
                    self.roster_image_list[i][3].y = 0.2 * self.image_width
                else:
                    self.roster_image_list[i][3].y = 0.2 * self.image_width
            else:
                source = S.obs_get_source_by_name(self.roster_image_list[i][0])
                S.obs_source_set_enabled(source, False)
                S.obs_source_release(source)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].x = self.captain_size_multiplier * self.image_width
            source = S.obs_get_source_by_name(self.indicator_image_list[i][0])
            self.indicator_image_list[i][1].y = (2 * self.image_width - (S.obs_source_get_width(source))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])
            S.obs_source_release(source)

        self.indicator_scale('large')

    def set_position_captainsvertical(self):
        self.pre_postion_update()
        self.set_position_2x4_vertical()
        for i in range(0, len(self.roster_image_list)):
            S.vec2_zero(self.roster_image_list[i][3])
            if self.roster_image_list[i][1] == 1:
                scale = S.vec2()
                scale.x = self.captain_size_multiplier
                scale.y = self.captain_size_multiplier
                S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                          scale)
                if i < 8:
                    self.roster_image_list[i][3].y = 0.2 * self.image_width
                else:
                    self.roster_image_list[i][3].y = 0.2 * self.image_width
            else:
                source = S.obs_get_source_by_name(self.roster_image_list[i][0])
                S.obs_source_set_enabled(source, False)
                S.obs_source_release(source)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].y = self.captain_size_multiplier * self.image_width
            source = S.obs_get_source_by_name(self.indicator_image_list[i][0])
            self.indicator_image_list[i][1].x = (2 * self.image_width - (S.obs_source_get_width(source))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])
            S.obs_source_release(source)

        self.indicator_scale('large')

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
       getimage.dir_scan()
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
    away_indicator_source = S.obs_get_source_by_name(getimage.indicator_image_list[0][0])
    home_indicator_source = S.obs_get_source_by_name(getimage.indicator_image_list[1][0])

    if indicator_bool == True:
        S.obs_source_set_enabled(away_indicator_source, False)
        S.obs_source_set_enabled(home_indicator_source, False)
    else:
        S.obs_source_set_enabled(away_indicator_source, True)
        S.obs_source_set_enabled(home_indicator_source, True)

    S.obs_source_release(away_indicator_source)
    S.obs_source_release(home_indicator_source)

def add_pressed(props, prop):
    getimage.add_captains()
    getimage.new_event = 1
    getimage.dir_scan()
    getimage.update_images()
    print(getimage.roster_image_list)

    settings = S.obs_data_create()
    layout_callback(props, prop, settings)
    S.obs_data_release(settings)

def refresh_pressed(props, prop):
    getimage.new_event = 1
    getimage.dir_scan()
    getimage.update_images()

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

    S.obs_properties_add_bool(props, '_indicator', 'Remove Indicators')

    S.obs_properties_add_bool(props, '_visible', 'Automatically make visible:')

    S.obs_property_set_modified_callback(OS_list, OS_callback)
    S.obs_property_set_modified_callback(roster_layout, layout_callback)
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
        HUD_Path = '/'+current_path.split('/', 3)[1] + '/' + current_path.split('/', 3)[2] + '/' + 'Library/Application Support/Project Rio/HudFiles/decoded.hud.json'
        S.obs_data_set_string(settings, '_path', HUD_Path)
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), False)
    else:
        S.obs_property_set_visible(S.obs_properties_get(props, "_path"), True)

    return True

def layout_callback(props, prop, settings):
    if S.obs_data_get_string(settings, '_roster_layout') == 'horizontal':
        left_text_allignment(props, prop)
        getimage.set_position_horizontal()
    if S.obs_data_get_string(settings, '_roster_layout') == 'vertical':
        center_text_allignment(props, prop)
        getimage.set_position_vertical()
    if S.obs_data_get_string(settings, '_roster_layout') == '2x4':
        left_text_allignment(props, prop)
        getimage.set_position_2x4()
    if S.obs_data_get_string(settings, '_roster_layout') == '2x4vertical':
        center_text_allignment(props, prop)
        getimage.set_position_2x4_vertical()
    if S.obs_data_get_string(settings, '_roster_layout') == 'captainshorizontal':
        left_text_allignment(props, prop)
        getimage.set_position_captainshorizontal()
    if S.obs_data_get_string(settings, '_roster_layout') == 'captainsvertical':
        center_text_allignment(props, prop)
        getimage.set_position_captainsvertical()
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