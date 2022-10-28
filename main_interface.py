# Main module where the fantasy manager's team is defined

import stat_scraper
import os.path
import json

# Defines each player
class Player:

    # 9 statistical categories per player for fantasy basketball
    def __init__(self,name):
        self.name = name
        self.team = ''

        # stats will be saved as 2 item arrays: [yahoo projected stat, live current season stat]
        self.fg_perc = 0
        self.ft_perc = 0
        self.threes_made = 0
        self.pts = 0
        self.rebs = 0
        self.assists = 0
        self.steals = 0
        self.blocks = 0
        self.turnovers = 0

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
    def get_all_stats(self,name):
        pass

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
    def add_player(self,name):
        if self.can_add_player() == True:
            new_player = Player(name=name)
            self.roster.add(new_player.name)
            

    # Delete player from roster
    def del_player(self,name):
        if name in self.roster:
            self.roster.remove(name)
        else:
            print('Player not in roster')

    # Update all stats - Called when new player added to roster
    def update_all_team_stats(self):
        stat_scraper

    # Update season stats
    def update_season_stats(self):
        stat_scraper


# Takes in user input. If valid entry, adds player
def add_player_input(input,team):



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
    if os.path.exists('all_projected_stats.json'):

        # Already exists so don't need to scrape Rotowire for each player's stats
        with open('all_projected_stats.json','r') as file:
            all_projected_stats = json.load(file)

    else:
        all_projected_stats = {}
        dr = stat_scraper.start_session()
        stat_scraper.scrape_all_projected(dr,player_url_list,all_projected_stats)

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

    print('Time to pick your team!')

    # Continuously asks what the user would like to do
    while True:
        print('What would you like to do?')
        try:
            choice = int(input('1 - Add player to my team, 2 - Remove player from my team, \n '
              '3 - Add player to opposing team, 4 - Remove player from opposing team, '
                  '5 - Compare Teams!, 6 - Exit: '))
        except ValueError:
            print('Invalid entry')
        else:
            if choice < 1 or choice > 6:
                print('Invalid entry')
            else:

                if choice == 1:



                break





















if __name__ == '__main__':
    main()



