import mysql.connector
from mysql.connector import errorcode

class dbconnect:
    def __init__(self, username, password, host, dbname):
        self.username = username
        self.password = password
        self.host = host
        self.dbname = dbname
    
    def dbconnect(self):
        self.cnx = mysql.connector.connect(user=self.username,
                                          password=self.password,
                                          host=self.host,
                                          database=self.dbname)
        return self.cnx

