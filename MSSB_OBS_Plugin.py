import obspython as S
import os
import json

canvas_width = 1280
canvas_height = 720
HUD_width = 550
HUD_height = 80

symbol_font = S.obs_data_create()
S.obs_data_set_string(symbol_font, "face", "DejaVu Sans Mono")
S.obs_data_set_int(symbol_font, "flags", 1)
S.obs_data_set_int(symbol_font, "size", 32)

star_font = S.obs_data_create()
S.obs_data_set_string(star_font, "face", "Heiti TC")
S.obs_data_set_int(star_font, "flags", 1)
S.obs_data_set_int(star_font, "size", 24)

small_symbol_font = S.obs_data_create()
S.obs_data_set_string(small_symbol_font, "face", "DejaVu Sans Mono")
S.obs_data_set_int(small_symbol_font, "flags", 1)
S.obs_data_set_int(small_symbol_font, "size", 20)

smaller_font = S.obs_data_create()
S.obs_data_set_string(smaller_font, "face", "Helvetica")
S.obs_data_set_int(smaller_font, "flags", 0)
S.obs_data_set_int(smaller_font, "size", 24)

default_font = S.obs_data_create()
S.obs_data_set_string(default_font, "face", "Helvetica")
S.obs_data_set_int(default_font, "flags", 0)
S.obs_data_set_int(default_font, "size", 32)


color_source1 = "Scoreboard Base"

color_default = 0xFF944e28


def script_defaults(settings):
    S.obs_data_set_int(settings, "_scoreboard_base_color", color_default)
    S.obs_data_set_string(settings, "_menu", "HUD Location")


    S.obs_data_set_obj(settings, "_inning_font", smaller_font)
    S.obs_data_set_obj(settings, "_halfinning_font", small_symbol_font)

    S.obs_data_set_obj(settings, "_away_player_font", default_font)
    S.obs_data_set_obj(settings, "_away_captain_font", smaller_font)
    S.obs_data_set_obj(settings, "_away_score_font", default_font)
    S.obs_data_set_obj(settings, "_away_stars_font", star_font)

    S.obs_data_set_obj(settings, "_home_player_font", default_font)
    S.obs_data_set_obj(settings, "_home_captain_font", smaller_font)
    S.obs_data_set_obj(settings, "_home_score_font", default_font)
    S.obs_data_set_obj(settings, "_home_stars_font", star_font)



    S.obs_data_set_obj(settings, "_chem_font", smaller_font)
    S.obs_data_set_obj(settings, "_bases_font", symbol_font)

    S.obs_data_set_obj(settings, "_count_font", default_font)
    S.obs_data_set_obj(settings, "_outs_font", small_symbol_font)

    S.obs_data_set_obj(settings, "_star_chance_font", default_font)



class HUD:
    def __init__(self):
        # set the intitial position of to be 0,0
        pos = S.vec2()
        self.location = pos
        self.location.x = 0
        self.location.y = 0

        self.current_event_num = -1
        self.current_hud = "None"

        # HUD values
        self.inning = None
        self.halfinning = None
        self.balls = None
        self.strikes = None
        self.outs = None

        self.awayplayer = None
        self.awaycaptain = None
        self.awayscore = None
        self.awaystars = None

        self.homeplayer = None
        self.homecaptain = None
        self.homescore = None
        self.homestars = None

        self.runner_1b = None
        self.runner_2b = None
        self.runner_3b = None
        self.chem = None
        self.star_chance = None

    def create_HUD(self):

        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)
        settings = S.obs_data_create()

        props = S.obs_properties_create()

        group = S.obs_scene_add_group2(scene, "HUD", signal=True)

        # HUD Text Boxes
        # Scene add must be called immediately after to avoid OBS crash
        # Crash issue may have been casued by not making a new settings every source

        # Inning
        settings = S.obs_data_create()
        Inning_Text = S.obs_source_create("text_ft2_source", 'inning_text', settings, None)
        S.obs_scene_add(scene, Inning_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "inning_text"))

        # Halfinning
        settings = S.obs_data_create()
        Halfinning_Text = S.obs_source_create("text_ft2_source", 'halfinning_text', settings, None)
        S.obs_scene_add(scene, Halfinning_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "halfinning_text"))

        # Count
        settings = S.obs_data_create()
        Count_Text = S.obs_source_create("text_ft2_source", 'count_text', settings, None)
        S.obs_scene_add(scene, Count_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "count_text"))

        # Outs
        settings = S.obs_data_create()
        Outs_Text = S.obs_source_create("text_ft2_source", 'outs_text', settings, None)
        S.obs_scene_add(scene, Outs_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "outs_text"))

        # Away Player Name
        settings = S.obs_data_create()
        Away_Player_Text = S.obs_source_create("text_ft2_source", 'away_player_text', settings, None)
        S.obs_scene_add(scene, Away_Player_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_player_text"))

        # Away Captain
        settings = S.obs_data_create()
        Away_Captain_Text = S.obs_source_create("text_ft2_source", 'away_captain_text', settings, None)
        S.obs_scene_add(scene, Away_Captain_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_captain_text"))

        # Away Score
        settings = S.obs_data_create()
        Away_Score_Text = S.obs_source_create("text_ft2_source", 'away_score_text', settings, None)
        S.obs_scene_add(scene, Away_Score_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_score_text"))

        # Away Stars
        settings = S.obs_data_create()
        Away_Stars_Text = S.obs_source_create("text_ft2_source", 'away_stars_text', settings, None)
        S.obs_scene_add(scene, Away_Stars_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_stars_text"))

        # Home Player Name
        settings = S.obs_data_create()
        Home_Player_Text = S.obs_source_create("text_ft2_source", 'home_player_text', settings, None)
        S.obs_scene_add(scene, Home_Player_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_player_text"))

        # Home Captain
        settings = S.obs_data_create()
        Home_Captain_Text = S.obs_source_create("text_ft2_source", 'home_captain_text', settings, None)
        S.obs_scene_add(scene, Home_Captain_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_captain_text"))

        # Home Score
        settings = S.obs_data_create()
        Home_Score_Text = S.obs_source_create("text_ft2_source", 'home_score_text', settings, None)
        S.obs_scene_add(scene, Home_Score_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_score_text"))

        # Home Stars
        settings = S.obs_data_create()
        Home_Stars_Text = S.obs_source_create("text_ft2_source", 'home_stars_text', settings, None)
        S.obs_scene_add(scene, Home_Stars_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_stars_text"))

        # 1st Base
        settings = S.obs_data_create()
        Runner_1b_Text = S.obs_source_create("text_ft2_source", 'runner_1b_text', settings, None)
        S.obs_scene_add(scene, Runner_1b_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "runner_1b_text"))

        # 2nd Base
        settings = S.obs_data_create()
        Runner_2b_Text = S.obs_source_create("text_ft2_source", 'runner_2b_text', settings, None)
        S.obs_scene_add(scene, Runner_2b_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "runner_2b_text"))

        # 3rd Base
        settings = S.obs_data_create()
        Runner_3b_Text = S.obs_source_create("text_ft2_source", 'runner_3b_text', settings, None)
        S.obs_scene_add(scene, Runner_3b_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "runner_3b_text"))

        # Chem
        settings = S.obs_data_create()
        Chem_Text = S.obs_source_create("text_ft2_source", 'chem_text', settings, None)
        S.obs_scene_add(scene, Chem_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "chem_text"))

        # Star Chance
        settings = S.obs_data_create()
        Star_Chance_Text = S.obs_source_create("text_ft2_source", 'star_chance_text', settings, None)
        S.obs_scene_add(scene, Star_Chance_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "star_chance_text"))

        # HUD Graphics
        S.obs_data_set_int(settings, "width", HUD_width)
        S.obs_data_set_int(settings, "height", HUD_height)
        S.obs_data_set_int(settings, "color", color_default)
        scoreboard_base = S.obs_source_create("color_source", 'scoreboard_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "scoreboard_base"))

        # Text Locations

        # Inning
        position = S.vec2()
        S.vec2_set(position, 375, 25)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'inning_text'), position)

        # Halfinning
        S.vec2_zero(position)
        S.vec2_set(position, 375, 5)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'halfinning_text'), position)

        # Away Player
        S.vec2_zero(position)
        S.vec2_set(position, 5, 5)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_player_text'), position)

        # Away Captain
        S.vec2_zero(position)
        S.vec2_set(position, 5, 45)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_captain_text'), position)

        # Away Score
        S.vec2_zero(position)
        S.vec2_set(position, 150, 5)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_score_text'), position)

        # Away Stars
        S.vec2_zero(position)
        S.vec2_set(position, 115, 45)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_stars_text'), position)

        # Home Player
        S.vec2_zero(position)
        S.vec2_set(position, 185, 5)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_player_text'), position)

        # Home Captain
        S.vec2_zero(position)
        S.vec2_set(position, 185, 45)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_captain_text'), position)

        # Home Score
        S.vec2_zero(position)
        S.vec2_set(position, 330, 5)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_score_text'), position)

        # Home Stars
        S.vec2_zero(position)
        S.vec2_set(position, 295, 45)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_stars_text'), position)

        # 1st Base
        S.vec2_zero(position)
        S.vec2_set(position, 440, 12)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'runner_1b_text'), position)

        # 2nd Base
        S.vec2_zero(position)
        S.vec2_set(position, 428, 0)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'runner_2b_text'), position)

        # 3rd Base
        S.vec2_zero(position)
        S.vec2_set(position, 416, 12)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'runner_3b_text'), position)

        # Chem
        S.vec2_zero(position)
        S.vec2_set(position, 420, 45)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'chem_text'), position)

        # Outs
        S.vec2_zero(position)
        S.vec2_set(position, 475, 45)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'outs_text'), position)

        # Count
        S.vec2_zero(position)
        S.vec2_set(position, 480, 10)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'count_text'), position)

        # Star Chance
        S.vec2_zero(position)
        S.vec2_set(position, 5, 80)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'star_chance_text'), position)

    def update_text(self):
        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)

        # Inning
        source = S.obs_get_source_by_name("inning_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.inning))
        S.obs_source_update(source, settings)

        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Halfinning
        source = S.obs_get_source_by_name("halfinning_text")
        settings = S.obs_data_create()
        if str(self.halfinning) == "0":
            halfinning_string = "▲"
            position = S.vec2()
            S.vec2_zero(position)
            S.vec2_set(position, 375, 0)
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'halfinning_text'), position)
        else:
            halfinning_string = "▼"
            position = S.vec2()
            S.vec2_zero(position)
            S.vec2_set(position, 375, 45)
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'halfinning_text'), position)

        S.obs_data_set_string(settings, "text", halfinning_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Count
        source = S.obs_get_source_by_name("count_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(str(self.balls) + "-" + str(self.strikes)))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Outs
        source = S.obs_get_source_by_name("outs_text")
        settings = S.obs_data_create()
        if str(self.outs) == "1":
            outs_string = "● ○ ○"
        elif str(self.outs) == "2":
            outs_string = "● ● ○"
        else:
            outs_string = "○ ○ ○"
        S.obs_data_set_string(settings, "text", outs_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Away Player
        source = S.obs_get_source_by_name("away_player_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.awayplayer))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Away Captain
        source = S.obs_get_source_by_name("away_captain_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.awaycaptain))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Away Score
        source = S.obs_get_source_by_name("away_score_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.awayscore))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Away Stars
        source = S.obs_get_source_by_name("away_stars_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str("★: " + str(self.awaystars)))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Home Player
        source = S.obs_get_source_by_name("home_player_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.homeplayer))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Home Captain
        source = S.obs_get_source_by_name("home_captain_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.homecaptain))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Home Score
        source = S.obs_get_source_by_name("home_score_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str(self.homescore))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Home Stars
        source = S.obs_get_source_by_name("home_stars_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str("★: " + str(self.homestars)))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # 1st Base
        source = S.obs_get_source_by_name("runner_1b_text")
        settings = S.obs_data_create()
        if self.runner_1b == "1":
            runner_1b_string = "◆"
        else:
            runner_1b_string = "◇"
        print(runner_1b_string)
        S.obs_data_set_string(settings, "text", runner_1b_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # 2nd Base
        source = S.obs_get_source_by_name("runner_2b_text")
        settings = S.obs_data_create()
        if self.runner_2b == "1":
            runner_2b_string = "◆"
        else:
            runner_2b_string = "◇"
        S.obs_data_set_string(settings, "text", runner_2b_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # 3rd Base
        source = S.obs_get_source_by_name("runner_3b_text")
        settings = S.obs_data_create()

        if self.runner_3b == "1":
            runner_3b_string = "◆"
        else:
            runner_3b_string = "◇"
        S.obs_data_set_string(settings, "text", runner_3b_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Chem
        source = S.obs_get_source_by_name("chem_text")
        settings = S.obs_data_create()
        S.obs_data_set_string(settings, "text", str("♪:" + str(self.chem)))
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

        # Star Chance
        source = S.obs_get_source_by_name("star_chance_text")
        settings = S.obs_data_create()
        if self.star_chance == "1":
            star_chance_string = "Star Chance!"
        else:
            star_chance_string = ""
        S.obs_data_set_string(settings, "text", star_chance_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)


    def dir_scan(self):
        hud_file_path = "/Users/matthewgreene/Library/Application Support/ProjectRio/HudFiles/decoded.hud.json"
        if not os.path.isfile(hud_file_path):
            return ""
        with open(hud_file_path) as f:
            hud_data = json.load(f)

        # Return if the event hasn't changed
        if (self.current_event_num == hud_data['Event Num']):
            return self.current_event_num

        print("New HUD:", self.current_event_num, hud_data['Event Num'])
        self.current_event_num = hud_data['Event Num']

        # Bookkeepping vars
        away_team_captain_char = str()
        home_team_captain_char = str()

        # Dicts to hold data for characters and teams(player)
        player_batter_data = {'Name': '', 'RBI': 0, 'SO': 0, 'BB/HBP': 0, 'AB': 0, 'H': 0, 'HR': 0}
        character_batter_data = {'Name': '', 'RBI': 0, 'SO': 0, 'BB/HBP': 0, 'AB': 0, 'H': 0, 'HR': 0}
        player_pitcher_data = {'Name': '', 'ER': 0, 'H': 0, 'SO': 0, 'STAM': 0, 'BB/HBP': 0, 'NP': 0}
        character_pitcher_data = {'Name': '', 'ER': 0, 'H': 0, 'SO': 0, 'STAM': 0, 'BB/HBP': 0, 'NP': 0}

        for team in range(0, 2):
            for roster in range(0, 9):
                team_roster_str = "Team " + str(team) + " Roster " + str(roster)
                if (hud_data[team_roster_str]["Captain"] == 1):
                    # Captains
                    if (team == 0):
                        home_team_captain_char = hud_data[team_roster_str]["CharID"]
                    else:
                        away_team_captain_char = hud_data[team_roster_str]["CharID"]

                captain_star_str = str()
                if hud_data[team_roster_str]['Superstar']:
                    captain_star_str += '*'
                if hud_data[team_roster_str]['Captain']:
                    captain_star_str += ' ©'

                # Get batter and pitcher data both for the player and individual character
                if team != hud_data["Half Inning"]:
                    batter_offensive_data = hud_data[team_roster_str]["Offensive Stats"]
                    player_batter_data['Name'] = hud_data['Away Player'] if team == 1 else hud_data['Home Player']
                    player_batter_data['AB'] += batter_offensive_data["At Bats"]
                    player_batter_data['H'] += batter_offensive_data["Hits"]
                    player_batter_data['HR'] += batter_offensive_data["Homeruns"]
                    player_batter_data['BB/HBP'] += batter_offensive_data["Walks (4 Balls)"]
                    player_batter_data['BB/HBP'] += batter_offensive_data["Walks (Hit)"]
                    player_batter_data['SO'] += batter_offensive_data["Strikeouts"]
                    player_batter_data['RBI'] += batter_offensive_data["RBI"]
                    if roster == hud_data["Batter Roster Loc"]:
                        character_batter_data['Name'] = str(hud_data[team_roster_str]["RosterID"]) + ". " + \
                                                        hud_data[team_roster_str]["CharID"] + captain_star_str
                        character_batter_data['AB'] += batter_offensive_data["At Bats"]
                        character_batter_data['H'] += batter_offensive_data["Hits"]
                        character_batter_data['HR'] += batter_offensive_data["Homeruns"]
                        character_batter_data['BB/HBP'] += batter_offensive_data["Walks (4 Balls)"]
                        character_batter_data['BB/HBP'] += batter_offensive_data["Walks (Hit)"]
                        character_batter_data['SO'] += batter_offensive_data["Strikeouts"]
                        character_batter_data['RBI'] += batter_offensive_data["RBI"]

                else:
                    pitcher_defensive_data = hud_data[team_roster_str]["Defensive Stats"]
                    player_pitcher_data['Name'] = hud_data['Away Player'] if team == 1 else hud_data['Home Player']
                    player_pitcher_data['ER'] += pitcher_defensive_data["Earned Runs"]
                    player_pitcher_data['H'] += pitcher_defensive_data["Hits Allowed"]
                    player_pitcher_data['STAM'] = 'NA'
                    player_pitcher_data['BB/HBP'] += pitcher_defensive_data["Batters Walked"]
                    player_pitcher_data['BB/HBP'] += pitcher_defensive_data["Batters Hit"]
                    player_pitcher_data['SO'] += pitcher_defensive_data["Strikeouts"]
                    player_pitcher_data['NP'] += pitcher_defensive_data["Pitches Thrown"]
                    if roster == hud_data["Pitcher Roster Loc"]:
                        character_pitcher_data['Name'] = hud_data[team_roster_str]["CharID"] + captain_star_str
                        character_pitcher_data['ER'] += pitcher_defensive_data["Earned Runs"]
                        character_pitcher_data['H'] += pitcher_defensive_data["Hits Allowed"]
                        character_pitcher_data['STAM'] += pitcher_defensive_data["Stamina"]
                        character_pitcher_data['BB/HBP'] += pitcher_defensive_data["Batters Walked"]
                        character_pitcher_data['BB/HBP'] += pitcher_defensive_data["Batters Hit"]
                        character_pitcher_data['SO'] += pitcher_defensive_data["Strikeouts"]
                        character_pitcher_data['NP'] += pitcher_defensive_data["Pitches Thrown"]

        # hud_output_file = os.path.join(output_dir, 'hud.txt')
        # batter_data_output_file = os.path.join(output_dir, 'batter_data.txt')
        # pitcher_data_output_file = os.path.join(output_dir, 'pitcher_data.txt')

        # Main HUD
        if hud_data['Half Inning'] == "0":
            self.halfinning = "0"
        else:
            self.halfinning = "1"

        self.inning = str(hud_data['Inning'])

        # Runners on
        self.runner_1b = "1" if hud_data.get("Runner 1B") else "0"
        self.runner_2b = "1" if hud_data.get("Runner 2B") else "0"
        self.runner_3b = "1" if hud_data.get("Runner 3B") else "0"

        self.awaycaptain = away_team_captain_char
        self.homecaptain = home_team_captain_char

        self.awayplayer = str(hud_data['Away Player'])
        self.homeplayer = str(hud_data['Home Player'])

        self.awayscore = hud_data['Away Score']
        self.homescore = hud_data['Home Score']

        self.awaystars = hud_data['Away Stars']
        self.homestars = hud_data['Home Stars']

        self.balls = hud_data['Balls']
        self.strikes = hud_data['Strikes']
        self.outs = hud_data['Outs']
        self.chem = hud_data['Chemistry Links on Base']
        print(self.chem, "chem")
        if hud_data['Star Chance']:
            self.star_chance = "1"
        else:
            self.star_chance = "0"

        self.update_text()
    # Previous Event info
    # First check if previous event exists and had contact
    # if (hud_data.get('Previous Event')):
    #    if (hud_data.get('Pitch') and hud_data.get('Contact')):
    #        contact_output_file = os.path.join(output_dir, 'contact.txt')
    #        with open(contact_output_file, 'w', encoding="utf-8") as f:


graphics = HUD()


def script_tick(seconds):
    if pause_HUD_bool == False:
        graphics.dir_scan()

def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    scene = S.obs_scene_from_source(current_scene)

    # Pause HUD
    global pause_HUD_bool
    pause_HUD_bool = S.obs_data_get_bool(settings, "_pause_HUD")

    #Real Time position update
    hpositionslider = S.obs_data_get_int(settings, "_hslider")
    vpositionslider = S.obs_data_get_int(settings, "_vslider")
    HUD_Group = S.obs_scene_find_source(scene, "HUD")
    position = S.vec2()
    S.vec2_set(position, int(((canvas_width - HUD_width) * (hpositionslider / 1000))), int(((canvas_height - HUD_height) * (vpositionslider / 1000))))
    S.obs_sceneitem_set_pos(HUD_Group, position)

    # Color Update
    source = S.obs_get_source_by_name("scoreboard_base")
    scoreboard_base_color = S.obs_data_get_int(settings, "_scoreboard_base_color")
    S.obs_data_set_int(settings, "color", scoreboard_base_color)
    S.obs_source_update(source, settings)

    # Fonts
    source = S.obs_get_source_by_name("away_player_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_away_player_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("away_captain_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_away_captain_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("away_score_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_away_score_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("away_stars_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_away_stars_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("home_player_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_home_player_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("home_captain_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_home_captain_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("home_score_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_home_score_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("home_stars_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_home_stars_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("inning_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_inning_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("halfinning_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_halfinning_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("chem_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_chem_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("runner_1b_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_bases_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("runner_2b_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_bases_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("runner_3b_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_bases_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("outs_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_outs_font"))
    S.obs_source_update(source, settings)

    source = S.obs_get_source_by_name("star_chance_text")
    S.obs_data_set_obj(settings, "font", S.obs_data_get_obj(settings, "_star_chance_font"))
    S.obs_source_update(source, settings)

def add_pressed(props, prop):
    graphics.create_HUD()
    graphics.update_text()

def remove_pressed(props, prop):
    S.obs_source_remove(S.obs_get_source_by_name("HUD"))

def script_description():
    return "Better Mario Baseball Game HUD \nBy MattGree and PeacockSlayer (and Rio Dev team)"


def script_properties():  # ui
    props = S.obs_properties_create()

    # Main menuing list
    menu_list = S.obs_properties_add_list(props, "_menu", "Choose", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(menu_list, "HUD Location", "location")
    S.obs_property_list_add_string(menu_list, "Colors", "color")
    S.obs_property_list_add_string(menu_list, "Stats", "stats")
    S.obs_property_list_add_string(menu_list, "Canvas Size", "size")
    S.obs_property_list_add_string(menu_list, "Fonts", "fonts")

    # Location Properties
    S.obs_properties_add_button(props, "button", "Add HUD", add_pressed)
    S.obs_properties_add_button(props, "removebutton", "Remove HUD", remove_pressed)
    S.obs_properties_add_int_slider(props, "_hslider", "Horizontal Location", 0, 1000, 1)
    S.obs_properties_add_int_slider(props, "_vslider", "Vertical Location", 0, 1000, 1)
    bool = S.obs_properties_add_bool(props, "_bool", "_bool:")

    # Color
    S.obs_properties_add_color(props, "_scoreboard_base_color", "Scoreboard Base")

    # Stats
    S.obs_properties_add_bool(props, "_pause_HUD", "Pause HUD")

    # Canvas Size Properties
    canvas_size_list = S.obs_properties_add_list(props, "_canvas_size", "Resolution", S.OBS_COMBO_TYPE_LIST,
                                                 S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(canvas_size_list, "720p", "small")
    S.obs_property_list_add_string(canvas_size_list, "1080p", "medium")
    S.obs_property_set_visible(canvas_size_list, False)

    # Fonts
    S.obs_properties_add_font(props, "_away_player_font", "Away Player:")
    S.obs_properties_add_font(props, "_away_captain_font", "Away Captain:")
    S.obs_properties_add_font(props, "_away_score_font", "Away Score:")
    S.obs_properties_add_font(props, "_away_stars_font", "Away Stars:")

    S.obs_properties_add_font(props, "_home_player_font", "Home Player:")
    S.obs_properties_add_font(props, "_home_captain_font", "Home Captain:")
    S.obs_properties_add_font(props, "_home_score_font", "Home Score:")
    S.obs_properties_add_font(props, "_home_stars_font", "Home Stars:")

    S.obs_properties_add_font(props, "_inning_font", "Inning Font:")
    S.obs_properties_add_font(props, "_halfinning_font", "Halfinning Font:")

    S.obs_properties_add_font(props, "_chem_font", "Chem Font:")
    S.obs_properties_add_font(props, "_bases_font", "Bases Font:")

    S.obs_properties_add_font(props, "_count_font", "Count Font:")
    S.obs_properties_add_font(props, "_outs_font", "Outs Font:")

    S.obs_properties_add_font(props, "_star_chance_font", "Star Chance Font:")

    S.obs_property_set_visible(bool, False)
    S.obs_property_set_modified_callback(menu_list, menu_callback)

    return props


def menu_callback(props, prop, settings):
    # Return true is needed for the callback function to complete properly
    menu_list_selection = S.obs_data_get_string(settings, "_menu")
    print(menu_list_selection, "Selection update")

    # Location
    S.obs_property_set_visible(S.obs_properties_get(props, "_hslider"), menu_list_selection == "location")
    S.obs_property_set_visible(S.obs_properties_get(props, "_vslider"), menu_list_selection == "location")

    # Color
    S.obs_property_set_visible(S.obs_properties_get(props, "_scoreboard_base_color"), menu_list_selection == "color")

    # Stats
    S.obs_property_set_visible(S.obs_properties_get(props, "_pause_HUD"), menu_list_selection == "stats")

    # Canvas Size
    S.obs_property_set_visible(S.obs_properties_get(props, "_canvas_size"), menu_list_selection == "size")

    # Fonts
    S.obs_property_set_visible(S.obs_properties_get(props, "_away_player_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_away_captain_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_away_score_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_away_stars_font"), menu_list_selection == "fonts")

    S.obs_property_set_visible(S.obs_properties_get(props, "_home_player_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_home_captain_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_home_score_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_home_stars_font"), menu_list_selection == "fonts")

    S.obs_property_set_visible(S.obs_properties_get(props, "_inning_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_halfinning_font"), menu_list_selection == "fonts")

    S.obs_property_set_visible(S.obs_properties_get(props, "_chem_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_bases_font"), menu_list_selection == "fonts")

    S.obs_property_set_visible(S.obs_properties_get(props, "_count_font"), menu_list_selection == "fonts")
    S.obs_property_set_visible(S.obs_properties_get(props, "_outs_font"), menu_list_selection == "fonts")

    S.obs_property_set_visible(S.obs_properties_get(props, "_star_chance_font"), menu_list_selection == "fonts")
    return True
