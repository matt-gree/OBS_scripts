import obspython as S
import os
import json
import platform as plt

#def script_defaults(settings):

images_directory = str(os.path.dirname(__file__)) + "/Images/"

class pitcherstats:
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
        self.new_event = 0
        self.images_added = False

        self.batters_faced = str()
        self.runs_allowed = str()
        self.earned_runs = str()
        self.walks = str()
        self.hbp = str()
        self.hits = str()
        self.hrs = str()
        self.pitches_thrown = str()
        self.stamina = str()
        self.strikeouts = str()
        self.outs = str()
        self.pitcher = str()

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
            """self.HUD_path = "/" + current_path.split("/", 3)[1] + "/" + current_path.split("/", 3)[
                2] + "/" + "Library/Application Support/ProjectRio/HudFiles/decoded.hud.json" """
        elif str(plt.platform()).lower()[0] == 'w':
            self.platform = 'Windows'
            current_path = str(os.path.realpath(__file__))
            """self.HUD_path = current_path.split("\\")[0] + "/" + current_path.split("\\")[1] + "/" + current_path.split("\\")[
                2] + "/Documents/Project Rio/HudFiles/decoded.hud.json" """
        else:
            self.platform = 'Unknown'


    def add_pitching_stats(self):
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Pitcher_Stats_Text = S.obs_source_create("text_ft2_source", 'pitcher_stats_text', settings, None)
        else:
            Pitcher_Stats_Text = S.obs_source_create("text_gdiplus", 'pitcher_stats_text', settings, None)
        S.obs_scene_add(self.scene, Pitcher_Stats_Text)

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

        self.new_event = 1

        self.current_event_num = hud_data['Event Num']

        self.home_player = hud_data["Home Player"]
        self.away_player = hud_data["Away Player"]

        # Bookkeepping vars
        if "Previous Event" in hud_data.keys():
            if "Pitch" in hud_data["Previous Event"].keys():
                team = hud_data["Previous Event"]["Pitch"]["Pitcher Team Id"]
                self.pitcher = hud_data["Previous Event"]["Pitch"]["Pitcher Char Id"]
                for roster in range(0, 9):
                    team_roster_str = "Team " + str(team) + " Roster " + str(roster)
                    if hud_data[team_roster_str]["CharID"] == self.pitcher:
                        pitcher_id = roster

        team_roster_str = "Team " + str(team) + " Roster " + str(pitcher_id)

        # Vars to hold data for characters and teams(player)
        self.batters_faced = hud_data[team_roster_str]["Defensive Stats"]["Batters Faced"]
        self.runs_allowed = hud_data[team_roster_str]["Defensive Stats"]["Runs Allowed"]
        self.earned_runs = hud_data[team_roster_str]["Defensive Stats"]["Earned Runs"]
        self.walks = hud_data[team_roster_str]["Defensive Stats"]["Batters Walked"]
        self.hbp = hud_data[team_roster_str]["Defensive Stats"]["Batters Hit"]
        self.hits = hud_data[team_roster_str]["Defensive Stats"]["Hits Allowed"]
        self.hrs = hud_data[team_roster_str]["Defensive Stats"]["HRs Allowed"]
        self.pitches_thrown = hud_data[team_roster_str]["Defensive Stats"]["Pitches Thrown"]
        self.stamina = hud_data[team_roster_str]["Defensive Stats"]["Stamina"]
        self.strikeouts = hud_data[team_roster_str]["Defensive Stats"]["Strikeouts"]
        self.outs = hud_data[team_roster_str]["Defensive Stats"]["Outs Pitched"]

    def custom_stats(self):
        custom_stats_list = []
        stats_string = ""
        custom_stats_list.append("Pitcher: " + self.pitcher)
        if S.obs_data_get_bool(globalsettings, "_batters_faced") == True:
            custom_stats_list.append("Batters Faced: " + str(self.batters_faced))
        if S.obs_data_get_bool(globalsettings, "_runs_allowed") == True:
            custom_stats_list.append("Runs Allowed: " + str(self.runs_allowed))
        if S.obs_data_get_bool(globalsettings, "_earned_runs") == True:
            custom_stats_list.append("Earned Runs: " + str(self.runs_allowed))
        if S.obs_data_get_bool(globalsettings, "_batters_walked") == True:
            custom_stats_list.append("Walks: " + str(self.walks))
        if S.obs_data_get_bool(globalsettings, "_batters_hit") == True:
            custom_stats_list.append("HBP: " + str(self.hbp))
        if S.obs_data_get_bool(globalsettings, "_hits_allowed") == True:
            custom_stats_list.append("Hits Allowed: " + str(self.hits))
        if S.obs_data_get_bool(globalsettings, "_hrs_allowed") == True:
            custom_stats_list.append("HRs Allowed: " + str(self.hrs))
        if S.obs_data_get_bool(globalsettings, "_pitches_thrown") == True:
            custom_stats_list.append("Pitch Count: " + str(self.pitches_thrown))
        if S.obs_data_get_bool(globalsettings, "_stamina") == True:
            custom_stats_list.append("Stamina: " + str(self.stamina))
        if S.obs_data_get_bool(globalsettings, "_strikeouts") == True:
            custom_stats_list.append("Strikeouts: " + str(self.strikeouts))
        if S.obs_data_get_bool(globalsettings, "_outs_pitcher") == True:
            custom_stats_list.append("Outs Pitched: " + str(self.outs))

        for line in custom_stats_list:
            stats_string += line + "\n"

        source = S.obs_get_source_by_name("pitcher_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", stats_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

def script_load(settings):

    S.timer_add(check_for_updates, 1000)

    global globalsettings
    globalsettings = settings

    global getstats
    getstats = pitcherstats()

    getstats.new_event = 1
    getstats.dir_scan()

    print(getstats.scene)

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, "_path")

def check_for_updates():
   if pause_bool == False:
       getstats.dir_scan()
       getstats.custom_stats()


def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    getstats.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global globalsettings
    globalsettings = settings

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, "_pause")

def script_description():
    return "Mario Baseball team roster images\nOBS interface by MattGree \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nDonations are welcomed!"

def add_pressed(props, prop):
    getstats.add_pitching_stats()
    getstats.dir_scan()
    getstats.custom_stats()

#def refresh_pressed(props, prop):
#    getimage.new_event = 1
#    getimage.dir_scan()
#    getimage.update_images()

def remove_pressed(props, prop):
    S.obs_source_remove(S.obs_get_source_by_name("Home Roster"))
    S.obs_source_remove(S.obs_get_source_by_name("Away Roster"))
    S.obs_source_remove(S.obs_get_source_by_name("Away Roster"))
    S.obs_source_remove(S.obs_get_source_by_name("away_player_text"))
    S.obs_source_remove(S.obs_get_source_by_name("home_player_text"))


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_bool(props, "_pause", "Pause")
    S.obs_properties_add_bool(props, "_batters_faced", "Batters Faced")
    S.obs_properties_add_bool(props, "_runs_allowed", "Runs Allowed")
    S.obs_properties_add_bool(props, "_earned_runs", "Earned Runs")
    S.obs_properties_add_bool(props, "_batters_walked", "Batters Walked")
    S.obs_properties_add_bool(props, "_batters_hit", "Batters Hit")
    S.obs_properties_add_bool(props, "_hits_allowed", "Hits Allowed")
    S.obs_properties_add_bool(props, "_hrs_allowed", "HRs Allowed")
    S.obs_properties_add_bool(props, "_pitches_thrown", "Batters Faced")
    S.obs_properties_add_bool(props, "_stamina", "Stamina")
    S.obs_properties_add_bool(props, "_strikeouts", "Strikeouts")
    S.obs_properties_add_bool(props, "_outs_pitcher", "Outs Pitched")
    S.obs_properties_add_button(props, "_add_button", "Add", add_pressed)
    S.obs_properties_add_button(props, "_removebutton", "Remove", remove_pressed)
    OS_list = S.obs_properties_add_list(props, "_OS_list", "OS:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, "Custom", "custom")
    S.obs_property_list_add_string(OS_list, "Windows", "windows")
    S.obs_property_list_add_string(OS_list, "MacOS", "macOS")
    S.obs_properties_add_text(props, "_path", "Path to HUD json:", S.OBS_TEXT_DEFAULT)

    S.obs_property_set_modified_callback(OS_list, OS_callback)

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

