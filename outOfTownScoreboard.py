import obspython as S
import json
import time
import math

class scoreboard:
    def __init__(self):
        self.ongoingGames_all = {}
        self.ongoingGames_inTimeRange = []
        self.live_text = "test"

    def get_live_games(self, timeRange):
        #to do: make API call
        ongoingGames_json = json.load(open('C:/Users/nlann/Documents/Project Rio/ongoingGamesExample.json'))
        self.ongoingGames_all = ongoingGames_json["ongoing_games"]
        print(time.asctime(time.gmtime(math.floor(timeRange))))

        self.ongoingGames_previous = self.ongoingGames_inTimeRange
        self.ongoingGames_inTimeRange = []
        for game in self.ongoingGames_all:
            if game['start_time'] > timeRange:
                self.ongoingGames_inTimeRange.append(game)
        print(self.ongoingGames_inTimeRange[-1])
        print(len(self.ongoingGames_inTimeRange))

        #to do: check if live games are stale and mark them somehow
        #to do: track if a game just dissappeared, meaning the game just finished
        #to do: exclude game from current HUD file.

    def live_game_fomatting(self, gameIndex):
        gameInfo = self.ongoingGames_inTimeRange[gameIndex]
        self.live_h_player = gameInfo["home_player"]
        self.live_a_player = gameInfo["away_player"]
        nameLength = max(len(self.live_a_player), len(self.live_h_player))

        self.live_h_score = gameInfo["home_score"]
        self.live_a_score = gameInfo["away_score"]

        self.live_inning = gameInfo["inning"]
        self.live_halfInning = gameInfo["half_inning"]
        halfInnChar = "↑" if self.live_halfInning == 0 else "↓"

        self.live_outs = gameInfo["outs"]
        if self.live_outs == 0:
            outsString = "○○○"
        elif self.live_outs == 1:
            outsString = "●○○"
        elif self.live_outs >= 2:
            outsString = "●●○"
        else:
            outsString = ""

        self.live_gameMode = "Stars Off, Season 5"

        self.live_pitcherID = gameInfo["pitcher"]
        if self.live_halfInning == 0:
            self.live_pitcherName = gameInfo[f"home_roster_{self.live_pitcherID}_char"]
            pitcherString = "P " + str(self.live_pitcherName)
            pitcherString = "P Boo"
            batterString = "B Toad(R)"

        liveString = self.live_gameMode.ljust(30," ") + "\n" + \
            self.live_a_player.ljust(nameLength," ") + " " + str(self.live_a_score).ljust(3," ") + batterString + "\n" + \
            self.live_h_player.ljust(nameLength," ") + " " + str(self.live_h_score).ljust(3," ") + pitcherString + "\n" + \
            str(self.live_inning) + str(halfInnChar).ljust(15, " ") + outsString 
        return liveString

    def update_displays(self):
        display1_source = S.obs_get_source_by_name("display1")
        if display1_source is not None:
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "text", self.live_game_fomatting(-1))
            S.obs_source_update(display1_source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(display1_source)

def toggle_display_pressed(props, prop):
    current_scene = S.obs_frontend_get_current_scene()
    sb.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    display1 = S.obs_scene_find_source(sb.scene,'display1')

    if display1 is None: #source doesn't exist, so create
        settings = S.obs_data_create()
        #if sb.platform == 'MacOS':
        #    display1 = S.obs_source_create("text_ft2_source", 'display1', settings, None)
        #else:
        display1 = S.obs_source_create("text_gdiplus", 'display1', settings, None)
        S.obs_scene_add(sb.scene, display1)
        S.obs_source_release(display1)
        S.obs_data_release(settings)
    else: #source exists, so delete
        S.obs_sceneitem_remove(display1)


def script_load(settings):

    S.timer_add(check_for_updates, 2000)

    global globalsettings
    globalsettings = settings

    global sb
    sb = scoreboard()

def check_for_updates():
    if pause_bool == False:
        sb.get_live_games(time.time()-60*60*24*10)
        sb.update_displays()

def script_update(settings):
    current_scene = S.obs_frontend_get_current_scene()
    scoreboard.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    global globalsettings
    globalsettings = settings

    global pause_bool
    pause_bool = S.obs_data_get_bool(settings, "_pause")

def script_description():
    return "test"

def script_properties():
    props = S.obs_properties_create()

    S.obs_properties_add_bool(props, "_pause", "Pause")
    
    S.obs_properties_add_button(props, "_toggleDisplayButton", "Toggle Display", toggle_display_pressed)

    return props
