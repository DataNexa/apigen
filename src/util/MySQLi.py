import mysql.connector

class MySQLi:

    _instance = None

    def __init__(self, host, user, password, database):
        if MySQLi._instance is None:
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.connection = None
            MySQLi._instance = self

    def connect(self):
        if self.connection is None:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            
    @staticmethod
    def get_instance(host=None, user=None, password=None, database=None):
        if MySQLi._instance is None:
            MySQLi(host, user, password, database)
        return MySQLi._instance
