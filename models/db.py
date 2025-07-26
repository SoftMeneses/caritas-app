import mysql.connector
from mysql.connector import Error

class Database:
    @staticmethod
    def crear_conexion():
        conexion = None
        try:
            conexion = mysql.connector.connect(
                host='localhost', 
                user='root',  
                password='mysql',  
                database='caritas',
                port=3306
            )
        except Error as e:
            print(f"Error: '{e}'")

        return conexion
