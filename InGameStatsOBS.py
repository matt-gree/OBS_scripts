import obspython as S
import os
import json
import platform as plt
from urllib.parse import urlencode
from urllib.request import urlopen, Request, HTTPError
import time
import threading
import ssl
from project_rio_lib.stat_file_parser import HudObj

# If you run this on a mac and get an SSL error, run the following code in Termianl:
# /Applications/Python\ 3.10/Install\ Certificates.command

#def script_defaults(settings):

class PitcherStats:
    def __init__(self):
        self.web_pitching_stats_loc = S.vec2()
        self.web_batting_stats_loc = S.vec2()

        self.pitcher = str()
        self.batter = str()

        self.current_event_num = -1
        self.current_half_inning = 0

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        self.pitching_web = {
            'Batters Faced': 0,
            'Runs Allowed': 0,
            'Walks': 0,
            'HBP': 0,
            'Hits': 0,
            'Pitches Thrown': 0,
            'Strikeouts': 0,
            'Outs Pitched': 0
        }

        self.batting_web = {
            'At Bats': 0,
            'Hits': 0,
            'Singles': 0,
            'Doubles': 0,
            'Triples': 0,
            'Home Runs': 0,
            'Sac Flys': 0,
            'Strikeouts': 0,
            'Walks': 0,
            'HBP': 0,
            'RBI': 0
        }

        self.pitching_hud_file = {
            'Batters Faced': 0,
            'Runs Allowed': 0,
            'Earned Runs': 0,
            'Walks': 0,
            'HBP': 0,
            'Hits': 0,
            'Home Runs': 0,
            'Pitches Thrown': 0,
            'Stamina': 0,
            'Strikeouts': 0,
            'Outs Pitched': 0,
        }

        self.batting_hud_file = {
            'Team Index': 0,
            'Roster Location': 0,
            'At Bats': 0,
            'Hits': 0,
            'Singles': 0,
            'Doubles': 0,
            'Triples': 0,
            'Home Runs': 0,
            'Successful Bunts': 0,
            'Sacrifice Flies': 0,
            'Strikeouts': 0,
            'Walks': 0,
            'HBP': 0,
            'RBI': 0,
            'Steals': 0,
            'Star Hits': 0,
        }
        
        self.batting_summary = {
            'At Bats': 0,
            'AVG': 0,
            'SLG': 0,
            'Hits': 0,
            'Singles': 0,
            'Doubles': 0,
            'Triples': 0,
            'Home Runs': 0,
            'RBI': 0,
            'Strikeouts': 0,
            'Walks': 0,
            'HBP': 0,
            'SO%': 0,
        }

        self.pitching_summary = {
            'Earned Runs': 0,
            'Outs Pitched': 0,
            'ERA': 0,
            'Strikeouts': 0,
            'Batters Faced': 0,
            'Opponent AVG': 0,
            'K%': 0,
            'Innings Pitched': 0
        }

        self.is_new_event = 1

        self.pitching_string = str()
        self.batting_string = str()

        self.away_string = str()
        self.home_string = str()

        self.home_player = str()
        self.away_player = str()

        self.web_data_home = {}
        self.web_data_away = {}

        self.calledWebInd = False

        self.mode_names = []
        self.got_modes = False

        self.debugMode = True

        if str(plt.platform()).lower()[0] == 'm':
            self.platform = 'MacOS'
        elif str(plt.platform()).lower()[0] == 'w':
            self.platform = 'Windows'
        else:
            self.platform = 'Unknown'

    def flip_teams(self):
        if self.debugMode:
            print("flip_teams")

        #flip web stats
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "away_summary_stats_text"), self.web_pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "home_summary_stats_text"), self.web_batting_stats_loc)

        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "home_summary_stats_text"), self.web_pitching_stats_loc)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(self.scene, "away_summary_stats_text"), self.web_batting_stats_loc)

        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "home_summary_stats_text"), self.web_pitching_stats_loc)
        S.obs_sceneitem_get_pos(S.obs_scene_find_source_recursive(self.scene, "away_summary_stats_text"), self.web_batting_stats_loc)

    def add_summary_stats(self):
        if self.debugMode:
            print("adding summmary stats")

        current_scene = S.obs_frontend_get_current_scene()
        self.scene = S.obs_scene_from_source(current_scene)
        S.obs_source_release(current_scene)

        #check if the sources already exist.
        old_bSummary_source = S.obs_scene_find_source(self.scene,'away_summary_stats_text')
        old_pSummary_source = S.obs_scene_find_source(self.scene,'home_summary_stats_text')

        #Add batting text box
        if old_bSummary_source is None: # only create if it doesn't already exist
            settings = S.obs_data_create()
            if self.platform == 'MacOS':
                batting_summary_Stats_Text = S.obs_source_create("text_ft2_source", 'away_summary_stats_text', settings, None)
            else:
                batting_summary_Stats_Text = S.obs_source_create("text_gdiplus", 'away_summary_stats_text', settings, None)
            S.obs_scene_add(self.scene, batting_summary_Stats_Text)
            S.obs_source_release(batting_summary_Stats_Text)
            S.obs_data_release(settings)

        #Add pitching text box
        if old_pSummary_source is None: # only create if it doesn't already exist
            settings = S.obs_data_create()
            if self.platform == 'MacOS':
                pitching_summary_Stats_Text = S.obs_source_create("text_ft2_source", 'home_summary_stats_text', settings, None)
            else:
                pitching_summary_Stats_Text = S.obs_source_create("text_gdiplus", 'home_summary_stats_text', settings, None)
            S.obs_scene_add(self.scene, pitching_summary_Stats_Text)
            S.obs_source_release(pitching_summary_Stats_Text)
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

    
    def get_web_stats(self, threading_bool=True):
        if self.debugMode:
            print("get web stats")

        url_base = "https://api.projectrio.app/stats/?"
        
        #check if the stats should be filtered by game mode
        web_stat_mode = S.obs_data_get_string(globalsettings, "_web_mode_list")
        if web_stat_mode == "all":
            mode_url_addition = ""
        else:
            mode_url_addition = "&tag=" + web_stat_mode

        url_home = f'{url_base}&by_char=1&username={self.home_player}{mode_url_addition}&exclude_fielding=1'
        url_away = f'{url_base}&by_char=1&username={self.away_player}{mode_url_addition}&exclude_fielding=1'
        
        if self.debugMode:
            print(url_home)
            print(url_away)

        def make_api_call():
            #check if stats were found for each player.
            
            def fetch_data(url):
                try:
                    return json.loads(urlopen(url).read())
                except ssl.SSLCertVerificationError as e:
                    print(f'SSL Certificate verification failed. Ensure all certificates for Python have been installed: {e}')
                except HTTPError as e:
                    print(f'HTTPError: {e.code} - {e.reason}. Likely an invalid username and nothing to worry about. Check URL or request parameters.')
                return {}

            self.web_data_home = fetch_data(url_home)
            self.web_data_away = fetch_data(url_away)
            
            self.calledWebInd = True

            print("Home stats found:", bool(self.web_data_home))
            print("Away stats found:", bool(self.web_data_away))

        # make_api_call()
        if threading_bool:
            api_call_thread = threading.Thread(target=make_api_call)
            api_call_thread.start()
        else:
            make_api_call()
        
    def parse_web_stats(self):
        if self.debugMode:
            print("parse web stats")

        def get_web_data(team, character, action):
            if team == 0:
                return self.web_data_away.get('Stats', {}).get(character, {}).get(action, {})
            elif team == 1:
                return self.web_data_home.get('Stats', {}).get(character, {}).get(action, {})

        if self.current_half_inning == 0:
            web_data_pitcher = get_web_data(1, self.pitcher, 'Pitching')
            web_data_batter = get_web_data(0, self.batter, 'Batting')
        else:
            web_data_batter = get_web_data(1, self.batter, 'Batting')
            web_data_pitcher = get_web_data(0, self.pitcher, 'Pitching')

        if self.debugMode:
            print("batter found", bool(web_data_batter), web_data_batter)
            print("pitcher found", bool(web_data_pitcher), web_data_pitcher)

        if web_data_batter:
            self.batting_web['At Bats'] = web_data_batter["summary_at_bats"]
            self.batting_web['Hits'] = web_data_batter["summary_hits"]
            self.batting_web['Singles'] = web_data_batter["summary_singles"]
            self.batting_web['Doubles'] = web_data_batter["summary_doubles"]
            self.batting_web['Triples'] = web_data_batter["summary_triples"]
            self.batting_web['Home Runs'] = web_data_batter["summary_homeruns"]
            self.batting_web['Sac Flys'] = web_data_batter["summary_sac_flys"]
            self.batting_web['Strikeouts'] = web_data_batter["summary_strikeouts"]
            self.batting_web['Walks'] = web_data_batter["summary_walks_bb"]
            self.batting_web['HBP'] = web_data_batter["summary_walks_hbp"]
            self.batting_web['RBI'] = web_data_batter["summary_rbi"]
        else:
            for key in self.batting_web:
                self.batting_web[key] = 0

        if web_data_pitcher:
            self.pitching_web['Batters Faced'] = web_data_pitcher["batters_faced"]
            self.pitching_web['Runs Allowed'] = web_data_pitcher["runs_allowed"]
            self.pitching_web['Walks'] = web_data_pitcher["walks_bb"]
            self.pitching_web['HBP'] = web_data_pitcher["walks_hbp"]
            self.pitching_web['Hits'] = web_data_pitcher["hits_allowed"]
            self.pitching_web['Pitches Thrown'] = web_data_pitcher["total_pitches"]
            self.pitching_web['Strikeouts'] = web_data_pitcher["strikeouts_pitched"]
            self.pitching_web['Outs Pitched'] = web_data_pitcher["outs_pitched"]
        else:
            for key in self.pitching_web:
                self.pitching_web[key] = 0

    def set_visible(self):
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, "away_summary_stats_text"), True)
        S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(self.scene, "home_summary_stats_text"), True)

    def summary_stats(self):
        #updates web stat variables
        getstats.parse_web_stats()

        self.batting_string = self.batter
        self.batting_summary['At Bats'] = self.batting_hud_file['At Bats'] + self.batting_web['At Bats']
        self.batting_summary['Hits'] = self.batting_hud_file['Hits'] + self.batting_web['Hits']
        self.batting_summary['Singles'] = self.batting_hud_file['Singles'] + self.batting_web['Singles']
        self.batting_summary['Doubles'] = self.batting_hud_file['Doubles'] + self.batting_web['Doubles']
        self.batting_summary['Triples'] = self.batting_hud_file['Triples'] + self.batting_web['Triples']
        self.batting_summary['Home Runs'] = self.batting_hud_file['Home Runs'] + self.batting_web['Home Runs']
        self.batting_summary['AVG'] = 0 if self.batting_summary['At Bats'] == 0 else self.batting_summary['Hits'] / self.batting_summary['At Bats']
        self.batting_summary['SLG'] = 0 if self.batting_summary['At Bats'] == 0 else (
            self.batting_summary['Singles'] +
            2 * self.batting_summary['Doubles'] +
            3 * self.batting_summary['Triples'] +
            4 * self.batting_summary['Home Runs']
        ) / self.batting_summary['At Bats']
        self.batting_summary['RBI'] = self.batting_hud_file['RBI'] + self.batting_web['RBI']
        self.batting_summary['Strikeouts'] = self.batting_hud_file['Strikeouts'] + self.batting_web['Strikeouts']
        self.batting_summary['Walks'] = self.batting_hud_file['Walks'] + self.batting_web['Walks']
        self.batting_summary['HBP']  = self.batting_hud_file['HBP'] + self.batting_web['HBP']
        self.batting_summary['SO%'] = 0 if self.batting_summary['At Bats'] == 0 else (self.batting_summary['Strikeouts'] / self.batting_summary['At Bats']) * 100

        self.batting_string += f"  ({self.batting_summary['At Bats']} ABs)\nAvg: {self.batting_summary['AVG']:.3f}  SLG: {self.batting_summary['SLG']:.3f}  SO%: {self.batting_summary['SO%']:.0f}%"

        self.pitching_string = self.pitcher
        self.pitching_summary['Earned Runs'] = self.pitching_hud_file['Earned Runs'] + self.pitching_web['Runs Allowed']
        self.pitching_summary['Outs Pitched'] = self.pitching_hud_file['Outs Pitched'] + self.pitching_web['Outs Pitched']
        self.pitching_summary['ERA'] = 0 if self.pitching_summary['Outs Pitched'] == 0 else 27*(self.pitching_summary['Earned Runs']/(self.pitching_summary['Outs Pitched']))
        self.pitching_summary['Strikeouts'] = self.pitching_hud_file['Strikeouts'] + self.pitching_web['Strikeouts']
        self.pitching_summary['Batters Faced'] = self.pitching_hud_file['Batters Faced'] + self.pitching_web['Batters Faced']
        self.pitching_summary['Hits'] = self.pitching_hud_file['Hits'] + self.pitching_web['Hits']
        self.pitching_summary['Opponent AVG'] = 0 if self.pitching_summary['Batters Faced'] == 0 else self.pitching_summary['Hits']/self.pitching_summary['Batters Faced']
        self.pitching_summary['K%'] = 0 if self.pitching_summary['Batters Faced'] == 0 else 100* self.pitching_summary['Strikeouts']/self.pitching_summary['Batters Faced']
        self.pitching_summary['Innings Pitched'] = (self.pitching_summary['Outs Pitched']//3) + (self.pitching_summary['Outs Pitched']%3/10)

        self.pitching_string += f"  ({self.pitching_summary['Innings Pitched']:.1f} IP)\nERA: {self.pitching_summary['ERA']:.1f}  K%: {self.pitching_summary['K%']:.0f}%  Opp Avg: {self.pitching_summary['Opponent AVG']:.3f}"

        if self.debugMode:
            print(self.batting_summary)
            print(self.pitching_summary)

        
        if self.current_half_inning == 0:
            self.away_string = self.batting_string
            self.home_string = self.pitching_string
        else:
            self.away_string = self.pitching_string
            self.home_string = self.batting_string

    def dir_scan(self):
        hud_file_path = S.obs_data_get_string(globalsettings, '_path')
        hud_file_path = hud_file_path.replace("\\", "/")
        
        if not os.path.isfile(hud_file_path):
            return

        with open(hud_file_path) as f:
            hud_data = json.load(f)
        
        hud_data_object = HudObj(hud_data)
        
        print(self.current_event_num)
        print(hud_data_object.event_number)
        print(self.is_new_event)


        if (self.current_event_num == hud_data_object.event_number):
            if (self.is_new_event != 1):
                return False
            
        self.is_new_event = 0

        self.current_event_num = hud_data['Event Num']
        self.current_half_inning = hud_data["Half Inning"]


        self.home_player = hud_data["Home Player"]
        self.away_player = hud_data["Away Player"]

        global visible_bool

        if visible_bool is True and ((hud_data_object.event_number == '0b')
                                     or (self.current_event_num == '0b')
                                     or (hud_data_object.event_integer() < int(str(self.current_event_num)[:-1]))):

            S.timer_remove(check_for_updates)
            
            def visible_threading():
                # Needed so the stats are made visible after the api call is made on the thread
                self.get_web_stats(threading_bool=False)
                self.set_visible()

            api_call_thread = threading.Thread(target=visible_threading)
            api_call_thread.start()
            print("Fetching stats and making visible")

            S.timer_add(check_for_updates, 1000)

        teamStr = "Away" if self.current_half_inning == 1 else "Home"
        pitcher_id = hud_data['Pitcher Roster Loc']

        p_team_roster_str = teamStr + " Roster " + str(pitcher_id)

        # Vars to hold data for characters and teams(player)
        self.pitcher = hud_data[p_team_roster_str]["CharID"]
        self.pitching_hud_file['Batters Faced'] = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Faced"]
        self.pitching_hud_file['Runs Allowed'] = hud_data[p_team_roster_str]["Defensive Stats"]["Runs Allowed"]
        self.pitching_hud_file['Earned Runs'] = hud_data[p_team_roster_str]["Defensive Stats"]["Earned Runs"]
        self.pitching_hud_file['Walks'] = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Walked"]
        self.pitching_hud_file['HBP'] = hud_data[p_team_roster_str]["Defensive Stats"]["Batters Hit"]
        self.pitching_hud_file['Hits'] = hud_data[p_team_roster_str]["Defensive Stats"]["Hits Allowed"]
        self.pitching_hud_file['Home Runs'] = hud_data[p_team_roster_str]["Defensive Stats"]["HRs Allowed"]
        self.pitching_hud_file['Pitches Thrown'] = hud_data[p_team_roster_str]["Defensive Stats"]["Pitches Thrown"]
        self.pitching_hud_file['Stamina'] = hud_data[p_team_roster_str]["Defensive Stats"]["Stamina"]
        self.pitching_hud_file['Strikeouts'] = hud_data[p_team_roster_str]["Defensive Stats"]["Strikeouts"]
        self.pitching_hud_file['Outs Pitched'] = hud_data[p_team_roster_str]["Defensive Stats"]["Outs Pitched"]

        b_teamStr = "Away" if self.current_half_inning == 0 else "Home"
        self.batting_hud_file['Roster Location'] = hud_data["Batter Roster Loc"]

        b_team_roster_str = b_teamStr + " Roster " + str(self.batting_hud_file['Roster Location'])

        self.batter = hud_data[b_team_roster_str]["CharID"]
        self.batting_hud_file['At Bats'] = hud_data[b_team_roster_str]["Offensive Stats"]["At Bats"]
        self.batting_hud_file['Hits'] = hud_data[b_team_roster_str]["Offensive Stats"]["Hits"]
        self.batting_hud_file['Singles'] = hud_data[b_team_roster_str]["Offensive Stats"]["Singles"]
        self.batting_hud_file['Doubles'] = hud_data[b_team_roster_str]["Offensive Stats"]["Doubles"]
        self.batting_hud_file['Triples'] = hud_data[b_team_roster_str]["Offensive Stats"]["Triples"]
        self.batting_hud_file['Home Runs'] = hud_data[b_team_roster_str]["Offensive Stats"]["Homeruns"]
        self.batting_hud_file['Successful Bunts'] = hud_data[b_team_roster_str]["Offensive Stats"]["Successful Bunts"]
        self.batting_hud_file['Sacrifice Flies'] = hud_data[b_team_roster_str]["Offensive Stats"]["Sac Flys"]
        self.batting_hud_file['Strikeouts'] = hud_data[b_team_roster_str]["Offensive Stats"]["Strikeouts"]
        self.batting_hud_file['Walks'] = hud_data[b_team_roster_str]["Offensive Stats"]["Walks (4 Balls)"]
        self.batting_hud_file['HBP'] = hud_data[b_team_roster_str]["Offensive Stats"]["Walks (Hit)"]
        self.batting_hud_file['RBI'] = hud_data[b_team_roster_str]["Offensive Stats"]["RBI"]
        self.batting_hud_file['Steals'] = hud_data[b_team_roster_str]["Offensive Stats"]["Bases Stolen"]
        self.batting_hud_file['Star Hits'] = hud_data[b_team_roster_str]["Offensive Stats"]["Star Hits"]

        self.summary_stats()
            

    def summary_stats_display(self):
        source = S.obs_get_source_by_name("away_summary_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", self.away_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)
        
        source = S.obs_get_source_by_name("home_summary_stats_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", self.home_string)
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
    getstats = PitcherStats()

    getstats.new_event = 1
    getstats.dir_scan()

    getstats.summary_stats()

def check_for_updates():
    if pause_bool is False:
        getstats.dir_scan()
        # getstats.summary_stats()
        getstats.summary_stats_display()

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
    return "Mario Baseball Stats Version 2.0.0\n" \
           "OBS interface by MattGree \n" \
           "Thanks to the Rio Devs for developing the HUD files  \n" \
           "Support me on YouTube! \n" \

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
    
def flip_teams(props, prop):
    getstats.flip_teams()
    
def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_bool(props, "_pause", "Pause")

    S.obs_properties_add_button(props, "_addSummaryStatsButton", "Add Summary Stats", add_summary_pressed)

    OS_list = S.obs_properties_add_list(props, "_OS_list", "OS:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, "Custom", "custom")
    S.obs_property_list_add_string(OS_list, "Windows", "windows")
    S.obs_property_list_add_string(OS_list, "MacOS", "macOS")
    S.obs_properties_add_text(props, "_path", "Path to HUD json:", S.OBS_TEXT_DEFAULT)

    S.obs_properties_add_button(props, "_flipteams", "Flip Team Locations", flip_teams)

    #add dropdown for modes to filter web stats
    web_mode_list = S.obs_properties_add_list(props, "_web_mode_list", "Mode for Web Stats:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    
    #if the list of modes was already fetched, don't do it again.
    # global getstats
    # if getstats.got_modes == False:
        # getstats.get_active_modes()
        # getstats.got_modes = True

    #add modes to the dropdown
    S.obs_property_list_add_string(web_mode_list, "All", "all")
    S.obs_property_list_add_string(web_mode_list, 'S10 Stars Off', 'S10SuperstarsOff')
    S.obs_property_list_add_string(web_mode_list, 'S10 Stars Off Hazards', 'S10SuperstarsOffHazards')
    S.obs_property_list_add_string(web_mode_list, 'S10 Stars On', 'S10SuperstarsOn')
    S.obs_property_list_add_string(web_mode_list, 'S10 Big Balla', 'S10BigBalla')
    S.obs_property_list_add_string(web_mode_list, 'MBA CL', 'MBAChampionsLeague2024')
    S.obs_property_list_add_string(web_mode_list, 'NNL Season 6', 'NNLSeason6')
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
        HUD_Path = current_path.split("\\", maxsplit=1)[0] + "/" + current_path.split("\\")[1] + "/" + current_path.split("\\")[2] + "/Documents/Project Rio/HudFiles/decoded.hud.json"
        S.obs_data_set_string(settings, "_path", HUD_Path)
    elif S.obs_data_get_string(settings, "_OS_list") == "macOS":
        current_path = str(os.path.realpath(__file__))
        HUD_Path = "/"+current_path.split("/", 3)[1] +"/"+ current_path.split("/", 3)[2] + "/" + "Library/Application Support/Project Rio/HudFiles/decoded.hud.json"
        S.obs_data_set_string(settings, "_path", HUD_Path)
    return True