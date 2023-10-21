'''
Intended to parse in-game Rio HUD files

How to use:
- import RioHudLib obviously
- open a Rio hud json file
- convert from json string to obj using json.loads(jsonStr)
- create hudObj with your stat json obj using the following:
	myStats = HudFileScan.hudObj(jsonObj)
- call any of the built-in methods to get some stats

- ex:
	import RioHudLib
	import json
	with open("path/to/RioHudFile.json", "r") as jsonStr:
		jsonObj = json.loads(jsonStr)
		myHUD = RioHudLib.StatObj(jsonObj)
		inning = myHUD.inning()
		awayTeamRoster = myHUD.roster(0)

Team args:
- arg == 0 means team0 which is the away team
- arg == 1 means team1 which is the home team

Roster args:
- arg == 0 -> 8 for each of the 9 roster spots
- arg == -1 or no arg provided means all characters on that team (if function allows)

'''

class hudObj:
    def __init__(self, hud_json: dict):
        self.hud_json = hud_json
        self.event_number = self.hud_json['Event Num']
    
    def inning(self):
        return self.hud_json['Inning']
    
    def event_integer(self):
        return int(str(self.event_number)[:-1])
    
    def half_inning(self):
        return self.hud_json['Half Inning']
    
    def inning_float(self):
        return float(self.hud_json['Inning'] + 0.5*self.hud_json['Half Inning'])
    
    def team_roster_str_list(self, teamNum: int):
        self.__errorCheck_teamNum(teamNum)
        team_string = "Away" if teamNum == 0 else "Home"
        team_roster_str_list = []
        for i in range (9):
             team_roster_str_list.append(f'{team_string} Roster {i}')
        
        return team_roster_str_list

    def roster(self, teamNum: int):
        roster_dict = {}
        for player in self.team_roster_str_list(teamNum):
            player_index = int(player[-1])
            roster_dict[player_index] = {}
            roster_dict[player_index]['captain'] = self.hud_json[player]['Captain']
            roster_dict[player_index]['char_id'] = self.hud_json[player]['CharID']

        return roster_dict
    
    def inning_end(self):
        if self.hud_json['Outs'] + self.hud_json['Num Outs During Play'] == 3:
            return True
        
        return False
    
    def player(self, teamNum: int):
        self.__errorCheck_teamNum(teamNum)
        if teamNum == 0:
            return self.hud_json['Away Player']
        elif teamNum == 1:
            return self.hud_json['Home Player']
    
    def event_result(self):
        if str(self.hud_json['Event Num'])[-1] == 'b':
            return self.hud_json['Result of AB']
        
        return 'In Play'
    
    def captain_index(self, teamNum: int):
        self.__errorCheck_teamNum(teamNum)
        for player in self.team_roster_str_list(teamNum):
            if self.hud_json[player]['Captain'] == 1:
                return int(player[-1])
        raise Exception(f'No captain on teamNum {teamNum}')

    def __errorCheck_teamNum(this, teamNum: int):
        # tells if the teamNum is invalid
        if teamNum != 0 and teamNum != 1:
            raise Exception(
                f'Invalid team arg {teamNum}. Function only accepts team args of 0 (home team) or 1 (away team).')

    def __errorCheck_rosterNum(this, rosterNum: int):
        # tells if rosterNum is invalid. allows -1 arg
        if rosterNum < -1 or rosterNum > 8:
            raise Exception(f'Invalid roster arg {rosterNum}. Function only accepts roster args of from 0 to 8.')