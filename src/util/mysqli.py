import mysql.connector
from mysql.connector import Error
from util.MySQLi import MySQLi

def execute(query):
    connection = MySQLi.get_instance().connect()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        MySQLi.get_instance().close()
    except Error as e:
        MySQLi.get_instance().close()
        print(f"The error '{e}' occurred")
        return False

def query(query):
    connection = MySQLi.get_instance().connect()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        MySQLi.get_instance().close()
        return result
    except Error as e:
        MySQLi.get_instance().close()
        print(f"The error '{e}' occurred")
        return False