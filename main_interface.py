# Main module where the fantasy manager's team is defined

import stat_scraper

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


    # Returns the number of games that week
    def get_weekly_games(self,team):
        #stat_scraper

    # Populates all stats with both projected and current season stats
    # Called when new player is added
    def get_all_stats(self,name):

    # Updates current season stats
    def get_curr_season_stats(self,name):


# Defines the manager's team
class Team:

    def __init__(self,max_players):

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




