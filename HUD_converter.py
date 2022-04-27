import os, sys
from pprint import pprint
import threading, time
import json

WAIT_TIME_SECONDS = 2

stat_file_dir = str()
output_dir = str()

def dir_scan(current_event_num):
    hud_file_path = os.path.join(stat_file_dir, 'decoded.hud.json')
    if not os.path.isfile(hud_file_path):
        return ""
    with open(hud_file_path) as f:
        hud_data = json.load(f)
    
    #Return if the event hasn't changed
    if (current_event_num == hud_data['Event Num']):
        return current_event_num
    
    print("New HUD:", current_event_num, hud_data['Event Num'])
    current_event_num = hud_data['Event Num']

    #Bookkeepping vars
    away_team_captain_char = str()
    home_team_captain_char = str()

    #Dicts to hold data for characters and teams(player)
    player_batter_data = {'Name': '', 'RBI': 0, 'SO': 0, 'BB/HBP': 0, 'AB': 0, 'H': 0, 'HR': 0}
    character_batter_data = {'Name': '', 'RBI': 0, 'SO': 0, 'BB/HBP': 0, 'AB': 0, 'H': 0, 'HR': 0}
    player_pitcher_data = {'Name': '', 'ER': 0, 'H': 0, 'SO': 0, 'STAM': 0, 'BB/HBP': 0, 'NP': 0}
    character_pitcher_data = {'Name': '', 'ER': 0, 'H': 0, 'SO': 0, 'STAM': 0, 'BB/HBP': 0, 'NP': 0}
    
    for team in range(0,2):
        for roster in range(0,9):
            team_roster_str = "Team " + str(team) + " Roster " + str(roster)
            if (hud_data[team_roster_str]["Captain"] == 1):
                #Captains
                if (team == 0):
                    home_team_captain_char = hud_data[team_roster_str]["CharID"]
                else:
                    away_team_captain_char = hud_data[team_roster_str]["CharID"]

            captain_star_str = str()
            if hud_data[team_roster_str]['Superstar']:
                captain_star_str += '★'
            if hud_data[team_roster_str]['Captain']:
                captain_star_str += ' ©'
            
            #Get batter and pitcher data both for the player and individual character
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
                    character_batter_data['Name'] = str(hud_data[team_roster_str]["RosterID"]) + ". " + hud_data[team_roster_str]["CharID"] + captain_star_str
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
                    character_pitcher_data['Name'] =  hud_data[team_roster_str]["CharID"] + captain_star_str
                    character_pitcher_data['ER'] += pitcher_defensive_data["Earned Runs"]
                    character_pitcher_data['H'] += pitcher_defensive_data["Hits Allowed"]
                    character_pitcher_data['STAM'] += pitcher_defensive_data["Stamina"]
                    character_pitcher_data['BB/HBP'] += pitcher_defensive_data["Batters Walked"]
                    character_pitcher_data['BB/HBP'] += pitcher_defensive_data["Batters Hit"]
                    character_pitcher_data['SO'] += pitcher_defensive_data["Strikeouts"]
                    character_pitcher_data['NP'] += pitcher_defensive_data["Pitches Thrown"]

    hud_output_file = os.path.join(output_dir, 'hud.txt')
    batter_data_output_file = os.path.join(output_dir, 'batter_data.txt')
    pitcher_data_output_file = os.path.join(output_dir, 'pitcher_data.txt')

    #Main HUD
    with open(hud_output_file, 'w', encoding="utf-8") as f:
        away_batter_indicator = "◂" if hud_data['Half Inning'] == 0 else " "
        home_batter_indicator = "◂" if hud_data['Half Inning'] == 1 else " "
        inning_str = str(hud_data['Inning']) + (' ▲' if hud_data['Half Inning'] == 0 else ' ▼')

        #Runners on
        runner_1b = "◆" if hud_data.get("Runner 1B") else "◇"
        runner_2b = "◆" if hud_data.get("Runner 2B") else "◇"
        runner_3b = "◆" if hud_data.get("Runner 3B") else "◇"

        away_team_captain_char = f"({away_team_captain_char})"
        home_team_captain_char = f"({home_team_captain_char})"

        fill = max(len(str(hud_data['Away Player'])), len(str(hud_data['Home Player'])))
        captain_fill = max(len(away_team_captain_char), len(home_team_captain_char))
        score_fill = max(len(str(hud_data['Away Score'])), len(str(hud_data['Home Score'])))
        f.write(f"{hud_data['Away Player']:<{fill}} {away_team_captain_char:>{captain_fill}} |{hud_data['Away Score']:>{score_fill}}  ★: {hud_data['Away Stars']} {away_batter_indicator}\n")
        f.write(f"{hud_data['Home Player']:<{fill}} {home_team_captain_char:>{captain_fill}} |{hud_data['Home Score']:>{score_fill}}  ★: {hud_data['Home Stars']} {home_batter_indicator}\n")

        f.write("Inning: " + inning_str  + '\n')
        f.write(str(hud_data['Balls']) + "-" + str(hud_data['Strikes']) + "    " + str(hud_data['Outs']) + " Out" + "  | " + runner_2b + '\n')
        f.write("♪ on Base: " + str(hud_data['Chemistry Links on Base']) + "  |" + runner_3b + " " + runner_1b + '\n')
        if hud_data['Star Chance']:
            f.write("Star Chance!!!")

    #Do pitching and batting in the same loop. Loop 0 is character info, loop 1 is team info
    for team in range(0,2):
        pitcher_deffensive_data = character_pitcher_data if team == 0 else player_pitcher_data
        pitcher_data_output_file = os.path.join(output_dir, 'character_pitcher_data.txt') if team == 0 else os.path.join(output_dir, 'player_pitcher_data.txt')
        #Pitching
        with open(pitcher_data_output_file, 'w', encoding="utf-8") as f:

            f.write(str(pitcher_deffensive_data['Name'])+ '\n')
            f.write("ER:     " + str(pitcher_deffensive_data["ER"]) + '\n')
            f.write("H:      " + str(pitcher_deffensive_data["H"]) + '\n')        
            f.write("SO:     " + str(pitcher_deffensive_data["SO"]) + '\n')
            f.write("STAM:   " + str(pitcher_deffensive_data["STAM"]) + '\n')
            f.write("BB/HBP: " + str(pitcher_deffensive_data["BB/HBP"]) + '\n')
            f.write("NP:     " + str(pitcher_deffensive_data["NP"]) + '\n')

        #Batting
        batter_offensive_data = character_batter_data if team == 0 else player_batter_data
        batter_data_output_file = os.path.join(output_dir, 'character_batter_data.txt', encoding="utf-8") if team == 0 else os.path.join(output_dir, 'player_batter_data.txt')
        with open(batter_data_output_file, 'w') as f:
            f.write(str(batter_offensive_data["Name"]))
            f.write("   " + str(batter_offensive_data["H"]) + "-" + str(batter_offensive_data["AB"]) )
            f.write(", RBI: " + str(batter_offensive_data["RBI"]))
            f.write(", SO: " + str(batter_offensive_data["SO"]))
            f.write(", HR: " + str(batter_offensive_data["HR"]))
            f.write(", BB/HBP: " + str(batter_offensive_data["BB/HBP"]))

    #Previous Event info
    #First check if previous event exists and had contact
    #if (hud_data.get('Previous Event')):
    #    if (hud_data.get('Pitch') and hud_data.get('Contact')):
    #        contact_output_file = os.path.join(output_dir, 'contact.txt')
    #        with open(contact_output_file, 'w', encoding="utf-8") as f:
    return current_event_num

if __name__ == '__main__':
    application_path = os.path.dirname(sys.executable)
    print(application_path)
    config_file_path = os.path.join(application_path, 'config.txt')
    #For local testing uncomment
    config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.txt')

    #Get directories from config file
    with open(config_file_path) as f:
        lines = f.readlines()
        for line in lines:
            if "StatFile Directory" in line:
                stat_file_dir = line.split("=")[1]
                stat_file_dir = stat_file_dir.replace('\n', '')
                stat_file_dir = stat_file_dir.replace('\"', '')
            if "OBS Output Directory" in line:
                output_dir = line.split("=")[1]
                output_dir = output_dir.replace('\n', '')
                output_dir = output_dir.replace('\"', '')
    
    #Check if directories exist
    if not (os.path.isdir(stat_file_dir)):
        print('Could not find StatFile folder location. Path from config.txt =', stat_file_dir)
        exit()

    if not (os.path.isdir(output_dir)):
        print('Could not find OBS folder location. Path from config.txt =', output_dir)
        exit()

    #Begin periodically checking for new HUD file
    current_event_num = -1
    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_SECONDS):
        current_event_num = dir_scan(current_event_num)
