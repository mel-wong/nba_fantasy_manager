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
    dropdown.select_by_index(1)
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

        if url is None:
            print(f'Cannot find {k}')


# get player's projected stats from Roto
def scrape_player_url(driver, player):

    # Checks if already on Rotowire site
    if driver.current_url is not None and 'rotowire' in driver.current_url:
        print('Already on rotowire')
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

    # Fixes issue with slightly differing names between Rotowire and NBA.com
    while 'search' in driver.current_url:

        # Accounts for periods in names
        if '.' in player:
            split_name = player.split('.')
            rev_name = ''.join(split_name)
            scrape_player_url(driver, rev_name)

        # Ignore third string which usually consists of Sr, Jr, I
        elif ' ' in player:
            split_name = player.split(' ')
            split_name.pop()
            rev_name = ' '.join(split_name)
            scrape_player_url(driver, rev_name)

        # Cannot find player
        else:
            break

    else:
        return driver.current_url


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
        curr_stats.append(rows[-1].text)

    return curr_stats


if __name__ == '__main__':

    if os.path.exists('player_url_list.json'):

        # Load JSON as dictionary
        with open('player_url_list.json', 'r') as file:
            player_list = json.load(file)

    # player_list = {}
    dr = start_session()
    #all_projected_stats = {}
    #scrape_all_projected(dr, player_list, all_projected_stats)
    scrape_player_current('Precious Achiuwa',player_list,dr)
