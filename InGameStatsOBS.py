import obspython as S
import os
import json
import platform as plt
from urllib.parse import urlencode
from urllib.request import urlopen, Request
import time
import re

# If you run this on a mac and get an SSL error, run the following code in Termianl:
# /Applications/Python\ 3.10/Install\ Certificates.command

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

        #web stats
        self.p_w_batters_faced = 0
        self.p_w_runs_allowed = 0
        self.p_w_walks = 0
        self.p_w_hbp = 0
        self.p_w_hits = 0
        self.p_w_pitches_thrown = 0
        self.p_w_strikeouts = 0
        self.p_w_outs = 0

        self.b_w_at_bats = 0
        self.b_w_hits = 0
        self.b_w_singles = 0
        self.b_w_doubles = 0
        self.b_w_triples = 0
        self.b_w_homeruns = 0
        self.b_w_sac_flys = 0
        self.b_w_strikeouts = 0
        self.b_w_walks = 0
        self.b_w_HBP = 0
        self.b_w_RBI = 0

        #hud stats
        self.p_h_batters_faced = 0
        self.p_h_runs_allowed = 0
        self.p_h_earned_runs = 0
        self.p_h_walks = 0
        self.p_h_hbp = 0
        self.p_h_hits = 0
        self.p_h_hrs = 0
        self.p_h_pitches_thrown = 0
        self.p_h_stamina = 0
        self.p_h_strikeouts = 0
        self.p_h_outs = 0
        self.p_h_pitcher = str()

        self.b_h_batter = str()
        self.b_h_team_index = 0
        self.b_h_roster_loc = 0
        self.b_h_at_bats = 0
        self.b_h_hits = 0
        self.b_h_singles = 0
        self.b_h_doubles = 0
        self.b_h_triples = 0
        self.b_h_homeruns = 0
        self.b_h_successful_bunts = 0
        self.b_h_sac_flys = 0
        self.b_h_strikeouts = 0
        self.b_h_walks = 0
        self.b_h_HBP = 0
        self.b_h_RBI = 0
        self.b_h_steals = 0
        self.b_h_star_hits = 0
        self.BATTER_HUD_STATS_LIST = []

        #summary stats

        self.b_hud_stats_string = str()
        self.b_t_stats_string = str()
        self.b_t_avg = 0 
        self.b_t_hits = 0
        self.b_t_hr = 0
        self.b_t_rbi = 0
        self.b_t_k = 0
        self.b_t_bb = 0
        self.b_t_hbp = 0

        self.p_hud_stats_string = str()
        self.p_t_stats_string = str()
        self.p_t_ER = 0
        self.p_t_ERA = 0
        self.p_t_k = 0
        self.p_t_oppAvg = 0

        self.b_combined_text_output = str()
        self.p_combined_text_output = str()


        self.image_width = 60

        self.home_player = str()
        self.away_player = str()

        self.calledWebInd = False
        self.web_home_statsFound = False
        self.web_away_statsFound = False
        self.web_batter_statsFound = False
        self.web_pitcher_statsFound = False

        self.mode_names = []
        self.got_modes = False

        self.debugMode = False

        self.game_start = False

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
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "batter_combined_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_combined_stats_text"), self.batting_stats_loc)

        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_combined_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "batter_combined_stats_text"), self.batting_stats_loc)

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "pitcher_combined_stats_text"), self.pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "batter_combined_stats_text"), self.batting_stats_loc)

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

    def add_summary_stats(self):
        if self.debugMode:
            print("adding summmary stats")

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        #check if the sources already exist.
        old_bSummary_source = S.obs_scene_find_source(self.scene,'batter_summary_stats_text')
        old_pSummary_source = S.obs_scene_find_source(self.scene,'pitcher_summary_stats_text')

        #Add batting text box
        if old_bSummary_source is None: #only create if it doesn't already exist
            settings = S.obs_data_create()
            if self.platform == 'MacOS':
                Batter_Summary_Stats_Text = S.obs_source_create("text_ft2_source", 'batter_summary_stats_text', settings, None)
            else:
                Batter_Summary_Stats_Text = S.obs_source_create("text_gdiplus", 'batter_summary_stats_text', settings, None)
            S.obs_scene_add(self.scene, Batter_Summary_Stats_Text)
            S.obs_source_release(Batter_Summary_Stats_Text)
            S.obs_data_release(settings)

        #Add pitching text box
        if old_pSummary_source is None: #only create if it doesn't already exist
            settings = S.obs_data_create()
            if self.platform == 'MacOS':
                Pitcher_Summary_Stats_Text = S.obs_source_create("text_ft2_source", 'pitcher_summary_stats_text', settings, None)
            else:
                Pitcher_Summary_Stats_Text = S.obs_source_create("text_gdiplus", 'pitcher_summary_stats_text', settings, None)
            S.obs_scene_add(self.scene, Pitcher_Summary_Stats_Text)
            S.obs_source_release(Pitcher_Summary_Stats_Text)
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

    
    def get_web_stats(self):
        if self.debugMode:
            print("get web stats")

        url_base = "https://api.projectrio.app/stats/?"
        
        #check if the stats should be filtered by game mode
        web_stat_mode = S.obs_data_get_string(globalsettings, "_web_mode_list")
        if web_stat_mode == "all":
            mode_url_addition = ""
        else:
            mode_url_addition = "&tag=" + web_stat_mode

        url_home = url_base + "&by_char=1&username=" + self.home_player + mode_url_addition
        url_away = url_base + "&by_char=1&username=" + self.away_player + mode_url_addition
        
        if self.debugMode:
            print(url_home)
            print(url_away)

        #check if stats were found for each player.
        self.web_home_statsFound = False
        self.web_away_statsFound = False
        try:
            self.web_data_home = json.loads(urlopen(url_home).read())
            self.web_home_statsFound = True   
        except:
            self.web_home_statsFound = False
        
        try:
            self.web_data_away = json.loads(urlopen(url_away).read())
            self.web_away_statsFound = True    
        except:
            self.web_away_statsFound = False
        self.calledWebInd = True
        
        print("Home stats found:", self.web_home_statsFound)
        print("Away stats found:", self.web_away_statsFound)

    def parse_web_stats(self):
        if self.debugMode:
            print("parse web stats")
        
        #assign batter and pitcher stat variables
        #home
        self.web_batter_statsFound = False
        self.web_pitcher_statsFound = False
        if self.web_home_statsFound:
            if self.half_inning_cur == 0:
                if self.p_h_pitcher in self.web_data_home["Stats"]:
                    web_data_pitcher = self.web_data_home["Stats"][self.p_h_pitcher]["Pitching"]
                    self.web_pitcher_statsFound = True
            else:
                if self.b_h_batter in self.web_data_home["Stats"]:
                    web_data_batter = self.web_data_home["Stats"][self.b_h_batter]["Batting"]
                    self.web_batter_statsFound = True

        #away
        if self.web_away_statsFound:
            if self.half_inning_cur == 0:
                if self.b_h_batter in self.web_data_away["Stats"]:
                    web_data_batter = self.web_data_away["Stats"][self.b_h_batter]["Batting"]
                    self.web_batter_statsFound = True
            else:
                if self.p_h_pitcher in self.web_data_away["Stats"]:
                    web_data_pitcher = self.web_data_away["Stats"][self.p_h_pitcher]["Pitching"]
                    self.web_pitcher_statsFound = True

        if self.debugMode:
            print("batter found", self.web_batter_statsFound)
            print("pitcher found", self.web_pitcher_statsFound)

        if self.web_batter_statsFound:
            self.b_w_at_bats = web_data_batter["summary_at_bats"]
            self.b_w_hits = web_data_batter["summary_hits"]
            self.b_w_singles = web_data_batter["summary_singles"]
            self.b_w_doubles = web_data_batter["summary_doubles"]
            self.b_w_triples = web_data_batter["summary_triples"]
            self.b_w_homeruns = web_data_batter["summary_homeruns"]
            self.b_w_sac_flys = web_data_batter["summary_sac_flys"]
            self.b_w_strikeouts = web_data_batter["summary_strikeouts"]
            self.b_w_walks = web_data_batter["summary_walks_bb"]
            self.b_w_HBP = web_data_batter["summary_walks_hbp"]
            self.b_w_RBI = web_data_batter["summary_rbi"]
        else:
            self.b_w_at_bats = 0
            self.b_w_hits = 0
            self.b_w_singles = 0
            self.b_w_doubles = 0
            self.b_w_triples = 0
            self.b_w_homeruns = 0
            self.b_w_sac_flys = 0
            self.b_w_strikeouts = 0
            self.b_w_walks = 0
            self.b_w_HBP = 0
            self.b_w_RBI = 0

        if self.web_pitcher_statsFound:
            self.p_w_batters_faced = web_data_pitcher["batters_faced"]
            self.p_w_runs_allowed = web_data_pitcher["runs_allowed"]
            self.p_w_walks = web_data_pitcher["walks_bb"]
            self.p_w_hbp = web_data_pitcher["walks_hbp"]
            self.p_w_hits = web_data_pitcher["hits_allowed"]
            self.p_w_pitches_thrown = web_data_pitcher["total_pitches"]
            self.p_w_strikeouts = web_data_pitcher["strikeouts_pitched"]
            self.p_w_outs = web_data_pitcher["outs_pitched"]
        else:
            self.p_w_batters_faced = 0
            self.p_w_runs_allowed = 0
            self.p_w_walks = 0
            self.p_w_hbp = 0
            self.p_w_hits = 0
            self.p_w_pitches_thrown = 0
            self.p_w_strikeouts = 0
            self.p_w_outs = 0

    def set_visible(self):
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, "batter_summary_stats_text"), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, "pitcher_summary_stats_text"), True)

    def summary_stats(self):
        if self.debugMode:
            print("summary stats")

        #update web stat variables
        getstats.parse_web_stats()

        self.b_t_stats_string = "Batter: " + self.b_h_batter
        self.b_t_avg = 0 if (self.b_w_at_bats + self.b_h_at_bats) == 0 else (self.b_w_hits + self.b_h_hits)/(self.b_w_at_bats + self.b_h_at_bats)
        self.b_t_hits = self.b_w_hits + self.b_h_hits
        self.b_t_hr = self.b_w_homeruns + self.b_h_homeruns
        self.b_t_rbi = self.b_w_RBI + self.b_h_RBI
        self.b_t_k = self.b_w_strikeouts + self.b_h_strikeouts
        self.b_t_bb = self.b_w_walks + self.b_h_walks
        self.b_t_hbp = self.b_w_HBP + self.b_h_HBP

        self.b_t_stats_string += "\nAvg: " + str('{0:.3f}'.format(float(self.b_t_avg))) + " H: " + str(self.b_t_hits) + " HR: " + str(self.b_t_hr) + " RBI: " +  str(self.b_t_rbi) + " SO: " + str(self.b_t_k)

        self.p_t_stats_string = "Pitcher: " + self.p_h_pitcher  
        self.p_t_ER = self.p_w_runs_allowed + self.p_h_earned_runs
        self.p_t_ERA = 0 if (self.p_w_outs + self.p_h_outs) == 0 else 9*((self.p_w_runs_allowed + self.p_h_earned_runs)/((self.p_w_outs + self.p_h_outs)/3))
        self.p_t_k = self.p_w_strikeouts + self.p_h_strikeouts
        self.p_t_oppAvg = 0 if (self.p_w_batters_faced + self.p_h_batters_faced) == 0 else (self.p_w_hits + self.p_h_hits)/(self.p_w_batters_faced + self.p_h_batters_faced)

        self.p_t_stats_string += "\nERA: " + str('{0:.1f}'.format(float(self.p_t_ERA))) + " K: " + str(self.p_t_k) + " Opp Avg.: " + str('{0:.3f}'.format(float(self.p_t_oppAvg)))

    def dir_scan(self):
        if self.debugMode:
            print("hud stats")

        hud_file_path = S.obs_data_get_string(globalsettings, "_path")
        if not os.path.isfile(hud_file_path):
            return ""

        with open(hud_file_path) as f:
            hud_data = json.load(f)

        # Return if the event hasn't changed
        if str(hud_data['Event Num'])[0] == '0':
            self.game_start = True

        if (self.current_event_num == hud_data['Event Num']):
            if (self.new_event != 1):
                return self.current_event_num

        self.new_event = 1

        self.current_event_num = hud_data['Event Num']

        self.home_player = hud_data["Home Player"]
        self.away_player = hud_data["Away Player"]

        global visible_bool

        print(f"game start bool {self.game_start}")

        if (visible_bool is True) and (self.current_event_num[0] != '0') and (self.game_start == True):
            S.timer_remove(check_for_updates)
            self.get_web_stats()
            self.set_visible()
            print("stats visible")
            self.game_start = False
            S.timer_add(check_for_updates, 1000)

        # Bookkeepping vars
        if "Previous Event" in hud_data.keys():
            if "Pitch" in hud_data["Previous Event"].keys():
                teamInt = hud_data["Previous Event"]["Pitch"]["Pitcher Team Id"]
                teamStr = "Away" if teamInt == 0 else "Home"
                self.p_h_pitcher = hud_data["Previous Event"]["Pitch"]["Pitcher Char Id"]
                for roster in range(0, 9):
                    team_roster_str = teamStr + " Roster " + str(roster)
                    if hud_data[team_roster_str]["CharID"] == self.p_h_pitcher:
                        pitcher_id = roster
            else:
                return self.current_event_num
        else:
            teamStr = "Home"
            self.p_h_pitcher = "First Event"
            pitcher_id = 0

        p_team_roster_str = teamStr + " Roster " + str(pitcher_id)

        # Vars to hold data for characters and teams(player)
        self.p_h_pitcher = hud_data[p_team_roster_str]["CharID"]
        self.p_h_batters_faced = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Faced"]
        self.p_h_runs_allowed = hud_data[p_team_roster_str]["Defensive Stats"]["Runs Allowed"]
        self.p_h_earned_runs = hud_data[p_team_roster_str]["Defensive Stats"]["Earned Runs"]
        self.p_h_walks = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Walked"]
        self.p_h_hbp = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Hit"]
        self.p_h_hits = hud_data[p_team_roster_str]["Defensive Stats"]["Hits Allowed"]
        self.p_h_hrs = hud_data[p_team_roster_str]["Defensive Stats"]["HRs Allowed"]
        self.p_h_pitches_thrown = hud_data[p_team_roster_str]["Defensive Stats"]["Pitches Thrown"]
        self.p_h_stamina = hud_data[p_team_roster_str]["Defensive Stats"]["Stamina"]
        self.p_h_strikeouts = hud_data[p_team_roster_str]["Defensive Stats"]["Strikeouts"]
        self.p_h_outs = hud_data[p_team_roster_str]["Defensive Stats"]["Outs Pitched"]

        self.half_inning_cur = hud_data["Half Inning"]

        self.b_h_team_index = self.half_inning_cur

        b_teamStr = "Away" if self.b_h_team_index == 0 else "Home"
        self.b_h_roster_loc = hud_data["Batter Roster Loc"]

        b_team_roster_str = b_teamStr + " Roster " + str(self.b_h_roster_loc)
        self.b_h_batter = hud_data[b_team_roster_str]["CharID"]
        self.b_h_at_bats = hud_data[b_team_roster_str]["Offensive Stats"]["At Bats"]
        self.b_h_hits = hud_data[b_team_roster_str]["Offensive Stats"]["Hits"]
        self.b_h_singles = hud_data[b_team_roster_str]["Offensive Stats"]["Singles"]
        self.b_h_doubles = hud_data[b_team_roster_str]["Offensive Stats"]["Doubles"]
        self.b_h_triples = hud_data[b_team_roster_str]["Offensive Stats"]["Triples"]
        self.b_h_homeruns = hud_data[b_team_roster_str]["Offensive Stats"]["Homeruns"]
        self.b_h_successful_bunts = hud_data[b_team_roster_str]["Offensive Stats"]["Successful Bunts"]
        self.b_h_sac_flys = hud_data[b_team_roster_str]["Offensive Stats"]["Sac Flys"]
        self.b_h_strikeouts = hud_data[b_team_roster_str]["Offensive Stats"]["Strikeouts"]
        self.b_h_walks = hud_data[b_team_roster_str]["Offensive Stats"]["Walks (4 Balls)"]
        self.b_h_HBP = hud_data[b_team_roster_str]["Offensive Stats"]["Walks (Hit)"]
        self.b_h_RBI = hud_data[b_team_roster_str]["Offensive Stats"]["RBI"]
        self.b_h_steals = hud_data[b_team_roster_str]["Offensive Stats"]["Bases Stolen"]
        self.b_h_star_hits = hud_data[b_team_roster_str]["Offensive Stats"]["Star Hits"]

        self.BATTER_HUD_STATS_LIST = [
            self.b_h_at_bats,
            self.b_h_hits,
            self.b_h_singles,
            self.b_h_doubles,
            self.b_h_triples,
            self.b_h_homeruns,
            self.b_h_successful_bunts,
            self.b_h_sac_flys,
            self.b_h_strikeouts,
            self.b_h_walks,
            self.b_h_HBP,
            self.b_h_RBI,
            self.b_h_steals,
            self.b_h_star_hits,
        ]

        if str(self.half_inning_old) != str(hud_data["Half Inning"]):
            self.flip_teams()
            self.half_inning_old = str(hud_data["Half Inning"])

    def stat_output_create(self):
        #to do: edit to make the strings within this function, and let the other functions just grab the totals.

        b_custom_stats_list = []
        b_custom_stats_list.append("Batter: " + str(self.b_h_batter))
        self.b_stats_string = ""
        b_custom_stats_list.append("Season Stats:")
        b_custom_stats_list.append("AVG: " + str('{0:.3f}'.format(float(self.b_t_avg))))
        #b_custom_stats_list.append("Hits: " + str(self.b_t_hits))
        if self.b_t_hr != 0: b_custom_stats_list.append("Season HRs: " + str(self.b_t_hr))
        for i in range(len(self.BATTER_HUD_STATS_LIST)):
            if self.BATTER_HUD_STATS_LIST[i] != 0:
                if i == 0:
                    b_custom_stats_list.append("Current Game: ")
                    b_custom_stats_list.append(str(self.b_h_hits) + ' for ' + str(self.b_h_at_bats))
                # if i == 1:
                # b_custom_stats_list.append("Hits: " + str(self.b_h_hits))
                if i == 2:
                    single = " Single" if self.b_h_singles == 1 else " Singles"
                    b_custom_stats_list.append(str(self.b_h_singles) + single)
                if i == 3:
                    double = " Double" if self.b_h_doubles == 1 else " Doubles"
                    b_custom_stats_list.append(str(self.b_h_doubles) + double)
                if i == 4:
                    triple = " Triple" if self.b_h_triples == 1 else " Triples"
                    b_custom_stats_list.append(str(self.b_h_triples) + triple)
                if i == 5:
                    homerun = " Home Run" if self.b_h_homeruns == 1 else " Home Runs"
                    b_custom_stats_list.append(str(self.b_h_homeruns) + homerun)
                if i == 6:
                    bunt = " Successful Bunt" if self.b_h_successful_bunts == 1 else " Successful Bunts"
                    b_custom_stats_list.append(str(self.b_h_successful_bunts) + bunt)
                if i == 7:
                    sacfly = " Sac Fly" if self.b_h_sac_flys == 1 else " Sac Flies"
                    b_custom_stats_list.append(str(self.b_h_sac_flys) + sacfly)
                if i == 8:
                    strikeout = " Strikeout" if self.b_h_strikeouts == 1 else " Strikeouts"
                    b_custom_stats_list.append(str(self.b_h_strikeouts) + strikeout)
                if i == 9:
                    walk = " Walk" if self.b_h_walks == 1 else " Walks"
                    b_custom_stats_list.append(str(self.b_h_walks) + walk)
                if i == 10:
                    hbp = " HBP" if self.b_h_HBP == 1 else " HBPs"
                    b_custom_stats_list.append(str(self.b_h_HBP) + hbp)
                if i == 11:
                    b_custom_stats_list.append(str(self.b_h_RBI) + " RBI")
                if i == 12:
                    steal = " Steal" if self.b_h_steals == 1 else " Steals"
                    b_custom_stats_list.append(str(self.b_h_steals) + steal)
                if i == 13:
                    starhit = " Star Hit" if self.b_h_star_hits == 1 else " Star Hits"
                    b_custom_stats_list.append(str(self.b_h_star_hits) + starhit)

        for line in b_custom_stats_list:
            self.b_stats_string += line + "\n"

        p_seasonAvg_stat_string = self.p_t_stats_string 
        p_game_stat_string = f'Pitcher: {self.p_h_pitcher} \n Season Stats:\n ERA: {self.p_t_ERA:.1f}\n Opp AVG: {self.p_t_oppAvg:.3f} \n Game Stats:\n'
        for line in self.p_hud_stats_string[1:]:
            p_game_stat_string += line + "\n"

        self.p_combined_text_output = p_game_stat_string


    def stat_output_update_display(self):
        b_source = S.obs_get_source_by_name("batter_combined_stats_text")
        if b_source is not None:
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "text", self.b_stats_string)
            S.obs_source_update(b_source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(b_source)
        S.obs_source_release(b_source)

        p_source = S.obs_get_source_by_name("pitcher_combined_stats_text")
        if p_source is not None:
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "text", self.p_combined_text_output)
            S.obs_source_update(p_source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(p_source)
        S.obs_source_release(p_source)

    def summary_stats_display(self):
        source = S.obs_get_source_by_name("batter_summary_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", self.b_t_stats_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)
        
        source = S.obs_get_source_by_name("pitcher_summary_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", self.p_t_stats_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        if self.debugMode:
            print(self.b_t_stats_string)
            print(self.p_t_stats_string)

    def custom_stats(self):
        p_custom_stats_list = []
        if self.p_h_pitcher != "First Event":
            p_custom_stats_list.append("Pitcher: " + str(self.p_h_pitcher))
        p_stats_string = ""
        p_stats_list = S.obs_data_get_string(globalsettings, "_pitching_stats").split(";")
        for item in p_stats_list:
            if item == "Batters Faced" or item == "1" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Batters Faced: " + str(self.p_h_batters_faced))
            if item == "Runs Allowed" or item == "2" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Runs Allowed: " + str(self.p_h_runs_allowed))
            if item == "Earned Runs" or item == "3" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Earned Runs: " + str(self.p_h_runs_allowed))
            if item == "Walks" or item == "4" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Walks: " + str(self.p_h_walks))
            if item == "HBP" or item == "5" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("HBP: " + str(self.p_h_hbp))
            if item == "Hits Allowed" or item == "6" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Hits Allowed: " + str(self.p_h_hits))
            if item == "HRs Allowed" or item == "7" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("HRs Allowed: " + str(self.p_h_hrs))
            if item == "Pitch Count" or item == "8" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Pitch Count: " + str(self.p_h_pitches_thrown))
            if item == "Stamina" or item == "9" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Stamina: " + str(self.p_h_stamina))
            if item == "Strikeouts" or item == "10" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Strikeouts: " + str(self.p_h_strikeouts))
            if item == "Outs Pitched" or item == "11" and self.p_h_pitcher != "First Event":
                p_custom_stats_list.append("Outs Pitched: " + str(self.p_h_outs))

        for line in p_custom_stats_list:
            p_stats_string += line + "\n"

        #to be used in the combined stat code
        self.p_hud_stats_string = p_custom_stats_list

        source = S.obs_get_source_by_name("pitcher_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", p_stats_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

def script_load(settings):

    S.timer_add(check_for_updates, 1000)

    global globalsettings
    globalsettings = settings

    global HUD_path
    HUD_path = S.obs_data_get_string(settings, "_path")

    global visible_bool
    visible_bool = S.obs_data_get_bool(settings, '_visible')

    global getstats
    getstats = pitcherstats()

    getstats.new_event = 1
    getstats.dir_scan()

    getstats.summary_stats()
    

def check_for_updates():
   if pause_bool == False:
        getstats.dir_scan()
        getstats.summary_stats()
        getstats.custom_stats()
        getstats.summary_stats_display()
        

        #new - eventually delete the other displays
        getstats.stat_output_create()
        getstats.stat_output_update_display()

def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    getstats.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global globalsettings
    globalsettings = settings

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, "_pause")

    global visible_bool
    visible_bool = S.obs_data_get_bool(settings, '_visible')

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

def add_summary_pressed(props, prop):
    getstats.add_summary_stats()
    getstats.dir_scan()
    getstats.parse_web_stats()
    getstats.summary_stats()
    getstats.summary_stats_display()

def toggle_stat_display_pressed(props, prop):
    #code source to be added or removed when this button is pressed
    if getstats.debugMode:
        print("toggle combined stats")

    current_scene = S.obs_frontend_get_current_scene()
    getstats.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    #check if the sources already exist.
    Batter_Combined_Stats_Source = S.obs_scene_find_source(getstats.scene,'batter_combined_stats_text')
    Pitcher_Combined_Stats_Source = S.obs_scene_find_source(getstats.scene,'pitcher_combined_stats_text')

    #batting text box
    if Batter_Combined_Stats_Source is None: #source doesn't exist, so create
        settings = S.obs_data_create()
        if getstats.platform == 'MacOS':
            Batter_Combined_Stats_Source = S.obs_source_create("text_ft2_source", 'batter_combined_stats_text', settings, None)
        else:
            Batter_Combined_Stats_Source = S.obs_source_create("text_gdiplus", 'batter_combined_stats_text', settings, None)
        S.obs_scene_add(getstats.scene, Batter_Combined_Stats_Source)
        S.obs_source_release(Batter_Combined_Stats_Source)
        S.obs_data_release(settings)
    else: #source exists, so delete
        S.obs_sceneitem_remove(Batter_Combined_Stats_Source)

    #pitching text box
    if Pitcher_Combined_Stats_Source is None: #source doesn't exist, so create
        settings = S.obs_data_create()
        if getstats.platform == 'MacOS':
            Pitcher_Combined_Stats_Source = S.obs_source_create("text_ft2_source", 'pitcher_combined_stats_text', settings, None)
        else:
            Pitcher_Combined_Stats_Source = S.obs_source_create("text_gdiplus", 'pitcher_combined_stats_text', settings, None)
        S.obs_scene_add(getstats.scene, Pitcher_Combined_Stats_Source)
        S.obs_source_release(Pitcher_Combined_Stats_Source)
        S.obs_data_release(settings)    
    else: #source exists, so delete
        S.obs_sceneitem_remove(Pitcher_Combined_Stats_Source)
    
def flip_teams(props, prop):
    getstats.flip_teams()
    
def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_bool(props, "_pause", "Pause")
    S.obs_properties_add_text(props, "_pitching_stats", "Pitching Stats", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(props, "_batting_stats", "Batting Stats", S.OBS_TEXT_DEFAULT)

    S.obs_properties_add_button(props, "_add_button", "Add Game Stats", add_pressed)
    S.obs_properties_add_button(props, "_removebutton", "Remove Game Stats", remove_pressed)

    S.obs_properties_add_button(props, "_addSummaryStatsButton", "Add Summary Stats", add_summary_pressed)

    S.obs_properties_add_button(props, "_toggleStatOutputButton", "Toggle Stat Display", toggle_stat_display_pressed)

    OS_list = S.obs_properties_add_list(props, "_OS_list", "OS:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, "Custom", "custom")
    S.obs_property_list_add_string(OS_list, "Windows", "windows")
    S.obs_property_list_add_string(OS_list, "MacOS", "macOS")
    S.obs_properties_add_text(props, "_path", "Path to HUD json:", S.OBS_TEXT_DEFAULT)

    S.obs_properties_add_button(props, "_flipteams", "Flip Team Locations", flip_teams)

    #add dropdown for modes to filter web stats
    web_mode_list = S.obs_properties_add_list(props, "_web_mode_list", "Mode for Web Stats:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    

    #if the list of modes was already fetched, don't do it again.
    global getstats
    if getstats.got_modes == False:
        getstats.get_active_modes()
        getstats.got_modes = True

    #add modes to the dropdown
    S.obs_property_list_add_string(web_mode_list, "All", "all")

    S.obs_property_list_add_string(web_mode_list, 'Stars Off Season7', 'StarsOffSeason7')
    S.obs_property_list_add_string(web_mode_list, 'Stars On Season 7', 'StarsOnHazardousSeason7')
    S.obs_property_list_add_string(web_mode_list, 'Big Balla Season 7', 'BigBallaRandomsSeason7')
    S.obs_property_list_add_string(web_mode_list, 'Stars Off Hazards Season 7', 'StarsOffHazardousSeason7')
    S.obs_property_list_add_string(web_mode_list, 'Stars Off Hazards Randoms Season 7', 'StarsOffHazardousRandomsSeason7')
    S.obs_property_list_add_string(web_mode_list, 'Stars Off Hazards Season 7', 'StarsOffMegaSeason7')
    # for i in range(len(getstats.mode_names)):
    # S.obs_property_list_add_string(web_mode_list, getstats.mode_names[i], re.sub(r'[^a-zA-Z0-9]', '', getstats.mode_names[i]))

    S.obs_properties_add_button(props, "_getWebStats", "Get Web Stats", get_stats_func)

    S.obs_properties_add_bool(props, '_visible', 'Automatically make visible and fetch stats:')

    S.obs_property_set_modified_callback(OS_list, OS_callback)

    return props

def get_stats_func(props, prop):
    getstats.get_web_stats()

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