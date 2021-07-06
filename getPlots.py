from bs4 import BeautifulSoup
import urllib2
import time

MAX_PAGES = 20
plot_links = []

plot_links_file = open("plot_links.txt","w")


# This one is old, use the getPlotData one

# https://realestatehungary.hu/szukites/elado+lakas+vii-ker+xiii-ker{0} - apartments in 7th or 8th
# https://realestatehungary.hu/szukites/elado+telek+lakoovezeti-telek+ix-ker+v-ker+vi-ker+vii-ker+viii-ker+xiii-ker+ix-v-vi-vii-viii-xiii-ker{0} - plots anywhere
for page_counter in range(1, MAX_PAGES): # max 30 pages, starting at 1
    page_appendix = '?page={0}'.format(page_counter) if (page_counter > 1) else ''
    link = "https://realestatehungary.hu/szukites/elado+lakas+vii-ker+30-75-mFt+50-100-m2+2-szoba-felett{0}".format(page_appendix)
    print ("requesting {0}".format(link))
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    search_response = opener.open(link).read()

    soup = BeautifulSoup(search_response, "html5lib")

    req_plot_links = soup.findAll("a", class_="listing__link")

    if (len(req_plot_links) > 0):
        print ("appending {0} links".format(len(req_plot_links)))
        for a in req_plot_links:
            plot_links.append(a['href'])
            plot_links_file.write("https://realestatehungary.hu/{0}\n".format(a['href']))

    #Is there a next page
    next_page = soup.select('a[href^="{0}?page={1}"]'.format(link, page_counter+1))
    print (next_page)

    # if not (bool(next_page)):
    #     print("no next_page button")
    #     break
    if (page_counter == MAX_PAGES):
        print ("hit counter limit!")
        break

    time.sleep(10)

# print plot_links
print "Finished! got {0} links".format(len(plot_links))
plot_links_file.close()


