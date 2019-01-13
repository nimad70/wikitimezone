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

""" tbody #1 - main table """
# print(wikitables[1])
# res1 = wikitables[1]
# print(res1.text)

""" tbody #2 """
# print(wikitables[0])
# res0 = wikitables[0]
# print(res0.text)

""" Find all tables with table tag """
wikitable = soup.findAll('table')
all_tr = wikitable[0].findAll('tr')
# print(all_tr)
# print
for t in all_tr:
    print
    print (t.text)

