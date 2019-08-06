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
