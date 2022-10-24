# File to scrape Rotowire and NBA.com for player and team statistics

import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


# Create browser session to access NBA.com
def start_session():
    service = Service('./chromedriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service = service,options=chrome_options)
    driver.get('https://www.nba.com/players')
    dropdown = 'div.Pagination_pageDropdown__KgjBU > div > label > div>select'
    dropdown = Select(driver.find_element(by=By.CSS_SELECTOR,value=dropdown))
    dropdown.select_by_index(0)

    page_source = driver.page_source


    return page_source


# get full list of NBA players from NBA.com
def get_player_list(driver,player_list):

    #res = requests.get('https://www.nba.com/players')
    soup = bs4.BeautifulSoup(driver, "lxml")
    table = soup.select("table[class=players-list]")

    for t in table:

        rows = t.findAll('tr')

        # Ignore header row
        for row in rows[1:]:
            cells = row.select('p')
            player_list.append(cells[0].text + ' ' + cells[1].text)



# get access to Rotowire
def get_page_access(browser):

    # check if successfully accessed Rotowire
    if browser.page.status_code == requests.codes.ok:
        print('success!')
        page_soup = BeautifulSoup(self.html,'lxml')
        return page_soup
    else:
        return None

# get player's projected stats
def scrape_projected(browser,player):
    page_html = get_page_access(browser)
    if page_html is None:
        print('Site access failed!')

    # Rotowire page successfully accessed
    else:
        #search_box = page_html.select('top-nav-section__search')
        tab = page_html.select("div[id=nbaStats] > div[id=webix_hs_center]> table")
        #tab = tab_div.select("div", {"id": "webix_hs_center"})

        #tds = page_html.find_all('td', {'class': 'webix_hcell align-r bg-black-squeeze'})
        print(tab)


        #search_box.select('input')['value'] = player
        #player_page = browser.submit(search_box,browser.page.url)





if __name__ == '__main__':

    player_list = []
    dr = start_session()
    get_player_list(dr,player_list)
    print(len(player_list))
