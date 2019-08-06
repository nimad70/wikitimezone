# Author:nima daryabar
# Show a timezone table using wikipedia

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import re
import requests


# Connect to database
def connect_to_db():
    # Turn db_check to false if user enters correct database info
    db_check = True
    while db_check:
        try:
            db_username = input("Enter Database username: ")
            db_password = input("Enter Database password: ")
            host = input("Enter Host: ")
            db_name = input("Enter Database name: ")
            cnx = mysql.connector.connect(user=db_username,
                                          password=db_password,
                                          host=host,
                                          database=db_name)
        # connection errors
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("> Wrong database username or password")
                print()
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("> No database")
                print()
            else:
                print("> ", err)
                print()
        else:
            db_check = False
    """ 
        MySQLCursorBuffered can be useful in situations where multiple queries,
        with small result sets, need to be combined or computed with each other
        more info on: [https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorbuffered.html]
    """
    dbcursor = cnx.cursor(buffered=True)
    return cnx, dbcursor


""" 
    Check if table exist
    return (t_exist_ans)
    t_exist_ans: True if table exists or False if table doesn't exist
"""
def check_table_exist(dbcrs, tablename):
    t_exist_ans = False
    try:
        query = ('SELECT COUNT(*) FROM %s') % tablename
        dbcrs.execute(query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            print("> No table with this name")
            print()
        else:
            print(err.msg)
            print()
    else:
        t_exist_ans = True
    return t_exist_ans


""" 
    create table or check if it already exicts
    return (table_name, dbcurs)
    table_name: table name asked from user to craete or check if it already exists
    dbcurs: cursor object
"""
def get_table_to_save(dbcurs):
    check_table = input("Create table(y/n): ")
    table_name = ""
    # user's attemps entering table name
    user_attemps = 0

    # If answer is yes 'y'
    if check_table == 'y':
        table_name = input("Enter table name to create: ")
        # check if table is already created
        try:
            # table definition: (id, country_code, latitude_longitude, TZ_database_name, UTC, UTC_DST)
            dbcurs.execute("CREATE TABLE %s ("
                             "`id` int(11) NOT NULL AUTO_INCREMENT,"
                             "`country_code` VARCHAR(5),"
                             "`latitude_longitude` VARCHAR(25),"
                             "`tz_db_name` VARCHAR(50),"
                             "`utc` VARCHAR(6),"
                             "`utc_dtc` varchar(6),"
                             "PRIMARY KEY(`id`), UNIQUE INDEX `tz_db_name` (`tz_db_name`)"
                             ") ENGINE=InnoDB" % table_name)
        # Table errors
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already exists.")
            else:
                print(err.msg)
        else:
            print("Table created")
            print()

    # if answer is no 'n'
    else:
        exist_tb = True
        bye = False

        # repeat utill user enters correct table name
        while exist_tb:

            user_attemps += 1
            # If user can't remeber the table name
            if user_attemps > 3:

                correct_y_n = True
                while correct_y_n:

                    # Check if user wants to continue entering table name
                    entering_ans = input("Finish entering names(y/n): ")
                    if entering_ans == 'y':
                        correct_y_n = False
                        exist_tb = False
                        print("Good luck!")
                        break

                    elif entering_ans == 'n':
                        if user_attemps > 6:
                            print("Sorry! you've tried a lot :) bye :D")
                            bye = True
                            break
                        correct_y_n = False
                        print("Seriously?! ok! -__-, one more time!")
                        print()

                    else:
                        print("Plz! (y/n)")
                        print()
                
                if bye:
                    break
                
                if not exist_tb:
                    break

            table_name = input("Enter table name: ")
            exist_table_ans = check_table_exist(dbcurs, table_name)
            if exist_table_ans:
                exist_tb = False
    return table_name, dbcurs


""" 
    save data into database
    func_works_correctly: True if data is added correctly 
    or False if there is a problem in adding data to DB
"""
def save_in_database(cnxdb, dbcrsor, tb_name, sample_list):
    func_works_correctly = False

    # insert data
    # notice: it will prevent duplicated data to insert to the table
    for timezone in sample_list:
        code, latlong, tz, utc, dst = timezone
        add_timezone = ("INSERT IGNORE INTO {} "
                        "(country_code, latitude_longitude, tz_db_name, utc, utc_dtc) "
                        "VALUES (%(country_code)s, %(latitude_longitude)s, %(tz_name)s, %(utc_offset)s, %(dst_offset)s)".format(tb_name))
        # table name and timezone info
        data_timezone = {
            'country_code': code,
            'latitude_longitude': latlong,
            'tz_name': tz,
            'utc_offset': utc,
            'dst_offset':dst,
        }
        #  Insert data
        dbcrsor.execute(add_timezone, data_timezone)

    cnxdb.commit()
    func_works_correctly = True
    return func_works_correctly


"""
   fetch data from database
   check_fetch: check if data is fetched or not(True/False)
   fetchresult: all data that is fetched from DB
"""
def fetch_all_data(dbcr, table_tofetch):
    print("Fetch all data")
    check_fetch = False
    fquery = ('SELECT * FROM {}'.format(table_tofetch))
    dbcr.execute(fquery)
    fetchresult = dbcr.fetchall()
    
    # True if data is fetched correctly
    if fetchresult:
        check_fetch = True
    # or False
    else:
        print("No record in table to fetch, please insert some data!")

    return check_fetch, fetchresult


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
