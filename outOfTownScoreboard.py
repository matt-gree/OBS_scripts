import obspython as S
import json
import time
import math
from urllib.request import urlopen

charMapping = {
    0: "Mario",
    1: "Luigi",
    2: "DK",
    3: "Diddy",
    4: "Peach",
    5: "Daisy",
    6: "Yoshi",
    7: "Baby Mario",
    8: "Baby Luigi",
    9: "Bowser",
    10: "Wario",
    11: "Waluigi",
    12: "Koopa(G)",
    13: "Toad(R)",
    14: "Boo",
    15: "Toadette",
    16: "Shy Guy(R)",
    17: "Birdo",
    18: "Monty",
    19: "Bowser Jr",
    20: "Paratroopa(R)",
    21: "Pianta(B)",
    22: "Pianta(R)",
    23: "Pianta(Y)",
    24: "Noki(B)",
    25: "Noki(R)",
    26: "Noki(G)",
    27: "Bro(H)",
    28: "Toadsworth",
    29: "Toad(B)",
    30: "Toad(Y)",
    31: "Toad(G)",
    32: "Toad(P)",
    33: "Magikoopa(B)",
    34: "Magikoopa(R)",
    35: "Magikoopa(G)",
    36: "Magikoopa(Y)",
    37: "King Boo",
    38: "Petey",
    39: "Dixie",
    40: "Goomba",
    41: "Paragoomba",
    42: "Koopa(R)",
    43: "Paratroopa(G)",
    44: "Shy Guy(B)",
    45: "Shy Guy(Y)",
    46: "Shy Guy(G)",
    47: "Shy Guy(Bk)",
    48: "Dry Bones(Gy)",
    49: "Dry Bones(G)",
    50: "Dry Bones(R)",
    51: "Dry Bones(B)",
    52: "Bro(F)",
    53: "Bro(B)",
    None: "None"
}

modeMapping = {
    10: "Stars On, S5",
    11: "Stars Off, S5",
    12: "Big Balla, S5"
}

stadMapping = {
    0: "Mario Stadium",
    1: "Bowser Castle",
    2: "Wario Palace",
    3: "Yoshi Park",
    4: "Peach Garden",
    5: "DK Jungle"
}
class displayStruct:
    def __init__(self, gType, gIndex, displayTime):
        self.gameType = gType
        self.gameIndex = gIndex
        self.displayStartTime = displayTime

class scoreboard:
    def __init__(self):
        self.liveGames_all = {}
        self.liveGames_inTimeRange = []

        self.time_gotLiveGames = 0
        self.time_gotRecentGames = 0

        self.live_gameInd = True #if there is a live game occuring. Initialized to true so the script calls the API at loading.

        self.nliveGames_previous = 0
        self.nliveGames = 0

        self.gameJustEndedInd = False
        self.gameJustEndedTime = 0

        self.nRecentGames = 10 #how many recent games are displayed
        
        self.displayCycleSec = 10 #how long until the displays cycle to the next game

        self.liveGameTimeRange = 60*60*1 #only look for games in the live game endpoint in the last hour.

        self.displayedGames = [displayStruct("None", 0, 0),
                               displayStruct("None", 0, 0)]

        self.recentGameDisplayedIndex = 0
        self.liveGameDisplayedIndex = 0

    #calls the live game endpoint to check for games.
    def get_live_games(self, timeRange):
        sb.time_gotLiveGames = time.time()

        url_liveGames = 'https://api.projectrio.app//populate_db/ongoing_game/'
        testInd = False

        if test_bool:
            liveGames_json = json.load(open('C:/Users/nlann/Documents/Project Rio/ongoingGamesExample.json'))
        else:
            liveGames_json = json.loads(urlopen(url_liveGames).read())
            print("live games API call", time.asctime(time.localtime(math.floor(time.time()))))
            
        self.liveGames_all = liveGames_json["ongoing_games"]

        self.liveGames_previous = self.liveGames_inTimeRange
        self.liveGames_inTimeRange = []
        for game in self.liveGames_all:
            if int(game['start_time']) > int(timeRange):
                self.liveGames_inTimeRange.append(game)

        sb.nliveGames_previous = sb.nliveGames
        sb.nliveGames = len(self.liveGames_inTimeRange)

        if sb.nliveGames > 0:
            self.live_gameInd = True
        else:
            self.live_gameInd = False

        if sb.nliveGames_previous > sb.nliveGames: #need to update to ignore stale games
            sb.gameJustEndedInd = True
            sb.gameJustEndedTime = time.time()
            self.get_recent_games(sb.nRecentGames)
            self.displayedGames[0] = displayStruct("Recent", 0, time.time())

        #to do: check if live games are stale and mark them somehow
        #to do: exclude game from current HUD file.
    
    #retrieves the last x completed games
    def get_recent_games(self, nGames):
        sb.time_gotRecentGames = time.time()

        url_recentGames = "https://api.projectrio.app/games/?&limit_games=" + str(nGames)

        testInd = False

        if test_bool:
            recentGames_json = json.load(open('C:/Users/nlann/Documents/Project Rio/recentGamesExample.json'))
        else:
            recentGames_json = json.loads(urlopen(url_recentGames).read())
            print("recent games API call", time.asctime(time.localtime(math.floor(time.time()))))
        self.recentGames = recentGames_json["games"]

    #formats
    def recent_game_formatting(self, gameIndex):
        gameInfo = self.recentGames[gameIndex]

        self.recent_h_player = gameInfo["Home User"]
        self.recent_a_player = gameInfo["Away User"]
        nameLength = max(len(self.recent_a_player), len(self.recent_h_player))

        if gameInfo["Innings Played"] == gameInfo["Innings Selected"]:
            fString = "Final"
        else:
            fString = "Final(" + str(gameInfo["Innings Played"]) + "/" + str(gameInfo["Innings Selected"]) + ")"


        self.recent_gameMode = modeMapping[gameInfo["Game Mode"]]

        self.recent_h_captain = gameInfo["Home Captain"]
        self.recent_a_captain = gameInfo["Away Captain"]
        
        self.recent_h_score = gameInfo["Home Score"]
        self.recent_a_score = gameInfo["Away Score"]

        self.recent_stadium = stadMapping[gameInfo["Stadium"]]

        gameShownString = "(Showing " + str(gameIndex + 1) + "/" + str(self.nRecentGames) + ")"

        timeSinceGame_s = time.time() - gameInfo["date_time_end"]
        timeSinceGame_m = math.floor(timeSinceGame_s/60)
        timeSinceGame_h = math.floor(timeSinceGame_m/60)

        if timeSinceGame_h <= 0:
            timeSinceGame = str(timeSinceGame_m) + " Mins Ago"
        elif timeSinceGame_h == 1:
            timeSinceGame = str(timeSinceGame_h) + " Hr Ago"
        else: 
            timeSinceGame = str(timeSinceGame_h) + " Hrs Ago"

        #option 1
        recentString = self.recent_gameMode + fString.rjust(30 - len(self.recent_gameMode)," ") + "\n" + \
            self.recent_a_player.ljust(nameLength," ") + " " + str(self.recent_a_score).ljust(3," ") + self.recent_a_captain.rjust(30 - nameLength - 4) + "\n" + \
            self.recent_h_player.ljust(nameLength," ") + " " + str(self.recent_h_score).ljust(3," ") + self.recent_h_captain.rjust(30 - nameLength - 4) + "\n" + \
            self.recent_stadium + timeSinceGame.rjust(30 - len(self.recent_stadium))

        recentString = fString + timeSinceGame.rjust(30 - len(fString)) + "\n" + \
            self.recent_a_player.ljust(nameLength," ") + " " + str(self.recent_a_score).ljust(3," ") + self.recent_a_captain.rjust(30 - nameLength - 4) + "\n" + \
            self.recent_h_player.ljust(nameLength," ") + " " + str(self.recent_h_score).ljust(3," ") + self.recent_h_captain.rjust(30 - nameLength - 4) + "\n" + \
            self.recent_stadium +  self.recent_gameMode .rjust(30 - len(self.recent_stadium))
  
        return recentString
    
    def live_game_fomatting(self, gameIndex):
        gameInfo = self.liveGames_inTimeRange[gameIndex]

        self.live_h_player = gameInfo["home_player"]
        self.live_a_player = gameInfo["away_player"]
        nameLength = max(len(self.live_a_player), len(self.live_h_player))

        self.live_h_score = gameInfo["home_score"]
        self.live_a_score = gameInfo["away_score"]

        self.live_stadium = stadMapping[gameInfo["stadium_id"]]

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

        self.live_R1 = gameInfo["runner_on_first"]
        self.live_R2 = gameInfo["runner_on_second"]
        self.live_R3 = gameInfo["runner_on_third"]
        runnerString = "◄" if self.live_R3 else "‹"
        runnerString += "▲" if self.live_R2 else "^"
        runnerString += "►" if self.live_R1 else "›"

        self.live_gameMode = modeMapping[gameInfo["tag_set"]]

        self.live_pitcherID = gameInfo["pitcher"]
        self.live_batterID = gameInfo["batter"]

        if self.live_halfInning == 0:
            self.live_pitcherName = charMapping[gameInfo[f"home_roster_{self.live_pitcherID}_char"]]
            pitcherString = "P " + str(self.live_pitcherName)
            self.live_batterName = charMapping[gameInfo[f"away_roster_{self.live_batterID}_char"]]
            batterString = "B " + str(self.live_batterName)

            homeCharString = pitcherString
            awayCharString = batterString
        else: 
            self.live_pitcherName = charMapping[gameInfo[f"away_roster_{self.live_pitcherID}_char"]]
            pitcherString = "P " + str(self.live_pitcherName)
            self.live_batterName = charMapping[gameInfo[f"home_roster_{self.live_batterID}_char"]]
            batterString = "AB " + str(self.live_batterName)
            homeCharString = batterString
            awayCharString = pitcherString

        #option 1
        #liveString = self.live_gameMode + "●Live".rjust(30 - len(self.live_gameMode)," ") + "\n" + \
            # self.live_a_player.ljust(nameLength," ") + " " + str(self.live_a_score).ljust(3," ") + awayCharString.rjust(30 - nameLength - 4) + "\n" + \
            # self.live_h_player.ljust(nameLength," ") + " " + str(self.live_h_score).ljust(3," ") + homeCharString.rjust(30 - nameLength - 4) + "\n" + \
            # self.live_stadium.ljust(14, " ") + str(self.live_inning) + str(halfInnChar).ljust(5, " ") + runnerString .ljust(7," ") + outsString
        
        #option 2
        liveString = (str(self.live_inning) + str(halfInnChar).ljust(5, " ") + runnerString.ljust(7," ") + outsString).ljust(30 - 5, " ") + "●Live" + "\n" + \
            self.live_a_player.ljust(nameLength," ") + " " + str(self.live_a_score).ljust(3," ") + awayCharString.rjust(30 - nameLength - 4) + "\n" + \
            self.live_h_player.ljust(nameLength," ") + " " + str(self.live_h_score).ljust(3," ") + homeCharString.rjust(30 - nameLength - 4) + "\n" + \
            self.live_stadium + self.live_gameMode.rjust(30 - len(self.live_stadium))

        return liveString

    def decide_games_to_display(self):
        if live_displayInd and recent_displayInd:#both displays 
            if self.nliveGames == 0: #if no live games, both show recent
                if self.displayedGames[0].displayStartTime < time.time() - self.displayCycleSec: #if time to change
                        self.recentGameDisplayedIndex = (self.recentGameDisplayedIndex + 1) % self.nRecentGames
                        self.displayedGames[0] = displayStruct("Recent", self.recentGameDisplayedIndex, time.time())
                if self.displayedGames[1].displayStartTime < time.time() - self.displayCycleSec: #if time to change
                        self.recentGameDisplayedIndex = (self.recentGameDisplayedIndex + 1) % self.nRecentGames
                        self.displayedGames[1] = displayStruct("Recent", self.recentGameDisplayedIndex, time.time())
            else: #if there's at least 1 live game
                #live display
                if self.displayedGames[0].displayStartTime < time.time() - self.displayCycleSec: #if time to change
                    if self.nliveGames > 1: #if more than 1 live game, then just rotate between them
                        self.liveGameDisplayedIndex = (self.liveGameDisplayedIndex + 1) % self.nliveGames
                        self.displayedGames[0] = displayStruct("Live", self.liveGameDisplayedIndex, time.time())
                    else: #just show single live game
                        self.displayedGames[0] = displayStruct("Live", 0, time.time())
                #recent display
                if self.displayedGames[1].displayStartTime < time.time() - self.displayCycleSec: #if past time, then update game
                    self.recentGameDisplayedIndex = (self.recentGameDisplayedIndex + 1) % self.nRecentGames
                    self.displayedGames[1] = displayStruct("Recent", self.recentGameDisplayedIndex, time.time())
        elif live_displayInd and not recent_displayInd: #just live display
            self.displayedGames[1] = displayStruct("None", 0, 0)
            if self.displayedGames[0].displayStartTime < time.time() - self.displayCycleSec: #if time to change
                if self.nliveGames == 0: #if no live games, show recent
                    self.recentGameDisplayedIndex = (self.recentGameDisplayedIndex + 1) % self.nRecentGames
                    self.displayedGames[0] = displayStruct("Recent", self.recentGameDisplayedIndex, time.time())
                elif self.nliveGames > 1: #if more than 1 live game, then just rotate between them
                    self.liveGameDisplayedIndex = (self.liveGameDisplayedIndex + 1) % self.nliveGames
                    self.displayedGames[0] = displayStruct("Live", self.liveGameDisplayedIndex, time.time())
                else: #rotate live game with 1 recent game
                    if self.displayedGames[0].gameType == "Live":
                        self.recentGameDisplayedIndex = (self.recentGameDisplayedIndex + 1) % self.nRecentGames
                        self.displayedGames[0] = displayStruct("Recent", self.recentGameDisplayedIndex, time.time())
                    else:
                        self.liveGameDisplayedIndex = 0
                        self.displayedGames[0] = displayStruct("Live", self.liveGameDisplayedIndex, time.time())
        elif not live_displayInd and recent_displayInd: #just recent display
            self.displayedGames[0] = displayStruct("None", 0, 0)
            if self.displayedGames[1].displayStartTime < time.time() - self.displayCycleSec: #if time to change
                self.recentGameDisplayedIndex = (self.recentGameDisplayedIndex + 1) % self.nRecentGames
                self.displayedGames[1] = displayStruct("Recent", self.recentGameDisplayedIndex, time.time())
        else:
            self.displayedGames[0] = displayStruct("None", 0, 0)
            self.displayedGames[1] = displayStruct("None", 0, 0)

    def update_displays(self):
        liveDisplay_source = S.obs_get_source_by_name("liveDisplay")
        if liveDisplay_source is not None:
            settings = S.obs_data_create()
            if self.displayedGames[0].gameType == "None":
                S.obs_data_set_string(settings, "text", "")
            elif self.displayedGames[0].gameType == "Live":
                S.obs_data_set_string(settings, "text", self.live_game_fomatting(self.displayedGames[0].gameIndex))
            else:
                S.obs_data_set_string(settings, "text", self.recent_game_formatting(self.displayedGames[0].gameIndex))
            S.obs_source_update(liveDisplay_source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(liveDisplay_source)

        recentDisplay_source = S.obs_get_source_by_name("recentDisplay")
        if recentDisplay_source is not None:
            settings = S.obs_data_create()
            if self.displayedGames[1].gameType == "None":
                S.obs_data_set_string(settings, "text", "")
            else:
                S.obs_data_set_string(settings, "text", self.recent_game_formatting(self.displayedGames[1].gameIndex))
            S.obs_source_update(recentDisplay_source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(recentDisplay_source)


def update_display_pressed(props, prop):

    global recent_displayInd
    global live_displayInd
    live_displayInd = S.obs_data_get_bool(globalsettings, "_live_game_display")
    recent_displayInd = S.obs_data_get_bool(globalsettings, "_recent_game_display")

    current_scene = S.obs_frontend_get_current_scene()
    sb.scene = S.obs_scene_from_source(current_scene)
    S.obs_source_release(current_scene)

    liveDisplay = S.obs_scene_find_source(sb.scene,'liveDisplay')

    if liveDisplay is None and live_displayInd: #source doesn't exist, and the checkbox is true, then create            
        sb.get_live_games(time.time()-60*60*1*1)

        settings = S.obs_data_create()
        #if sb.platform == 'MacOS':
        #    liveDisplay = S.obs_source_create("text_ft2_source", 'liveDisplay', settings, None)
        #else:
        liveDisplay = S.obs_source_create("text_gdiplus", 'liveDisplay', settings, None)
        S.obs_scene_add(sb.scene, liveDisplay)
        S.obs_source_release(liveDisplay)
        S.obs_data_release(settings)
    
    if liveDisplay is not None and not live_displayInd: #source exists and the checkbox is false, then remove
        S.obs_sceneitem_remove(liveDisplay)


    recentDisplay = S.obs_scene_find_source(sb.scene,'recentDisplay')

    if recentDisplay is None and recent_displayInd: #source doesn't exist, and the checkbox is true, then create
        recent_displayInd = True

        sb.get_recent_games(sb.nRecentGames)

        settings = S.obs_data_create()
        #if sb.platform == 'MacOS':
        #    recentDisplay = S.obs_source_create("text_ft2_source", 'recentDisplay', settings, None)
        #else:
        recentDisplay = S.obs_source_create("text_gdiplus", 'recentDisplay', settings, None)
        S.obs_scene_add(sb.scene, recentDisplay)
        S.obs_source_release(recentDisplay)
        S.obs_data_release(settings)
    
    if recentDisplay is not None and not recent_displayInd: #source exists and the checkbox is false, then remove
        S.obs_sceneitem_remove(recentDisplay)
        recent_displayInd = False



def script_load(settings):

    S.timer_add(check_for_updates, 5000)

    global globalsettings
    globalsettings = settings

    global sb
    sb = scoreboard()

    global ds
    ds = displayStruct(str(), 0, 0)

    global test_bool
    test_bool = False
    
    global live_displayInd
    global recent_displayInd
    live_displayInd = S.obs_data_get_bool(globalsettings, "_live_game_display")
    recent_displayInd = S.obs_data_get_bool(globalsettings, "_recent_game_display")

def check_for_updates():
    if pause_bool == False:
        if sb.gameJustEndedInd and sb.gameJustEndedTime < time.time() - 2*60: #treat a just ended live game as still live for 2 minutes
            sb.gameJustEndedInd = False
        
        if sb.live_gameInd:
            if sb.time_gotLiveGames < time.time() - 20: #call every 20 seconds if there is a live game occuring
                sb.get_live_games(time.time()-60*60*1*1)
        else:
            if sb.time_gotLiveGames < time.time() - 5*60: #call every 5 minutes if there are no live games occuring
                sb.get_live_games(time.time()-60*60*1*1)
        if sb.time_gotRecentGames < time.time() - 30*60: #calls every 60 minutes. If the live games list shrinks, it also calls this function.
            sb.get_recent_games(sb.nRecentGames)
        
        sb.decide_games_to_display()
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
    return  "By Nuche17\n" \
            "**USE A CASCADIA MONO FONT FOR THE DISPLAYS**\n" \
            "Adds scenes that show recent and live games in the database.\n" \
            "Each scene cycles through several games every 10 seconds.\n" \
            "If the live scene is the only one selected, it will prioritize live games, but if there is only 1 or none, it will also show recent games.\n" \
            "The recent games scene will only show recent games (currently the last 10).\n" \
            "If both scenes are selected, the Live display will exclusively show live games, as long as there's at least one happening.\n" \
            "When changing settings, press the Update Button to process the changes.\n" \
            "The code will look for new live games every 5 minutes. If there are any live games, it will refresh them every 20 seconds.\n" \
            "Recent games will update every 30 minutes, or when a live game ends."

def script_properties():
    props = S.obs_properties_create()

    S.obs_properties_add_bool(props, "_pause", "Pause")\
    
    S.obs_properties_add_button(props, "_updateDisplayButton", "Update Displays", update_display_pressed)

    S.obs_properties_add_bool(props, "_live_game_display", "Show Live Games Display")
    S.obs_properties_add_bool(props, "_recent_game_display", "Show Recent Games Display")

    return props

