import mysql.connector
from mysql.connector import Error

class Database:
    @staticmethod
    def crear_conexion():
        conexion = None
        try:
            conexion = mysql.connector.connect(
                host='localhost', 
                user='caritas',  
                password='caritas',  
                database='caritas',
                port=3307
            )
        except Error as e:
            print(f"Error: '{e}'")

        return conexion
