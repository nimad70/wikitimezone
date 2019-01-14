# Author:nima daryabar
# Show a timezone table using wikipedia

from bs4 import BeautifulSoup
import re

from scrape import webscraping


print("https://www.wikipedia.org/")
print
""" URL to send request """
wiki_url = 'https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
""" Get response for the specific url """
res = webscraping(wiki_url)
# print(page)
print
""" Pars as html using bs4 lib """ 
soup = BeautifulSoup(res.text, 'html.parser')
print(soup.title.text)
# print(soup)

""" Find tables by class attribute 'wikitable' """
# wikitables = soup.find_all('table', attrs={'class': 'wikitable'})
# print(len(wikitables))
# print(wikitables)

# print(wikitables[0])
# res0 = wikitables[0]
# print(res0.text)

""" Find all tables with table tag """
wikitable = soup.findAll('tbody')
all_tr = wikitable[0].find_all('tr')

i = 1
soup.findAll()
timezone_dict = {}
for tr in all_tr:
    all_td = tr.find_all('td')
    if all_td:
        print("0", all_td[0])
        print("1", all_td[1])
        print("2", all_td[2])
        print("3", all_td[3])
        print("4", all_td[4])
        print("5", all_td[5])
        print("6", all_td[6])
        print("7", all_td[7])
        print
        break
        # for td in all_td:
        #     print td
        #     print(u''.join(td.text).encode('utf-8'))
    i += 1
