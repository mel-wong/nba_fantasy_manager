# File to scrape Rotowire and NBA.com for player and team statistics
import time
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import os.path
from datetime import date, datetime, timedelta

# Create browser session to access different stat websites
def start_session():
    service = Service('./chromedriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


# write player names and Rotowire URL dictionary to JSON
def initialize_player_list(driver, player_list):

    driver.get('https://www.nba.com/players')
    dropdown = 'div.Pagination_pageDropdown__KgjBU > div > label > div>select'
    dropdown = Select(driver.find_element(by=By.CSS_SELECTOR, value=dropdown))

    # Changes dropdown selection to show all players
    dropdown.select_by_index(0)
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, "lxml")
    table = soup.select("table[class=players-list]")

    for t in table:

        rows = t.findAll('tr')

        # Ignore header row
        for row in rows[1:]:
            name = row.select('p')
            key = name[0].text + ' ' + name[1].text

            # set URL to None for now
            player_list[key] = None

    # Populate player list with corresponding Rotowire URL
    for k in player_list.keys():
        url = scrape_player_url(driver, k)
        player_list[k] = url
        print(k)

        if url is None:
            print(f'Cannot find {k}')

    # Save to JSON
    filename = 'player_url_list.json'
    out_file = open(filename, 'w')
    json.dump(player_list, out_file)
    out_file.close()


def search_box_actions(driver,player):

    # Checks if already on Rotowire site
    if driver.current_url is not None and 'rotowire' in driver.current_url:
        pass
    else:
        driver.get('https://www.rotowire.com')

    # Automate searching for player on Rotowire to get their page URL for stats
    search_css = "#search-for-players"
    input_element = driver.find_element(by=By.CSS_SELECTOR, value=search_css)
    actions = ActionChains(driver)
    actions.click(input_element)
    actions.send_keys(player)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    return driver.current_url


# get player's projected stats from Roto
def scrape_player_url(driver, player):

    print(f'Scraping player: {player}')
    url = search_box_actions(driver,player)

    # Fixes issue with slightly differing names between Rotowire and NBA.com
    while 'search' in url:

        # Accounts for periods in names
        if '.' in player:
            split_name = player.split('.')
            player = ''.join(split_name)
            search_box_actions(driver, player)

        # Ignore third string which usually consists of Sr, Jr, I
        elif ' ' in player:
            split_name = player.split(' ')

            # Ignore third string which usually consists of Sr, Jr, I
            if len(split_name) == 3:
                split_name.pop()
                player = ' '.join(split_name)

            # Ignore first name in case uses nickname
            elif len(split_name) == 2:
                player = split_name[1]

            url = search_box_actions(driver, player)

        # Cannot find player
        else:
            break

    return url


# Scrape the player's projected stats
def scrape_player_projected(driver, player_list, player):

    url = player_list[player]
    driver.get(url)

    # Give page time to load stats before scraping
    time.sleep(1)
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, "lxml")
    table = soup.select("div.webix_ss_footer > div.webix_hs_center > table>tbody")
    stat_list = []
    print(player)

    for t in table:

        rows = t.findAll('tr')

        # Ignore header row
        for row in rows[1:]:
            cols = row.findAll('td')

            # Ignore age column
            for col in cols[1:]:
                stat = col.find('div')

                # Convert to float
                stat = float(stat.text)
                stat_list.append(stat)

    return stat_list


# Scrape projected stats for all players and save as JSON
def scrape_all_projected(driver, player_list, all_projected_stats):

    for player in player_list.keys():
        all_projected_stats[player] = scrape_player_projected(driver, player_list, player)

    # Write all data to json file
    filename = 'all_projected_stats.json'
    out_file = open(filename, 'w')
    json.dump(all_projected_stats, out_file)
    out_file.close()

# Called when adding a player
def scrape_player_current(player,player_url_list, driver):

    curr_stats = []

    url = player_url_list[player]
    driver.get(url)

    # Give page time to load stats before scraping
    time.sleep(1)
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, "lxml")

    table = soup.select('div.webix_ss_body > div.webix_ss_center > div')

    cols = table[0].findAll('div',recursive=False)

    # Ignore age column
    for col in cols[1:]:
        rows = col.findAll('div')
        curr_stats.append(float(rows[-1].text))

    return curr_stats


# Scrape for player's team
def scrape_player_team(driver, player, player_url_list):

    url = player_url_list[player]
    driver.get(url)
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, "lxml")

    info = soup.select('div.p-card__player-info')

    for i in info:
        team = i.findAll('a')

    team_url = 'https://www.rotowire.com'+team[0]['href']
    return team[0].text, team_url


# Scrape weekly game count
def scrape_player_weekly_games(driver, team_url):
    driver.get(team_url)

    # wait for page scripts to load
    time.sleep(1)
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, "lxml")

    curr_date = date.today()
    week_start = curr_date-timedelta((7+curr_date.weekday())%7)
    week_end = curr_date + timedelta((7+6-curr_date.weekday())%7)

    # Handle week that overlaps Dec and Jan
    year_start = week_start.strftime('%Y')
    year_end = week_end.strftime('%Y')

    counter = 0

    # Scrape upcoming games
    table = soup.select('div.news-feed__main')

    for t in table:
        rows = t.findAll('div', recursive=False)

        for row in rows:
            games = row.findAll('span')

            for game in games:
                game_str = game.text

                #Make the day zero-padded
                temp = game_str.split(' ')
                if len(temp[1])==1:
                    temp[1] = '0'+temp[1]

                #Force year since year not scraped
                if year_start == year_end or temp[0] == 'Dec':
                    game_str = temp[0]+' '+temp[1]+ ' ' + year_start
                else:
                    game_str = temp[0] + ' ' + temp[1] + ' ' + year_end

                d = datetime.strptime(game_str,'%b %d %Y')

                if d.date() >= week_start and d.date() <= week_end:
                    counter +=1

    # Check if any games this week already played
    played_table = soup.select('div.webix_ss_center > div > div.webix_column.align-l.webix_first>div')

    for row in played_table:
        played_str = row.text
        played_str = played_str + '/' + year_start
        d = datetime.strptime(played_str, '%m/%d/%Y')

        if d.date() >= week_start and d.date() <= week_end:
            counter += 1
        elif d.date() < week_start:
            break

    return counter


if __name__ == '__main__':

    if os.path.exists('player_url_list.json'):

        # Load JSON as dictionary
        with open('player_url_list.json', 'r') as file:
            player_list = json.load(file)

    dr = start_session()
    #initialize_player_list(dr,player_list)
    #test = scrape_player_team(dr,'Pascal Siakam',player_list)
    scrape_player_weekly_games(dr,'https://www.rotowire.com/basketball/team/toronto-raptors-tor')
    #all_projected_stats = {}
    #scrape_all_projected(dr, player_list, all_projected_stats)

