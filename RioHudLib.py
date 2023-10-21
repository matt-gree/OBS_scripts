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

    def event_number(self):
        return self.hud_json['Event Num']
    
    def inning(self):
        return self.hud_json['Inning']
    
    def half_inning(self):
        return self.hud_json['Half Inning']

    def roster(self, team):
        roster_dict = {}
        team_string = "Away" if team == 0 else "Home"
        for roster in range(9):
            roster_dict[roster_dict] = {}
            team_roster_str = f'{team_string} Roster {roster}'
            roster_dict[roster_dict]['captain'] = self.hud_json[team_roster_str]['Captain']
            roster_dict[roster_dict]['char_id'] = self.hud_json[team_roster_str]['CharID']

        return roster_dict
    
    def inning_end(self):
        if self.hud_json['Outs'] + self.hud_json['Num Outs During Play'] == 3:
            return True
        
        return False
    
    def event_result(self):
        if str(self.hud_json['Event Num'])[-1] == 'b':
            return self.hud_json['Result of AB']
        
        return 'In Play'
