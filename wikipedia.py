# Author:nima daryabar
# Show a timezone table using wikipedia

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import re
import requests

# from scrape import webscraping
# from db import dbconnect


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
                print("Wrong database username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("No database")
            else:
                print(err)
        else:
            db_check = False
    """ 
        MySQLCursorBuffered can be useful in situations where multiple queries,
        with small result sets, need to be combined or computed with each other
        more info on: [https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorbuffered.html]
    """
    dbcursor = cnx.cursor(buffered=True)
    return cnx, dbcursor


# Check if table exist
def check_table_exist(dbcrs, tablename):
    t_exist_ans = False
    try:
        q = ('SELECT COUNT(*) FROM %s') % tablename
        dbcrs.execute(q)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            print("No table with this name")
        else:
            print(err.msg)
    else:
        t_exist_ans = True
    return t_exist_ans


def get_table_to_save(dbcurs):
    check_table = input("Create table(y/n): ")
    table_name = ""
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
                             "`UTC_DST` varchar(6),"
                             "PRIMARY KEY(`id`)) ENGINE=InnoDB" % table_name)
        # Table errors
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("table created")
            print()
    else:
        exist_tb = True
        while exist_tb:
            table_name = input("Enter table name: ")
            exist_table_ans = check_table_exist(dbcurs, table_name)
            if exist_table_ans:
                exist_tb = False
    return table_name, dbcurs


# save data into database
def save_in_database(cnxdb, dbcrsor, tb_name, sample_refinelist):
    func_works_correctly = False

    # insert data
    # notice: it will prevent duplicated data to insert to the table
    for citem in sample_refinelist:
        cid, cyear, cname, cprice, cmileage, ccity = citem
        cmileage = int(cmileage)

        # beacause our items are not a lot for ML part,
        # so for better result we distinguish seller cities to 'تهران' as 1
        # and 'دیگر شهرستان ها' as 2 and save them in citynamecode column in table
        if ccity == 'تهران':
            ccitycode = 1
        else:
            ccitycode = 2

        dbcrsor.execute('INSERT IGNORE INTO %s VALUES (\'%d\', \'%d\', \'%s\', \'%d\', \'%d\', \'%s\', \'%d\')' % (tb_name,
                                                                                                                    cid,
                                                                                                                    cyear,
                                                                                                                    cname,
                                                                                                                    cprice,
                                                                                                                    cmileage,
                                                                                                                    ccity,
                                                                                                                    ccitycode))
    cnxdb.commit()
    func_works_correctly = True
    return func_works_correctly


def fetch_all_data(dbcr, table_tofetch):
    print("fetch all data")
    check_fetch = False
    fquery = ('SELECT * FROM %s') % table_tofetch
    dbcr.execute(fquery)
    fetchresult = dbcr.fetchall()
    if fetchresult:
        check_fetch = True
    else:
        print("No record in table to fetch, please insert some data!")
    return check_fetch, fetchresult











print("https://www.wikipedia.org/")
print()

# URL to send request
wiki_url = 'https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
# Get response for the specific url
# res = webscraping(wiki_url)
res = requests.get(wiki_url)
print()

# Pars as html using bs4 lib
soup = BeautifulSoup(res.text, 'html.parser')
print(soup.title.text)

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

# print()
# print(timezone_list)
# print()

# for n in timezone_list:
#     print(n)
#     print

# connect to database
print()
print("Database")
print()

cnx_db, dbcursr = connect_to_db()
print()
# print(cnx_db)
# print()
# print(dbcursr)

# create table or get table name(from user)
tble_name, gettabledbcursr = get_table_to_save(dbcursr)

