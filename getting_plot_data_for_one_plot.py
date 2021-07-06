from bs4 import BeautifulSoup
import urllib2
import time
import re
import csv

def split_on_non_numeric(s):
    print (s)
    return filter(None, re.split(r'[a-zA-Z.]+', s))[0].replace(" ", "")

MAX_PAGES = 1
plots = []

csv_file = open('plot_details.csv', 'wb+')
f = csv.writer(csv_file, delimiter='\t')

# f.writerow(["addy", "url", "models"])

for page_counter in range(1, MAX_PAGES+1): # max 30 pages, starting at 1
    page_appendix = '?page={0}'.format(page_counter) if (page_counter > 1) else ''
    link = "https://ingatlan.com/lista/elado+telek+lakoovezeti-telek+ix-ker+v-ker+vi-ker+vii-ker+viii-ker+xiii-ker+ix-v-vi-vii-viii-xiii-ker{0}".format(page_appendix)
    print ("requesting {0}".format(link))
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(link,headers=hdr)
    search_response = urllib2.urlopen(req).read()


    search_soup = BeautifulSoup(search_response, "html5lib")

    req_plot_links = search_soup.findAll("a", class_="listing__link")

    if (len(req_plot_links) > 0):
        plot_data = {}

        for a in req_plot_links:
            plot_link = "https://ingatlan.com/{0}".format(a['href'])
            plot_data['url'] = plot_link

            print ("requesting {0}".format(plot_link))
            req = urllib2.Request(plot_link,headers=hdr)
            plot_info = urllib2.urlopen(req).read()

            plot_details_soup = BeautifulSoup(plot_info, "html5lib")

            district = split_on_non_numeric(plot_details_soup.find("div", class_="card listing").find("h1").get_text())
            plot_data['district'] = district

            plot_numbers = plot_details_soup.find_all("div", class_="listing-parameters")[0]
            lot_size_string = plot_numbers.find("div", class_="parameter-lot-size").find("span", class_="parameter-value").get_text()
            lot_size = split_on_non_numeric(lot_size_string)
            plot_data['lot_size'] = lot_size

            lot_price_string = plot_numbers.find("div", class_="parameter-price").find("span", class_="parameter-value").get_text()
            lot_price = split_on_non_numeric(lot_price_string)
            plot_data['lot_price'] = lot_price

            plots.append(plot_data)
            break

    #Is there a next page
    next_page = search_soup.select('a[href^="{0}?page={1}"]'.format(link, page_counter+1))

    if not (bool(next_page)):
        break
    if (page_counter == MAX_PAGES+1):
        print ("hit counter limit!")
        break


csv_file.close()
print (plots)
