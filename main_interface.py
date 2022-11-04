# Main module where the fantasy manager's team is defined

import stat_scraper
import os.path
import json
import csv
import numpy as np
from collections import namedtuple

# Defines each player
class Player:

    # Player information and stats
    def __init__(self,name, team='', roto_url='', team_url='', curr_week_games=[], games_played=[], min_per_gm=[],
                 fg_perc=[], ft_perc=[],threes_made=[], pts=[], rebs=[], assists=[],steals=[], blocks=[], turnovers=[] ):
        self.name = name
        self.team = team

        self.roto_url = roto_url
        self.team_url = team_url
        self.curr_week_games = curr_week_games

        # stats will be saved as 2 item arrays: [Rotowire projected stat, live current season stat]
        self.games_played = games_played
        self.min_per_gm = min_per_gm
        self.fg_perc = fg_perc
        self.ft_perc = ft_perc
        self.threes_made = threes_made
        self.pts = pts
        self.rebs = rebs
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.turnovers = turnovers


    # Returns the number of games that week
    def get_weekly_games(self,team):
        #stat_scraper
        pass

    # Populates all stats with both projected and current season stats, weekly games
    # Called when new player is added
    def populate_player_stats(self,projected_stats, player_url, driver):

        # Scrape player's current season stats
        curr_season = stat_scraper.scrape_player_current(self.name,player_url, driver)

        self.games_played = [projected_stats[self.name][0], curr_season[0]]
        self.min_per_gm = [projected_stats[self.name][1], curr_season[1]]
        self.pts = [projected_stats[self.name][2], curr_season[2]]
        self.rebs = [projected_stats[self.name][3], curr_season[3]]
        self.assists = [projected_stats[self.name][4], curr_season[4]]
        self.steals = [projected_stats[self.name][5], curr_season[5]]
        self.blocks = [projected_stats[self.name][6], curr_season[6]]
        self.threes_made = [projected_stats[self.name][7], curr_season[7]]
        self.fg_perc = [projected_stats[self.name][8], curr_season[8]]
        self.ft_perc = [projected_stats[self.name][9], curr_season[9]]
        self.turnovers = [projected_stats[self.name][10], curr_season[10]]

        self.team, self.team_url = stat_scraper.scrape_player_team(driver, self.name, player_url)
        self.roto_url = player_url[self.name]
        self.curr_week_games = stat_scraper.scrape_player_weekly_games(driver, self.team_url)


    # Returns all player weekly cumulative stats as a list for csv writing
    def player_stats(self):

        projected_player_stats = [self.name,'(Projected)',self.games_played[0],self.min_per_gm[0]*self.curr_week_games,
                                  self.pts[0]*self.curr_week_games,self.rebs[0]*self.curr_week_games,self.assists[0]*self.curr_week_games,
                                  self.steals[0]*self.curr_week_games,self.blocks[0]*self.curr_week_games,
                                  self.threes_made[0]*self.curr_week_games,self.fg_perc[0],self.ft_perc[0],
                                  self.turnovers[0]*self.curr_week_games]
        curr_play_stats = [self.name,'(Current Season)',self.games_played[1],self.min_per_gm[1]*self.curr_week_games,
                           self.pts[1]*self.curr_week_games,self.rebs[1]*self.curr_week_games,self.assists[1]*self.curr_week_games,
                           self.steals[1]*self.curr_week_games,self.blocks[1]*self.curr_week_games,
                           self.threes_made[1]*self.curr_week_games,self.fg_perc[1],self.ft_perc[1],
                           self.turnovers[1]*self.curr_week_games]

        return projected_player_stats, curr_play_stats

    # Encoder to save player as JSON string for future script runs
    def to_json(self):
        return json.dumps(self,default=lambda o:o.__dict__)

    # Updates current season stats
    def get_curr_season_stats(self,name):
        pass


# Defines the manager's team
class Team:

    def __init__(self,max_players=0):

        # Roster is the set of players on manager's team
        self.roster = set()
        self.max_players = max_players

    # Checks if additional players can be added based on max team size
    def can_add_player(self, player_name):

        if len(self.roster) >= self.max_players:
            print('Maximum number of players reached!')
            return False

        elif player_name in self.roster:
            print('Player already exists!')
            return False

        else:
            return True

    # Add player to roster
    def add_player(self,name,projected_stats, player_url, driver):
        if self.can_add_player(name) == True:

            # Populate player object with stats
            new_player = Player(name=name)
            new_player.populate_player_stats(projected_stats, player_url, driver)
            self.roster.add(new_player)

    # Delete player from roster
    def del_player(self,name):

        for player in self.roster:
            if name == player.name:
                self.roster.remove(player)
                print(f'{name} removed from roster!')
                break
        else:
            print('Player not in roster')
            print(f'Roster size: {len(self.roster)}')

    # Convert each rostered player object into list for csv writing
    def team_data(self):

        stats = []
        for player in self.roster:
            proj, curr = player.player_stats()
            stats.append(proj)
            stats.append(curr)

        return stats

    # Save team's player objects for future use
    def team_to_json(self):

        json_data = []

        for player in self.roster:
            json_data.append(player.to_json())

        return json_data



    # Calculate team total weekly stats
    def get_totals(self):

        totals_proj = np.zeros(13)
        totals_curr = np.zeros(13)

        for player in self.roster:

            temp_proj, temp_curr = player.player_stats()
            for i in range(2,len(temp_proj)):
                totals_proj[i] += temp_proj[i]
                totals_curr[i] += temp_curr[i]

        # Convert numpy array to list for csv writing
        totals_proj = list(totals_proj)
        totals_curr = list(totals_curr)

        totals_proj[0] = totals_curr[0] = 'Weekly Totals'
        totals_proj[1] = 'Projected Stats'
        totals_curr[1] = 'Current Season'

        return totals_proj, totals_curr


# Checks player name input. If valid entry, returns full player name
def check_player_input(input_name,player_list):

    for key in player_list.keys():
        if input_name.lower() in key.lower():
            return key

    print('Player does not exist')
    return None

# Export team player objects as JSON for future use
def export_teams_json(my_team,opp_team):

    # Save my team data
    my_json = my_team.team_to_json()
    with open('my_team.json', 'w') as f:
        json.dump(my_json,f)

    # Save opposing team data
    opp_json = opp_team.team_to_json()
    with open('opp_team.json','w') as g:
        json.dump(opp_json,g)

# Decode team JSON file
def import_team_json(file,team):

    with open(file,'r') as f:
        json_list_of_strs = json.load(f)

    # go through each player string
    for i in json_list_of_strs:
        player = json.loads(i,object_hook=as_player)
        team.roster.add(player)

def as_player(json_str):

    i = json_str
    if 'name' in json_str:
        return Player(name=i['name'], team=i['team'], roto_url=i['roto_url'], team_url=i['team_url'],
                      curr_week_games=i['curr_week_games'], games_played=i['games_played'],
                      min_per_gm=i['min_per_gm'],
                      fg_perc=i['fg_perc'], ft_perc=i['ft_perc'], threes_made=i['threes_made'], pts=i['pts'],
                      rebs=i['rebs'], assists=i['assists'], steals=i['steals'], blocks=i['blocks'],
                      turnovers=i['turnovers'])


        # Main module
def main():

    print('Initializing Stats...')
    # Checks if player url list JSON exists
    if os.path.exists('player_url_list.json'):

        # Already exists so no need to scrape NBA.com
        with open('player_url_list.json','r') as file:
            player_url_list = json.load(file)

    # Does not exist so scrape for players and matching URLs
    else:
        player_url_list = {}
        dr = stat_scraper.start_session()
        stat_scraper.initialize_player_list(dr,player_url_list)

    # Checks if projected stats JSON exists
    # Scrapes all player's projected stats ahead of time to identify top players
    # Projected stats typically remain consistent throughout the season so we don't update it
    if os.path.exists('all_projected_stats.json'):

        # Already exists so don't need to scrape Rotowire for each player's stats
        with open('all_projected_stats.json','r') as file:
            all_projected_stats = json.load(file)

    else:
        all_projected_stats = {}
        dr = stat_scraper.start_session()
        stat_scraper.scrape_all_projected(dr,player_url_list,all_projected_stats)


    # Start a webdriver to grab stats
    # Stats populated through javascript so need to use webdriver
    driver = stat_scraper.start_session()

    # Input the maximum allowable players per team
    while True:
        try:
            max_players = int(input('Max players in a team: '))
        except ValueError:
            print('Not a valid number. Try again.')
        else:
            break

    # Initialize two teams with the max number of players
    my_team = Team(max_players=max_players)
    opp_team = Team(max_players=max_players)

    # Checks if my_team.json has already been created so that we don't need to repeat player input
    if os.path.exists('my_team.json'):

        # File exists so read my team and opposing team players
        import_team_json('my_team.json',my_team)

    # Checks if opp_team.json has already been created so that we don't need to repeat player input
    if os.path.exists('opp_team.json'):
        # File exists so read my team and opposing team players
        import_team_json('opp_team.json', opp_team)

    print('Done Initialization!')

    exit_script = 0

    # Continuously asks what the user would like to do
    while exit_script==0:

        print('What would you like to do?')
        try:
            choice = int(input('1 - Add player to my team, 2 - Add player to opposing team, \n'
                               '3 - Remove player from my team, 4 - Remove player from opposing team \n'
                               '5 - Compare Teams!, 6 - Exit: '))
        except ValueError:
            print('Invalid entry')
        else:
            if choice < 1 or choice > 6:
                print('Invalid entry')
            else:

                # Adding a player
                if choice == 1 or choice == 2:
                    print('Updating team...')
                    input_name = input('Add a player: ')
                    full_name = check_player_input(input_name, player_url_list)

                    # If player found
                    if full_name is not None:

                        if choice == 1:
                            my_team.add_player(full_name,all_projected_stats,player_url_list, driver)
                            print(f'Player Added: {full_name}')
                            print(f'Roster Size: {len(my_team.roster)}')

                        elif choice == 2:
                            opp_team.add_player(full_name,all_projected_stats,player_url_list, driver)
                            print(f'Player Added: {full_name}')
                            print(f'Roster Size: {len(opp_team.roster)}')

                # Deleting a player
                elif choice == 3 or choice == 4:
                    input_name = input('Delete a player: ')
                    full_name = check_player_input(input_name, player_url_list)

                    # If player found
                    if full_name is not None:

                        if choice == 3:
                            my_team.del_player(full_name)
                        elif choice == 4:
                            opp_team.del_player(full_name)

                # Compare stats = create CSV of rostered players' stats
                elif choice == 5:

                    file_name = 'Weekly Team Stats.csv'
                    header_one = [['My Team'],['']]
                    data_header = [['Player','Stat Type','Games Played','Minutes per Game','Points per Game','Rebounds',
                                   'Assists','Steals','Blocks', '3PM','FG%', 'FT%','Turnovers'],['']]
                    header_two = [[''],['Opposing Team'],['']]
                    my_total_proj, my_total_curr = my_team.get_totals()
                    opp_total_proj, opp_total_curr = opp_team.get_totals()

                    with open(file_name,'w',newline='') as f:
                        writer = csv.writer(f)

                        writer.writerows(header_one)
                        writer.writerows(data_header)
                        writer.writerows(my_team.team_data())
                        writer.writerow(my_total_proj)
                        writer.writerow(my_total_curr)

                        writer.writerows(header_two)
                        writer.writerows(data_header)
                        writer.writerows(opp_team.team_data())
                        writer.writerow(opp_total_proj)
                        writer.writerow(opp_total_curr)

                # End program
                elif choice == 6:
                    while True:
                        save = input('Save current teams? [Y/N] ')

                        # Save teams into JSON files
                        if save.lower() == 'y':
                            export_teams_json(my_team,opp_team)
                            break

                        # No saving needs to be done, so continue
                        elif save.lower() == 'n':
                            break
                        else:
                            print('Incorrect input!')


                    print('Goodbye!')
                    exit_script = 1






















if __name__ == '__main__':
    main()



