from bs4 import BeautifulSoup
import re

from scrape import webscraping


print("https://www.wikipedia.org/")
print
wiki_url = 'https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
res = webscraping(wiki_url)
wiki_text_page = res.text
# print(page)
# print page
print
wiki_soup = BeautifulSoup(wiki_text_page, 'html.parser')
# print(wiki_soup)


