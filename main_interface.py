# Main module where the fantasy manager's team is defined

import stat_scraper
import os.path
import json
import csv

# Defines each player
class Player:

    # Statistical categories per player
    def __init__(self,name):
        self.name = name
        self.team = ''

        # stats will be saved as 2 item arrays: [Rotowire projected stat, live current season stat]
        self.games_played = []
        self.min_per_gm = []
        self.fg_perc = []
        self.ft_perc = []
        self.threes_made = []
        self.pts = []
        self.rebs = []
        self.assists = []
        self.steals = []
        self.blocks = []
        self.turnovers = []

    # Returns the NBA team that the player plays for
    def get_team(self, name):
        #stat_scraper
        pass


    # Returns the number of games that week
    def get_weekly_games(self,team):
        #stat_scraper
        pass

    # Populates all stats with both projected and current season stats
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

    # Returns all player stats as a list
    def player_stats(self):

        projected_player_stats = [self.name,'(Projected)',self.games_played[0],self.min_per_gm[0],self.pts[0],self.rebs[0],self.assists[0],
                                  self.steals[0],self.blocks[0],self.threes_made[0],self.fg_perc[0],self.ft_perc[0],
                                  self.turnovers[0]]
        curr_play_stats = [self.name,'(Current Season)',self.games_played[1],self.min_per_gm[1],self.pts[1],self.rebs[1],self.assists[1],
                           self.steals[1],self.blocks[1],self.threes_made[1],self.fg_perc[1],self.ft_perc[1],
                           self.turnovers[1]]

        return projected_player_stats, curr_play_stats

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
    def can_add_player(self):

        if len(self.roster) >= self.max_players:
            print('Maximum number of players reached!')
            return False

        else:
            return True

    # Add player to roster
    def add_player(self,name,projected_stats, player_url, driver):
        if self.can_add_player() == True:

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

    # Convert each rostered player object into list
    def team_data(self):

        stats = []
        for player in self.roster:
            proj, curr = player.player_stats()
            stats.append(proj)
            stats.append(curr)

        return stats


    # Update season stats
    def update_season_stats(self):
        stat_scraper


# Checks player name input. If valid entry, returns full player name
def check_player_input(input_name,player_list):

    for key in player_list.keys():
        if input_name.lower() in key.lower():
            return key

    print('Player does not exist')
    return None


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

    # Checks if Team Stats.csv has already been created so that we don't need to repeat player input
    if os.path.exists('Team Stats.csv'):

        # File exists so read my team and opposing team players
        with open('Team Stats.csv',newline='') as f:
            reader = csv.reader(f)

            # Skip header
            for i in range(4):
                next(reader)

            for row in reader:




    # Start a webdriver to grab stats
    # Stats populated through javascript so need to use webdriver
    driver = stat_scraper.start_session()

    print('Done Initialization!')

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

                    file_name = 'Team Stats.csv'
                    header_one = [['My Team'],['']]
                    data_header = [['Player','Stat Type','Games Played','Minutes per Game','Points per Game','Rebounds',
                                   'Assists','Steals','Blocks', '3PM','FG%', 'FT%','Turnovers'],['']]
                    header_two = [[''],['Opposing Team'],['']]

                    with open(file_name,'w',newline='') as f:
                        writer = csv.writer(f)

                        writer.writerows(header_one)
                        writer.writerows(data_header)
                        writer.writerows(my_team.team_data())

                        writer.writerows(header_two)
                        writer.writerows(data_header)
                        writer.writerows(opp_team.team_data())

                # End program
                elif choice == 6:
                    print('Goodbye!')
                    exit_script = 1






















if __name__ == '__main__':
    main()



