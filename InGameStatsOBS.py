import obspython as S
import os
import json
import platform as plt
from urllib.parse import urlencode
from urllib.request import urlopen, Request
import time
import re

#def script_defaults(settings):

images_directory = str(os.path.dirname(__file__)) + "/Images/"

class pitcherstats:
    def __init__(self):

        self.location = S.vec2()

        self.pitching_stats_loc = S.vec2()
        self.batting_stats_loc = S.vec2()
        self.web_pitching_stats_loc = S.vec2()
        self.web_batting_stats_loc = S.vec2()

        self.away_team_roster = []
        self.home_team_roster = []

        self.away_team_captain = str()
        self.home_team_captain = str()

        self.current_event_num = -1

        self.half_inning_old = 0
        self.half_inning_cur = 0

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

        self.calledWebInd = False
        self.web_home_statsFound = False
        self.web_away_statsFound = False
        self.web_batter_statsFound = False
        self.web_pitcher_statsFound = False

        self.mode_names = []
        self.got_modes = False

        self.debugMode = False

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
        if self.debugMode:
            print("flip_teams")

        #flip hud stats
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "batter_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_stats_text"), self.batting_stats_loc)

        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "batter_stats_text"), self.batting_stats_loc)

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "batter_stats_text"), self.batting_stats_loc)

        #flip web stats
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "web_batter_stats_text"), self.web_pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "web_pitcher_stats_text"), self.web_batting_stats_loc)

        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "web_pitcher_stats_text"), self.web_pitching_stats_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "web_batter_stats_text"), self.web_batting_stats_loc)

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "web_pitcher_stats_text"), self.web_pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "web_batter_stats_text"), self.web_batting_stats_loc)

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

    def add_web_stats(self):
        if self.debugMode:
            print("add web stats start")

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        #check if the sources already exist.
        old_b_source = S.obs_scene_find_source(self.scene,'web_batter_stats_text')
        old_p_source = S.obs_scene_find_source(self.scene,'web_pitcher_stats_text')

        #Add batting text box
        if old_b_source is None: #only create if it doesn't already exist
            print("creating b")
            settings = S.obs_data_create()
            if self.platform == 'MacOS':
                Web_Batter_Stats_Text = S.obs_source_create("text_ft2_source", 'web_batter_stats_text', settings, None)
            else:
                Web_Batter_Stats_Text = S.obs_source_create("text_gdiplus", 'web_batter_stats_text', settings, None)
            S.obs_scene_add(self.scene, Web_Batter_Stats_Text)
            S.obs_source_release(Web_Batter_Stats_Text)
            S.obs_data_release(settings)

        #Add pitching text box
        if old_p_source is None: #only create if it doesn't already exist
            print("creating p")
            settings = S.obs_data_create()
            if self.platform == 'MacOS':
                Web_Pitcher_Stats_Text = S.obs_source_create("text_ft2_source", 'web_pitcher_stats_text', settings, None)
            else:
                Web_Pitcher_Stats_Text = S.obs_source_create("text_gdiplus", 'web_pitcher_stats_text', settings, None)
            S.obs_scene_add(self.scene, Web_Pitcher_Stats_Text)
            S.obs_source_release(Web_Pitcher_Stats_Text)
            S.obs_data_release(settings)
    
    
    def get_active_modes(self):
        if self.debugMode:
            print("Get modes")
        
        #parameters for the post request
        modes_json = {
            "Active": "true",
            "Client": "true"
        }
        modes_url = "https://api.projectrio.app/tag_set/list"

        #post request converted into a json file
        modes_req = Request(modes_url, urlencode(modes_json).encode())
        modes_string = urlopen(modes_req).read().decode('utf-8')
        modes = json.loads(modes_string)

        #compile mode names received from the API
        for comm in modes["Tag Sets"]:
            if comm["comm_type"] == 'Official' and comm["end_date"] > time.time():
                self.mode_names.append(comm['name'])

    def rioWeb_stats(self):
        if self.debugMode:
            print("web stats")
        #assign batter and pitcher stat variables
        #home
        self.web_batter_statsFound = False
        self.web_pitcher_statsFound = False
        if self.web_home_statsFound:
            if self.half_inning_cur == 0:
                if self.p_pitcher in self.web_data_home["Stats"]:
                    web_data_pitcher = self.web_data_home["Stats"][self.p_pitcher]["Pitching"]
                    self.web_pitcher_statsFound = True
            else:
                if self.b_batter in self.web_data_home["Stats"]:
                    web_data_batter = self.web_data_home["Stats"][self.b_batter]["Batting"]
                    self.web_batter_statsFound = True

        #away
        if self.web_away_statsFound:
            if self.half_inning_cur == 0:
                if self.b_batter in self.web_data_away["Stats"]:
                    web_data_batter = self.web_data_away["Stats"][self.b_batter]["Batting"]
                    self.web_batter_statsFound = True
            else:
                if self.p_pitcher in self.web_data_away["Stats"]:
                    web_data_pitcher = self.web_data_away["Stats"][self.p_pitcher]["Pitching"]
                    self.web_pitcher_statsFound = True

        if self.debugMode:
            print("batter found", self.web_batter_statsFound)
            print("pitcher found", self.web_pitcher_statsFound)

        b_web_stats_string = "Batter: " + self.b_batter
        if self.web_batter_statsFound:
            b_web_avg = web_data_batter["summary_hits"]/web_data_batter["summary_at_bats"]
            b_web_hits = web_data_batter["summary_hits"]
            b_web_hr = web_data_batter["summary_homeruns"]
            b_web_rbi = web_data_batter["summary_rbi"]
            b_web_k = web_data_batter["summary_strikeouts"]
            b_web_bb = web_data_batter["summary_walks_bb"]
            b_web_hbp = web_data_batter["summary_walks_hbp"]

            b_web_stats_string += "\nAvg: " + str('{0:.3f}'.format(float(b_web_avg))) + " H: " + str(b_web_hits) + " HR: " + str(b_web_hr) + " RBI: " +  str(b_web_rbi) + " K: " + str(b_web_k)


        source = S.obs_get_source_by_name("web_batter_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", b_web_stats_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        p_web_stats_string = "Pitcher: " + self.p_pitcher
        if self.web_pitcher_statsFound:    
            p_web_ER = web_data_pitcher["runs_allowed"]
            p_web_ERA = 0 if web_data_pitcher["batters_faced"] == 0 else web_data_pitcher["runs_allowed"]/(web_data_pitcher["outs_pitched"]*9/3)
            p_web_k = web_data_pitcher["strikeouts_pitched"]
            p_web_oppAvg = 0 if web_data_pitcher["batters_faced"] == 0 else web_data_pitcher["hits_allowed"]/web_data_pitcher["batters_faced"]

            p_web_stats_string += "\nERA: " + str('{0:.1f}'.format(float(p_web_ERA))) + " K: " + str(p_web_k) + " Opp Avg.: " + str('{0:.3f}'.format(float(p_web_oppAvg)))
        
        source = S.obs_get_source_by_name("web_pitcher_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", p_web_stats_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        if self.debugMode:
            print(b_web_stats_string)
            print(p_web_stats_string)
        

    def dir_scan(self):
        if self.debugMode:
            print("hud stats")

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
        self.p_pitcher = hud_data[p_team_roster_str]["CharID"]
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


        self.half_inning_cur = hud_data["Half Inning"]

        self.b_team_index = self.half_inning_cur

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
    if getstats.calledWebInd:
        getstats.rioWeb_stats()

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, "_path")

def check_for_updates():
   if pause_bool == False:
        getstats.dir_scan()
        if getstats.calledWebInd:
            getstats.rioWeb_stats()
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

def get_web_stats(props, prop):
    if getstats.debugMode:
        print("get web stats")

    url_base = "https://api.projectrio.app/stats/?"
    
    #check if the stats should be filtered by game mode
    web_stat_mode = S.obs_data_get_string(globalsettings, "_web_mode_list")
    if web_stat_mode == "all":
        mode_url_addition = ""
    else:
        mode_url_addition = "&tag=" + web_stat_mode

    url_home = url_base + "&by_char=1&username=" + getstats.home_player + mode_url_addition
    url_away = url_base + "&by_char=1&username=" + getstats.away_player + mode_url_addition
    
    if getstats.debugMode:
        print(url_home)
        print(url_away)

    #check if stats were found for each player.
    getstats.web_home_statsFound = False
    getstats.web_away_statsFound = False
    try:
        getstats.web_data_home = json.loads(urlopen(url_home).read())
        getstats.web_home_statsFound = True   
    except:
        getstats.web_home_statsFound = False
    
    try:
        getstats.web_data_away = json.loads(urlopen(url_away).read())
        getstats.web_away_statsFound = True    
    except:
        getstats.web_away_statsFound = False
    getstats.calledWebInd = True
    
    print("Home stats found:", getstats.web_home_statsFound)
    print("Away stats found:", getstats.web_away_statsFound)

    getstats.add_web_stats()
    
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

    #add dropdown for modes to filter web stats
    web_mode_list = S.obs_properties_add_list(props, "_web_mode_list", "Mode for Web Stats:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    
    #if the list of modes was already fetched, don't do it again.
    #if getstats.got_modes == False:
        #getstats.get_active_modes()
        #getstats.got_modes = True

    #add modes to the dropdown
    S.obs_property_list_add_string(web_mode_list, "All", "all")

    #for i in range(len(getstats.mode_names)):
        #S.obs_property_list_add_string(web_mode_list, getstats.mode_names[i], re.sub(r'[^a-zA-Z0-9]', '', getstats.mode_names[i]))

    S.obs_properties_add_button(props, "_getWebStats", "Get Web Stats", get_web_stats)

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