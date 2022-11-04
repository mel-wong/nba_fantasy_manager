# nba_fantasy_manager
The purpose of this program is to scrape NBA player statistics to identify which players to add / delete for NBA fantasy.

The program scrapes each NBA player from NBA.com and then scrapes each player's projected stats through Rotowire.com. The corresponding website URLs
for each player and their stats are saved as JSON files so that they don't need to be scraped again the next time.

The program also identifies how many games each player will play this week (Monday - Sunday) to calculate the cumulative weekly stats
for comparison. The weekly stats are then written into a .csv file for easy comparison.

To avoid having to input the team's players every time the program is run, there is also an option
to save my team and the opposing team's players in JSON files.