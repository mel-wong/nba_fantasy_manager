# File to scrape Rotowire and NBA.com for player and team statistics
import time

import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# Create browser session to access different stat websites
def start_session():
    service = Service('./chromedriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(service = service,options=chrome_options)

    return driver


# get full list of NBA players from NBA.com
def get_player_list(driver,player_list):

    driver.get('https://www.nba.com/players')
    dropdown = 'div.Pagination_pageDropdown__KgjBU > div > label > div>select'
    dropdown = Select(driver.find_element(by=By.CSS_SELECTOR,value=dropdown))
    dropdown.select_by_index(0)
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, "lxml")
    table = soup.select("table[class=players-list]")

    for t in table:

        rows = t.findAll('tr')

        # Ignore header row
        for row in rows[1:]:
            name = row.select('p')
            player_list.append(name[0].text + ' ' + name[1].text)



# get access to Rotowire
def get_page_access(browser):

    # check if successfully accessed Rotowire
    if browser.page.status_code == requests.codes.ok:
        print('success!')
        page_soup = BeautifulSoup(self.html,'lxml')
        return page_soup
    else:
        return None

# get player's projected stats from Roto
def scrape_projected(driver,player):

    # Checks if already on Rotowire site
    if driver.current_url is not None and 'rotowire' in driver.current_url:
        print('Already on rotowire')
    else:
        driver.get('https://www.rotowire.com')
        search_css = "#search-for-players"
        search_xpath = '/html/body/div/div/header/div[1]/div[2]/div[3]/div[1]/input'
        #input_element = driver.find_element(by=By.CSS_SELECTOR,value=search_css)
        input_element = driver.find_element(by=By.XPATH, value=search_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(input_element)
        actions.send_keys(player)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        #driver.execute_script('arguments[0].send_keys(player)',input_element)
        #input_element.click()
        #input_element.send_keys(player)
       # input_element.send_keys(Keys.ENTER)

        time.sleep(3)

        print(driver.current_url)




    search_css = "div[=nbaStats] > div[id=webix_hs_center]> table"






if __name__ == '__main__':

    player_list = []
    dr = start_session()
    scrape_projected(dr,'siakam')
    #get_player_list(dr,player_list)
    #print(player_list[0])
