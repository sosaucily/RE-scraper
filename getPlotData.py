# coding=utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import urllib2
import time
import re
import csv

def split_on_non_numeric(s):
    return filter(None, re.split(r'[a-zA-Z.]+', s))[0].replace(" ", "")

MAX_PAGES_PER_DISTRICT = 10
STARTING_PAGE = 1
plots = {}

districts = ['viii']#, 'v']

for d in districts:
    plots[d] = []

superbreak = False
district_check_count = 0

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--incognito')
options.add_argument("user-data-dir=/Users/jessesmith/Proj/scrape/inglatan/chromedata")
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(20)
driver.fullscreen_window()
domain = "https://ingatlan.com"
# driver.get("https://www.google.com/")
# time.sleep(10)
driver.get(domain)
time.sleep(20)
# base_link = "{0}/lista/elado+lakas+{1}-ker+30-70-mFt+60-120-m2+2-szoba-felett".format(domain, district)

# for page_counter in range(STARTING_PAGE, MAX_PAGES+1): # max 30 pages, starting at 1
    # if superbreak:
    #     break

    # Using this logic to only append the received plot data if we get data in this iteration for all districts.
    # interation_plot_data = {}
for district in districts:
    page_counter = STARTING_PAGE
    base_link = "{0}/szukites/elado+lakas+{1}-ker+30-90-mFt+50-150-m2+2-szoba-felett".format(domain, district)

    page_appendix = '?page={0}'.format(page_counter) if (page_counter > 1) else ''
    paginated_link = "{0}{1}".format(base_link, page_appendix)
    print ("\nrequesting page {0} - {1}".format(page_counter, paginated_link))

    driver.get(paginated_link)
    time.sleep(20)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");

    for page_counter in range(STARTING_PAGE, STARTING_PAGE+MAX_PAGES_PER_DISTRICT): # max 30 pages, starting at 1
        search_soup=BeautifulSoup(driver.page_source, 'html5lib')

        plot_cards = search_soup.findAll("div", class_="listing__card")
        print ("checking {0} cards on this page".format(len(plot_cards)))

        for card in plot_cards:
            try:
                plot_data = {}
                plot_data['url'] = "https://ingatlan.com/{0}".format(card.find("a", class_="listing__link")['href'])

                address_full = card.find("div", class_="listing__address").get_text()
                plot_data['address'] = address_full.split(',')[0].strip()
                plot_data['district'] = address_full.split(',')[1].split('.')[0].strip()

                plot_data['price'] = split_on_non_numeric(card.find("div", class_="price").get_text())
                plot_data['size'] = split_on_non_numeric(card.find("div", class_="listing__data--area-size").get_text())
                # plot_data['rooms'] = card.find("div", class_="listing__data--room-count").get_text()
            except:
                continue

            plots[district].append(plot_data)

        try:
            print("moving to page {0}".format(page_counter+1))
            driver.find_element_by_partial_link_text("VETKE").click();
        except:
            print("No next button, try next district")
            break

        page_counter += 1
        time.sleep(20)



        # End district loop

for district in districts:
    csv_file = open('flat_details_district_{0}.csv'.format(district), 'ab+')
    f = csv.writer(csv_file, delimiter='\t')

    print ("got a total of {0} plots".format(len(plots[district])))
    for plot in plots[district]:
        f.writerow([
                    plot["address"].encode('utf-8'), #address
                    plot["district"], #district
                    plot["url"], #ingatlan link
                    plot["size"], #size
                    "{0}000000".format(plot["price"]), #price of plot
                    # plot["rooms"], #sold by
                  ])

    csv_file.close()
