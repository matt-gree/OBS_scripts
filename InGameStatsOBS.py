import obspython as S
import os
import json
import platform as plt

#def script_defaults(settings):

images_directory = str(os.path.dirname(__file__)) + "/Images/"

class pitcherstats:
    def __init__(self):

        self.location = S.vec2()

        self.pitching_stats_loc = S.vec2()
        self.batting_stats_loc = S.vec2()

        self.away_team_roster = []
        self.home_team_roster = []

        self.away_team_captain = str()
        self.home_team_captain = str()

        self.current_event_num = -1

        self.half_inning_old = 0

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        self.new_event = 0
        self.images_added = False

        self.p_batters_faced = str()
        self.p_runs_allowed = str()
        self.p_earned_runs = str()
        self.p_walks = str()
        self.p_hbp = str()
        self.p_hits = str()
        self.p_hrs = str()
        self.p_pitches_thrown = str()
        self.p_stamina = str()
        self.p_strikeouts = str()
        self.p_outs = str()
        self.p_pitcher = str()


        self.b_team_index = str()
        self.b_roster_loc = str()
        self.b_at_bats = str()
        self.b_hits = str()
        self.b_singles = str()
        self.b_doubles = str()
        self.b_triples = str()
        self.b_homeruns = str()
        self.b_successful_bunts = str()
        self.b_sac_flys = str()
        self.b_strikeouts = str()
        self.b_walks = str()
        self.b_HBP = str()
        self.b_RBI = str()
        self.b_steals = str()
        self.b_star_hits = str()

        self.image_width = 60

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

    def flip_teams(self):
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "batter_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_stats_text"), self.batting_stats_loc)

        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "batter_stats_text"), self.batting_stats_loc)

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "batter_stats_text"), self.batting_stats_loc)

    def add_pitching_stats(self):
        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Pitcher_Stats_Text = S.obs_source_create("text_ft2_source", 'pitcher_stats_text', settings, None)
        else:
            Pitcher_Stats_Text = S.obs_source_create("text_gdiplus", 'pitcher_stats_text', settings, None)
        S.obs_scene_add(self.scene, Pitcher_Stats_Text)
        S.obs_source_release(Pitcher_Stats_Text)
        S.obs_data_release(settings)

        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Batter_Stats_Text = S.obs_source_create("text_ft2_source", 'batter_stats_text', settings, None)
        else:
            Batter_Stats_Text = S.obs_source_create("text_gdiplus", 'batter_stats_text', settings, None)
        S.obs_scene_add(self.scene, Batter_Stats_Text)
        S.obs_source_release(Batter_Stats_Text)
        S.obs_data_release(settings)

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
                teamInt = hud_data["Previous Event"]["Pitch"]["Pitcher Team Id"]
                teamStr = "Away" if teamInt == 0 else "Home"
                self.p_pitcher = hud_data["Previous Event"]["Pitch"]["Pitcher Char Id"]
                for roster in range(0, 9):
                    team_roster_str = teamStr + " Roster " + str(roster)
                    if hud_data[team_roster_str]["CharID"] == self.p_pitcher:
                        pitcher_id = roster
            else:
                return self.current_event_num
        else:
            team = 1
            self.p_pitcher = "First Event"
            pitcher_id = 0

        p_team_roster_str = teamStr + " Roster " + str(pitcher_id)

        # Vars to hold data for characters and teams(player)
        self.p_batters_faced = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Faced"]
        self.p_runs_allowed = hud_data[p_team_roster_str]["Defensive Stats"]["Runs Allowed"]
        self.p_earned_runs = hud_data[p_team_roster_str]["Defensive Stats"]["Earned Runs"]
        self.p_walks = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Walked"]
        self.p_hbp = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Hit"]
        self.p_hits = hud_data[p_team_roster_str]["Defensive Stats"]["Hits Allowed"]
        self.p_hrs = hud_data[p_team_roster_str]["Defensive Stats"]["HRs Allowed"]
        self.p_pitches_thrown = hud_data[p_team_roster_str]["Defensive Stats"]["Pitches Thrown"]
        self.p_stamina = hud_data[p_team_roster_str]["Defensive Stats"]["Stamina"]
        self.p_strikeouts = hud_data[p_team_roster_str]["Defensive Stats"]["Strikeouts"]
        self.p_outs = hud_data[p_team_roster_str]["Defensive Stats"]["Outs Pitched"]

        self.b_team_index = hud_data["Half Inning"]
        b_teamStr = "Away" if self.b_team_index == 0 else "Home"
        self.b_roster_loc = hud_data["Batter Roster Loc"]

        b_team_roster_str = b_teamStr + " Roster " + str(self.b_roster_loc)
        self.b_batter = hud_data[b_team_roster_str]["CharID"]
        self.b_at_bats = hud_data[b_team_roster_str]["Offensive Stats"]["At Bats"]
        self.b_hits = hud_data[b_team_roster_str]["Offensive Stats"]["Hits"]
        self.b_singles = hud_data[b_team_roster_str]["Offensive Stats"]["Singles"]
        self.b_doubles = hud_data[b_team_roster_str]["Offensive Stats"]["Doubles"]
        self.b_triples = hud_data[b_team_roster_str]["Offensive Stats"]["Triples"]
        self.b_homeruns = hud_data[b_team_roster_str]["Offensive Stats"]["Homeruns"]
        self.b_successful_bunts = hud_data[b_team_roster_str]["Offensive Stats"]["Successful Bunts"]
        self.b_sac_flys = hud_data[b_team_roster_str]["Offensive Stats"]["Sac Flys"]
        self.b_strikeouts = hud_data[b_team_roster_str]["Offensive Stats"]["Strikeouts"]
        self.b_walks = hud_data[b_team_roster_str]["Offensive Stats"]["Walks (4 Balls)"]
        self.b_HBP = hud_data[b_team_roster_str]["Offensive Stats"]["Walks (Hit)"]
        self.b_RBI = hud_data[b_team_roster_str]["Offensive Stats"]["RBI"]
        self.b_steals = hud_data[b_team_roster_str]["Offensive Stats"]["Bases Stolen"]
        self.b_star_hits = hud_data[b_team_roster_str]["Offensive Stats"]["Star Hits"]

        if str(self.half_inning_old) != str(hud_data["Half Inning"]):
            self.flip_teams()
            self.half_inning_old = str(hud_data["Half Inning"])

    def custom_stats(self):
        p_custom_stats_list = []
        if self.p_pitcher != "First Event":
            p_custom_stats_list.append("Pitcher: " + str(self.p_pitcher))
        p_stats_string = ""
        p_stats_list = S.obs_data_get_string(globalsettings, "_pitching_stats").split(";")
        for item in p_stats_list:
            if item == "Batters Faced" or item == "1" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Batters Faced: " + str(self.p_batters_faced))
            if item == "Runs Allowed" or item == "2" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Runs Allowed: " + str(self.p_runs_allowed))
            if item == "Earned Runs" or item == "3" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Earned Runs: " + str(self.p_runs_allowed))
            if item == "Walks" or item == "4" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Walks: " + str(self.p_walks))
            if item == "HBP" or item == "5" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("HBP: " + str(self.p_hbp))
            if item == "Hits Allowed" or item == "6" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Hits Allowed: " + str(self.p_hits))
            if item == "HRs Allowed" or item == "7" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("HRs Allowed: " + str(self.p_hrs))
            if item == "Pitch Count" or item == "8" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Pitch Count: " + str(self.p_pitches_thrown))
            if item == "Stamina" or item == "9" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Stamina: " + str(self.p_stamina))
            if item == "Strikeouts" or item == "10" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Strikeouts: " + str(self.p_strikeouts))
            if item == "Outs Pitched" or item == "11" and self.p_pitcher != "First Event":
                p_custom_stats_list.append("Outs Pitched: " + str(self.p_outs))

        for line in p_custom_stats_list:
            p_stats_string += line + "\n"

        source = S.obs_get_source_by_name("pitcher_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", p_stats_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        b_custom_stats_list = []
        b_custom_stats_list.append("Batter: " + str(self.b_batter))
        b_stats_string = ""
        p_stats_list = S.obs_data_get_string(globalsettings, "_batting_stats").split(";")
        for item in p_stats_list:
            if item == "At Bats" or item == "1":
                b_custom_stats_list.append("At Bats: " + str(self.b_at_bats))
            if item == "Hits" or item == "2":
                b_custom_stats_list.append("Hits: " + str(self.b_hits))
            if item == "Singles" or item == "3":
                b_custom_stats_list.append("Singles: " + str(self.b_singles))
            if item == "Doubles" or item == "4":
                b_custom_stats_list.append("Doubles: " + str(self.b_doubles))
            if item == "Triples" or item == "5":
                b_custom_stats_list.append("Triples: " + str(self.b_triples))
            if item == "Home Runs" or item == "6":
                b_custom_stats_list.append("Home Runs: " + str(self.b_homeruns))
            if item == "Sucessful Bunts" or item == "7":
                b_custom_stats_list.append("Sucessful Bunts: " + str(self.b_successful_bunts))
            if item == "Sac Flys" or item == "8":
                b_custom_stats_list.append("Sac Flys: " + str(self.b_sac_flys))
            if item == "Strikeouts" or item == "9":
                b_custom_stats_list.append("Strikeouts: " + str(self.b_walks))
            if item == "Walks" or item == "10":
                b_custom_stats_list.append("Walks: " + str(self.b_walks))
            if item == "HBP" or item == "11":
                b_custom_stats_list.append("HBP: " + str(self.b_HBP))
            if item == "RBI" or item == "12":
                b_custom_stats_list.append("RBI: " + str(self.b_RBI))
            if item == "Steals" or item == "13":
                b_custom_stats_list.append("Steals: " + str(self.b_steals))
            if item == "Star Hits" or item == "14":
                b_custom_stats_list.append("Star Hits: " + str(self.b_star_hits))


        for line in b_custom_stats_list:
            b_stats_string += line + "\n"

        source = S.obs_get_source_by_name("batter_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", b_stats_string)
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
    return "Mario Baseball Pitcher Stats\n" \
           "OBS interface by MattGree \n" \
           "Thanks to the Rio Devs for developing the HUD files  \n" \
           "Donations are welcomed! \n" \
           "Pitching Stats Options: \n" \
           "1. Batters Faced;   " \
           "2. Runs Allowed;    " \
           "3. Earned Runs; \n" \
           "4. Walks;   " \
           "5. HBP;   " \
           "6. Hits Allowed;   " \
           "7. HRs Allowed; \n" \
           "8. Pitch Count;   " \
           "9. Stamina;   " \
           "10. Strikeouts;   " \
           "11. Outs Pitched   \n" \
           "Batting Stats Options: \n" \
           "1. At Bats;   " \
           "2. Hits;    " \
           "3. Singles;   " \
           "4. Doubles;   " \
           "5. Triples;   " \
           "6. Home Runs;   \n" \
           "7. Sucessful Bunts;   " \
           "8. Sac Flys;   " \
           "9. Strikeouts;   " \
           "10. Walks;   " \
           "11. HBP;   \n" \
           "12. RBI;   " \
           "13. Steals;   " \
           "14. Star Hits;   \n" \
           "Enter the numbers of stats you wish displayed, seperated by a ;" \


def add_pressed(props, prop):
    getstats.add_pitching_stats()
    getstats.dir_scan()
    getstats.custom_stats()

def remove_pressed(props, prop):
    pitcher_stats = S.obs_get_source_by_name("pitcher_stats_text")
    S.obs_source_remove(pitcher_stats)
    S.obs_source_release(pitcher_stats)

    batter_stats = S.obs_get_source_by_name("batter_stats_text")
    S.obs_source_remove(batter_stats)
    S.obs_source_release(batter_stats)

def flip_teams(props, prop):
    getstats.flip_teams()

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_bool(props, "_pause", "Pause")
    S.obs_properties_add_text(props, "_pitching_stats", "Pitching Stats", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(props, "_batting_stats", "Batting Stats", S.OBS_TEXT_DEFAULT)

    S.obs_properties_add_button(props, "_add_button", "Add", add_pressed)
    S.obs_properties_add_button(props, "_removebutton", "Remove", remove_pressed)

    OS_list = S.obs_properties_add_list(props, "_OS_list", "OS:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, "Custom", "custom")
    S.obs_property_list_add_string(OS_list, "Windows", "windows")
    S.obs_property_list_add_string(OS_list, "MacOS", "macOS")
    S.obs_properties_add_text(props, "_path", "Path to HUD json:", S.OBS_TEXT_DEFAULT)

    S.obs_properties_add_button(props, "_flipteams", "Flip Team Locations", flip_teams)

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