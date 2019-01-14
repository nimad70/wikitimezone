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

# i = 1
# for tr in all_tr:
#     all_td = tr.find_all('td')
#     if all_td:
#         print("0", all_td[0])
#         print(all_td[0].text)
#         print
#         print("1", all_td[1])
#         print(all_td[1].text)
#         print
#         print("2", all_td[2])
#         print(all_td[2].text)
#         print
#         print("3", all_td[3])
#         print(all_td[3].text)
#         print
#         print("4", all_td[4])
#         print(all_td[4].text)
#         print
#         print("5", all_td[5])
#         print(all_td[5].text)
#         print
#         print("6", all_td[6])
#         print(all_td[6].text)
#         print
#         print("7", all_td[7])
#         print(all_td[7].text)
#         print
#         break
#         # for td in all_td:
#         #     print td
#         #     print(u''.join(td.text).encode('utf-8'))
#     i += 1
# save all_td[0,1,2,5,6]

_ = 0
timezone_list = []
for tr in all_tr:
    all_td = tr.find_all('td')
    if all_td:
        timezone = [all_td[0].text, all_td[1].text, all_td[2].text, all_td[5].text, all_td[6].text]
        timezone_list.append(timezone)
        _ += 1
        if _ > 4:
            break
print(timezone_list)
print
for n in timezone_list:
    print(n)
    print

