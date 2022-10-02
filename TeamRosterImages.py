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

        self.home_roster_loc = S.vec2()
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"),
                                self.home_roster_loc)
        self.away_roster_loc = S.vec2()
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"),
                                self.away_roster_loc)

        self.new_event = 0
        self.images_added = False

        self.home_roster_loc = S.vec2()
        self.away_roster_loc = S.vec2()

        self.home_player_loc = S.vec2()
        self.away_player_loc = S.vec2()

        self.image_width = 60
        self.home_group_width = 0
        self.home_group_height = 0

        self.away_group_width = 0
        self.away_group_height = 0

        self.canvas_width = 1280
        self.canvas_height = 720

        self.home_player = ""
        self.away_player = ""

        if str(plt.platform()).lower()[0] == 'm':
            self.platform = 'MacOS'
            current_path = str(os.path.realpath(__file__))
            self.HUD_path = "/" + current_path.split("/", 3)[1] + "/" + current_path.split("/", 3)[
                2] + "/" + "Library/Application Support/ProjectRio/HudFiles/decoded.hud.json"
        elif str(plt.platform()).lower()[0] == 'w':
            self.platform = 'Windows'
            current_path = str(os.path.realpath(__file__))
            self.HUD_path = current_path.split("\\")[0] + "/" + current_path.split("\\")[1] + "/" + current_path.split("\\")[
                2] + "/Documents/Project Rio/HudFiles/decoded.hud.json"
        else:
            self.platform = 'Unknown'

    def add_captains(self):
        home_group = S.obs_scene_add_group(self.scene, "Home Roster")
        away_group = S.obs_scene_add_group(self.scene, "Away Roster")
        for i in range(0,len(self.roster_image_list)):
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "file", str(images_directory) + str(self.away_team_captain) + '.png')
            source = S.obs_source_create("image_source", self.roster_image_list[i][0], settings, None)
            S.obs_scene_add(self.scene, source)
            self.images_added = True
            if i < 9:
                S.obs_sceneitem_group_add_item(home_group,
                                               S.obs_scene_find_source(self.scene, self.roster_image_list[i][0]))
            else:
                S.obs_sceneitem_group_add_item(away_group,
                                               S.obs_scene_find_source(self.scene, self.roster_image_list[i][0]))

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

    def dir_scan(self):
        hud_file_path = self.HUD_path
        if not os.path.isfile(hud_file_path):
            return ""

        with open(hud_file_path) as f:
            hud_data = json.load(f)

        # Return if the event hasn't changed
        if (self.current_event_num == hud_data['Event Num']):
            if (self.new_event != 1):
                return self.current_event_num

        self.new_event = 1

        print("New HUD:", self.current_event_num, hud_data['Event Num'])
        self.current_event_num = hud_data['Event Num']

        self.home_player = hud_data["Home Player"]
        self.away_player = hud_data["Away Player"]

        # Bookkeepping vars

        # Dicts to hold data for characters and teams(player)
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
        """
        print(S.obs_data_get_string(globalsettings, "_roster_layout"), "roster_layout")
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "horizontal":
            getimage.set_position_horizontal()
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "vertical":
            getimage.set_position_vertical()
        if S.obs_data_get_string(globalsettings, "_roster_layout") == "2x4":
            getimage.set_position_2x4()
            """
    def pre_postion_update(self):
        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        if S.obs_get_source_by_name("Team1Roster8") is not None:
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"),
                                    self.home_roster_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"),
                                    self.away_roster_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "home_player_text"),
                                    self.home_player_loc)
            S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "away_player_text"),
                                    self.away_player_loc)
            for item in self.roster_image_list:
                S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, item[0]), item[3])
        else:
            self.home_roster_loc = S.vec2()
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
            self.away_roster_loc = S.vec2()
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)

    def set_position_horizontal(self):
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
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"),
                                self.home_roster_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"),
                                self.away_roster_loc)

    def set_position_vertical(self):
        self.pre_postion_update()

        print(self.scene)
        for i in range(0, len(self.roster_image_list)):
            scale = S.vec2()
            scale.x = 1
            scale.y = 1
            S.obs_sceneitem_set_scale(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), scale)
            S.vec2_zero(self.roster_image_list[i][3])
            self.roster_image_list[i][3].y = i * self.image_width
            if i > 8:
                self.roster_image_list[i][3].y = (i-9) * self.image_width
            print(self.roster_image_list[i][3].y)
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]), self.roster_image_list[i][3])
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)

    def set_position_2x4(self):
        self.pre_postion_update()

        print("set_position_2x4")
        counter = 0
        for i in range(0,len(self.roster_image_list)):
            S.vec2_zero(self.roster_image_list[i][3])
            if self.roster_image_list[i][1] == 1:
                scale = S.vec2()
                scale.x = 1.6
                scale.y = 1.6
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
                    self.roster_image_list[i][3].x = counter%4 * self.image_width + 1.6 *self.image_width
                    counter +=1
                else:
                    self.roster_image_list[i][3].x = counter%4 * self.image_width + 1.6 *self.image_width
                    self.roster_image_list[i][3].y = self.image_width
                    counter += 1
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, self.roster_image_list[i][0]),
                                    self.roster_image_list[i][3])

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)

        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Home Roster"), self.home_roster_loc)

        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "Away Roster"), self.away_roster_loc)

def script_load(settings):

    S.timer_add(check_for_updates, 1000)

    global getimage
    getimage = rosterimages()

    getimage.new_event = 1
    getimage.dir_scan()
    #getimage.update_images()

    print(getimage.scene)

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, "_path")

def check_for_updates():
   if pause_bool == False:
       getimage.dir_scan()
       print(getimage.home_roster_loc.x, "X Home")
       getimage.update_images()
       print(getimage.roster_image_list)


def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    getimage.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global globalsettings
    globalsettings = settings

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, "_pause")

def script_description():
    return "Mario Baseball team roster images\nOBS interface by MattGree \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nDonations are welcomed!"

def add_pressed(props, prop):
    getimage.add_captains()
    getimage.new_event = 1
    getimage.dir_scan()
    getimage.update_images()
    #getimage.new_event = 1
    #getimage.dir_scan()
    #getimage.update_images()
    #IDK why this has to be done twice
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

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "refreshbutton", "Refresh HUD", refresh_pressed)
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

    S.obs_properties_add_button(props, "_flipteams", "Flip Team Locations", flip_teams)

    S.obs_property_set_modified_callback(OS_list, OS_callback)
    S.obs_property_set_modified_callback(roster_layout, layout_callback)

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
