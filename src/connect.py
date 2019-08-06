import mysql.connector
from mysql.connector import errorcode


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