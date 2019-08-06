# Author:nima daryabar
# Show a timezone table using wikipedia

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import re
import requests


print()
print("https://www.wikipedia.org/")
print()

# URL to send request
wiki_url = 'https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
# Get response for the specific url
res = requests.get(wiki_url)

# Pars as html using bs4 lib
soup = BeautifulSoup(res.text, 'html.parser')
# print wikipedia page title
print(soup.title.text)
print()

# Find all tables with table tag
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

# counter to specify data limitation
_ = 0
# Making a timezone list
timezone_list = []
for tr in all_tr:
    all_td = tr.find_all('td')
    if all_td:
        timezone = [all_td[0].text, all_td[1].text, all_td[2].text, all_td[5].text, all_td[6].text]
        timezone_list.append(timezone)
        _ += 1
        if _ > 4:
            break

# just for checking timezone_list[]
# for timezone in timezone_list:
#     code, lat, coun, utc, dst = timezone
#     print("code: ", code)
#     print("lat: ", lat)
#     print("coun: ", coun)
#     print("utc: ", utc)
#     print("dst: ", dst)
#     print()
# print()

# connect to database
cnx_db, dbcursr = connect_to_db()
print()

# create table or get table name(from user)
tble_name, gettabledbcursr = get_table_to_save(dbcursr)

# Add or fetch data into/from database
check_to_continue_add_fetch = True
while check_to_continue_add_fetch:
    print()
    print("Want to Add data to table or Fetch data from table or quit?")
    
    # check if user import right answer(a/f), not anything else
    check_answer_add_fetch = True
    
    while check_answer_add_fetch:
        answer_add_fetch_quit = input("[a for Add data/f for Fetch data/q for quit] (a/f/q): ")
        
        # Add data to DB
        if answer_add_fetch_quit == 'a':
            # turn to false to not start the while loop for getting right answer(a/f)
            check_answer_add_fetch = False
            print()
            print("---------------------")
            print("You choose 'Add data'")
            print("---------------------")
            print()
            # notify user about extraction time
            print()
            print("It will takes a little time , please be patient, thanks!")
            print()
            print()
            answer = save_in_database(cnx_db, dbcursr, tble_name, timezone_list)
            
            # Tell user if data is added to DB correctly or not
            if answer:
                print("Data inserted correctly")
            else:
                print("Ops! Something goes wrong")

        # Fetch data from db
        elif answer_add_fetch_quit == 'f':
            # turn to false to not start the while loop for getting right answer(a/f)
            check_answer_add_fetch = False
            print()
            print("-----------------------")
            print("you choose 'fetch data'")
            print("-----------------------")
            print()
            checking_fetch_result, fetching_result = fetch_all_data(dbcursr, tble_name)
            print(fetching_result)

            if checking_fetch_result:
                for (id_, code, latlon, tzname, utcoffset, dstoffset) in fetching_result:
                    print("No.", id_)
                    print("Country code: ", code)
                    print("Latitude, longitude ±DDMM(SS)±DDDMM(SS): ", latlon)
                    print("TZ database name: ", tzname)
                    print("UTC offset ±hh:mm: ", utcoffset)
                    print("UTC DST offset ±hh:mm: ", dstoffset)
                    print("-----------------------")
                    print()
        
        # Quit all 
        elif answer_add_fetch_quit == 'q':
            check_to_continue_add_fetch = False
            break

        else:
            # not enter any a or f, ask again to enter the right answer
            print("> Wrong answer, enter again please!")
            print()
    print()
    print()
    print("--------------------------")
