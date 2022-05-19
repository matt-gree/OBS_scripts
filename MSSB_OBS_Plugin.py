import obspython as S
import os
import json
import platform as plt

symbol_font = S.obs_data_create()
S.obs_data_set_string(symbol_font, "face", "DejaVu Sans Mono")
S.obs_data_set_int(symbol_font, "flags", 1)
S.obs_data_set_int(symbol_font, "size", 32)

small_symbol_font = S.obs_data_create()
S.obs_data_set_string(small_symbol_font, "face", "DejaVu Sans Mono")
S.obs_data_set_int(small_symbol_font, "flags", 1)
S.obs_data_set_int(small_symbol_font, "size", 24)

smaller_font = S.obs_data_create()
S.obs_data_set_string(smaller_font, "face", "Trebuchet MS")
S.obs_data_set_int(smaller_font, "flags", 1)
S.obs_data_set_int(smaller_font, "size", 22)

default_font = S.obs_data_create()
S.obs_data_set_string(default_font, "face", "Trebuchet MS")
S.obs_data_set_int(default_font, "flags", 1)
S.obs_data_set_int(default_font, "size", 32)

away_player_font = S.obs_data_create()
S.obs_data_set_string(away_player_font, "face", "Trebuchet MS")
S.obs_data_set_int(away_player_font, "flags", 1)
S.obs_data_set_int(away_player_font, "size", 32)

home_player_font = S.obs_data_create()
S.obs_data_set_string(home_player_font, "face", "Trebuchet MS")
S.obs_data_set_int(home_player_font, "flags", 1)
S.obs_data_set_int(home_player_font, "size", 32)

captain_font = S.obs_data_create()
S.obs_data_set_string(captain_font, "face", "Trebuchet MS")
S.obs_data_set_int(captain_font, "flags", 1)
S.obs_data_set_int(captain_font, "size", 26)

#Windows only
chem_font = S.obs_data_create()
S.obs_data_set_string(chem_font, "face", "DejaVu Sans Mono")
S.obs_data_set_int(chem_font, "flags", 1)
S.obs_data_set_int(chem_font, "size", 36)


outline_color = 0xFFdddddd
inset_color = 0xFF302a28
star_chance_color = 0xFF2d9ac9

# Captain colors
mario_color = 0xFF0303ed
luigi_color = 0xFF148d14
yoshi_color = 0xFF35b238
birdo_color = 0xFFc364ec
peach_color = 0xFFc18eff
daisy_color = 0xFF217bf8
dk_color = 0xFF3764a0
diddy_color = 0xFF6ea4d8
wario_color = 0xFF00cce8
waluigi_color = 0xFF9e446e
bowser_color = 0xFF002202
bowserjr_color = 0xFF926625

canvas_height = 100
canvas_width = 100

# HUD Location Data
# Scoreboard was designed in 720p and converted to percentages for rescaling


def script_defaults(settings):
    S.obs_data_set_int(settings, "_scoreboard_base_color", outline_color)
    S.obs_data_set_string(settings, "_menu", "HUD Location")
    S.obs_data_set_bool(settings, "_pause_HUD", False)


    S.obs_data_set_obj(settings, "_inning_font", default_font)
    S.obs_data_set_obj(settings, "_halfinning_font", small_symbol_font)

    S.obs_data_set_obj(settings, "_away_player_font", away_player_font)
    S.obs_data_set_obj(settings, "_away_captain_font", captain_font)
    S.obs_data_set_obj(settings, "_away_score_font", default_font)
    S.obs_data_set_obj(settings, "_away_stars_font", symbol_font)

    S.obs_data_set_obj(settings, "_home_player_font", home_player_font)
    S.obs_data_set_obj(settings, "_home_captain_font", captain_font)
    S.obs_data_set_obj(settings, "_home_score_font", default_font)
    S.obs_data_set_obj(settings, "_home_stars_font", symbol_font)

    S.obs_data_set_obj(settings, "_chem_font", small_symbol_font)
    S.obs_data_set_obj(settings, "_bases_font", symbol_font)

    S.obs_data_set_obj(settings, "_count_font", default_font)
    S.obs_data_set_obj(settings, "_outs_font", small_symbol_font)

    S.obs_data_set_obj(settings, "_star_chance_font", default_font)

    S.obs_data_set_string(settings, "_canvas_resolution", "medium")
    
class HUD:
    def __init__(self):
        # set the intitial position of to be 0,0
        pos = S.vec2()
        self.location = pos
        self.location.x = 0
        self.location.y = 0

        self.current_event_num = -1

        # HUD values
        self.inning = 0
        self.halfinning = 0
        self.balls = 0
        self.strikes = 0
        self.outs = 0

        self.awayplayer = 0
        self.awaycaptain = 0
        self.awayscore = 0
        self.awaystars = 0

        self.homeplayer = 0
        self.homecaptain = 0
        self.homescore = 0
        self.homestars = 0

        self.runner_1b = 0
        self.runner_2b = 0
        self.runner_3b = 0
        self.chem = 0
        self.star_chance = 0

        self.canvas_width = 0
        self.canvas_height = 0

        self.scoreboard_base_height = 0
        self.scoreboard_padding = 0
        self.all_inset_heights = 0
        self.player_base_width = 0
        self.inning_base_width = 0
        self.bases_base_width = 0
        self.count_base_width = 0

        self.scoreboard_base_width = 0

        self.away_base_xlocation = 0
        self.home_base_xlocation = 0
        self.inning_base_xlocation = 0
        self.bases_base_xlocation = 0
        self.count_base_xlocation = 0

        self.max_font_size = 0
        self.platform = None

    def location_assignment(self):

        canvas_resolution = S.obs_data_get_string(globalsettings, "_canvas_size")

        if canvas_resolution == "small":
            self.canvas_width = 1280
            self.canvas_height = 720
        elif canvas_resolution == "medium":
            self.canvas_width = 1920
            self.canvas_height = 1080

        self.scoreboard_base_height = int(self.canvas_height * (80 / 720))
        self.scoreboard_padding = int(self.canvas_width * (5 / 1280))

        self.all_inset_heights = int(self.scoreboard_base_height - 2 * self.scoreboard_padding)
        self.player_base_width = int(self.canvas_width * (200 / 1280))
        self.inning_base_width = int(self.canvas_width * (45 / 1280))
        self.bases_base_width = int(self.canvas_width * (55 / 1280))
        self.count_base_width = int(self.canvas_width * (80 / 1280))

        self.scoreboard_base_width = int(2 * self.player_base_width + self.inning_base_width + self.bases_base_width + self.count_base_width + 6 * self.scoreboard_padding)

        self.away_base_xlocation = self.scoreboard_padding
        self.home_base_xlocation = self.scoreboard_padding + self.player_base_width + self.away_base_xlocation
        self.inning_base_xlocation = self.scoreboard_padding + self.player_base_width + self.home_base_xlocation
        self.bases_base_xlocation = self.scoreboard_padding + self.inning_base_width + self.inning_base_xlocation
        self.count_base_xlocation = self.scoreboard_padding + self.bases_base_width + self.bases_base_xlocation

    def create_HUD(self):

        if str(graphics.canvas_height) == "720":
            S.obs_data_set_int(symbol_font, "size", 32)

            S.obs_data_set_int(small_symbol_font, "size", 20)

            S.obs_data_set_int(smaller_font, "size", 22)

            S.obs_data_set_int(default_font, "size", 32)

            S.obs_data_set_int(away_player_font, "size", 32)

            S.obs_data_set_int(home_player_font, "size", 32)

            S.obs_data_set_int(captain_font, "size", 26)

            S.obs_data_set_int(chem_font, "size", 24)

            self.max_font_size = 32

        elif str(graphics.canvas_height) == "1080":
            S.obs_data_set_int(symbol_font, "size", int(32 * 1.5))

            S.obs_data_set_int(small_symbol_font, "size", int(20 * 1.5))

            S.obs_data_set_int(smaller_font, "size", int(22 * 1.5))

            S.obs_data_set_int(default_font, "size", int(32 * 1.5))

            S.obs_data_set_int(away_player_font, "size", int(32 * 1.5))

            S.obs_data_set_int(home_player_font, "size", int(32 * 1.5))

            S.obs_data_set_int(captain_font, "size", int(26 * 1.5))

            S.obs_data_set_int(chem_font, "size", int(24 * 1.5))

            self.max_font_size = 48

        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)

        if str(plt.platform()).lower()[0] == 'm':
            self.platform = 'MacOS'
        elif str(plt.platform()).lower()[0] == 'w':
            self.platform = 'Windows'
        else:
            self.platform = 'Unknown'

        group = S.obs_scene_add_group(scene, "HUD")

        # HUD Text Boxes
        # Scene add must be called immediately after to avoid OBS crash
        # Crash issue was probably caused by not making a new settings every source
        # Text boxes with symbols must be made to gdi+ sources on Windows
        # Other if statements should probably be removed

        # Inning
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Inning_Text = S.obs_source_create("text_ft2_source", 'inning_text', settings, None)
        else:
            Inning_Text = S.obs_source_create("text_ft2_source", 'inning_text', settings, None)
        S.obs_scene_add(scene, Inning_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "inning_text"))

        # Halfinning
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Halfinning_Text = S.obs_source_create("text_ft2_source", 'halfinning_text', settings, None)
        else:
            Halfinning_Text = S.obs_source_create("text_gdiplus", 'halfinning_text', settings, None)
        S.obs_scene_add(scene, Halfinning_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "halfinning_text"))

        # Count
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Count_Text = S.obs_source_create("text_ft2_source", 'count_text', settings, None)
        else:
            Count_Text = S.obs_source_create("text_ft2_source", 'count_text', settings, None)
        S.obs_scene_add(scene, Count_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "count_text"))

        # Outs
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Outs_Text = S.obs_source_create("text_ft2_source", 'outs_text', settings, None)
        else:
            Outs_Text = S.obs_source_create("text_gdiplus", 'outs_text', settings, None)
        S.obs_scene_add(scene, Outs_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "outs_text"))

        # Away Player Name
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Away_Player_Text = S.obs_source_create("text_ft2_source", 'away_player_text', settings, None)
        else:
            Away_Player_Text = S.obs_source_create("text_ft2_source", 'away_player_text', settings, None)
        S.obs_scene_add(scene, Away_Player_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_player_text"))

        # Away Captain
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Away_Captain_Text = S.obs_source_create("text_ft2_source", 'away_captain_text', settings, None)
        else:
            Away_Captain_Text = S.obs_source_create("text_ft2_source", 'away_captain_text', settings, None)
        S.obs_scene_add(scene, Away_Captain_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_captain_text"))

        # Away Score
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Away_Score_Text = S.obs_source_create("text_ft2_source", 'away_score_text', settings, None)
        else:
            Away_Score_Text = S.obs_source_create("text_ft2_source", 'away_score_text', settings, None)
        S.obs_scene_add(scene, Away_Score_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_score_text"))

        # Away Stars
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Away_Stars_Text = S.obs_source_create("text_ft2_source", 'away_stars_text', settings, None)
        else:
            Away_Stars_Text = S.obs_source_create("text_gdiplus", 'away_stars_text', settings, None)
        S.obs_scene_add(scene, Away_Stars_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_stars_text"))

        # Home Player Name
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Home_Player_Text = S.obs_source_create("text_ft2_source", 'home_player_text', settings, None)
        else:
            Home_Player_Text = S.obs_source_create("text_ft2_source", 'home_player_text', settings, None)
        S.obs_scene_add(scene, Home_Player_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_player_text"))

        # Home Captain
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Home_Captain_Text = S.obs_source_create("text_ft2_source", 'home_captain_text', settings, None)
        else:
            Home_Captain_Text = S.obs_source_create("text_ft2_source", 'home_captain_text', settings, None)
        S.obs_scene_add(scene, Home_Captain_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_captain_text"))

        # Home Score
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Home_Score_Text = S.obs_source_create("text_ft2_source", 'home_score_text', settings, None)
        else:
            Home_Score_Text = S.obs_source_create("text_ft2_source", 'home_score_text', settings, None)
        S.obs_scene_add(scene, Home_Score_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_score_text"))

        # Home Stars
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Home_Stars_Text = S.obs_source_create("text_ft2_source", 'home_stars_text', settings, None)
        else:
            Home_Stars_Text = S.obs_source_create("text_gdiplus", 'home_stars_text', settings, None)
        S.obs_scene_add(scene, Home_Stars_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_stars_text"))

        # 1st Base
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Runner_1b_Text = S.obs_source_create("text_ft2_source", 'runner_1b_text', settings, None)
        else:
            Runner_1b_Text = S.obs_source_create("text_gdiplus", 'runner_1b_text', settings, None)
        S.obs_scene_add(scene, Runner_1b_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "runner_1b_text"))

        # 2nd Base
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Runner_2b_Text = S.obs_source_create("text_ft2_source", 'runner_2b_text', settings, None)
        else:
            Runner_2b_Text = S.obs_source_create("text_gdiplus", 'runner_2b_text', settings, None)
        S.obs_scene_add(scene, Runner_2b_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "runner_2b_text"))

        # 3rd Base
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Runner_3b_Text = S.obs_source_create("text_ft2_source", 'runner_3b_text', settings, None)
        else:
            Runner_3b_Text = S.obs_source_create("text_gdiplus", 'runner_3b_text', settings, None)
        S.obs_scene_add(scene, Runner_3b_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "runner_3b_text"))

        # Chem
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Chem_Text = S.obs_source_create("text_ft2_source", 'chem_text', settings, None)
        else:
            Chem_Text = S.obs_source_create("text_gdiplus", 'chem_text', settings, None)
        S.obs_scene_add(scene, Chem_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "chem_text"))

        # Star Chance
        settings = S.obs_data_create()
        if self.platform == 'MacOS':
            Star_Chance_Text = S.obs_source_create("text_ft2_source", 'star_chance_text', settings, None)
        else:
            Star_Chance_Text = S.obs_source_create("text_ft2_source", 'star_chance_text', settings, None)
        S.obs_scene_add(scene, Star_Chance_Text)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "star_chance_text"))

        # HUD Graphics
        # Away
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.player_base_width)
        S.obs_data_set_int(settings, "height", self.all_inset_heights)
        S.obs_data_set_int(settings, "color", inset_color)
        scoreboard_base = S.obs_source_create("color_source", 'away_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "away_base"))
        position = S.vec2()
        S.vec2_set(position, self.away_base_xlocation, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_base'), position)

        # Home
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.player_base_width)
        S.obs_data_set_int(settings, "height", self.all_inset_heights)
        S.obs_data_set_int(settings, "color", inset_color)
        scoreboard_base = S.obs_source_create("color_source", 'home_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "home_base"))
        position = S.vec2()
        S.vec2_set(position, self.home_base_xlocation, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_base'), position)

        # Inning
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.inning_base_width)
        S.obs_data_set_int(settings, "height", self.all_inset_heights)
        S.obs_data_set_int(settings, "color", inset_color)
        scoreboard_base = S.obs_source_create("color_source", 'inning_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "inning_base"))
        position = S.vec2()
        S.vec2_set(position, self.inning_base_xlocation, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'inning_base'), position)

        # Bases
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.bases_base_width)
        S.obs_data_set_int(settings, "height", self.all_inset_heights)
        S.obs_data_set_int(settings, "color", inset_color)
        scoreboard_base = S.obs_source_create("color_source", 'bases_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "bases_base"))
        position = S.vec2()
        S.vec2_set(position, self.bases_base_xlocation, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'bases_base'), position)

        # Count
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.count_base_width)
        S.obs_data_set_int(settings, "height", self.all_inset_heights)
        S.obs_data_set_int(settings, "color", inset_color)
        scoreboard_base = S.obs_source_create("color_source", 'count_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "count_base"))
        position = S.vec2()
        S.vec2_set(position, self.count_base_xlocation, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'count_base'), position)

        # Base
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.scoreboard_base_width)
        S.obs_data_set_int(settings, "height", self.scoreboard_base_height)
        S.obs_data_set_int(settings, "color", outline_color)
        scoreboard_base = S.obs_source_create("color_source", 'scoreboard_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "scoreboard_base"))

        # Star Chance Inset
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.player_base_width)
        S.obs_data_set_int(settings, "height", S.obs_data_get_int(default_font, "size")+self.scoreboard_padding)
        S.obs_data_set_int(settings, "color", star_chance_color)
        scoreboard_base = S.obs_source_create("color_source", 'star_chance_inset', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "star_chance_inset"))
        position = S.vec2()
        S.vec2_set(position, self.scoreboard_base_width, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'star_chance_inset'), position)

        # Star Chance Base
        settings = S.obs_data_create()
        S.obs_data_set_int(settings, "width", self.player_base_width + 2*self.scoreboard_padding)
        S.obs_data_set_int(settings, "height", S.obs_data_get_int(default_font, "size") + 3*self.scoreboard_padding)
        S.obs_data_set_int(settings, "color", outline_color)
        scoreboard_base = S.obs_source_create("color_source", 'star_chance_base', settings, None)
        S.obs_scene_add(scene, scoreboard_base)
        S.obs_sceneitem_group_add_item(group, S.obs_scene_find_source(scene, "star_chance_base"))
        position = S.vec2()
        S.vec2_set(position, self.scoreboard_base_width - self.scoreboard_padding, 0)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'star_chance_base'), position)

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
            S.vec2_set(position, self.inning_base_xlocation + ((self.inning_base_width - S.obs_source_get_width(S.obs_get_source_by_name("halfinning_text")))/2), self.scoreboard_padding)
            S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'halfinning_text'), position)
        else:
            halfinning_string = "▼"
            position = S.vec2()
            S.vec2_zero(position)
            S.vec2_set(position, self.inning_base_xlocation + ((self.inning_base_width - S.obs_source_get_width(S.obs_get_source_by_name("halfinning_text")))/2), ((self.scoreboard_base_height - 2*self.scoreboard_padding) - S.obs_source_get_height(S.obs_get_source_by_name("halfinning_text"))))
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
        S.obs_data_set_string(settings, "text", str("★:" + str(self.awaystars)))
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
        S.obs_data_set_string(settings, "text", str("★:" + str(self.homestars)))
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
            S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(scene, 'star_chance_base'), True)
            S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(scene, 'star_chance_inset'), True)
        else:
            star_chance_string = ""
            S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(scene, 'star_chance_base'), False)
            S.obs_sceneitem_set_visible(S.obs_scene_find_source_recursive(scene, 'star_chance_inset'), False)
        S.obs_data_set_string(settings, "text", star_chance_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)

    def stats_dependent_update(self):
        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)

        # Used for player name font size, and for updating the inning centered position
        # This function does not work when decreasing the length, but this error should never come up
        single_digit_width = int(S.obs_data_get_int(default_font, "size") * (19 / 32))  # Default for Trebuchet MS font
        print(len(str(self.inning)))
        if len(str(self.inning)) == 1:
            single_digit_width = S.obs_source_get_width(S.obs_get_source_by_name("inning_text"))

        if self.platform != "MacOS":
            S.obs_data_set_obj(globalsettings, "_chem_font", chem_font)

        # Text Resizing
        if len(str(self.awayplayer)) != 0:
            player_name_max_width = self.player_base_width - 3 * self.scoreboard_padding - 2 * single_digit_width
            print(player_name_max_width, "max_width")
            print(len(str(self.awayplayer)), "length")
            average_character_width = S.obs_data_get_int(default_font, "size") * (
                0.68)  # This was determined through testing
            for i in range(0, self.max_font_size + 1):
                if len(str(self.awayplayer)) * i * 0.55 > player_name_max_width:
                    i + 1
                    break
            print(i, "font")
            S.obs_data_set_int(away_player_font, "size", i)

        if len(str(self.homeplayer)) != 0:
            for i in range(0, self.max_font_size + 1):
                if len(str(self.homeplayer)) * i * 0.55 > player_name_max_width:
                    i + 1
                    break
            print(i, "home font")
            S.obs_data_set_int(home_player_font, "size", i)

        # Fonts
        source = S.obs_get_source_by_name("away_player_text")
        S.obs_data_set_obj(globalsettings, "font", away_player_font)
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("away_captain_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_away_captain_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("away_score_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_away_score_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("away_stars_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_away_stars_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("home_player_text")
        S.obs_data_set_obj(globalsettings, "font", home_player_font)
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("home_captain_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_home_captain_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("home_score_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_home_score_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("home_stars_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_home_stars_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("inning_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_inning_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("halfinning_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_halfinning_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("chem_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_chem_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("runner_1b_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_bases_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("runner_2b_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_bases_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("runner_3b_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_bases_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("count_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_count_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("outs_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_outs_font"))
        S.obs_source_update(source, globalsettings)

        source = S.obs_get_source_by_name("star_chance_text")
        S.obs_data_set_obj(globalsettings, "font", S.obs_data_get_obj(globalsettings, "_star_chance_font"))
        S.obs_source_update(source, globalsettings)

        # Updates graphics features that chance based on the stats files
        # Captain Base Color Update
        settings = S.obs_data_create()
        source = S.obs_get_source_by_name("away_base")
        S.obs_data_set_int(settings, "color", self.home_away_color(str(self.awaycaptain)))
        S.obs_source_update(source, settings)

        settings = S.obs_data_create()
        source = S.obs_get_source_by_name("home_base")
        S.obs_data_set_int(settings, "color", self.home_away_color(str(self.homecaptain)))
        S.obs_source_update(source, settings)

        # Text Locations
        # Text sources using gdi+ on windows must be allgined different than others
        # Away Player (Constant Location)
        position = S.vec2()
        S.vec2_zero(position)
        S.vec2_set(position, 2 * self.scoreboard_padding, self.scoreboard_padding + self.max_font_size/2 - S.obs_data_get_int(away_player_font, "size")/2)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_player_text'), position)

        # Away Captain (Constant Location)
        S.vec2_zero(position)
        S.vec2_set(position, 2 * self.scoreboard_padding, self.scoreboard_base_height -  S.obs_data_get_int(captain_font, "size") - 2*self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_captain_text'), position)

        # Away Score (Variable Location)
        S.vec2_zero(position)
        S.vec2_set(position, self.home_base_xlocation - 2 * self.scoreboard_padding - len(str(self.awayscore))*single_digit_width , self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_score_text'), position)

        # Away Stars (Variable Location)
        S.vec2_zero(position)
        if self.platform == 'MacOS':
            S.vec2_set(position, self.home_base_xlocation - 2 * self.scoreboard_padding - S.obs_source_get_width(S.obs_get_source_by_name("away_stars_text")), self.scoreboard_base_height -  S.obs_data_get_int(symbol_font, "size") - 2 * self.scoreboard_padding)
        else:
            S.vec2_set(position, self.home_base_xlocation - 2 * self.scoreboard_padding - S.obs_source_get_width(S.obs_get_source_by_name("away_stars_text")), self.scoreboard_base_height - S.obs_data_get_int(symbol_font, "size") - self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'away_stars_text'), position)

        # Home Player (Constant Location)
        S.vec2_zero(position)
        S.vec2_set(position, self.home_base_xlocation + self.scoreboard_padding, self.scoreboard_padding + self.max_font_size/2 - S.obs_data_get_int(home_player_font, "size")/2)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_player_text'), position)

        # Home Captain (Constant Location)
        S.vec2_zero(position)
        S.vec2_set(position, self.scoreboard_padding + self.home_base_xlocation, self.scoreboard_base_height -  S.obs_data_get_int(captain_font, "size") - 2 * self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_captain_text'), position)

        # Home Score (Variable Location)
        S.vec2_zero(position)
        S.vec2_set(position, self.inning_base_xlocation - 2 * self.scoreboard_padding - len(str(self.homescore)) * single_digit_width, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_score_text'), position)

        # Home Stars (Variable Location)
        S.vec2_zero(position)
        if self.platform == 'MacOS':
            S.vec2_set(position, self.inning_base_xlocation - 2 * self.scoreboard_padding - S.obs_source_get_width(S.obs_get_source_by_name("home_stars_text")), self.scoreboard_base_height -  S.obs_data_get_int(symbol_font, "size") - 2 * self.scoreboard_padding)
        else:
            S.vec2_set(position, self.inning_base_xlocation - 2 * self.scoreboard_padding - S.obs_source_get_width(S.obs_get_source_by_name("home_stars_text")), self.scoreboard_base_height - S.obs_data_get_int(symbol_font, "size") - self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'home_stars_text'), position)

        inning_centered_location = self.inning_base_xlocation + (self.inning_base_width - (len(str(self.inning)) * single_digit_width))/2

        # Inning (Centered Location) Font size is used rather than get_height since it is more accurate
        position = S.vec2()
        S.vec2_set(position, inning_centered_location, ((self.scoreboard_base_height - 2*self.scoreboard_padding) - S.obs_data_get_int(default_font, "size") - (S.obs_data_get_int(default_font, "size")/2)))
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'inning_text'), position)

        # Halfinning (Centered Location) Position is handled above
        # S.vec2_zero(position)
        # S.vec2_set(position, inning_base_xlocation + ((inning_base_width - S.obs_source_get_width(S.obs_get_source_by_name("halfinning_text")))/2), scoreboard_padding)
        # S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'halfinning_text'), position)

        # 2nd Base (Centered Location)
        S.vec2_zero(position)
        if self.platform == 'MacOS':
            S.vec2_set(position, self.bases_base_xlocation+((self.bases_base_width - S.obs_source_get_width(S.obs_get_source_by_name("runner_2b_text")))/2), 0)
        else:
            S.vec2_set(position, self.bases_base_xlocation + ((self.bases_base_width - S.obs_source_get_width(S.obs_get_source_by_name("runner_2b_text"))) / 2), self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'runner_2b_text'), position)

        # 1st Base (Off-Centered Location)
        S.vec2_zero(position)
        if self.platform == 'MacOS':
            S.vec2_set(position, self.bases_base_xlocation+((self.bases_base_width - S.obs_source_get_width(S.obs_get_source_by_name("runner_2b_text")))/2) + (S.obs_source_get_width(S.obs_get_source_by_name("runner_1b_text"))/1.6), S.obs_source_get_width(S.obs_get_source_by_name("runner_1b_text"))/1.6)
        else:
            S.vec2_set(position, self.bases_base_xlocation + ((self.bases_base_width - S.obs_source_get_width(S.obs_get_source_by_name("runner_2b_text"))) / 2) + (S.obs_source_get_width(S.obs_get_source_by_name("runner_1b_text")) / 1.6), self.scoreboard_padding + S.obs_source_get_width(S.obs_get_source_by_name("runner_1b_text")) / 1.6)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'runner_1b_text'), position)

        # 3rd Base (Off-Centered Location)
        S.vec2_zero(position)
        if self.platform == 'MacOS':
            S.vec2_set(position, self.bases_base_xlocation+((self.bases_base_width - S.obs_source_get_width(S.obs_get_source_by_name("runner_2b_text")))/2) - (S.obs_source_get_width(S.obs_get_source_by_name("runner_1b_text"))/1.6), S.obs_source_get_width(S.obs_get_source_by_name("runner_3b_text"))/1.6)
        else:
            S.vec2_set(position, self.bases_base_xlocation + ((self.bases_base_width - S.obs_source_get_width(S.obs_get_source_by_name("runner_2b_text"))) / 2) - (S.obs_source_get_width(S.obs_get_source_by_name("runner_1b_text")) / 1.6), self.scoreboard_padding + S.obs_source_get_width(S.obs_get_source_by_name("runner_3b_text")) / 1.6)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'runner_3b_text'), position)

        # Chem (Centered Location)
        S.vec2_zero(position)
        S.vec2_set(position, self.bases_base_xlocation + ((self.bases_base_width - S.obs_source_get_width(S.obs_get_source_by_name("chem_text")))/2), self.scoreboard_base_height - S.obs_data_get_int(smaller_font, "size") - 2.5 * self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'chem_text'), position)

        # Outs (Centered Location)
        S.vec2_zero(position)
        if self.platform == 'MacOS':
            S.vec2_set(position, self.count_base_xlocation + ((self.count_base_width - S.obs_source_get_width(S.obs_get_source_by_name("outs_text")))/2), self.scoreboard_base_height - S.obs_data_get_int(symbol_font, "size")- self.scoreboard_padding)
        else:
            S.vec2_set(position, self.count_base_xlocation + ((self.count_base_width - S.obs_source_get_width(S.obs_get_source_by_name("outs_text"))) / 2), self.scoreboard_base_height - S.obs_data_get_int(symbol_font, "size"))
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'outs_text'), position)

        # Count (Centered Location)
        S.vec2_zero(position)
        S.vec2_set(position, self.count_base_xlocation + ((self.count_base_width - S.obs_source_get_width(S.obs_get_source_by_name("count_text")))/2), 2 * self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'count_text'), position)

        # Star Chance (Constant Location)
        S.vec2_zero(position)
        S.vec2_set(position, self.scoreboard_base_width+self.scoreboard_padding, self.scoreboard_padding)
        S.obs_sceneitem_set_pos(S.obs_scene_find_source_recursive(scene, 'star_chance_text'), position)


    def dir_scan(self):

        hud_file_path = S.obs_data_get_string(globalsettings, "_path")
        if not os.path.isfile(hud_file_path):
            return ""

        with open(hud_file_path) as f:
            hud_data = json.load(f)

        # Return if the event hasn't changed
        if (self.current_event_num == hud_data['Event Num']):
            return self.current_event_num

        print("New HUD:", self.current_event_num, hud_data['Event Num'])
        self.current_event_num = hud_data['Event Num']

        print(S.obs_source_get_width(S.obs_get_source_by_name("count_text")))

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
        if str(hud_data['Half Inning']) == "0":
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
        if hud_data['Star Chance']:
            self.star_chance = "1"
        else:
            self.star_chance = "0"

        self.update_text()
        self.stats_dependent_update()



    # Previous Event info
    # First check if previous event exists and had contact
    # if (hud_data.get('Previous Event')):
    #    if (hud_data.get('Pitch') and hud_data.get('Contact')):
    #        contact_output_file = os.path.join(output_dir, 'contact.txt')
    #        with open(contact_output_file, 'w', encoding="utf-8") as f:

    def home_away_color(self, home_or_away_captain):
        if home_or_away_captain == "Mario":
            return mario_color
        if home_or_away_captain == "Luigi":
            return luigi_color
        if home_or_away_captain == "Peach":
            return peach_color
        if home_or_away_captain == "Daisy":
            return daisy_color
        if home_or_away_captain == "Yoshi":
            return yoshi_color
        if home_or_away_captain == "Birdo":
            return birdo_color
        if home_or_away_captain == "Yoshi":
            return yoshi_color
        if home_or_away_captain == "Wario":
            return wario_color
        if home_or_away_captain == "Waluigi":
            return waluigi_color
        if home_or_away_captain == "DK":
            return dk_color
        if home_or_away_captain == "Diddy":
            return diddy_color
        if home_or_away_captain == "Bowser":
            return bowser_color
        if home_or_away_captain == "Bowser Jr":
            return bowserjr_color
        return inset_color

def script_load(settings):
    global pause_HUD_bool
    pause_HUD_bool = False
    global graphics
    graphics = HUD()

def script_tick(seconds):
    if pause_HUD_bool == False:
        graphics.dir_scan()

def script_update(settings):
    global globalsettings
    globalsettings = settings
    current_scene = S.obs_frontend_get_current_scene()
    scene = S.obs_scene_from_source(current_scene)

    graphics.location_assignment()

    # Pause HUD
    global pause_HUD_bool
    pause_HUD_bool = S.obs_data_get_bool(settings, "_pause_HUD")

    #Real Time position update
    hpositionslider = S.obs_data_get_int(settings, "_hslider")
    vpositionslider = S.obs_data_get_int(settings, "_vslider")
    HUD_Group = S.obs_scene_find_source(scene, "HUD")
    position = S.vec2()
    S.vec2_set(position, int(((graphics.canvas_width - graphics.scoreboard_base_width) * (hpositionslider / 1000))), int(((graphics.canvas_height - graphics.scoreboard_base_height) * (vpositionslider / 1000))))
    S.obs_sceneitem_set_pos(HUD_Group, position)

    # Color Update
    source = S.obs_get_source_by_name("scoreboard_base")
    scoreboard_base_color = S.obs_data_get_int(settings, "_scoreboard_base_color")
    S.obs_data_set_int(settings, "color", scoreboard_base_color)
    S.obs_source_update(source, settings)

def add_pressed(props, prop):
    graphics.create_HUD()
    graphics.update_text()
    graphics.stats_dependent_update()
    graphics.update_text()
    graphics.stats_dependent_update()

def refresh_pressed(props, prop):
    graphics.update_text()
    graphics.stats_dependent_update()
    print(S.obs_source_get_width(S.obs_get_source_by_name("inning_text")))

def remove_pressed(props, prop):
    S.obs_source_remove(S.obs_get_source_by_name("HUD"))

def script_description():
    return "Custom Mario Baseball Game HUD \nOBS interface by MattGree \nThanks to PeacockSlayer (and Rio Dev team) for developing the HUD files  \nDonations are welcomed!"


def script_properties():  # ui
    props = S.obs_properties_create()

    # Main menuing list
    menu_list = S.obs_properties_add_list(props, "_menu", "Choose", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(menu_list, "HUD Location", "location")
    S.obs_property_list_add_string(menu_list, "Colors", "color")
    S.obs_property_list_add_string(menu_list, "Stats", "stats")
    S.obs_property_list_add_string(menu_list, "Canvas Size", "size")
    #S.obs_property_list_add_string(menu_list, "Fonts", "fonts")

    # Location Properties
    S.obs_properties_add_button(props, "button", "Add HUD", add_pressed)
    S.obs_properties_add_button(props, "refreshbutton", "Refresh HUD", refresh_pressed)
    S.obs_properties_add_button(props, "removebutton", "Remove HUD", remove_pressed)
    S.obs_properties_add_int_slider(props, "_hslider", "X Location", 0, 1000, 1)
    S.obs_properties_add_int_slider(props, "_vslider", "Y Location", 0, 1000, 1)
    bool = S.obs_properties_add_bool(props, "_bool", "_bool:")

    # Color
    S.obs_properties_add_color(props, "_scoreboard_base_color", "Scoreboard Base")

    # Stats
    S.obs_properties_add_bool(props, "_pause_HUD", "Pause HUD")
    OS_list = S.obs_properties_add_list(props, "_OS_list", "OS:", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(OS_list, "Custom", "custom")
    S.obs_property_list_add_string(OS_list, "Windows", "windows")
    S.obs_property_list_add_string(OS_list, "MacOS", "macOS")
    S.obs_properties_add_text(props, "_path", "Path to HUD json:", S.OBS_TEXT_DEFAULT)

    # Canvas Size Properties
    canvas_size_list = S.obs_properties_add_list(props, "_canvas_size", "Resolution", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
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
    S.obs_property_set_visible(S.obs_properties_get(props, "_OS_list"), menu_list_selection == "stats")
    S.obs_property_set_visible(S.obs_properties_get(props, "_path"), menu_list_selection == "stats")

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
