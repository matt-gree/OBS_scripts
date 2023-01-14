import obspython as S
import os
import json
import platform as plt

#def script_defaults(settings):

images_directory = str(os.path.dirname(__file__)) + "/Images/"

class rosterimages:
    def __init__(self):

        self.location = S.vec2()

        self.away_team_roster = []
        self.home_team_roster = []

        self.halfinning = 0

        self.away_team_captain = str()
        self.home_team_captain = str()

        self.current_event_num = -1

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        self.roster_image_list = [
            ["Team0Roster0", 0, "", S.vec2()],
            ["Team0Roster1", 0, "", S.vec2()],
            ["Team0Roster2", 0, "", S.vec2()],
            ["Team0Roster3", 0, "", S.vec2()],
            ["Team0Roster4", 0, "", S.vec2()],
            ["Team0Roster5", 0, "", S.vec2()],
            ["Team0Roster6", 0, "", S.vec2()],
            ["Team0Roster7", 0, "", S.vec2()],
            ["Team0Roster8", 0, "", S.vec2()],
            ["Team1Roster0", 0, "", S.vec2()],
            ["Team1Roster1", 0, "", S.vec2()],
            ["Team1Roster2", 0, "", S.vec2()],
            ["Team1Roster3", 0, "", S.vec2()],
            ["Team1Roster4", 0, "", S.vec2()],
            ["Team1Roster5", 0, "", S.vec2()],
            ["Team1Roster6", 0, "", S.vec2()],
            ["Team1Roster7", 0, "", S.vec2()],
            ["Team1Roster8", 0, "", S.vec2()],
        ]

        self.indicator_image_list = [
            ["away_indicator", S.vec2()],
            ["home_indicator", S.vec2()]
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

        self.home_player = ""
        self.away_player = ""

        if str(plt.platform()).lower()[0] == 'm':
            self.platform = 'MacOS'
            current_path = str(os.path.realpath(__file__))
            """self.HUD_path = "/" + current_path.split("/", 3)[1] + "/" + current_path.split("/", 3)[
                2] + "/" + "Library/Application Support/ProjectRio/HudFiles/decoded.hud.json" """
        elif str(plt.platform()).lower()[0] == 'w':
            self.platform = 'Windows'
            current_path = str(os.path.realpath(__file__))
            """self.HUD_path = current_path.split("\\")[0] + "/" + current_path.split("\\")[1] + "/" + current_path.split("\\")[
                2] + "/Documents/Project Rio/HudFiles/decoded.hud.json" """
        else:
            self.platform = 'Unknown'

        self.indicator_images_exist = True

    def add_image_source(self, image_name, OBS_name, scene):
        #will only add images in the images_directory
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "file", str(images_directory) + image_name + '.png')
        source = S.obs_source_create("image_source", OBS_name, settings, None)
        S.obs_scene_add(scene, source)

    def add_captains(self):
        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        home_group = S.obs_scene_add_group(self.scene, "Home Roster")
        away_group = S.obs_scene_add_group(self.scene, "Away Roster")
        #Home and Away Player Names
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Home_Captain_Text = S.obs_source_create("text_ft2_source", 'home_player_text', settings, None)
        else:
            Home_Captain_Text = S.obs_source_create("text_gdiplus", 'home_player_text', settings, None)
        S.obs_scene_add(self.scene, Home_Captain_Text)

        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Away_Captain_Text = S.obs_source_create("text_ft2_source", 'away_player_text', settings, None)
        else:
            Away_Captain_Text = S.obs_source_create("text_gdiplus", 'away_player_text', settings, None)
        S.obs_scene_add(self.scene, Away_Captain_Text)
        text_postions = S.vec2()
        text_postions.x = 500
        text_postions.y = 500
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, 'home_player_text'), text_postions)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, 'away_player_text'), text_postions)

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
        hud_file_path = S.obs_data_get_string(globalsettings, "_path")
        if not os.path.isfile(hud_file_path):
            return ""

        with open(hud_file_path) as f:
            hud_data = json.load(f)

        # Return if the event hasn't changed
        if (self.current_event_num == hud_data['Event Num']):
            if (self.new_event != 1):
                return self.current_event_num

        if hud_data['Event Num'] == "0a":
            return self.current_event_num

        print(hud_data['Event Num'])

        self.halfinning = hud_data["Half Inning"]

        self.new_event = 1

        self.current_event_num = hud_data['Event Num']

        self.home_player = hud_data["Home Player"]
        self.away_player = hud_data["Away Player"]

        # Roster Data
        for team in range(0, 2):
            for roster in range(0, 9):
                team_roster_str = "Team " + str(team) + " Roster " + str(roster)
                if (team == 0) & (hud_data[team_roster_str]["Captain"] != 1):
                    self.roster_image_list[roster][2] = (str(hud_data[team_roster_str]["CharID"]))
                    self.roster_image_list[roster][1] = 0
                elif (team == 1) & (hud_data[team_roster_str]["Captain"] != 1):
                    self.roster_image_list[roster+9][2] = (str(hud_data[team_roster_str]["CharID"]))
                    self.roster_image_list[roster + 9][1] = 0
                else:
                    # Captains
                    if (team == 0):
                        self.roster_image_list[roster][2] = (str(hud_data[team_roster_str]["CharID"]))
                        self.roster_image_list[roster][1] = 1
                    else:
                        self.roster_image_list[roster+9][2] = (str(hud_data[team_roster_str]["CharID"]))
                        self.roster_image_list[roster+9][1] = 1

        for index in range(0,18):
            i = 0
            if self.roster_image_list[index][1] == 1:
                if index < 9:
                    away_captain_index = index
                else:
                    home_captain_index = index

        self.roster_image_list[away_captain_index][1] = 0
        self.roster_image_list[home_captain_index-9][1] = 1
        self.roster_image_list[home_captain_index][1] = 0
        self.roster_image_list[away_captain_index+9][1] = 1

        print(self.roster_image_list[away_captain_index][2])
        print(self.roster_image_list[home_captain_index][2])

    def update_images(self):
        if (self.new_event == 0):
            return self.current_event_num

        for image in self.roster_image_list:
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "file",
                                            str(images_directory) + str(image[2]) + '.png')
            source = S.obs_get_source_by_name(image[0])
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

        source = S.obs_get_source_by_name("home_player_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.home_player))

        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        source = S.obs_get_source_by_name("away_player_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.away_player))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        self.new_event = 0

        if S.obs_data_get_string(globalsettings, "_roster_layout") == "horizontal":
            self.set_position_horizontal()
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "vertical":
            self.set_position_vertical()
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "2x4":
            self.set_position_2x4()
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "2x4vertical":
            self.set_position_2x4_vertical()
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "captainshorizontal":
            self.set_position_captainshorizontal()
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "captainsvertical":
            self.set_position_captainsvertical()

        if self.halfinning == 0:
            source = S.obs_get_source_by_name("home_indicator")
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "file", str(images_directory) + str("glove") + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

            source = S.obs_get_source_by_name("away_indicator")
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "file", str(images_directory) + str("bat") + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

        elif self.halfinning == 1:
            source = S.obs_get_source_by_name("home_indicator")
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "file", str(images_directory) + str("bat") + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

            source = S.obs_get_source_by_name("away_indicator")
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "file", str(images_directory) + str("glove") + '.png')
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)

    def indicator_scale(self, size):
        if size == "small":
            self.away_indicator_scale.x = self.away_indicator_scale_multiplier_small
            self.away_indicator_scale.y = self.away_indicator_scale_multiplier_small
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, "away_indicator"), self.away_indicator_scale)

            self.home_indicator_scale.x = self.home_indicator_scale_multiplier_small
            self.home_indicator_scale.y = self.home_indicator_scale_multiplier_small
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, "home_indicator"), self.home_indicator_scale)

        elif size == "large":
            self.away_indicator_scale.x = self.away_indicator_scale_multiplier_large
            self.away_indicator_scale.y = self.away_indicator_scale_multiplier_large
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, "away_indicator"), self.away_indicator_scale)

            self.home_indicator_scale.x = self.home_indicator_scale_multiplier_large
            self.home_indicator_scale.y = self.home_indicator_scale_multiplier_large
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, "home_indicator"), self.home_indicator_scale)

    def pre_postion_update(self):
        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        if S.obs_get_source_by_name("Team1Roster8") is not None:
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "home_player_text"), self.home_player_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "away_player_text"), self.away_player_loc)
            for item in self.roster_image_list:
                S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, item[0]), item[3])
        else:
            self.home_roster_loc = S.vec2()
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
            self.away_roster_loc = S.vec2()
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)


        if S.obs_get_source_by_name("away_indicator") is not None:
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "away_player_text"), self.indicator_image_list[0][1])
        if S.obs_get_source_by_name("home_indicator") is not None:
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "home_player_text"), self.indicator_image_list[1][1])

        #Batting and Fielding Icon Scale
        if S.obs_source_get_width(S.obs_get_source_by_name('away_indicator')) == 0:
            self.away_indicator_scale_multiplier_small = 0
            self.away_indicator_scale_multiplier_large = 0
        else:
            self.away_indicator_scale_multiplier_small = (self.image_width)/S.obs_source_get_width(S.obs_get_source_by_name('away_indicator'))
            self.away_indicator_scale_multiplier_large = self.away_indicator_scale_multiplier_small * self.captain_size_multiplier

        if S.obs_source_get_width(S.obs_get_source_by_name('home_indicator')) == 0:
            self.home_indicator_scale_multiplier_small = 0
            self.home_indicator_scale_multiplier_large = 0
        else:
            self.home_indicator_scale_multiplier_small = (self.image_width) / S.obs_source_get_width(S.obs_get_source_by_name('home_indicator'))
            self.home_indicator_scale_multiplier_large = self.home_indicator_scale_multiplier_small * self.captain_size_multiplier

    def enable_roster_images(self):
        for i in range(0, len(self.roster_image_list)):
            S.obs_source_set_enabled(S.obs_get_source_by_name(self.roster_image_list[i][0]), True)

    def alignment(self, source_name, align_int):
        # align_int = 8 for center bottom, = 9 for bottom left
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
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)


        self.alignment("away_player_text", 9)
        self.alignment("home_player_text", 9)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].x = 9 * self.image_width
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale("small")

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
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)


        self.alignment("away_player_text", 8)
        self.alignment("home_player_text", 8)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].y = 9 * self.image_width
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale("small")

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

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)

        self.alignment("away_player_text", 9)
        self.alignment("home_player_text", 9)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].x = 4 * self.image_width + self.captain_size_multiplier * self.image_width
            self.indicator_image_list[i][1].y = (2 * self.image_width - (S.obs_source_get_width(S.obs_get_source_by_name(self.indicator_image_list[i][0])))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale("large")

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

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)

        self.alignment("away_player_text", 8)
        self.alignment("home_player_text", 8)

        #Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].y = 4 * self.image_width + self.captain_size_multiplier * self.image_width
            self.indicator_image_list[i][1].x = (2 * self.image_width - (S.obs_source_get_width(S.obs_get_source_by_name(self.indicator_image_list[i][0])))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale("large")

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
                S.obs_source_set_enabled(S.obs_get_source_by_name(self.roster_image_list[i][0]), False)

        self.alignment("away_player_text", 9)
        self.alignment("home_player_text", 9)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].x = self.captain_size_multiplier * self.image_width
            self.indicator_image_list[i][1].y = (2 * self.image_width - (S.obs_source_get_width(S.obs_get_source_by_name(self.indicator_image_list[i][0])))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale("large")

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
                S.obs_source_set_enabled(S.obs_get_source_by_name(self.roster_image_list[i][0]), False)

        self.alignment("away_player_text", 8)
        self.alignment("home_player_text", 8)

        # Set indicator location and scale
        for i in range(0,len(self.indicator_image_list)):
            S.vec2_zero(self.indicator_image_list[i][1])
            self.indicator_image_list[i][1].y = self.captain_size_multiplier * self.image_width
            self.indicator_image_list[i][1].x = (2 * self.image_width - (S.obs_source_get_width(S.obs_get_source_by_name(self.indicator_image_list[i][0])))*self.away_indicator_scale_multiplier_large)/2
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.indicator_image_list[i][0]), self.indicator_image_list[i][1])

        self.indicator_scale("large")

def script_load(settings):

    S.timer_add(check_for_updates, 1000)

    global globalsettings
    globalsettings = settings

    global getimage
    getimage = rosterimages()

    getimage.new_event = 1
    getimage.dir_scan()

    print(getimage.scene)

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, "_path")


def check_for_updates():
   if pause_bool == False:
       getimage.dir_scan()
       getimage.update_images()


def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    getimage.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, "_pause")

    indicator_bool = S.obs_data_get_bool(settings, "_indicator")
    if indicator_bool == True:
        S.obs_source_set_enabled(S.obs_get_source_by_name(getimage.indicator_image_list[0][0]), False)
        S.obs_source_set_enabled(S.obs_get_source_by_name(getimage.indicator_image_list[1][0]), False)
    else:
        S.obs_source_set_enabled(S.obs_get_source_by_name(getimage.indicator_image_list[0][0]), True)
        S.obs_source_set_enabled(S.obs_get_source_by_name(getimage.indicator_image_list[1][0]), True)


def script_description():
    return "Mario Baseball team roster images\nOBS interface by MattGree \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nDonations are welcomed!"

def add_pressed(props, prop):
    getimage.add_captains()
    getimage.new_event = 1
    getimage.dir_scan()
    getimage.update_images()
    print(getimage.roster_image_list)
    getimage.set_position_horizontal()

def refresh_pressed(props, prop):
    getimage.new_event = 1
    getimage.dir_scan()
    getimage.update_images()

def remove_pressed(props, prop):
    S.obs_source_remove(S.obs_get_source_by_name("Home Roster"))
    S.obs_source_remove(S.obs_get_source_by_name("Away Roster"))
    S.obs_source_remove(S.obs_get_source_by_name("Away Roster"))
    S.obs_source_remove(S.obs_get_source_by_name("away_player_text"))
    S.obs_source_remove(S.obs_get_source_by_name("home_player_text"))

def flip_teams(props, prop):
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "Home Roster"), getimage.home_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "Away Roster"), getimage.away_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "home_player_text"), getimage.home_player_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "away_player_text"), getimage.away_player_loc)

    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, "Home Roster"), getimage.away_roster_loc)
    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, "Away Roster"), getimage.home_roster_loc)
    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, "home_player_text"), getimage.away_player_loc)
    S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(getimage.scene, "away_player_text"), getimage.home_player_loc)

    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "Home Roster"), getimage.home_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "Away Roster"), getimage.away_roster_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "home_player_text"), getimage.home_player_loc)
    S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(getimage.scene, "away_player_text"), getimage.away_player_loc)

def center_text_allignment(props, prop):
    getimage.alignment('away_player_text', 8)
    getimage.alignment('home_player_text', 8)

def left_text_allignment(props, prop):
    getimage.alignment('away_player_text', 9)
    getimage.alignment('home_player_text', 9)

def script_properties():
    props = S.obs_properties_create()
    #S.obs_properties_add_button(props, "refreshbutton", "Refresh HUD", refresh_pressed)
    S.obs_properties_add_bool(props, "_pause", "Pause")
    S.obs_properties_add_button(props, "_add_button", "Add", add_pressed)
    S.obs_properties_add_button(props, "_removebutton", "Remove", remove_pressed)

    OS_list = S.obs_properties_add_list(props, "_OS_list", "OS:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, "Custom", "custom")
    S.obs_property_list_add_string(OS_list, "Windows", "windows")
    S.obs_property_list_add_string(OS_list, "MacOS", "macOS")
    S.obs_properties_add_text(props, "_path", "Path to HUD json:", S.OBS_TEXT_DEFAULT)

    roster_layout = S.obs_properties_add_list(props, "_roster_layout", "Roster Layout:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(roster_layout, "Horizontal", "horizontal")
    S.obs_property_list_add_string(roster_layout, "Veritcal", "vertical")
    S.obs_property_list_add_string(roster_layout, "2 x 4", "2x4")
    S.obs_property_list_add_string(roster_layout, "2 x 4 Vertical", "2x4vertical")
    S.obs_property_list_add_string(roster_layout, "Captains", "captainshorizontal")
    S.obs_property_list_add_string(roster_layout, "Captains Vertical", "captainsvertical")

    S.obs_properties_add_button(props, "_flipteams", "Flip Team Locations", flip_teams)

    S.obs_properties_add_button(props, "_centerallignment", "Text Allignment Center", center_text_allignment)
    S.obs_properties_add_button(props, "_leftallignment", "Text Allignment Left", left_text_allignment)

    font_property = S.obs_properties_add_font(props, "_player_font", "Player Font:")

    S.obs_properties_add_bool(props, "_indicator", "Remove Indicators")

    S.obs_property_set_modified_callback(OS_list, OS_callback)
    S.obs_property_set_modified_callback(roster_layout, layout_callback)
    S.obs_property_set_modified_callback(font_property, font_callback)

    return props

def OS_callback(props, prop, settings):
    if S.obs_data_get_string(settings, "_OS_list") == "windows":
        current_path = str(os.path.realpath(__file__))
        HUD_Path = current_path.split("\\")[0] + "/" + current_path.split("\\")[1] + "/" + current_path.split("\\")[2] + "/Documents/Project Rio/HudFiles/decoded.hud.json"
        S.obs_data_set_string(settings, "_path", HUD_Path)
    elif S.obs_data_get_string(settings, "_OS_list") == "macOS":
        current_path = str(os.path.realpath(__file__))
        HUD_Path = "/"+current_path.split("/", 3)[1] +"/"+ current_path.split("/", 3)[2] + "/" + "Library/Application Support/ProjectRio/HudFiles/decoded.hud.json"
        S.obs_data_set_string(settings, "_path", HUD_Path)
    return True

def layout_callback(props, prop, settings):
    if S.obs_data_get_string(settings, "_roster_layout") == "horizontal":
        getimage.set_position_horizontal()
    if S.obs_data_get_string(settings, "_roster_layout") == "vertical":
        getimage.set_position_vertical()
    if S.obs_data_get_string(settings, "_roster_layout") == "2x4":
        getimage.set_position_2x4()
    if S.obs_data_get_string(settings, "_roster_layout") == "2x4vertical":
        getimage.set_position_2x4_vertical()
    if S.obs_data_get_string(settings, "_roster_layout") == "captainshorizontal":
        getimage.set_position_captainshorizontal()
    if S.obs_data_get_string(settings, "_roster_layout") == "captainsvertical":
        getimage.set_position_captainsvertical()
    return True

def font_callback(props, prop, settings):
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_player_font"))
    source = S.obs_get_source_by_name("away_player_text")
    S.obs_data_set_bool(settings, "outline", True)
    S.obs_source_update(source, settings)
    source = S.obs_get_source_by_name("home_player_text")
    S.obs_source_update(source, settings)

    return True